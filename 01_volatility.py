# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
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
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>

#  написать код в однопоточном/однопроцессорном стиле

import pandas
from os import listdir
from os.path import isfile, join
from threading import Thread
import time


class Exchange(Thread):


    def __init__(self, path):
        super().__init__()
        self.path = path
        self.dict_of_results = {}
        self.max_volatility_3 = []
        self.min_volatility_3 = []
        self.zero_list = []

    def run(self):
        files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for file in files:
            ticket_file = pandas.read_csv(self.path + file)
            whole_size = len(ticket_file['PRICE'])
            min = ticket_file['PRICE'][0]
            max = ticket_file['PRICE'][0]
            for price_per_piece in range(whole_size):
                a_share = ticket_file['PRICE'][price_per_piece]
                if min > a_share:
                    min = a_share
                if max < a_share:
                    max = a_share

            # name = ticket_file[ticket_file.keys()[0]][0]
            # print(self.dict_of_results)
            average = (max + min) / 2
            volatility = ((max - min) / average) * 100
            self.dict_of_results[ticket_file[ticket_file.keys()[0]][0]] = float(round(volatility, 2))
        self.max_volatility_3 = self.find_max_stick()
        self.min_volatility_3 = self.find_min_stick()
        self.zero_list = self.find_zero_stick()

    def find_max_stick(self):
        max_1 = 0
        key_1 = ''
        max_2 = 0
        key_2 = ''
        max_3 = 0
        key_3 = ''
        for key, value in self.dict_of_results.items():
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

    def find_min_stick(self):
        min_1 = 100
        key_1 = ''
        min_2 = 100
        key_2 = ''
        min_3 = 100
        key_3 = ''
        for key, value in self.dict_of_results.items():
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

    def find_zero_stick(self):
        zero = 0
        key_1 = ''
        zero_list_1 = []
        for key, value in self.dict_of_results.items():
            if value == zero:
                zero = value
                key_1 = key
                zero_list_1.append(f'{key_1} - {zero}')
        return zero_list_1


    def show_result(self):
        print(self.max_volatility_3)
        print(self.min_volatility_3)
        print(self.zero_list)


start_time = time.time()

volatility_check = Exchange('trades/')
volatility_check.start()
volatility_check.join()
volatility_check.show_result()

end_time = round(time.time() - start_time, 2)
print(end_time)
# files = [f for f in listdir('trades/') if isfile(join('trades/', f))]
# # print(files)
# info = pandas.read_csv('trades/TICKER_ALH9.csv')
# info2 = info.keys()
# print(info2)
# whole_size = len(info['PRICE'])
# min = info['PRICE'][0]
# max = info['PRICE'][0]
# for price_per_piece in range(whole_size):
#     a_share = info['PRICE'][price_per_piece]
#     if min > a_share:
#         min = a_share
#     if max < a_share:
#         max = a_share
# print(max)
# print(min)
#
# average = (max + min) / 2
# volatility = ((max - min) / average) * 100
# print('Средняя', average)
# print('Волатильность', round(volatility), '%')
