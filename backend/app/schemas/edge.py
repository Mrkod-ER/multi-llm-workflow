from pydantic import BaseModel, Field, model_validator

class Edge(BaseModel):
    """A directed edge acting as a connection between two nodes."""
    id: str
    source: str = Field(..., description="The ID of the source node.")
    target: str = Field(..., description="The ID of the target node.")

    @model_validator(mode="after")
    def validate_no_self_reference(self) -> 'Edge':
        if self.source == self.target:
            raise ValueError(f"Self-referencing edges are not allowed (node {self.source}).")
        return self
