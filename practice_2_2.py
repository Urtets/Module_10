import pprint
import requests
from threading import Thread, Event
import queue


CLIENT_ID = 'X4DlFyVDCXWKHRLYkq7wiM959JxZMZIQiggNobRONyEjcKgxzleb26dI9hNeupQv'
CLIENT_SECRET = 'uasMvLLbqXbw12DfWONMvRYBu6uQe1gw7CfFjMDvNtyXwitUj0cG6J81udrhxjIH8A_k2K4cbok_z54sW7aRFQ'
# ACCESS_TOKEN = 'CXyFeSBw2lAdG41xkuU3LS6a_nwyxwwCz2dCkUohw-rw0C49x2HqP__6_4is5RPx'
ACCESS_TOKEN2 = '3XmVgLYkiuRV1X_2j7YLdyNH65neWaEfYNX7SBU54hbcVVcgxfnYJ09FrOKYvMGT'
RANDOM_GENRE_API_URL = 'https://binaryjazz.us/wp-json/genrenator/v1/genre/'
GENIUS_API_URL = 'https://api.genius.com/search'
# GENIUS_API_URL2 = 'https://api.genius.com/search?q='
GENIUS_URL = 'https://genius.com'
# genius_search_url = f"http://api.genius.com/search?q=jazz&access_token={ACCESS_TOKEN2}"


all_songs = []


class GetGenre(Thread):

    def __init__(self, queue, stop_event):
        self.queue = queue
        self.stop_event = stop_event
        super().__init__()


    def run(self):
        while not self.stop_event.is_set():
            genre = requests.get(RANDOM_GENRE_API_URL).json()
            # genre = requests.get(RANDOM_GENRE_API_URL)
            # print(genre)
            self.queue.put(genre)


class Genius(Thread):

    def __init__(self, queue):
        self.queue = queue
        super().__init__()


    def run(self):
        genre = self.queue.get()
        # print('genre:', genre)
        print(self.queue.qsize())
        data = requests.get(GENIUS_API_URL, params={'access_token': ACCESS_TOKEN2, 'q': genre})
        # data = requests.get(genius_search_url)
        # print('data:', data)
        data = data.json()
        print(data)
        try:
            song_id = data['response']['hits'][0]['result']['api_path']
            all_songs.append({'genre': genre, 'song': f'{GENIUS_URL}{song_id}'})
        except IndexError as e:
            self.run()
            print(e)
            # pass


queue = queue.Queue()
stop_event = Event()
counter = 10
genre_list = []
genius_list = []

for _ in range(4):
    t = GetGenre(queue, stop_event)
    t.start()
    genre_list.append(t)

for _ in range(20):
    t = Genius(queue)
    t.start()
    genius_list.append(t)

for t in genius_list:
    t.join()
# stop_event.set()

for t in genre_list:
    t.join()

stop_event.set()

print(queue.qsize())
pprint.pprint(all_songs)
print(len(all_songs))