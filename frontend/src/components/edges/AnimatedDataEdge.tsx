"use client";
import {
  BaseEdge,
  getStraightPath,
  type EdgeProps,
} from "@xyflow/react";

/**
 * AnimatedDataEdge — a custom React Flow edge that renders an animated
 * "data packet" particle travelling from source to target along the path.
 */
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
  const [edgePath] = getStraightPath({ sourceX, sourceY, targetX, targetY });

  const strokeColor = selected ? "rgba(148,100,255,0.9)" : "rgba(148,100,255,0.45)";

  return (
    <>
      <BaseEdge
        id={id}
        path={edgePath}
        style={{ stroke: strokeColor, strokeWidth: selected ? 2.5 : 2 }}
      />
      {/* Animated travelling dot */}
      <circle r="4" fill="rgba(148,100,255,0.9)">
        <animateMotion dur="1.6s" repeatCount="indefinite" path={edgePath} />
      </circle>
    </>
  );
}
