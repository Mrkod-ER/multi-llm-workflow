"use client";
import { X, CheckCircle2, XCircle, Clock, ChevronRight } from "lucide-react";
import { useWorkflowStore } from "@/store/workflowStore";
import { cn } from "@/lib/utils";

interface ResultsDrawerProps {
  open: boolean;
  onClose: () => void;
}

export function ResultsDrawer({ open, onClose }: ResultsDrawerProps) {
  const { runResult } = useWorkflowStore();

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div className="fixed inset-0 z-30 bg-black/30 backdrop-blur-[2px]" onClick={onClose} />
      )}

      {/* Drawer panel */}
      <div
        className={cn(
          "fixed bottom-0 left-0 right-0 z-40 transition-transform duration-300 ease-in-out",
          open ? "translate-y-0" : "translate-y-full"
        )}
        style={{ maxHeight: "45vh" }}
      >
        <div
          className="mx-4 mb-4 rounded-2xl border border-white/10 overflow-hidden shadow-2xl"
          style={{ background: "rgba(14,11,28,0.97)", backdropFilter: "blur(16px)" }}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-3 border-b border-white/[0.06]">
            <div className="flex items-center gap-3">
              {runResult?.status === "success" ? (
                <CheckCircle2 size={16} className="text-emerald-400" />
              ) : (
                <XCircle size={16} className="text-red-400" />
              )}
              <span className="text-sm font-semibold text-white/90">
                Execution {runResult?.status === "success" ? "Completed" : "Failed"}
              </span>
              {runResult && (
                <span className="text-xs text-white/40 flex items-center gap-1">
                  <Clock size={11} />
                  {runResult.total_duration_ms.toFixed(0)}ms total
                </span>
              )}
            </div>
            <button id="close-results-drawer" onClick={onClose} className="p-1.5 rounded-lg text-white/30 hover:text-white/70 hover:bg-white/5 transition-colors">
              <X size={14} />
            </button>
          </div>

          {/* Results table */}
          <div className="overflow-y-auto p-4 space-y-2" style={{ maxHeight: "calc(45vh - 56px)" }}>
            {runResult?.results.map((result) => (
              <div
                key={result.node_id}
                className="flex items-start gap-3 p-3 rounded-xl border border-white/[0.06] bg-white/[0.02]"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    {result.error ? (
                      <XCircle size={12} className="text-red-400 shrink-0" />
                    ) : (
                      <CheckCircle2 size={12} className="text-emerald-400 shrink-0" />
                    )}
                    <span className="text-xs font-mono text-white/60">{result.node_id}</span>
                    <span className="ml-auto text-[10px] text-white/30">{result.duration_ms.toFixed(1)}ms</span>
                  </div>
                  {result.error ? (
                    <p className="text-xs text-red-400/80 leading-relaxed">{result.error}</p>
                  ) : (
                    <p className="text-xs text-white/60 leading-relaxed line-clamp-2">
                      {typeof result.output === "string"
                        ? result.output
                        : JSON.stringify(result.output, null, 2)}
                    </p>
                  )}
                </div>
              </div>
            ))}
            {!runResult?.results.length && (
              <p className="text-sm text-white/30 text-center py-4">No results yet. Run a workflow first.</p>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
