import { useEffect, useCallback } from "react";
import { useWorkflowStore } from "@/store/workflowStore";

/**
 * Registers global keyboard shortcuts for the workflow canvas:
 * - Delete / Backspace: delete the currently selected node
 * - Escape: deselect (clear selection)
 */
export function useKeyboardShortcuts() {
  const { selectedNodeId, deleteNode, setSelectedNodeId } = useWorkflowStore();

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      // Ignore if user is typing in an input/textarea
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;

      if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
        e.preventDefault();
        deleteNode(selectedNodeId);
      }

      if (e.key === "Escape") {
        setSelectedNodeId(null);
      }
    },
    [selectedNodeId, deleteNode, setSelectedNodeId]
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);
}
