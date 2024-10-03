from flask import Flask

from Controller.analysis_endp import analysis_endp
from Controller.kite_util_endp import kite_util

app = Flask(__name__)

app.register_blueprint(analysis_endp, url_prefix = '/analysis')
app.register_blueprint(kite_util, url_prefix = '/kite')

@app.route('/health')
def health_check():
    return "200 OK"

if __name__ == '__main__':
    app.run(debug=True)