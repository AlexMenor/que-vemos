""" Defines SessionHandler class """

import uuid
from typing import Callable, List
from .entities.user import User
from .entities.session import Session
from .entities.user_payload import UserPayload
from .entities.watchable import Watchable


class SessionHandler:
    """ Handles all active sessions, represents an entrypoint for business logic """

    def __init__(self, get_watchables: Callable[[], List[Watchable]]):
        self.__sessions = {}
        self.__get_watchables = get_watchables

    def init_session(self) -> UserPayload:
        session_id = SessionHandler.gen_random_id()

        first_user = SessionHandler.__create_user()

        session = Session(session_id, first_user, self.__get_watchables())

        self.__save_session(session)

        return UserPayload(first_user.id, session_id, session.watchables)

    def join_user_to_session(self, session_id: str):
        if session_id not in self.__sessions:
            raise SessionNotFound

        session = self.__sessions[session_id]

        new_user = SessionHandler.__create_user()
        session.add_user(new_user)

        return UserPayload(new_user.id, session_id, session.watchables)

    def __save_session(self, session: Session):
        self.__sessions[session.id] = session

    @staticmethod
    def __create_user():
        user_id = SessionHandler.gen_random_id()
        return User(user_id)

    @staticmethod
    def gen_random_id() -> str:
        return uuid.uuid4()


class SessionNotFound(Exception):
    """ Exception raised when a Session is not found in this handler"""
    def __init__(self):
        self.message = "There is no session with such id"
        super().__init__(self.message)