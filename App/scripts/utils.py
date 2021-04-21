import datetime as dt
from sqlalchemy import func
import numpy as np

## Text et Hexa ##
def stringToHex(stringValue):
    hexValue = ""
    for l in stringValue:
        hexValue += hex(ord(l))[2:]
    return '0x' + hexValue

def hexToString(hexValue):
    if hexValue[:2] == "0x":
        hexValue = hexValue[2:]
    stringValue =  bytes.fromhex(hexValue).decode("ASCII")
    return stringValue

## TIME ## 
def detect_strptime(timestamp):
    try :
        timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except:
        try:
            timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        except:
            try:
                timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d')
            except:
                assert False
    return timestamp

def convertFrequencyToSec(frequency:str)->int:
    nbTime = frequency.split(' ')[0]
    timeCode = frequency.split(' ')[1]
    if timeCode == "i":
        time_str = dt.datetime.strptime(nbTime, '%M')
    elif timeCode == "H":
        time_str = dt.datetime.strftime(nbTime,'%H')
    elif time_str == "":
        time_str = dt.datetime.strftime(nbTime,'%d')
    elif time_str == "":
        time_str = dt.datetime.strftime(nbTime,'%m')
    elif time_str == "":
        time_str = dt.datetime.strftime(nbTime,'%Y')
    return int(time_str.strftime('%S'))

def detectEachFrequency(dateLastQuery,frequency):
    dateLastQuery = dt.datetime.strptime(dateLastQuery,'%Y-%m-%d %H:%M:%S')
    now = dt.datetime.now()
    delay = dt.timedelta(seconds=frequency)
    if now - dateLastQuery > delay :
        return True
    else :
        return False

## Interroger base de données par tranche de sequence
def statsSensorsData(data_list):
    return np.max(data_list),np.min(data_list),np.mean(data_list),np.median(data_list)

def readSensorsDatabase(SensorsDatabase,date_from:str,date_to:str):
    sensors_data = SensorsDatabase.query.filter(SensorsDatabase.timestamp.between(date_from, date_to))
    return sensors_data

def getMaxValueSensors(db,SensorsDatabase):
    maxValue = db.session.query(func.max(SensorsDatabase.temperature)).scalar()
    return maxValue

def getMinValueSensors(db,SensorsDatabase):
    minValue = db.session.query(func.min(SensorsDatabase.temperature)).scalar()
    return minValue

def getMeanValueSensors(db,SensorsDatabase):
    meanValue = db.session.query(func.avg(SensorsDatabase.temperature)).scalar()
    return meanValue

def getMedianValueSensors(db,SensorsDatabase):
    # medianValue = db.session.query(func.median(SensorsDatabase.temperature)).scalar()
    medianValue = 0
    return medianValue
