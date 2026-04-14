"use client";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { MonitorPlay } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";

export function OutputNode({ id, data, selected }: NodeProps) {
  const { nodeStatuses, runResult, streamingTexts } = useWorkflowStore();
  const status = nodeStatuses[id];
  const isExecuting = status === "running";
  const isDone = status === "success";

  const liveOutput = streamingTexts[id] || runResult?.final_output?.[id];
  const displayText = liveOutput ? String(liveOutput) : (data as any).result || null;

  return (
    <div
      className={cn(
        "w-[230px] rounded-xl border p-0 overflow-hidden shadow-xl transition-all duration-200",
        selected
          ? "border-[#fb923c] shadow-[0_0_20px_rgba(251,146,60,0.35)]"
          : isDone
          ? "border-[rgba(251,146,60,0.7)] shadow-[0_0_14px_rgba(251,146,60,0.2)]"
          : "border-[rgba(251,146,60,0.25)] hover:border-[rgba(251,146,60,0.55)]",
        isExecuting && "node-executing"
      )}
      style={{ background: "rgba(20,10,5,0.97)" }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2.5" style={{ background: "rgba(251,146,60,0.1)" }}>
        <div className="w-6 h-6 rounded-md flex items-center justify-center" style={{ background: "rgba(251,146,60,0.18)" }}>
          <MonitorPlay size={13} className="text-[#fb923c]" />
        </div>
        <span className="text-xs font-semibold text-[#fb923c] uppercase tracking-widest">Output</span>
        {isExecuting && (
          <span className="ml-auto flex h-2 w-2 rounded-full bg-[#fb923c] animate-ping" />
        )}
        {isDone && !isExecuting && (
          <span className="ml-auto text-[9px] text-[#fb923c]/70 bg-[rgba(251,146,60,0.1)] px-1.5 py-0.5 rounded font-mono">done</span>
        )}
      </div>

      {/* Body — fixed height with scroll */}
      <div className="px-3 py-2.5 h-[72px] overflow-y-auto scrollbar-thin scrollbar-track-transparent scrollbar-thumb-white/10">
        {displayText ? (
          <p className="text-xs text-white/75 leading-relaxed">{displayText}</p>
        ) : (
          <p className="text-xs italic text-white/25 mt-2">Awaiting execution…</p>
        )}
      </div>

      <Handle
        type="target"
        position={Position.Left}
        className="!w-3 !h-3 !border-2 !border-[#fb923c] !bg-[#14080a]"
      />
    </div>
  );
}
