"use client";
import { useCallback, useEffect } from "react";
import {
  ReactFlow,
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useWorkflowStore } from "@/store/workflowStore";
import { InputNode } from "@/components/nodes/InputNode";
import { LLMNode } from "@/components/nodes/LLMNode";
import { OutputNode } from "@/components/nodes/OutputNode";

const nodeTypes = {
  inputNode: InputNode,
  llmNode: LLMNode,
  outputNode: OutputNode,
};

export function WorkflowCanvas() {
  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    setSelectedNodeId,
  } = useWorkflowStore();

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: { id: string }) => {
      setSelectedNodeId(node.id);
    },
    [setSelectedNodeId]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNodeId(null);
  }, [setSelectedNodeId]);

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        defaultEdgeOptions={{
          animated: false,
          style: { strokeWidth: 2, stroke: "rgba(148,100,255,0.5)" },
        }}
        connectionLineStyle={{ stroke: "rgba(148,100,255,0.8)", strokeWidth: 2 }}
        proOptions={{ hideAttribution: true }}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={24}
          size={1}
          color="rgba(255,255,255,0.06)"
        />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            if (node.type === "inputNode") return "#4ade80";
            if (node.type === "llmNode") return "#818cf8";
            return "#fb923c";
          }}
          maskColor="rgba(5,4,15,0.8)"
          style={{ height: 100 }}
        />
      </ReactFlow>
    </div>
  );
}
