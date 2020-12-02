from abc import ABC, abstractmethod
from typing import List

from ..entities.watchable import Watchable


class WatchablesStore(ABC):
    @abstractmethod
    async def get_some_watchables(self, n: int) -> List[Watchable]:
        raise NotImplementedError
