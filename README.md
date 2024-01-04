A backend project to analyse data from the National Stock Exchange, to provide fundamental TA and recommendations on trade, with possibility to prepare and train models to predict stock trend. 

Based on [_nsedt_](https://github.com/pratik141/nsedt) module by pratik141 

## Current  Functionalities

Following table highlights the available endpoints, their details and examples.

Base URL for the service is as follows :-

```
https://nse-analyser.onrender.com/
```
Endpoint details are as follows

| Endpoint  | Request Type | Parameters | Description | Example |
| :---: | :---: | :---: |    :----:   |   :----:|
| /health | GET | N/A  | Tells if the service is running       |  https://nse-analyser.onrender.com/health  |
| /getStockData?start_date=yyyy-mm-dd&end_date=yyyy-mm-dd&symbol=xxx | GET | start_date, end_date, symbol  | Fetch Historic OHLCV data for a stock from NSE, based on start and end date and stock code       |  https://nse-analyser.onrender.com/getStockData?start_date=2023-06-02&end_date=2024-01-01&symbol=ITC  |
| /getStockTaData?start_date=yyyy-mm-dd&end_date=yyyy-mm-dd&symbol=xxx | GET | start_date, end_date, symbol  | Fetch calculated TA data for a stock from NSE, based on start and end date and stock code       |  https://nse-analyser.onrender.com/getStockData?start_date=2023-06-02&end_date=2024-01-01&symbol=ITC  |
| /taConfigParams | GET | N/A  | Fetch the config values that will be used to calculate TA data  |  https://nse-analyser.onrender.com/taConfigParams  |
| /taConfigParams | POST | JSON fetched from the above request with updated values as payload | Update the config values that will be used to calculate TA data  |  https://nse-analyser.onrender.com/taConfigParams  |=======

## Features

- Automatically persist historic data in CSV format, available for personal use out of the service too.
- Provides TA data for following :
    - Close
    - Close EMA
    - Volume
    - Volume EMA
    - % deviation b/n actual volume and average
    - MACD
    - MACD Signal
    - RSI
    - Best fit regression channel data

## Instructions to run in local

Install python on your system and run following commands in root directory
```
pip install -r requirements.txt
python app.py
```