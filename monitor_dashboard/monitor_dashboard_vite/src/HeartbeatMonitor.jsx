import React from "react";
export default function HeartbeatMonitor() {
  // Placeholder: Replace with real data source
  const bpm = 72 + Math.round(Math.random() * 4 - 2);
  return (
    <div style={{ background: '#23272e', borderRadius: 8, padding: 16, minWidth: 220 }}>
      <h2>Heartbeat</h2>
      <div style={{ fontSize: 48, fontWeight: 700, color: bpm > 80 ? '#ff5252' : '#4caf50' }}>{bpm} BPM</div>
      <div style={{ fontSize: 14, color: '#aaa' }}>System Pulse</div>
    </div>
  );
}
