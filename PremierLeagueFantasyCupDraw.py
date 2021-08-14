import random
import sys
import time

players = [
    'Blue4ever (Adi Ginzburg)',
    'Red or dead (Kfir Emmer)',
    'Atias (Dudi Atias)',
    'Roe ikeda (Roe Ikeda)',
    'Hazans (Dor Hazan)',
    'Show Me The Mane (Ehud Gershon)',
    'Danny Shaw-ve-Ivan-y (Hadar Grubman)',
    'Shaw Mee De Mane (David Peres)',
    'Mandelim (Ohad Mandel)',
    'Yellowmania (Yaniv Salomon)',
    'Gg! (Michael Peleg)',
    'Mkharbatyan (Alon Shamir)',
    'Wan Man Shaw (Ronen Pari)',
    'Boom Shaka Saka (Tal Avraham)',
    'OT FC (Attar Tur)',
    'HTA (Daniel Zilberberg)',
    'Borussia Shkolar (Yuval Shkolar)',
    'Hapo hell (Yoav Mor)',
    'GrealishChildish (Or Portal)',
    'The Larks (Niv Yosefi)',
    'Charlie and a half (Idan Even)',
    'Harrison Lord (Tom Harel)',
    'cococoufal (Daniel Simon)',
    'baruch sarusi (Baruch Sarusi)',
    'F.C Trentola (Karel Poborsky)',
    'It Almost Came Home (Alex Golts)',
    'Saka Avocado (Alon Meir)',
    'AbraDubravka (Rani Eylat)',
    'Moura bora (Tomer Goldthorpe)',
    'FORZA GUNNERS (Elad Kainer)'
]

round_of_16 = [
    'Winner 1',
    'Winner 2',
    'Winner 3',
    'Winner 4',
    'Winner 5',
    'Winner 6',
    'Winner 7',
    'Winner 8',
    'Winner 9',
    'Winner 10',
    'Winner 11',
    'Winner 12',
    'Winner 13',
    'Winner 14',
    'Winner 15',
    'Best looser'
]

quarter_finals = [
    'Winner 16',
    'Winner 17',
    'Winner 18',
    'Winner 19',
    'Winner 20',
    'Winner 21',
    'Winner 22',
    'Winner 23'
]

semi_finals = [
    'Winner 24',
    'Winner 25',
    'Winner 26',
    'Winner 27'
]

final = [
    'Winner 28',
    'Winner 29'
]


def print_same_line(prefix, suffix):
    sleep_time = 1
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for wait in range(5):
        time.sleep(sleep_time)
        sys.stdout.write('.')
        sys.stdout.flush()
    time.sleep(sleep_time)
    sys.stdout.write(suffix)
    sys.stdout.flush()


def print_line_no_delay(line):
    sys.stdout.write(line)
    sys.stdout.flush()


def shuffle_stage_and_print(stage_name, stage_players, first_match):
    for index in range(5000):
        random.shuffle(stage_players)

    print_line_no_delay('\n{}:\n'.format(stage_name))
    for index in range(len(stage_players)):
        if index % 2 == 0:
            match_number = (index/2) + first_match
            if match_number > 9:
                spaces = '   '
            else:
                spaces = '    '
            print_same_line('Match {}.{}'.format(match_number, spaces), stage_players[index])
        else:
            print_same_line(' - ', '{}\n'.format(stage_players[index]))


def main():
    shuffle_stage_and_print('First Round', players, 1)
    shuffle_stage_and_print('Round of 16', round_of_16, 16)
    shuffle_stage_and_print('Quarter Finals', quarter_finals, 24)
    shuffle_stage_and_print('Semi Finals:', semi_finals, 28)
    shuffle_stage_and_print('Final', final, 30)


if __name__ == "__main__":
    main()
