import logging
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException

from app.providers.discovery import list_all_models
from app.providers.factory import ProviderFactory
from app.providers.schema import LLMProviderType

router = APIRouter(prefix="/models", tags=["Models"])
logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="List all available models",
    description="Returns a combined list of models available in Ollama locally and from configured cloud providers.",
    response_model=List[Dict[str, Any]]
)
async def get_available_models():
    """
    Dynamically discovers and aggregates all LLM models available
    across configured providers (Ollama, OpenAI etc).
    """
    models = await list_all_models()
    return models


@router.get(
    "/health",
    summary="Check provider connectivity",
    description="Pings all configured LLM providers and returns their connectivity status.",
)
async def get_provider_health():
    """Queries health of each LLM provider to help users diagnose connectivity issues."""
    health_status = {}
    
    for provider_type in LLMProviderType:
        try:
            provider = ProviderFactory.get_provider(provider_type)
            is_healthy = await provider.health_check()
            health_status[provider_type.value] = {"status": "ok" if is_healthy else "degraded"}
        except Exception as e:
            logger.warning(f"Health check failed for {provider_type}: {e}")
            health_status[provider_type.value] = {"status": "error", "detail": str(e)}
    
    return {"providers": health_status}
