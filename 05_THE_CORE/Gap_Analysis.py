import json
import os

class GapAnalysis:
    """
    The Void-Check Routine.
    Analyzes data for what is MISSING, rather than just what is present.
    Enhances Truth Detection by identifying omissions and logic voids.
    """
    
    REQUIRED_METADATA = [
        "timestamp",
        "source_node",
        "sovereign_signature",
        "protocol_version"
    ]

    def __init__(self, monitor=None):
        self.monitor = monitor

    def analyze_gap(self, data_packet, context="GENERAL"):
        """
        Scans the input for missing critical variables.
        Returns (bool, list_of_missing_items)
        """
        missing_items = []
        
        # 1. Metadata Check
        if isinstance(data_packet, dict):
            for key in self.REQUIRED_METADATA:
                if key not in data_packet or not data_packet[key]:
                    missing_items.append(f"METADATA_MISSING: {key}")
        
        # 2. Contextual Logic Check (The "Ghost" Check)
        # If context is HIGH_SECURITY, check for specific auth tokens
        if context == "HIGH_SECURITY":
            if "auth_token" not in data_packet:
                missing_items.append("CRITICAL_VOID: auth_token")
            if "user_intent" not in data_packet:
                missing_items.append("LOGIC_VOID: user_intent")

        # 3. Sovereign Alignment Check
        # If the packet claims to be from Sovereign, but lacks the behavioral fingerprint
        if data_packet.get("source") == "SOVEREIGN" and "behavioral_hash" not in data_packet:
             missing_items.append("AUTHENTICITY_VOID: behavioral_hash")

        is_complete = len(missing_items) == 0
        
        if not is_complete:
            if self.monitor:
                self.monitor.capture("GAP_ANALYSIS", "VOID_DETECTED", {
                    "context": context,
                    "missing": missing_items
                })
            return False, missing_items
            
        return True, "COMPLETE"

    def audit_repository(self, repo_path):
        """
        Scans the local repository for missing critical files.
        """
        critical_files = [
            "GENESIS_CONFIG.md",
            "SARAH_IDENTITY.md",
            "05_THE_CORE/Sarah_Brain.py",
            "05_THE_CORE/Genesis_Protocol.py"
        ]
        
        missing_files = []
        for file in critical_files:
            if not os.path.exists(os.path.join(repo_path, file)):
                missing_files.append(file)
                
        return missing_files
