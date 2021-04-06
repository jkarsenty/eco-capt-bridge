import os
import sys
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('.env')
sys.path.append('.')

from dotenv import load_dotenv
from generate_hd_wallet import generate_hdwallet, generate_list_adresses_keys
from generate_web3_connection import (create_web3_connection,
                                      generate_ganache_url,
                                      generate_ropsten_url)


INFURA_ID = seed_phrase = os.getenv("INFURA_ID")
SEED = os.getenv("SEED")
MNEMONIC = os.getenv("MNEMONIC")

if __name__ == "__main__":

    ## get addresses ##
    hd_wallet = generate_hdwallet(mnemonic=MNEMONIC)
    account_infos = generate_list_adresses_keys(hd_wallet,2)

    account_1_infos = account_infos[0]
    account_1 = account_1_infos[0]
    private_key = account_1_infos[1]

    account_2 = account_infos[1][0] #address of 2nd account

    ## create web3 connections ##
    url = generate_ropsten_url(INFURA_ID)
    web3 = create_web3_connection(url)

    ## check ropsten eth is not none
    balance = web3.eth.getBalance(account_1)
    assert web3.fromWei(balance,"ether") > 0

    ## interact with smart contract ##
    
