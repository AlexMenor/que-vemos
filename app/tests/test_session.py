from ..entities.session_summary import SessionSummary
from ..entities.user import User
from ..entities.session import Session, NotMoreUsersAllowedException, UserNotFoundInSession, WatchableNotFound
from ..entities.watchable import Watchable, WatchableType

import pytest

@pytest.fixture
def user():
    return User("UnID")

@pytest.fixture
def watchables():
    watchable = Watchable("Narcos", "Se centra en la historia real de una peligrosa difusión y propagación de una red de cocaína por todo el mundo durante los años 70 y 80.", 2015, WatchableType.SERIES)
    return [watchable] 

@pytest.fixture
def session_with_user(watchables, user):
    session = Session("OtroID",  watchables)

    session.add_user(user)

    return session

@pytest.fixture
def session_with_vote_yes(session_with_user, user):
    session = session_with_user

    session.vote(user.id, 0, True)

    return session

def test_users_getter(session_with_user):
    assert session_with_user.get_users()[0].id is not None

def test_add_user(watchables):
    session = Session("OtroID", watchables)
    new_user = User("Nuevo_user")

    session.add_user(new_user)

    users = session.get_users()

    assert len(users) == 1
    assert users[0].id == new_user.id

def test_add_user_throws_exception(session_with_user):
    session = session_with_user
    new_user = User("OtroID")

    for i in range(0, Session.MAX_USERS_PER_SESSION - 1):
        session.add_user(new_user)

    with pytest.raises(NotMoreUsersAllowedException):
        session.add_user(new_user)

def test_vote(session_with_vote_yes, user):
    session = session_with_vote_yes

    assert session._Session__votes[0][user.id] == True

def test_vote_throws_if_not_found_user(session_with_user):
    session = session_with_user

    with pytest.raises(UserNotFoundInSession):
        session.vote("No existe", 0, True)

def test_vote_throws_if_not_found_watchable(user, session_with_user):
    session = session_with_user

    with pytest.raises(WatchableNotFound):
        session.vote(user.id, 1, True)

def test_count_yes(user, session_with_vote_yes):
    session = session_with_vote_yes

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, False)

    yes_votes, total_votes = session.get_votes_of_watchable(0)

    assert yes_votes == 1
    assert total_votes == 2

def test_count_yes_none_voted(session_with_user):
    session = session_with_user

    yes_votes, total_votes = session.get_votes_of_watchable(0)

    assert yes_votes == 0
    assert total_votes == 0

def test_is_match_positive(session_with_vote_yes):
    session = session_with_vote_yes

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, True)

    assert session.is_match() == True

def test_is_match_negative(session_with_vote_yes):
    session = session_with_vote_yes

    new_user = User("Nuevo_user")
    session.add_user(new_user)

    session.vote(new_user.id, 0, False)

    assert session.is_match() == False

def test_summary(session_with_vote_yes: Session, user, watchables):
    summary: SessionSummary = session_with_vote_yes.summary()

    assert summary.votes[0].title == watchables[0].title

    assert summary.votes[0].votes[0][0].id == user.id

    assert summary.votes[0].votes[0][1]

    assert summary.users[0].id == user.id

