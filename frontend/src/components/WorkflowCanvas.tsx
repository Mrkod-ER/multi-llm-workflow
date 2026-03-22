"use client";
import { useState, useCallback } from "react";
import {
  ReactFlow,
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useWorkflowStore } from "@/store/workflowStore";
import { InputNode } from "@/components/nodes/InputNode";
import { LLMNode } from "@/components/nodes/LLMNode";
import { OutputNode } from "@/components/nodes/OutputNode";
import { AnimatedDataEdge } from "@/components/edges/AnimatedDataEdge";
import { CanvasContextMenu } from "@/components/CanvasContextMenu";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { useAutoLayout } from "@/hooks/useAutoLayout";

const nodeTypes = {
  inputNode: InputNode,
  llmNode: LLMNode,
  outputNode: OutputNode,
};

const edgeTypes = {
  animatedData: AnimatedDataEdge,
};

interface ContextMenuState {
  screenX: number;
  screenY: number;
  canvasX: number;
  canvasY: number;
}

export function WorkflowCanvas() {
  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    setSelectedNodeId,
  } = useWorkflowStore();

  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const { screenToFlowPosition } = useReactFlow();

  // Register keyboard shortcuts
  useKeyboardShortcuts();

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: { id: string }) => {
      setSelectedNodeId(node.id);
    },
    [setSelectedNodeId]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNodeId(null);
    setContextMenu(null);
  }, [setSelectedNodeId]);

  const onPaneContextMenu = useCallback(
    (e: React.MouseEvent | MouseEvent) => {
      e.preventDefault();
      const clientX = "clientX" in e ? e.clientX : 0;
      const clientY = "clientY" in e ? e.clientY : 0;
      const canvasPos = screenToFlowPosition({ x: clientX, y: clientY });
      setContextMenu({ screenX: clientX, screenY: clientY, canvasX: canvasPos.x, canvasY: canvasPos.y });
    },
    [screenToFlowPosition]
  );

  return (
    <div className="w-full h-full relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        onPaneContextMenu={onPaneContextMenu}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        defaultEdgeOptions={{
          type: "animatedData",
          style: { strokeWidth: 2 },
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

      {contextMenu && (
        <CanvasContextMenu
          x={contextMenu.screenX}
          y={contextMenu.screenY}
          canvasX={contextMenu.canvasX}
          canvasY={contextMenu.canvasY}
          onClose={() => setContextMenu(null)}
        />
      )}
    </div>
  );
}
