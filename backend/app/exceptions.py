import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class WorkflowError(Exception):
    """Base exception for workflow-related errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(WorkflowError)
    async def workflow_error_handler(
        request: Request, exc: WorkflowError
    ) -> JSONResponse:
        logger.error(f"WorkflowError: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "WorkflowError", "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred.",
            },
        )
