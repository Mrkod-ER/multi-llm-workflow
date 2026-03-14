import { create } from "zustand";
import { addEdge, applyNodeChanges, applyEdgeChanges } from "@xyflow/react";
import type {
  Node,
  Edge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  Connection,
} from "@xyflow/react";
import { NodeType, type WorkflowRunResponse, type ModelInfo } from "@/lib/types";

let nodeIdCounter = 3;

interface WorkflowState {
  // Graph state
  nodes: Node[];
  edges: Edge[];
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;

  // Selected node
  selectedNodeId: string | null;
  setSelectedNodeId: (id: string | null) => void;

  // Node mutations
  addNode: (type: NodeType, position?: { x: number; y: number }) => void;
  updateNodeData: (nodeId: string, data: Partial<Record<string, unknown>>) => void;
  deleteNode: (nodeId: string) => void;

  // Execution state
  isRunning: boolean;
  runResult: WorkflowRunResponse | null;
  executingNodeId: string | null;
  setIsRunning: (v: boolean) => void;
  setRunResult: (result: WorkflowRunResponse | null) => void;
  setExecutingNodeId: (id: string | null) => void;

  // Models
  models: ModelInfo[];
  setModels: (models: ModelInfo[]) => void;
}

const defaultNodes: Node[] = [
  {
    id: "1",
    type: "inputNode",
    position: { x: 80, y: 200 },
    data: { type: NodeType.INPUT, text: "Write a short poem about the ocean." },
  },
  {
    id: "2",
    type: "llmNode",
    position: { x: 420, y: 180 },
    data: {
      type: NodeType.LLM,
      system_prompt: "You are a thoughtful poet.",
      model: "mock-model",
      provider: "mock",
    },
  },
  {
    id: "3",
    type: "outputNode",
    position: { x: 760, y: 200 },
    data: { type: NodeType.OUTPUT, result: "" },
  },
];

const defaultEdges: Edge[] = [
  { id: "e1-2", source: "1", target: "2" },
  { id: "e2-3", source: "2", target: "3" },
];

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  nodes: defaultNodes,
  edges: defaultEdges,
  selectedNodeId: null,
  isRunning: false,
  runResult: null,
  executingNodeId: null,
  models: [],

  onNodesChange: (changes) =>
    set((state) => ({ nodes: applyNodeChanges(changes, state.nodes) })),

  onEdgesChange: (changes) =>
    set((state) => ({ edges: applyEdgeChanges(changes, state.edges) })),

  onConnect: (connection: Connection) =>
    set((state) => ({ edges: addEdge(connection, state.edges) })),

  setSelectedNodeId: (id) => set({ selectedNodeId: id }),

  addNode: (type, position = { x: 300, y: 300 }) => {
    const id = String(++nodeIdCounter);
    const dataMap: Record<NodeType, Record<string, unknown>> = {
      [NodeType.INPUT]: { type: NodeType.INPUT, text: "" },
      [NodeType.LLM]: {
        type: NodeType.LLM,
        system_prompt: "",
        model: "mock-model",
        provider: "mock",
      },
      [NodeType.OUTPUT]: { type: NodeType.OUTPUT, result: "" },
    };
    const typeMap: Record<NodeType, string> = {
      [NodeType.INPUT]: "inputNode",
      [NodeType.LLM]: "llmNode",
      [NodeType.OUTPUT]: "outputNode",
    };
    set((state) => ({
      nodes: [
        ...state.nodes,
        { id, type: typeMap[type], position, data: dataMap[type] },
      ],
    }));
  },

  updateNodeData: (nodeId, data) =>
    set((state) => ({
      nodes: state.nodes.map((n) =>
        n.id === nodeId ? { ...n, data: { ...n.data, ...data } } : n
      ),
    })),

  deleteNode: (nodeId) =>
    set((state) => ({
      nodes: state.nodes.filter((n) => n.id !== nodeId),
      edges: state.edges.filter(
        (e) => e.source !== nodeId && e.target !== nodeId
      ),
      selectedNodeId:
        state.selectedNodeId === nodeId ? null : state.selectedNodeId,
    })),

  setIsRunning: (v) => set({ isRunning: v }),
  setRunResult: (result) => set({ runResult: result }),
  setExecutingNodeId: (id) => set({ executingNodeId: id }),
  setModels: (models) => set({ models }),
}));
