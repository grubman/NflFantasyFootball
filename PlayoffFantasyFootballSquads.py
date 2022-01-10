import requests
import csv
import time

time.sleep(1)
response = requests.get("http://api.sportradar.us/nfl/official/trial/v7/en/seasons/2021/REG/standings/season.json?api_key=bmw3vkatxrey3zmwd6ykwmze")
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
        print "processing {} conference".format(conference["name"])
        divisions = conference["divisions"]
        for division in divisions:
            print "processing {} division".format(division["name"])
            teams = division["teams"]
            for team in teams:
                team_name = "{} {}".format(team["market"], team["name"])
                print "processing {}".format(team_name)
                team_conference_rank = team["rank"]["conference"]
                if team_conference_rank <= 7:
                    print "team is in the playoffs (ranked: {})".format(team_conference_rank)
                    team_id = team["id"]
                    roster_url = "http://api.sportradar.us/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key=bmw3vkatxrey3zmwd6ykwmze".format(team_id)
                    print "calling roster url - {}".format(roster_url)
                    time.sleep(1)
                    roster_response = requests.get("http://api.sportradar.us/nfl/official/trial/v7/en/teams/{}/full_roster.json?api_key=bmw3vkatxrey3zmwd6ykwmze".format(team_id))
                    roster = roster_response.json()
                    players = roster["players"]
                    rosters_file_writer.writerow([team_name, "D/ST", team_name])
                    for player in players:
                        position = player["position"]
                        if position in position_mapping:
                            name = player["name"]
                            rosters_file_writer.writerow([team_name, position_mapping[position], name])




