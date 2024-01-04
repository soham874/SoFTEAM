from flask import Flask, request
import Util.OHLCVdata as ohlcData
from datetime import datetime
import json

app = Flask(__name__)

# 1. volume(20) [vol > EMA]
# 2. RSI (last 5 days) [val > 70 or val < 30]
# 3. MACD, signal (12,26,9) last 3 days [crossover, side]
# 4. 200 days EMA [price crosses, side]
# 5. Regression channel data for 30 days (15 on either side) [close hits upper or lower channel, its position relative to median]

# 6. Pattern over last few days
# 7. Trend before pattern

def jsonify_df_object(df_object):
    return json.loads(df_object.to_json(orient='records', date_format='iso').replace('\\"', '"'))

@app.route('/health')
def health_check():
    return "200 OK"

@app.route('/getStockData', methods=['GET'])
def getStockData():
    # Get query parameters or use default values
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    symbol = request.args.get('symbol')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    return jsonify_df_object(ohlcData.generate_data(start_date,end_date,symbol)) 

if __name__ == '__main__':
    app.run(debug=True)