import json
from Crypto.Cipher import AES

teams = [
    "Baltimore Ravens",
    "Buffalo Bills",
    "Chicago Bears",
    "Cleveland Browns",
    "Green Bay Packers",
    "Indianapolis Colts",
    "Kansas City Chiefs",
    "Los Angeles Rams",
    "New Orleans Saints",
    "Pittsburgh Steelers",
    "Seattle Seahawks",
    "Tampa Bay Buccaneers",
    "Tennessee Titans",
    "Washington Football Team"
]


def collect_bid(team, max_bid):
    while True:
        print("Enter your bid for {} (between 0 and {}): ".format(team, max_bid))
        bid_str = raw_input()
        if not bid_str.isdigit():
            print("Error: Not an integer!")
            continue
        bid = int(bid_str)
        if bid < 0 or bid > max_bid:
            print("Error: Not in range!")
            continue
        return bid


def collect_bids():
    bids = {}
    total_bids = 0
    for team in teams:
        max_bid = 1000-total_bids
        bid = 0
        if max_bid != 0:
            bid = collect_bid(team, max_bid)
        bids[team] = bid
        total_bids += bid
    return bids


def get_priority_team(value_teams):
    while True:
        print("Choose a team to prioritize higher:")
        for index in range(len(value_teams)):
            print("{}. {}".format(index + 1, value_teams[index]))
        priority_index_str = raw_input()
        if not priority_index_str.isdigit():
            print("Error: Not an integer!")
            continue
        priority_index = int(priority_index_str)
        if priority_index < 1 or priority_index > len(value_teams):
            print("Error: Not in range!")
            continue
        return value_teams[priority_index-1]


def ask_for_priority(value, value_teams):
    priority = []
    print("The following teams have the same bid value ({}): {}".format(value, ', '.join(value_teams)))
    while len(value_teams) > 1:
        priority_team = get_priority_team(value_teams)
        value_teams.remove(priority_team)
        priority.append(priority_team)
    priority.append(value_teams[0])
    return priority


def collect_priority(bids):
    reverse_bids = {}
    bid_values = []
    priority = []
    for bid in bids:
        value = bids[bid]
        if value not in reverse_bids:
            reverse_bids[value] = []
            bid_values.append(value)
        reverse_bids[value].append(bid)
    bid_values.sort(reverse=True)
    for value in bid_values:
        value_teams = reverse_bids[value]
        if len(value_teams) == 1:
            priority.append(value_teams[0])
        else:
            priority.extend(ask_for_priority(value, value_teams))
    return priority


def verify_bids(bids, priority):
    print("Here are your bids:")
    for bid in bids:
        print("{} - {}".format(bid, bids[bid]))
    print("Here is the order of priority:")
    for index in range(len(priority)):
        print("{}. {}".format(index+1, priority[index]))
    print("Are you sure? (Y/N)")
    answer = raw_input()
    lower_answer = answer.lower()
    return lower_answer == "y" or lower_answer == "yes"


def collect_name():
    while True:
        print("Name your bids: ")
        name = raw_input()
        if name.isalnum():
            return name
        print("Error: Not alpha-numeric!")


def collect_password():
    while True:
        print("Enter password: ")
        password = raw_input()
        print("Re-enter password: ")
        password2 = raw_input()
        if password == password2:
            return password.zfill(16)[:16]
        print("Passwords don't match")


def encrypt_bids(bids, priority):
    name = collect_name()
    bids["Name"] = name
    bids["priority"] = priority
    bids_json = json.dumps(bids).encode("utf-8")
    aes = AES.new(collect_password().encode("utf-8"), AES.MODE_ECB)
    encrypted_bid = aes.encrypt(bids_json.zfill(16 * (int(len(bids_json) / 16)+1)))
    encrypted_file = open("{}.bids".format(name), 'wb')
    encrypted_file.write(encrypted_bid)
    encrypted_file.close()


def main():
    bids = {}
    priority = []
    is_verified = False
    while not is_verified:
        bids = collect_bids()
        priority = collect_priority(bids)
        is_verified = verify_bids(bids, priority)
    encrypt_bids(bids, priority)


if __name__ == "__main__":
    main()
