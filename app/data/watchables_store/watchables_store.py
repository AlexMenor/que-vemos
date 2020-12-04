""" Declares WatchableStore interface"""

from abc import ABC, abstractmethod
from typing import List

from app.entities.watchable import Watchable


class WatchablesStore(ABC):
    """ A watchables store just... stores watchables """
    @abstractmethod
    async def get_some_watchables(self, n: int) -> List[Watchable]:
        raise NotImplementedError
