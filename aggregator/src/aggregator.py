import os
import socket
import PyDbConn
import encryptData
from datetime import datetime
import datetime as dt
import json
import contract_access
from hexbytes import HexBytes
import struct
import eth_keys
from json import dumps
import shortuuid
import rootcomputer
import bridge_to_blockchain


def main():
    # Bundle size of how many data points we want to collect
    MAX_BUNDLE_SIZE = 256

    # every time we successfully get a valid piece of data this will go up
    input_recieved = 0

    # every time we successfully get a valid piece of data, we add the data to this array
    data_to_push = []

    # format of how send the data over the socket and the hostname of the socket
    FORMAT = "utf-8"
    HOST = socket.gethostbyname(socket.gethostname())  # Server IP or Hostname
    print(HOST)
    # Pick an open Port (1000+ recommended), must match the clients port
    PORT = 12345

    # init the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Socket created')

    # managing error exception, make sure the socket loads the host with the port correctly
    try:
        s.bind((HOST, PORT))
    except socket.error:
        print('Bind failed')

    # let the socket listen for messages
    s.listen(5)
    print('Socket awaiting messages')

    # if a message is sent, save the connection and address
    (conn, addr) = s.accept()
    print('Connected')

    # Primary Engine - Get Data, then HANDLE IT (currently commented to only do one transaction)
    # https://youtube.com/clip/Ugkxmg-3GFGdwX7o75-y8WuHeosru7OHZsy2
    # while True :
    while input_recieved < MAX_BUNDLE_SIZE:
        # recieve data, get current time
        data = conn.recv(1024).decode(FORMAT)
        date = datetime.now()

        if len(data) < 1:
            continue
        print(data)

        # return data confirm to pi's side
        reply = "Got: " + data
        conn.send(reply.encode(FORMAT))

        # data to JSON object, parse and collect data
        json_data = json.loads(data)

        # parse the data that was returned
        parsed_data = parse_data(json_data, date)

        # If the key wasn't returned from the blockchain or the timestamp was not fresh, then the piece of data we got was not valid
        # i.e. parse_data() returned an empty list, but if the length was greater than 0, we can append that piece of data from the sensor
        if len(parsed_data) != 0:
          #  print("true")
            data_to_push.append(parsed_data)
            input_recieved += 1

    tag = shortuuid.uuid()
    data_to_SQL(data_to_push, tag)

    merkle_root, ret_data, root_node = merk(data_to_push)
    print("data out from merkin: ", ret_data)
    data_to_BC(merkle_root, tag)
    # get sensor ID from first entry in pushing data
    sens_id = data_to_push[0][6]
    bridge_to_blockchain.store_sensor_data(sens_id, tag, merkle_root)
    data_to_push = []
    input_recieved = 0
  #  Indent all above for while true


######################## DATA TRANSFER FUNCTIONS ############################################################

# data_to_x Expects MxN list array, where each of M rows is a list of N entries corresponding to necessary data:
    # [Transaction_ID, Time, Temperature, Humidity, X_value, Y_value, Sensor_ID, Signature]
def data_to_SQL(datain, tag):
    for n in datain:
        PyDbConn.addEntry(n, tag)


def data_to_BC(merkle_root, tag):
    # Need to do this with Michael because idk what is ready and what isnt  -Alex
    print("Computed merkle root: ", merkle_root)
    print("for tag: ", tag)
    #cp = contract_access.ContractAccess(123)
    # for n in datain:
    #    timestamp = str(datetime.timestamp(n[1]))
    #    addr = HexBytes(n[7])
    #    sensorID = n[6]
    #    data = []
    #    for i in range(2, 6):
    #        test = HexBytes(float_to_hex(n[i]))
    #        print(test)
    #        data.append(test)
    #        # print(hex_to_float(HexBytes.hex(test)))
    #    tx_hash = (cp.transaction(addr, sensorID, data, timestamp))
    #    print(HexBytes.hex(tx_hash))
    #    cp.call(addr)


################################ DATA PROCESSING FUNCTIONS################################################################################

# parse single line of input JSON object to piece apart integers, return list of things in a defined manner.
# RETURN list in form:
#   [Transaction_ID, Time, Temperature, Humidity, X_value, Y_value, Sensor_ID, Signature] (order used in SQL)
def parse_data(data, date):
    signature = data["sig"]
    msg = data["message"]

    sensor_data = msg["Data"]
    sensID = msg["SensorID"]

    signature = signature.replace("0x", "")
    signature_ekeys = eth_keys.datatypes.Signature(bytes.fromhex(signature))

    msg = dumps(msg).encode("utf8")

  #  print("key comparison start")

    # Get the public key from the blockchain here
    returned_key_from_blockchain = bridge_to_blockchain.get_enrollment_data(
        sensID)

  #  print("test")

  #  # Get the key from the signature of the message that was sent
    recovered_public_key_from_data = signature_ekeys.recover_public_key_from_msg(
        msg)

    # Check that the returned key from the blockchain for that sensor id is equal to the key that is recovered from the data signature
    if(str(recovered_public_key_from_data) == returned_key_from_blockchain):

       #############
       # is the timestap fresh
       #############

        # calling verify message expects that the 0x in the hex value is removed, so that is done here
        public_key = returned_key_from_blockchain.replace("0x", "")

        # Create an eth_keys version of the key, turning the string of hex into bytes, then getting the hex from those bytes
        eth_public_key = eth_keys.datatypes.PublicKey(
            bytes.fromhex(public_key))

        # Check if this new eth_key version of the key can verify the message and signature that was sent
        if(eth_public_key.verify_msg(msg, signature_ekeys)):

            listed_data = []

            # Append the data from the message into an array
            listed_data.append("0x1234959329ILOVEBLOCKCHAINDATETEST")
            listed_data.append(date)
            listed_data.append(sensor_data[2])
            listed_data.append(sensor_data[3])
            listed_data.append(sensor_data[0])
            listed_data.append(sensor_data[1])
            listed_data.append(sensID)

            return listed_data

    if len(returned_key_from_blockchain) == 0:
        print("DATA NOT ACCEPTED: Sensor of ID ", sensID, "is not enrolled!")
    else:
        print("DATA NOT ACCEPTED: Message signature is invalid! Invalid message recieved from sensor of ID ", sensID)
    return []

# add the data together into single stringe, then compute and return the merkle root.


def merk(data):
    merklable_strings = []
    for i in data:
        buff = ""
        for j in i:
            if isinstance(j, datetime):
                # preventative measure for consistent root calculation, one would argue that 10 milliseconds is enough precision anyways.
                ftime = round(j.timestamp(), 2)
                buff += str(ftime)
            elif not isinstance(j, str):
                buff += str(j)
            else:
                buff += j
        merklable_strings.append(buff)

    return rootcomputer.computeMerkleRoot(merklable_strings)


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def hex_to_float(h):
    return struct.unpack('!f', bytes.fromhex(h[2:]))[0]


if __name__ == "__main__":
    main()
