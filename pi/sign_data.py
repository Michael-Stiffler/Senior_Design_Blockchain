from json import dumps
import eth_keys
import os
from dotenv import load_dotenv


def SignData(sensor_data, UUID):

    load_dotenv()
    data_split = sensor_data.split("|")
    data_list = []

    for data in data_split:
        data_list.append(str(data))

    msg = {
        "SensorID": UUID,
        "Data": data_list,
    }

    private_key = os.getenv("PRIVATE_KEY_ENROLLMENT").replace("0x", "")
    signature = eth_keys.datatypes.PrivateKey(bytes.fromhex(
        private_key)).sign_msg(dumps(msg).encode("utf8"))

    data_dict = {
        "message": msg,
        "sig": str(signature)
    }

    return data_dict
