from fastapi import FastAPI

from.session_handler import SessionHandler
from .data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from .data.watchables_store.watchables_store import WatchablesStore
from .data.session_store.in_memory_session_store import InMemorySessionStore
from .data.session_store.session_store import SessionStore

watchables_store: WatchablesStore = InMemoryWatchablesStore()

session_store: SessionStore = InMemorySessionStore()

session_handler = SessionHandler(watchables_store, session_store)


app = FastAPI()

@app.post("/session")
async def create_session():
    session_id = await session_handler.init_session()
    return {"session_id": session_id}