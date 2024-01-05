import Service.OHLCVdata as OHLCVdata
import pandas as pd
import ta
import Common.constants as serviceConstants
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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
  
def __private_construct_regression_channel(processedStockDataList,reducedStockDataList, min_window=10, max_window=30):

    best_upper = None
    best_lower = None
    best_median = None
    best_window = None
    best_error = float('inf')
    
    for window_size in range(min_window, max_window):
        # Extract the last m2 rows from the OHLC data
        data_subset = reducedStockDataList.tail(window_size)

        # Extract features (X) and target (Y)
        X = np.arange(len(data_subset)).reshape(-1, 1)
        Y = data_subset['Close'].values

        # Fit a straight line through the dataset
        model = LinearRegression()
        model.fit(X, Y)

        # Predict Y values
        predictions = model.predict(X)

        # Calculate upper and lower bounds using Standard Deviation of +2 / -2
        upper_bound = predictions + 2 * np.std(Y - predictions)
        lower_bound = predictions - 2 * np.std(Y - predictions)

        # Calculate the error in the estimation
        error = np.sum((Y - predictions) ** 2)

        # Update the best band if the current window size has a lower error
        if error < best_error:
            best_upper = upper_bound
            best_lower = lower_bound
            best_median = predictions

            best_window = window_size
            best_error = error

    processedStockDataList['Regression Upper Band'] = np.concatenate(([None] * (processedStockDataList.shape[0] - len(best_upper)), best_upper))
    processedStockDataList['Regression Lower Band'] = np.concatenate(([None] * (processedStockDataList.shape[0] - len(best_lower)), best_lower))
    processedStockDataList['Regression Median'] = np.concatenate(([None] * (processedStockDataList.shape[0] - len(best_median)), best_median))

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
        'Open' :  reducedStockDataList['Open'],
        'High' : reducedStockDataList['High'],
        'Low' : reducedStockDataList['Low'], 
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

    __private_construct_regression_channel(processedStockDataList,reducedStockDataList)

    return processedStockDataList
