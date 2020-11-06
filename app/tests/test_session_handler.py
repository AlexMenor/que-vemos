import pytest
from ..session_handler import SessionHandler
from ..entities.watchable import Watchable

def get_watchables():
    watchable = Watchable("Narcos", "Se centra en la historia real de una peligrosa difusión y propagación de una red de cocaína por todo el mundo durante los años 70 y 80.", 2015)
    return [watchable] 

@pytest.fixture
def session_handler():
    return SessionHandler(get_watchables)

def test_init_session(session_handler: SessionHandler):
    session = session_handler.init_session()

    assert session.watchables[0] == get_watchables()[0]

    sessions = session_handler._SessionHandler__sessions

    assert session.id in sessions

