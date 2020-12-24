""" This file is the entrypoint of the application """

from fastapi import FastAPI
from .middleware.logging import LoggingMiddleware
from .routes import session_routes
from fastapi.middleware.cors import CORSMiddleware
from .data.session_store.redis_session_store import redis_session_store
from .config.config import MODE, config

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(session_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    if config[MODE] == 'prod':
        await redis_session_store.init_pool()
