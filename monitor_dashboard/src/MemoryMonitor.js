import React from "react";
export default function MemoryMonitor() {
  // Placeholder: Replace with real memory data
  const used = 2.1, total = 8.0;
  return (
    <div style={{ background: '#23272e', borderRadius: 8, padding: 16, minWidth: 220 }}>
      <h2>Memory</h2>
      <div style={{ fontSize: 32, color: '#ffd600' }}>{used} / {total} GB</div>
      <div style={{ fontSize: 14, color: '#aaa' }}>Active Memory</div>
    </div>
  );
}
