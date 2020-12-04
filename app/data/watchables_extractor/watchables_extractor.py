"""

Script to fetch and parse data from The Movie DB,
instantiate application entities and serialized them

"""

import http.client
import json
import os
from typing import List
from pickle import Pickler
from app.data.watchables_extractor.data_request_exception import DataRequestException
from app.entities.watchable import Watchable, WatchableType

MOVIE_DB_API_KEY = os.getenv('MOVIE_DB_API_KEY')
MOVIE_DB_URL = "api.themoviedb.org"
MOVIE_DB_PATH = "/3/trending/all/day?api_key={}".format(MOVIE_DB_API_KEY)

MOVIE_DB_IMG_BASE_PATH = "https://image.tmdb.org/t/p/w500/"

PICKLE_SERIALIZED_DATA_PATH = "./app/data/watchables_extractor/serialized_data"
JSON_SERIALIZED_DATA_PATH = "./app/serverless/serialized_data.json"

PAGES_TO_FETCH = 2

connection = http.client.HTTPSConnection(MOVIE_DB_URL)


def fetch_data(page=1):
    connection.request("GET", MOVIE_DB_PATH + '&page={}'.format(page))

    res = connection.getresponse()

    if res.status != 200:
        raise DataRequestException

    return json.load(res)

def parse_watchable(item):
    media_type = item['media_type']
    if media_type == 'movie':
        if 'release_date' in item:
            year = item['release_date'].split('-')[0]
        else:
            year = None
        watchable_type = WatchableType.MOVIE
        title = item['title']
    else:
        if 'first_air_date' in item:
            year = item['first_air_date'].split('-')[0]
        else:
            year = None
        watchable_type = WatchableType.SERIES
        title = item['name']

    return Watchable(title, item['overview'], year, watchable_type,
                     MOVIE_DB_IMG_BASE_PATH + item['poster_path'],
                     popularity=item['popularity'])

def parse_list(item_list) -> List[Watchable]:
    result = []
    for item in item_list:
        if item['media_type'] == 'tv' or item['media_type'] == 'movie':
            result.append(parse_watchable(item))

    return result

def main():
    all_watchables = []

    for i in range(PAGES_TO_FETCH):
        data = fetch_data(i+1)

        list_of_items = data['results']

        list_of_watchables = parse_list(list_of_items)

        all_watchables += list_of_watchables

    with open(PICKLE_SERIALIZED_DATA_PATH, 'wb+') as pickle_file:
        Pickler(pickle_file).dump(all_watchables)

    with open(JSON_SERIALIZED_DATA_PATH, 'w+') as json_file:
        json.dump(all_watchables, json_file, sort_keys=True, indent=4, default=lambda o: o.__dict__)


if __name__ == '__main__':
    if MOVIE_DB_API_KEY is None:
        raise Exception('MOVIE_DB_API_KEY is needed')
    main()
