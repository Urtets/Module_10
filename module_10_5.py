import multiprocessing
import threading
import logging
import time

def read_info(name):
    all_data = []
    with open(name, 'r') as file_read:
        for line in file_read:
            readline = line
            all_data.append(readline)
    # print(all_data)


def worker(name, begin_time):
    logging.debug('Begin')
    all_data = []
    with open(name, 'r') as file_read:
        for line in file_read:
            readline = line
            all_data.append(readline)
    logging.debug('Finish')
    print(time.time() - begin_time)

filenames = [f'.//file {number}.txt' for number in range(1, 5)]

if __name__ == '__main__':
    beginning = time.time()
    with multiprocessing.Pool(processes=len(filenames)) as pool:
        results = pool.map(read_info, filenames)
    lapsed_time = time.time() - beginning
    print("многопроцессный", round(lapsed_time, 5))
    beginning = time.time()
    for name in filenames:
        read_info(name)
    lapsed_time = time.time() - beginning
    print("линейный", round(lapsed_time, 5))

    beginning = time.time()
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    threads = []
    for i in range(len(filenames)):
        thread = threading.Thread(target=worker, args=(filenames[i], beginning), name=f'Worker-{i}')
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    logging.debug(str(time.time() - beginning))
