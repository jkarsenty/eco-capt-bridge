import os
import sys
import json
from web3 import Web3
from dotenv import load_dotenv
load_dotenv(".env")
sys.path.append(".")

from App.scripts.generate_hd_wallet import generate_hdwallet, generate_list_adresses_keys
from App.scripts.generate_web3_connection import generate_ganache_url,generate_ropsten_url,create_web3_connection

from pprint import pprint

INFURA_ID = os.getenv("INFURA_ID")
SEED = os.getenv("SEED")
MNEMONIC = os.getenv("MNEMONIC")

## get addresses ##
hd_wallet = generate_hdwallet(mnemonic=SEED)
account_infos = generate_list_adresses_keys(hd_wallet,2)

account_1_infos = account_infos[0]
# print(account_infos)
account_1 = account_1_infos[0]
private_key = account_1_infos[1]

account_2 = account_infos[1][0] #address of 2nd account

url = generate_ropsten_url(INFURA_ID)
web3 = create_web3_connection(url)
web3.eth.defaultAccount = account_1
print(web3.eth.defaultAccount)


balance = web3.eth.getBalance(account_1)
print(web3.fromWei(balance,"ether"))

## interact with smart contract ##
def generate_tx_data(web3:Web3,nonce:int,account_to:str,value:int,gas:int,gasPrice:int):
    tx_data = {
        "nonce":nonce,
        "to":account_to,
        "value":web3.toWei(value,"ether"),
        "gas":gas,
        "gasPrice":web3.toWei(gasPrice,"gwei")
    }
    return tx_data

def make_signed_transaction(web3:Web3,tx_data:dict,private_key:str):
    return web3.eth.account.signTransaction(tx,private_key)
    
contract_address = "0x523cadf901Eab4b5d235a9Ac9932392CEB4780c7"
abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
abi = json.loads(abi_str)
contract = web3.eth.contract(address=contract_address,abi=abi)

pprint(contract.functions.getAllServices().call())

# # Send transaction ##
# # get nonce
# nonce = web3.eth.getTransactionCount(account_1)
# # transaction details
# tx_data = generate_tx_data(nonce,account_2,0.25,2000000,50)
# signed_tx = make_signed_transaction(tx_data,private_key)

# tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# print(web3.toHex(tx_hash))

tx_hash = contract.functions.addAlert(0,"0x30302e30312e3030303030313230323130313031313031323030313530343430").transact()
print(tx_hash)

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


# # print(stringToHex("Hello"))
# # print(hexToString("48656c6c6f"))

# print(stringToHex("i"))