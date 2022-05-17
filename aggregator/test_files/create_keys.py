# msg = dumps({
#     "glossary": {
#         "title": "example glossary",
#         "GlossDiv": {
#             "title": "S",
#             "GlossList": {
#                 "GlossEntry": {
#                     "ID": "SGML",
#                     "SortAs": "SGML",
#                     "GlossTerm": "Standard Generalized Markup Language",
#                     "Acronym": "SGML",
#                     "Abbrev": "ISO 8879:1986",
#                     "GlossDef": {
#                         "para": "A meta-markup language, used to create markup languages such as DocBook.",
#                         "GlossSeeAlso": ["GML", "XML"]
#                     },
#                     "GlossSee": "markup"
#                 }
#             }
#         }
#     }
# }).encode("utf8")

# signature = self.PrivK.sign_msg(msg)
# print('Message:', msg)
# print('Signature: [r = {0}, s = {1}, v = {2}]'.format(
#     hex(signature.r), hex(signature.s), hex(signature.v)))
# # ECDSA public key recovery from signature + verify signature
# # (using the curve secp256k1 + Keccak-256 hash)
# recoveredPubKey = signature.recover_public_key_from_msg(msg)
# print('Recovered public key (128 hex digits):', recoveredPubKey)
# print('Public key correct?', recoveredPubKey == self.PubK)
# valid = self.PubK.verify_msg(msg, signature)
# print("Signature valid?", valid)


import pycoin
import ecdsa
import eth_keys
import hashlib
import secrets
import os
from json import dumps


class CreateKeys():

    def __init__(self):
        self.PrivK = eth_keys.keys.PrivateKey(os.urandom(32))
        self.PubK = self.PrivK.public_key
        print(type(self.PrivK))

    def private_key_to_env(self):
        os.environ["PRIVATE_KEY_ENROLLMENT"] = str(self.PrivK)

    def public_key_to_file(self):
        file = open("enr.txt", 'a')
        file.writelines(str(self.PubK))


key = CreateKeys()
key.private_key_to_env()
key.public_key_to_file()
