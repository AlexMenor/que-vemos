""" Declares an implementation of SessionStore """

from app.entities.session import Session
from app.session_handler import SessionNotFound
from .session_store import SessionStore


class InMemorySessionStore(SessionStore):
    """
    This implementation of SessionStore
    stores session inside a dict where the
    keys are each session.id
    """
    def __init__(self):
        self.__sessions = {}

    async def save(self, session: Session) -> None:
        """
         If session already exists in the dict
         it makes no difference to assign the same
         reference again. If the user of this method
         makes a copy of a previously retrieved session
         it would still save the modified session
       """
        self.__sessions[session.id] = session

    async def get_one(self, session_id: str) -> Session:
        if session_id not in self.__sessions:
            raise SessionNotFound

        return self.__sessions[session_id]
