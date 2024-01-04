import Common.constants as serviceConst

def __private_convert_data_to_DOHLCV(nsedtData):

    # List to store the objects
    result_list = []

    # Iterate over the DataFrame rows
    for row in nsedtData.iterrows():
        # Create a dictionary for each row
        obj = {
            'Date': row['Date'],
            'Open': row['Open Price'],
            'High': row['High Price'],
            'Low': row['Low Price'],
            'Close': row['Close Price'],
            'Volume': row['Total Traded Quantity']
        }
        
        # Append the dictionary to the result list
        result_list.append(obj)

    return result_list