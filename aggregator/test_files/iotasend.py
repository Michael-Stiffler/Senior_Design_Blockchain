from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString

#devnet so set testnet = true
api = Iota('https://nodes.devnet.iota.org:443', testnet=True)

#api = Iota('http://71.64.99.46:443')
#random address
address = 'ZLGVEQ9JUZZWCZXLWVNTHBDX9G9KZTJP9VEERIIFHY9SIQKYBVAHIMLHXPQVE9IXFDDXNHQINXJDRPFDXNYVAPLZAW'
test = Address.random(len(address))
#example message basically we can call TryteString and convert it
message = TryteString.from_unicode('Hello world')
#simple transaction last group had tag var inside the transaction
tx = ProposedTransaction(
    address=Address(address),
    message=message,
    value=0
)

print(address)
result = api.send_transfer(transfers=[tx])
print(result['bundle'].tail_transaction.hash)
