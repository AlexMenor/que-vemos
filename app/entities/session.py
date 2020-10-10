""" Defines session class """

from typing import List
from .user import User
from .watchable import Watchable

class Session:
    """ Contains users, the watchables they are choosing from and their choices """

    MAX_USERS_PER_SESSION = 8
    def __init__(self, session_id: str, first_user: User, watchables: List[Watchable]):
        self.id = session_id
        self.__users: List[User] = [first_user]
        self.watchables = watchables

    def get_users(self) -> List[User]:
        return self.__users

    def add_user(self, new_user: User) -> None:
        if len(self.__users) < Session.MAX_USERS_PER_SESSION:
            self.__users.append(new_user)
        else:
            raise NotMoreUsersAllowedException

class NotMoreUsersAllowedException(Exception):
    """ Exception raised when the number of users in a session is already the maximum """
    def __init__(self):
        self.message = "The session already have the maximum number of users allowed"
        super().__init__(self.message)
