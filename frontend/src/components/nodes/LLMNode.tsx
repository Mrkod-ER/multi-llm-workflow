"use client";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { BrainCircuit } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";

const PROVIDER_COLORS: Record<string, string> = {
  openai: "#10a37f",
  ollama: "#7c3aed",
  mock: "#6366f1",
};

export function LLMNode({ id, data, selected }: NodeProps) {
  const { nodeStatuses, streamingTexts } = useWorkflowStore();
  const isExecuting = nodeStatuses[id] === "running";
  const streamingText = streamingTexts[id];
  const provider = String((data as any).provider ?? "mock");
  const accentColor = PROVIDER_COLORS[provider] ?? "#6366f1";

  return (
    <div
      className={cn(
        "min-w-[240px] rounded-xl border p-0 overflow-hidden shadow-xl transition-all duration-200",
        selected
          ? "shadow-[0_0_20px_rgba(99,102,241,0.4)]"
          : "hover:shadow-[0_0_12px_rgba(99,102,241,0.2)]",
        isExecuting && "node-executing"
      )}
      style={{
        background: "rgba(12,10,28,0.95)",
        borderColor: selected ? accentColor : `${accentColor}55`,
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2" style={{ background: `${accentColor}18` }}>
        <div className="w-6 h-6 rounded-md flex items-center justify-center" style={{ background: `${accentColor}28` }}>
          <BrainCircuit size={13} style={{ color: accentColor }} />
        </div>
        <span className="text-xs font-semibold uppercase tracking-widest" style={{ color: accentColor }}>LLM</span>
        <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded font-mono" style={{ background: `${accentColor}22`, color: accentColor }}>
          {provider}
        </span>
        {isExecuting && (
          <span className="flex h-2 w-2 rounded-full animate-ping" style={{ background: accentColor }} />
        )}
      </div>
      {/* Body */}
      <div className="px-3 py-2 space-y-1.5">
        {!streamingText && (
          <>
            <div>
              <p className="text-[10px] text-white/40 mb-0.5">Model</p>
              <p className="text-xs text-white/80 font-mono">{(data as any).model || "—"}</p>
            </div>
            <div>
              <p className="text-[10px] text-white/40 mb-0.5">System Prompt</p>
              <p className="text-xs text-white/60 leading-relaxed line-clamp-2">
                {(data as any).system_prompt || <span className="italic text-white/25">No prompt set…</span>}
              </p>
            </div>
          </>
        )}
        {streamingText && (
          <div className="pt-0.5">
            <p className="text-[10px] uppercase tracking-wider mb-1" style={{ color: accentColor }}>Output Stream</p>
            <p className="text-xs text-white/90 leading-relaxed line-clamp-4 font-mono break-words">
              {streamingText}
              {isExecuting && <span className="inline-block w-1.5 h-3 ml-0.5 align-middle animate-pulse bg-white/70" />}
            </p>
          </div>
        )}
      </div>
      <Handle type="target" position={Position.Left} className="!w-3 !h-3 !border-2 !bg-[#0c0a1c]" style={{ borderColor: accentColor }} />
      <Handle type="source" position={Position.Right} className="!w-3 !h-3 !border-2 !bg-[#0c0a1c]" style={{ borderColor: accentColor }} />
    </div>
  );
}
