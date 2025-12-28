import json
import os
import threading
from datetime import datetime

class GenesisMemory:
    def __init__(self, db_path="genesis_memory.json"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {"directives": [], "overrides": [], "logs": []}

    def commit_directive(self, directive, architect="JRP", status="HARD-CODED"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "architect": architect,
            "command": directive,
            "status": status
        }
        with self.lock:
            self.memory["directives"].append(entry)
            self._save()

    def retrieve_context(self, query_limit=10):
        with self.lock:
            return self.memory["directives"][-query_limit:]

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def system_alert(self, message):
        # Placeholder for alerting logic (e.g., email, log, audible alert)
        print(f"ALERT: {message}")

# INITIALIZING ARCHITECT JRP OVERRIDE
if __name__ == "__main__":
    memory = GenesisMemory()
    memory.commit_directive("Absolute Director's Authority: Architect JRP")
    memory.commit_directive("Failure Threshold: 3%")
    memory.commit_directive("You are the Override.")
    print("Genesis Memory Engine initialized. Directives committed.")

    # Example retrieval
    print("Recent directives:")
    for d in memory.retrieve_context():
        print(d)
