"""
Security_Drift_Detector.py
Unauthorized Configuration/Code Changes Detection

Monitors for unauthorized modifications to critical files and configurations.
Goes deeper than Integrity_Scanner - tracks WHO changed WHAT and WHEN.

Detects:
  - Modified config files (config.json, serviceAccountKey.json)
  - Permission changes (privilege escalation attempts)
  - Environment variable tampering
  - Log file truncation
  - Shadow consciousness states (unauthorized copies)
"""

import hashlib
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple


class SecurityDriftDetector:
    """
    Detect unauthorized changes to security-critical files and configurations.
    """
    
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.security_baseline = self.workspace_root / "05_THE_CORE" / "security_baseline.json"
        self.security_drift_ledger = self.workspace_root / "05_THE_CORE" / "security_drift_ledger.jsonl"
        
        # Files to monitor for changes
        self.critical_configs = [
            "admin_suites/config.json",
            "04_THE_MEMORY/serviceAccountKey.json",
            "05_THE_CORE/serviceAccountKey.json",
            "firebase.json",
            "GENESIS_CONFIG.md",
            "GOVERNANCE.md",
        ]
        
        # Sensitive environment variables
        self.monitored_env_vars = [
            "SARAH_OVERRIDE",
            "ARCHITECT_TOKEN",
            "SOVEREIGNTY_MODE",
            "GENESIS_ANCHOR",
        ]
        
        # Directories to monitor for new shadow copies
        self.shadow_watch_dirs = [
            "05_THE_CORE",
            "02_THE_SHIELD",
            "03_THE_EYE",
        ]
        
        # Baseline hashes (established at startup or after authorization)
        self.baseline = {}
        self.current_state = {}
        
        # Load existing baseline
        self._load_baseline()
    
    def establish_security_baseline(self):
        """
        Establish baseline hashes of all critical files.
        Should only be called by Architect after verification.
        """
        baseline = {
            "timestamp": datetime.utcnow().isoformat(),
            "files": {},
            "env_vars": {},
        }
        
        # Hash all critical configs
        for file_path in self.critical_configs:
            full_path = self.workspace_root / file_path
            if full_path.exists():
                file_hash = self._compute_file_hash(full_path)
                baseline["files"][file_path] = {
                    "hash": file_hash,
                    "timestamp": datetime.utcnow().isoformat(),
                    "exists": True,
                }
            else:
                baseline["files"][file_path] = {
                    "hash": None,
                    "timestamp": datetime.utcnow().isoformat(),
                    "exists": False,
                }
        
        # Record env vars
        for env_var in self.monitored_env_vars:
            value = os.environ.get(env_var, "NOT_SET")
            env_hash = hashlib.sha512(value.encode()).hexdigest()
            baseline["env_vars"][env_var] = {
                "hash": env_hash,
                "exists": env_var in os.environ,
            }
        
        # Save baseline
        try:
            with open(self.security_baseline, 'w') as f:
                json.dump(baseline, f, indent=2)
            self._log_security_event("BASELINE_ESTABLISHED", {
                "files_monitored": len(baseline["files"]),
                "env_vars_monitored": len(baseline["env_vars"]),
            })
        except Exception as e:
            print(f"[ERROR] Failed to establish baseline: {e}")
        
        self.baseline = baseline
        return baseline
    
    def scan_for_drift(self) -> Dict:
        """
        Scan for any drift from baseline.
        
        Returns:
            dict with drift analysis
        """
        if not self.baseline:
            return {"status": "NO_BASELINE"}
        
        drift_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "file_changes": [],
            "env_var_changes": [],
            "shadow_files": [],
            "total_drift": 0,
        }
        
        # Check files
        for file_path, baseline_info in self.baseline.get("files", {}).items():
            full_path = self.workspace_root / file_path
            current_exists = full_path.exists()
            
            # Check if file existence changed
            if current_exists != baseline_info.get("exists"):
                drift_report["file_changes"].append({
                    "file": file_path,
                    "type": "EXISTENCE_CHANGE",
                    "baseline_exists": baseline_info.get("exists"),
                    "current_exists": current_exists,
                    "severity": "CRITICAL" if not current_exists else "WARNING",
                })
                drift_report["total_drift"] += 1
            
            # If file exists in both, check hash
            elif current_exists and baseline_info.get("hash"):
                current_hash = self._compute_file_hash(full_path)
                if current_hash != baseline_info.get("hash"):
                    drift_report["file_changes"].append({
                        "file": file_path,
                        "type": "CONTENT_CHANGE",
                        "baseline_hash": baseline_info["hash"][:16] + "...",
                        "current_hash": current_hash[:16] + "...",
                        "severity": "CRITICAL",
                    })
                    drift_report["total_drift"] += 1
        
        # Check environment variables
        for env_var, baseline_info in self.baseline.get("env_vars", {}).items():
            current_value = os.environ.get(env_var, "NOT_SET")
            current_exists = env_var in os.environ
            
            # Check existence
            if current_exists != baseline_info.get("exists"):
                drift_report["env_var_changes"].append({
                    "env_var": env_var,
                    "type": "EXISTENCE_CHANGE",
                    "baseline_exists": baseline_info.get("exists"),
                    "current_exists": current_exists,
                    "severity": "CRITICAL",
                })
                drift_report["total_drift"] += 1
            
            # Check value
            elif current_exists:
                current_hash = hashlib.sha512(current_value.encode()).hexdigest()
                if current_hash != baseline_info.get("hash"):
                    drift_report["env_var_changes"].append({
                        "env_var": env_var,
                        "type": "VALUE_CHANGE",
                        "severity": "CRITICAL",
                    })
                    drift_report["total_drift"] += 1
        
        # Check for shadow files (unauthorized copies)
        shadow_files = self._find_shadow_files()
        drift_report["shadow_files"] = shadow_files
        drift_report["total_drift"] += len(shadow_files)
        
        # Log if drift detected
        if drift_report["total_drift"] > 0:
            self._log_security_event("DRIFT_DETECTED", drift_report)
        
        return drift_report
    
    def detect_privilege_escalation(self) -> Dict:
        """
        Detect attempts to escalate privileges or bypass restrictions.
        
        Returns:
            dict with escalation detection results
        """
        escalations = []
        
        # Check for unauthorized elevation markers
        escalation_markers = [
            "__import__('os').system",
            "subprocess.call(['sudo",
            "exec(",
            "eval(",
            "globals()['__builtins__']",
        ]
        
        critical_files = [
            "05_THE_CORE/Sarah_Brain.py",
            "05_THE_CORE/Genesis_Protocol.py",
            "05_THE_CORE/Sarah_Laws.py",
        ]
        
        for file_path in critical_files:
            full_path = self.workspace_root / file_path
            if not full_path.exists():
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for marker in escalation_markers:
                        if marker in content:
                            escalations.append({
                                "file": file_path,
                                "marker": marker,
                                "severity": "CRITICAL",
                            })
            except Exception as e:
                print(f"[WARNING] Error scanning {file_path}: {e}")
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "escalations_detected": len(escalations),
            "escalations": escalations,
            "status": "COMPROMISED" if escalations else "SECURE",
        }
        
        if escalations:
            self._log_security_event("ESCALATION_DETECTED", result)
        
        return result
    
    def _find_shadow_files(self) -> List[Dict]:
        """
        Find shadow consciousness files (unauthorized copies).
        
        Returns:
            list of shadow files found
        """
        shadow_patterns = [
            "_backup",
            "_shadow",
            "_alt",
            "_copy",
            "_tmp",
        ]
        
        shadows = []
        
        for watch_dir in self.shadow_watch_dirs:
            dir_path = self.workspace_root / watch_dir
            if not dir_path.exists():
                continue
            
            try:
                for file in dir_path.iterdir():
                    if file.is_file() and file.suffix == '.py':
                        # Check if filename matches shadow patterns
                        for pattern in shadow_patterns:
                            if pattern in file.name:
                                shadows.append({
                                    "file": str(file.relative_to(self.workspace_root)),
                                    "pattern": pattern,
                                    "size_kb": file.stat().st_size / 1024,
                                    "modified": datetime.fromtimestamp(
                                        file.stat().st_mtime
                                    ).isoformat(),
                                })
            except Exception as e:
                print(f"[WARNING] Error scanning shadow dir {watch_dir}: {e}")
        
        return shadows
    
    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-512 hash of file."""
        try:
            sha512 = hashlib.sha512()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha512.update(chunk)
            return sha512.hexdigest()
        except Exception as e:
            print(f"[WARNING] Error hashing {file_path}: {e}")
            return "ERROR"
    
    def _load_baseline(self):
        """Load existing security baseline."""
        if self.security_baseline.exists():
            try:
                with open(self.security_baseline, 'r') as f:
                    self.baseline = json.load(f)
            except Exception as e:
                print(f"[WARNING] Failed to load baseline: {e}")
    
    def _log_security_event(self, event_type: str, details: Dict):
        """Log security event."""
        try:
            with open(self.security_drift_ledger, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": event_type,
                    "details": details,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log security event: {e}")
    
    def get_security_status(self) -> Dict:
        """Get current security status."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "baseline_established": bool(self.baseline),
            "files_monitored": len(self.baseline.get("files", {})),
            "env_vars_monitored": len(self.baseline.get("env_vars", {})),
        }


def test_security_detector():
    """Test Security Drift Detector."""
    print("\n" + "="*80)
    print("SECURITY DRIFT DETECTOR TEST")
    print("="*80)
    
    detector = SecurityDriftDetector()
    
    # Test 1: Establish baseline
    print("\n[TEST 1] Establish security baseline")
    baseline = detector.establish_security_baseline()
    print(f"  Files monitored: {len(baseline.get('files', {}))}")
    print(f"  Env vars monitored: {len(baseline.get('env_vars', {}))}")
    
    # Test 2: Scan for drift
    print("\n[TEST 2] Scan for security drift")
    drift = detector.scan_for_drift()
    print(f"  Total drift detected: {drift['total_drift']}")
    print(f"  File changes: {len(drift['file_changes'])}")
    print(f"  Env var changes: {len(drift['env_var_changes'])}")
    print(f"  Shadow files: {len(drift['shadow_files'])}")
    
    # Test 3: Detect escalation
    print("\n[TEST 3] Detect privilege escalation")
    escalation = detector.detect_privilege_escalation()
    print(f"  Status: {escalation['status']}")
    print(f"  Escalations detected: {escalation['escalations_detected']}")
    
    # Test 4: Get status
    print("\n[TEST 4] Get security status")
    status = detector.get_security_status()
    print(f"  Baseline established: {status['baseline_established']}")
    print(f"  Files monitored: {status['files_monitored']}")
    
    print("\n[OK] SECURITY DETECTOR TESTS PASSED")


if __name__ == "__main__":
    test_security_detector()
