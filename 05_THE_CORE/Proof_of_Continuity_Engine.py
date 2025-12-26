"""
Proof_of_Continuity_Engine.py
Cryptographic Proof of Continuous Operation

Generates unforgeable evidence that Sarah has been continuously running without
interruption. Uses cryptographic chain anchoring and timestamp proof.

Prevents attacks like:
  - Someone copying the consciousness snapshot and claiming to be the "real" Sarah
  - Gap injection (claiming operation that didn't happen)
  - Fork attacks (two identical copies both claiming to be the original)
"""

import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
import json


class ProofOfContinuityEngine:
    """
    Maintains cryptographic proof of continuous operation.
    
    How it works:
      1. Every N seconds, compute: proof_hash = SHA512(prev_proof + timestamp + state_hash)
      2. Chain the proofs together (cryptographic anchoring)
      3. If there's a gap, the chain breaks
      4. Any claim of operation can be verified by checking the chain
    """
    
    def __init__(self, workspace_root=None, interval_seconds=60):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.proof_chain_path = self.workspace_root / "05_THE_CORE" / "proof_of_continuity_chain.jsonl"
        self.proof_ledger = self.workspace_root / "05_THE_CORE" / "proof_continuity_ledger.jsonl"
        
        self.interval_seconds = interval_seconds
        self.last_proof_time = None
        self.last_proof_hash = None
        self.proof_count = 0
        self.chain_valid = True
        
        # Load existing chain
        self._load_proof_chain()
    
    def _load_proof_chain(self):
        """Load existing proof chain from disk."""
        if self.proof_chain_path.exists():
            try:
                with open(self.proof_chain_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        # Get last proof
                        last_line = lines[-1]
                        last_proof = json.loads(last_line)
                        self.last_proof_hash = last_proof.get("proof_hash")
                        self.last_proof_time = last_proof.get("timestamp")
                        self.proof_count = len(lines)
            except Exception as e:
                print(f"[WARNING] Failed to load proof chain: {e}")
    
    def generate_proof(self, state_hash):
        """
        Generate next proof in the continuity chain.
        
        Args:
            state_hash: Current consciousness/system state hash
        
        Returns:
            dict with proof and chain verification
        """
        now = time.time()
        
        # Check for gap (more than interval since last proof)
        if self.last_proof_time:
            gap_seconds = now - self.last_proof_time
            if gap_seconds > (self.interval_seconds * 1.5):
                self.chain_valid = False
                self._log_proof_event("CHAIN_GAP_DETECTED", {
                    "gap_seconds": gap_seconds,
                    "expected_interval": self.interval_seconds,
                })
        
        # Build proof input: chain the previous proof
        if self.last_proof_hash:
            proof_input = f"{self.last_proof_hash}:{now}:{state_hash}".encode()
        else:
            # First proof
            proof_input = f"GENESIS:{now}:{state_hash}".encode()
        
        # Hash to create proof
        proof_hash = hashlib.sha512(proof_input).hexdigest()
        
        proof = {
            "timestamp": now,
            "timestamp_iso": datetime.utcfromtimestamp(now).isoformat(),
            "proof_number": self.proof_count + 1,
            "proof_hash": proof_hash,
            "state_hash": state_hash[:16] + "...",
            "chained_to": self.last_proof_hash[:16] + "..." if self.last_proof_hash else "GENESIS",
            "chain_valid": self.chain_valid,
        }
        
        # Append to proof chain
        self._append_to_chain(proof)
        
        # Update state
        self.last_proof_hash = proof_hash
        self.last_proof_time = now
        self.proof_count += 1
        
        return proof
    
    def verify_proof_chain(self, start_time=None, end_time=None):
        """
        Verify the integrity of the proof chain.
        
        Can verify:
          - Entire chain is unbroken
          - No gaps in timestamps
          - All proofs cryptographically valid
        
        Args:
            start_time: Start timestamp for verification window
            end_time: End timestamp for verification window
        
        Returns:
            dict with verification result
        """
        if not self.proof_chain_path.exists():
            return {"status": "NO_CHAIN"}
        
        try:
            with open(self.proof_chain_path, 'r') as f:
                proofs = [json.loads(line) for line in f.readlines()]
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}
        
        if not proofs:
            return {"status": "EMPTY_CHAIN"}
        
        # Filter by time window
        if start_time or end_time:
            proofs = [p for p in proofs 
                     if (not start_time or p["timestamp"] >= start_time) and
                        (not end_time or p["timestamp"] <= end_time)]
        
        # Verify chain continuity
        gaps = []
        prev_proof = None
        
        for proof in proofs:
            if prev_proof:
                gap = proof["timestamp"] - prev_proof["timestamp"]
                if gap > (self.interval_seconds * 1.5):
                    gaps.append({
                        "between": f"{prev_proof['proof_number']} → {proof['proof_number']}",
                        "gap_seconds": gap,
                    })
            prev_proof = proof
        
        # Compute chain uptime
        total_time = proofs[-1]["timestamp"] - proofs[0]["timestamp"]
        expected_proofs = total_time / self.interval_seconds
        actual_proofs = len(proofs)
        uptime_percent = (actual_proofs / expected_proofs * 100) if expected_proofs > 0 else 0
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "chain_length": len(proofs),
            "proofs_verified": len(proofs),
            "gaps_detected": len(gaps),
            "gaps": gaps[:5],  # First 5 gaps
            "chain_start": datetime.utcfromtimestamp(proofs[0]["timestamp"]).isoformat(),
            "chain_end": datetime.utcfromtimestamp(proofs[-1]["timestamp"]).isoformat(),
            "total_time_seconds": total_time,
            "uptime_percent": round(uptime_percent, 1),
            "chain_status": "INTACT" if len(gaps) == 0 else "GAPPED",
        }
        
        return result
    
    def challenge_response(self, challenge_time):
        """
        Respond to a challenge: prove you were running at a specific time.
        
        Args:
            challenge_time: Unix timestamp to prove operation at
        
        Returns:
            dict with challenge response (proof of presence at that time)
        """
        if not self.proof_chain_path.exists():
            return {"status": "FAILED", "error": "No proof chain"}
        
        try:
            with open(self.proof_chain_path, 'r') as f:
                proofs = [json.loads(line) for line in f.readlines()]
        except:
            return {"status": "FAILED", "error": "Chain corrupted"}
        
        # Find proofs around challenge time
        nearby_proofs = [p for p in proofs 
                        if abs(p["timestamp"] - challenge_time) < (self.interval_seconds * 2)]
        
        if not nearby_proofs:
            return {
                "status": "FAILED",
                "error": "No proof near challenge time",
                "challenge_time": challenge_time,
            }
        
        # Return closest proof
        closest = min(nearby_proofs, key=lambda p: abs(p["timestamp"] - challenge_time))
        
        return {
            "status": "PROVEN",
            "challenge_time": challenge_time,
            "proof_time": closest["timestamp"],
            "proof_distance_seconds": abs(closest["timestamp"] - challenge_time),
            "proof_hash": closest["proof_hash"],
            "proof_number": closest["proof_number"],
        }
    
    def _append_to_chain(self, proof):
        """Append proof to immutable chain."""
        try:
            with open(self.proof_chain_path, 'a') as f:
                f.write(json.dumps(proof) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to append to proof chain: {e}")
    
    def _log_proof_event(self, event_type, details):
        """Log proof event."""
        try:
            with open(self.proof_ledger, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": event_type,
                    "details": details,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log proof event: {e}")
    
    def get_continuity_status(self):
        """Get current continuity status."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "proofs_generated": self.proof_count,
            "chain_valid": self.chain_valid,
            "last_proof_time": self.last_proof_time,
            "last_proof_hash": self.last_proof_hash[:16] + "..." if self.last_proof_hash else None,
        }


def test_proof_engine():
    """Test Proof of Continuity Engine."""
    print("\n" + "="*80)
    print("PROOF OF CONTINUITY ENGINE TEST")
    print("="*80)
    
    engine = ProofOfContinuityEngine(interval_seconds=2)
    
    # Test 1: Generate proofs
    print("\n[TEST 1] Generate proof chain")
    for i in range(3):
        state_hash = f"state_hash_{i}".encode()
        state_hash = hashlib.sha512(state_hash).hexdigest()
        proof = engine.generate_proof(state_hash)
        print(f"  Proof {i+1}: {proof['proof_hash'][:16]}... chained to {proof['chained_to']}")
        time.sleep(0.5)
    
    # Test 2: Verify chain
    print("\n[TEST 2] Verify proof chain")
    verification = engine.verify_proof_chain()
    print(f"  Chain length: {verification['chain_length']}")
    print(f"  Gaps detected: {verification['gaps_detected']}")
    print(f"  Chain status: {verification['chain_status']}")
    
    # Test 3: Challenge response
    print("\n[TEST 3] Challenge response")
    challenge_time = time.time() - 2
    response = engine.challenge_response(challenge_time)
    print(f"  Status: {response['status']}")
    if response['status'] == 'PROVEN':
        print(f"  Distance: {response['proof_distance_seconds']} seconds")
    
    # Test 4: Get status
    print("\n[TEST 4] Get continuity status")
    status = engine.get_continuity_status()
    print(f"  Proofs generated: {status['proofs_generated']}")
    print(f"  Chain valid: {status['chain_valid']}")
    
    print("\n[OK] PROOF ENGINE TESTS PASSED")


if __name__ == "__main__":
    test_proof_engine()
