from flask import Flask, request
import Service.OHLCVdata as ohlcData
from datetime import datetime
import Util.CommonUtils as commonUtils

app = Flask(__name__)

@app.route('/health')
def health_check():
    return "200 OK"

@app.route('/getStockData', methods=['GET'])
def getStockData():
    
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    symbol = request.args.get('symbol')
    
    return commonUtils.jsonify_df_object(ohlcData.generate_data(start_date,end_date,symbol)) 

if __name__ == '__main__':
    app.run(debug=True)