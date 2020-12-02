import pytest
from ..session_handler import SessionHandler, SessionNotFound
from ..data.in_memory_watchables_store import InMemoryWatchablesStore
from ..entities.watchable import Watchable


watchables_store = InMemoryWatchablesStore()

@pytest.fixture
def session_handler():
    return SessionHandler(watchables_store)

def test_init_session(session_handler: SessionHandler):
    session = session_handler.init_session()

    assert isinstance(session.watchables[0], Watchable)

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

    