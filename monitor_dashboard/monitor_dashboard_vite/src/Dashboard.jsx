import React from "react";
import HeartbeatMonitor from "./HeartbeatMonitor";
import ChatInterface from "./ChatInterface";
import LogicTracer from "./LogicTracer";
import Dreaming2D from "./Dreaming2D";
import Dreaming3D from "./Dreaming3D";
import MemoryMonitor from "./MemoryMonitor";
import ErrorTracker from "./ErrorTracker";

export default function Dashboard() {
  return (
    <div className="sovereign-app">
      <header style={{ padding: '0 20px', paddingTop: '20px' }}>
         <h1 style={{ fontSize: '1.5rem', color: 'var(--accent-pulse)' }}>Sovereign Monitor</h1>
         <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>System Status: RESONANT</p>
      </header>

      <main className="dashboard-grid">
        <div style={{ gridColumn: '1 / -1' }}>
            <ChatInterface />
        </div>
        <div className="card"><HeartbeatMonitor /></div>
        <div className="card"><LogicTracer /></div>
        <div className="card"><Dreaming2D /></div>
        <div className="card"><Dreaming3D /></div>
        <div className="card"><MemoryMonitor /></div>
        <div className="card"><ErrorTracker /></div>
      </main>
    </div>
  );
}
