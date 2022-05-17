from encryptData import *
import rsa
import shortuuid

#data entry input example
dataIN = "4.8972974|-11.8278724|1.2726362|66.29288|28.000000"

#function returns cipher text, including unique ID
#Standard Data Encryption
encode = SDEnc(dataIN, CreateID(8))

#get private key from file key.txt
PrivK = GetPrivKey()
print(encode)
#test decryption
decry = SDDec(encode)
print(decry)


