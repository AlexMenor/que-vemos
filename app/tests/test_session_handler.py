import pytest

from ..data.session_store.in_memory_session_store import InMemorySessionStore
from ..session_handler import SessionHandler, SessionNotFound
from app.data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore


watchables_store = InMemoryWatchablesStore()
session_store = InMemorySessionStore()

@pytest.fixture
def session_handler():
    return SessionHandler(watchables_store, session_store)

@pytest.mark.asyncio
async def test_init_session(session_handler: SessionHandler):
    session_id = await session_handler.init_session()

    assert (await session_handler._SessionHandler__session_store.get_one(session_id)).id == session_id

@pytest.mark.asyncio
async def test_join_user_to_session_throw(session_handler: SessionHandler):
    session = await session_handler.init_session()

    with pytest.raises(SessionNotFound):
        await session_handler.join_user_to_session("no-soy-una-sesion")

@pytest.mark.asyncio
async def test_join_user_to_session(session_handler: SessionHandler):
    session_id = await session_handler.init_session()
    
    user_payload = await session_handler.join_user_to_session(session_id)

@pytest.mark.asyncio
async def test_emit_vote_throws_if_session_not_found(session_handler: SessionHandler):
    with pytest.raises(SessionNotFound):
        await session_handler.emit_vote_to_session('no existo', 'yo tampoco', 404, True)

