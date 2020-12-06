""" This file is the entrypoint of the application """

from fastapi import FastAPI
from .middleware.logging import LoggingMiddleware
from .routes import session_routes

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(session_routes.router)
