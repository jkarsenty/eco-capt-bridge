import sys
import os
sys.path.append('./App')
import time 
from flask import Flask,render_template
from flask import jsonify, request, url_for, redirect

from scripts.get_rpi_capteurs import load_measure_config_example, choose_one_measure
from scripts.get_rpi_capteurs import generate_alerteConfig,generate_measureBody,generate_measureHeader
from scripts.request_functions import addMeasurePost, addAlertPost
from scripts.generate_web3_connection import generate_ropsten_url, create_web3_connection
from scripts.generate_hd_wallet import generate_hdwallet,generate_list_adresses_keys


app = Flask(__name__)

app.config["INFURA_ID"] = os.getenv("INFURA_ID")
app.config["SEED"] = os.getenv("SEED")
app.config["ADDRESS_TECH_MASTER"] = ""
app.config["PRIVATE_KEY"] = ""
app.config["web3"] = None
app.config["contract"] = None

def connect_web3():
    INFURA_ID = app.config["INFURA_ID"]
    url = generate_ropsten_url(INFURA_ID)
    web3 = create_web3_connection(url)
    app.config["web3"] = web3
    return web3 

def create_wallet():
    SEED = app.config["SEED"]
    hd_wallet = generate_hdwallet(mnemonic=SEED)
    account_infos = generate_list_adresses_keys(hd_wallet,1)

    account_1_infos = account_infos[0]
    account_1 = account_1_infos[0]
    private_key = account_1_infos[1]
    app.config["ADDRESS_TECH_MASTER"] = account_1
    app.config["PRIVATE_KEY"] = private_key

def create_contract():
    contract_address = "0x523cadf901Eab4b5d235a9Ac9932392CEB4780c7"
    abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    abi = json.loads(abi_str)
    web3 = app.config["web3"]
    contract = web3.eth.contract(address=contract_address,abi=abi)
    app.config["contract"] = contract
    return contract

def get_serviceId():
    contract = app.config["contract"]
    num_service = len(contract.functions.getAllServices().call())
    return 0

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
    


@app.route('/addAlert',methods=['GET','POST'])
def addAlert():
    data = request.get_json()
    if data == None:
        measure_config = load_measure_config_example()
        one_measure = choose_one_measure(measure_config)
        _alerteConfig = generate_alerteConfig(one_measure)
        _serviceId = 0
    else :
        _serviceId = data["_serviceId"]
        _alerteConfig = data["_alerteConfig"]



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
        _alerteConfig = generate_alerteConfig(one_measure)

        resp = addAlertPost(endpoint='printAlert',_serviceId=0,_alerteConfig=_alerteConfig)
        data = resp.json()

    return jsonify(data)


