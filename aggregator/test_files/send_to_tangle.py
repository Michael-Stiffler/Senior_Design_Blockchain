from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString

import json
import glob
import os
import string

api = Iota('http://localhost:14265')

# Generate a random address
address = Address.random()

# Get all files in a directory and find the newest created file
list_of_files = glob.glob('C:/Users/LK/Desktop/*')
latest_file = max(list_of_files, key=os.path.getctime)
_, filename = os.path.split(latest_file)
name = os.path.splitext(filename)[0].replace("-", "").replace("_", "")

# Convert integers to alphabets
dic = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E',
       '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J'}
output = []
for i in name:
    output.append(dic[i])
finalname = ''.join(output)

f = open(latest_file, 'r')
# Data read from the file and store into a variable
data = f.read()

# transcation object to be sent to the tangle
# Tag is the file name of the data file, i.e. date and time
tx = ProposedTransaction(
    address=Address(address),
    message=TryteString.from_unicode(json.dumps(data)),
    tag=Tag(finalname),
    value=0
)

tx = api.prepare_transfer(transfers=[tx])

result = api.send_trytes(tx['trytes'], depth=3, min_weight_magnitude=9)

print('Transaction sent to the tangle!')
