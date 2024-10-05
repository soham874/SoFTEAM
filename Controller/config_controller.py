from flask import Blueprint, request
import traceback
from Service import ConfigHandler
import Common.constants as serviceConst

config_handler = Blueprint('config_handler', __name__)

@config_handler.route('/taConfigParams' , methods = ['GET' , 'POST'])
def fetch_and_update_ta_config():
    try: 
        if request.method == 'POST':
            new_constants_data = request.get_json()
            ConfigHandler.update_new_data(serviceConst.TA_PARAM_FILE_PATH, new_constants_data)
        ConfigHandler.return_existing_data(serviceConst.TA_PARAM_FILE_PATH)
    except Exception as e:
        traceback.print_exc()
        return {"exception_message" : repr(e)}, 500

@config_handler.route('/rssConfigParams' , methods = ['GET' , 'POST'])
def fetch_and_update_rss__config():
    try: 
        if request.method == 'POST':
            new_constants_data = request.get_json()
            ConfigHandler.update_new_data(serviceConst.RSS_PARAM_FILE_PATH, new_constants_data)
        ConfigHandler.return_existing_data(serviceConst.RSS_PARAM_FILE_PATH)
    except Exception as e:
        traceback.print_exc()
        return {"exception_message" : repr(e)}, 500