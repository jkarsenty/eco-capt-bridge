## fonctions pour interagir avec le smart-contract (web3 connection hd wallet etc...)

import json
import os
import sys
from pprint import pprint
from typing import List, Optional

from dotenv import load_dotenv

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic, is_mnemonic
from web3 import Web3

############# Env Variables #############

load_dotenv('.env')
INFURA_ID = os.getenv("INFURA_ID")
MNEMONIC = os.getenv("MNEMONIC")
SEED = os.getenv("SEED")

############# HD WALLET #############

def generate_mnemonic_phrase(strength:int=128,language:str="english"):
    """ 
    strength : choose strength 128 (Default), 160, 192, 224 or 256
    language : choose language english (Default), french, italian, spanish, chinese_simplified, 
            chinese_traditional,japanese or korean
    """
    mnemonic = generate_mnemonic(language=LANGUAGE, strength=STRENGTH)
    return mnemonic

def generate_hdwallet(mnemonic:str= MNEMONIC,cryptocurrency=EthereumMainnet,passphrase:Optional[str]=None)->BIP44HDWallet:
    """[summary]
    Args:
        cryptocurrency (hdwallet.cryptocurrencies, optional): crypto of the wallet. Defaults to EthereumMainnet.
        mnemonic (str, optional): mnemonic phrase from where we generate the wallet. Defaults to MNEMONIC.
        passphrase (Optional[str], optional): Secret passphrase/password for mnemonic. Defaults to None.
    Returns:
        BIP44HDWallet : wallet generate from mnemonic
    """

    ## Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    ## Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=mnemonic, passphrase=passphrase
    )
    # print("Mnemonic:", bip44_hdwallet.mnemonic())

    ## Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    return bip44_hdwallet

def generate_list_adresses_keys(bip44_hdwallet:BIP44HDWallet,n_address:int)->List[str]:
    list_of_addresses_keys = []
    for address_index in range(n_address):
        ## Derivation from Ethereum BIP44 derivation path
        bip44_derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
        )
        ## Drive Ethereum HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)

        ## Append public and private key to the list
        list_of_addresses_keys.append((bip44_hdwallet.address(),bip44_hdwallet.private_key()))

        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()
        
    return list_of_addresses_keys

def createBridgeWallet(mnemonic:str):
    hd_wallet = generate_hdwallet(mnemonic=mnemonic)
    account_infos = generate_list_adresses_keys(hd_wallet,1)
    assert isinstance(account_infos,list)
    assert len(account_infos) == 1
    account_infos = account_infos[0]
    assert isinstance(account_infos,tuple)
    bridgeAddress = account_infos[0]
    private_key = account_infos[1]
    return bridgeAddress,private_key

############# WEB 3 #############

def generate_ganache_url()->str:
    return "HTTP://127.0.0.1:7545"

def generate_ropsten_url(infura_id:str=INFURA_ID):
    return f"https://ropsten.infura.io/v3/{INFURA_ID}"

def create_web3_connection(url:str)->Web3:
    web3 = Web3(Web3.HTTPProvider(url))
    return web3

def connectWeb3(infura_id:Optional[str]=None):
    if infura_id == None:
        url = generate_ganache_url()
    else:
        url = generate_ropsten_url(infura_id=infura_id)
    web3 = Web3(Web3.HTTPProvider(url))
    web3 = create_web3_connection(url)
    assert web3.isConnected()
    return web3

############# TRANSACTIONS #############
def generateContract(web3,contract_address:str,abi_str:str):
    contract_address = web3.toChecksumAddress(contract_address)
    abi = json.loads(abi_str)
    contract = web3.eth.contract(address=contract_address, abi=abi)
    return contract

def generate_tx_data_transfer(web3,addressFrom:str,addressTo:str,value:int,gas:int,gasPrice:int):
    nonce = web3.eth.get_transactionCount(addressFrom)
    tx_data_transfer = {
        "nonce":nonce,
        "to":addressTo,
        "value":web3.toWei(value,"ether"),
        "gas":gas,
        "gasPrice":web3.toWei(gasPrice,"gwei")
    }
    return tx_data_transfer

def generate_tx_data(web3, addressFrom:str):
    nonce = web3.eth.getTransactionCount(addressFrom)
    tx_data = {
        'nonce': nonce,
        'gas': 5000000,
        'gasPrice': web3.toWei(10, 'gwei'),
    }
    return tx_data

def make_signed_transaction(web3:Web3,tx_data:dict,private_key:str,bridgeAddress:str):
    return web3.eth.account.signTransaction(tx_data,private_key)


def setBridgeAddress(web3,addressFrom:str,_serviceId:int,bridgeAddress:str):
    tx_data = generate_tx_data(web3,addressFrom=addressFrom)
    tx_data_built = contract.functions.setBridgeAddress(_serviceId,
                                bridgeAddress).buildTransaction(tx_data)
    signed_tx = make_signed_transaction(web3, tx_data_built, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash

def setTechMasterAddress(web3,addressFrom:str,_serviceId:int,_techMasterAddress:str):
    tx_data = generate_tx_data(web3,addressFrom=addressFrom)
    tx_data_built = contract.functions.setTechMasterAddress(_serviceId,
                                _techMasterAddress).buildTransaction(tx_data)
    signed_tx = make_signed_transaction(web3, tx_data_built, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash


def addAlert(web3,bridgeAddress:str,_serviceId:int,_alertBody:str):
    tx_data = generate_tx_data(web3,addressFrom=bridgeAddress)
    tx_data_built = contract.functions.addAlert(
                _serviceId=_serviceId,
                _alertBody=_alertBody).buildTransaction(tx_data)

    signed_tx = make_signed_transaction(web3, tx_data_built, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash

def addMeasure(web3,bridgeAddress:str,_serviceId:int,_measureHeader:str, _measurebody:str):
    tx_data = generate_tx_data(web3,addressFrom=bridgeAddress)
    tx_data_built = contract.functions.addMeasure(
            _serviceId=_serviceId,
            _measureHeader=_measureHeader,
            _measurebody=_measurebody).buildTransaction(tx_data)

    signed_tx = make_signed_transaction(web3, tx_data_built, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash

if __name__ == "__main__":

    web3 = connectWeb3(infura_id=INFURA_ID)
    bridgeAddress, private_key = createBridgeWallet(mnemonic=SEED)
    _techMasterAddress = ""
    _ownerAddress = ""   
    # balance = web3.eth.getBalance(bridgeAddress)
    # print(web3.fromWei(balance,"ether"))

    # old_contract_address = "0x2Cc8051b857158761A04F33b0106679FCa42A8df"
    # old_abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    contract_address = "0x2Cc8051b857158761A04F33b0106679FCa42A8df" #"0x94cbd0d05363c877Ef5C942781f569c9Ba22c515"
    abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "uint256", "name": "_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceElementUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [], "name": "_serviceIdCounter", "outputs": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes6", "name": "_macAddress", "type": "bytes6"}, {"internalType": "string", "name": "_description", "type": "string"}], "name": "addIot", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "IotIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getConfig", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "uint64", "name": "prevContractDate", "type": "uint64"}, {"internalType": "uint64", "name": "nextContractDate", "type": "uint64"}, {"internalType": "address", "name": "customerAddress", "type": "address"}, {"internalType": "address", "name": "prevContract", "type": "address"}, {"internalType": "address", "name": "nextContract", "type": "address"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.Config", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getIot", "outputs": [{"components": [{"internalType": "bytes6", "name": "mac", "type": "bytes6"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.Iot[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "IotIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_alertConfigId", "type": "uint256"}], "name": "toggleAlertConfig", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "toggleContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_iotId", "type": "uint256"}], "name": "toggleIOT", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "toggleService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    contract = generateContract(web3,contract_address,abi_str)
    pprint(contract.functions.getAllServices().call())
    pprint(contract.functions.getOneService(0).call())
    ## tx data ##
    # tx_data_transfer = generate_tx_data_transfer(web3=web3,addressFrom=bridgeAddress,
    #                                     addressTo=account_2,value=0.5,gas=50000,gasPrice=10)
    tx_data = generate_tx_data(web3,bridgeAddress)

    ## send tx ##
    # tx_hash_bridge = setBridgeAddress(web3,_techMasterAddress,0,bridgeAddress)
    # print(f"Tx Hash : {web3.toHex(tx_hash_bridge)}")
    
    #web3.eth.waitForTransactionReceipt(tx_hash_techmaster)

    # print("\n***********************\n")
    # pprint(contract.functions.getAllServices().call())
