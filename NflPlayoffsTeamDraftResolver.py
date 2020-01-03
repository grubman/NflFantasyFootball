import os
import json
import random
import time
import sys
from Crypto.Cipher import AES


tie_breaker_order = []
bidder_to_reversed_bids = {}
bidder_to_original_bids = {}
logs = []
final_results = {}
fast_forward = False


def reverse_bids(bids_content):
    reversed_bids = {"values": [], "priority": bids_content["priority"]}
    del bids_content["priority"]
    for bid in bids_content:
        value = bids_content[bid]
        if value not in reversed_bids:
            reversed_bids[value] = []
            reversed_bids["values"].append(value)
        reversed_bids[value].append(bid)
    reversed_bids["values"].sort(reverse=True)
    return reversed_bids


def decrypt_bids_file(name, file):
    encrypted_file = open(file, 'rb')
    content = encrypted_file.read()
    while True:
        print("Enter password for {}".format(name))
        password = input()
        aes = AES.new(password.zfill(16)[:16].encode("utf-8"), AES.MODE_ECB)
        bids_content = json.loads(aes.decrypt(content).decode("utf-8").lstrip('0'))
        if name == bids_content["Name"]:
            print("Decrypted successfully!")
            del bids_content["Name"]
            bids_content_copy = dict(bids_content)
            bids_content_copy["priority"] = list(bids_content["priority"])
            bidder_to_original_bids[name] = bids_content_copy
            return reverse_bids(bids_content)
        else:
            print("Wrong password")


def decrypt_bids_files():
    global bidder_to_reversed_bids
    for file in os.listdir(path='.'):
        if file.endswith('.bids'):
            name = file[:len(file)-5]
            bidder_to_reversed_bids[name] = decrypt_bids_file(name, file)


def randomize_tie_breaker_order():
    users = list(bidder_to_reversed_bids.keys())
    global tie_breaker_order
    for index in range(5000):
        random.shuffle(users)
    print()
    print("Tie-Breaker order is:")
    for index in range(len(users)):
        back_index = len(users) - index - 1
        if not fast_forward:
            time.sleep(5)
        print("{}. {}".format(back_index+1, users[back_index]))
    tie_breaker_order = users


def find_highest_offer():
    highest_offer = 0
    for bidder in bidder_to_reversed_bids:
        bids = bidder_to_reversed_bids[bidder]
        if bids["values"][0] > highest_offer:
            highest_offer = bids["values"][0]
    return highest_offer


def get_prioritized_team(teams, priority):
    for team in priority:
        if team in teams:
            return team


def get_bidded_teams(offer):
    teams = {}
    for bidder in bidder_to_reversed_bids:
        bids = bidder_to_reversed_bids[bidder]
        if offer in bids:
            teams[bidder] = get_prioritized_team(bids[offer], bids["priority"])
    return teams


def reverse_bidder_to_team(bidder_to_team):
    team_to_bidder = {}
    for bidder in bidder_to_team:
        team = bidder_to_team[bidder]
        if team not in team_to_bidder:
            team_to_bidder[team] = []
        team_to_bidder[team].append(bidder)
    return team_to_bidder


def remove_team_from_bids(team):
    for bidder in bidder_to_reversed_bids:
        bids = bidder_to_reversed_bids[bidder]
        bids["priority"].remove(team)
        for bid in bids:
            if bid == "priority" or bid == "values":
                continue
            else:
                teams = bids[bid]
                if team in teams:
                    if len(teams) == 1:
                        del bids[bid]
                        bids["values"].remove(bid)
                    else:
                        teams.remove(team)
                    break


def assign_team(bidder, team, offer):
    logs.append("{} takes {} with a bid of {}".format(bidder, team, offer))
    if bidder not in final_results:
        final_results[bidder] = []
    final_results[bidder].append(team)
    if len(final_results[bidder]) == 3:
        del bidder_to_reversed_bids[bidder]
        logs.append("{} has 3 teams, he is done".format(bidder))
    remove_team_from_bids(team)


def find_tie_breaker_winner(bidders):
    for bidder in tie_breaker_order:
        if bidder in bidders:
            tie_breaker_order.remove(bidder)
            tie_breaker_order.append(bidder)
            logs.append("{} have won the tie break, the new order is {}".format(bidder, ", ".join(tie_breaker_order)))
            return bidder


def resolve_draft_results():
    while len(bidder_to_reversed_bids) > 0:
        highest_offer = find_highest_offer()
        bidder_to_team = get_bidded_teams(highest_offer)
        team_to_bidders = reverse_bidder_to_team(bidder_to_team)
        for team in team_to_bidders:
            bidders = [bidder for bidder in team_to_bidders[team] if bidder in bidder_to_reversed_bids]
            if len(bidders) == 1:
                assign_team(bidders[0], team, highest_offer)
            else:
                logs.append("{} are tied, offered {} on {}".format(", ".join(bidders), highest_offer, team))
                winner = find_tie_breaker_winner(bidders)
                assign_team(winner, team, highest_offer)


def print_results():
    for log in logs:
        if not fast_forward:
            time.sleep(5)
        print(log)
    print("\n\npress Enter for final results:")
    input()
    for bidder in final_results:
        print("{}: {}".format(bidder, ", ".join(final_results[bidder])))
    print("\n\npress enter for original bids:")
    input()
    for bidder in bidder_to_original_bids:
        original_bid = bidder_to_original_bids[bidder]
        priority = original_bid["priority"]
        print("\n{}:".format(bidder))
        for index in range(len(priority)):
            print("{}. {} - {}".format(index + 1, priority[index], original_bid[priority[index]]))


def main():
    global fast_forward
    if len(sys.argv) > 1 and sys.argv[1] == "--fast":
        fast_forward = True

    decrypt_bids_files()
    randomize_tie_breaker_order()
    resolve_draft_results()
    print_results()


if __name__ == "__main__":
    main()
