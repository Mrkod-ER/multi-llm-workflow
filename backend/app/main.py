import contextlib
import logging
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.logger import setup_logging

# Setup structured logging
setup_logging()
logger = logging.getLogger(__name__)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan context manager.
    Used for startup and shutdown events (e.g., DB connection, Redis setup).
    """
    logger.info("Starting up Multi-LLM Workflow Builder backend...")
    yield
    logger.info("Shutting down backend...")

from app.config import get_settings
from app.exceptions import setup_exception_handlers
from app.middleware import setup_middlewares

app = FastAPI(
    title="Multi-LLM Workflow Builder",
    description="Backend API for orchestrating multi-LLM workflows",
    version="0.1.0",
    lifespan=lifespan,
)

settings = get_settings()

# Setup custom middlewares (request id, etc)
setup_middlewares(app)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Register API routers
from app.api.v1 import api_v1_router  # noqa: E402
app.include_router(api_v1_router)

@app.get("/health", tags=["System"])
async def health_check() -> JSONResponse:
    """
    Health check endpoint.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "version": app.version,
        }
    )
