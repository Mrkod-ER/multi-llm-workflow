from fastapi.testclient import TestClient
import pytest

from app.schemas.node import Node, NodePosition, NodeType, InputNodeData, OutputNodeData
from app.schemas.edge import Edge
from app.schemas.workflow import Workflow

# --- Helpers ---
def make_simple_workflow():
    n1 = Node(id="n1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="hello world"))
    n2 = Node(id="n2", type=NodeType.OUTPUT, position=NodePosition(x=1, y=0), data=OutputNodeData())
    e1 = Edge(id="e1", source="n1", target="n2")
    return Workflow(nodes=[n1, n2], edges=[e1])


# --- Validate endpoint tests ---
def test_validate_valid_workflow(client: TestClient):
    wf = make_simple_workflow()
    response = client.post("/api/v1/workflows/validate", json=wf.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["execution_order"] == ["n1", "n2"]
    assert data["node_count"] == 2


def test_validate_cyclic_workflow(client: TestClient):
    n1 = Node(id="n1", type=NodeType.INPUT, position=NodePosition(x=0, y=0), data=InputNodeData(text="start"))
    n2 = Node(id="n2", type=NodeType.OUTPUT, position=NodePosition(x=1, y=0), data=OutputNodeData())
    edges = [
        Edge(id="e1", source="n1", target="n2"),
        Edge(id="e2", source="n2", target="n1"),  # creates cycle
    ]
    wf = {"nodes": [n1.model_dump(), n2.model_dump()], "edges": [e.model_dump() for e in edges]}
    response = client.post("/api/v1/workflows/validate", json=wf)
    assert response.status_code == 422
    data = response.json()
    assert data["valid"] is False


# --- Run endpoint tests ---
def test_run_simple_workflow(client: TestClient):
    wf = make_simple_workflow()
    request_payload = {"workflow": wf.model_dump()}
    response = client.post("/api/v1/workflows/run", json=request_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["results"]) == 2
    assert data["results"][0]["output"] == "hello world"


# --- Models endpoint tests ---
def test_get_models(client: TestClient):
    response = client.get("/api/v1/models/")
    # Models endpoint hits Ollama/OpenAI; it may be empty in CI but must not error
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_provider_health(client: TestClient):
    response = client.get("/api/v1/models/health")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert "mock" in data["providers"]
