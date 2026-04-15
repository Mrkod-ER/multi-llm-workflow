from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMProviderType(str, Enum):
    """The type of provider resolving the execution."""

    OPENAI = "openai"
    OLLAMA = "ollama"
    GEMINI = "gemini"
    MOCK = "mock"


class ChatMessage(BaseModel):
    """A standard chat message object."""

    role: str = Field(..., description="'system', 'user', or 'assistant'")
    content: str = Field(..., description="The content of the message")


class LLMRequest(BaseModel):
    """Standardized request pushed to the Provider Layer."""

    provider: LLMProviderType
    model: str
    messages: List[ChatMessage]
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None)


class LLMResponse(BaseModel):
    """Standardized response returned by the Provider Layer."""

    content: str
    model: str
    usage: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata around token usage overhead"
    )
