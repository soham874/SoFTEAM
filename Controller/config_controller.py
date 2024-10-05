from flask import Blueprint, request
from Common.log_config import get_logger
from Service.Kite.KiteService import KiteService
import traceback

config_handler = Blueprint('config_handler', __name__)

@config_handler.route('/' , methods = ['GET' , 'POST'])
def fetch_and_update_config():
    try: 
        config_file = request.args.get('config_file_name')
        if request.method == 'POST':
            new_config_file = request.get_json()

    
    except Exception as e:
        traceback.print_exc()
        return {"exception_message" : repr(e)}, 500