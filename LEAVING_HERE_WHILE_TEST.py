#   CONTRACT ACCESS 
# 
# 
# 
# #################################################################

# pragma solidity ^0.4.18;

# contract sensor_enrollment {

#     struct sensor_info {
#         string merkle_root;
#     }

#     struct enrollment_info{
#         string key;
#     }

#     mapping(string => mapping(string => sensor_info)) tag_to_token;
#     mapping(string => enrollment_info) token_to_key;

#     function StoreSensorData(string token_, string tag_, string data_) public {
#         sensor_info storage location = tag_to_token[tag_][token_];
#         location.merkle_root = data_;
#     }

#     function RetrieveSensorData(string token_, string tag_) view public returns (string) {
#         sensor_info storage location = tag_to_token[tag_][token_];
#         return (location.merkle_root);
#     }

#     function StoreEnrollmentData(string id_, string key_) public {
#         enrollment_info storage location = token_to_key[id_];
#         location.key = key_;
#     }

#     function RetrieveEnrollmentData(string id_) view public returns (string){
#         enrollment_info storage location = token_to_key[id_];
#         return (location.key);
#     }
# }

##################################################################


import json
from web3 import Web3
from dotenv import load_dotenv
import os
from hexbytes import HexBytes


class ContractAccess:

    def __init__(self, contract_address):

        load_dotenv()
        ganache_url = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        abi = json.loads('[{"constant":false,"inputs":[{"name":"id_","type":"string"},{"name":"key_","type":"string"}],"name":"StoreEnrollmentData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"id_","type":"string"}],"name":"RetrieveEnrollmentData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"}],"name":"RetrieveSensorData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"},{"name":"data_","type":"string"}],"name":"StoreSensorData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        address = self.web3.toChecksumAddress(contract_address)

        self.real_contract = self.web3.eth.contract(
            address=address,
            abi=abi
        )

    def store_sensor_data(self, token, tag, data):
        tx_hash = self.real_contract.functions.StoreSensorData(
            token, tag, data).transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_hash

    def retrieve_sensor_data(self, token, tag):
        return self.real_contract.functions.RetrieveSensorData(
            token, tag).call()

    def store_enrollment_data(self, id_, key):
        tx_hash = self.real_contract.functions.StoreEnrollmentData(
            id_, key).transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_hash

    def retrieve_enrollment_data(self, id_):
        return self.real_contract.functions.RetrieveEnrollmentData(
            id_).call()


# cp.transaction("0xDEE7796E89C82F36BAdd1375076f39D69FafE252",
#                "ID123", [HexBytes('0x01234567890123456789012345678901'), HexBytes('0x01231567890123456789012345678901')], "Today")
# cp.call("0xDEE7796E89C82F36BAdd1375076f39D69FafE252")
# cp.transaction("0xEEE7796E89C82F36BAdd1375076f39D69FafE252",
#                "ID999", [HexBytes('0x01234567890123456789012345678901'), HexBytes('0x01231567890123456789012345678901')], "Tomorrow")
# cp.call("0xEEE7796E89C82F36BAdd1375076f39D69FafE252")
