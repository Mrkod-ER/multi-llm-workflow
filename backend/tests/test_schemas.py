import pytest
from pydantic import ValidationError
from app.schemas.node import Node, NodePosition, InputNodeData, LLMNodeData, OutputNodeData, NodeType
from app.schemas.edge import Edge
from app.schemas.workflow import Workflow


def test_valid_input_node():
    node = Node(
        id="node-1",
        type=NodeType.INPUT,
        position=NodePosition(x=100, y=100),
        data=InputNodeData(text="Test input")
    )
    assert node.id == "node-1"
    assert node.data.type == NodeType.INPUT


def test_edge_self_reference_validation():
    with pytest.raises(ValidationError, match="Self-referencing edges are not allowed"):
        Edge(id="edge-1", source="node-1", target="node-1")


def test_workflow_empty_nodes_validation():
    with pytest.raises(ValidationError, match="Workflow must contain at least one node"):
        Workflow(nodes=[], edges=[])


def test_workflow_missing_input_validation():
    node = Node(
        id="node-2",
        type=NodeType.OUTPUT,
        position=NodePosition(x=0, y=0),
        data=OutputNodeData()
    )
    with pytest.raises(ValidationError, match="Workflow must contain at least one INPUT node"):
        Workflow(nodes=[node], edges=[])


def test_valid_workflow():
    node_in = Node(
        id="node-1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="Hi")
    )
    node_out = Node(
        id="node-2", type=NodeType.OUTPUT, position=NodePosition(x=1, y=1), data=OutputNodeData()
    )
    edge = Edge(id="edge-1", source="node-1", target="node-2")
    
    workflow = Workflow(nodes=[node_in, node_out], edges=[edge])
    assert len(workflow.nodes) == 2
    assert len(workflow.edges) == 1
