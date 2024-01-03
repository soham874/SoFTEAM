from nsedt import equity as eq
import pandas as pd
import logging as log
import Common.constants as serviceConst

# Configure the logging module
log.basicConfig(level=log.INFO)

def generate_data(start_date, end_date, symbol):

    fileName = serviceConst.BASEDIR/serviceConst.STOCK_INFO_FILE_PATH/f'{symbol}.csv'

    try:
        df = pd.read_csv(fileName, parse_dates=['Date'])
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Open Price', 'High Price', 'Low Price', 'Close Price','Prev Close Price', 'Total Traded Quantity', 'Total Traded Value','52 Week High Price', '52 Week Low Price', 'VWAP', 'Deliverable Volume', 'Deliverable Percent', 'Series'])

    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    existing_data = df.loc[mask]
    
    result = None
    # if dataset empty, fetch new data and save it to csv
    if existing_data.empty:
        log.info("No data found between the requested range, fetching and saving new data")
        new_data = fetch_data(start_date, end_date, symbol)
        new_data.to_csv(fileName, index=False)
        result = new_data
    
    # if requested dataset is part of saved dataset, return the extracted result 
    elif (existing_data['Date'].iloc[0] <= start_date) & (existing_data['Date'].iloc[-1] >= end_date):
        log.info("Requested dataset already present as part of saved data, returning the same")
        result =  df[mask].copy()
    
    # if requested dataset is partially present, flush the old data and save a new one. Can be optimized later
    else:
        log.info("Dataset requested between %s and %s, but cached data present for %s and %s. Hence flushing old data and saving new.",start_date,end_date,existing_data['Date'].iloc[0],existing_data['Date'].iloc[-1])
        with open(fileName, 'w', newline=''):
            pass
        new_data = fetch_data(start_date, end_date, symbol)
        new_data.to_csv(fileName, index=False)
        result =  new_data
    
    return result

def fetch_data(start_date, end_date, symbol):
    log.info("Fetching data for Scripe %s between dates %s and %s from NSE", symbol,start_date,end_date)
    new_data = eq.get_price(start_date, end_date, symbol)
    print(new_data)
    new_data['Date'] = pd.to_datetime(new_data['Date'], unit='ms')
    return new_data