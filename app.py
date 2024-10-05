from flask import Flask, Response
from flask_apscheduler import APScheduler
from Service.NewsAnalysis.RssConsumer import RssConsumer
import os, random, time, json, time

from Controller.analysis_endp import analysis_endp
from Controller.kite_util_endp import kite_util
from Controller.config_controller import config_handler
import Common.constants as constants
from Service import ConfigHandler

app = Flask(__name__)

rssConsumer = RssConsumer()

app.register_blueprint(analysis_endp, url_prefix = '/analysis')
app.register_blueprint(kite_util, url_prefix = '/kite')
app.register_blueprint(config_handler, url_prefix = '/config')

@app.route('/health')
def health_check():
    return "200 OK"

time.sleep((random.randint(1, 10) + os.getpid()) % 10)

if not os.path.exists('lockfile'):
    with open('lockfile', 'w') as f:
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()

        cached_articles = []

        @scheduler.task('interval', 
                        id='rss_news_analyser', 
                        seconds=ConfigHandler.fetch_value_from_config(constants.RSS_PARAM_FILE_PATH,"feed_check_duration_sec"))
        def refresh_feed():
            new_articles = rssConsumer.prepare_feed_data()
            cached_articles.append(new_articles)
            print(f"New news length -> {len(new_articles)}")

        @app.route('/cached-articles')
        def get_cached_articles():

            def generate():
                while True:
                    if cached_articles and cached_articles[0]:
                        yield (json.dumps(cached_articles.pop(0))+"\n").encode('utf-8')
                    time.sleep(5)

            return Response(generate(), mimetype='text/event-stream')