## fonctions pour interagir avec le smart-contract (web3 connection hd wallet etc...)

import json
import os
import sys
#sys.path.append(".")
from pprint import pprint
from typing import List, Optional

# from App.scripts.generate_web3_connection import (create_web3_connection,
#                                                   generate_ganache_url,
#                                                   generate_ropsten_url)
from dotenv import load_dotenv

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic, is_mnemonic
from web3 import Web3

## Env variable
load_dotenv('.env')
INFURA_ID = os.getenv("INFURA_ID")
MNEMONIC = os.getenv("MNEMONIC")
SEED = os.getenv("SEED")


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

def generate_ganache_url()->str:
    return "HTTP://127.0.0.1:7545"

def generate_ropsten_url(infura_id:str=INFURA_ID):
    return f"https://ropsten.infura.io/v3/{INFURA_ID}"

def create_web3_connection(url:str)->Web3:
    web3 = Web3(Web3.HTTPProvider(url))
    assert web3.isConnected()
    return web3

    
if __name__ == "__main__":

    ## get addresses ##
    hd_wallet = generate_hdwallet(mnemonic=SEED)
    account_infos = generate_list_adresses_keys(hd_wallet,3)

    account_1_infos = account_infos[0]
    # print(account_infos)
    account_1 = account_1_infos[0]
    assert account_1 == "0x9F52Fd356973FAA3ECe41e99F37bf4F3bAEBd096"
    private_key = account_1_infos[1]

    account_2 = account_infos[1][0] # public address of 2nd account
    account_3 = account_infos[2][0]

    url = generate_ropsten_url(INFURA_ID)
    web3 = create_web3_connection(url)

    balance = web3.eth.getBalance(account_1)
    print(web3.fromWei(balance,"ether"))

    ## interact with smart contract ##
    def generate_transfer_data(web3:Web3,nonce:int,account_to:str,value:int,gas:int,gasPrice:int):
        tx_data = {
            "nonce":nonce,
            "to":account_to,
            "value":web3.toWei(value,"ether"),
            "gas":gas,
            "gasPrice":web3.toWei(gasPrice,"gwei")
        }
        return tx_data

    def make_signed_transaction(web3:Web3,tx_data:dict,private_key:str):
        return web3.eth.account.signTransaction(tx_data,private_key)

    old_contract_address = web3.toChecksumAddress("0x2Cc8051b857158761A04F33b0106679FCa42A8df")
    contract_address = web3.toChecksumAddress(
        "0x94cbd0d05363c877Ef5C942781f569c9Ba22c515")
    old_abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_service_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    abi_str = '[{"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "address", "name": "_customerAddress", "type": "address"}, {"internalType": "address", "name": "_prevContract", "type": "address"}, {"internalType": "uint64", "name": "_prevContractDate", "type": "uint64"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_alert", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "AlertReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ContractUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "bytes32", "name": "_header", "type": "bytes32"}, {"indexed": false, "internalType": "bytes32", "name": "_body", "type": "bytes32"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "MeasureReceive", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "uint256", "name": "_id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceElementUpdate", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "_message", "type": "string"}, {"indexed": false, "internalType": "address", "name": "_author", "type": "address"}], "name": "ServiceUpdate", "type": "event"}, {"inputs": [], "name": "_serviceIdCounter", "outputs": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_alertBody", "type": "bytes32"}], "name": "addAlert", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigCustomer", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint64", "name": "_dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "_dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "_codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "_valueAlert", "type": "bytes8"}], "name": "addAlertConfigLegislator", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes6", "name": "_macAddress", "type": "bytes6"}, {"internalType": "string", "name": "_description", "type": "string"}], "name": "addIot", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "bytes32", "name": "_measureHeader", "type": "bytes32"}, {"internalType": "bytes32", "name": "_measurebody", "type": "bytes32"}], "name": "addMeasure", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "bytes8", "name": "_version", "type": "bytes8"}, {"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "bytes8", "name": "_measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "_timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "_nbTime", "type": "uint8"}], "name": "addService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAlerts", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllAlertConfigs", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"internalType": "uint64", "name": "dateOn", "type": "uint64"}, {"internalType": "uint64", "name": "dateOff", "type": "uint64"}, {"internalType": "bytes8", "name": "codeAlert", "type": "bytes8"}, {"internalType": "bytes8", "name": "valueAlert", "type": "bytes8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.AlertConfig[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getAllMeasures", "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}, {"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getAllServices", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "IotIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getConfig", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "uint64", "name": "prevContractDate", "type": "uint64"}, {"internalType": "uint64", "name": "nextContractDate", "type": "uint64"}, {"internalType": "address", "name": "customerAddress", "type": "address"}, {"internalType": "address", "name": "prevContract", "type": "address"}, {"internalType": "address", "name": "nextContract", "type": "address"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.Config", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getIot", "outputs": [{"components": [{"internalType": "bytes6", "name": "mac", "type": "bytes6"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "internalType": "struct ClientContract.Iot[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_measureId", "type": "uint256"}], "name": "getMeasuresById", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "getOneService", "outputs": [{"components": [{"internalType": "bytes8", "name": "version", "type": "bytes8"}, {"internalType": "bytes8", "name": "measureType", "type": "bytes8"}, {"internalType": "bytes1", "name": "timeCode", "type": "bytes1"}, {"internalType": "uint8", "name": "nbTime", "type": "uint8"}, {"internalType": "bool", "name": "isActive", "type": "bool"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "address", "name": "bridgeAddress", "type": "address"}, {"internalType": "address", "name": "techMasterAddress", "type": "address"}, {"internalType": "address", "name": "legislatorAddress", "type": "address"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertConfigIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "alertIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "measureIdCounter", "type": "tuple"}, {"components": [{"internalType": "uint256", "name": "_value", "type": "uint256"}], "internalType": "struct Counters.Counter", "name": "IotIdCounter", "type": "tuple"}], "internalType": "struct ClientContract.Service", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_bridgeAddress", "type": "address"}], "name": "setBridgeAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_legislatorAddress", "type": "address"}], "name": "setLegislatorAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "address", "name": "_techMasterAddress", "type": "address"}], "name": "setTechMasterAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_alertConfigId", "type": "uint256"}], "name": "toggleAlertConfig", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "toggleContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}, {"internalType": "uint256", "name": "_iotId", "type": "uint256"}], "name": "toggleIOT", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_serviceId", "type": "uint256"}], "name": "toggleService", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    abi = json.loads(old_abi_str)
    contract = web3.eth.contract(address=contract_address, abi=abi)

    #pprint(contract.functions.getAllServices().call())

    ## Send transaction ##

    # get nonce
    nonce = web3.eth.getTransactionCount(account_1)

    #########################
    ## transaction details ##
    #########################
    tx_data_transfer = generate_transfer_data(web3,nonce,account_2,0.5,50000,10)

    tx_data = {
        'nonce': nonce,
        'gas': 5000000,
        'gasPrice': web3.toWei(10, 'gwei'),
    }

    ## setTechMasterAddress tx
    tx_data_setTechMaster_built = contract.functions.setTechMasterAddress(
        _serviceId=0,
        _techMasterAddress="0x9F52Fd356973FAA3ECe41e99F37bf4F3bAEBd096"
    ).buildTransaction(tx_data)
    # pprint(tx_data_setTechMaster_built)

    ## setBridgeAddress tx
    tx_data_setBridge_built = contract.functions.addAlert(
        0, 
        "0x9F52Fd356973FAA3ECe41e99F37bf4F3bAEBd096"
        ).buildTransaction(tx_data)
    pprint(tx_data_setBridge_built)

    ## addAlert tx
    tx_data_alert_built = contract.functions.addAlert(
        0,
        "0x30302e30312e3030303030323230323130343133313031373030303030303039"
    ).buildTransaction(tx_data)
    # pprint(tx_data_alert_built)


    ###############
    ## Signed tx ##
    ###############
    # signed_tx_transfer = make_signed_transaction(web3, tx_data_transfer, private_key=private_key)
    # signed_tx_techmaster = make_signed_transaction(web3=web3, tx_data=tx_data_setTechMaster_built, private_key=private_key)
    
    signed_tx_bridge = make_signed_transaction(web3, tx_data_setBridge_built, private_key=private_key)
    # signed_tx_alert = make_signed_transaction(web3, tx_data_alert_built, private_key=private_key)
    print(f"Signed Tx : {signed_tx_bridge}")

    #############
    ## Send tx ##
    #############
    # tx_hash_transfer = web3.eth.sendRawTransaction(signed_tx_transfer.rawTransaction)
    # tx_hash_techmaster = web3.eth.sendRawTransaction(signed_tx_techmaster.rawTransaction)
    tx_hash_bridge = web3.eth.sendRawTransaction(signed_tx_bridge.rawTransaction)
    print(f"Tx Hash : {web3.toHex(tx_hash_bridge)}")
    
    #web3.eth.waitForTransactionReceipt(tx_hash_techmaster)

    # print("\n***********************\n")

    # pprint(contract.functions.getAllServices().call())
