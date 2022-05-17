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


import json
from web3 import Web3
from dotenv import load_dotenv
import os


class ContractDeploy:

    def __init__(self):

        load_dotenv()
        ganache_url = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        abi = json.loads('[{"constant":false,"inputs":[{"name":"id_","type":"string"},{"name":"key_","type":"string"}],"name":"StoreEnrollmentData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"id_","type":"string"}],"name":"RetrieveEnrollmentData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"}],"name":"RetrieveSensorData","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token_","type":"string"},{"name":"tag_","type":"string"},{"name":"data_","type":"string"}],"name":"StoreSensorData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        bytecode = "608060405234801561001057600080fd5b506108fe806100206000396000f300608060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806316e54de614610067578063454d36281461011657806352e7cf35146101f8578063d7f5740914610320575b600080fd5b34801561007357600080fd5b50610114600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610415565b005b34801561012257600080fd5b5061017d600480360381019080803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091929192905050506104a2565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101bd5780820151818401526020810190506101a2565b50505050905090810190601f1680156101ea5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561020457600080fd5b506102a5600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091929192905050506105b8565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156102e55780820151818401526020810190506102ca565b50505050905090810190601f1680156103125780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561032c57600080fd5b50610413600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610737565b005b60006001836040518082805190602001908083835b60208310151561044f578051825260208201915060208101905060208303925061042a565b6001836020036101000a038019825116818451168082178552505050505050905001915050908152602001604051809103902090508181600001908051906020019061049c92919061082d565b50505050565b606060006001836040518082805190602001908083835b6020831015156104de57805182526020820191506020810190506020830392506104b9565b6001836020036101000a03801982511681845116808217855250505050505090500191505090815260200160405180910390209050806000018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156105ab5780601f10610580576101008083540402835291602001916105ab565b820191906000526020600020905b81548152906001019060200180831161058e57829003601f168201915b5050505050915050919050565b6060600080836040518082805190602001908083835b6020831015156105f357805182526020820191506020810190506020830392506105ce565b6001836020036101000a0380198251168184511680821785525050505050509050019150509081526020016040518091039020846040518082805190602001908083835b60208310151561065c5780518252602082019150602081019050602083039250610637565b6001836020036101000a03801982511681845116808217855250505050505090500191505090815260200160405180910390209050806000018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156107295780601f106106fe57610100808354040283529160200191610729565b820191906000526020600020905b81548152906001019060200180831161070c57829003601f168201915b505050505091505092915050565b600080836040518082805190602001908083835b602083101515610770578051825260208201915060208101905060208303925061074b565b6001836020036101000a0380198251168184511680821785525050505050509050019150509081526020016040518091039020846040518082805190602001908083835b6020831015156107d957805182526020820191506020810190506020830392506107b4565b6001836020036101000a038019825116818451168082178552505050505050905001915050908152602001604051809103902090508181600001908051906020019061082692919061082d565b5050505050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061086e57805160ff191683800117855561089c565b8280016001018555821561089c579182015b8281111561089b578251825591602001919060010190610880565b5b5090506108a991906108ad565b5090565b6108cf91905b808211156108cb5760008160009055506001016108b3565b5090565b905600a165627a7a723058200ff014589279750bf7ca7b45db138e4af28061488e123bbb7f7f9916f0ded4800029"

        self.contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

    def deploy_contract(self):
        tx_hash = self.contract.constructor().transact()
        tx_recepit = self.web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_recepit.contractAddress


cp = ContractDeploy()
contract_address = cp.deploy_contract()
print(contract_address)