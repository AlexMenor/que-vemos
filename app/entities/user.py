""" Contains user entity """

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """ An user represents a client of the service that has joined / started a session """
    id: str
    name: Optional[str] = None
