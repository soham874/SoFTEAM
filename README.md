A project to analyse data from the National Stock Exchange, to provide fundamental TA and recommendations on trade, with possibility to prepare and train models to predict stock trend. 

Based on [ _nsedt_](https://github.com/pratik141/nsedt) module by pratik141 

## Current  Functionalities

- Fetch Historic OHLCV data for a stock from NSE, based on start and end date and stock code. For eg :- Fetch data for ITC b/n 2023-06-02 and 2024-01-01
```
http://localhost:5000/getStockData?start_date=2023-06-02&end_date=2024-01-01&symbol=ITC
```

## Features

- Automatically persist historic data in CSV format, available for personal use out of the service too.

## Instructions to run in local

Install python on your system and run following commands in root directory
```
pip install -r requirements.txt
python app.py
```