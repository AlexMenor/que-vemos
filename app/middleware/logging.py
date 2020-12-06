import logging
import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware
from app.config.logging_config import handler

logger = logging.getLogger("HTTPMiddleware")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        request_id = str(uuid.uuid4())

        logger.info(f"id: {request_id} path={request.url.path} {request.method}")

        response = await call_next(request)

        process_time = time.time() - start_time
        process_time_ms = process_time * 1000

        logger.info(f"id: {request_id} status_code={response.status_code} took: {process_time_ms}ms")

        return response
