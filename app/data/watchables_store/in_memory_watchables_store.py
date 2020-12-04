""" Declares an implementation of the interface WatchablesStore"""

from pickle import Unpickler
from typing import List
import random

from app.data.watchables_extractor.watchables_extractor import PICKLE_SERIALIZED_DATA_PATH
from app.entities.watchable import Watchable
from .watchables_store import WatchablesStore

class InMemoryWatchablesStore(WatchablesStore):
    """ This implementation of WatchablesStore just reads a previously
        serialized data and returns it from memory """
    def __init__(self):
        with open(PICKLE_SERIALIZED_DATA_PATH, 'rb') as file:
            self.__watchables = Unpickler(file).load()

    async def get_some_watchables(self, n: int) -> List[Watchable]:
        return random.sample(self.__watchables, n)
