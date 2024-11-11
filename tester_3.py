import threading

counter = 0
lock = threading.Lock()
print(lock.locked())

def increment(name):
    global counter
    # lock.acquire()
    with lock:
        for i in range(1000):
            counter += 1
            print(name, counter)
    # lock.release()


def decrement(name):
    global counter
    # lock.acquire()
    try:
        lock.acquire()
        for i in range(1000):
            counter -= 1
            print(name, counter)
    except Exception:
        pass
    finally:
        lock.release()


thread1 = threading.Thread(target=increment, args=('thread1',))
thread2 = threading.Thread(target=decrement, args=('thread2',))
thread3 = threading.Thread(target=increment, args=('thread3',))
thread4 = threading.Thread(target=decrement, args=('thread4',))

thread1.start()
thread3.start()
thread2.start()
thread4.start()