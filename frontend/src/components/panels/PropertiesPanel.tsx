"use client";
import { useWorkflowStore } from "@/store/workflowStore";
import { NodeType } from "@/lib/types";
import { Trash2, X, ChevronDown } from "lucide-react";

const PROVIDERS = [
  { value: "mock",   label: "Mock (Test)",     color: "#6366f1" },
  { value: "openai", label: "OpenAI",           color: "#10a37f" },
  { value: "gemini", label: "Google Gemini",    color: "#4285f4" },
  { value: "ollama", label: "Ollama (Local)",   color: "#7c3aed" },
];

export function PropertiesPanel() {
  const { nodes, selectedNodeId, setSelectedNodeId, updateNodeData, deleteNode } = useWorkflowStore();
  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  if (!selectedNode) {
    return (
      <aside className="w-72 shrink-0 border-l border-white/[0.06] flex flex-col items-center justify-center p-6 text-center"
        style={{ background: "rgba(8,6,20,0.97)" }}>
        <div className="w-14 h-14 rounded-2xl border border-white/[0.07] flex items-center justify-center mb-4"
          style={{ background: "rgba(255,255,255,0.03)" }}>
          <span className="text-2xl">👆</span>
        </div>
        <p className="text-sm font-medium text-white/30">Select a node</p>
        <p className="text-xs text-white/20 mt-1">Click any node to edit its properties</p>
      </aside>
    );
  }

  const data = selectedNode.data as any;
  const nodeType: NodeType = data.type;

  return (
    <aside className="w-72 shrink-0 border-l border-white/[0.06] flex flex-col overflow-y-auto"
      style={{ background: "rgba(8,6,20,0.97)" }}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3.5 border-b border-white/[0.06]"
        style={{ background: "rgba(255,255,255,0.02)" }}>
        <div>
          <p className="text-[9px] text-white/30 uppercase tracking-[0.15em] mb-0.5">Properties</p>
          <p className="text-sm font-semibold text-white/90 capitalize">{nodeType} Node</p>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => { deleteNode(selectedNode.id); }}
            className="p-1.5 rounded-lg text-red-400/50 hover:bg-red-500/10 hover:text-red-400 transition-colors"
            title="Delete Node"
          >
            <Trash2 size={13} />
          </button>
          <button
            onClick={() => setSelectedNodeId(null)}
            className="p-1.5 rounded-lg text-white/25 hover:text-white/60 hover:bg-white/5 transition-colors"
          >
            <X size={13} />
          </button>
        </div>
      </div>

      {/* Fields */}
      <div className="p-4 space-y-5 flex-1">
        {nodeType === NodeType.INPUT && (
          <Field label="Prompt Text">
            <textarea
              id="input-text-field"
              rows={5}
              className="w-full rounded-lg px-3 py-2.5 text-sm text-white/80 placeholder:text-white/20 focus:outline-none resize-none transition-colors"
              style={{
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
              onFocus={(e) => (e.target.style.borderColor = "rgba(74,222,128,0.5)")}
              onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
              placeholder="Enter the initial prompt text…"
              value={data.text ?? ""}
              onChange={(e) => updateNodeData(selectedNode.id, { text: e.target.value })}
            />
          </Field>
        )}

        {nodeType === NodeType.LLM && (
          <>
            <Field label="Provider">
              <div className="relative">
                <select
                  id="llm-provider-select"
                  className="w-full appearance-none rounded-lg px-3 py-2.5 text-sm text-white/80 focus:outline-none cursor-pointer pr-8 transition-colors"
                  style={{
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    color: "rgba(255,255,255,0.8)",
                  }}
                  value={data.provider ?? "mock"}
                  onChange={(e) => updateNodeData(selectedNode.id, { provider: e.target.value })}
                >
                  {PROVIDERS.map((p) => (
                    <option key={p.value} value={p.value} style={{ background: "#0c0a1c", color: "#e2e8f0" }}>
                      {p.label}
                    </option>
                  ))}
                </select>
                <ChevronDown size={13} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30 pointer-events-none" />
              </div>
            </Field>

            <Field label="Model Name">
              <input
                id="llm-model-input"
                type="text"
                className="w-full rounded-lg px-3 py-2.5 text-sm text-white/80 placeholder:text-white/20 focus:outline-none transition-colors font-mono"
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
                onFocus={(e) => (e.target.style.borderColor = "rgba(99,102,241,0.5)")}
                onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
                placeholder="e.g. gpt-4o, gemini-1.5-flash, llama3"
                value={data.model ?? ""}
                onChange={(e) => updateNodeData(selectedNode.id, { model: e.target.value })}
              />
              <p className="text-[10px] text-white/25 mt-1">
                {data.provider === "gemini" && "Try: gemini-2.5-flash, gemini-1.5-flash, gemini-1.5-pro"}
                {data.provider === "openai" && "Try: gpt-4o, gpt-4-turbo, gpt-3.5-turbo"}
                {data.provider === "ollama" && "Try: llama3, mistral, phi3"}
                {data.provider === "mock" && "Any name works for mock testing"}
              </p>
            </Field>

            <Field label="System Prompt">
              <textarea
                id="llm-system-prompt-field"
                rows={5}
                className="w-full rounded-lg px-3 py-2.5 text-sm text-white/80 placeholder:text-white/20 focus:outline-none resize-none transition-colors"
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
                onFocus={(e) => (e.target.style.borderColor = "rgba(99,102,241,0.5)")}
                onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
                placeholder="You are a helpful assistant…"
                value={data.system_prompt ?? ""}
                onChange={(e) => updateNodeData(selectedNode.id, { system_prompt: e.target.value })}
              />
            </Field>
          </>
        )}

        {nodeType === NodeType.OUTPUT && (
          <Field label="Result (read-only)">
            <textarea
              readOnly
              rows={8}
              className="w-full rounded-lg px-3 py-2.5 text-sm text-white/50 resize-none cursor-default leading-relaxed"
              style={{
                background: "rgba(255,255,255,0.02)",
                border: "1px solid rgba(255,255,255,0.05)",
              }}
              placeholder="Output will appear here after run…"
              value={typeof data.result === "string" ? data.result : ""}
            />
          </Field>
        )}

        {/* Node ID */}
        <div className="pt-2 border-t border-white/[0.05]">
          <p className="text-[10px] text-white/20">
            Node: <span className="font-mono text-white/30">{selectedNode.id}</span>
          </p>
        </div>
      </div>
    </aside>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <label className="block text-[10px] font-semibold text-white/40 uppercase tracking-[0.12em]">{label}</label>
      {children}
    </div>
  );
}
