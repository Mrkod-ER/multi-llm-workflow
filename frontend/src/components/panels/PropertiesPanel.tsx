"use client";
import { useWorkflowStore } from "@/store/workflowStore";
import { NodeType } from "@/lib/types";
import { Trash2, X } from "lucide-react";

export function PropertiesPanel() {
  const { nodes, selectedNodeId, setSelectedNodeId, updateNodeData, deleteNode } = useWorkflowStore();
  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  if (!selectedNode) {
    return (
      <aside className="w-72 shrink-0 glass border-l border-white/[0.06] flex flex-col items-center justify-center p-6 text-center">
        <div className="w-12 h-12 rounded-xl bg-white/[0.04] flex items-center justify-center mb-3">
          <span className="text-2xl">👆</span>
        </div>
        <p className="text-sm text-white/40">Click any node to edit its properties</p>
      </aside>
    );
  }

  const data = selectedNode.data as any;
  const nodeType: NodeType = data.type;

  return (
    <aside className="w-72 shrink-0 glass border-l border-white/[0.06] flex flex-col overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06]">
        <div>
          <p className="text-[10px] text-white/40 uppercase tracking-widest mb-0.5">Properties</p>
          <p className="text-sm font-semibold text-white/90">{nodeType} Node</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => { deleteNode(selectedNode.id); }}
            className="p-1.5 rounded-lg text-red-400/60 hover:bg-red-500/10 hover:text-red-400 transition-colors"
            title="Delete Node"
          >
            <Trash2 size={13} />
          </button>
          <button
            onClick={() => setSelectedNodeId(null)}
            className="p-1.5 rounded-lg text-white/30 hover:text-white/70 hover:bg-white/5 transition-colors"
          >
            <X size={13} />
          </button>
        </div>
      </div>

      {/* Fields */}
      <div className="p-4 space-y-4 flex-1">
        {nodeType === NodeType.INPUT && (
          <Field label="Prompt Text">
            <textarea
              id="input-text-field"
              rows={5}
              className="w-full bg-white/[0.04] border border-white/10 rounded-lg px-3 py-2 text-sm text-white/80 placeholder:text-white/25 focus:outline-none focus:border-violet-500/60 resize-none"
              placeholder="Enter the initial prompt text…"
              value={data.text ?? ""}
              onChange={(e) => updateNodeData(selectedNode.id, { text: e.target.value })}
            />
          </Field>
        )}

        {nodeType === NodeType.LLM && (
          <>
            <Field label="Provider">
              <select
                id="llm-provider-select"
                className="w-full bg-white/[0.04] border border-white/10 rounded-lg px-3 py-2 text-sm text-white/80 focus:outline-none focus:border-violet-500/60"
                value={data.provider ?? "mock"}
                onChange={(e) => updateNodeData(selectedNode.id, { provider: e.target.value })}
              >
                <option value="mock">Mock (Test)</option>
                <option value="openai">OpenAI</option>
                <option value="ollama">Ollama (Local)</option>
              </select>
            </Field>
            <Field label="Model Name">
              <input
                id="llm-model-input"
                type="text"
                className="w-full bg-white/[0.04] border border-white/10 rounded-lg px-3 py-2 text-sm text-white/80 placeholder:text-white/25 focus:outline-none focus:border-violet-500/60"
                placeholder="e.g. gpt-4o, llama3, mock-model"
                value={data.model ?? ""}
                onChange={(e) => updateNodeData(selectedNode.id, { model: e.target.value })}
              />
            </Field>
            <Field label="System Prompt">
              <textarea
                id="llm-system-prompt-field"
                rows={5}
                className="w-full bg-white/[0.04] border border-white/10 rounded-lg px-3 py-2 text-sm text-white/80 placeholder:text-white/25 focus:outline-none focus:border-violet-500/60 resize-none"
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
              className="w-full bg-white/[0.02] border border-white/[0.06] rounded-lg px-3 py-2 text-sm text-white/60 resize-none cursor-default"
              placeholder="Output will appear here after run…"
              value={typeof data.result === "string" ? data.result : ""}
            />
          </Field>
        )}

        {/* Node ID */}
        <div className="pt-2 border-t border-white/[0.06]">
          <p className="text-[10px] text-white/25">Node ID: <span className="font-mono">{selectedNode.id}</span></p>
        </div>
      </div>
    </aside>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <label className="block text-[11px] font-medium text-white/50 uppercase tracking-wider">{label}</label>
      {children}
    </div>
  );
}
