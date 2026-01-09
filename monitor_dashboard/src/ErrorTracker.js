import React from "react";
export default function ErrorTracker() {
  // Placeholder: Replace with real error log data
  const errors = [
    { time: '12:01', msg: 'No errors detected.' }
  ];
  return (
    <div style={{ background: '#23272e', borderRadius: 8, padding: 16, minWidth: 220 }}>
      <h2>Error Tracker</h2>
      <ul style={{ fontSize: 14, color: '#ff5252', paddingLeft: 18 }}>
        {errors.map((e, i) => (
          <li key={i}>{e.time}: {e.msg}</li>
        ))}
      </ul>
    </div>
  );
}
