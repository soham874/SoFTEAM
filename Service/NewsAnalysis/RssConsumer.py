"""
Every minute;
1. Fetch feed for all RSS URLs. Filter out feed data for last 30 min.
2. Maintain a cache with TTL of 60 min. If the current feed title does not exist in the cache, push it and add it to processinglist
3. Filter the processinglist to find unique titles
4. For each of this title, analyse the news

"""

from Common.log_config import get_logger
from Common import ConfigHandler
import feedparser
from newspaper import Article
import html
import random

class RssConsumer:

    def __init__(self) -> None:
        self.log = get_logger(__name__)
        pass

    def fetch_feed(self):
        url_list = ConfigHandler.return_existing_data_dict()['rss_urls']
        self.log.info(f"Fetching data from URLs {url_list}")
        return f"{url_list} -> {random.randint(0,999)}"
