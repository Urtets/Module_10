import threading
import random
import time


class Bank(threading.Thread):

    def __init__(self):
        super().__init__()
        self.balance = 0
        self.lock = threading.Lock()


    def deposit(self):
        transactions = 100
        random_number = 0
        for i in range(transactions):
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            random_number = random.randint(50, 500)
            self.balance += random_number
            print(f'Пополнение: {random_number}. Баланс: {self.balance}')
            time.sleep(0.001)


    def take(self):
        transactions = 100
        random_number = 0
        for i in range(transactions):
            print(f'Запрос на {random_number}')
            random_number = random.randint(50, 500)
            if random_number > self.balance:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()
            else:
                self.balance -= random_number
                print(f'Снятие: {random_number}. Баланс: {self.balance}')
                time.sleep(0.001)


if __name__ == '__main__':
    bk = Bank()

    # Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')