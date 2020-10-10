""" Defines session class """

from dataclasses import dataclass
from typing import List
from .user import User
from .watchable import Watchable

@dataclass
class Session:
    """ Contains users, the watchables they are choosing from and their choices """
    id: str
    users: List[User]
    watchables: List[Watchable]
