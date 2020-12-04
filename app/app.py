from fastapi import FastAPI, HTTPException

from .entities.user_payload import UserPayload
from .session_handler import SessionHandler
from .data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from .data.watchables_store.watchables_store import WatchablesStore
from .data.session_store.in_memory_session_store import InMemorySessionStore
from .data.session_store.session_store import SessionStore
from .session_handler import SessionNotFound

watchables_store: WatchablesStore = InMemoryWatchablesStore()

session_store: SessionStore = InMemorySessionStore()

session_handler = SessionHandler(watchables_store, session_store)

app = FastAPI()

@app.post("/session", status_code=201)
async def create_session():
    session_id = await session_handler.init_session()
    return {"session_id": session_id}


@app.post("/session/{session_id}/user", responses={404: {'description': 'Session not found'}}, status_code=201, response_model=UserPayload)
async def user_joins_session(session_id: str):
    try:
        return await session_handler.join_user_to_session(session_id)
    except SessionNotFound:
        raise HTTPException(status_code=404, detail=f'A session with id {session_id} could not be found')

