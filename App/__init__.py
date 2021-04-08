import sys
sys.path.append('.')
import time 
from flask import Flask,render_template
from flask import jsonify, request, url_for, redirect

from scripts.get_rpi_capteurs import load_measure_config_example, choose_one_measure
from scripts.get_rpi_capteurs import generate_alerteConfig,generate_measureBody,generate_measureHeader



app = Flask(__name__)
capteurs_data = []

@app.route('/')
def index():
    title = "eco-capt-bridge - Home"
    return render_template("index.html",title=title)

@app.route('/about',methods=['GET','POST'])
def about():
    title = "eco-capt-bridge - About"
    if request.method == "POST":
        _measureHeader = request.form["_measureHeader"]
        _measureBody = request.form["_measureBody"]
        _alerteConfig = request.form["_alerteConfig"]
        return redirect(url_for("ecocapt"))
    else : 
        # measure_config = load_measure_config_example()
        # one_measure = choose_one_measure(measure_config)
        # _measureHeader = generate_measureHeader(one_measure)
        # _measureBody = generate_measureBody(one_measure)
        # _alerteConfig = generate_alerteConfig(one_measure)
        
        # capteurs_data.extend([_measureHeader,_measureBody,_alerteConfig])    

        return render_template("about.html", title=title)
    
@app.route('/ecocapt', methods=['GET','POST'])
def ecocapt():
    title = "eco-capt-bridge - Data"
    if request.method == 'POST':
        data = request.get_json()
        data_json = jsonify(data)
        return render_template("ecocapt.html",title=title,data=data)
    else:
        return render_template("ecocapt.html",title=title)

