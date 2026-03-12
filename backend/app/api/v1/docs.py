from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse

system_router = APIRouter(tags=["System"])


@system_router.get("/docs/swagger", include_in_schema=False)
async def swagger_ui() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Multi-LLM Workflow API Docs")


@system_router.get("/docs/redoc", include_in_schema=False)
async def redoc_ui() -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="Multi-LLM Workflow API Docs")
