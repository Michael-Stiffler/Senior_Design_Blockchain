###############################################################


# pragma solidity >=0.7.0 <0.9.0;

# contract Storage {

#     uint256 number;

#     function store(uint256 num) public {
#         number = num;
#     }

#     function retrieve() public view returns (uint256){
#         return number;
#     }
# }


###############################################################

import json
from web3 import Web3
from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('INFURA_API_KEY')
url = "https://ropsten.infura.io/v3/"
wallet = os.getenv('METAMASK_WALLET')
private_key = os.getenv('METAMASK_PRIV_KEY')

web3 = Web3(Web3.HTTPProvider(url + api_key))
nonce = web3.eth.getTransactionCount(wallet)
web3.eth.defaultAccount = wallet

abi = json.loads('[{"inputs": [], "name":"retrieve", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "num", "type": "uint256"}], "name": "store", "outputs": [], "stateMutability":"nonpayable", "type":"function"}]')
address = web3.toChecksumAddress(os.getenv('CONTRACT_ADDRESS'))


def main():

    contract = web3.eth.contract(address=address, abi=abi)

    send_data(contract)
    retrieve_data(contract)


def send_data(contract):

    contract = web3.eth.contract(address=address, abi=abi)

    transaction = contract.functions.store(10).buildTransaction({
        'from': wallet,
        'nonce': nonce
    })

    signed_txn = web3.eth.account.signTransaction(
        transaction, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    print(tx_hash)


def retrieve_data(contract):

    data = contract.functions.retrieve().call()
    print(data)


if __name__ == "__main__":

    main()
