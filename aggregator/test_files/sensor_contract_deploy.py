##################################################################

# pragma solidity ^0.4.18;

# contract sensor_enrollment {

#     struct packet {
#         string publickey;
#     }

#     mapping (address => packet) mapped_data;
#     address[] list_of_packets;

#     function add(address address_, string key) public {
#         packet storage location = mapped_data[address_];

#         location.publickey = key;
#         list_of_packets.push(address_) -1;
#     }

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


class SensorContractDeploy:

    def __init__(self):

        load_dotenv()
        ganache_url = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        abi = json.loads('[{"constant":true,"inputs":[],"name":"count","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"address_","type":"address"},{"name":"key","type":"string"}],"name":"add","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"address_","type":"address"}],"name":"get","outputs":[{"name":"","type":"address"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
        bytecode = "608060405234801561001057600080fd5b50610496806100206000396000f300608060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806306661abd1461005c57806336d6da5514610087578063c2bc2efc14610110575b600080fd5b34801561006857600080fd5b506100716101ff565b6040518082815260200191505060405180910390f35b34801561009357600080fd5b5061010e600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919291929050505061020c565b005b34801561011c57600080fd5b50610151600480360381019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506102d4565b604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200180602001828103825283818151815260200191508051906020019080838360005b838110156101c35780820151818401526020810190506101a8565b50505050905090810190601f1680156101f05780820380516001836020036101000a031916815260200191505b50935050505060405180910390f35b6000600180549050905090565b60008060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000209050818160000190805190602001906102669291906103c5565b506001808490806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050505050565b6000606060008060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002090508381600001808054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156103b45780601f10610389576101008083540402835291602001916103b4565b820191906000526020600020905b81548152906001019060200180831161039757829003601f168201915b505050505090509250925050915091565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061040657805160ff1916838001178555610434565b82800160010185558215610434579182015b82811115610433578251825591602001919060010190610418565b5b5090506104419190610445565b5090565b61046791905b8082111561046357600081600090555060010161044b565b5090565b905600a165627a7a72305820450b18dccd227c7ec55a175aeac51b7da411dd3d13deba16cd58e5ef5f427fd90029"

        self.contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

    def deploy_contract(self):
        tx_hash = self.contract.constructor().transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_recepit.contractAddress


cp = SensorContractDeploy()
contract_address = cp.deploy_contract()
print(contract_address)
