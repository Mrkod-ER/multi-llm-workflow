import contextlib
import logging
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Setup simple logger for now
logging.basicConfig(level=logging.INFO)
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

app = FastAPI(
    title="Multi-LLM Workflow Builder",
    description="Backend API for orchestrating multi-LLM workflows",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be configured via settings later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
