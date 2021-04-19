import json
from typing import List
import random
import datetime as dt

def stringToHex(stringValue):
    hexValue = ""
    for l in stringValue:
        hexValue += hex(ord(l))[2:]
    return hexValue

def hexToString(hexValue):
    if hexValue[:2] == "0x":
        hexValue = hexValue[2:]
    stringValue =  bytes.fromhex(hexValue).decode("ASCII")
    return stringValue

def load_measure_config_example(path_measure_config="App/scripts/get_rpi_capteurs/measures_config.json"):
    with open(path_measure_config,"r") as f:
        measure_config = json.loads(f.read())
    return measure_config

def choose_one_measure(measure_config:List[dict]):
    one_measure = random.choice(measure_config)
    return one_measure 

def decrypt_data_sensors(data):
    temperature = data["temperature"]
    humidity = data["humidity"]
    timestamp = data["timestamp"]
    datetime_obj = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    # print(datetime_obj)
    timestamp = datetime_obj.strftime('%Y%m%d%H%M')
    # print(timestamp)

    return temperature, humidity, timestamp
    
def generate_one_measure(
    temperature:int,
    humidity:int,
    timestamp:str,
    version:str="00.01.00",
    measureType:str="SON_0001",
    timeCode:str="i",
    nbTime:str="001",
    idAlert:str="0002"
    ):
    
    one_measure = {
        "_measureHeader": {
            "version": version,
            "date": timestamp,
            "measureType":measureType ,
            "timeCode": timeCode,
            "nbTime": nbTime
        },
        "_measureBody": {
            "maxValue": "00000045",
            "minValue": "00000009",
            "meanValue": "00000026",
            "medianValue": "00000018"
        },
        "_alertBody": {
            "version": version,
            "idAlert": idAlert,
            "date": timestamp,
            "valueAlerte": "00000009"
        }
    }

    return one_measure


    

def generate_measureHeader(one_measure:dict)->str:
    _measureHeader = one_measure["_measureHeader"]
    version = _measureHeader["version"]
    date = _measureHeader["date"]
    measureType = _measureHeader["measureType"]
    timeCode = _measureHeader["timeCode"]
    nbTime = _measureHeader["nbTime"]
    
    _measureHeader_hex = "0x" + stringToHex(f"{version}{date}{measureType}{timeCode}{nbTime}")
    assert len(_measureHeader_hex) == 66
    return _measureHeader_hex

def generate_measureBody(one_measure:dict)->str:
    _measureBody = one_measure["_measureBody"]
    maxValue = _measureBody["maxValue"]
    minValue = _measureBody["minValue"]
    meanValue = _measureBody["meanValue"]
    medianValue = _measureBody["medianValue"]
    
    _measureBody_hex = "0x" + stringToHex(f"{maxValue}{minValue}{meanValue}{medianValue}")
    assert len(_measureBody_hex) == 66
    return _measureBody_hex


def generate_alertBody(one_measure: dict) -> str:
    _alertBody = one_measure["_alertBody"]
    version = _alertBody["version"]
    idAlerte = _alertBody["idAlerte"]
    date = _alertBody["date"]
    valueAlerte = _alertBody["valueAlerte"]
    
    _alerteConfig_hex = "0x" + stringToHex(f"{version}{idAlerte}{date}{valueAlerte}")
    assert len(_alerteConfig_hex) == 66
    return _alerteConfig_hex

