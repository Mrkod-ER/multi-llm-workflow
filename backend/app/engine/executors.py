import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

from app.schemas.node import Node, NodeType
from app.engine.memory import MemoryStore

logger = logging.getLogger(__name__)

class ExecutionContext:
    """Context object passed to every node executor during execution."""
    def __init__(self, memory: MemoryStore, workflow_id: str):
        self.memory = memory
        self.workflow_id = workflow_id


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


class LLMNodeExecutor(BaseNodeExecutor):
    """Executes an LLM node, calling the appropriate provider layer."""
    
    async def execute(self, node: Node, context: ExecutionContext) -> Any:
        logger.info(f"Executing LLMNode {node.id}")
        
        system_prompt = node.data.system_prompt
        model_name = node.data.model
        provider_name = node.data.provider
        
        # We will stub the actual LLM call here heavily until Phase 5 
        # where we implement the LLM Provider abstractions.
        # For now, it just mocks finding inputs from memory.
        
        logger.debug(f"LLM Call stub: Provider={provider_name}, Model={model_name}")
        
        # Simulated LLM generation based on inputs
        generated_output = f"Simulated response from {model_name}"
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
