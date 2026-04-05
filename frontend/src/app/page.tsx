"use client";
import { useState } from "react";
import { ReactFlowProvider } from "@xyflow/react";
import { Topbar } from "@/components/Topbar";
import { WorkflowCanvas } from "@/components/WorkflowCanvas";
import { PropertiesPanel } from "@/components/panels/PropertiesPanel";
import { ResultsDrawer } from "@/components/panels/ResultsDrawer";

import { HistoryDrawer } from "@/components/panels/HistoryDrawer";

export default function Home() {
  const [showResults, setShowResults] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  return (
    <ReactFlowProvider>
      <div className="flex flex-col h-screen w-screen overflow-hidden bg-[oklch(10%_0.02_265)]">
        <Topbar 
          onShowResults={() => setShowResults(true)} 
          onShowHistory={() => setShowHistory(true)} 
        />
        <div className="flex flex-1 overflow-hidden">
          <main className="flex-1 relative overflow-hidden">
            <WorkflowCanvas />
          </main>
          <PropertiesPanel />
        </div>
        <ResultsDrawer open={showResults} onClose={() => setShowResults(false)} />
        <HistoryDrawer isOpen={showHistory} onClose={() => setShowHistory(false)} />
      </div>
    </ReactFlowProvider>
  );
}
