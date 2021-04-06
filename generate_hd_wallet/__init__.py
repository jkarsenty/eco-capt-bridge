import os
from dotenv import load_dotenv

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic, is_mnemonic
from typing import Optional,List
from pprint import pprint

## Mnemonic words seed
load_dotenv('.env')
MNEMONIC = os.getenv("MNEMONIC")

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