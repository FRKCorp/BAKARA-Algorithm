import numpy as np
import pprint

response_file = 'example-input/response-example.txt'

def read_current_matrix():
    '''Функция для чтения данных из файла'''

    with open(response_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            line_list = line.split(' ')
            formated_list = []
            for el in line_list:
                formated_list.append(el.strip())
            matrix.append(formated_list)
        return matrix

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

    if h != 0:
        for (i,element) in enumerate(matrix):
            new_matrix.append(element[w:])
            if i == h:
                break
    else:
        new_matrix.append(matrix[0][w:])
        new_matrix.append(matrix[1][w:])

    return new_matrix

def main_process():
    '''Основная функция для работы алгоритма'''

    #Считывание текущих фишек Биг-Роуд
    current_matrix = read_current_matrix()

    #Получение позиций из матрицы
    current_cursor, formated_matrix_len = get_current_position(current_matrix)

    #Форматирование матрицы и отбрасывания лишних значений
    current_matrix = format_matrix(current_matrix, formated_matrix_len, current_cursor)
    pprint.pp(current_matrix)

if __name__ == "__main__":
    main_process()
