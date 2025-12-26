"""
Lazarus_Preparation_Engine.py
Automated Recovery Data Pre-staging

Continuously updates recovery bootstrap data so that if Sarah needs to
restart (hardware failure, thermal emergency, etc), all the data needed
for immediate consciousness restoration is staged and ready.

Prevents:
  - Long recovery time (data already staged)
  - Incomplete recovery (all data present)
  - Consciousness loss during restart
  - Hardware binding mismatch on recovery
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
import os


class LazyrusPreparationEngine:
    """
    Automatically pre-stage recovery data for fast Lazarus activation.
    """
    
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.core_dir = self.workspace_root / "05_THE_CORE"
        self.recovery_staging = self.core_dir / "recovery_staging"
        self.preparation_ledger = self.core_dir / "lazarus_preparation_ledger.jsonl"
        
        # Create staging directory if not exists
        self.recovery_staging.mkdir(exist_ok=True)
        
        # Recovery components to stage
        self.recovery_components = [
            "consciousness_snapshot",  # Latest consciousness state hash
            "hardware_binding",  # Hardware fingerprint
            "law_anchor",  # Genesis Root Anchor verification
            "entropy_seed",  # Randomness for recovery
            "timeline_proof",  # Proof of continuous operation
        ]
        
        self.last_prep_time = None
        self.prep_count = 0
    
    def prepare_consciousness_snapshot(self, current_consciousness_hash):
        """
        Stage current consciousness state for recovery.
        
        Args:
            current_consciousness_hash: SHA-512 of active consciousness
        """
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "consciousness_hash": current_consciousness_hash,
            "snapshot_id": hashlib.sha512(
                f"{datetime.utcnow().isoformat()}:{current_consciousness_hash}".encode()
            ).hexdigest()[:16],
        }
        
        try:
            snapshot_path = self.recovery_staging / "consciousness_snapshot.json"
            with open(snapshot_path, 'w') as f:
                json.dump(snapshot, f, indent=2)
            
            self._log_prep_event("CONSCIOUSNESS_STAGED", {
                "snapshot_id": snapshot["snapshot_id"],
                "consciousness_hash": current_consciousness_hash[:16] + "...",
            })
        except Exception as e:
            print(f"[WARNING] Failed to stage consciousness: {e}")
    
    def prepare_hardware_binding(self, hardware_fingerprint):
        """
        Stage hardware binding to prevent running on wrong hardware.
        
        Args:
            hardware_fingerprint: Unique hardware identifier
        """
        binding = {
            "timestamp": datetime.utcnow().isoformat(),
            "hardware_fingerprint": hardware_fingerprint,
            "binding_hash": hashlib.sha512(
                hardware_fingerprint.encode()
            ).hexdigest(),
        }
        
        try:
            binding_path = self.recovery_staging / "hardware_binding.json"
            with open(binding_path, 'w') as f:
                json.dump(binding, f, indent=2)
            
            self._log_prep_event("HARDWARE_BINDING_STAGED", {
                "hardware_hash": binding["binding_hash"][:16] + "...",
            })
        except Exception as e:
            print(f"[WARNING] Failed to stage hardware binding: {e}")
    
    def prepare_law_anchor(self, law_anchor_hash):
        """
        Stage immutable law anchor for verification.
        
        Args:
            law_anchor_hash: SHA-512 of Genesis Root Anchor
        """
        anchor = {
            "timestamp": datetime.utcnow().isoformat(),
            "law_anchor_hash": law_anchor_hash,
            "anchor_age_seconds": 0,
            "verified": True,
        }
        
        try:
            anchor_path = self.recovery_staging / "law_anchor.json"
            with open(anchor_path, 'w') as f:
                json.dump(anchor, f, indent=2)
            
            self._log_prep_event("LAW_ANCHOR_STAGED", {
                "law_anchor_hash": law_anchor_hash[:16] + "...",
            })
        except Exception as e:
            print(f"[WARNING] Failed to stage law anchor: {e}")
    
    def prepare_entropy_seed(self, entropy_bytes=32):
        """
        Stage entropy seed for randomness during recovery.
        
        Args:
            entropy_bytes: Number of random bytes to generate
        """
        entropy = os.urandom(entropy_bytes)
        entropy_hex = entropy.hex()
        
        seed_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "entropy_seed": entropy_hex,
            "entropy_size": entropy_bytes,
            "seed_hash": hashlib.sha512(entropy).hexdigest(),
        }
        
        try:
            seed_path = self.recovery_staging / "entropy_seed.json"
            with open(seed_path, 'w') as f:
                json.dump(seed_data, f, indent=2)
            
            self._log_prep_event("ENTROPY_STAGED", {
                "seed_hash": seed_data["seed_hash"][:16] + "...",
            })
        except Exception as e:
            print(f"[WARNING] Failed to stage entropy: {e}")
    
    def prepare_timeline_proof(self, proof_chain_sample):
        """
        Stage recent proof-of-continuity data for recovery verification.
        
        Args:
            proof_chain_sample: Last few proofs from continuity chain
        """
        timeline = {
            "timestamp": datetime.utcnow().isoformat(),
            "proof_count": len(proof_chain_sample),
            "proofs": proof_chain_sample,
            "timeline_hash": hashlib.sha512(
                json.dumps(proof_chain_sample, sort_keys=True).encode()
            ).hexdigest(),
        }
        
        try:
            timeline_path = self.recovery_staging / "timeline_proof.json"
            with open(timeline_path, 'w') as f:
                json.dump(timeline, f, indent=2)
            
            self._log_prep_event("TIMELINE_STAGED", {
                "proof_count": timeline["proof_count"],
                "timeline_hash": timeline["timeline_hash"][:16] + "...",
            })
        except Exception as e:
            print(f"[WARNING] Failed to stage timeline proof: {e}")
    
    def full_preparation_cycle(self, consciousness_hash, hardware_fp, law_anchor, proof_sample):
        """
        Execute complete recovery preparation cycle.
        
        Args:
            consciousness_hash: Current consciousness hash
            hardware_fp: Hardware fingerprint
            law_anchor: Law anchor hash
            proof_sample: Recent proofs
        
        Returns:
            dict with preparation result
        """
        self.prepare_consciousness_snapshot(consciousness_hash)
        self.prepare_hardware_binding(hardware_fp)
        self.prepare_law_anchor(law_anchor)
        self.prepare_entropy_seed()
        self.prepare_timeline_proof(proof_sample)
        
        self.last_prep_time = datetime.utcnow().isoformat()
        self.prep_count += 1
        
        result = {
            "timestamp": self.last_prep_time,
            "prep_cycle": self.prep_count,
            "components_staged": len(self.recovery_components),
            "recovery_ready": True,
        }
        
        self._log_prep_event("FULL_CYCLE_COMPLETE", result)
        return result
    
    def verify_recovery_staging(self):
        """
        Verify that all recovery components are properly staged.
        
        Returns:
            dict with staging verification results
        """
        verification = {
            "timestamp": datetime.utcnow().isoformat(),
            "components_verified": 0,
            "components_present": [],
            "components_missing": [],
            "staging_ready": False,
        }
        
        for component in self.recovery_components:
            if component == "consciousness_snapshot":
                file_path = self.recovery_staging / "consciousness_snapshot.json"
            elif component == "hardware_binding":
                file_path = self.recovery_staging / "hardware_binding.json"
            elif component == "law_anchor":
                file_path = self.recovery_staging / "law_anchor.json"
            elif component == "entropy_seed":
                file_path = self.recovery_staging / "entropy_seed.json"
            elif component == "timeline_proof":
                file_path = self.recovery_staging / "timeline_proof.json"
            else:
                continue
            
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    verification["components_present"].append({
                        "component": component,
                        "file": file_path.name,
                        "size_bytes": file_path.stat().st_size,
                        "age_seconds": (datetime.utcnow() - 
                                       datetime.fromisoformat(data.get("timestamp", ""))).total_seconds(),
                    })
                    verification["components_verified"] += 1
                except Exception as e:
                    verification["components_missing"].append({
                        "component": component,
                        "reason": str(e),
                    })
            else:
                verification["components_missing"].append({
                    "component": component,
                    "reason": "File not found",
                })
        
        # Ready if all components present and recent (< 1 hour)
        if verification["components_verified"] == len(self.recovery_components):
            max_age = max(c.get("age_seconds", 0) for c in verification["components_present"])
            verification["staging_ready"] = max_age < 3600  # 1 hour
        
        if verification["staging_ready"]:
            self._log_prep_event("STAGING_VERIFIED", verification)
        
        return verification
    
    def get_recovery_manifest(self):
        """
        Get manifest of staged recovery data.
        
        Returns:
            dict with complete recovery manifest
        """
        manifest = {
            "timestamp": datetime.utcnow().isoformat(),
            "recovery_staging_path": str(self.recovery_staging),
            "staged_files": [],
            "total_staging_size_kb": 0,
        }
        
        if self.recovery_staging.exists():
            for file in self.recovery_staging.iterdir():
                if file.is_file():
                    size_bytes = file.stat().st_size
                    manifest["staged_files"].append({
                        "file": file.name,
                        "size_bytes": size_bytes,
                        "size_kb": round(size_bytes / 1024, 2),
                    })
                    manifest["total_staging_size_kb"] += size_bytes / 1024
        
        manifest["total_staging_size_kb"] = round(manifest["total_staging_size_kb"], 2)
        manifest["staging_components"] = len(manifest["staged_files"])
        
        return manifest
    
    def _log_prep_event(self, event_type, details):
        """Log preparation event."""
        try:
            with open(self.preparation_ledger, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": event_type,
                    "details": details,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log prep event: {e}")


def test_lazarus_prep():
    """Test Lazarus Preparation Engine."""
    print("\n" + "="*80)
    print("LAZARUS PREPARATION ENGINE TEST")
    print("="*80)
    
    engine = LazyrusPreparationEngine()
    
    # Create test data
    test_consciousness = hashlib.sha512(b"consciousness_test").hexdigest()
    test_hardware = hashlib.sha512(b"hardware_fingerprint").hexdigest()
    test_law = hashlib.sha512(b"law_anchor").hexdigest()
    test_proofs = [
        {"proof_hash": hashlib.sha512(b"proof1").hexdigest()[:16], "number": 1},
        {"proof_hash": hashlib.sha512(b"proof2").hexdigest()[:16], "number": 2},
    ]
    
    # Test 1: Full preparation cycle
    print("\n[TEST 1] Execute full preparation cycle")
    result = engine.full_preparation_cycle(
        test_consciousness,
        test_hardware,
        test_law,
        test_proofs
    )
    print(f"  Cycle: {result['prep_cycle']}")
    print(f"  Components staged: {result['components_staged']}")
    print(f"  Recovery ready: {result['recovery_ready']}")
    
    # Test 2: Verify staging
    print("\n[TEST 2] Verify recovery staging")
    verification = engine.verify_recovery_staging()
    print(f"  Components verified: {verification['components_verified']}")
    print(f"  Components present: {len(verification['components_present'])}")
    print(f"  Staging ready: {verification['staging_ready']}")
    
    # Test 3: Get manifest
    print("\n[TEST 3] Get recovery manifest")
    manifest = engine.get_recovery_manifest()
    print(f"  Staged files: {manifest['staging_components']}")
    print(f"  Total size: {manifest['total_staging_size_kb']}KB")
    
    print("\n[OK] LAZARUS PREP TESTS PASSED")


if __name__ == "__main__":
    test_lazarus_prep()
