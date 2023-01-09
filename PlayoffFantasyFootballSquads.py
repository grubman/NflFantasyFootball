import requests
import csv
import time

time.sleep(1)
# need to register with different mail to https://developer.sportradar.com/ every year and get a new trial api_key
api_key = "94hm864884z4rb8n8ppujbtr"
response = requests.get('https://api.sportradar.us/nfl/official/trial/v7/en/seasons/2022/REG/standings/season.json?api_key={}'.format(api_key))
standings = response.json()
conferences = standings["conferences"]
position_mapping = {
    "CB": "DP",
    "DB": "DP",
    "DE": "DP",
    "DT": "DP",
    "FB": "RB",
    "K": "K",
    "LB": "DP",
    "QB": "QB",
    "RB": "RB",
    "SAF": "DP",
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
                team_conference_rank = team["rank"]["conference"]
                if team_conference_rank <= 7:
                    print("team is in the playoffs (ranked: {})".format(team_conference_rank))
                    team_id = team["id"]
                    roster_url = "https://api.sportradar.us/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key={}".format(team_id, api_key)
                    print("calling roster url - {}".format(roster_url))
                    time.sleep(1)
                    roster_response = requests.get("https://api.sportradar.us/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key={}".format(team_id, api_key))
                    roster = roster_response.json()
                    players = roster["players"]
                    rosters_file_writer.writerow([team_name, "D/ST", team_name])
                    for player in players:
                        position = player["position"]
                        if position in position_mapping:
                            name = player["name"]
                            rosters_file_writer.writerow([team_name, position_mapping[position], name])




