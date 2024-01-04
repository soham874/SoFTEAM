from nsedt import equity as eq
import pandas as pd
import Common.constants as serviceConst

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
        print("No data found between the requested range, fetching and saving new data")
        new_data = __private_fetch_data(start_date, end_date, symbol)
        new_data.to_csv(fileName, index=False)
        result = new_data
    
    # if requested dataset is part of saved dataset, return the extracted result 
    elif (existing_data['Date'].iloc[0] <= start_date) & (existing_data['Date'].iloc[-1] >= end_date):
        print("Requested dataset already present as part of saved data, returning the same")
        result =  df[mask].copy()
    
    # if requested dataset is partially present, flush the old data and save a new one. Can be optimized later
    else:
        print(f"Dataset requested between {start_date} and {end_date}, but cached data present for {existing_data['Date'].iloc[0]} and {existing_data['Date'].iloc[-1]}. Hence flushing old data and saving new.")
        with open(fileName, 'w', newline=''):
            pass
        new_data = __private_fetch_data(start_date, end_date, symbol)
        new_data.to_csv(fileName, index=False)
        result =  new_data
    
    return result

def __private_fetch_data(start_date, end_date, symbol):
    print(f"Fetching data for Scripe {symbol} between dates {start_date} and {end_date} from NSE")
    new_data = eq.get_price(start_date, end_date, symbol)
    new_data['Date'] = pd.to_datetime(new_data['Date'], unit='ms')
    return new_data