import sys
sys.path.append('./App')
import time 
from flask import Flask,render_template
from flask import jsonify, request, url_for, redirect

from scripts.get_rpi_capteurs import load_measure_config_example, choose_one_measure
from scripts.get_rpi_capteurs import generate_alerteConfig,generate_measureBody,generate_measureHeader



app = Flask(__name__)
app.config['CAPTEURS_DATA'] = []

@app.route('/')
def index():
    title = "eco-capt-bridge - Home"
    return render_template("index.html",title=title)

@app.route('/capteurs',methods=['GET','POST'])
def capteurs():
    capteurs_data = app.config['CAPTEURS_DATA']
    title = "eco-capt-bridge - About"
    if request.method == "POST" :
        if "send_data" in request.form :
            measure_config = load_measure_config_example()
            one_measure = choose_one_measure(measure_config)
            _measureHeader = generate_measureHeader(one_measure)
            _measureBody = generate_measureBody(one_measure)
            _alerteConfig = generate_alerteConfig(one_measure)
            capteurs_data.extend([("_measureHeader",_measureHeader),("_measureBody",_measureBody),("_alerteConfig",_alerteConfig)]) 
        
        elif "init_data" in request.form :
            app.config['CAPTEURS_DATA'] = []

        return redirect(url_for("processpost"))
    else :         
        return render_template("capteurs.html", title=title)
    
@app.route('/processpost', methods=['GET','POST'])
def processpost():
    title = "eco-capt-bridge - Data"
    return render_template("processpost.html",title=title,data=app.config['CAPTEURS_DATA'])