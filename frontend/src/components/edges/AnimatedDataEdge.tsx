"use client";
import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  useReactFlow,
  type EdgeProps,
} from "@xyflow/react";

export function AnimatedDataEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  selected,
}: EdgeProps) {
  const { setEdges } = useReactFlow();

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const strokeColor = selected ? "rgba(148,100,255,1)" : "rgba(148,100,255,0.4)";

  const deleteEdge = () => {
    setEdges((edges) => edges.filter((e) => e.id !== id));
  };

  return (
    <>
      <BaseEdge
        id={id}
        path={edgePath}
        style={{ stroke: strokeColor, strokeWidth: selected ? 2.5 : 1.8 }}
      />
      {/* Animated travelling dot */}
      <circle r="3.5" fill="rgba(148,100,255,0.9)">
        <animateMotion dur="1.8s" repeatCount="indefinite" path={edgePath} />
      </circle>

      {/* Delete button — visible on hover/select */}
      <EdgeLabelRenderer>
        <div
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            pointerEvents: "all",
            opacity: selected ? 1 : 0,
            transition: "opacity 0.15s ease",
          }}
          className="nodrag nopan group"
        >
          <button
            onClick={deleteEdge}
            className="flex items-center justify-center w-5 h-5 rounded-full bg-red-500/80 hover:bg-red-500 border border-red-400/60 text-white text-[10px] font-bold shadow-lg transition-all duration-150 hover:scale-110"
            title="Delete edge"
          >
            ×
          </button>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
