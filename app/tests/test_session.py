from ..entities.user import User
from ..entities.session import Session
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

