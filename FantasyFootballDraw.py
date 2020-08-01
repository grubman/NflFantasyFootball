import random
import sys
import time

players = [
    'Adi',
    'Ayal',
    'Daniel',
    'Ehud',
    'Felix',
    'Gilad',
    'Hadar F',
    'Hadar G',
    'On',
    'Ophir'
]


def print_line(prefix, suffix):
    sleep_time = 3
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for wait in range(3):
        time.sleep(sleep_time)
        sys.stdout.write('.')
        sys.stdout.flush()
    time.sleep(sleep_time)
    sys.stdout.write('{}\n'.format(suffix))
    sys.stdout.flush()


def print_results():
    for index in range(len(players)):
        back_index = 9 - index
        print_line('Pick number {} goes to '.format(back_index + 1), ' {}'.format(players[back_index]))


def validate_number(input_str, name, min_value, max_value):
    if not input_str.isdigit():
        print('{} should be a number'.format(name))
        sys.exit(1)

    value = int(input_str)
    if value < min_value or value > max_value:
        print('{} should be between {} and {}'.format(name, min_value, max_value))
        sys.exit(1)

    return value


def validate_input():
    consolation_prize_winner = sys.argv[1]
    if consolation_prize_winner not in players:
        print('ConsolationPrizeWinner should be one of {players}'.format(players=', '.join(players)))
        sys.exit(1)

    input_name = 'onlyChoice' if len(sys.argv) == 3 else 'FirstChoice'
    min_value = 5 if len(sys.argv) == 3 else 1
    consolation_prize_winner_first_pick = validate_number(sys.argv[2], input_name, min_value, max_value=10)

    consolation_prize_winner_second_pick = 0
    if len(sys.argv) == 4:
        consolation_prize_winner_second_pick = validate_number(sys.argv[3], 'SecondChoice', min_value=1, max_value=10)

    return consolation_prize_winner, consolation_prize_winner_first_pick, consolation_prize_winner_second_pick


def consolation_prize_draw(array, pick_number):
    for index in range(5000):
        random.shuffle(array)
    result = array[0] == 1
    print_line("Consolation draw for pick {} is ".format(pick_number), " successful" if result else " not successful")
    return result


def get_consolation_prize_spot(first_pick, second_pick):
    if second_pick == 0:
        return first_pick
    if consolation_prize_draw([1, 0], first_pick):
        return first_pick
    if consolation_prize_draw([1, 0, 0], second_pick):
        return second_pick
    return 0


def main():
    if len(sys.argv) != 4 and len(sys.argv) != 3 and len(sys.argv) != 1:
        print('usage: FantasyFootballDraw.py\n')
        print('usage: FantasyFootballDraw.py <ConsolationPrizeWinner> <OnlyChoice>\n')
        print('usage: FantasyFootballDraw.py <ConsolationPrizeWinner> <FirstChoice> <SecondChoice>\n')
        sys.exit(1)

    consolation_prize_winner = ''
    consolation_prize_winner_final_spot = 0
    if len(sys.argv) > 1:
        consolation_prize_winner, consolation_prize_winner_first_pick, consolation_prize_winner_second_pick = validate_input()
        consolation_prize_winner_final_spot = get_consolation_prize_spot(consolation_prize_winner_first_pick, consolation_prize_winner_second_pick)

    if consolation_prize_winner_final_spot != 0:
        players.remove(consolation_prize_winner)

    for index in range(5000):
        random.shuffle(players)

    if consolation_prize_winner_final_spot != 0:
        players.insert(consolation_prize_winner_final_spot-1, consolation_prize_winner)

    print_results()


if __name__ == "__main__":
    main()
