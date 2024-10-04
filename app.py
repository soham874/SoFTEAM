from flask import Flask
from flask_apscheduler import APScheduler
from Service.NewsAnalysis.RssConsumer import RssConsumer

from Controller.analysis_endp import analysis_endp
from Controller.kite_util_endp import kite_util

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

rssConsumer = RssConsumer()

app.register_blueprint(analysis_endp, url_prefix = '/analysis')
app.register_blueprint(kite_util, url_prefix = '/kite')

@app.route('/health')
def health_check():
    return "200 OK"

@scheduler.task('interval', id='rss_news_analyser', seconds=10)
def refresh_feed():
    rssConsumer.fetch_feed()

if __name__ == '__main__':
    app.run(debug=True)