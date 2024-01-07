from Service import TaService
from Util import CommonUtils
from datetime import datetime, timedelta
import pandas as pd
import Common.constants as serviceConstants
import time

def __private_add_analysis_fields(ta_data):

    return

def __private_generate_analysis_results_for_single_symbol(symbol):

    # Get today's date
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=(365 + CommonUtils.return_config_json_value(serviceConstants.CONSIDER_DAYS_FOR_TA_REPORT)))).strftime("%Y-%m-%d")

    end_date = datetime.strftime(end_date, '%Y-%m-%d')

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    ta_data = CommonUtils.jsonify_df_object(TaService.perform_and_return_ta_data(start_date,end_date,symbol))[-CommonUtils.return_config_json_value(serviceConstants.CONSIDER_DAYS_FOR_TA_REPORT):]

    __private_add_analysis_fields(ta_data)

    return {"Stock":symbol,"Data":ta_data}

def generate_stock_analysis_data(symbolListString):

    symbolList = symbolListString.split(',')

    result_set = []
    for symbol in symbolList:
        result_set.append(__private_generate_analysis_results_for_single_symbol(symbol))
        time.sleep(2)
        
    return result_set