import pprint
import random
import time

import main_algorithm
from AlgorithmClass import Algorythm

import logging
logger = logging.getLogger(__name__)

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
        logger.info(f'⚠️ Алгоритм встретил ничью и пропускает текущую серию.  |  Ставка на: {formated_bid}')
    elif code == 1:
        logger.info(f'✅ Алгоритм определил красивую серию.  |  Ставка на: {formated_bid}')
    elif code == 2:
        logger.info(f'✅ Алгоритм определил НЕ красивую серии.  |  Ставка на: {formated_bid}')
    elif code == 3:
        logger.info(f'🔹 Алгоритм определил Качели.  |  Ставка на: {formated_bid}')
    else:
        logger.info('❌ Алгоритм не смог найти ни один патерн')

def format_bid(code, bid):
    formated_bid = None
    formated_pattern = None

    if bid == 'B':
        formated_bid = 'Банкир'
    if bid == 'P':
        formated_bid = 'Игрок'
    if bid is None:
        formated_bid = 'Не определенно'

    if code == 0:
        formated_pattern = 'Ничья'
    elif code == 1:
        formated_pattern = 'Красивый'
    elif code == 2:
        formated_pattern = 'НЕ Красивый'
    elif code == 3:
        formated_pattern = 'Качели'

    return formated_pattern, formated_bid

def debug_alg_stat(alg: Algorythm):
    print(f'Previous Predict: {alg.previousPredict} | Last Win: {alg.lastWinElement} | Games: {alg.gamesCounter} | LoseStreak: {alg.loseStreak} | Win/Lose: {alg.win_lose}')


def main_realize(data_list: dict, algorithm_stat: dict, changed_table: str):
    """Реализация алгоритма к текущему Биг-Роуд"""

    all_tables_result = {}

    table_id = changed_table

    # Форматирование текущего Биг-Роуд к матрице
    matrix = read_current_matrix(data_list[table_id])

    # Применение алгоритма к текущей матрице, и получение определённого патерна, ожидаемой ставки и последнего выйгрыша
    pattern, bid, last_win = main_algorithm.main_process(matrix, algorithm_stat[table_id])
    logger.info('*' * 45)
    logger.info(f'🔹 Изменение в Биг-Роуд:')
    if pattern >= 0:
        # Проверка на первый ход алгоритма
        if algorithm_stat[table_id].check_first_turn(bid):
            logger.info(f'🔹 Первый, ход, алгоритм предлагает ставить на: {bid}')
        else:
            # Определение Победы или Поражения алгоритма в прошлой серии или обработка Ничьи
            win_or_lose = algorithm_stat[table_id].check_win(last_win, bid)
            if win_or_lose:
                logger.info(f'✅ Алгоритм ПОБЕДИЛ в прошлой ставке, его статистика:')
            elif not win_or_lose:
                logger.info(f'❌ Алгоритм ПРОИГРАЛ в прошлой ставке, его статистика:')
            elif win_or_lose == 'Skip':
                logger.info(f'🔹 Алгоритм ПРОПУСКАЛ предыдущую ставку, его статистика:')
            algorithm_stat[table_id].print_stat()
            logger.info('-'*54)
            logger.info('Следующая ставка:')
            pattern_review(pattern, bid)
    else:
        logger.info('⚠️ Неправильное количество серий для анализа')
        logger.info('⚠️ Алгоритм работает с восьмой по сороковую серию')

    logger.info('*' * 45)

    f_pattern, f_bid = format_bid(pattern, bid)

    result = {
        "pattern": f_pattern,
        "bid": f_bid,
        "wins": algorithm_stat[table_id].win_lose['Wins'],
        "loses": algorithm_stat[table_id].win_lose['Lose'],
        "loseStreak": algorithm_stat[table_id].loseStreak
    }

    all_tables_result[table_id] = result
    all_tables_result['table_id'] = table_id

    return all_tables_result