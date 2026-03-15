"use client";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { MonitorPlay } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";

export function OutputNode({ id, data, selected }: NodeProps) {
  const { executingNodeId, runResult } = useWorkflowStore();
  const isExecuting = executingNodeId === id;

  // Try to get live result from execution output
  const liveOutput = runResult?.final_output?.[id];
  const displayText = liveOutput
    ? String(liveOutput)
    : (data as any).result || null;

  return (
    <div
      className={cn(
        "min-w-[220px] rounded-xl border p-0 overflow-hidden shadow-xl transition-all duration-200",
        selected
          ? "border-[#fb923c] shadow-[0_0_20px_rgba(251,146,60,0.3)]"
          : "border-[rgba(251,146,60,0.3)] hover:border-[#fb923c]",
        isExecuting && "node-executing"
      )}
      style={{ background: "rgba(20,10,5,0.95)" }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2" style={{ background: "rgba(251,146,60,0.12)" }}>
        <div className="w-6 h-6 rounded-md flex items-center justify-center" style={{ background: "rgba(251,146,60,0.2)" }}>
          <MonitorPlay size={13} className="text-[#fb923c]" />
        </div>
        <span className="text-xs font-semibold text-[#fb923c] uppercase tracking-widest">Output</span>
        {isExecuting && (
          <span className="ml-auto flex h-2 w-2 rounded-full bg-[#fb923c] animate-ping" />
        )}
      </div>
      {/* Body */}
      <div className="px-3 py-2 min-h-[50px]">
        {displayText ? (
          <p className="text-xs text-white/70 leading-relaxed line-clamp-4">{displayText}</p>
        ) : (
          <p className="text-xs italic text-white/25">Awaiting execution…</p>
        )}
      </div>
      <Handle type="target" position={Position.Left} className="!w-3 !h-3 !border-2 !border-[#fb923c] !bg-[#14080a]" />
    </div>
  );
}
