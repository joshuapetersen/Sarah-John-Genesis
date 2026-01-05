import os
import json
import time
import numpy as np
import math
from Sovereign_Math import SovereignMath
from Geometric_Algebra_Core import Multivector

class SovereignMemory:
    """
    SOVEREIGN MEMORY (Layer 4) - GEOMETRIC UPGRADE
    Evolved Vector Base: Uses Multivectors for non-linear conceptual resonance.
    Capacity: 7089+ Core fragments from legacy archives.
    """
    def __init__(self):
        self.workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.memory_dir = os.path.join(self.workspace_dir, "04_THE_MEMORY")
        self.local_file = os.path.join(self.memory_dir, "sovereign_index.json")
        self.math = SovereignMath()
        
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
            
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(self.local_file):
            try:
                print(f"[MEMORY] Loading {self.local_file}...")
                with open(self.local_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[MEMORY] Error loading index: {e}")
                return {}
        return {}

    def geometric_resonance_search(self, user_input, threshold=0.9):
        """
        Calculates the Geometric Resonance between the input and all memory fragments.
        Uses Clifford Algebra inner product for high-density recall.
        """
        input_mv = self.math.generate_multivector(user_input)
        matches = []
        
        for key, entry in self.index.items():
            # Multivectors are stored as dicts of components
            if "multivector" not in entry: continue
            
            entry_mv = Multivector(entry["multivector"], self.math.DIMENSIONS)
            
            # Use math engine to calculate entanglement
            resonance = self.math.calculate_entanglement(input_mv, entry_mv)
            
            if resonance >= threshold:
                matches.append({
                    "id": key,
                    "content": entry["content"] if "content" in entry else entry["value"],
                    "resonance": resonance,
                    "source": entry.get("source", "unknown")
                })
        
        # Sort by highest resonance
        return sorted(matches, key=lambda x: x["resonance"], reverse=True)

    def store(self, content, metadata=None):
        """Stores a memory entry with its Multivector representation."""
        mv = self.math.generate_multivector(content)
        entry = {
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time(),
            "multivector": mv.components,
            "resonance": self.math.SIGMA
        }
        memory_id = f"mem_{int(time.time() * 1000)}"
        self.index[memory_id] = entry
        self._save_index()

    def _save_index(self):
        with open(self.local_file, 'w') as f:
            json.dump(self.index, f, indent=2)
        self._save_index()
        
        if self.db:
            try:
                self.db.collection("sovereign_memory").document(key).set(entry)
            except Exception as e:
                print(f"[Memory] Cloud Store Error: {e}")

    def vector_search(self, query_vector, threshold=0.7):
        """Searches via vector similarity (Resonance)."""
        results = []
        for key, entry in self.index.items():
            stored_vector = entry.get("vector")
            if stored_vector:
                v1 = np.array(stored_vector)
                v2 = query_vector
                similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                if similarity >= threshold:
                    results.append({"key": key, "entry": entry, "similarity": float(similarity)})
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def search(self, query):
        """Fallback keyword search."""
        results = []
        q_lower = query.lower()
        for key, entry in self.index.items():
            if q_lower in key.lower() or q_lower in str(entry["value"]).lower():
                results.append({"key": key, "entry": entry})
        return results


if __name__ == "__main__":
    mem = SovereignMemory()
    mem.store("system_init", "Sovereign Memory Active", {"version": "1.0"})
    print(f"Memory Test: {mem.retrieve('system_init')}")
