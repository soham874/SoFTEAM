from Common import ConfigHandler
from flask import Blueprint, request, render_template
from Service.TA import OHLCVdata, TaService, Plotter, TaResultAnalyser
from datetime import datetime
import Util.CommonUtils as commonUtils
import plotly.io as pio
import json

analysis_endp = Blueprint('anys_endp', __name__)

@analysis_endp.route('/getStockData', methods=['GET'])
def getStockData():
    
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    symbol = request.args.get('symbol')
    
    return commonUtils.jsonify_df_object(OHLCVdata.generate_data(start_date,end_date,symbol)) 

@analysis_endp.route('/getStockTaData', methods=['GET'])
def getTaStockData():
    
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    symbol = request.args.get('symbol')
    
    return commonUtils.jsonify_df_object(TaService.perform_and_return_ta_data(start_date,end_date,symbol)) 

@analysis_endp.route('/taConfigParams', methods=['GET'])
def get_constants():
    return ConfigHandler.return_existing_data()

@analysis_endp.route('/taConfigParams', methods=['POST'])
def update_new_constants():
    new_constants_data = request.get_json()
    return ConfigHandler.update_new_data(new_constants_data)

@analysis_endp.route('/plotTaData', methods=['GET'])
def generate_plot():
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    symbol = request.args.get('symbol')
    
    result_dataset = TaService.perform_and_return_ta_data(start_date,end_date,symbol)
    #return Plotter.plot_data()
    fig_html = pio.to_html(Plotter.plot_data(result_dataset), full_html=False)

    return render_template("plot.html", plot=fig_html)

@analysis_endp.route('/generateTaResult', methods=['GET'])
def get_group_ta_result():
    symbolList = request.args.get('symbolList')

    #parsed_json_data = json.loads()
    return render_template("ta_analysis_result.html",json_data=json.dumps(TaResultAnalyser.generate_stock_analysis_data(symbolList)))
