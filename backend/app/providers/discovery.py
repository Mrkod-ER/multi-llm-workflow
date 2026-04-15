import logging
from typing import Any, Dict, List

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


async def list_ollama_models() -> List[Dict[str, Any]]:
    """Fetches dynamically loaded models from the local Ollama instance."""
    settings = get_settings()
    url = f"{settings.ollama_base_url.rstrip('/')}/api/tags"

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                models = []
                for model in data.get("models", []):
                    models.append(
                        {
                            "id": model["name"],
                            "provider": "ollama",
                            "size": model.get("size", 0),
                            "details": model.get("details", {}),
                        }
                    )
                return models
    except Exception as e:
        logger.warning(f"Could not connect to local Ollama to list models: {e}")

    return []


async def list_openai_models() -> List[Dict[str, Any]]:
    """Returns static or dynamically fetched models via LiteLLM/OpenAI SDK."""
    settings = get_settings()
    if not settings.openai_api_key:
        return []

    return [
        {"id": "gpt-4o", "provider": "openai"},
        {"id": "gpt-4-turbo", "provider": "openai"},
        {"id": "gpt-3.5-turbo", "provider": "openai"},
    ]


async def list_gemini_models() -> List[Dict[str, Any]]:
    """Returns available Gemini models when GOOGLE_API_KEY is configured."""
    settings = get_settings()
    if not settings.google_api_key:
        return []

    return [
        {"id": "gemini-1.5-flash", "provider": "gemini", "description": "Fast & efficient"},
        {"id": "gemini-1.5-pro",   "provider": "gemini", "description": "Most capable"},
        {"id": "gemini-2.0-flash", "provider": "gemini", "description": "Latest generation"},
    ]


async def list_all_models() -> List[Dict[str, Any]]:
    """Aggregates models actively available across all configured providers."""
    ollama_models = await list_ollama_models()
    openai_models = await list_openai_models()
    gemini_models = await list_gemini_models()

    return ollama_models + openai_models + gemini_models
