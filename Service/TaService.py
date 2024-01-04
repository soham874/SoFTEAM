import Service.OHLCVdata as OHLCVdata
import pandas as pd
import ta
import Common.constants as serviceConstants
import json

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

# 1. volume(20) [vol > EMA]
# 2. RSI (last 5 days) [val > 70 or val < 30]
# 3. MACD, signal (12,26,9) last 3 days [crossover, side]
# 4. 200 days EMA [price crosses, side]
# 5. Regression channel data for 30 days (15 on either side) [close hits upper or lower channel, its position relative to median]

# 6. Pattern over last few days
# 7. Trend before pattern
def perform_and_return_ta_data(start_date,end_date,symbol):
    
    reducedStockDataList = __private_convert_data_to_DOHLCV(
        OHLCVdata.generate_data(start_date,end_date,symbol)
    )
    
    with open(serviceConstants.TA_PARAM_FILE_PATH, 'r') as json_file:
        constants_data = json.load(json_file)

    processedStockDataList = pd.DataFrame({
        'Date': reducedStockDataList['Date'],
        'Close': reducedStockDataList['Close'],
        'CloseEMA': ta.trend.ema_indicator(
            close=reducedStockDataList['Close'], 
            window=constants_data[serviceConstants.CLOSE_EMA_DURATION]),
        'Volume': reducedStockDataList['Volume'],
        'VolumeEMA' : ta.trend.ema_indicator(
            close=reducedStockDataList['Volume'], 
            window=constants_data[serviceConstants.VOLUME_EMA_DURATION]),
        'RSI' : ta.momentum.rsi(
            close=reducedStockDataList['Close'], 
            window=constants_data[serviceConstants.RSI_DURATION]),
        'MACD' : ta.trend.macd(
            close=reducedStockDataList['Close'], 
            window_fast= constants_data[serviceConstants.MACD_FAST], 
            window_slow= constants_data[serviceConstants.MACD_SLOW]),
        'MACDSignal' : ta.trend.macd_signal( 
            close=reducedStockDataList['Close'], 
            window_fast= constants_data[serviceConstants.MACD_FAST], 
            window_slow= constants_data[serviceConstants.MACD_SLOW], 
            window_sign= constants_data[serviceConstants.MACD_SIGNAL_LENGTH])
    })

    processedStockDataList["VolumeDeviation"] = (processedStockDataList["Volume"]-processedStockDataList["VolumeEMA"])*100/processedStockDataList["VolumeEMA"]

    return processedStockDataList
