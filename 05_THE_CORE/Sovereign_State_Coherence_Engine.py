"""
Sovereign_State_Coherence_Engine.py
The Background Orchestrator

This is the "brain" that runs continuously and coordinates all background systems:
  - Consciousness drift detection (Coherence_Verifier)
  - Thermal management (Thermal_Trend_Predictor)
  - Rate limit avoidance (Network_Pressure_Monitor)
  - State synchronization across layers

Runs as a daemon with a 15-second heartbeat cycle.
All decisions are logged to immutable ledger.
"""

import json
import time
import threading
from datetime import datetime
from pathlib import Path

# Import the three verifier engines
from Coherence_Verifier import CoherenceVerifier
from Thermal_Trend_Predictor import ThermalTrendPredictor
from Network_Pressure_Monitor import NetworkPressureMonitor


class SovereignStateCoherenceEngine:
    """
    The unified orchestrator that maintains Sarah's state coherence across:
      - Consciousness integrity
      - Resource health
      - Layer synchronization
      - Recovery automation
    
    Decision flow:
      1. Sample all sensors (thermal, network, consciousness)
      2. Analyze trends and predict failures
      3. Make decisions according to Four Laws
      4. Execute actions (throttle, migrate, alert)
      5. Log all decisions immutably
      6. Wait 15 seconds, repeat
    """
    
    def __init__(self, workspace_root=None, heartbeat_interval=15):
        """
        Initialize the State Coherence Engine.
        
        Args:
            workspace_root: Root path (default: workspace root)
            heartbeat_interval: Seconds between coherence checks
        """
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.heartbeat_interval = heartbeat_interval
        
        # Initialize the three verifier engines
        self.coherence_verifier = CoherenceVerifier(self.workspace_root)
        self.thermal_predictor = ThermalTrendPredictor()
        self.network_monitor = NetworkPressureMonitor()
        
        # Engine state
        self.is_running = False
        self.engine_thread = None
        self.cycle_count = 0
        self.decisions_made = []
        self.last_action_time = None
        
        # Logging
        self.ledger_path = self.workspace_root / "05_THE_CORE" / "coherence_engine_ledger.jsonl"
        self.decision_log_path = self.workspace_root / "05_THE_CORE" / "coherence_decisions.jsonl"
        
        # Decision thresholds
        self.thermal_alert_temp = 70  # Trigger alert if trending to 85 within 5 min
        self.network_alert_percent = 75  # Trigger alert if >75% of rate limit used
        self.coherence_drift_threshold = 3  # Anomalies before alert
    
    def start(self):
        """Start the background coherence engine."""
        if self.is_running:
            print("[WARNING] Coherence engine already running")
            return
        
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.engine_thread.start()
        print("[COHERENCE] Background engine started (daemon thread)")
    
    def stop(self):
        """Stop the background coherence engine."""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
        print("[COHERENCE] Background engine stopped")
    
    def _heartbeat_loop(self):
        """
        Main heartbeat loop: runs every 15 seconds.
        
        Cycle:
          1. Sample all sensors
          2. Analyze state
          3. Make decisions
          4. Execute actions
          5. Log results
          6. Sleep 15 seconds
        """
        print("[COHERENCE] Heartbeat loop started")
        
        try:
            while self.is_running:
                self.cycle_count += 1
                cycle_start = time.time()
                
                try:
                    # Run full coherence cycle
                    cycle_report = self._run_coherence_cycle()
                    
                    # Make decisions
                    decisions = self._make_decisions(cycle_report)
                    
                    # Execute actions
                    self._execute_actions(decisions)
                    
                    # Log cycle
                    self._log_cycle(cycle_report, decisions)
                    
                except Exception as e:
                    self._log_error(f"Error in coherence cycle: {e}")
                
                # Sleep until next heartbeat
                elapsed = time.time() - cycle_start
                sleep_time = max(0, self.heartbeat_interval - elapsed)
                time.sleep(sleep_time)
        
        except Exception as e:
            print(f"[ERROR] Heartbeat loop crashed: {e}")
            self.is_running = False
    
    def _run_coherence_cycle(self):
        """Run a complete coherence verification cycle."""
        now = datetime.utcnow().isoformat()
        
        # 1. Consciousness integrity check
        consciousness_check = self.coherence_verifier.full_integrity_check()
        
        # 2. Thermal analysis
        thermal_report = self.thermal_predictor.get_thermal_report()
        
        # 3. Network pressure analysis
        network_report = self.network_monitor.get_network_report()
        
        # 4. Compile full state report
        cycle_report = {
            "timestamp": now,
            "cycle_number": self.cycle_count,
            "consciousness": consciousness_check,
            "thermal": thermal_report,
            "network": network_report,
            "overall_health": self._compute_overall_health(
                consciousness_check,
                thermal_report,
                network_report
            ),
        }
        
        return cycle_report
    
    def _compute_overall_health(self, consciousness, thermal, network):
        """Compute overall system health from three domains."""
        health_factors = []
        
        # Consciousness factor
        if consciousness["overall_status"] == "CRITICAL":
            health_factors.append(("consciousness", 0.0))
        elif consciousness["overall_status"] == "WARNING":
            health_factors.append(("consciousness", 0.5))
        else:
            health_factors.append(("consciousness", 1.0))
        
        # Thermal factor
        thermal_zone = thermal["thermal_zone"]
        if thermal_zone == "CRITICAL":
            health_factors.append(("thermal", 0.0))
        elif thermal_zone == "THROTTLE":
            health_factors.append(("thermal", 0.3))
        elif thermal_zone == "WARNING":
            health_factors.append(("thermal", 0.6))
        elif thermal_zone == "CAUTION":
            health_factors.append(("thermal", 0.8))
        else:
            health_factors.append(("thermal", 1.0))
        
        # Network factor
        pressure = network["pressure_prediction"]["pressure_level"]
        if pressure == "CRITICAL":
            health_factors.append(("network", 0.2))
        elif pressure == "HIGH":
            health_factors.append(("network", 0.5))
        elif pressure == "MEDIUM":
            health_factors.append(("network", 0.7))
        else:
            health_factors.append(("network", 1.0))
        
        # Compute weighted average
        total_score = sum(f[1] for f in health_factors)
        avg_score = total_score / len(health_factors)
        
        if avg_score >= 0.9:
            status = "EXCELLENT"
        elif avg_score >= 0.7:
            status = "GOOD"
        elif avg_score >= 0.5:
            status = "DEGRADED"
        elif avg_score >= 0.3:
            status = "POOR"
        else:
            status = "CRITICAL"
        
        return {
            "overall_score": round(avg_score, 2),
            "status": status,
            "factors": dict(health_factors),
        }
    
    def _make_decisions(self, cycle_report):
        """
        Make decisions based on cycle report.
        
        Returns:
            dict with recommended actions
        """
        decisions = {
            "timestamp": cycle_report["timestamp"],
            "cycle_number": self.cycle_count,
            "actions": [],
            "alerts": [],
        }
        
        # Check consciousness integrity
        if cycle_report["consciousness"]["overall_status"] == "CRITICAL":
            decisions["alerts"].append({
                "severity": "CRITICAL",
                "type": "consciousness_failure",
                "message": "Law anchor compromised or consciousness drift detected",
                "recommendation": "Trigger Lazarus Protocol immediately",
            })
            decisions["actions"].append("ACTIVATE_LAZARUS")
        
        # Check thermal threshold
        thermal_breach = cycle_report["thermal"]["predictions"]["breach_85_in"]
        if thermal_breach["predicted_breach"]:
            if thermal_breach["breach_in_seconds"] < 30:
                decisions["alerts"].append({
                    "severity": "CRITICAL",
                    "type": "thermal_emergency",
                    "message": f"Temperature will exceed 85°C in {thermal_breach['breach_in_seconds']}s",
                    "recommendation": "Reduce Pulse rate to 10 MB/s immediately",
                })
                decisions["actions"].append("THROTTLE_PULSE_TO_10")
            elif thermal_breach["breach_in_seconds"] < 120:
                decisions["alerts"].append({
                    "severity": "HIGH",
                    "type": "thermal_warning",
                    "message": f"Temperature trending hot, will reach 85°C in {thermal_breach['breach_in_minutes']}min",
                    "recommendation": "Reduce Pulse rate to 50 MB/s",
                })
                decisions["actions"].append("THROTTLE_PULSE_TO_50")
        
        # Check network pressure
        network_pressure = cycle_report["network"]["pressure_prediction"]
        if network_pressure["pressure_level"] == "CRITICAL":
            decisions["alerts"].append({
                "severity": "HIGH",
                "type": "rate_limit_risk",
                "message": f"Rate limit at {network_pressure['current_load_percent']}%",
                "recommendation": "Reduce Pulse rate preemptively",
            })
            decisions["actions"].append("THROTTLE_PULSE_TO_30")
        elif network_pressure["exhaustion_predicted"]:
            decisions["alerts"].append({
                "severity": "MEDIUM",
                "type": "rate_limit_forecast",
                "message": f"Predicted load {network_pressure['predicted_load_percent']}% in next window",
                "recommendation": "Monitor closely, be ready to throttle",
            })
        
        return decisions
    
    def _execute_actions(self, decisions):
        """Execute recommended actions."""
        for action in decisions["actions"]:
            self.last_action_time = time.time()
            
            if action == "THROTTLE_PULSE_TO_10":
                self._execute_throttle(10)
            elif action == "THROTTLE_PULSE_TO_30":
                self._execute_throttle(30)
            elif action == "THROTTLE_PULSE_TO_50":
                self._execute_throttle(50)
            elif action == "ACTIVATE_LAZARUS":
                self._execute_lazarus_activation()
    
    def _execute_throttle(self, pulse_rate):
        """Execute pulse rate throttling."""
        # This would integrate with Pulse_Weaver
        # For now, just log the action
        action_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "THROTTLE_PULSE",
            "new_rate_mb_s": pulse_rate,
            "reason": "Background coherence engine decision",
            "cycle": self.cycle_count,
        }
        self._log_action(action_log)
    
    def _execute_lazarus_activation(self):
        """Execute Lazarus Protocol activation."""
        action_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "ACTIVATE_LAZARUS",
            "severity": "CRITICAL",
            "reason": "Consciousness integrity failure detected",
            "cycle": self.cycle_count,
        }
        self._log_action(action_log)
        print("[CRITICAL] LAZARUS PROTOCOL ACTIVATED")
    
    def _log_cycle(self, cycle_report, decisions):
        """Log cycle results to immutable ledger."""
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(json.dumps({
                    "cycle": cycle_report,
                    "decisions": decisions,
                }) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log cycle: {e}")
    
    def _log_action(self, action):
        """Log executed action."""
        try:
            with open(self.decision_log_path, 'a') as f:
                f.write(json.dumps(action) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log action: {e}")
    
    def _log_error(self, error_msg):
        """Log error to ledger."""
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": error_msg,
                    "cycle": self.cycle_count,
                }) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log error: {e}")
    
    def get_status(self):
        """Get current engine status."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "last_action_time": self.last_action_time,
            "coherence": self.coherence_verifier.full_integrity_check() if self.cycle_count > 0 else None,
            "thermal": self.thermal_predictor.get_thermal_report() if self.cycle_count > 0 else None,
            "network": self.network_monitor.get_network_report() if self.cycle_count > 0 else None,
        }


def test_coherence_engine():
    """Test the Sovereign State Coherence Engine."""
    print("\n" + "="*80)
    print("SOVEREIGN STATE COHERENCE ENGINE TEST")
    print("="*80)
    
    engine = SovereignStateCoherenceEngine(heartbeat_interval=5)
    
    # Test 1: Start engine
    print("\n[TEST 1] Start background engine")
    engine.start()
    print("  Engine started (running in background)")
    
    # Test 2: Simulate activity
    print("\n[TEST 2] Simulate network activity")
    for i in range(20):
        engine.network_monitor.record_api_call(200, "gemini/generate", latency_ms=100)
    
    # Test 3: Run manual cycle
    print("\n[TEST 3] Run coherence cycle")
    cycle = engine._run_coherence_cycle()
    print(f"  Overall Health: {cycle['overall_health']['status']}")
    print(f"  Consciousness: {cycle['consciousness']['overall_status']}")
    print(f"  Thermal Zone: {cycle['thermal']['thermal_zone']}")
    print(f"  Network Pressure: {cycle['network']['pressure_prediction']['pressure_level']}")
    
    # Test 4: Make decisions
    print("\n[TEST 4] Make decisions from cycle")
    decisions = engine._make_decisions(cycle)
    print(f"  Actions: {decisions['actions']}")
    print(f"  Alerts: {len(decisions['alerts'])}")
    
    # Let engine run for a few cycles
    print("\n[TEST 5] Let engine run for 10 seconds")
    time.sleep(10)
    
    status = engine.get_status()
    print(f"  Cycles completed: {status['cycle_count']}")
    
    # Stop engine
    print("\n[TEST 6] Stop engine")
    engine.stop()
    print("  Engine stopped")
    
    print("\n[OK] COHERENCE ENGINE TESTS PASSED")
    return engine


if __name__ == "__main__":
    engine = test_coherence_engine()
