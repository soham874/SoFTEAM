from flask import Flask, request
from Service.NewsAnalysis.RssConsumer import RssConsumer
import os, random, time, time, debugpy
from Common.log_config import get_logger

if os.environ["DEBUG_MODE"]== "true":
    print("Waiting for debugger to attach...")
    debugpy.listen(("0.0.0.0", 5678))  # Bind to all interfaces on port 5678
    debugpy.wait_for_client()  # Pause execution until the debugger is attached
    print("Debugger attached.")

app = Flask(__name__)

from Controller.analysis_endp import analysis_endp
from Controller.kite_util_endp import kite_util
from Controller.config_controller import config_handler
from Controller.rss_controller import rss_controller, init_scheduler

time.sleep((random.randint(1, 10) + os.getpid()) % 10)

log = get_logger(__name__)

app.register_blueprint(analysis_endp, url_prefix = '/analysis')
app.register_blueprint(kite_util, url_prefix = '/kite')
app.register_blueprint(config_handler, url_prefix = '/config')
app.register_blueprint(rss_controller, url_prefix = '/news')

init_scheduler(app, log)

@app.route('/health')
def health_check():
    return "200 OK"

@app.route('/', methods = ["GET"])
def upstox_code():
    return {'code':request.args.get('code')}, 200