from pickle import Unpickler
from typing import List
import random

from .watchables_store import WatchablesStore
from .watchables_extractor import PICKLE_SERIALIZED_DATA_PATH
from ..entities.watchable import Watchable

class InMemoryWatchablesStore(WatchablesStore):
    def __init__(self):
        self.__watchables = Unpickler(PICKLE_SERIALIZED_DATA_PATH).load()

    def get_some_watchables(self, n: int) -> List[Watchable]:
        return random.sample(self.__watchables, n)
