from abc import ABC, abstractmethod

from ..entities.session import Session

class SessionStore(ABC):
    @abstractmethod
    async def save(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id: str) -> Session:
        raise NotImplementedError
