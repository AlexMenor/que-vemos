""" Defines session class """

from typing import List, Dict
from functools import reduce
from .user import User
from .watchable import Watchable

class Session:
    """ Contains users, the watchables they are choosing from and their choices """

    MAX_USERS_PER_SESSION = 8
    def __init__(self, session_id: str, watchables: List[Watchable]):
        self.id = session_id
        self.__users: List[User] = []
        self.watchables = watchables
        self.__votes = {}

    def get_users(self) -> List[User]:
        return self.__users

    def add_user(self, new_user: User) -> None:
        if len(self.__users) < Session.MAX_USERS_PER_SESSION:
            self.__users.append(new_user)
        else:
            raise NotMoreUsersAllowedException

    def vote(self, user_id: str, watchable_index: int, vote: bool):
        self.__checkUserExists(user_id)
        self.__checkWatchableExists(watchable_index)

        if watchable_index not in self.__votes:
            watchable_current_votes = {}
        else:
            watchable_current_votes = self.__votes[watchable_index]

        watchable_current_votes[user_id] = vote

        self.__votes[watchable_index] = watchable_current_votes

    def is_match(self) -> bool:
        for watchable_index in self.__votes:
            if self.__count_yes(self.__votes[watchable_index]) == len(self.__users):
                return True
        return False

    def __checkUserExists(self, user_id: str):
        if len(list(filter(lambda u: u.id == user_id, self.__users))) != 1:
            raise UserNotFoundInSession

    def __checkWatchableExists(self, watchable_index: int):
        if watchable_index >= len(self.watchables):
            raise WatchableNotFound

    def __count_yes(self, votes_of_watchable: Dict) -> int :
        return reduce(lambda acum, vote: acum + 1 if votes_of_watchable[vote] else acum, votes_of_watchable, 0)


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
