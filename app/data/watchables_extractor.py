import http.client
import json
import os
from .data_request_exception import DataRequestException
from ..entities.watchable import Watchable, WatchableType
from typing import List
from pickle import Pickler

MOVIE_DB_API_KEY = os.getenv('MOVIE_DB_API_KEY')
MOVIE_DB_URL = "api.themoviedb.org"
MOVIE_DB_PATH = "/3/trending/all/day?api_key={}".format(MOVIE_DB_API_KEY)

MOVIE_DB_IMG_BASE_PATH = "https://image.tmdb.org/t/p/w500/"

PAGES_TO_FETCH = 2

connection = http.client.HTTPSConnection(MOVIE_DB_URL)

def fetch_data(page=1):
    connection.request("GET", MOVIE_DB_PATH + '&page={}'.format(page))

    res = connection.getresponse()

    if res.status != 200:
        raise DataRequestException

    return json.load(res)

def parse_watchable(item):
    type = item['media_type']
    if type == 'movie':
        year = item['release_date'].split('-')[0]
        watchable_type = WatchableType.MOVIE
        title = item['title']
    else:
        year = item['first_air_date'].split('-')[0]
        watchable_type = WatchableType.SERIES
        title = item['name']

    return Watchable(title, item['overview'], year, watchable_type, MOVIE_DB_IMG_BASE_PATH + item['poster_path'])

def parse_list(list) -> List[Watchable]:
    result = []
    for item in list:
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

    with open('serialized_data', 'wb+') as file:
        Pickler(file).dump(all_watchables)


if __name__ == '__main__':
    if MOVIE_DB_API_KEY is None:
        raise Exception('MOVIE_DB_API_KEY is needed')
    main()


