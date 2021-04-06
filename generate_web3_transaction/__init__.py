def generate_tx_data(web3:Web3,nonce:int,account_to:str,value:int,gas:int,gasPrice:int):
    tx_data = {
        'nonce':nonce,
        'to':account_to,
        'value':web3.toWei(value,'ether'),
        'gas':gas,
        'gasPrice':web3.toWei(gasPrice,'gwei')
    }
    return tx_data

def make_signed_transaction(web3:Web3,tx_data:dict,private_key:str):
    return web3.eth.account.signTransaction(tx,private_key)