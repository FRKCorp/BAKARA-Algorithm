import pprint
import random
import time

import main_algorithm

element_list = ['P', 'B', 'T']
counter = 0
filename = '../example-input/response-example.txt'

def read_current_matrix():
    '''Функция для чтения текущих данных из файла'''

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            line_list = line.split(' ')
            formated_list = []
            for el in line_list:
                formated_list.append(el.strip())
            matrix.append(formated_list)
        return matrix

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

def main_realize():
    print('Тестирование для алгоритма:')
    input()

    while True:
        time.sleep(10)

        added_val = write_new_element_to_file()
        print()
        print('*'*100)
        print(f'Добавлен новый элемент - {added_val}')
        print('Применяем алгоритм к текущей матрицы:')
        main_algorithm.main_process()
        print('*' * 100)
        print()

if __name__ == "__main__":
    main_realize()
