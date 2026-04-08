import asyncio
import logging
import time
from typing import AsyncGenerator, Dict

from app.engine.executors import ExecutionContext, NodeExecutorFactory
from app.engine.graph import validate_dag
from app.engine.memory import MemoryStore
from app.schemas.api import NodeExecutionResult, WorkflowRunRequest, WorkflowRunResponse
from app.schemas.workflow import Workflow

logger = logging.getLogger(__name__)


class WorkflowRunner:
    """Orchestrates the execution of a Workflow definition."""

    def __init__(self, request: WorkflowRunRequest):
        self.workflow: Workflow = request.workflow
        self.memory = MemoryStore()

    async def run(self, workflow_id: str = "run_1") -> WorkflowRunResponse:
        total_start_time = time.perf_counter()

        # 1. Validation and Topological Sort
        # Will raise exceptions handled by API if cycle is detected
        logger.info(f"Validating and sorting DAG for workflow: {self.workflow.nodes!r}")
        try:
            sorted_node_ids = validate_dag(
                nodes=self.workflow.nodes, edges=self.workflow.edges
            )
        except Exception as e:
            logger.error(f"DAG Validation failed: {e}")
            raise

        # Map IDs to Node objects for fast lookup
        node_map = {node.id: node for node in self.workflow.nodes}
        context = ExecutionContext(memory=self.memory, workflow_id=workflow_id)

        results: Dict[str, NodeExecutionResult] = {}

        # 2. Sequential Execution Map
        for node_id in sorted_node_ids:
            node = node_map[node_id]
            executor = NodeExecutorFactory.get_executor(node.type)

            # Record timing
            node_start = time.perf_counter()

            try:
                # E.g. in real apps, we retrieve the dependencies inputs from memory here
                # dependencies = get_node_dependencies(node_id, self.workflow.edges)

                output = await executor.execute(node, context)

                node_duration = (time.perf_counter() - node_start) * 1000  # ms

                results[node_id] = NodeExecutionResult(
                    node_id=node_id, output=output, duration_ms=round(node_duration, 2)
                )

            except Exception as e:
                logger.exception(f"Execution failed for node {node_id}: {e}")
                node_duration = (time.perf_counter() - node_start) * 1000
                results[node_id] = NodeExecutionResult(
                    node_id=node_id,
                    output=None,
                    duration_ms=round(node_duration, 2),
                    error=str(e),
                )
                # Fail fast on graph execution
                break

        total_duration = (time.perf_counter() - total_start_time) * 1000
        status = (
            "success"
            if all(r.error is None for r in results.values())
            and len(results) == len(sorted_node_ids)
            else "error"
        )

        return WorkflowRunResponse(
            status=status,
            total_duration_ms=round(total_duration, 2),
            results=list(results.values()),
            final_output=self.memory.read_all(),
        )

    async def run_stream(
        self, workflow_id: str = "run_1"
    ) -> AsyncGenerator[Dict, None]:
        queue = asyncio.Queue()

        async def _execute_graph():
            try:
                sorted_node_ids = validate_dag(
                    nodes=self.workflow.nodes, edges=self.workflow.edges
                )
            except Exception as e:
                logger.error(f"DAG Validation failed: {e}")
                await queue.put({"type": "error", "error": str(e)})
                await queue.put({"type": "done"})
                return

            node_map = {node.id: node for node in self.workflow.nodes}
            context = ExecutionContext(
                memory=self.memory, workflow_id=workflow_id, stream_queue=queue
            )

            total_start_time = time.perf_counter()
            results: Dict[str, NodeExecutionResult] = {}

            for node_id in sorted_node_ids:
                node = node_map[node_id]
                executor = NodeExecutorFactory.get_executor(node.type)

                await queue.put({"type": "node_start", "node_id": node_id})
                node_start = time.perf_counter()

                try:
                    output = await executor.execute(node, context)
                    node_duration = (time.perf_counter() - node_start) * 1000

                    results[node_id] = NodeExecutionResult(
                        node_id=node_id,
                        output=output,
                        duration_ms=round(node_duration, 2),
                    )

                    await queue.put(
                        {
                            "type": "node_end",
                            "node_id": node_id,
                            "output": output,
                            "duration_ms": round(node_duration, 2),
                        }
                    )

                except Exception as e:
                    logger.exception(f"Execution failed for node {node_id}: {e}")
                    node_duration = (time.perf_counter() - node_start) * 1000
                    results[node_id] = NodeExecutionResult(
                        node_id=node_id,
                        output=None,
                        duration_ms=round(node_duration, 2),
                        error=str(e),
                    )
                    await queue.put(
                        {
                            "type": "node_error",
                            "node_id": node_id,
                            "error": str(e),
                            "duration_ms": round(node_duration, 2),
                        }
                    )
                    break

            total_duration = (time.perf_counter() - total_start_time) * 1000
            status = (
                "success"
                if all(r.error is None for r in results.values())
                and len(results) == len(sorted_node_ids)
                else "error"
            )

            final_response = WorkflowRunResponse(
                status=status,
                total_duration_ms=round(total_duration, 2),
                results=list(results.values()),
                final_output=self.memory.read_all(),
            )

            # Persist to Redis out-of-band via fire-and-forget or awaited task
            try:
                from app.services.redis_client import redis_client

                # We store a summary dictionary containing response and workflow structure
                run_data = {
                    "request": self.workflow.model_dump(),
                    "response": final_response.model_dump(),
                }
                await redis_client.save_run(workflow_id, run_data)
            except Exception as e:
                logger.error(f"Failed to persist workflow {workflow_id} to Redis: {e}")

            await queue.put(
                {"type": "workflow_end", "result": final_response.model_dump()}
            )
            await queue.put({"type": "done"})

        task = asyncio.create_task(_execute_graph())

        while True:
            event = await queue.get()
            if event["type"] == "done":
                break
            yield event
