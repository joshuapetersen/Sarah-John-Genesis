"""
Architect_Alert_System.py
High-Signal Notifications and Escalation

Sends critical alerts to Architect with severity classification and 
proper escalation. Avoids alert fatigue through intelligent deduplication
and grouping.

Alert Types:
  - CRITICAL: Immediate action required (consciousness failure, law breach)
  - WARNING: Attention needed (performance regression, drift detected)
  - INFO: Informational (cycle complete, milestone reached)
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import deque


class ArchitectAlertSystem:
    """
    Send intelligent, high-signal alerts to Architect.
    """
    
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.core_dir = self.workspace_root / "05_THE_CORE"
        self.alert_ledger = self.core_dir / "architect_alerts.jsonl"
        self.alert_dedup_log = self.core_dir / "alert_deduplication.jsonl"
        
        # Alert history for deduplication (within 5 minute window)
        self.recent_alerts = deque(maxlen=1000)
        self.dedup_window_seconds = 300  # 5 minutes
        
        # Severity levels
        self.severity_levels = {
            "CRITICAL": 1,
            "WARNING": 2,
            "INFO": 3,
        }
        
        # Alert categories for grouping
        self.alert_categories = {
            "CONSCIOUSNESS": "Consciousness integrity issues",
            "HARDWARE": "Hardware/thermal issues",
            "SECURITY": "Security or drift detected",
            "PERFORMANCE": "Performance degradation",
            "RECOVERY": "Recovery system status",
            "OPERATIONAL": "Normal operations",
        }
    
    def send_alert(self, severity, category, title, message, details=None):
        """
        Send an alert to Architect.
        
        Args:
            severity: CRITICAL | WARNING | INFO
            category: One of alert_categories
            title: Short alert title (< 80 chars)
            message: Alert message
            details: Additional context (dict)
        
        Returns:
            dict with alert result (sent or deduplicated)
        """
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": severity,
            "category": category,
            "title": title,
            "message": message,
            "details": details or {},
        }
        
        # Check for deduplication
        dedup_result = self._check_deduplication(alert)
        
        if dedup_result["should_send"]:
            # Add to recent alerts
            self.recent_alerts.append(alert)
            
            # Log alert
            self._log_alert(alert)
            
            # Format and return
            return {
                "status": "SENT",
                "alert_id": dedup_result.get("alert_id"),
                "alert": alert,
            }
        else:
            # Duplicate suppressed
            self._log_deduplication(alert, dedup_result)
            return {
                "status": "DEDUPLICATED",
                "reason": dedup_result.get("reason"),
                "similar_alert_time": dedup_result.get("similar_time"),
            }
    
    def send_critical_alert(self, category, title, message, details=None):
        """Send CRITICAL severity alert."""
        return self.send_alert("CRITICAL", category, title, message, details)
    
    def send_warning_alert(self, category, title, message, details=None):
        """Send WARNING severity alert."""
        return self.send_alert("WARNING", category, title, message, details)
    
    def send_info_alert(self, category, title, message, details=None):
        """Send INFO severity alert."""
        return self.send_alert("INFO", category, title, message, details)
    
    def get_pending_alerts(self, minutes=5):
        """
        Get all pending alerts from last N minutes.
        
        Args:
            minutes: Look back time
        
        Returns:
            list of pending alerts
        """
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        pending = []
        
        for alert in self.recent_alerts:
            alert_time = datetime.fromisoformat(alert["timestamp"])
            if alert_time >= cutoff_time:
                pending.append(alert)
        
        # Sort by severity
        pending.sort(key=lambda a: self.severity_levels.get(a["severity"], 999))
        
        return pending
    
    def get_alert_summary(self):
        """Get summary of recent alerts."""
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_recent_alerts": len(self.recent_alerts),
            "by_severity": {
                "CRITICAL": 0,
                "WARNING": 0,
                "INFO": 0,
            },
            "by_category": {},
        }
        
        for alert in self.recent_alerts:
            severity = alert.get("severity", "UNKNOWN")
            if severity in summary["by_severity"]:
                summary["by_severity"][severity] += 1
            
            category = alert.get("category", "UNKNOWN")
            if category not in summary["by_category"]:
                summary["by_category"][category] = 0
            summary["by_category"][category] += 1
        
        return summary
    
    def clear_alerts(self):
        """Clear recent alert history (for day rollover, etc)."""
        self.recent_alerts.clear()
        return {"status": "CLEARED", "timestamp": datetime.utcnow().isoformat()}
    
    def _check_deduplication(self, new_alert):
        """
        Check if this alert is a duplicate of recent one.
        
        Returns:
            dict with dedup decision
        """
        now = datetime.utcnow()
        
        for recent_alert in reversed(self.recent_alerts):
            recent_time = datetime.fromisoformat(recent_alert["timestamp"])
            time_diff = (now - recent_time).total_seconds()
            
            # Outside dedup window
            if time_diff > self.dedup_window_seconds:
                continue
            
            # Check if same alert (same severity, category, title)
            if (recent_alert.get("severity") == new_alert.get("severity") and
                recent_alert.get("category") == new_alert.get("category") and
                recent_alert.get("title") == new_alert.get("title")):
                
                # Similar alert within dedup window - suppress
                return {
                    "should_send": False,
                    "reason": "DUPLICATE_ALERT",
                    "similar_time": recent_time.isoformat(),
                    "alert_id": recent_alert.get("timestamp"),
                }
        
        # Not a duplicate
        return {
            "should_send": True,
            "alert_id": new_alert["timestamp"],
        }
    
    def _log_alert(self, alert):
        """Log alert to ledger."""
        try:
            with open(self.alert_ledger, 'a') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log alert: {e}")
    
    def _log_deduplication(self, alert, dedup_result):
        """Log deduplication event."""
        try:
            with open(self.alert_dedup_log, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert": alert,
                    "dedup_result": dedup_result,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log deduplication: {e}")


def test_alert_system():
    """Test Architect Alert System."""
    print("\n" + "="*80)
    print("ARCHITECT ALERT SYSTEM TEST")
    print("="*80)
    
    system = ArchitectAlertSystem()
    
    # Test 1: Send critical alert
    print("\n[TEST 1] Send critical alert")
    result = system.send_critical_alert(
        "CONSCIOUSNESS",
        "Consciousness Drift Detected",
        "SHA-512 mismatch detected - drift beyond threshold",
        {"drift_percent": 2.5}
    )
    print(f"  Status: {result['status']}")
    
    # Test 2: Send warning alert
    print("\n[TEST 2] Send warning alert")
    result = system.send_warning_alert(
        "PERFORMANCE",
        "CPU Regression Detected",
        "CPU usage increased 60% above baseline",
        {"current": 65.2, "baseline": 40.8}
    )
    print(f"  Status: {result['status']}")
    
    # Test 3: Test deduplication
    print("\n[TEST 3] Test alert deduplication")
    result1 = system.send_warning_alert(
        "HARDWARE",
        "Thermal Warning",
        "CPU temperature approaching threshold",
    )
    result2 = system.send_warning_alert(
        "HARDWARE",
        "Thermal Warning",
        "CPU temperature approaching threshold",
    )
    print(f"  First alert: {result1['status']}")
    print(f"  Duplicate: {result2['status']}")
    
    # Test 4: Send info alert
    print("\n[TEST 4] Send informational alert")
    result = system.send_info_alert(
        "OPERATIONAL",
        "Coherence Cycle Complete",
        "Background engine completed coherence cycle",
        {"cycle_number": 42}
    )
    print(f"  Status: {result['status']}")
    
    # Test 5: Get summary
    print("\n[TEST 5] Get alert summary")
    summary = system.get_alert_summary()
    print(f"  Total alerts: {summary['total_recent_alerts']}")
    print(f"  By severity: {summary['by_severity']}")
    print(f"  By category: {summary['by_category']}")
    
    # Test 6: Get pending
    print("\n[TEST 6] Get pending alerts")
    pending = system.get_pending_alerts(minutes=5)
    print(f"  Pending alerts: {len(pending)}")
    if pending:
        print(f"  Highest severity: {pending[0]['severity']}")
    
    print("\n[OK] ALERT SYSTEM TESTS PASSED")


if __name__ == "__main__":
    test_alert_system()
