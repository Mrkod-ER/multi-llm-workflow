import dagre from "@dagrejs/dagre";
import { useCallback } from "react";
import { useReactFlow, type Node, type Edge } from "@xyflow/react";
import { useWorkflowStore } from "@/store/workflowStore";

const NODE_WIDTH = 260;
const NODE_HEIGHT = 120;

/**
 * Returns a function that auto-arranges all nodes in a left-to-right
 * hierarchical layout using the Dagre graph library.
 */
export function useAutoLayout() {
  const { setNodes } = useReactFlow();
  const { nodes, edges } = useWorkflowStore();

  const applyLayout = useCallback(() => {
    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    g.setGraph({ rankdir: "LR", nodesep: 60, ranksep: 80 });

    nodes.forEach((node) => {
      g.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
    });

    edges.forEach((edge) => {
      g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);

    const laidOutNodes: Node[] = nodes.map((node) => {
      const { x, y } = g.node(node.id);
      return {
        ...node,
        position: {
          x: x - NODE_WIDTH / 2,
          y: y - NODE_HEIGHT / 2,
        },
      };
    });

    setNodes(laidOutNodes);
  }, [nodes, edges, setNodes]);

  return { applyLayout };
}
