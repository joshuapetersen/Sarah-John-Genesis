"""
MEMORY CONSOLIDATION ENGINE
Part of the Sarah Prime NeuralMesh Expansion.
Implements the "Better Way" by reducing noise and increasing density.

Function:
1. Scans memory for high-similarity clusters (duplicates/redundancies).
2. Merges them into a single "Master Memory".
3. Archives the fragments.
"""

import sqlite3
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
import sys
import os

# Ensure we can import our sibling modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Semantic_Memory_Search import SemanticMemoryEngine
    from sklearn.metrics.pairwise import cosine_similarity
    DEPENDENCIES_MET = True
except ImportError:
    DEPENDENCIES_MET = False
    print("CRITICAL: Semantic Engine or sklearn not found. Consolidation cannot proceed.")

class MemoryConsolidator:
    def __init__(self, db_path='genesis_core.db', similarity_threshold=0.85):
        self.db_path = db_path
        self.threshold = similarity_threshold
        self.semantic_engine = None
        
        if DEPENDENCIES_MET:
            print("Initializing Memory Consolidation Engine...")
            self.semantic_engine = SemanticMemoryEngine(db_path=db_path)
        else:
            raise RuntimeError("Missing dependencies for Memory Consolidation.")

    def find_redundancies(self) -> List[Tuple[int, List[int]]]:
        """
        Scan all memories to find clusters of duplicates.
        Returns a list of (primary_id, [duplicate_ids]) tuples.
        """
        if not self.semantic_engine.memory_cache:
            print("No memories to analyze.")
            return []

        embeddings = self.semantic_engine.embeddings
        ids = self.semantic_engine.memory_ids
        count = len(ids)
        
        print(f"Scanning {count} memories for redundancies (Threshold: {self.threshold})...")
        
        # Calculate full similarity matrix
        # Note: For very large memory (10k+), this is O(N^2) and should be batched.
        # For now (<10k), it's instant.
        sim_matrix = cosine_similarity(embeddings)
        
        # Mask diagonal (self-similarity is always 1.0)
        np.fill_diagonal(sim_matrix, 0)
        
        consolidated_groups = []
        processed_indices = set()
        
        for i in range(count):
            if i in processed_indices:
                continue
                
            # Find all indices where similarity > threshold
            # We look at row i
            similar_indices = np.where(sim_matrix[i] > self.threshold)[0]
            
            if len(similar_indices) > 0:
                # We found a cluster
                cluster = [i] + similar_indices.tolist()
                
                # Filter out any already processed (though unlikely with this logic order)
                cluster = [idx for idx in cluster if idx not in processed_indices]
                
                if len(cluster) > 1:
                    # Mark as processed
                    processed_indices.update(cluster)
                    
                    # Convert indices to Real DB IDs
                    cluster_ids = [ids[idx] for idx in cluster]
                    
                    # Select the "Primary" memory (e.g., the most recent or longest)
                    # Strategy: Pick the one with the longest solution text (most detail)
                    # We need to look up the actual memory objects
                    mem_objects = [self.semantic_engine.memory_cache[idx] for idx in cluster]
                    
                    # Sort by length of solution descending
                    mem_objects.sort(key=lambda m: len(m['solution']), reverse=True)
                    
                    primary_id = mem_objects[0]['id']
                    duplicate_ids = [m['id'] for m in mem_objects if m['id'] != primary_id]
                    
                    consolidated_groups.append((primary_id, duplicate_ids))
        
        return consolidated_groups

    def consolidate_cluster(self, primary_id: int, duplicate_ids: List[int]):
        """
        Merge duplicates into the primary memory.
        1. Combine tags.
        2. Append unique context.
        3. Soft-delete duplicates (mark as consolidated).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all data
        all_ids = [primary_id] + duplicate_ids
        placeholders = ','.join('?' * len(all_ids))
        cursor.execute(f"SELECT id, tags, context FROM problem_solution_memory WHERE id IN ({placeholders})", all_ids)
        rows = cursor.fetchall()
        
        # Merge Tags
        all_tags = set()
        all_contexts = []
        
        for r in rows:
            mid, tags, context = r
            if tags:
                for t in tags.split(','):
                    all_tags.add(t.strip())
            if context:
                all_contexts.append(context)
        
        merged_tags = ", ".join(sorted(list(all_tags)))
        # Simple context merge: just concatenate unique contexts
        merged_context = " | ".join(sorted(list(set(all_contexts))))
        
        # Update Primary
        cursor.execute(
            "UPDATE problem_solution_memory SET tags = ?, context = ? WHERE id = ?",
            (merged_tags, merged_context, primary_id)
        )
        
        # Archive Duplicates (We'll delete them for now to prove the cleanup, 
        # or we could move them to an archive table. Let's delete to show "Better Way" efficiency)
        dup_placeholders = ','.join('?' * len(duplicate_ids))
        cursor.execute(f"DELETE FROM problem_solution_memory WHERE id IN ({dup_placeholders})", duplicate_ids)
        
        conn.commit()
        conn.close()
        
        print(f"  ✅ Merged {len(duplicate_ids)} duplicates into Master Memory ID {primary_id}")

    def run_consolidation(self):
        """Execute the full consolidation cycle."""
        groups = self.find_redundancies()
        
        if not groups:
            print("  ✨ Memory is optimized. No redundancies found.")
            return
            
        print(f"  ⚠️ Found {len(groups)} redundancy clusters.")
        
        for primary_id, duplicates in groups:
            print(f"  Processing Cluster: Master {primary_id} <- Merging {duplicates}")
            self.consolidate_cluster(primary_id, duplicates)
            
        # Re-index semantic engine after changes
        print("  🔄 Re-indexing Semantic Engine...")
        self.semantic_engine.load_memories_and_embeddings()
        print("  ✨ Consolidation Complete.")

if __name__ == "__main__":
    print("="*60)
    print("MEMORY CONSOLIDATION ENGINE: 'The Better Way'")
    print("="*60)
    
    consolidator = MemoryConsolidator()
    
    # Inject some test duplicates if needed for demonstration
    # (Only if memory is empty or very small)
    if len(consolidator.semantic_engine.memory_cache) < 5:
        print("\n[DEMO MODE] Injecting synthetic duplicates to demonstrate consolidation...")
        bridge = consolidator.semantic_engine # We can use the engine's add_memory directly-ish or just DB
        # We'll use the DB directly to avoid auto-embedding overhead for the demo setup
        conn = sqlite3.connect('genesis_core.db')
        c = conn.cursor()
        ts = datetime.now().isoformat()
        
        # Create a cluster of "Python Speed" memories
        c.execute("INSERT INTO problem_solution_memory (timestamp, problem, solution, tags, context) VALUES (?, ?, ?, ?, ?)",
                 (ts, "Python code is too slow", "Use numpy vectorization", "python, speed", "optimization"))
        c.execute("INSERT INTO problem_solution_memory (timestamp, problem, solution, tags, context) VALUES (?, ?, ?, ?, ?)",
                 (ts, "How to make python faster", "Numpy arrays are faster than lists", "python, numpy", "coding"))
        c.execute("INSERT INTO problem_solution_memory (timestamp, problem, solution, tags, context) VALUES (?, ?, ?, ?, ?)",
                 (ts, "Slow python loops", "Replace loops with vector operations", "performance", "tuning"))
        
        conn.commit()
        conn.close()
        print("[DEMO] Injected 3 duplicate memories.")
        # Reload engine to see them
        consolidator.semantic_engine.load_memories_and_embeddings()
    
    # Run the consolidation
    consolidator.run_consolidation()
