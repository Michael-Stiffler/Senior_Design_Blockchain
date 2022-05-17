##################################################################

# pragma solidity ^0.4.18;

# contract sensor_enrollment {

#     struct packet {
#         string publickey;
#     }

#     mapping (address => packet) mapped_data;
#     address[] list_of_packets;

# function add(address address_, string key) public {
#     packet storage location = mapped_data[address_];

#     location.publickey = key;
#     list_of_packets.push(address_) -1;
# }

#      function get(address address_) view public returns (address, string) {
#         packet storage location = mapped_data[address_];

#         return (address_, location.publickey);
#     }

#     function count() view public returns (uint) {
#         return list_of_packets.length;
#     }
# }

##################################################################


import json
from web3 import Web3
from dotenv import load_dotenv
import os


class SensorContractAccess:

    def __init__(self, contract_address):

        load_dotenv()
        ganache_url = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        abi = json.loads('[{"constant":true,"inputs":[],"name":"count","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"address_","type":"address"},{"name":"key","type":"string"}],"name":"add","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"address_","type":"address"}],"name":"get","outputs":[{"name":"","type":"address"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
        address = self.web3.toChecksumAddress(
            "0xeE1e7Ff00AE0237fE9f2958C5E5b7aFcD0AB1CD4")
        # address = web3.toChecksumAddress(contract_address)

        self.real_contract = self.web3.eth.contract(
            address=address,
            abi=abi
        )

    def transaction(self, addr, key):
        tx_hash = self.real_contract.functions.add(self.web3.toChecksumAddress(
            addr), key).transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

        tx_hash = self.real_contract.functions.add(self.web3.toChecksumAddress(
            addr), key).transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

    def call(self, addr):
        sensor = self.real_contract.functions.get(
            self.web3.toChecksumAddress(addr)).call()
        return sensor


cp = SensorContractAccess(123)
cp.transaction("0xDEE7796E89C82F36BAdd1375076f39D69FafE252", "123")
print(cp.call("0xDEE7796E89C82F36BAdd1375076f39D69FafE252"))
cp.transaction("0xEEE7796E89C82F36BAdd1375076f39D69FafE252", "321")
print(cp.call("0xEEE7796E89C82F36BAdd1375076f39D69FafE252"))
