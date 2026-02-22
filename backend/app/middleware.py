import time
import uuid
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware to inject a request ID and track execution time."""
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.perf_counter()
        
        # We can add request_id to logger context here if we use structlog,
        # but for now we'll just log it.
        logger.debug(f"Request started: {request.method} {request.url.path} [id={request_id}]")
        
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        logger.debug(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code} [id={request_id}] in {process_time:.4f}s")
        return response

def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
