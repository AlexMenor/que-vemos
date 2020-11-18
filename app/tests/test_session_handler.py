import pytest
from ..session_handler import SessionHandler, SessionNotFound
from ..entities.watchable import Watchable, WatchableType

def get_watchables():
    watchable = Watchable("Narcos", "Se centra en la historia real de una peligrosa difusión y propagación de una red de cocaína por todo el mundo durante los años 70 y 80.", 2015, WatchableType.SERIES)
    return [watchable]

@pytest.fixture
def session_handler():
    return SessionHandler(get_watchables)

def test_init_session(session_handler: SessionHandler):
    session = session_handler.init_session()

    assert session.watchables[0] == get_watchables()[0]

    sessions = session_handler._SessionHandler__sessions

    assert session.id in sessions

def test_join_user_to_session_throw(session_handler: SessionHandler):
    session = session_handler.init_session()

    with pytest.raises(SessionNotFound):
        session_handler.join_user_to_session("no-soy-una-sesion")

def test_join_user_to_session(session_handler: SessionHandler):
    session = session_handler.init_session()
    
    user_payload = session_handler.join_user_to_session(session.id)

    assert session.get_users()[0].id == user_payload.user_id

    