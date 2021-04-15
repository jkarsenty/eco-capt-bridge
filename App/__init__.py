import sys
import os
import json
sys.path.append('./App')
import time 
from flask import Flask,render_template
from flask import jsonify, request, url_for, redirect

from scripts.get_rpi_capteurs import load_measure_config_example, choose_one_measure
from scripts.get_rpi_capteurs import generate_alertBody,generate_measureBody,generate_measureHeader
from scripts.request_functions import addMeasurePost, addAlertPost

from scripts.tx_functions import createBridgeWallet, connectWeb3, generateContract, addAlertFunct, addMeasureFunct

app = Flask(__name__)

app.config["INFURA_ID"] = os.getenv("INFURA_ID")
app.config["SEED"] = os.getenv("SEED")
app.config["CONTRACT_ADRESSE"] = os.getenv("CONTRACT_ADRESSE")
app.config["ABI"] = os.getenv("ABI")

@app.route('/')
def index():
    title = "eco-capt-bridge - Home"
    return render_template("index.html",title=title)


@app.route('/capteurs_v2',methods=['GET','POST'])
def capteurs_v2():
    title = "eco-capt-bridge - Capteurs Button"
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
    contract_address = app.config["CONTRACT_ADRESSE"]
    abi_str = app.config["ABI"]
    web3 = connectWeb3(infura_id=infura_id)
    bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
    contract = generateContract(web3, contract_address, abi_str)
    
    while n < 10:
        print("Sending Data...")
        data = request.get_json()
        if data == None:
            measure_config = load_measure_config_example()
            one_measure = choose_one_measure(measure_config)
            _measureHeader = generate_measureHeader(one_measure)
            _measureBody = generate_measureBody(one_measure)
            _serviceId = 0
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
        print("Data Sent to the Blockchain")
        try:
            web3.eth.waitForTransactionReceipt(tx_hash)
        except:
            time.sleep(60)
        n += 1

@app.route('/addAlert',methods=['GET','POST'])
def addAlert():
    n=0
    infura_id = app.config["INFURA_ID"]
    seed = app.config["SEED"]
    contract_address = app.config["CONTRACT_ADRESSE"]
    abi_str = app.config["ABI"]
    web3 = connectWeb3(infura_id=infura_id)
    bridgeAddress, private_key = createBridgeWallet(mnemonic=seed)
    contract = generateContract(web3, contract_address, abi_str)
 
    while n < 10:
        data = request.get_json()
        if data == None:
            measure_config = load_measure_config_example()
            one_measure = choose_one_measure(measure_config)
            _alertBody = generate_alertBody(one_measure)
            _serviceId = 0
        else :
            _serviceId = data["_serviceId"]
            _alertBody = data["_alerteConfig"]

        tx_hash = addAlertFunct(
            web3=web3,
            contract=contract,
            bridgeAddress=bridgeAddress,
            private_key=private_key,
            _serviceId=_serviceId,
            _alertBody=_alertBody
        )

        try:
            web3.eth.waitForTransactionReceipt(tx_hash)
        except:
            time.sleep(60)
        n += 1

@app.route('/printMeasure',methods=['GET','POST'])
def printMeasure():
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
    data = request.get_json()
    if data == None:
        measure_config = load_measure_config_example()
        one_measure = choose_one_measure(measure_config)
        _alerteConfig = generate_alertBody(one_measure)

        resp = addAlertPost(endpoint='printAlert',_serviceId=0,_alerteConfig=_alerteConfig)
        data = resp.json()

    return jsonify(data)


