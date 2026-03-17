"use client";
import { ReactFlowProvider } from "@xyflow/react";
import { Topbar } from "@/components/Topbar";
import { WorkflowCanvas } from "@/components/WorkflowCanvas";
import { PropertiesPanel } from "@/components/panels/PropertiesPanel";

export default function Home() {
  return (
    <ReactFlowProvider>
      <div className="flex flex-col h-screen w-screen overflow-hidden bg-[oklch(10%_0.02_265)]">
        <Topbar />
        <div className="flex flex-1 overflow-hidden">
          <main className="flex-1 relative overflow-hidden">
            <WorkflowCanvas />
          </main>
          <PropertiesPanel />
        </div>
      </div>
    </ReactFlowProvider>
  );
}
