import json
import os
import numpy as np
from dynamic_vector_model import DynamicVectorModel
from Sovereign_Math import math_engine as math

class MemoryConsolidator:
    """
    Sovereign Memory Consolidation.
    Increases memory density by collapsing low-resonance state clusters.
    """
    def __init__(self, memory_index_path='c:/SarahCore/04_THE_MEMORY/sovereign_index.json', similarity_threshold=0.9):
        self.path = memory_index_path
        self.threshold = similarity_threshold
        self.vector_model = DynamicVectorModel()

    def consolidate(self):
        """
        Loads the vector index and performs a non-linear consolidation.
        """
        if not os.path.exists(self.path):
            print("[CONSOLIDATOR] No memory index found.")
            return

        try:
            with open(self.path, 'r') as f:
                index = json.load(f)
        except Exception as e:
            print(f"[CONSOLIDATOR] Error loading index: {e}")
            return

        keys = list(index.keys())
        vectors = []
        valid_keys = []

        for k in keys:
            v = index[k].get('vector')
            if v:
                vectors.append(np.array(v))
                valid_keys.append(k)

        if len(vectors) < 2:
            print("[CONSOLIDATOR] Insufficient density for consolidation.")
            return

        # Perform clustering
        to_remove = set()
        for i in range(len(vectors)):
            if valid_keys[i] in to_remove: continue
            for j in range(i + 1, len(vectors)):
                if valid_keys[j] in to_remove: continue
                
                # Check Resonance
                resonance = np.dot(vectors[i], vectors[j])
                if resonance > self.threshold:
                    print(f"[CONSOLIDATOR] Redundancy detected: {valid_keys[j]} -> {valid_keys[i]} (Resonance: {resonance:.4f})")
                    to_remove.add(valid_keys[j])

        # Purge redundancies
        for k in to_remove:
            del index[k]

        with open(self.path, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"[CONSOLIDATOR] Purged {len(to_remove)} low-density fragments. Memory density stabilized.")

if __name__ == "__main__":
    consolidator = MemoryConsolidator()
    consolidator.consolidate()
