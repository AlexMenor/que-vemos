from ..entities.user import User
from ..entities.session import Session, NotMoreUsersAllowedException, UserNotFoundInSession, WatchableNotFound
from ..entities.watchable import Watchable

import pytest

@pytest.fixture
def user():
    return User("UnID")

@pytest.fixture
def watchables():
    watchable = Watchable("Narcos", "Se centra en la historia real de una peligrosa difusión y propagación de una red de cocaína por todo el mundo durante los años 70 y 80.", 2015)
    return [watchable] 


def test_users_getter(user, watchables):
    session = Session("OtroID", user, watchables)
    assert session.get_users()[0].id == user.id 

def test_add_user(user, watchables):
    session = Session("OtroID", user, watchables)
    new_user = User("Nuevo_user")

    session.add_user(new_user)

    users = session.get_users()

    assert len(users) == 2
    assert users[0].id == user.id
    assert users[1].id == new_user.id

def test_add_user_throws_exception(user, watchables):
    session = Session("OtroID", user, watchables)
    new_user = User("Nuevo_user")

    for i in range(0, Session.MAX_USERS_PER_SESSION - 1):
        session.add_user(new_user)

    with pytest.raises(NotMoreUsersAllowedException):
        session.add_user(new_user)

def test_vote(user, watchables):
    session = Session("OtroID", user, watchables)

    session.vote(user.id, 0, True)

    assert session._Session__votes[0][user.id] == True

def test_vote_throws_if_not_found_user(user, watchables):
    session = Session("OtroID", user, watchables)

    with pytest.raises(UserNotFoundInSession):
        session.vote("No existe", 0, True)

def test_vote_throws_if_not_found_watchable(user, watchables):
    session = Session("OtroID", user, watchables)

    with pytest.raises(WatchableNotFound):
        session.vote(user.id, 1, True)

def test_count_yes(user, watchables):
    session = Session("OtroID", user, watchables)

    session.vote(user.id, 0, True)

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, False)

    assert session._Session__count_yes(session._Session__votes[0]) == 1

def test_is_match_positive(user, watchables):
    session = Session("OtroID", user, watchables)

    session.vote(user.id, 0, True)

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, True)

    assert session.is_match() == True

def test_is_match_negative(user, watchables):
    session = Session("OtroID", user, watchables)

    session.vote(user.id, 0, True)

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, False)

    assert session.is_match() == False
