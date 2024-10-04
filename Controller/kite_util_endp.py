from flask import Blueprint, request
from Common.log_config import get_logger
from Service.Kite.KiteService import KiteService
import traceback

kite_util = Blueprint('kite_util', __name__)

@kite_util.route('/login')
def kite_login():
    try:
        global kiteService

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
    
@kite_util.route('/fetch-data')
def execute_get_calls():
    try:
        log = get_logger(__name__)

        extension = request.args.get('method')
        kiteService = KiteService()

        log.info(f"Getting data about {extension}")

        return kiteService.execute_method(extension), 200
    
    except Exception as e:
        traceback.print_exc()
        return {"exception_message" : repr(e)}, 500