import logging
import uuid

from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.api import WorkflowRunRequest, WorkflowRunResponse, WorkflowValidationError
from app.schemas.workflow import Workflow
from app.engine.graph import validate_dag, WorkflowCycleError
from app.engine.runner import WorkflowRunner
from app.exceptions import WorkflowError

router = APIRouter(prefix="/workflows", tags=["Workflows"])
logger = logging.getLogger(__name__)


@router.post(
    "/validate",
    summary="Validate a workflow DAG",
    description="Runs structural validation on the workflow without executing it. Checks for cycles and connectivity.",
    response_model=dict
)
async def validate_workflow(workflow: Workflow):
    """
    Validates the structural integrity of a workflow graph:
    - Checks that there are no circular dependencies
    - Confirms at least one INPUT node is present
    - Returns a topologically sorted execution order
    """
    try:
        sorted_ids = validate_dag(nodes=workflow.nodes, edges=workflow.edges)
        return {
            "valid": True,
            "execution_order": sorted_ids,
            "node_count": len(workflow.nodes),
            "edge_count": len(workflow.edges),
        }
    except WorkflowCycleError as e:
        return JSONResponse(
            status_code=422,
            content={"valid": False, "error": str(e)}
        )
    except Exception as e:
        logger.error(f"Unexpected validation error: {e}")
        raise HTTPException(status_code=500, detail="Workflow validation encountered an unexpected error.")


@router.post(
    "/run",
    summary="Execute a workflow",
    description="Validates, topologically sorts, and executes all nodes in the workflow using the configured LLM providers.",
    response_model=WorkflowRunResponse
)
async def run_workflow(request: WorkflowRunRequest):
    """
    Triggers a full workflow execution:
    1. Validates the DAG structure
    2. Sorts nodes topologically
    3. Executes each node via the appropriate provider
    4. Returns structured results per-node and final aggregated output.
    """
    workflow_id = str(uuid.uuid4())
    logger.info(f"Starting workflow run: {workflow_id}")
    
    try:
        runner = WorkflowRunner(request)
        result = await runner.run(workflow_id=workflow_id)
        return result
    except WorkflowCycleError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except WorkflowError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.exception(f"Unhandled error during workflow run {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during workflow execution.")

@router.websocket("/ws/run")
async def ws_run_workflow(websocket: WebSocket):
    """
    WebSocket endpoint for real-time workflow execution.
    Expects a WorkflowRunRequest JSON payload upon connection.
    Streams execution events (node_start, node_chunk, node_end, error, workflow_end).
    """
    await websocket.accept()
    logger.info("WebSocket connected for workflow run stream")
    
    try:
        data = await websocket.receive_json()
        request = WorkflowRunRequest(**data)
        workflow_id = str(uuid.uuid4())
        
        runner = WorkflowRunner(request)
        async for event in runner.run_stream(workflow_id=workflow_id):
            await websocket.send_json(event)
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected by client")
    except ValidationError as e:
        logger.error(f"WebSocket validaton error: {e}")
        await websocket.send_json({"type": "error", "error": "Invalid workflow payload"})
        await websocket.close(code=1008) # Policy Violation
    except Exception as e:
        logger.exception(f"WebSocket unhandled error: {e}")
        await websocket.send_json({"type": "error", "error": str(e)})
        # It may be already closed, but we try
        try:
            await websocket.close(code=1011) # Internal Error
        except Exception:
            pass
