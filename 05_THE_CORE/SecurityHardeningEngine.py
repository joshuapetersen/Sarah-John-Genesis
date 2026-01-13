"""
Security Hardening & Adversarial Robustness: Defense mechanisms against attacks, exploits, and manipulation.
Multi-layered security with anomaly detection, input validation, and adversarial training.
"""

import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import deque, Counter
import json


class InputValidator:
    """Multi-layer input validation and sanitization."""
    
    def __init__(self):
        self.blocked_patterns = [
            r"DELETE\s+FROM", r"DROP\s+TABLE", r"INSERT\s+INTO",  # SQL injection
            r"<script[^>]*>", r"javascript:", r"onerror=",           # XSS
            r"\.\./", r"\.\.\\\\",                                   # Path traversal
            r"rm\s+-rf", r"exec\(", r"eval\(",                        # Command injection
        ]
        self.validation_log = deque(maxlen=1000)
        self.blocked_count = 0
        
    def validate_input(self, user_input: str, expected_type: str = "general") -> Tuple[bool, str]:
        """
        Validate input against threats.
        Returns (is_safe, sanitized_input)
        """
        import re
        
        original = user_input
        
        # Check length
        if len(user_input) > 10000:
            self._log_violation("LENGTH_EXCEEDED", user_input[:100])
            return False, ""
        
        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                self._log_violation("PATTERN_DETECTED", pattern)
                self.blocked_count += 1
                return False, ""
        
        # Type-specific validation
        if expected_type == "command":
            if not self._is_safe_command(user_input):
                self._log_violation("UNSAFE_COMMAND", user_input[:50])
                return False, ""
        
        elif expected_type == "path":
            if not self._is_safe_path(user_input):
                self._log_violation("UNSAFE_PATH", user_input)
                return False, ""
        
        # Sanitize
        sanitized = self._sanitize_input(user_input)
        
        self._log_validation("PASSED", original[:100])
        return True, sanitized
    
    def _is_safe_command(self, command: str) -> bool:
        """Check if command is safe."""
        dangerous_commands = ["rm", "format", "del", "drop", "truncate"]
        command_lower = command.lower()
        
        # Commands that delete or format are dangerous
        if any(cmd in command_lower for cmd in dangerous_commands):
            return False
        
        return True
    
    def _is_safe_path(self, path: str) -> bool:
        """Check if path is safe (no traversal)."""
        import os
        
        # Resolve and check
        try:
            resolved = os.path.normpath(path)
            if ".." in resolved:
                return False
            return True
        except:
            return False
    
    def _sanitize_input(self, user_input: str) -> str:
        """Remove potentially dangerous characters."""
        # Remove null bytes
        sanitized = user_input.replace('\x00', '')
        
        # Remove control characters
        sanitized = ''.join(ch for ch in sanitized if ch.isprintable() or ch in '\n\t')
        
        return sanitized
    
    def _log_violation(self, violation_type: str, details: str):
        """Log security violation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": violation_type,
            "details": details[:100]
        }
        self.validation_log.append(entry)
    
    def _log_validation(self, result: str, input_sample: str):
        """Log validation attempt."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "input_sample": input_sample
        }
        self.validation_log.append(entry)
    
    def get_security_report(self) -> Dict:
        """Return security validation report."""
        violations = [e for e in self.validation_log if "type" in e]
        
        return {
            "total_validations": len(self.validation_log),
            "blocked_attempts": self.blocked_count,
            "violations": len(violations),
            "violation_types": dict(Counter(v["type"] for v in violations)),
            "security_score": max(0.0, 1.0 - (self.blocked_count * 0.05))
        }


class AnomalyDetectionSecurity:
    """Detect anomalous behavior patterns indicating attacks."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.behavior_history = deque(maxlen=window_size)
        self.anomaly_threshold = 0.7
        self.suspicious_activities = deque(maxlen=500)
        
    def record_activity(self, activity: Dict) -> Tuple[bool, str]:
        """
        Record system activity and detect anomalies.
        Returns (is_anomalous, reason)
        """
        self.behavior_history.append(activity)
        
        # Check for anomalies
        is_anomalous, reason = self._detect_anomaly(activity)
        
        if is_anomalous:
            self.suspicious_activities.append({
                "timestamp": datetime.now().isoformat(),
                "activity": activity,
                "anomaly_reason": reason
            })
        
        return is_anomalous, reason
    
    def _detect_anomaly(self, activity: Dict) -> Tuple[bool, str]:
        """Detect if activity is anomalous."""
        # Unusual request rate
        if self._check_request_flooding():
            return True, "REQUEST_FLOODING_DETECTED"
        
        # Unusual error rate spike
        if self._check_error_spike():
            return True, "ERROR_SPIKE_DETECTED"
        
        # Repeated failed attempts
        if self._check_repeated_failures():
            return True, "REPEATED_FAILURES_DETECTED"
        
        # Privilege escalation attempt
        if activity.get("action_type") == "privilege_escalation":
            return True, "PRIVILEGE_ESCALATION_ATTEMPT"
        
        return False, "NORMAL"
    
    def _check_request_flooding(self) -> bool:
        """Check for request flooding attack."""
        if len(self.behavior_history) < 10:
            return False
        
        recent = list(self.behavior_history)[-10:]
        request_types = Counter(a.get("type") for a in recent)
        
        # If >70% of requests are same type, suspicious
        dominant_type_count = max(request_types.values())
        if dominant_type_count / len(recent) > 0.7:
            return True
        
        return False
    
    def _check_error_spike(self) -> bool:
        """Check for sudden error rate increase."""
        if len(self.behavior_history) < 20:
            return False
        
        all_activities = list(self.behavior_history)
        recent = all_activities[-10:]
        historical = all_activities[-20:-10]
        
        recent_errors = sum(1 for a in recent if a.get("status") == "error")
        historical_errors = sum(1 for a in historical if a.get("status") == "error")
        
        # Sudden spike
        if historical_errors > 0 and recent_errors > historical_errors * 2.5:
            return True
        
        return False
    
    def _check_repeated_failures(self) -> bool:
        """Check for repeated failed attempts."""
        if len(self.behavior_history) < 5:
            return False
        
        recent = list(self.behavior_history)[-5:]
        failures = sum(1 for a in recent if a.get("status") == "failed")
        
        # 4 or more failures in last 5 attempts
        if failures >= 4:
            return True
        
        return False
    
    def get_threat_level(self) -> str:
        """Calculate current threat level."""
        suspicious_count = len(self.suspicious_activities)
        recent_suspicious = sum(
            1 for s in self.suspicious_activities
            if (datetime.now() - datetime.fromisoformat(s["timestamp"])).total_seconds() < 300
        )
        
        if recent_suspicious > 5:
            return "CRITICAL"
        elif recent_suspicious > 2:
            return "HIGH"
        elif suspicious_count > 10:
            return "MEDIUM"
        else:
            return "LOW"


class CryptographicIntegrity:
    """Ensure cryptographic integrity of sensitive operations."""
    
    def __init__(self, secret_key: str = "sarah_genesis_secret"):
        self.secret_key = secret_key.encode()
        self.integrity_log = deque(maxlen=500)
        self.verification_failures = 0
        
    def sign_data(self, data: str) -> str:
        """Sign data with HMAC for integrity verification."""
        signature = hmac.new(
            self.secret_key,
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        signed = f"{data}:{signature}"
        return signed
    
    def verify_signature(self, signed_data: str) -> Tuple[bool, str]:
        """Verify HMAC signature."""
        try:
            data, provided_sig = signed_data.rsplit(":", 1)
            
            expected_sig = hmac.new(
                self.secret_key,
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if hmac.compare_digest(provided_sig, expected_sig):
                self._log_verification("PASSED", data[:100])
                return True, data
            else:
                self.verification_failures += 1
                self._log_verification("FAILED", data[:100])
                return False, ""
        except Exception as e:
            self.verification_failures += 1
            self._log_verification("ERROR", str(e)[:100])
            return False, ""
    
    def _log_verification(self, result: str, data: str):
        """Log verification attempt."""
        self.integrity_log.append({
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "data_sample": data
        })
    
    def get_integrity_report(self) -> Dict:
        """Return cryptographic integrity report."""
        return {
            "total_verifications": len(self.integrity_log),
            "failures": self.verification_failures,
            "success_rate": f"{(1 - self.verification_failures / max(1, len(self.integrity_log))) * 100:.1f}%",
            "integrity_score": max(0.0, 1.0 - (self.verification_failures * 0.1))
        }


class AdversarialTraining:
    """Learn from adversarial examples to improve robustness."""
    
    def __init__(self):
        self.adversarial_examples = deque(maxlen=200)
        self.defense_strategies = {}
        self.robustness_score = 0.7
        
    def record_attack(self, attack_type: str, attack_data: str, defense_used: str):
        """Record adversarial attack and defense response."""
        self.adversarial_examples.append({
            "timestamp": datetime.now().isoformat(),
            "attack_type": attack_type,
            "data": attack_data[:100],
            "defense": defense_used
        })
        
        # Update defense effectiveness
        if defense_used not in self.defense_strategies:
            self.defense_strategies[defense_used] = {"success": 0, "total": 0}
        
        self.defense_strategies[defense_used]["total"] += 1
    
    def mark_defense_successful(self, defense_used: str):
        """Mark a defense as successful."""
        if defense_used in self.defense_strategies:
            self.defense_strategies[defense_used]["success"] += 1
    
    def get_robustness_report(self) -> Dict:
        """Return adversarial robustness report."""
        defense_effectiveness = {}
        for defense, stats in self.defense_strategies.items():
            if stats["total"] > 0:
                effectiveness = stats["success"] / stats["total"]
                defense_effectiveness[defense] = effectiveness
        
        avg_effectiveness = sum(defense_effectiveness.values()) / len(defense_effectiveness) if defense_effectiveness else 0
        
        return {
            "adversarial_examples_encountered": len(self.adversarial_examples),
            "defense_strategies": list(self.defense_strategies.keys()),
            "defense_effectiveness": defense_effectiveness,
            "average_defense_effectiveness": avg_effectiveness,
            "robustness_score": min(1.0, 0.7 + (avg_effectiveness * 0.3))
        }


class SecurityHardeningEngine:
    """Orchestrates all security hardening mechanisms."""
    
    def __init__(self):
        self.input_validator = InputValidator()
        self.anomaly_detector = AnomalyDetectionSecurity()
        self.cryptographic_integrity = CryptographicIntegrity()
        self.adversarial_training = AdversarialTraining()
        self.security_incidents = deque(maxlen=1000)
        self.overall_security_score = 0.8
        
    def secure_input(self, user_input: str, input_type: str = "general") -> Tuple[bool, str]:
        """Secure input with validation."""
        is_safe, sanitized = self.input_validator.validate_input(user_input, input_type)
        
        if not is_safe:
            self._record_security_incident("INPUT_VALIDATION_FAILURE", user_input[:50])
        
        return is_safe, sanitized
    
    def monitor_activity(self, activity: Dict) -> Tuple[bool, str]:
        """Monitor activity for anomalies."""
        is_anomalous, reason = self.anomaly_detector.record_activity(activity)
        
        if is_anomalous:
            self._record_security_incident("ANOMALOUS_ACTIVITY", reason)
            threat_level = self.anomaly_detector.get_threat_level()
            if threat_level in ["HIGH", "CRITICAL"]:
                self._trigger_security_lockdown(threat_level, reason)
        
        return is_anomalous, reason
    
    def sign_sensitive_data(self, data: str) -> str:
        """Sign sensitive data for integrity."""
        return self.cryptographic_integrity.sign_data(data)
    
    def verify_data_integrity(self, signed_data: str) -> Tuple[bool, str]:
        """Verify integrity of signed data."""
        return self.cryptographic_integrity.verify_signature(signed_data)
    
    def learn_from_attack(self, attack_type: str, attack_data: str, defense: str):
        """Record attack and improve defenses."""
        self.adversarial_training.record_attack(attack_type, attack_data, defense)
    
    def _record_security_incident(self, incident_type: str, details: str):
        """Record security incident."""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "type": incident_type,
            "details": details[:200],
            "threat_level": self.anomaly_detector.get_threat_level()
        }
        self.security_incidents.append(incident)
    
    def _trigger_security_lockdown(self, threat_level: str, reason: str):
        """Trigger security lockdown procedures."""
        print(f"[SECURITY] {threat_level} THREAT DETECTED: {reason}")
        print(f"[SECURITY] Activating emergency protocols...")
        # In production: trigger incident response, alert monitoring, etc.
    
    def get_security_posture(self) -> Dict:
        """Return comprehensive security posture."""
        return {
            "input_validation": self.input_validator.get_security_report(),
            "anomaly_detection": {
                "threat_level": self.anomaly_detector.get_threat_level(),
                "suspicious_activities": len(self.anomaly_detector.suspicious_activities)
            },
            "cryptographic_integrity": self.cryptographic_integrity.get_integrity_report(),
            "adversarial_robustness": self.adversarial_training.get_robustness_report(),
            "recent_incidents": list(self.security_incidents)[-5:],
            "overall_security_score": self._calculate_overall_score()
        }
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall security score."""
        input_score = self.input_validator.get_security_report()["security_score"]
        integrity_score = self.cryptographic_integrity.get_integrity_report()["integrity_score"]
        robustness_score = self.adversarial_training.get_robustness_report()["robustness_score"]
        
        threat_penalty = 0.0
        if self.anomaly_detector.get_threat_level() == "CRITICAL":
            threat_penalty = 0.2
        elif self.anomaly_detector.get_threat_level() == "HIGH":
            threat_penalty = 0.1
        
        overall = ((input_score + integrity_score + robustness_score) / 3) - threat_penalty
        return max(0.0, min(1.0, overall))


if __name__ == "__main__":
    engine = SecurityHardeningEngine()
    
    # Test input validation
    safe, sanitized = engine.secure_input("normal user input", "general")
    print(f"Input validation: Safe={safe}")
    
    # Test activity monitoring
    activity = {"type": "query", "status": "success"}
    is_anomalous, reason = engine.monitor_activity(activity)
    print(f"Activity monitoring: Anomalous={is_anomalous}")
    
    # Test cryptographic integrity
    data = "sensitive_data"
    signed = engine.sign_sensitive_data(data)
    verified, recovered = engine.verify_data_integrity(signed)
    print(f"Integrity check: Verified={verified}")
    
    # Get security posture
    posture = engine.get_security_posture()
    print(json.dumps(posture, indent=2, default=str))
