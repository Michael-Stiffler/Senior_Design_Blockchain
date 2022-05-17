##################################################################

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


from web3 import Web3
from dotenv import load_dotenv
import os
import json

class ContractAccess:

    def __init__(self, contract_address):

        load_dotenv()

        api_key = os.getenv('INFURA_API_KEY')
        url = "https://ropsten.infura.io/v3/"
        self.wallet = os.getenv('METAMASK_WALLET')
        self.private_key = os.getenv('METAMASK_PRIV_KEY')

        self.web3 = Web3(Web3.HTTPProvider(url + api_key))
        self.nonce = self.web3.eth.getTransactionCount(self.wallet)
        self.web3.eth.defaultAccount = self.wallet

        abi = json.loads('[{"constant":false,"inputs":[{"name":"id_","type":"string"},{"name":"key_","type":"string"}],"name":"StoreEnrollmentData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"id_","type":"string"}],"name":"RetrieveEnrollmentData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"}],"name":"RetrieveSensorData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"},{"name":"data_","type":"string"}],"name":"StoreSensorData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        address = self.web3.toChecksumAddress(contract_address)

        self.real_contract = self.web3.eth.contract(
            address=address,
            abi=abi
        )

    def store_sensor_data(self, token, tag, data):

        transaction = self.real_contract.functions.StoreSensorData(
            token, tag, data).buildTransaction({
                'from': self.wallet,
                'nonce': self.nonce,
                'gasPrice': web3.toWei('20', 'gwei'),
                'gas': '0'
            })

        gas = self.web3.eth.estimate_gas(transaction)
        transaction.update({'gas': gas})

        signed_txn = self.web3.eth.account.signTransaction(
            transaction, private_key=self.private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_hash

    def retrieve_sensor_data(self, token, tag):
        return self.real_contract.functions.RetrieveSensorData(
            token, tag).call()

    def store_enrollment_data(self, id_, key):

        transaction = self.real_contract.functions.StoreEnrollmentData(
            id_, key).buildTransaction({
                'from': self.wallet,
                'nonce': self.nonce,
                'gasPrice': web3.toWei('20', 'gwei'),
                'gas': '0'
            })

        gas = self.web3.eth.estimate_gas(transaction)
        transaction.update({'gas': gas})

        signed_txn = self.web3.eth.account.signTransaction(
            transaction, private_key=self.private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_hash

    def retrieve_enrollment_data(self, id_):
        return self.real_contract.functions.RetrieveEnrollmentData(
            id_).call()
