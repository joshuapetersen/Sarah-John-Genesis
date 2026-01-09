import React from "react";
export default function LogicTracer() {
  // Placeholder: Replace with real logic trace data
  const trace = [
    "Input received",
    "Preprocessing",
    "Vector expansion",
    "Decision node: Alpha",
    "Output generated"
  ];
  return (
    <div style={{ background: '#23272e', borderRadius: 8, padding: 16, minWidth: 220 }}>
      <h2>Logic Trace</h2>
      <ul style={{ fontSize: 15, color: '#fff', paddingLeft: 18 }}>
        {trace.map((step, i) => (
          <li key={i}>{step}</li>
        ))}
      </ul>
    </div>
  );
}
