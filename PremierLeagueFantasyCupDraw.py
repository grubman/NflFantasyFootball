import random
import sys
import time

players = [
    'Hadar Grubman',
    'Kfir Emmer',
    'Daniel Zilberberg',
    'Bar Badihi',
    'Ofer Nikos Tsitiat',
    'hadar hason',
    'Michael Peleg',
    'Or Portal',
    'Omer Apel',
    'Dani Shafir',
    'David Cohen',
    'Idan Shwartz',
    'Yuval Shkolar',
    'Baruch Sarusi',
    'Dudi Atias',
    'Idan Even',
    'Adi Ginzburg',
    'Yogev Balilti',
    'Dor Hazan',
    'Alon Meir',
    'Oran Turgeman',
    'Tomer Goldthorpe',
    'Alex Golts',
    'Elad Kainer',
    'Roe Ikeda',
    'Rani Eylat',
    'Yaniv Salomon',
    'Daniel Simon',
    'Tal Avraham',
    'Alon Shamir',
    'Ohad Mandel',
    'Tom Harel',
    'David Peres',
    'Ronen Pari'
]


def print_same_line(prefix, suffix):
    sleep_time = 1
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for wait in range(3):
        time.sleep(sleep_time)
        sys.stdout.write('.')
        sys.stdout.flush()
    time.sleep(sleep_time)
    sys.stdout.write(suffix)
    sys.stdout.flush()


def print_line_no_delay(line):
    sys.stdout.write(line)
    sys.stdout.flush()


def shuffle_stage_and_print(stage_name, stage_players, first_match, match_week):
    for index in range(5000):
        random.shuffle(stage_players)

    print_line_no_delay('\n{}: (Match Week {})\n'.format(stage_name, match_week))
    for index in range(len(stage_players)):
        if index % 2 == 0:
            match_number = int((index/2) + first_match)
            if match_number > 9:
                spaces = '   '
            else:
                spaces = '    '
            print_same_line('Match {}.{}'.format(match_number, spaces), stage_players[index])
        else:
            print_same_line(' - ', '{}\n'.format(stage_players[index]))


def shuffle_subgroup(original_group, subgroup_size):
    group = []
    group.extend(original_group)

    for index in range(5000):
        random.shuffle(group)

    return group[0:subgroup_size], group[subgroup_size:]


def generate_winners_list(first_winner_index, winners_count):
    winners = []
    for index in range(winners_count):
        winners.append('Winner ' + str(index + first_winner_index))

    return winners


def main():
    (preliminary_round_players, rest_of_players) = shuffle_subgroup(players, 4)
    rest_of_players.extend(generate_winners_list(1, 2))

    preliminary_round_game_week = shuffle_subgroup(range(10, 17), 1)[0][0]
    round_game_weeks = shuffle_subgroup(range(18, 39), 4)[0]
    round_game_weeks.sort()

    shuffle_stage_and_print('Preliminary Round', preliminary_round_players, 1, preliminary_round_game_week)
    shuffle_stage_and_print('First Round', rest_of_players, 3, 17)
    shuffle_stage_and_print('Round of 16', generate_winners_list(3, 16), 19, round_game_weeks[0])
    shuffle_stage_and_print('Quarter Finals', generate_winners_list(19, 8), 27, round_game_weeks[1])
    shuffle_stage_and_print('Semi Finals:', generate_winners_list(27, 4), 31, round_game_weeks[2])
    shuffle_stage_and_print('Final', generate_winners_list(31, 2), 33, round_game_weeks[3])


if __name__ == "__main__":
    main()
