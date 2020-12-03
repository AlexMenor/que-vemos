from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from.session_handler import SessionHandler
from .data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from .data.watchables_store.watchables_store import WatchablesStore
from .data.session_store.in_memory_session_store import InMemorySessionStore
from .data.session_store.session_store import SessionStore

watchables_store: WatchablesStore = InMemoryWatchablesStore()

session_store: SessionStore = InMemorySessionStore()

session_handler = SessionHandler(watchables_store, session_store)


async def create_session(_):
    session_id = await session_handler.init_session()
    response = JSONResponse({'session_id': session_id})
    response.status_code = 201
    return response


app = Starlette(debug=True, routes=[
    Route('/session', create_session, methods=['POST']),
])