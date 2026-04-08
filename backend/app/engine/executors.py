import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

from app.engine.memory import MemoryStore
from app.schemas.node import Node, NodeType

logger = logging.getLogger(__name__)

import asyncio


class ExecutionContext:
    """Context object passed to every node executor during execution."""

    def __init__(
        self, memory: MemoryStore, workflow_id: str, stream_queue: asyncio.Queue = None
    ):
        self.memory = memory
        self.workflow_id = workflow_id
        self.stream_queue = stream_queue


class BaseNodeExecutor(ABC):
    """Abstract base class that all node executors must implement."""

    @abstractmethod
    async def execute(self, node: Node, context: ExecutionContext) -> Any:
        """
        Executes the logic for the node.
        Must return the output produced by the node.
        """
        pass


class InputNodeExecutor(BaseNodeExecutor):
    """Executes an INPUT node, placing its static text into memory."""

    async def execute(self, node: Node, context: ExecutionContext) -> Any:
        logger.info(f"Executing InputNode {node.id}")
        # The node.data is guaranteed to be InputNodeData via Pydantic
        text = node.data.text
        context.memory.write(key=node.id, value=text)
        return text


class OutputNodeExecutor(BaseNodeExecutor):
    """Executes an OUTPUT node, aggregating dependencies from memory."""

    async def execute(self, node: Node, context: ExecutionContext) -> Any:
        logger.info(f"Executing OutputNode {node.id}")

        # We assume the engine will have populated the memory with
        # outputs from the parent nodes. For the output node, we
        # just retrieve them.
        # Note: The dependency tracking happens in the runner.
        # This executor just acts as a collection point.

        # For our MVP, the output simply represents "completion"
        return {"status": "completed"}


from app.providers.factory import ProviderFactory
from app.providers.schema import ChatMessage, LLMProviderType, LLMRequest


class LLMNodeExecutor(BaseNodeExecutor):
    """Executes an LLM node, calling the appropriate provider layer."""

    async def execute(self, node: Node, context: ExecutionContext) -> Any:
        logger.info(f"Executing LLMNode {node.id}")

        system_prompt = node.data.system_prompt
        model_name = node.data.model
        provider_name = node.data.provider

        # Build messages based on incoming connections in a real scenario
        # For now, we take a placeholder user prompt logic, maybe from the engine
        # Here we just execute the stream.
        messages = []
        if system_prompt:
            messages.append(ChatMessage(role="system", content=system_prompt))

        # Get edges targeting this node to retrieve their outputs from memory
        # In a generic way, we could append memory outputs. For MVP, we pass dummy text or what's in memory.
        # Check if there is an input in memory
        input_texts = [
            val for key, val in context.memory.store.items() if key != node.id
        ]
        if input_texts:
            messages.append(
                ChatMessage(role="user", content=" ".join(str(x) for x in input_texts))
            )
        else:
            messages.append(ChatMessage(role="user", content="Hello!"))  # Fallback

        provider = ProviderFactory.get_provider(LLMProviderType(provider_name))

        request = LLMRequest(
            provider=LLMProviderType(provider_name), model=model_name, messages=messages
        )

        generated_output = ""

        async for chunk in provider.generate_stream(request):
            generated_output += chunk
            if context.stream_queue:
                await context.stream_queue.put(
                    {"type": "node_chunk", "node_id": node.id, "content": chunk}
                )

        context.memory.write(key=node.id, value=generated_output)
        return generated_output


class NodeExecutorFactory:
    """Factory to retrieve the appropriate executor for a given node type."""

    _executors: Dict[NodeType, BaseNodeExecutor] = {
        NodeType.INPUT: InputNodeExecutor(),
        NodeType.OUTPUT: OutputNodeExecutor(),
        NodeType.LLM: LLMNodeExecutor(),
    }

    @classmethod
    def get_executor(cls, node_type: NodeType) -> BaseNodeExecutor:
        executor = cls._executors.get(node_type)
        if not executor:
            raise ValueError(f"No executor registered for node type: {node_type}")
        return executor
