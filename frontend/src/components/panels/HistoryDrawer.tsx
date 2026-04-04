"use client";
import { X, History, CheckCircle2, XCircle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWorkflowStore } from "@/store/workflowStore";
import { useEffect } from "react";

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function HistoryDrawer({ isOpen, onClose }: HistoryDrawerProps) {
  const { runsHistory, loadHistory } = useWorkflowStore();

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen, loadHistory]);

  return (
    <div
      className={cn(
        "fixed bottom-0 left-0 right-0 z-50 glass border-t border-white/10 transition-transform duration-300 ease-[cubic-bezier(0.2,0.8,0.2,1)] will-change-transform shadow-[0_-20px_40px_rgba(0,0,0,0.5)]",
        isOpen ? "translate-y-0" : "translate-y-[100%]"
      )}
      style={{ height: "45vh" }}
    >
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-white/[0.02]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-teal-500/20 flex items-center justify-center">
              <History size={16} className="text-teal-400" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-white/90">Execution History</h2>
              <p className="text-xs text-white/50">Past workflow runs</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-white/10 text-white/50 hover:text-white transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-custom">
          {runsHistory.length === 0 ? (
            <div className="text-white/40 text-sm flex flex-col pt-10 items-center justify-center space-y-4">
              <History size={32} className="opacity-20" />
              <p>No history found</p>
            </div>
          ) : (
            <div className="grid gap-3">
              {runsHistory.map((run, idx) => {
                const status = run.response?.status;
                const isSuccess = status === "success";
                const totalDuration = run.response?.total_duration_ms ?? 0;
                let parsedDate = "Unknown";
                try {
                  parsedDate = new Date(run.timestamp).toLocaleString();
                } catch {}

                return (
                  <div key={run.id || idx} className="flex flex-col bg-black/40 rounded border border-white/10 p-3 hover:bg-black/60 transition-colors">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {isSuccess ? <CheckCircle2 size={14} className="text-emerald-400" /> : <XCircle size={14} className="text-red-400" />}
                        <span className="text-xs font-mono text-white/50">ID: {run.id?.slice(0, 8)}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs text-white/40">{parsedDate}</span>
                        <div className="flex items-center gap-1 text-xs text-white/40 bg-white/5 px-2 py-0.5 rounded">
                          <Clock size={12} />
                          {totalDuration}ms
                        </div>
                      </div>
                    </div>
                    {/* Basic output preview */}
                    <div className="text-xs text-emerald-100/70 font-mono pl-5 line-clamp-2">
                       {JSON.stringify(run.response?.final_output) || "No output"}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
