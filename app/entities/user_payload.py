""" Defines UserPayload class """

from dataclasses import dataclass
from typing import List
from .watchable import Watchable


@dataclass
class UserPayload:
    """ Represents the information that an user should have after joining the session"""
    user_id: str
    session_id: str
    watchables: List[Watchable]
