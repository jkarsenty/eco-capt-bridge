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

