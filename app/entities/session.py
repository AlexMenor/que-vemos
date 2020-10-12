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
        self.__votes = {}

    def get_users(self) -> List[User]:
        return self.__users

    def add_user(self, new_user: User) -> None:
        if len(self.__users) < Session.MAX_USERS_PER_SESSION:
            self.__users.append(new_user)
        else:
            raise NotMoreUsersAllowedException
    
    def __checkUserExists(self, user_id: int):
        try:
            self.__users.index(user_id)
        except:
            raise UserNotFoundInSession
    
    def __checkWatchableExists(self, watchable_index: int):
        if watchable_index >= len(self.watchables):
            raise WatchableNotFound


    def vote(self, user_id: int, watchable_index: int, vote: bool):
        __checkUserExists(user_id)
        __checkWatchableExists(watchable_index)

        if watchable_index not in self.__votes:
            watchable_current_votes = {}
        else:
            watchable_current_votes = self.__votes[watchable_index]

        watchable_current_votes[user_id] = vote

        self.__votes[watchable_index] = watchable_current_votes



class NotMoreUsersAllowedException(Exception):
    """ Exception raised when the number of users in a session is already the maximum """
    def __init__(self):
        self.message = "The session already have the maximum number of users allowed"
        super().__init__(self.message)

class UserNotFoundInSession(Exception):
    """ Exception raised when the user is not found in the session"""
    def __init__(self):
        self.message = "There is no user with such id in the session"
        super().__init__(self.message)

class WatchableNotFound(Exception):
    """ Exception raised when the watchable is not found in the session"""
    def __init__(self):
        self.message = "There is no watchable with such index in the session"
        super().__init__(self.message)