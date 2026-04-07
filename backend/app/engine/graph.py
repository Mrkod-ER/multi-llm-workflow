from collections import defaultdict, deque
from typing import Dict, List

from app.exceptions import WorkflowError
from app.schemas.edge import Edge
from app.schemas.node import Node


class WorkflowCycleError(WorkflowError):
    """Raised when the workflow graph contains a cycle."""

    def __init__(
        self,
        message: str = "A cycle was detected in the workflow graph. LLM DAGs cannot contain circular dependencies.",
    ):
        super().__init__(message=message, status_code=400)


def build_adjacency_list(edges: List[Edge]) -> Dict[str, List[str]]:
    """
    Builds a directed adjacency list mapping node ID -> list of target node IDs.
    """
    adj_list: Dict[str, List[str]] = defaultdict(list)
    for edge in edges:
        adj_list[edge.source].append(edge.target)
    return adj_list


def build_in_degree_map(nodes: List[Node], edges: List[Edge]) -> Dict[str, int]:
    """
    Computes the in-degree (number of incoming edges) for every node.
    """
    in_degree: Dict[str, int] = {node.id: 0 for node in nodes}
    for edge in edges:
        if edge.target in in_degree:
            in_degree[edge.target] += 1
    return in_degree


def validate_dag(nodes: List[Node], edges: List[Edge]) -> List[str]:
    """
    Validates that the provided nodes and edges form a Directed Acyclic Graph (DAG)
    and returns a topologically sorted list of node IDs determining execution order.

    Uses Kahn's Algorithm for topological sorting.
    """
    in_degree = build_in_degree_map(nodes, edges)
    adj_list = build_adjacency_list(edges)

    # Start with nodes that have no prerequisites
    queue = deque([node_id for node_id, count in in_degree.items() if count == 0])

    sorted_nodes: List[str] = []

    while queue:
        current_node = queue.popleft()
        sorted_nodes.append(current_node)

        # Decrement the in-degree of all target nodes
        for target in adj_list[current_node]:
            if target in in_degree:
                in_degree[target] -= 1
                if in_degree[target] == 0:
                    queue.append(target)

    if len(sorted_nodes) != len(nodes):
        raise WorkflowCycleError()

    return sorted_nodes


def get_node_dependencies(node_id: str, edges: List[Edge]) -> List[str]:
    """
    Returns a list of all node IDs that directly feed into the given node.
    """
    return [edge.source for edge in edges if edge.target == node_id]
