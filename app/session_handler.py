""" Defines SessionHandler class """

import uuid

from .data.session_store.session_store import SessionStore
from .entities.user import User
from .entities.session import Session
from .entities.user_payload import UserPayload
from .data.watchables_store.watchables_store import WatchablesStore


class SessionHandler:
    """ Handles all active sessions, represents an entrypoint for business logic """

    NUM_OF_WATCHABLES_PER_SESSION = 20

    def __init__(self, watchables_store: WatchablesStore, session_store: SessionStore):
        self.__session_store = session_store
        self.__watchables_store = watchables_store

    async def init_session(self) -> str:
        session_id = SessionHandler.gen_random_id()

        watchables = await self.__watchables_store.\
            get_some_watchables(SessionHandler.NUM_OF_WATCHABLES_PER_SESSION)

        session = Session(session_id, watchables)

        await self.__session_store.save(session)

        return session.id

    async def join_user_to_session(self, session_id: str) -> UserPayload:

        session = await self.__session_store.get_one(session_id)

        new_user = SessionHandler.__create_user()
        session.add_user(new_user)

        await self.__session_store.save(session)

        return UserPayload(new_user.id, session_id, session.watchables)

    async def emit_vote_to_session(self, session_id: str, user_id: str, watchable_index: int, vote: bool) -> None:
        session = await self.__session_store.get_one(session_id)

        session.vote(user_id, watchable_index, vote)

        await self.__session_store.save(session)


    @staticmethod
    def __create_user():
        user_id = SessionHandler.gen_random_id()
        return User(user_id)

    @staticmethod
    def gen_random_id() -> str:
        return str(uuid.uuid4())


class SessionNotFound(Exception):
    """ Exception raised when a Session is not found in this handler"""
    def __init__(self):
        self.message = "There is no session with such id"
        super().__init__(self.message)
