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

def main_realize(data_list: list):
    matrix = read_current_matrix(data_list)
    print('*' * 100)
    print(f'Изменение в Биг-Роуд')
    print('Применяем алгоритм к текущей матрице:')
    pprint.pp(matrix)
    main_algorithm.main_process(matrix)
    print('*' * 100)

if __name__ == "__main__":
    main_realize()
