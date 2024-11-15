import datetime
import multiprocessing as mp
from PIL import Image
from queue import Empty

def realize_image(image_paths, pipe: mp.Pipe, stop_event):
    for image_path in image_paths:
        image = Image.open(image_path)
        image = image.resize((800, 600))
        image.save(image_path)
        pipe.send(image_path)
    stop_event.set()

def change_color(pipe: mp.Pipe, stop_event):
    while not stop_event.is_set():

        image_path = pipe.recv()

        image = Image.open(image_path)
        image = image.convert('L')
        image.save(image_path)

if __name__ == '__main__':
    data = []
    # queue = mp.Queue()
    conn1, conn2 = mp.Pipe()
    stop_event = mp.Event()
    for image in range(1, 3):
        data.append(f'./images/img_{image}.jpg')

    realize_process = mp.Process(target=realize_image, args=(data, conn1, stop_event))
    change_process = mp.Process(target=change_color, args=(conn2, stop_event))
    start = datetime.datetime.now()
    realize_process.start()
    change_process.start()

    realize_process.join()
    change_process.join()
    end = datetime.datetime.now()
    print(end - start)