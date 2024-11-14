import random
import time
from threading import Thread
from queue import Queue


class Table:

    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        rand_time = random.randint(3, 10)
        time.sleep(rand_time)


class Cafe:

    def __init__(self, *tables):
        self.que = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests: Guest):
        guest_list = list(guests)
        counter = 0
        for table in self.tables:
            if table.guest is None:
                table.guest = guest_list.pop(counter)
                counter += 1
                table.guest.start()
                print(f'{table.guest.name} сел(-а) за стол номер {table.number}')
        if len(guest_list) > 0:
            for guest in guest_list:
                self.que.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not (self.que.empty()) or self.check_empty():
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None

                if table.guest is None and not self.que.empty():
                    table.guest = self.que.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    table.guest.start()


    def check_empty(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
print(tables)
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
# guests = [Guest(name) for name in guests_names]
guests = []
for guest in guests_names:
    new_guest = Guest(guest)
    guests.append(new_guest)
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
