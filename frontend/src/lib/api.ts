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
};
