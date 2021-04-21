import datetime as dt


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

def convertFrequencyToSec(frequency:str):
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


## for 
