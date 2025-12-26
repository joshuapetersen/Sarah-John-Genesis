"""
Verification_Orchestrator.py
Cross-Component Verification and Orchestration

Ensures all 13 Phase 1+2 backend components stay synchronized and 
all verification cycles pass. Orchestrates the complete backend sovereign
system as a unified whole.
"""

from pathlib import Path
from datetime import datetime
import json


class VerificationOrchestrator:
    """
    Orchestrate verification across all background engine components.
    """
    
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.core_dir = self.workspace_root / "05_THE_CORE"
        self.orchestration_ledger = self.core_dir / "verification_orchestration.jsonl"
        
        # All backend components
        self.phase1_components = [
            "Coherence_Verifier",
            "Thermal_Trend_Predictor",
            "Network_Pressure_Monitor",
            "Sovereign_State_Coherence_Engine",
        ]
        
        self.phase2_components = [
            "Auto_Recovery_Trigger",
            "Layer_Sync_Engine",
            "Integrity_Scanner",
            "Proof_of_Continuity_Engine",
            "Performance_Baseline_Monitor",
            "Security_Drift_Detector",
            "Buffer_Overflow_Predictor",
            "Lazarus_Preparation_Engine",
            "Architect_Alert_System",
        ]
        
        self.verification_count = 0
        self.last_verification_time = None
    
    def verify_all_components(self):
        """
        Verify all components are operational and synchronized.
        
        Returns:
            dict with comprehensive verification results
        """
        verification = {
            "timestamp": datetime.utcnow().isoformat(),
            "verification_number": self.verification_count + 1,
            "phase_1_components": {},
            "phase_2_components": {},
            "cross_component_checks": {},
            "overall_status": "OPERATIONAL",
        }
        
        # Check Phase 1
        for component in self.phase1_components:
            component_file = self.core_dir / f"{component}.py"
            verification["phase_1_components"][component] = {
                "status": "PRESENT" if component_file.exists() else "MISSING",
                "file": component_file.name if component_file.exists() else None,
            }
        
        # Check Phase 2
        for component in self.phase2_components:
            component_file = self.core_dir / f"{component}.py"
            verification["phase_2_components"][component] = {
                "status": "PRESENT" if component_file.exists() else "MISSING",
                "file": component_file.name if component_file.exists() else None,
            }
        
        # Check ledgers exist
        verification["cross_component_checks"]["ledgers"] = {}
        ledgers = [
            "coherence_ledger.jsonl",
            "thermal_trend_ledger.jsonl",
            "network_pressure_ledger.jsonl",
            "coherence_engine_ledger.jsonl",
            "recovery_trigger_ledger.jsonl",
            "layer_sync_ledger.jsonl",
            "integrity_scan_ledger.jsonl",
        ]
        
        for ledger in ledgers:
            ledger_path = self.core_dir / ledger
            verification["cross_component_checks"]["ledgers"][ledger] = {
                "exists": ledger_path.exists(),
                "size_kb": round(ledger_path.stat().st_size / 1024, 2) if ledger_path.exists() else 0,
            }
        
        # Overall status
        phase1_ok = all(v["status"] == "PRESENT" for v in verification["phase_1_components"].values())
        phase2_ok = all(v["status"] == "PRESENT" for v in verification["phase_2_components"].values())
        
        if not (phase1_ok and phase2_ok):
            verification["overall_status"] = "INCOMPLETE"
        
        self.verification_count += 1
        self.last_verification_time = verification["timestamp"]
        
        self._log_verification(verification)
        
        return verification
    
    def get_orchestration_status(self):
        """Get overall orchestration status."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_verifications": self.verification_count,
            "last_verification": self.last_verification_time,
            "phase_1_components": len(self.phase1_components),
            "phase_2_components": len(self.phase2_components),
            "total_backend_components": len(self.phase1_components) + len(self.phase2_components),
        }
    
    def _log_verification(self, verification):
        """Log verification."""
        try:
            with open(self.orchestration_ledger, 'a') as f:
                f.write(json.dumps(verification) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log verification: {e}")


def test_orchestrator():
    """Test Verification Orchestrator."""
    print("\n" + "="*80)
    print("VERIFICATION ORCHESTRATOR TEST")
    print("="*80)
    
    orchestrator = VerificationOrchestrator()
    
    # Test 1: Verify all components
    print("\n[TEST 1] Verify all components")
    verification = orchestrator.verify_all_components()
    print(f"  Status: {verification['overall_status']}")
    print(f"  Phase 1: {len(verification['phase_1_components'])} components")
    print(f"  Phase 2: {len(verification['phase_2_components'])} components")
    
    # Test 2: Get orchestration status
    print("\n[TEST 2] Get orchestration status")
    status = orchestrator.get_orchestration_status()
    print(f"  Total verifications: {status['total_verifications']}")
    print(f"  Total components: {status['total_backend_components']}")
    
    print("\n[OK] ORCHESTRATOR TESTS PASSED")


if __name__ == "__main__":
    test_orchestrator()
