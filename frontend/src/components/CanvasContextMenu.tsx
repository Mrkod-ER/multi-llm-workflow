"use client";
import { useEffect, useRef } from "react";
import { FileText, BrainCircuit, MonitorPlay, X } from "lucide-react";
import { useWorkflowStore } from "@/store/workflowStore";
import { NodeType } from "@/lib/types";

interface ContextMenuProps {
  x: number;
  y: number;
  canvasX: number;
  canvasY: number;
  onClose: () => void;
}

const MENU_ITEMS = [
  { type: NodeType.INPUT, label: "Add Input Node", icon: FileText, color: "#4ade80" },
  { type: NodeType.LLM, label: "Add LLM Node", icon: BrainCircuit, color: "#818cf8" },
  { type: NodeType.OUTPUT, label: "Add Output Node", icon: MonitorPlay, color: "#fb923c" },
];

export function CanvasContextMenu({ x, y, canvasX, canvasY, onClose }: ContextMenuProps) {
  const { addNode } = useWorkflowStore();
  const ref = useRef<HTMLDivElement>(null);

  // Close when clicking outside
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        onClose();
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [onClose]);

  return (
    <div
      ref={ref}
      id="canvas-context-menu"
      className="fixed z-50 min-w-[180px] rounded-xl overflow-hidden shadow-2xl border border-white/10 py-1"
      style={{ left: x, top: y, background: "rgba(18,14,34,0.97)", backdropFilter: "blur(12px)" }}
    >
      <p className="px-3 py-1.5 text-[10px] font-semibold text-white/30 uppercase tracking-widest">Add Node</p>
      {MENU_ITEMS.map(({ type, label, icon: Icon, color }) => (
        <button
          key={type}
          id={`ctx-add-${type.toLowerCase()}`}
          onClick={() => { addNode(type, { x: canvasX, y: canvasY }); onClose(); }}
          className="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-white/75 hover:text-white transition-colors"
          style={{ background: "transparent" }}
          onMouseEnter={(e) => (e.currentTarget.style.background = `${color}12`)}
          onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
        >
          <Icon size={13} style={{ color }} />
          {label}
        </button>
      ))}
      <div className="my-1 border-t border-white/[0.06]" />
      <button
        onClick={onClose}
        className="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-white/40 hover:text-white/60 transition-colors"
      >
        <X size={13} />
        Cancel
      </button>
    </div>
  );
}
