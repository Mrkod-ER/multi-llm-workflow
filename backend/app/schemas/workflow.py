from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.schemas.node import Node, NodeType
from app.schemas.edge import Edge

class WorkflowMetadata(BaseModel):
    """Metadata describing the workflow's identity."""
    name: str = Field(..., description="The name of the workflow.")
    description: Optional[str] = Field(None, description="A brief description of what the workflow does.")
    version: str = Field("1.0", description="Version string for the workflow export.")

class Workflow(BaseModel):
    """A directed acyclic graph composed of nodes and edges."""
    nodes: List[Node] = Field(default_factory=list, description="A list of nodes making up the DAG.")
    edges: List[Edge] = Field(default_factory=list, description="A list of directed edges connecting the nodes.")

    @model_validator(mode="after")
    def validate_workflow_structure(self) -> 'Workflow':
        if not self.nodes:
            raise ValueError("Workflow must contain at least one node.")
        
        has_input = any(node.type == NodeType.INPUT for node in self.nodes)
        if not has_input:
            raise ValueError("Workflow must contain at least one INPUT node.")
        
        return self

class WorkflowExport(BaseModel):
    """The complete payload for importing/exporting a workflow as a JSON file."""
    metadata: WorkflowMetadata
    workflow: Workflow
