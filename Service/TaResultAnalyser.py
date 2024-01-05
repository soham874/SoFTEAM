from Service import TaService
from Util import CommonUtils
from datetime import datetime, timedelta
import pandas as pd
import Common.constants as serviceConstants

def __private_add_analysis_fields(ta_data):

    return

def generate_analysis_results(symbol):

    # Get today's date
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=(365 + serviceConstants.CONSIDER_DAYS_FOR_TA_REPORT))).strftime("%Y-%m-%d")

    end_date = datetime.strftime(end_date, '%Y-%m-%d')

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    ta_data = CommonUtils.jsonify_df_object(TaService.perform_and_return_ta_data(start_date,end_date,symbol))[-serviceConstants.CONSIDER_DAYS_FOR_TA_REPORT:]

    __private_add_analysis_fields(ta_data)

    return {"Stock":symbol,"Data":ta_data}