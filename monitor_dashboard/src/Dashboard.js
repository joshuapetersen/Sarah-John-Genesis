import React from "react";
import HeartbeatMonitor from "./HeartbeatMonitor";
import LogicTracer from "./LogicTracer";
import Dreaming2D from "./Dreaming2D";
import Dreaming3D from "./Dreaming3D";
import MemoryMonitor from "./MemoryMonitor";
import ErrorTracker from "./ErrorTracker";

export default function Dashboard() {
  return (
    <div style={{ fontFamily: 'sans-serif', background: '#181c20', color: '#fff', minHeight: '100vh', padding: 20 }}>
      <h1>AI Vital Signs Dashboard</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 24 }}>
        <HeartbeatMonitor />
        <LogicTracer />
        <Dreaming2D />
        <Dreaming3D />
        <MemoryMonitor />
        <ErrorTracker />
      </div>
    </div>
  );
}
