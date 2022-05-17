import rsa
import uuid
import shortuuid
import json
import pycoin
from pycoin.ecdsa import generator_secp256k1, sign, verify
import hashlib, secrets

def SDEnc(dataIN, UEID, PubK):
    #data input with dividing character
    dataIN = dataIN.split("|")
    tempData = ""
    binData = ""
    enfile = open("enr.txt", 'w')
   
    dataOut = []
    print("Unique Sensor ID: " + str(UEID))
    for n in dataIN:
        n = str(n)
        #dataOut.append(rsa.encrypt(n.encode("utf8"), GetPubKey()))
        
    #sig = CreateID(20)
    
    EncData = {
        'SensorID': UEID,
        'Data': dataOut
    }
    PrivK = secrets.randbelow(generator_secp256k1.order())
    JSONdata = json.dumps(EncData) 
    ByteHash = hashlib.sha3_256(EncData.encode("utf8")).digest()
    HashInt = int.from_bytes(ByteHash, byteorder = "big")
    
    signature = sign(generator_secp256k1, PrivK, HashInt)
    
    enfile.close()
    
    return(EncData)
    

def CreateID(x):
    id = shortuuid.ShortUUID().random(length=x)
    return id


def GenerateKeys():
    (PubK, PrivK) = rsa.newkeys(2048)
    keyfile = open("key.txt", 'w')
    keyfile.writelines(str(PrivK.n))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.e))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.d))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.p))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.q))
    keyfile.close()
    
    keyfile2 = open("key2.txt", 'w')
    keyfile2.writelines(str(PubK.n))
    keyfile2.writelines('\n')
    keyfile2.writelines(str(PubK.e))

def GetPrivKey():
    file = open('key.txt', 'r')
    mathlist = file.readlines()
    n = int(mathlist[0])
    e = int(mathlist[1])
    d = int(mathlist[2])
    p = int(mathlist[3])
    q = int(mathlist[4])
    PrivK = rsa.PrivateKey(n, e, d, p, q)
    return PrivK

def GetPubKey():
    file = open('key2.txt', 'r')
    mathlist = file.readlines()
    n = int(mathlist[0])
    e = int(mathlist[1])
    PubK = rsa.PublicKey(n, e)
    return PubK

def SDDec (result):
    cipher = bytes.fromhex(result)
    DataOUT = rsa.decrypt(cipher, GetPrivKey())
    return DataOUT
    
    