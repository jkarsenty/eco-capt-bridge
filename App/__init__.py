import sys
import os
import json
sys.path.append('./App')
import time 
import datetime as dt
from flask import Flask,render_template
from flask import jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from scripts.utils import detect_strptime

from scripts.get_rpi_capteurs import load_measure_config_example, choose_one_measure
from scripts.get_rpi_capteurs import generate_alertBody,generate_measureBody,generate_measureHeader

from scripts.tx_functions import createBridgeWallet, connectWeb3, generateContract, addAlertFunct, addMeasureFunct, setTechMasterAddress
from scripts.show_data_req_funct import addMeasurePost, addAlertPost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///sensors_data.db"
# Initialize Database
db = SQLAlchemy(app)

# Create Database Model
class SensorsData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=dt.datetime.utcnow)
        
    # Create fonction to return a string when we add something
    def __repr__(self):
        return "<Name %r>" % self.id

# Verify Env Variable exists
try :
    app.config["INFURA_ID"] = os.getenv("INFURA_ID")
    app.config["SEED"] = os.getenv("SEED")
    app.config["CONTRACT_ADRESS"] = os.getenv("CONTRACT_ADRESS")
    app.config["ABI"] = os.getenv("ABI")
    assert app.config["INFURA_ID"] != None and app.config["SEED"] != None
    assert app.config["CONTRACT_ADRESS"] != None and app.config["ABI"] != None
except :
    try :
        app.config["INFURA_ID"] = os.environ["INFURA_ID"]
        app.config["SEED"] = os.environ["SEED"]
        app.config["CONTRACT_ADRESS"] = os.environ["CONTRACT_ADRESS"]
        app.config["ABI"] = os.environ["ABI"]
        assert app.config["INFURA_ID"] != None and app.config["SEED"] != None
        assert app.config["CONTRACT_ADRESS"] != None and app.config["ABI"] != None
    except :
        print("error")
        assert False 


@app.route('/')
def index():
    title = "Eco-Capt-Bridge - Home"
    return render_template("index.html",title=title)

@app.route('/ownerPage', methods=['GET', 'POST'])
def ownerPage():
    title = "Eco-Capt-Bridge - Owner Page"
    if request.method == "POST":

        if "setTechMaster" in request.form:
            infura_id = app.config["INFURA_ID"]
            seed = app.config["SEED"]
            contract_address = app.config["CONTRACT_ADRESS"]
            abi_str = app.config["ABI"]
            web3 = connectWeb3(infura_id=infura_id)
            bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
            contract = generateContract(web3, contract_address, abi_str)

            _serviceId = int(request.form["serviceId"])
            _techMasterAddress = request.form["techMasterAdress"]

            setTechMasterAddress(
                web3=web3,
                contract=contract,
                addressFrom=bridgeAddress,
                private_key=private_key,
                _serviceId=_serviceId,
                _techMasterAddress=_techMasterAddress
            )
        return render_template("ownerPage.html", title=title)
    else:
        return render_template("ownerPage.html", title=title)

@app.route('/techMasterPage', methods=['GET', 'POST'])
def techMasterPage():
    title = "Eco-Capt-Bridge - techMasterPage"
    
    if request.method == "POST":
        if "bridgeAddress" in request.form:
            infura_id = app.config["INFURA_ID"]
            seed = app.config["SEED"]
            contract_address = app.config["CONTRACT_ADRESS"]
            abi_str = app.config["ABI"]
            web3 = connectWeb3(infura_id=infura_id)
            bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
            contract = generateContract(web3, contract_address, abi_str)

            _serviceId = int(request.form["serviceId"])
            _techMasterAddress = request.form["bridgeAddress"]

            setTechMasterAddress(
                web3=web3,
                contract=contract,
                addressFrom=bridgeAddress,
                private_key=private_key,
                _serviceId=_serviceId,
                _techMasterAddress=_techMasterAddress
            )
        return render_template("techMasterPage.html", title=title)
    else:
        return render_template("techMasterPage.html", title=title)

@app.route('/capteurs_v2',methods=['GET','POST'])
def capteurs_v2():
    title = "Eco-Capt-Bridge - Send Data"
    if request.method == "POST" :
        if "addMeasure" in request.form :
            return redirect(url_for("addMeasure"))
        elif "addAlert" in request.form:
            return redirect(url_for("addAlert"))
        
        elif "printMeasure" in request.form :
            return redirect(url_for("printMeasure"))
        elif "printAlert" in request.form :
            return redirect(url_for("printAlert"))

    else :
        return render_template("capteurs_v2.html", title=title)

@app.route('/addMeasure',methods=['GET','POST'])
def addMeasure():
    n=0
    infura_id = app.config["INFURA_ID"]
    seed = app.config["SEED"]
    contract_address = app.config["CONTRACT_ADRESS"]
    abi_str = app.config["ABI"]
    web3 = connectWeb3(infura_id=infura_id)
    bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
    contract = generateContract(web3, contract_address, abi_str)
    
    while n < 20:
        app.logger.info("Sending Data...")
        data = request.get_json()
        if data == None:
            measure_config = load_measure_config_example()
            one_measure = choose_one_measure(measure_config)
            _measureHeader = generate_measureHeader(one_measure)
            _measureBody = generate_measureBody(one_measure)
            _serviceId = 3
        else :
            _serviceId = data["_serviceId"]
            _measureHeader = data["_measureHeader"]
            _measureBody = data["_measureBody"]
        

        tx_hash = addMeasureFunct(
            web3=web3,
            contract=contract,
            bridgeAddress=bridgeAddress,
            private_key=private_key,
            _serviceId=_serviceId,
            _measureHeader=_measureHeader,
            _measurebody=_measureBody
            )
        app.logger.info("Data Sent to the Blockchain")
        time.sleep(30)
        try:
            web3.eth.waitForTransactionReceipt(tx_hash)
        except:
            time.sleep(30)
        n += 1

    return redirect(url_for("capteurs_v2"))

@app.route('/addAlert',methods=['GET','POST'])
def addAlert():
    infura_id = app.config["INFURA_ID"]
    seed = app.config["SEED"]
    contract_address = app.config["CONTRACT_ADRESS"]
    abi_str = app.config["ABI"]
    web3 = connectWeb3(infura_id=infura_id)
    bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
    contract = generateContract(web3, contract_address, abi_str)
 
    app.logger.info("Sending Alert...")
    data = request.get_json()
    if data == None:
        measure_config = load_measure_config_example()
        one_measure = choose_one_measure(measure_config)
        _alertBody = generate_alertBody(one_measure)
        _alertConfigId = 0
        _serviceId = 0
    else :
        _serviceId = data["_serviceId"]
        _alertConfigId = data["_alertConfigId"]
        _alertBody = data["_alertBody"]

    tx_hash = addAlertFunct(
        web3=web3,
        contract=contract,
        bridgeAddress=bridgeAddress,
        private_key=private_key,
        _serviceId=_serviceId,
        _alertConfigId = _alertConfigId,
        _alertBody=_alertBody
    )

    app.logger.info("Alert Sent to the Blockchain")
    time.sleep(20)
    try:
        web3.eth.waitForTransactionReceipt(tx_hash)
    except:
        time.sleep(30)

    return redirect(url_for("capteurs_v2"))

@app.route('/printMeasure',methods=['GET','POST'])
def printMeasure():
    app.logger.info("Show Measure")
    data = request.get_json()
    if data == None:
        measure_config = load_measure_config_example()
        one_measure = choose_one_measure(measure_config)
        _measureHeader = generate_measureHeader(one_measure)
        _measureBody = generate_measureBody(one_measure)

        resp = addMeasurePost(endpoint='printMeasure',_serviceId=0,_measureHeader=_measureHeader,_measureBody=_measureBody)
        data = resp.json()

    return jsonify(data)

@app.route('/printAlert',methods=['GET','POST'])
def printAlert():
    app.logger.info("Show Alert")
    data = request.get_json()
    if data == None:
        measure_config = load_measure_config_example()
        one_measure = choose_one_measure(measure_config)
        _alertBody = generate_alertBody(one_measure)

        resp = addAlertPost(endpoint='printAlert',_serviceId=0,_alertConfigId = 0,_alertBody=_alertBody)
        data = resp.json()

    return jsonify(data)


@app.route('/sensors', methods=['GET','POST'])
def sensors():
    title = title = "Eco-Capt-Bridge - Sensors Data"
    if request.method == "POST":
        data = request.get_json()
        if data == None:
            data = request.form
        humidity = data["humidity"]
        assert humidity != None
        temperature = data["temperature"]
        assert temperature != None
        timestamp= data["timestamp"]
        assert timestamp != None
        try:
            timestamp = detect_strptime(timestamp)
        except:
            return "THE DATE FORMAT IS NOT GOOD"          
        
        # Add to Database
        news_sensors_data = SensorsData(temperature=temperature,humidity=humidity,timestamp=timestamp)
        try :
            db.session.add(news_sensors_data)
            db.session.commit()
        except:
            return "<h1> ERROR WITH THE ADDING TO DATABASE <h1/>"

        return redirect(url_for("sensors")) # jsonify(data)
    else: 
        sensors_data = SensorsData.query.all()
        return render_template("sensors.html",title=title,sensors_data=sensors_data)

@app.route("/clearSensorsDb", methods=["GET","POST"])
def clearSensorsDb():
    title = title = "Eco-Capt-Bridge - Clear Database"
    if request.method == "POST":
        
        try:
            num_rows_deleted = db.session.query(SensorsData).delete()
            app.logger.info(num_rows_deleted)
            db.session.commit()
        except:
            db.session.rollback()

        return render_template("clearSensorsDb.html",title=title)
    else: 
        return render_template("clearSensorsDb.html",title=title)