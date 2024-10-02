from flask import Blueprint, request
from Common.log_config import get_logger
from Service.KiteService import KiteService
import traceback

kite_util = Blueprint('kite_util', __name__)

kiteService = None

@kite_util.route('/login')
def kite_login():

    try:
        log = get_logger(__name__)
        totp = request.args.get('totp')

        log.info("Start Kite login process")
        kiteService = KiteService(totp)
        
        return {
            'message' : 'Auth headers fetched and cached successfully'
        }, 200
    
    except Exception as e:
        traceback.print_exc()
        return {"exception_message" : repr(e)}, 500