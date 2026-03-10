from fastapi import APIRouter

from app.api.v1 import workflows, models

# Central v1 router that aggregates all sub-routers
api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(workflows.router)
api_v1_router.include_router(models.router)
