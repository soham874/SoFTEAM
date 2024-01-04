import Common.constants as serviceConst
from Model import ReducedStockData

def __private_convert_data_to_DOHLCV(nsedtData):

    # List to store the objects
    result_list = [ReducedStockData(row['Date'], row['Open Price'], row['High Price'], row['Low Price'], row['Close Price'], row['Total Traded Quantity'])
               for row in nsedtData.itertuples(index=False)]

    return result_list