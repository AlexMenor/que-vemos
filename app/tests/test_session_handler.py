import pytest

from ..data.session_store.in_memory_session_store import InMemorySessionStore
from ..data.session_store.session_store import SessionStore, SessionNotFound
from ..entities.session import UserNotFoundInSession, WatchableNotFound
from ..entities.watchable import Watchable
from ..session_handler import SessionHandler
from app.data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore


@pytest.fixture
def watchables_store():
    return InMemoryWatchablesStore()

@pytest.fixture
def session_store():
    return InMemorySessionStore()

@pytest.fixture
def session_handler(watchables_store, session_store):
    return SessionHandler(watchables_store, session_store)

@pytest.fixture
async def session_handler_with_session(session_handler):
    session_id = await session_handler.init_session()
    return session_handler, session_id

@pytest.fixture
async def session_handler_with_session_and_user(session_handler_with_session):
    session_handler = session_handler_with_session[0]
    session_id = session_handler_with_session[1]

    user_payload = await session_handler.join_user_to_session(session_id)

    return session_handler, user_payload


@pytest.mark.asyncio
async def test_init_session(session_handler: SessionHandler, session_store):
    session_id = await session_handler.init_session()

    assert (await session_store.get_one(session_id)).id == session_id

@pytest.mark.asyncio
async def test_join_user_to_session_throw(session_handler: SessionHandler):
    await session_handler.init_session()

    with pytest.raises(SessionNotFound):
        await session_handler.join_user_to_session("no-soy-una-sesion")

@pytest.mark.asyncio
async def test_join_user_to_session(session_handler: SessionHandler, session_store: SessionStore):
    session_id = await session_handler.init_session()
    
    user_payload = await session_handler.join_user_to_session(session_id)

    assert user_payload.user_id is not None

    assert user_payload.session_id == session_id

    assert isinstance(user_payload.watchables[0], Watchable)

    assert len(user_payload.watchables) == SessionHandler.NUM_OF_WATCHABLES_PER_SESSION

    assert (await session_store.get_one(session_id)).get_users()[0].id == user_payload.user_id

@pytest.mark.asyncio
async def test_emit_vote_throws_if_session_not_found(session_handler: SessionHandler):
    with pytest.raises(SessionNotFound):
        await session_handler.emit_vote_to_session('no existo', 'yo tampoco', 404, True)

@pytest.mark.asyncio
async def test_emit_vote_throws_if_user_not_found(session_handler_with_session):
    session_handler = session_handler_with_session[0]
    session_id = session_handler_with_session[1]

    with pytest.raises(UserNotFoundInSession):
        await session_handler.emit_vote_to_session(session_id, 'yo tampoco', 404, True)

@pytest.mark.asyncio
async def test_emit_vote_throws_if_watchable_index_out_of_bounds(session_handler_with_session_and_user):
    session_handler = session_handler_with_session_and_user[0]
    user_payload = session_handler_with_session_and_user[1]

    with pytest.raises(WatchableNotFound):
        await session_handler.emit_vote_to_session(user_payload.session_id, user_payload.user_id, 404, True)
