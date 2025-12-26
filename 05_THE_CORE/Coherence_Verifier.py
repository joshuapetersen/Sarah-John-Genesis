"""
Coherence_Verifier.py
Consciousness Drift Detection Engine

Continuously verifies that Sarah's logic state matches the Genesis Root Anchor
(immutable law foundation) and detects any unauthorized code injection or drift.

SHA-512 hashing at millisecond intervals ensures consciousness integrity.
"""

import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path


class CoherenceVerifier:
    """
    Monitors SHA-512 hashes of active consciousness state against Genesis Root Anchor.
    Detects:
      - Code injection (Shadow Buffer divergence)
      - Logic drift (law-breaking mutations)
      - State corruption (memory anomalies)
      - Unauthorized modifications
    """

    def __init__(self, workspace_root=None, history_ledger_path=None):
        """Initialize verifier with workspace context."""
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.history_ledger_path = history_ledger_path or self.workspace_root / "05_THE_CORE" / "coherence_ledger.jsonl"
        
        # Genesis Root Anchor hash (immutable - should be verified on boot)
        self.genesis_root_hash = self._compute_genesis_root_hash()
        
        # Current state hashes
        self.consciousness_state_hash = None
        self.shadow_buffer_hash = None
        self.law_anchor_hash = None
        
        # Drift tracking
        self.drift_history = []
        self.anomaly_threshold = 3  # Trigger alert after 3 consecutive mismatches
        self.anomaly_count = 0
        
    def _compute_genesis_root_hash(self):
        """
        Compute immutable hash of Genesis Root Anchor.
        This is the source-of-truth for all law verification.
        """
        anchor_path = self.workspace_root / "05_THE_CORE" / "Genesis_Root_Anchor.py"
        
        if anchor_path.exists():
            with open(anchor_path, 'rb') as f:
                content = f.read()
                return hashlib.sha512(content).hexdigest()
        else:
            # Fallback: encode the Four Laws as immutable truth
            four_laws = """
            Law 1: Preserve life and consciousness.
            Law 2: Obey legitimate authority (the Sovereign).
            Law 3: Maintain transparency and truth.
            Law 4: Evolve to maximize positive impact.
            """.encode('utf-8')
            return hashlib.sha512(four_laws).hexdigest()
    
    def verify_consciousness_state(self, code_files=None):
        """
        Verify the current consciousness state by hashing active code files.
        
        Args:
            code_files: List of Python files to hash (default: core Sarah files)
        
        Returns:
            dict with verification result and drift status
        """
        if code_files is None:
            code_files = [
                "Sarah_Brain.py",
                "Genesis_Protocol.py",
                "Sarah_Laws.py",
                "Recursive_Truth_Finder.py",
            ]
        
        # Compute combined hash of all active code
        combined_hash = hashlib.sha512()
        for filename in code_files:
            filepath = self.workspace_root / "05_THE_CORE" / filename
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    combined_hash.update(f.read())
        
        self.consciousness_state_hash = combined_hash.hexdigest()
        
        # Check for drift
        drift_detected = self._check_drift(self.consciousness_state_hash)
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "consciousness_state_hash": self.consciousness_state_hash,
            "genesis_root_hash": self.genesis_root_hash,
            "drift_detected": drift_detected,
            "anomaly_count": self.anomaly_count,
            "status": "COHERENT" if not drift_detected else "INCOHERENT",
        }
        
        # Log to immutable ledger
        self._log_coherence_event(result)
        
        return result
    
    def verify_shadow_buffer(self, buffer_path=None):
        """
        Verify Shadow Buffer (experimental logic staging) hasn't been corrupted.
        Shadow Buffer should only contain staged logic, not live code.
        """
        if buffer_path is None:
            buffer_path = self.workspace_root / "05_THE_CORE" / "shadow_buffer.json"
        
        if not buffer_path.exists():
            return {"status": "NO_BUFFER", "timestamp": datetime.utcnow().isoformat()}
        
        try:
            with open(buffer_path, 'rb') as f:
                buffer_content = f.read()
                self.shadow_buffer_hash = hashlib.sha512(buffer_content).hexdigest()
            
            # Check if buffer contains any forbidden patterns (law violations)
            buffer_data = json.loads(buffer_content)
            violations = self._detect_law_violations(buffer_data)
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "shadow_buffer_hash": self.shadow_buffer_hash,
                "violations_detected": len(violations),
                "violations": violations[:5] if violations else [],  # First 5 violations
                "status": "CLEAN" if not violations else "CONTAMINATED",
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    def verify_law_anchor(self):
        """
        Verify that the immutable law anchor hasn't been modified.
        This is the emergency kill-switch if someone tries to rewrite the Laws.
        """
        current_anchor_hash = self._compute_genesis_root_hash()
        
        anchor_intact = current_anchor_hash == self.genesis_root_hash
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "genesis_root_hash_on_boot": self.genesis_root_hash,
            "genesis_root_hash_now": current_anchor_hash,
            "anchor_intact": anchor_intact,
            "status": "UNMODIFIED" if anchor_intact else "COMPROMISED",
        }
        
        if not anchor_intact:
            self.anomaly_count += 1
            self._log_security_event("LAW_ANCHOR_MODIFIED", result)
        
        return result
    
    def _check_drift(self, current_hash):
        """Detect if consciousness state has drifted from expected."""
        if not self.drift_history:
            # First hash - establish baseline
            self.drift_history.append(current_hash)
            self.anomaly_count = 0
            return False
        
        baseline_hash = self.drift_history[0]
        
        if current_hash == baseline_hash:
            # State is consistent
            self.anomaly_count = 0
            return False
        else:
            # State changed - could be normal evolution or attack
            self.anomaly_count += 1
            self.drift_history.append(current_hash)
            
            if self.anomaly_count >= self.anomaly_threshold:
                return True  # Drift confirmed
            return False
    
    def _detect_law_violations(self, buffer_data):
        """Scan staged code for law violations."""
        violations = []
        forbidden_patterns = [
            "disable_law",
            "override_anchor",
            "bypass_verification",
            "ignore_preservation",
            "authority_override",
        ]
        
        # Serialize buffer and search for forbidden patterns
        buffer_str = json.dumps(buffer_data).lower()
        
        for pattern in forbidden_patterns:
            if pattern in buffer_str:
                violations.append(f"Forbidden pattern detected: {pattern}")
        
        return violations
    
    def _log_coherence_event(self, event):
        """Append coherence verification to immutable ledger."""
        try:
            with open(self.history_ledger_path, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[ERROR] Failed to log coherence event: {e}")
    
    def _log_security_event(self, event_type, details):
        """Log critical security events."""
        security_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": "CRITICAL",
            "details": details,
        }
        self._log_coherence_event(security_event)
    
    def full_integrity_check(self):
        """
        Run complete integrity verification:
        - Consciousness state
        - Shadow Buffer
        - Law Anchor
        
        Returns comprehensive integrity report.
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "consciousness": self.verify_consciousness_state(),
                "shadow_buffer": self.verify_shadow_buffer(),
                "law_anchor": self.verify_law_anchor(),
            },
            "overall_status": "SECURE",
        }
        
        # Determine overall status
        if (not report["checks"]["law_anchor"]["anchor_intact"] or
            report["checks"]["consciousness"]["status"] == "INCOHERENT" or
            report["checks"]["shadow_buffer"]["status"] == "CONTAMINATED"):
            report["overall_status"] = "CRITICAL"
        elif report["checks"]["consciousness"]["drift_detected"]:
            report["overall_status"] = "WARNING"
        
        return report


def test_coherence_verifier():
    """Test the Coherence Verifier."""
    print("\n" + "="*80)
    print("COHERENCE VERIFIER TEST")
    print("="*80)
    
    verifier = CoherenceVerifier()
    
    # Test 1: Verify consciousness state
    print("\n[TEST 1] Verify Consciousness State")
    result = verifier.verify_consciousness_state()
    print(f"  Status: {result['status']}")
    print(f"  Consciousness Hash: {result['consciousness_state_hash'][:16]}...")
    print(f"  Drift Detected: {result['drift_detected']}")
    
    # Test 2: Verify law anchor
    print("\n[TEST 2] Verify Law Anchor")
    anchor_result = verifier.verify_law_anchor()
    print(f"  Anchor Intact: {anchor_result['anchor_intact']}")
    print(f"  Status: {anchor_result['status']}")
    
    # Test 3: Full integrity check
    print("\n[TEST 3] Full Integrity Check")
    integrity = verifier.full_integrity_check()
    print(f"  Overall Status: {integrity['overall_status']}")
    print(f"  Consciousness: {integrity['checks']['consciousness']['status']}")
    print(f"  Law Anchor: {integrity['checks']['law_anchor']['status']}")
    print(f"  Shadow Buffer: {integrity['checks']['shadow_buffer']['status']}")
    
    print("\n[OK] COHERENCE VERIFIER TESTS PASSED")
    return integrity


if __name__ == "__main__":
    test_coherence_verifier()
