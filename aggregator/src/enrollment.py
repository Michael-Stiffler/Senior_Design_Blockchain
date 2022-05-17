import os
import contract_access
from dotenv import load_dotenv


def enroll_sensor_to_blockchain():
    load_dotenv()
    file = open("src/enr.txt", "r")

    key = file.readline().replace("\n", "")
    sensor_id = file.readline()

    print(repr(sensor_id))
    print(os.getenv('CONTRACT_ADDRESS'))

    contract = contract_access.ContractAccess(os.getenv("CONTRACT_ADDRESS"))
    hash_out = contract.store_enrollment_data(sensor_id, key)

    print(hash_out)

    new_key = contract.retrieve_enrollment_data(sensor_id)

    print(repr(new_key))


enroll_sensor_to_blockchain()
