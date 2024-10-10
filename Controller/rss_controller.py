from flask import Response, render_template, Blueprint
from flask_apscheduler import APScheduler
from Service.NewsAnalysis.RssConsumer import RssConsumer
import os, time, json, time, traceback
from Service.Redis import get_dict, modify_with_lock, append_to_list, get_list
from datetime import datetime

import Common.constants as constants
from Service import ConfigHandler

rss_controller = Blueprint('rss_controller', __name__)

rssConsumer = RssConsumer()
feed_key = 'news-feed'

def init_scheduler(app, log):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    if not os.path.exists('lockfile'):
        log.info("Starting feed maintainance activity")
        with open('lockfile', 'w') as f:
            modify_with_lock(feed_key,None)
            @scheduler.task('interval', 
                            id='rss_news_analyser', 
                            seconds=ConfigHandler.fetch_value_from_config(constants.RSS_PARAM_FILE_PATH,"feed_check_duration_sec"))
            def refresh_feed():
                new_articles = rssConsumer.prepare_feed_data()

                if new_articles:

                    modify_with_lock(feed_key,new_articles)
                    log.info(f"Publishing {len(new_articles)} new articles")
                    
                    published_ts = datetime.now().isoformat()
                    for article in new_articles.values():
                        append_to_list(
                            'published-articles',{
                                'title' : article['title'],
                                'published_ts' : published_ts,
                                'article_link' : article['article_url']
                            }
                        )

@rss_controller.route('/cached-articles')
def get_cached_articles():

    def generate():
        batch_count = 0
        while True:
            batch_identifier = f"batch_{batch_count}"

            if get_dict(feed_key):
                #log.debug(f"publishing batch {batch_count}")
                yield (f"data:{json.dumps({'batch': batch_identifier, 'data': get_dict(feed_key)})}\n\n").encode('utf-8')
                modify_with_lock(feed_key,None)
                batch_count += 1
                
            time.sleep(1)
                    

    return Response(generate(), mimetype='text/event-stream')

@rss_controller.route('/fetch-published-articles')
def fetch_published_articles_list():
    try:
        return json.dumps(
            [json.loads(item) for item in get_list('published-articles')],
            indent=4
        ), 200
    except:
        traceback.print_exc()

@rss_controller.route('/live-news-feed')
def handle_rss_field():
    return render_template('rss_news_handler.html')  # Render your HTML file