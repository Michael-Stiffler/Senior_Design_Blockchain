import eth_keys
import os
import shortuuid


class Enrollment():

    def __init__(self):
        self.PrivK = eth_keys.keys.PrivateKey(os.urandom(32))
        self.PubK = self.PrivK.public_key
        self.uuid = shortuuid.ShortUUID().random(length=8)

    def private_key_to_env(self):
        os.environ["PRIVATE_KEY_ENROLLMENT"] = str(self.PrivK)
        print(str(self.PrivK))

    def uuid_to_env(self):
        os.environ["UUID_ENROLLMENT"] = str(self.uuid)
        print(str(self.uuid))

    def public_key_and_uuid_to_file(self):
        file = open("enr.txt", 'w')
        file.write(str(self.PubK) + "\n")
        file.write(str(self.uuid))


en = Enrollment()
en.private_key_to_env()
en.uuid_to_env()
en.public_key_and_uuid_to_file()
