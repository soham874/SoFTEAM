from flask import Flask
from flask_apscheduler import APScheduler
from Service.NewsAnalysis.RssConsumer import RssConsumer
import os, random, time, json

from Controller.analysis_endp import analysis_endp
from Controller.kite_util_endp import kite_util
from Controller.config_controller import config_handler

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

        @scheduler.task('interval', id='rss_news_analyser', seconds=30)
        def refresh_feed():
            print(f"New news length -> {json.dumps(rssConsumer.prepare_feed_data())}")