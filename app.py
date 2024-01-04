from flask import Flask, request
from Service import OHLCVdata, TaService, ConfigHandler
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
    
    return commonUtils.jsonify_df_object(OHLCVdata.generate_data(start_date,end_date,symbol)) 

@app.route('/getStockTaData', methods=['GET'])
def getTaStockData():
    
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    symbol = request.args.get('symbol')
    
    return commonUtils.jsonify_df_object(TaService.perform_and_return_ta_data(start_date,end_date,symbol)) 

@app.route('/taConfigParams', methods=['GET'])
def get_constants():
    return ConfigHandler.return_existing_data()

@app.route('/taConfigParams', methods=['POST'])
def update_new_constants():
    new_constants_data = request.get_json()
    return ConfigHandler.update_new_data(new_constants_data)

if __name__ == '__main__':
    app.run(debug=True)