import numpy as np

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
    res_string = []
    res_element = ''
    w = new_width[0]
    h = new_height

    if h == 0:
        get_correct_elements = False

        for w_id in range(w, -1, -1):

            if get_correct_elements:
                break

            for h_id in range(5, -1, -1):
                t_list = matrix[h_id][w_id:w_id+2]

                if 'T' not in t_list:
                    get_correct_elements = True
                    res_string = t_list
                    res_element = matrix[h][w+1]
                    break
    else:
        get_correct_elements = False

        for w_id in range(w, -1, -1):

            if get_correct_elements:
                break

            if w_id == w:
                cycle_start = h-1
            else:
                cycle_start = 5
            for h_id in range(cycle_start, -1, -1):
                t_list = matrix[h_id][w_id:w_id+2]

                if 'T' not in t_list:
                    get_correct_elements = True
                    res_string = t_list
                    res_element = matrix[h][w]
                    break


    return res_string, res_element

def check_pattern(matrix, element, stat):
    '''Функция для определения патерна и составления рекомендации для ставки'''

    who_to_bid = None

    if element != 'T':
        is_all_same = matrix.count(matrix[0]) == len(matrix)

        if stat.loseStreak >= 1:
            if is_all_same:
                if element == 'P':
                    who_to_bid = 'B'
                else:
                    who_to_bid = 'P'
                return 3, who_to_bid
            else:
                who_to_bid = element
                return 3, who_to_bid
        else:
            if is_all_same:
                who_to_bid = element
                return 1, who_to_bid
            else:
                if element == 'P':
                    who_to_bid = 'B'
                else:
                    who_to_bid = 'P'
                return 2, who_to_bid
    else:
        return 0, who_to_bid

def check_for_len(matrix):
    '''Функция для проверки длины матрицы'''

    len_sum = 0
    for l in matrix:
        len_sum += len(l)

    if len_sum < 8 or len_sum > 40:
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

def main_process(matrix, algorithm_stat):
    '''Основная функция для работы алгоритма'''

    # Считывание текущих фишек Биг-Роуд
    current_matrix = matrix

    # Проверка на длину матрицы
    if check_for_len(current_matrix):
        # Получение позиций из матрицы
        current_cursor, formated_matrix_len = get_current_position(current_matrix)

        # Форматирование матрицы и отбрасывания лишних значений
        previous_string, current_element  = format_matrix(current_matrix, formated_matrix_len, current_cursor)

        # Определение текущего патерна и рекомендации для ставки
        pattern_code, current_bid = check_pattern(previous_string, current_element, algorithm_stat)

        # Определение последнего выйгрыша, для расчёта победы или пройгрыша алгоритма
        last_win = get_last_element(current_matrix)

        return pattern_code, current_bid, last_win
    else:
        return -1, -1, -1