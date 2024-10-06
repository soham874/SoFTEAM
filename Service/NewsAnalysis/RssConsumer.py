from Common.log_config import get_logger
from Service import ConfigHandler
import feedparser
from newspaper import Article
import html, time, json, requests, traceback, os
from expiring_dict import ExpiringDict
from bs4 import BeautifulSoup
import Common.constants as constants
from Common.config_reader import ConfigReader

class RssConsumer:

    def __init__(self):
        self.log = get_logger(__name__)
        self.log.setLevel(ConfigReader().get_config_from_env_or_file('LOGGING_LEVEL_CRON'))
        self.cache = ExpiringDict(
            ConfigHandler.fetch_value_from_config(constants.RSS_PARAM_FILE_PATH,"cache_ttl_sec")
        )
        pass

    def __fetch_resources(self,url):
        response = requests.request(
            method="GET",
            headers={
                "User-Agent": "insomnium/0.2.3-a"
            },
            url=url
        )
                
        if not 200 <= response.status_code < 400:
            raise Exception (f"Failed to fetch feed from RSS {url}")
        
        return response.text

    def fetch_new_feed(self):
        url_list = ConfigHandler.fetch_value_from_config(constants.RSS_PARAM_FILE_PATH,"rss_url_list")
        self.log.debug(f"List of URLs to fetch feed from -> {url_list}")
        window_min = ConfigHandler.fetch_value_from_config(constants.RSS_PARAM_FILE_PATH,"consider_window_article_min")
        
        feed = []
        for url in url_list:
            try:
                self.log.debug(f"Fetching data from URL {url}")

                response = self.__fetch_resources(url)
                feedData = feedparser.parse(response)

                for entry in feedData.entries:
                    entry.title_detail.base = url

                feed += feedData.entries

            except Exception:
                traceback.print_exc()

        self.log.debug(f"Fetched all RSS data from input URLs. Feed size -> {len(feed)}. Filtering fresh data in last {window_min} minutes.")

        current_timestamp = time.mktime(time.gmtime())
        window = window_min*60

        for i in range(len(feed)-1 , -1, -1):
            published_ts = time.mktime(feed[i].get('published_parsed'))
            if current_timestamp - published_ts > window:
                del feed[i]

        self.log.debug(f"Filtered fresh data. Feed size -> {len(feed)}. Filtering based on previous processed cache")
        for i in range(len(feed)-1 , -1, -1):
            if feed[i].title not in self.cache:
                self.cache[feed[i].title] = feed[i]
            else:
                del feed[i]

        self.log.debug(f"Filtering new list to remove duplicate data. Feed size -> {len(feed)}")

        return feed
    
    def get_summary(self,url):

        # Strategy 1
        article_html = self.__fetch_resources(url)
        article = Article('')
        article.set_html(article_html)

        article.parse()
        if article.text != '':
            return article.text
        
        # Strategy 2
        self.log.warning(f"Strategy Newspaper3K failed to create article for URL {url}, trying Beautiful Soup")
        soup = BeautifulSoup(article.html, 'html.parser')

        script_tags = soup.find_all('script', type='application/ld+json')

        article_body = None

        for script_tag in script_tags:
            try:
                data = json.loads(script_tag.string)
                if data.get('@type') == 'NewsArticle':
                    article_body = data.get('articleBody')
                    break 
            except json.JSONDecodeError:
                continue 
        
        if article_body:
            return article_body

        self.log.error(f"All extraction strategies failed for article {url}")   
        return None
    
    def prepare_feed_data(self):
        new_feed = self.fetch_new_feed()

        formatted_news = {}
        for item in new_feed:
            formatted_news[item.title] = {
                'source' : item.title_detail.base,
                'title' : html.unescape(item.title),
                'published_date' : item.published,
                'article_url' : item.links[0]['href'],
                'text' : html.unescape(self.get_summary(item.links[0]['href']))
            }

        # if not os.path.exists('Resources/news_dump.json'):
        #     with open("Resources/news_dump.json", 'w') as json_file:
        #         json.dump(formatted_news, json_file, indent=4)

        return formatted_news