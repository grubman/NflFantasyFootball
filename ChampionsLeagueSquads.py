import http.client
import json
import time
import csv

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': 'fb98f620df7a4def92738e2f7bb95d80'}
connection.request('GET', '/v2/competitions/2001/matches', None, headers)
response = json.loads(connection.getresponse().read().decode())
matches = response['matches']
team_ids = []

for match in matches:
    if match['stage'] == 'LEAGUE_STAGE':
        match_day = match['matchday']
        date = match['utcDate']
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']

        print(f'{match_day},{date},{home_team},{away_team}')
        home_team_id = match['homeTeam']['id']
        away_team_id = match['awayTeam']['id']


        if home_team_id not in team_ids:
            team_ids.append(home_team_id)

        if away_team_id not in team_ids:
            team_ids.append(away_team_id)

with open('/Users/hagrubma/UCLSquads.csv', 'w') as squads_file:
    squads_file_writer = csv.writer(squads_file)
    request_counter = 1
    for team_id in team_ids:
        if request_counter % 10 == 0:
            time.sleep(60)

        connection.request('GET', '/v2/teams/' + str(team_id), None, headers)
        team_response = json.loads(connection.getresponse().read().decode())
        request_counter += 1

        team_name = team_response['name']
        team_players = team_response['squad']

        if len(team_players) == 0:
            print('No squad for ' + team_name)
            continue

        for team_player in team_players:
            player_name = team_player['name']
            squads_file_writer.writerow([team_name, player_name])

        print('Found squad for ' + team_name)

    print('Done')


