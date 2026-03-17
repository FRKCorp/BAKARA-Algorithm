import numpy as np
import pprint

import logging
logger = logging.getLogger(__name__)

response_file = 'example-input/response-example.txt'

# def read_current_matrix():
#     '''Функция для чтения данных из файла'''
#
#     with open(response_file, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         matrix = []
#         for line in lines:
#             line_list = line.split(' ')
#             formated_list = []
#             for el in line_list:
#                 formated_list.append(el.strip())
#             matrix.append(formated_list)
#         return matrix

def get_current_position(matrix):
    '''Функция для получения текущей позиции(куда нужно ставить фишку)'''

    lens_arr = []
    for l in matrix:
        lens_arr.append(len(l))

    is_all_same = lens_arr.count(lens_arr[0]) == len(lens_arr)

    cursor_id = 0
    if is_all_same:
        cursor_id = 0
    else:
        for (len_id, lens) in enumerate(lens_arr):
            if len_id > 0:
                if lens != lens_arr[len_id-1]:
                    cursor_id = len_id
                    break
    new_len = (lens_arr[0] - 2, lens_arr[0] - 1)
    return cursor_id, new_len

def format_matrix(matrix, new_width, new_height):
    '''Функция для форматирования матрицы к новым значениям(чтобы отбросить не влияющие на алгоритм элементы)'''
    new_matrix = []
    w = new_width[0]
    h = new_height

    if h >= 2:
        for (i,element) in enumerate(matrix):
            new_matrix.append(element[w:])
            if i == h:
                break
    else:
        if h == 1:
            for (i, m) in enumerate(matrix):
                if i == 0:
                    new_matrix.append(m[w:])
                else:
                    new_matrix.append(m[w-1:])
        if h == 0:
            for m in matrix:
                new_matrix.append(m[w:])

    return new_matrix

def check_pattern(matrix, pos):
    '''Функция для определения патерна и составления рекомендации для ставки'''

    who_to_bid = None
    current_list = matrix[pos]
    prev_winner = current_list[len(current_list) - 1]

    # Определение переменных для обычных случаев
    if pos >= 2:
        previous_list2 = matrix[pos-2]
        previous_list1 = matrix[pos-1]
    else:
        # Определение переменных для первой строки
        if pos == 1:
            previous_list2 = matrix[len(matrix)-1]
            previous_list1 = matrix[pos - 1]
        # Определение переменных для нулевой строки
        if pos == 0:
            previous_list2 = matrix[len(matrix) - 2]
            previous_list1 = matrix[len(matrix) - 1]


    if 'T' in previous_list1 or 'T' in previous_list2 or 'T' in current_list:
        return (0, who_to_bid)

    is_all_same2 = previous_list2.count(previous_list2[0]) == len(previous_list2)
    is_all_same1 = previous_list1.count(previous_list1[0]) == len(previous_list1)

    # Проверяем на красивый патерн
    if is_all_same1 and is_all_same2:
        # Делаем ставку на тот же цвет
        who_to_bid = prev_winner
        return (1, who_to_bid)
    # Проверяем на не красивый патерн
    elif not is_all_same1 and not is_all_same2:
        # Делаем ставку на противоположный цвет
        if prev_winner == 'P':
            who_to_bid = 'B'
        if prev_winner == 'B':
            who_to_bid = 'P'
        return (2, who_to_bid)
    # Проверяем на качели
    else:
        # Если последним был Крассивый патерн, то ставим на некрасивый
        if is_all_same1:
            if prev_winner == 'P':
                who_to_bid = 'B'
            if prev_winner == 'B':
                who_to_bid = 'P'
        # Если последним был не Крассивый патерн, то ставим на крассивый
        else:
            who_to_bid = prev_winner
        return (3, who_to_bid)

def check_for_len(matrix):
    '''Функция для проверки длины матрицы'''

    len_sum = 0
    for l in matrix:
        len_sum += len(l)

    if len_sum < 8:
        return False
    else:
        return True

def get_last_element(matrix):
    """Функция для получения последнего элемента матрицы"""
    lens_arr = []
    for l in matrix:
        lens_arr.append(len(l))

    is_all_same = lens_arr.count(lens_arr[0]) == len(lens_arr)

    if is_all_same:
        r_id = len(matrix)-1
        return matrix[r_id][len(matrix[r_id])-1]
    else:
        last_id = 0
        for (i,l) in enumerate(lens_arr):
            if i > 0:
                if l != lens_arr[i-1]:
                    last_id = i-1
                    break
        return matrix[last_id][len(matrix[last_id])-1]

def main_process(matrix):
    '''Основная функция для работы алгоритма'''

    # Считывание текущих фишек Биг-Роуд
    current_matrix = matrix

    # Проверка на длину матрицы
    if check_for_len(current_matrix):
        # Получение позиций из матрицы
        current_cursor, formated_matrix_len = get_current_position(current_matrix)

        # Форматирование матрицы и отбрасывания лишних значений
        current_matrix = format_matrix(current_matrix, formated_matrix_len, current_cursor)

        # Определение текущего патерна и рекомендации для ставки
        pattern_code, current_bid = check_pattern(current_matrix, current_cursor)

        # Определение последнего выйгрыша, для расчёта победы или пройгрыша алгоритма
        last_win = get_last_element(current_matrix)

        return pattern_code, current_bid, last_win
    else:
        return -1, -1, -1