import http.client
import json
import csv
import time

time.sleep(1)
# need to register with different mail to https://developer.sportradar.com/ every year and get a new trial api_key
api_key = "4WagDn6EGckKIB734rWSMiU1dhrGkFj41SCpXG3N"

connection = http.client.HTTPConnection('api.sportradar.us')
connection.request('GET', '/nfl/official/trial/v7/en/seasons/2025/REG/standings/season.json?api_key={}'.format(api_key))
standings = json.loads(connection.getresponse().read().decode())
conferences = standings["conferences"]
position_mapping = {
    "CB": "DB",
    "DB": "DB",
    "DE": "DL",
    "DT": "DL",
    "FB": "RB",
    "K": "K",
    "LB": "LB",
    "QB": "QB",
    "RB": "RB",
    "SAF": "DB",
    "TE": "TE",
    "WR": "WR"
}

with open('/Users/hagrubma/NFLRosters.csv', 'w') as rosters_file:
    rosters_file_writer = csv.writer(rosters_file)
    for conference in conferences:
        print("processing {} conference".format(conference["name"]))
        divisions = conference["divisions"]
        for division in divisions:
            print("processing {} division".format(division["name"]))
            teams = division["teams"]
            for team in teams:
                team_name = "{} {}".format(team["market"], team["name"])
                print("processing {}".format(team_name))
                team_id = team["id"]
                roster_url = "https://api.sportradar.us/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key={}".format(team_id, api_key)
                print("calling roster url - {}".format(roster_url))
                time.sleep(1)
                connection.request('GET', '/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key={}'.format(team_id, api_key))
                roster = json.loads(connection.getresponse().read().decode())
                players = roster["players"]
                rosters_file_writer.writerow([team_name, "D/ST", team_name])
                for player in players:
                    position = player["position"]
                    if position in position_mapping:
                        name = player["name"]
                        rosters_file_writer.writerow([team_name, position_mapping[position], name])
