## fonctions pour transformer les donnees mesurees et traitees pour leur donner le format hexa

def hexToString(hexValue):
    if hexValue[:2] == "0x":
        hexValue = hexValue[2:]
    stringValue =  bytes.fromhex(hexValue).decode("ASCII")
    return stringValue


def stringToHex(stringValue):
    hexValue = ""
    for l in stringValue:
        hexValue += hex(ord(l))[2:]
    return hexValue