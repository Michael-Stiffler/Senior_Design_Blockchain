
from datetime import datetime
import struct
from time import time
from hexbytes import HexBytes
import time
import numpy as np
#def float_to_hex(f):
#    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
#
#def hex_to_float(h) :
#    return struct.unpack('!f', bytes.fromhex(h[2:]))[0]
#
#test = float_to_hex(1512)
#print(test)
#print(HexBytes(test))
#
#print(hex_to_float(test)) 
#
#
#date = datetime.now() 
#
#print(type(date.timestamp()))
#
#time.sleep(1)
#
#print(date)
l = [1650181280.39, 1650181282.74, 1650181283.983, 1650181285.227, 1650185755.587, 1650185757.963, 1650185759.21, 1650185760.447, 1650186572.94, 1650186574.213, 1650186575.463, 1650186576.713, 1650186689.68, 1650186690.92, 1650186692.157, 1650186693.407, 1650188461.97, 1650188463.223, 1650188464.55, 1650188465.803]

print(all(l[i] <= l[i+1] for i in range(len(l) - 1)))
time = datetime.now()
print(round(1650188060.180771,2))
time = time.replace(microsecond=0)
print(time.timestamp())