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

    @abstractmethod
    async def get_one_and_lock(self, session_id: str) -> Session:
        raise NotImplementedError


class SessionNotFound(Exception):
    """ Exception raised when a Session is not found in this handler"""
    def __init__(self):
        self.message = "There is no session with such id"
        super().__init__(self.message)