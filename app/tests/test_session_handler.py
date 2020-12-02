import pytest

from ..data.in_memory_session_store import InMemorySessionStore
from ..session_handler import SessionHandler, SessionNotFound
from app.data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from ..entities.watchable import Watchable


watchables_store = InMemoryWatchablesStore()
session_store = InMemorySessionStore()

@pytest.fixture
def session_handler():
    return SessionHandler(watchables_store, session_store)

@pytest.mark.asyncio
async def test_init_session(session_handler: SessionHandler):
    session = await session_handler.init_session()

    assert isinstance(session.watchables[0], Watchable)

    assert await session_handler._SessionHandler__session_store.get_one(session.id) == session

@pytest.mark.asyncio
async def test_join_user_to_session_throw(session_handler: SessionHandler):
    session = await session_handler.init_session()

    with pytest.raises(SessionNotFound):
        await session_handler.join_user_to_session("no-soy-una-sesion")

@pytest.mark.asyncio
async def test_join_user_to_session(session_handler: SessionHandler):
    session = await session_handler.init_session()
    
    user_payload = await session_handler.join_user_to_session(session.id)

    assert session.get_users()[0].id == user_payload.user_id

    