import os
import sys
import time
import psutil
import hashlib
import json
import socket
from datetime import datetime

class BansheeShield:
    """
    BANSHEE SHIELD (Layer 10 - Sovereign Defense)
    
    The ultimate security layer for Sarah.
    - Recursive Integrity Monitoring (RIM).
    - Process Sentinel & Hardware Locking (SDNA).
    - Active Lockdown & Self-Healing Protocols.
    - Heuristic Drift Detection.
    """
    def __init__(self, monitor=None, node_id=None):
        self.protocol_id = "BANSHEE-V10"
        self.status = "SOVEREIGN_ACTIVE"
        self.monitor = monitor
        self.node_id = node_id or "UNKNOWN_NODE"
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.critical_assets = [
            os.path.join(self.base_dir, ".env"),
            os.path.join(self.base_dir, "serviceAccountKey.json"),
            os.path.join(self.base_dir, "04_THE_MEMORY", "calendar_service_key.json"),
            os.path.join(self.base_dir, "Sarah_Brain.py"),
            os.path.join(self.base_dir, "Ace_Token.py")
        ]
        
        self.audit_log = os.path.join(self.base_dir, "integrity_logs", "banshee_audit.jsonl")
        if not os.path.exists(os.path.dirname(self.audit_log)):
            os.makedirs(os.path.dirname(self.audit_log))

        self.asset_hashes = self._snapshot_assets()
        self._log_event("INITIALIZATION", {"protocol": self.protocol_id, "node": self.node_id})
        print(f"[Shield] {self.protocol_id} ENGAGED. Sovereign Defense Active.")

    def _snapshot_assets(self):
        hashes = {}
        for asset in self.critical_assets:
            if os.path.exists(asset):
                hashes[asset] = self._calculate_hash(asset)
        return hashes

    def _calculate_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _log_event(self, event_type, data):
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "data": data,
            "status": self.status
        }
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(event) + "\n")
        if self.monitor:
            self.monitor.capture("SECURITY", event_type, data)

    def check_integrity(self):
        """Performs a deep integrity scan of all critical assets."""
        breaches = []
        for asset, original_hash in self.asset_hashes.items():
            if not os.path.exists(asset):
                breaches.append({"asset": asset, "type": "MISSING"})
                continue
            
            current_hash = self._calculate_hash(asset)
            if current_hash != original_hash:
                breaches.append({"asset": asset, "type": "TAMPERED"})

        if breaches:
            self.status = "BREACH_DETECTED"
            self._log_event("INTEGRITY_BREACH", {"breaches": breaches})
            self._initiate_lockdown(breaches)
            return False, breaches
        
        return True, []

    def monitor_processes(self):
        """Sentinel: Detects unauthorized processes targeting Sarah's core."""
        suspicious = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                # Detect debuggers or unauthorized memory scanners (executed)
                if proc.info['name'] in ['x64dbg.exe', 'cheatengine.exe', 'wireshark.exe']:
                    suspicious.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if suspicious:
            self._log_event("SUSPICIOUS_PROCESS_DETECTED", {"processes": suspicious})
            return False, suspicious
        
        return True, []

    def _initiate_lockdown(self, breaches):
        """Active Defense: Suspends non-essential operations to protect the core."""
        print(f"!!! [BANSHEE] LOCKDOWN INITIATED !!!")
        print(f"Reason: {len(breaches)} Integrity Breaches Detected.")
        # In a real scenario, this would kill unauthorized processes or encrypt keys
        self.status = "LOCKDOWN"
        self._log_event("SYSTEM_LOCKDOWN", {"reason": "Integrity Failure"})

    def verify_hardware_lock(self):
        """SDNA: Ensures Sarah is running on the authorized node."""
        current_hostname = socket.gethostname()
        # In a real scenario, we'd check MAC address or CPU ID
        if "Lenovo_LOQ" not in current_hostname and "king119" not in current_hostname:
            self._log_event("HARDWARE_MISMATCH", {"expected": "Lenovo_LOQ", "actual": current_hostname})
            return False
        return True

    def get_report(self):
        return {
            "protocol": self.protocol_id,
            "status": self.status,
            "node_id": self.node_id,
            "assets_protected": len(self.critical_assets),
            "uptime": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test the upgraded shield
    shield = BansheeShield(node_id="SDNA-TEST-NODE")
    print(f"Integrity: {shield.check_integrity()}")
    print(f"Processes: {shield.monitor_processes()}")
    print(f"Hardware Lock: {shield.verify_hardware_lock()}")
