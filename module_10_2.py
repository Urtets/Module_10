import threading
import time


class Knight(threading.Thread):

    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.enemies = 100

    def run(self):
        print(f'{self.name}, на нас напали!')
        counter = 0
        while self.enemies > 0:
            self.enemies -= self.power
            time.sleep(1)
            counter += 1
            print(f'{self.name} сражается {counter}, осталось {self.enemies} воинов')
        print(f'{self.name} одержал победу спустя {counter} дней(дня)!')



if __name__ == "__main__":
    # Создание класса
    first_knight = Knight('Sir Lancelot', 10)
    second_knight = Knight("Sir Galahad", 20)
    # Запуск потоков и остановка текущего
    first_knight.start()
    second_knight.start()
    # Вывод строки об окончании сражения