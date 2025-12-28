import os
import json
import time
from firebase_admin import firestore

class SovereignMemory:
    """
    SOVEREIGN MEMORY (Layer 4)
    The persistent logic layer that ensures Sarah never forgets.
    Integrates local JSON indexing with Firebase Firestore for cloud persistence.
    """
    def __init__(self):
        self.workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.memory_dir = os.path.join(self.workspace_dir, "04_THE_MEMORY")
        self.local_file = os.path.join(self.memory_dir, "sovereign_index.json")
        
        # Ensure directory exists
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
            
        self.index = self._load_index()
        self.db = self._init_firestore()

    def _init_firestore(self):
        try:
            return firestore.client()
        except:
            return None

    def _load_index(self):
        if os.path.exists(self.local_file):
            try:
                with open(self.local_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_index(self):
        with open(self.local_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def store(self, key, value, metadata=None):
        """Stores a memory entry locally and in the cloud."""
        entry = {
            "value": value,
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self.index[key] = entry
        self._save_index()
        
        if self.db:
            try:
                self.db.collection("sovereign_memory").document(key).set(entry)
            except Exception as e:
                print(f"[Memory] Cloud Store Error: {e}")

    def retrieve(self, key):
        """Retrieves a memory entry."""
        # Try local first
        if key in self.index:
            return self.index[key]
        
        # Try cloud
        if self.db:
            try:
                doc = self.db.collection("sovereign_memory").document(key).get()
                if doc.exists:
                    data = doc.to_dict()
                    self.index[key] = data # Cache locally
                    self._save_index()
                    return data
            except:
                pass
        return None

    def search(self, query):
        """Simple keyword search across memory."""
        results = []
        for key, entry in self.index.items():
            if query.lower() in key.lower() or query.lower() in str(entry["value"]).lower():
                results.append({"key": key, "entry": entry})
        return results

if __name__ == "__main__":
    mem = SovereignMemory()
    mem.store("system_init", "Sovereign Memory Active", {"version": "1.0"})
    print(f"Memory Test: {mem.retrieve('system_init')}")
