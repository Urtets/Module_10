import threading
import time


def write_words(word_count, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for i in range(1, word_count + 1):
            time.sleep(0.1)
            f.write(f'Какое-то слово № {i}' + '\n')
    print(f'Завершилась запись в файл {file_name}')


start_time = time.time()

write_words(10, 'example1.txt')
write_words(30, 'example2.txt')
write_words(200, 'example3.txt')
write_words(100, 'example4.txt')

print(f'Работа функций: {round(time.time() - start_time, 5)} секунд')


Thread1 = threading.Thread(target=write_words, args=(10, 'example5.txt'))
Thread2 = threading.Thread(target=write_words, args=(30, 'example6.txt'))
Thread3 = threading.Thread(target=write_words, args=(200, 'example7.txt'))
Thread4 = threading.Thread(target=write_words, args=(100, 'example8.txt'))

start_time = time.time()

Thread1.start()
Thread2.start()
Thread3.start()
Thread4.start()

Thread1.join()
Thread2.join()
Thread3.join()
Thread4.join()

print(f'Работа потоков: {round(time.time() - start_time, 5)} секунд')