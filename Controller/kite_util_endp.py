from flask import Blueprint
from Common.log_config import get_logger
kite_util = Blueprint('kite_util', __name__)

@kite_util.route('/login')
def health_check():
    log = get_logger(__name__)
    log.info("Start Kite login process")
    return "200 OK"