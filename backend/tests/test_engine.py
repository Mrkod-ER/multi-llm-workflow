import pytest
import asyncio
from app.schemas.node import Node, NodePosition, NodeType, InputNodeData, OutputNodeData
from app.schemas.edge import Edge
from app.schemas.api import WorkflowRunRequest
from app.schemas.workflow import Workflow, WorkflowMetadata
from app.engine.graph import validate_dag, WorkflowCycleError
from app.engine.memory import MemoryStore
from app.engine.executors import InputNodeExecutor, OutputNodeExecutor, ExecutionContext
from app.engine.runner import WorkflowRunner


def test_topological_sort_linear():
    n1 = Node(id="1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="1"))
    # In order to strictly pass pydantic, use LLMNodeData for LLM node, or just omit if lazy.
    # LLM node data was strictly typed, let's just use INPUT -> OUTPUT for testing graph logic.
    n2 = Node(id="2", type=NodeType.OUTPUT, position=NodePosition(x=1, y=1), data=OutputNodeData(result="2"))
    
    edges = [Edge(id="e1", source="1", target="2")]
    sorted_ids = validate_dag([n1, n2], edges)
    assert sorted_ids == ["1", "2"]


def test_cycle_detection():
    n1 = Node(id="1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="1"))
    n2 = Node(id="2", type=NodeType.OUTPUT, position=NodePosition(x=1, y=1), data=OutputNodeData(result="2"))
    
    edges = [
        Edge(id="e1", source="1", target="2"),
        Edge(id="e2", source="2", target="1"), # Cycle
    ]
    with pytest.raises(WorkflowCycleError):
        validate_dag([n1, n2], edges)


@pytest.mark.asyncio
async def test_input_executor():
    node = Node(id="in_1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="hello"))
    mem = MemoryStore()
    ctx = ExecutionContext(mem, "wf_1")
    
    executor = InputNodeExecutor()
    res = await executor.execute(node, ctx)
    assert res == "hello"
    assert mem.read("in_1") == "hello"


@pytest.mark.asyncio
async def test_workflow_runner():
    n1 = Node(id="in_1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="test data"))
    n2 = Node(id="out_1", type=NodeType.OUTPUT, position=NodePosition(x=0, y=0), data=OutputNodeData())
    wf_metadata = WorkflowMetadata(name="test")
    wf = Workflow(nodes=[n1, n2], edges=[Edge(id="e1", source="in_1", target="out_1")])
    
    request = WorkflowRunRequest(workflow=wf)
    runner = WorkflowRunner(request)
    
    response = await runner.run("test_wf")
    assert response.status == "success"
    assert len(response.results) == 2
    assert response.results[0].node_id == "in_1"
    assert response.results[0].output == "test data"
    assert response.final_output.get("in_1") == "test data"
