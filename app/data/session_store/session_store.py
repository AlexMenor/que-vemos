""" Declares the interface of SessionStore """

from abc import ABC, abstractmethod

from app.entities.session import Session

class SessionStore(ABC):
    """
    This interface allows logic to retrieve and
    persists sessions
    """
    @abstractmethod
    async def save(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, session_id: str) -> Session:
        raise NotImplementedError
