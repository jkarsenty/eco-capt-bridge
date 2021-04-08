import os
import sys

from web3 import Web3
from dotenv import load_dotenv

load_dotenv('.env')
sys.path.append('.')

INFURA_ID = seed_phrase = os.getenv("INFURA_ID")

def generate_ganache_url()->str:
    return "HTTP://127.0.0.1:7545"

def generate_ropsten_url(infura_id:str=INFURA_ID):
    return f"https://ropsten.infura.io/v3/{INFURA_ID}"

def create_web3_connection(url:str)->Web3:
    web3 = Web3(Web3.HTTPProvider(url))
    assert web3.isConnected()
    return web3