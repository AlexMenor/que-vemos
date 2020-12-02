from .session_store import SessionStore
from app.entities.session import Session
from app.session_handler import SessionNotFound


class InMemorySessionStore(SessionStore):
    def __init__(self):
        self.__sessions = {}

    async def save(self, session: Session) -> None:
        # If session already exists in the dict
        # it makes no difference to assign the same
        # reference again
        self.__sessions[session.id] = session

    async def get_one(self, session_id: str) -> Session:
        if session_id not in self.__sessions:
            raise SessionNotFound

        return self.__sessions[session_id]
