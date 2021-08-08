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
    'Hadar',
    'On',
    'Ophir',
    'Tom'
]

divisions = [
    'ORDINARY GENTLEMEN',
    'GLORY HUNTERS'
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


def print_new_line(prefix, suffix):
    print_same_line(prefix, suffix)
    sys.stdout.write('\n')
    sys.stdout.flush()


def print_results():
    for index in range(len(players)):
        back_index = 9 - index
        print_new_line('Pick number {} goes to '.format(back_index + 1), ' {}'.format(players[back_index]))


def validate_number(input_str, name, min_value, max_value):
    if not input_str.isdigit():
        print('{} should be a number'.format(name))
        sys.exit(1)

    value = int(input_str)
    if value < min_value or value > max_value:
        print('{} should be between {} and {}'.format(name, min_value, max_value))
        sys.exit(1)

    return value


def validate_raw_input(arguments):
    consolation_prize_winner = arguments[0]
    if consolation_prize_winner not in players:
        print('ConsolationPrizeWinner should be one of {players}'.format(players=', '.join(players)))
        sys.exit(1)

    input_name = 'onlyChoice' if len(arguments) == 3 else 'FirstChoice'
    min_value = 5 if len(arguments) == 2 else 1
    consolation_prize_winner_first_pick = validate_number(arguments[1], input_name, min_value, max_value=10)

    consolation_prize_winner_second_pick = 0
    if len(arguments) == 3:
        consolation_prize_winner_second_pick = validate_number(arguments[2], 'SecondChoice', min_value=1, max_value=10)

    return consolation_prize_winner, consolation_prize_winner_first_pick, consolation_prize_winner_second_pick


def consolation_prize_draw(array_size, pick_number):
    array = [1]
    for index in range(array_size-1):
        array.append(0)
    for index in range(5000):
        random.shuffle(array)
    result = array[0] == 1
    print_new_line("Consolation draw for pick {} is ".format(pick_number), " successful" if result else " not successful")
    return result


def get_consolation_prize_spot(first_pick, second_pick):
    if second_pick == 0:
        return first_pick
    if consolation_prize_draw(2, first_pick):
        return first_pick
    if consolation_prize_draw(3, second_pick):
        return second_pick
    return 0


def reshuffle_divisions():
    for index in range(5000):
        random.shuffle(players)

    print_line_no_delay('The new divisions are:\n')
    print_line_no_delay('\t{}\t{}\n'.format(divisions[0], divisions[1]))

    for index, player in enumerate(players):
        if index % 2 == 0:
            postfix = ''
            if len(player) < 5:
                postfix = '\t'
            print_same_line('\t', '{}{}'.format(player, postfix))
        else:
            print_new_line('\t\t', player)


def usage_fail():
    print('usage: FantasyFootballDraw.py --reshuffle [<ConsolationPrizeWinner> <OnlyChoice>] | '
          '[<ConsolationPrizeWinner> <FirstChoice> <SecondChoice>]\n')
    sys.exit(1)


def main():
    if len(sys.argv) > 5:
        usage_fail()

    should_reshuffle_divisions = False
    for argument in sys.argv:
        if argument.startswith('--'):
            if argument == '--reshuffle':
                should_reshuffle_divisions = True
            else:
                usage_fail()

    if should_reshuffle_divisions:
        reshuffle_divisions()

    consolation_prize_winner = ''
    consolation_prize_winner_final_spot = 0

    arguments = [argument for argument in sys.argv if argument not in ['FantasyFootballDraw.py', '--reshuffle']]
    if len(arguments) > 0:
        consolation_prize_winner, consolation_prize_winner_first_pick, consolation_prize_winner_second_pick = \
            validate_raw_input(arguments)
        consolation_prize_winner_final_spot = \
            get_consolation_prize_spot(consolation_prize_winner_first_pick, consolation_prize_winner_second_pick)

    if consolation_prize_winner_final_spot != 0:
        players.remove(consolation_prize_winner)

    for index in range(5000):
        random.shuffle(players)

    if consolation_prize_winner_final_spot != 0:
        players.insert(consolation_prize_winner_final_spot-1, consolation_prize_winner)

    print_results()


if __name__ == "__main__":
    main()
