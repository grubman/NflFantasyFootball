import random
import sys
import time

players = [
    "Adi",
    "Ayal",
    "Daniel",
    "Ehud",
    "Felix",
    "Gilad",
    "Hadar",
    "Jean",
    "On",
    "Ophir",
    "Tom"
]

for index in range(5000):
    random.shuffle(players)

numOfPlayers = len(players)
for index in range(numOfPlayers):
    backIndex = numOfPlayers-index-1
    sys.stdout.write("Pick number {} goes to ".format(backIndex+1))
    sys.stdout.flush()
    for wait in range(3):
        time.sleep(3)
        sys.stdout.write(".")
        sys.stdout.flush()
    time.sleep(3)
    sys.stdout.write(" {}\n".format(players[backIndex]))
    sys.stdout.flush()



