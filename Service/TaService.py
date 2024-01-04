import Service.OHLCVdata as OHLCVdata
import pandas as pd

def __private_convert_data_to_DOHLCV(nsedtData):

    # List to store the objects
    return pd.DataFrame({
        'Date': nsedtData['Date'],
        'Open': nsedtData['Open Price'],
        'High': nsedtData['High Price'],
        'Low': nsedtData['Low Price'],
        'Close': nsedtData['Close Price'],
        'Volume': nsedtData['Total Traded Quantity']
    })

def perform_and_return_ta_data(start_date,end_date,symbol):
    
    reducedStockDataList = __private_convert_data_to_DOHLCV(
        OHLCVdata.generate_data(start_date,end_date,symbol)
    )

    processedStockDataList = pd.DataFrame({
        'Date': reducedStockDataList['Date'],
        'Close': reducedStockDataList['Close'],
        'Volume': reducedStockDataList['Volume']
    })

    return processedStockDataList
