/** Mirrors the NodeType enum from the backend */
export enum NodeType {
  INPUT = "INPUT",
  LLM = "LLM",
  OUTPUT = "OUTPUT",
}

export interface NodePosition {
  x: number;
  y: number;
}

export interface InputNodeData {
  type: NodeType.INPUT;
  text: string;
}

export interface LLMNodeData {
  type: NodeType.LLM;
  system_prompt: string;
  model: string;
  provider: string;
}

export interface OutputNodeData {
  type: NodeType.OUTPUT;
  result: string;
}

export type NodeData = InputNodeData | LLMNodeData | OutputNodeData;

export interface WorkflowNode {
  id: string;
  type: NodeType;
  position: NodePosition;
  data: NodeData;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
}

export interface Workflow {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
}

export interface NodeExecutionResult {
  node_id: string;
  output: unknown;
  duration_ms: number;
  error?: string;
}

export interface WorkflowRunResponse {
  status: "success" | "error";
  total_duration_ms: number;
  results: NodeExecutionResult[];
  final_output: Record<string, unknown>;
}

export interface ModelInfo {
  id: string;
  provider: string;
  size?: number;
  details?: Record<string, unknown>;
}
