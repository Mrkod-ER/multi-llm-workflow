import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.redis_client import redis_client

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)

@router.get(
    "/",
    summary="Get workflow execution history",
    description="Returns a chronologically descending list of all saved workflow runs.",
    response_model=List[Dict[str, Any]]
)
async def get_history(limit: int = 50):
    """
    Fetches the latest workflow runs stored in Redis.
    """
    try:
        runs = await redis_client.get_all_runs(limit=limit)
        return runs
    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history from database.")
