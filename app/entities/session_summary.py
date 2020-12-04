from dataclasses import dataclass
from typing import List, Tuple

from .user import User

@dataclass
class WatchableSummary:
    title: str
    votes: List[Tuple[User, bool]]

@dataclass
class SessionSummary:
    users: List[User]
    votes: List[WatchableSummary]

