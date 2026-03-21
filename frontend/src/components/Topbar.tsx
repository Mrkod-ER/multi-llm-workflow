"use client";
import { useState } from "react";
import { Play, Loader2, CheckCircle2, XCircle, Plus, FileText, BrainCircuit, MonitorPlay, GitBranch, LayoutTemplate, BarChart2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";
import { NodeType, type WorkflowRunResponse } from "@/lib/types";
import { api } from "@/lib/api";
import { useAutoLayout } from "@/hooks/useAutoLayout";

export function Topbar({ onShowResults }: { onShowResults: () => void }) {
  const { nodes, edges, addNode, setIsRunning, isRunning, setRunResult, setExecutingNodeId } = useWorkflowStore();
  const { applyLayout } = useAutoLayout();
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const handleRun = async () => {
    setIsRunning(true);
    setStatus("idle");
    setRunResult(null);

    // Map React Flow nodes to backend schema
    const workflowNodes = nodes.map((n) => ({
      id: n.id,
      type: (n.data as any).type,
      position: n.position,
      data: n.data,
    }));
    const workflowEdges = edges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
    }));

    try {
      // Simulate per-node execution indicator
      for (const node of nodes) {
        setExecutingNodeId(node.id);
        await new Promise((r) => setTimeout(r, 300));
      }
      setExecutingNodeId(null);

      const result: WorkflowRunResponse = await api.runWorkflow({
        workflow: { nodes: workflowNodes, edges: workflowEdges },
      });
      setRunResult(result);
      setStatus(result.status === "success" ? "success" : "error");
      onShowResults();
    } catch {
      setStatus("error");
      onShowResults();
    } finally {
      setIsRunning(false);
      setExecutingNodeId(null);
    }
  };

  const addNodeItems = [
    { type: NodeType.INPUT, label: "Input", icon: FileText, color: "#4ade80" },
    { type: NodeType.LLM, label: "LLM", icon: BrainCircuit, color: "#818cf8" },
    { type: NodeType.OUTPUT, label: "Output", icon: MonitorPlay, color: "#fb923c" },
  ];

  return (
    <header className="glass z-10 border-b border-white/[0.06] flex items-center px-4 gap-3 h-14 shrink-0">
      {/* Brand */}
      <div className="flex items-center gap-2 mr-4">
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-md">
          <GitBranch size={14} className="text-white" />
        </div>
        <span className="text-sm font-semibold text-white/90">Multi-LLM Workflow</span>
      </div>

      <div className="h-5 w-px bg-white/10" />

      {/* Add Node buttons */}
      <div className="flex items-center gap-1.5">
        {addNodeItems.map(({ type, label, icon: Icon, color }) => (
          <button
            key={type}
            id={`add-${label.toLowerCase()}-node`}
            onClick={() => addNode(type)}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 hover:scale-[1.03] active:scale-95"
            style={{
              background: `${color}15`,
              color,
              border: `1px solid ${color}30`,
            }}
          >
            <Plus size={11} />
            <Icon size={11} />
            {label}
          </button>
        ))}
      </div>

      <div className="ml-auto flex items-center gap-3">
        {/* Status badge */}
        {status === "success" && (
          <div className="flex items-center gap-1.5 text-xs text-emerald-400">
            <CheckCircle2 size={13} />
            <span>Run complete</span>
          </div>
        )}
        {status === "error" && (
          <div className="flex items-center gap-1.5 text-xs text-red-400">
            <XCircle size={13} />
            <span>Run failed</span>
          </div>
        )}

        {/* Auto Layout */}
        <button
          id="auto-layout-btn"
          onClick={applyLayout}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-white/50 hover:text-white/80 hover:bg-white/5 border border-white/10 transition-all"
          title="Auto-arrange nodes"
        >
          <LayoutTemplate size={12} />
          Auto Layout
        </button>

        {/* View Results */}
        {runResult && (
          <button
            id="view-results-btn"
            onClick={onShowResults}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-violet-300 hover:text-white bg-violet-500/10 hover:bg-violet-500/20 border border-violet-500/20 transition-all"
          >
            <BarChart2 size={12} />
            Results
          </button>
        )}

        {/* Run button */}
        <button
          id="run-workflow-btn"
          disabled={isRunning}
          onClick={handleRun}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200",
            isRunning
              ? "bg-violet-700/40 text-violet-300 cursor-not-allowed"
              : "bg-gradient-to-r from-violet-600 to-indigo-600 text-white hover:from-violet-500 hover:to-indigo-500 hover:shadow-lg hover:shadow-violet-500/25 active:scale-95"
          )}
        >
          {isRunning ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
          {isRunning ? "Running…" : "Run Workflow"}
        </button>
      </div>
    </header>
  );
}
