"""
Every minute;
1. Fetch feed for all RSS URLs. Filter out feed data for last 30 min.
2. Maintain a cache with TTL of 60 min. If the current feed title does not exist in the cache, push it and add it to processinglist
3. Filter the processinglist to find unique titles
4. For each of this title, analyse the news

"""

from Common.log_config import get_logger
from Service import ConfigHandler
import feedparser
from newspaper import Article
import html, time
from expiring_dict import ExpiringDict

class RssConsumer:

    def __init__(self) -> None:
        self.log = get_logger(__name__)
        self.cache = ExpiringDict(900)
        pass

    def fetch_new_feed(self):
        url_list = ["https://www.businesstoday.in/rssfeeds/?id=home",
                    "https://rss.app/feeds/tgll9PXJFaUoCjGV.xml",
                    "https://www.livemint.com/rss/industry",
                    "https://www.livemint.com/rss/markets",
                    "https://www.livemint.com/rss/companies",
                    "https://www.business-standard.com/rss/markets-106.rss"]
        window_min = 60
        
        feed = []
        for url in url_list:
            self.log.debug(f"Fetching data from URL {url}")
            feedData = feedparser.parse(url)

            # if not 200 <= feedData.status < 300:
            #     raise Exception (f"Failed to fetch feed from RSS {url}")
            
            feed += feedData.entries

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
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    
    def prepare_feed_data(self):
        new_feed = self.fetch_new_feed()

        formatted_news = {}
        for item in new_feed:
            formatted_news[item.title] = {
                'title' : html.unescape(item.title),
                'published_date' : item.published,
                'text' : html.unescape(self.get_summary(item.links[0]['href']))
            }

        return formatted_news
