""" This module contains watchable entity """

from dataclasses import dataclass
from typing import Optional
from enum import Enum

class WatchableType(str, Enum):
    """ Represent the type of watchable """
    MOVIE = 'MOVIE'
    SERIES = 'SERIES'

@dataclass
class Watchable:
    """ Represents something you can watch in a streaming platform """
    title: str
    synopsis: str
    year: int
    type: WatchableType
    poster: Optional[str] = None
    popularity: Optional[float] = None
