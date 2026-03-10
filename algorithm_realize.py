import pprint
import random
import time

import main_algorithm

element_list = ['P', 'B', 'T']
counter = 0

def read_current_matrix(data_list: list):
    '''Функция для чтения текущих данных из файла'''

    list_dict = {}

    for i in range(6):
        list_dict[i] = []

    for (i, el) in enumerate(data_list):
        list_dict[i%6].append(el)

    final_matrix = []
    for key in list_dict.keys():
        final_matrix.append(list_dict[key])

    return final_matrix


def write_new_element_to_file():
    '''Функция для записи в файл случайных значений'''

    global counter

    random_val = random.randint(0,100)
    if 0 <= random_val < 45:
        el_to_write = element_list[0]
    elif 45 <= random_val < 90:
        el_to_write = element_list[1]
    else:
        el_to_write = element_list[2]

    cur_mtrx = read_current_matrix()
    len_arr = []
    for l in cur_mtrx:
        len_arr.append(len(l))

    prev_len = len_arr[0]
    id_to_insert = 0
    for (i, l) in enumerate(len_arr):
        if i >= 0:
            if l != prev_len:
                id_to_insert = i
                break
            else:
                prev_len = l

    cur_mtrx[id_to_insert].append(el_to_write)
    formated_mtrx = []
    for l in cur_mtrx:
        s_to_insert = ''
        for el in l:
            s_to_insert += str(el) + ' '
        s_to_insert = s_to_insert.rstrip()
        s_to_insert += '\n'
        formated_mtrx.append(s_to_insert)

    with open(filename, 'w', encoding='utf-8') as file:
        for s in formated_mtrx:
            file.write(s)

    return el_to_write

def pattern_review(code, bid):
    formated_bid = None

    if bid == 'B':
        formated_bid = 'Банкир'
    if bid == 'P':
        formated_bid = 'Игрок'
    if bid is None:
        formated_bid = 'Не определенно'

    if code == 0:
        print(f'Алгоритм встретил ничью и пропускает текущую серию.  |  Ставка на: {formated_bid}')
    elif code == 1:
        print(f'Алгоритм определил две красивые серии подряд.  |  Ставка на: {formated_bid}')
    elif code == 2:
        print(f'Алгоритм определил две НЕ красивые серии подряд.  |  Ставка на: {formated_bid}')
    elif code == 3:
        print(f'Алгоритм определил Качели.  |  Ставка на: {formated_bid}')
    else:
        print('Алгоритм не смог найти ни один патерн')

def main_realize(data_list: list, algorithm_stat):
    """Реализация алгоритма к текущему Биг-Роуд"""

    # Форматирование текущего Биг-Роуд к матрице
    matrix = read_current_matrix(data_list)

    # Применение алгоритма к текущей матрице, и получение определённого патерна, ожидаемой ставки и последнего выйгрыша
    pattern, bid, last_win = main_algorithm.main_process(matrix)
    print('*' * 100)
    print(f'Изменение в Биг-Роуд:')
    print()
    if pattern > 0:
        if algorithm_stat.tieStreak:
            algorithm_stat.tieStreak = False
        # Проверка на первый ход алгоритма
        if algorithm_stat.check_first_turn(bid):
            print(f'Первый, ход, алгоритм предлагает ставить на: {bid}')
        else:
            # Определение Победы или Поражения алгоритма в прошлой серии
            win_or_lose = algorithm_stat.check_win(last_win, bid)
            if win_or_lose:
                print(f'Алгоритм ПОБЕДИЛ в прошлой ставке, его статистика:')
            else:
                print(f'Алгоритм ПРОИГРАЛ в прошлой ставке, его статистика:')
            algorithm_stat.print_stat()
            print()
            print('-'*50)
            print()
            print('Следующая ставка:')
            pattern_review(pattern, bid)
    else:
        if pattern == 0:
            if algorithm_stat.gamesCounter != 0:
                if not algorithm_stat.tieStreak:
                    algorithm_stat.calculate_tie()
                    print(f'Алгоритм ПРОИГРАЛ в прошлой ставке, его статистика:')
                    algorithm_stat.print_stat()
                    print()
                    print('-' * 50)
                    print()
                    pattern_review(pattern, bid)
                else:
                    pattern_review(pattern, bid)
            else:
                pattern_review(pattern, bid)
        else:
            print('Недостаточно завершённых серий для анализа')
            print('Алгоритм начнёт работу с восьмой завершённой серии')

    print('*' * 100)
    print()
    print()
    print()