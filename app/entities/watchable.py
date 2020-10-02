""" This module contains watchable entity """

from dataclasses import dataclass

@dataclass
class Watchable:
    """ Represents something you can watch in a streaming platform """
    title: str
    synopsis: str
    year: int
