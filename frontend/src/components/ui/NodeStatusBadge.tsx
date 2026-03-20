"use client";
import { cn } from "@/lib/utils";

type NodeStatus = "idle" | "running" | "success" | "error";

const STATUS_CONFIG: Record<NodeStatus, { label: string; color: string; bg: string; dot: string }> = {
  idle: { label: "Idle", color: "text-white/30", bg: "bg-white/[0.04]", dot: "bg-white/20" },
  running: { label: "Running", color: "text-violet-300", bg: "bg-violet-500/10", dot: "bg-violet-400 animate-ping" },
  success: { label: "Done", color: "text-emerald-400", bg: "bg-emerald-500/10", dot: "bg-emerald-400" },
  error: { label: "Error", color: "text-red-400", bg: "bg-red-500/10", dot: "bg-red-400" },
};

interface NodeStatusBadgeProps {
  status: NodeStatus;
  durationMs?: number;
}

export function NodeStatusBadge({ status, durationMs }: NodeStatusBadgeProps) {
  const cfg = STATUS_CONFIG[status];

  return (
    <div className={cn("flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-medium", cfg.bg, cfg.color)}>
      <span className={cn("w-1.5 h-1.5 rounded-full", cfg.dot)} />
      {cfg.label}
      {status === "success" && durationMs !== undefined && (
        <span className="opacity-60">{durationMs.toFixed(0)}ms</span>
      )}
    </div>
  );
}
