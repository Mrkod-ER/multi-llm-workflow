/** Base URL for the FastAPI backend */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const api = {
  /** Validate a workflow DAG structure */
  validateWorkflow: async (workflow: unknown) => {
    const res = await fetch(`${API_BASE_URL}/api/v1/workflows/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(workflow),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** Execute a workflow and return results */
  runWorkflow: async (request: unknown) => {
    const res = await fetch(`${API_BASE_URL}/api/v1/workflows/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** Fetch available models from all providers */
  listModels: async () => {
    const res = await fetch(`${API_BASE_URL}/api/v1/models/`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** Fetch provider health statuses */
  getProviderHealth: async () => {
    const res = await fetch(`${API_BASE_URL}/api/v1/models/health`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** Open a WebSocket connection to stream workflow execution */
  runWorkflowStream: (
    request: unknown,
    handlers: {
      onNodeStart: (nodeId: string) => void;
      onNodeChunk: (nodeId: string, chunk: string) => void;
      onNodeEnd: (nodeId: string, output: unknown) => void;
      onNodeError: (nodeId: string, error: string) => void;
      onWorkflowEnd: (result: unknown) => void;
      onError: (error: string) => void;
    }
  ): WebSocket => {
    // Convert http:// to ws://
    const wsBaseUrl = API_BASE_URL.replace(/^http/, "ws");
    const wsUrl = `${wsBaseUrl}/api/v1/workflows/ws/run`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      ws.send(JSON.stringify(request));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        switch (data.type) {
          case "node_start":
            handlers.onNodeStart(data.node_id);
            break;
          case "node_chunk":
            handlers.onNodeChunk(data.node_id, data.content);
            break;
          case "node_end":
            handlers.onNodeEnd(data.node_id, data.output);
            break;
          case "node_error":
            handlers.onNodeError(data.node_id, data.error);
            break;
          case "workflow_end":
            handlers.onWorkflowEnd(data.result);
            break;
          case "error":
            handlers.onError(data.error);
            break;
        }
      } catch (err) {
        handlers.onError(String(err));
      }
    };

    ws.onerror = () => {
      handlers.onError("WebSocket connection error");
    };

    return ws;
  },
};
