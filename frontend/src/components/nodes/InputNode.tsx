"use client";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";

export function InputNode({ id, data, selected }: NodeProps) {
  const { executingNodeId } = useWorkflowStore();
  const isExecuting = executingNodeId === id;

  return (
    <div
      className={cn(
        "min-w-[220px] rounded-xl border p-0 overflow-hidden shadow-xl transition-all duration-200",
        selected
          ? "border-[#4ade80] shadow-[0_0_20px_rgba(74,222,128,0.3)]"
          : "border-[rgba(74,222,128,0.3)] hover:border-[#4ade80]",
        isExecuting && "node-executing"
      )}
      style={{ background: "rgba(10,20,14,0.93)" }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2" style={{ background: "rgba(74,222,128,0.12)" }}>
        <div className="w-6 h-6 rounded-md flex items-center justify-center" style={{ background: "rgba(74,222,128,0.2)" }}>
          <FileText size={13} className="text-[#4ade80]" />
        </div>
        <span className="text-xs font-semibold text-[#4ade80] uppercase tracking-widest">Input</span>
        {isExecuting && (
          <span className="ml-auto flex h-2 w-2 rounded-full bg-[#4ade80] animate-ping" />
        )}
      </div>
      {/* Body */}
      <div className="px-3 py-2">
        <p className="text-[11px] text-white/50 mb-1">Prompt Text</p>
        <p className="text-xs text-white/80 leading-relaxed line-clamp-3">
          {(data as any).text || <span className="italic text-white/30">Empty prompt…</span>}
        </p>
      </div>
      <Handle type="source" position={Position.Right} className="!w-3 !h-3 !border-2 !border-[#4ade80] !bg-[#0a140e]" />
    </div>
  );
}
