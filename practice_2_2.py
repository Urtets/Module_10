import pprint
import requests
from threading import Thread, Event
import queue

ACCESS_TOKEN = 'CXyFeSBw2lAdG41xkuU3LS6a_nwyxwwCz2dCkUohw-rw0C49x2HqP__6_4is5RPx'
RANDOM_GENRE_API_URL = 'https://binaryjazz.us/wp-json/generator/v1/genre/'
GENIUS_API_URL = 'https://api.genius.com/search'
GENIUS_URL = 'https://genius.com'


all_songs = []


class GetGenre(Thread):

    def __init__(self, queue, counter):
        self.queue = queue
        self.counter = counter
        super().__init__()


    def run(self):
        while len(all_songs) < counter:
            # genre = requests.get(RANDOM_GENRE_API_URL).json()
            genre = requests.get(RANDOM_GENRE_API_URL)
            self.queue.put(genre)


class Genius(Thread):

    def __init__(self, queue):
        self.queue = queue
        super().__init__()


    def run(self):
        genre = self.queue.get()
        data = requests.get(GENIUS_API_URL, params={'access_token': ACCESS_TOKEN, 'q': genre})
        data = data.json()
        try:
            song_id = data['response']['hits'][0]['result']['api_path']
            all_songs.append({'genre': genre, 'song': f'{GENIUS_URL}{song_id}'})
        except IndexError as e:
            # self.run()
            pass


queue = queue.Queue()
# stop_event = Event()
counter = 10
genre_list = []
genius_list = []

for _ in range(10):
    t = GetGenre(queue, counter)
    t.start()
    genre_list.append(t)

for _ in range(counter):
    t = Genius(queue)
    t.start()
    genius_list.append(t)

for t in genius_list:
    t.join()
# stop_event.set()

for t in genre_list:
    t.join()

print(queue.qsize())
pprint.pprint(all_songs)
print(len(all_songs))