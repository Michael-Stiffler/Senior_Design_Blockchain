import os
from asyncio.windows_events import NULL
from dotenv import load_dotenv
from hexbytes import HexBytes
import contract_access
from datetime import datetime
import struct
from aggregator import merk
import numpy as np
import bridge_to_blockchain

def verifyData(data) :
    print(data)
    signature = data[7]
    addr = HexBytes(signature)
    cp = contract_access.ContractAccess(123)
    BCout = cp.call(addr)

    BCsensID = BCout[0]
    BCdata = BCout[1]
    BCtime = float(BCout[2])

    if (len(BCsensID) < 1) :
        print("SQL TABLE MUST BE REBUILT, FATAL TAMPERING DETECTED")
        return data

    data_to_compare = []
    data_to_compare.append(data[0])
    data_to_compare.append(datetime.fromtimestamp(BCtime))
    for i in BCdata :
        data_to_compare.append(hex_to_float((i.hex())[0:8]))
    data_to_compare.append(BCsensID)
    data_to_compare.append((HexBytes.hex(addr))[2:])

    print(data_to_compare)

    print()

    for i in range(8) :
        if isinstance(data[i], datetime) :
            if (data[i].replace(second=0,microsecond=0) != data_to_compare[i].replace(second=0,microsecond=0)) :
                print("Validation failed at: " + str(i) + "\n    in data with signature: " + str(signature))
                print("Graphing with appropriate data.")
                return data_to_compare
        elif (data[i] != data_to_compare[i]) :
            print("Validation failed at: " + str(i) + "\n in    data with signature: " + str(signature))
            print("Graphing with appropriate data.")
            return data_to_compare


    print("Validation complete for data with signature: " + str(signature))
    print()
    return data

def validate_by_merkle (data) :
    # input of many pyodb rows.
    if len(data) == 0:
        return []
    # return will be a 2D list of lists following same data structure as given rows

    # binning data by tag - expected a list of a 2^n list of lists.... jesus
    found_tags = [] 
    binned_data = []
    invalid_indices = []

    #create bins of data by tagname
    for i in data :
        row = []
        for col in range(len(i)-1):
            row.append(i[col])
        if i[7] in found_tags:
            idx = found_tags.index(i[7])
            binned_data[idx].append(row)
        else :
            found_tags.append(i[7])
            binned_data.append([row])

    # compute merkle root for each bin
    for k in range(len(binned_data)) :
        bin = binned_data[k]
        merkle_root, ret_data, root_node = merk(bin)
        tag = found_tags[k]
       # print("data out from merkin: ", ret_data)
        print("Computed merkle root: ", merkle_root)
        print("for tag: ", tag)

        sens_id = bin[0][6]
        print(sens_id)
        
        merkle_on_blockchain = bridge_to_blockchain.get_sensor_data(sens_id,tag)

        # if merkle roots to not match, prepare to discard data
        if (merkle_on_blockchain != merkle_root) :
            print("Computed root for tag", tag, "does not match blockchain entry. Data discarded!" )
            invalid_indices.append(k)
    
    # discard invalid data
    for i in sorted(invalid_indices, reverse=True) :
        del binned_data[i]

    # dump bins into validated data for return
    valed_data = []
    for bin in binned_data :
        for row in bin : 
            valed_data.append(row)
    
    if len(valed_data) > 0 :
        nparr = np.array(valed_data)
        sorted_data = nparr[nparr[:,1].argsort()] 
        return sorted_data
    return []



def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_float(h) :
    return struct.unpack('!f', bytes.fromhex(h))[0]