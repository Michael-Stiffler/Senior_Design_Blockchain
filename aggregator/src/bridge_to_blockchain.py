import contract_access
import os
from dotenv import load_dotenv

def get_enrollment_data(sens_id) :
    load_dotenv()
  #  print("Getting Enrollment Data : ", sens_id == 'HeAW6W3k')
    contract = contract_access.ContractAccess(os.getenv('CONTRACT_ADDRESS'))
  #  print(os.getenv('CONTRACT_ADDRESS'))
    key = contract.retrieve_enrollment_data(sens_id)
  #  print(key)
    return key

def get_sensor_data(sens_id, tag) :
    load_dotenv()
    contract = contract_access.ContractAccess(os.getenv('CONTRACT_ADDRESS'))
    merkle_root = contract.retrieve_sensor_data(sens_id,tag)
    return merkle_root

def store_sensor_data(sens_id, tag, data) :
    load_dotenv()
    contract = contract_access.ContractAccess(os.getenv('CONTRACT_ADDRESS'))
    hash = contract.store_sensor_data(sens_id,tag,data)
    return hash

def enroll_sensor_to_blockchain() :
    load_dotenv()
    file = open("flask-serv/enr.txt", "r")
    key = file.readline()
    sensor_id = file.readline()
    print(os.getenv('CONTRACT_ADDRESS'))
    contract = contract_access.ContractAccess(os.getenv("CONTRACT_ADDRESS"))
    hash_out = contract.store_enrollment_data(sensor_id,key)
    return


#0x6b3cb0082a61d1521afb3109d04699e5107d61e0d6827042832eed3698a74e234981ff07b502a87b15da8b9cfa720817ca71db1477290ed4ab52981a233305dd
#HeAW6W3k

# if __name__ == "__main__" : 
#     hash_out = enroll_sensor_to_blockchain()
#     print(hash_out)
#     
#     key1 = get_enrollment_data("HeAW6W3k")
#     key2 = get_enrollment_data("badinput")
# 
#     print(repr(key1))
#     print(repr(key2))
# 
#     store_sensor_data("HeAW6W3k", "tag1", "merkleroot1")
#     store_sensor_data("HeAW6W3k", "tag2", "merkleroot2")
# 
#     merkout1 = get_sensor_data("HeAW6W3k", "tag1")
#     merkout2 = get_sensor_data("HeAW6W3k", "tag2")
#     merkout3 = get_sensor_data("HeAW6W3k", "tag3")
# 
#     print(repr(merkout1))
#     print(repr(merkout2))
#     print(repr(merkout3))
    

