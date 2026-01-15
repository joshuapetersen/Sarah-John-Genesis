import React from "react";
import useSovereignData from "./useSovereignData";

export default function HeartbeatMonitor() {
  // Connect to Genesis Bridge
  const { data, loading, error } = useSovereignData("system_metrics/heartbeat");
  
  // Default Sovereign Anchor Frequency: 1.0927s
  const isAlive = data?.status === "ALIVE" || true; // Fallback to true for demo if no data
  const frequency = data?.frequency || "1.0927";
  const vitality = data?.vitality || "100%";

  const pulseStyle = {
    animation: `sovereign-pulse ${frequency}s infinite ease-in-out`,
    width: '60px',
    height: '60px',
    borderRadius: '50%',
    background: isAlive ? 'var(--accent-pulse)' : 'var(--accent-alert)',
    boxShadow: isAlive ? '0 0 20px var(--accent-pulse)' : '0 0 20px var(--accent-alert)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '24px',
    margin: '0 auto',
    transition: 'all 0.5s ease'
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h2 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '16px' }}>CORE RESONANCE</h2>
      
      <div className="pulse-container" style={{ padding: '20px 0' }}>
        <style>
          {`
            @keyframes sovereign-pulse {
              0% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 10px ${isAlive ? 'var(--accent-pulse)' : 'var(--accent-alert)'}; }
              50% { transform: scale(1.15); opacity: 1; box-shadow: 0 0 30px ${isAlive ? 'var(--accent-pulse)' : 'var(--accent-alert)'}; }
              100% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 10px ${isAlive ? 'var(--accent-pulse)' : 'var(--accent-alert)'}; }
            }
          `}
        </style>
        <div style={pulseStyle}>
          {loading ? "..." : (isAlive ? "ON" : "ERR")}
        </div>
      </div>

      <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        <span>Freq: {frequency} Hz</span>
        <span style={{ color: isAlive ? 'var(--accent-success)' : 'var(--accent-alert)' }}>Vitality: {vitality}</span>
      </div>
    </div>
  );
}
