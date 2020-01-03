import sys
import json
from Crypto.Cipher import AES

encrypted_file = open(sys.argv[1], 'rb')
content = encrypted_file.read()
aes = AES.new(sys.argv[2].zfill(16)[:16].encode("utf-8"), AES.MODE_ECB)
bidder_to_reversed_bids = json.loads(aes.decrypt(content).decode("utf-8").lstrip('0'))
if sys.argv[1] == "{}.bids".format(bidder_to_reversed_bids["Name"]):
    print("Decrypted successfully!")
else:
    print("Wrong password")

del bidder_to_reversed_bids["Name"]
priority = bidder_to_reversed_bids["priority"]
del bidder_to_reversed_bids["priority"]

for bid in bidder_to_reversed_bids:
    print("{} - {}".format(bid, bidder_to_reversed_bids[bid]))
for index in range(len(priority)):
    print("{}. {}".format(index+1, priority[index]))

