import http.client
import json
import time
import csv

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': 'fb98f620df7a4def92738e2f7bb95d80'}
connection.request('GET', '/v2/competitions/2000/teams', None, headers)
response = json.loads(connection.getresponse().read().decode())
teams = response['teams']
team_ids = []

for team in teams:
    team_ids.append(team['id'])


with open('/Users/hagrubma/WorldCupSquads.csv', 'w') as squads_file:
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
            player_position = team_player['position']
            player_number = team_player['shirtNumber']
            squads_file_writer.writerow([team_name, player_name, player_position, player_number])

        print('Found squad for ' + team_name)

    print('Done')


