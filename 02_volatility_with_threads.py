# -*- coding: utf-8 -*-
import time

# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
#  Внимание! это задание можно выполнять только после зачета lesson_012/01_volatility.py !!!

# тут ваш код в многопоточном стиле

import pandas
import queue
from os import listdir
from os.path import isfile, join
from threading import Thread


class Exchange(Thread):

    def __init__(self, file_info, file_dict):
        super().__init__()
        self.file_info = file_info
        self.file_dict = file_dict

    def run(self):
        whole_size = len(self.file_info['PRICE'])
        min = self.file_info['PRICE'][0]
        max = self.file_info['PRICE'][0]
        for price_per_piece in range(whole_size):
            a_share = self.file_info['PRICE'][price_per_piece]
            if min > a_share:
                min = a_share
            if max < a_share:
                max = a_share

        average = (max + min) / 2
        volatility = ((max - min) / average) * 100
        name = self.file_info['SECID'][0]
        value = float(round(volatility, 2))
        # print(f'{name} - {value}')

        self.file_dict[name] = value


def find_max_stick(dict_of_results):
    max_1 = 0
    key_1 = ''
    max_2 = 0
    key_2 = ''
    max_3 = 0
    key_3 = ''
    for key, value in dict_of_results.items():
        if value > max_1:
            max_1 = value
            key_1 = key
        if max_1 > value > max_2:
            max_2 = value
            key_2 = key
        if max_2 > value > max_3:
            max_3 = value
            key_3 = key
    return [f'{key_1} - {max_1}', f'{key_2} - {max_2}', f'{key_3} - {max_3}']


def find_min_stick(dict_of_results):
    min_1 = 100
    key_1 = ''
    min_2 = 100
    key_2 = ''
    min_3 = 100
    key_3 = ''
    for key, value in dict_of_results.items():
        if value != 0:
            if value < min_1:
                min_1 = value
                key_1 = key
            if min_1 < value < min_2:
                min_2 = value
                key_2 = key
            if min_2 < value < min_3:
                min_3 = value
                key_3 = key
    return [f'{key_1} - {min_1}', f'{key_2} - {min_2}', f'{key_3} - {min_3}']


def find_zero_stick(dict_of_results):
    zero = 0
    key_1 = ''
    zero_list_1 = []
    for key, value in dict_of_results.items():
        if value == zero:
            zero = value
            key_1 = key
            zero_list_1.append(f'{key_1} - {zero}')
    return zero_list_1


def show_result(dict_of_results):
    print(find_max_stick(dict_of_results))
    print(find_min_stick(dict_of_results))
    print(find_zero_stick(dict_of_results))


start_time = time.time()

path = 'trades/'
files = [f for f in listdir(path) if isfile(join(path, f))]
file_dict = {}
for file in files:

    ticker_file = pandas.read_csv(path + file)
    exchange = Exchange(ticker_file, file_dict)
    exchange.start()

show_result(file_dict)
end_time = round(time.time() - start_time, 2)
print(end_time)