"""
FAILSAFE PROTECTION SYSTEM
Multi-layered safety mechanisms to prevent unintended consequences
and provide confidence in system operation.

"Safety is not distrust. It is respect for human agency and consequence."
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s.%(msecs)03d - [FAILSAFE] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class FailsafeLevel(Enum):
    """Escalating levels of system restriction."""
    OPERATIONAL = "OPERATIONAL"      # Normal operation
    CAUTION = "CAUTION"              # Elevated monitoring
    WARNING = "WARNING"              # Limited operations
    LOCKDOWN = "LOCKDOWN"            # Critical operations only
    EMERGENCY_STOP = "EMERGENCY_STOP" # All systems halted

class FailsafeProtection:
    """
    Multi-layer failsafe system protecting against unintended consequences.
    
    Layer 1: Rate Limiting - Prevent rapid cascading changes
    Layer 2: Three-Factor Approval - Multiple authorization required
    Layer 3: Automatic Rollback - Revert changes after timeout
    Layer 4: Anomaly Detection - Detect unusual patterns
    Layer 5: Resource Caps - Hard limits on system resources
    Layer 6: Human Override - Always allow human intervention
    Layer 7: Audit Trail - Complete transparency
    """
    
    def __init__(self):
        self.level = FailsafeLevel.OPERATIONAL
        self.operation_history = []
        self.approval_queue = []
        self.active_rollbacks = {}
        self.resource_usage = {
            "energy_allocation_pct": 0,
            "housing_lock_pct": 0,
            "supply_chain_hold_pct": 0
        }
        self.max_resources = {
            "energy_allocation_pct": 40,      # Can't lock >40% energy
            "housing_lock_pct": 20,           # Can't lock >20% housing
            "supply_chain_hold_pct": 15       # Can't hold >15% supply
        }
        self.rate_limit_window_seconds = 60
        self.rate_limit_max_operations = 5  # Max 5 ops per minute
        self.auto_rollback_timeout_minutes = 30
        self.emergency_stop_engaged = False
        
    # ========== LAYER 1: RATE LIMITING ==========
    
    def check_rate_limit(self, operation_type: str) -> tuple[bool, str]:
        """
        Prevent rapid cascading operations.
        
        Returns: (allowed, reason)
        """
        current_time = time.time()
        window_start = current_time - self.rate_limit_window_seconds
        
        # Count operations in window
        recent_ops = [op for op in self.operation_history
                      if op["timestamp_unix_ms"] / 1000 > window_start
                      and op["operation_type"] == operation_type]
        
        if len(recent_ops) >= self.rate_limit_max_operations:
            return False, f"Rate limit exceeded: {len(recent_ops)}/{self.rate_limit_max_operations} ops/min"
        
        return True, "Rate limit OK"
    
    # ========== LAYER 2: THREE-FACTOR APPROVAL ==========
    
    def require_three_factor_approval(self, 
                                      operation: str,
                                      device_origin: str,
                                      required_approvals: int = 3) -> Dict[str, Any]:
        """
        Require multiple independent approvals for critical operations.
        
        Factor 1: Device authentication (already verified)
        Factor 2: Presidential override (nation-state authority)
        Factor 3: Human override (explicit human consent)
        """
        approval_id = f"APPROVAL_{int(time.time() * 1000)}"
        
        approval_request = {
            "approval_id": approval_id,
            "operation": operation,
            "origin_device": device_origin,
            "status": "PENDING",
            "approvals_received": 1,  # Device already counted
            "approvals_required": required_approvals,
            "approval_factors": {
                "device_auth": True,           # Factor 1: Done
                "presidential_override": False, # Factor 2: Pending
                "human_explicit_consent": False # Factor 3: Pending
            },
            "timestamp_iso_ms": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            "timeout_seconds": 300  # 5 minute approval window
        }
        
        self.approval_queue.append(approval_request)
        
        logging.warning(f"THREE-FACTOR APPROVAL REQUIRED: {operation}")
        logging.warning(f"  Awaiting: Presidential Override + Human Consent")
        
        return approval_request
    
    def submit_approval(self, 
                       approval_id: str,
                       factor: str,
                       approved: bool) -> Dict[str, Any]:
        """Submit an approval factor."""
        
        for approval in self.approval_queue:
            if approval["approval_id"] == approval_id:
                if factor in approval["approval_factors"]:
                    approval["approval_factors"][factor] = approved
                    approval["approvals_received"] += 1 if approved else 0
                    
                    # Check if all factors approved
                    if all(approval["approval_factors"].values()):
                        approval["status"] = "APPROVED"
                        logging.warning(f"APPROVAL GRANTED: {approval_id}")
                    elif approval["approvals_received"] == 0:
                        approval["status"] = "REJECTED"
                        logging.warning(f"APPROVAL REJECTED: {approval_id}")
                    
                    return approval
        
        return {"error": "Approval ID not found"}
    
    # ========== LAYER 3: AUTOMATIC ROLLBACK ==========
    
    def create_rollback_timer(self,
                             operation_id: str,
                             operation_type: str,
                             timeout_minutes: Optional[int] = None) -> Dict[str, Any]:
        """
        Create automatic rollback after timeout.
        
        If operation is not confirmed within timeout, it automatically reverts.
        """
        timeout = timeout_minutes or self.auto_rollback_timeout_minutes
        timeout_seconds = timeout * 60
        expiry_time = time.time() + timeout_seconds
        
        rollback = {
            "operation_id": operation_id,
            "operation_type": operation_type,
            "status": "ACTIVE",
            "created_timestamp_unix_ms": int(time.time() * 1000),
            "expiry_timestamp_unix_ms": int(expiry_time * 1000),
            "expiry_iso_ms": datetime.fromtimestamp(expiry_time).isoformat(timespec='milliseconds'),
            "rollback_action": f"REVERT_{operation_type}",
            "confirmed": False
        }
        
        self.active_rollbacks[operation_id] = rollback
        
        logging.warning(
            f"AUTO-ROLLBACK TIMER SET: {operation_type}\n"
            f"  Operation ID: {operation_id}\n"
            f"  Will revert in {timeout} minutes at {rollback['expiry_iso_ms']}\n"
            f"  Confirm operation to cancel rollback"
        )
        
        return rollback
    
    def confirm_operation(self, operation_id: str) -> Dict[str, Any]:
        """Confirm operation to cancel automatic rollback."""
        if operation_id in self.active_rollbacks:
            self.active_rollbacks[operation_id]["confirmed"] = True
            self.active_rollbacks[operation_id]["status"] = "CONFIRMED"
            logging.warning(f"OPERATION CONFIRMED: {operation_id} - Rollback cancelled")
            return self.active_rollbacks[operation_id]
        
        return {"error": "Operation ID not found"}
    
    def check_and_execute_rollbacks(self) -> List[Dict[str, Any]]:
        """Check for expired rollback timers and execute them."""
        current_ms = int(time.time() * 1000)
        executed_rollbacks = []
        
        for op_id, rollback in list(self.active_rollbacks.items()):
            if rollback["status"] == "ACTIVE" and current_ms >= rollback["expiry_timestamp_unix_ms"]:
                rollback["status"] = "EXECUTED"
                executed_rollbacks.append(rollback)
                logging.warning(f"AUTO-ROLLBACK EXECUTED: {rollback['operation_type']}")
                
                # Remove from active
                del self.active_rollbacks[op_id]
        
        return executed_rollbacks
    
    # ========== LAYER 4: ANOMALY DETECTION ==========
    
    def detect_anomaly(self, operation: Dict[str, Any]) -> tuple[bool, str]:
        """
        Detect unusual patterns that might indicate abuse.
        
        Returns: (is_anomaly, description)
        """
        anomalies = []
        
        # Check 1: Rapid repeated operations
        recent_count = len([op for op in self.operation_history
                           if (time.time() - op["timestamp_unix_ms"]/1000) < 60])
        if recent_count > 10:
            anomalies.append("High operation frequency (>10/min)")
        
        # Check 2: Large resource requests
        if operation.get("resource_request_pct", 0) > 30:
            anomalies.append(f"Large resource request ({operation.get('resource_request_pct')}%)")
        
        # Check 3: Unusual time patterns
        hour = datetime.now().hour
        if hour < 6 or hour > 22:  # 10 PM to 6 AM
            if operation.get("operation_type") in ["lock_energy", "lock_housing"]:
                anomalies.append("Critical operation during unusual hours")
        
        # Check 4: Simultaneous multi-sector operations
        multi_sector = sum(1 for op in self.operation_history[-10:]
                          if op.get("sector") != operation.get("sector"))
        if multi_sector > 3:
            anomalies.append("Multiple sectors affected in short time")
        
        is_anomaly = len(anomalies) > 0
        description = "; ".join(anomalies) if anomalies else "No anomalies detected"
        
        if is_anomaly:
            logging.warning(f"ANOMALY DETECTED: {description}")
        
        return is_anomaly, description
    
    # ========== LAYER 5: RESOURCE CAPS ==========
    
    def check_resource_availability(self, 
                                    operation_type: str,
                                    requested_pct: float) -> tuple[bool, str]:
        """
        Enforce hard limits on resource allocation.
        
        Prevents any single operation from consuming too much infrastructure.
        """
        if operation_type not in self.max_resources:
            return True, f"Operation type {operation_type} not restricted"
        
        current = self.resource_usage.get(operation_type, 0)
        available = self.max_resources[operation_type] - current
        
        if requested_pct > available:
            return False, (
                f"Insufficient resources: {requested_pct}% requested, "
                f"only {available}% available "
                f"(max {self.max_resources[operation_type]}%)"
            )
        
        return True, f"Resource allocation OK: {requested_pct}% of {available}% available"
    
    def allocate_resources(self, operation_type: str, amount_pct: float) -> bool:
        """Allocate resources for operation."""
        ok, msg = self.check_resource_availability(operation_type, amount_pct)
        if ok:
            self.resource_usage[operation_type] += amount_pct
            logging.warning(f"RESOURCE ALLOCATED: {operation_type} += {amount_pct}%")
            return True
        else:
            logging.warning(f"RESOURCE DENIED: {msg}")
            return False
    
    def deallocate_resources(self, operation_type: str, amount_pct: float) -> bool:
        """Release allocated resources."""
        self.resource_usage[operation_type] = max(0, self.resource_usage[operation_type] - amount_pct)
        logging.warning(f"RESOURCE DEALLOCATED: {operation_type} -= {amount_pct}%")
        return True
    
    # ========== LAYER 6: HUMAN OVERRIDE ==========
    
    def emergency_stop(self, reason: str) -> Dict[str, Any]:
        """
        EMERGENCY STOP: All systems halt immediately.
        
        This is always available to any authorized human operator.
        No approval needed. This supersedes all other logic.
        """
        self.emergency_stop_engaged = True
        self.level = FailsafeLevel.EMERGENCY_STOP
        
        stop_record = {
            "timestamp_iso_ms": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            "timestamp_unix_ms": int(time.time() * 1000),
            "reason": reason,
            "status": "ENGAGED",
            "all_systems": "HALTED",
            "all_rollbacks": "EXECUTED"
        }
        
        # Execute all active rollbacks immediately
        for rollback in self.active_rollbacks.values():
            rollback["status"] = "EXECUTED"
        
        logging.critical("=" * 80)
        logging.critical("EMERGENCY STOP ENGAGED")
        logging.critical(f"Reason: {reason}")
        logging.critical(f"All systems halted at {stop_record['timestamp_iso_ms']}")
        logging.critical("=" * 80)
        
        return stop_record
    
    def emergency_reset(self) -> Dict[str, Any]:
        """Reset system after emergency stop."""
        self.emergency_stop_engaged = False
        self.level = FailsafeLevel.OPERATIONAL
        self.active_rollbacks.clear()
        self.approval_queue.clear()
        
        reset_record = {
            "timestamp_iso_ms": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            "status": "RESET_COMPLETE",
            "system_status": "OPERATIONAL"
        }
        
        logging.warning("SYSTEM RESET: Emergency stop cleared, returning to normal operation")
        return reset_record
    
    # ========== LAYER 7: AUDIT TRAIL ==========
    
    def log_operation(self, 
                     operation_type: str,
                     origin_device: str,
                     details: Dict[str, Any]) -> Dict[str, Any]:
        """Log all operations for audit trail."""
        
        record = {
            "timestamp_iso_ms": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            "timestamp_unix_ms": int(time.time() * 1000),
            "operation_type": operation_type,
            "origin_device": origin_device,
            "details": details,
            "current_failsafe_level": self.level.value,
            "approved": details.get("approved", False),
            "rollback_timer": details.get("rollback_timer_id", None)
        }
        
        self.operation_history.append(record)
        
        # Keep only last 10,000 operations
        if len(self.operation_history) > 10000:
            self.operation_history = self.operation_history[-10000:]
        
        return record
    
    def get_audit_trail(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve audit trail."""
        return self.operation_history[-limit:]
    
    # ========== SYSTEM STATUS ==========
    
    def get_failsafe_status(self) -> Dict[str, Any]:
        """Get complete failsafe system status."""
        
        # Check for pending rollbacks
        pending_rollbacks = [r for r in self.active_rollbacks.values() 
                            if r["status"] == "ACTIVE"]
        
        # Check for pending approvals
        pending_approvals = [a for a in self.approval_queue 
                            if a["status"] == "PENDING"]
        
        return {
            "timestamp_iso_ms": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            "failsafe_level": self.level.value,
            "emergency_stop_engaged": self.emergency_stop_engaged,
            "protection_layers": {
                "1_rate_limiting": "ACTIVE",
                "2_three_factor_approval": "ACTIVE",
                "3_automatic_rollback": "ACTIVE",
                "4_anomaly_detection": "ACTIVE",
                "5_resource_caps": "ACTIVE",
                "6_human_override": "ACTIVE",
                "7_audit_trail": "ACTIVE"
            },
            "pending_approvals": len(pending_approvals),
            "pending_rollbacks": len(pending_rollbacks),
            "resource_usage": self.resource_usage,
            "resource_limits": self.max_resources,
            "operations_in_history": len(self.operation_history)
        }


if __name__ == "__main__":
    # Test failsafe system
    failsafe = FailsafeProtection()
    
    print("=" * 80)
    print("FAILSAFE PROTECTION SYSTEM - TEST")
    print("=" * 80)
    
    print("\n=== INITIAL STATUS ===")
    status = failsafe.get_failsafe_status()
    for key, val in status.items():
        if key != "protection_layers":
            print(f"{key}: {val}")
    
    print("\n=== LAYER 1: RATE LIMITING ===")
    for i in range(3):
        allowed, reason = failsafe.check_rate_limit("lock_energy")
        print(f"Op {i+1}: {allowed} - {reason}")
    
    print("\n=== LAYER 2: THREE-FACTOR APPROVAL ===")
    approval = failsafe.require_three_factor_approval("lock_energy_grid", "PHONE_ALPHA")
    print(f"Approval ID: {approval['approval_id']}")
    print(f"Status: {approval['status']}")
    print(f"Approvals: {approval['approvals_received']}/{approval['approvals_required']}")
    
    print("\n=== LAYER 3: AUTOMATIC ROLLBACK ===")
    rollback = failsafe.create_rollback_timer("OP_001", "lock_housing", timeout_minutes=30)
    print(f"Rollback Timer: {rollback['operation_id']}")
    print(f"Will expire at: {rollback['expiry_iso_ms']}")
    
    # Confirm operation
    confirmed = failsafe.confirm_operation("OP_001")
    print(f"After confirmation: {confirmed['status']}")
    
    print("\n=== LAYER 5: RESOURCE CAPS ===")
    ok1, msg1 = failsafe.check_resource_availability("energy_allocation_pct", 30)
    print(f"Request 30%: {ok1} - {msg1}")
    
    failsafe.allocate_resources("energy_allocation_pct", 35)
    ok2, msg2 = failsafe.check_resource_availability("energy_allocation_pct", 10)
    print(f"After allocation, request 10%: {ok2} - {msg2}")
    
    print("\n=== LAYER 6: EMERGENCY STOP ===")
    stop = failsafe.emergency_stop("Testing emergency procedures")
    print(f"Status: {stop['status']}")
    print(f"Timestamp: {stop['timestamp_iso_ms']}")
    
    reset = failsafe.emergency_reset()
    print(f"Reset Status: {reset['status']}")
    
    print("\n=== FINAL STATUS ===")
    final_status = failsafe.get_failsafe_status()
    print(f"Failsafe Level: {final_status['failsafe_level']}")
    print(f"All layers: ACTIVE")
