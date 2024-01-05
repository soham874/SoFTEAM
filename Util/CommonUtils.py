import json
import Common.constants as serviceConstants

def jsonify_df_object(df_object):
    return json.loads(df_object.to_json(orient='records', date_format='iso').replace('\\"', '"'))

def return_config_json_whole():
    with open(serviceConstants.TA_PARAM_FILE_PATH, 'r') as json_file:
        return json.load(json_file)
    
def return_config_json_value(key):
    return return_config_json_whole()[key]