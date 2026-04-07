from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """Available types of nodes in the workflow graph."""

    INPUT = "INPUT"
    LLM = "LLM"
    OUTPUT = "OUTPUT"


class NodePosition(BaseModel):
    """X and Y coordinates for rendering the node on the UI canvas."""

    x: float
    y: float


class InputNodeData(BaseModel):
    """Data payload for an Input node."""

    type: Literal[NodeType.INPUT] = NodeType.INPUT
    text: str = Field(default="", description="The initial input prompt text.")


class LLMNodeData(BaseModel):
    """Data payload for an LLM node."""

    type: Literal[NodeType.LLM] = NodeType.LLM
    system_prompt: str = Field(
        default="", description="The system prompt telling the LLM how to behave."
    )
    model: str = Field(
        ..., description="The name of the model to use (e.g., 'gpt-4o', 'llama3')."
    )
    provider: str = Field(
        ..., description="The provider hosting the model (e.g., 'openai', 'ollama')."
    )


class OutputNodeData(BaseModel):
    """Data payload for an Output node."""

    type: Literal[NodeType.OUTPUT] = NodeType.OUTPUT
    result: str = Field(
        default="", description="The final result populated after execution."
    )


# Discriminated union for node data allowing fast, type-safe parsing based on 'type' field
NodeData = Annotated[
    Union[InputNodeData, LLMNodeData, OutputNodeData], Field(discriminator="type")
]


class Node(BaseModel):
    """A generic node block in the workflow DAG."""

    id: str
    type: NodeType
    position: NodePosition
    data: NodeData
