import rsa
import uuid
import shortuuid
import json

def SDEnc(dataIN, UEID):
    #data input with dividing character
    dataIN = dataIN.split("|")
    tempData = ""
    binData = ""
    (PubK, PrivK) = rsa.newkeys(2048)
    
    enfile = open("enr.txt", 'w')
    keyfile = open("key.txt", 'w')
    dataOut = []
    print("Unique Sensor ID: " + str(UEID))
    for n in dataIN:
        #n = int(n.replace(".0", "")) #3rd input slot vestigial from arduino parameters, i.e. 1.0 not needed
        # if n < 0:
        #     n = n + 2**16  #if negative
        #     tempData = format(n, "b").zfill(16)
        # else:
        #     tempData = format(n, "b").zfill(16)
        
        # n = round(float(n), 5)
        # n = format(n, ".5f")
        # length = len(str(n))
        # n = str(n)
        # while length < 11:
        #     n = '*' + n
        #     length += 1
        # binData += '|' + n 
        n = str(n)
        dataOut.append(rsa.encrypt(n.encode("utf8"), PubK))
    sig = CreateID(20)
    UEID = rsa.encrypt(UEID.encode("utf8"), PubK)
    EncData = {
        'Cleveland': UEID,
        'State': dataOut,
        'University': sig
    }
    #binData = sig + binData + '|' + UEID
    
    #(PubK, PrivK) = rsa.newkeys(2048)
    #EncData = rsa.encrypt(binData.encode("utf8"), PubK)
   
    
    keyfile.writelines(str(PrivK.n))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.e))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.d))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.p))
    keyfile.writelines('\n')
    keyfile.writelines(str(PrivK.q))
    #print(str(PrivK.p))
    
    enfile.close()
    keyfile.close()
    return(EncData)
    

def CreateID(x):
    id = shortuuid.ShortUUID().random(length=x)
    return id

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

def SDDec (result):
    cipher = bytes.fromhex(result)
    DataOUT = rsa.decrypt(cipher, GetPrivKey())
    return DataOUT
    