import json
from typing import List
import random

import json
import random

def load_measure_config_example(path_measure_config="App/scripts/get_rpi_capteurs/measures_config.json"):
    with open(path_measure_config,"r") as f:
        measure_config = json.loads(f.read())
    return measure_config

def choose_one_measure(measure_config:List[dict]):
    one_measure = random.choice(measure_config)
    return one_measure 
    
def generate_measureHeader(one_measure:dict)->str:
    _measureHeader = one_measure["_measureHeader"]
    version = _measureHeader["version"]
    date = _measureHeader["date"]
    measureType = _measureHeader["measureType"]
    timeCode = _measureHeader["timeCode"]
    nbTime = _measureHeader["nbTime"]
    return bytes(f"{version}{date}{measureType}{timeCode}{nbTime}")

def generate_measureBody(one_measure:dict)->str:
    _measureBody = one_measure["_measureBody"]
    maxValue = _measureBody["maxValue"]
    minValue = _measureBody["minValue"]
    meanValue = _measureBody["meanValue"]
    medianValue = _measureBody["medianValue"]
    return bytes(f"{maxValue}{minValue}{meanValue}{medianValue}")

def generate_alerteConfig(one_measure:dict)->str:
    _alerteConfig = one_measure["_alerteConfig"]
    version = _alerteConfig["version"]
    idAlerte = _alerteConfig["idAlerte"]
    date = _alerteConfig["date"]
    valueAlerte = _alerteConfig["valueAlerte"]
    return bytes(f"{version}{idAlerte}{date}{valueAlerte}")