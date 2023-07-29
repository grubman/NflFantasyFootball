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
    sleep_time = 0
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


def validate_number(input_str):
    if not input_str.isdigit():
        print('The pick should be a number')
        sys.exit(1)

    value = int(input_str)
    if value < 1 or value > 10:
        print('The pick should be between 1 and 10')
        sys.exit(1)

    return value


def validate_raw_input(arguments):
    consolation_prize_winner = arguments[1]
    if consolation_prize_winner not in players:
        print('ConsolationPrizeWinner should be one of {players}'.format(players=', '.join(players)))
        sys.exit(1)

    return consolation_prize_winner, (validate_number(arguments[2]))


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
    print('usage: FantasyFootballDraw.py --reshuffle <ConsolationPrizeWinner> <OnlyChoice>')
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

    arguments = [argument for argument in sys.argv if argument != '--reshuffle']
    if len(arguments) != 3:
        usage_fail()

    consolation_prize_winner, consolation_prize_winner_pick = \
        validate_raw_input(arguments)

    if consolation_prize_winner_pick != 0:
        players.remove(consolation_prize_winner)

    for index in range(5000):
        random.shuffle(players)

    if consolation_prize_winner_pick != 0:
        players.insert(consolation_prize_winner_pick-1, consolation_prize_winner)

    print_results()


if __name__ == "__main__":
    main()
