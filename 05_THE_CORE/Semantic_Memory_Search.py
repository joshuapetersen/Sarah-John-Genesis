"""
SEMANTIC MEMORY SEARCH ENGINE
Part of the Sarah Prime NeuralMesh Expansion
Implements First Absolute Law: Logic must be derived from data density.
"""

import sqlite3
import json
import os
import pickle
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Any

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("CRITICAL WARNING: sentence-transformers not found. Semantic search will fail.")

class SemanticMemoryEngine:
    """
    High-density semantic retrieval system.
    Replaces linear keyword search with vector-based similarity.
    """
    
    def __init__(self, db_path='genesis_core.db', model_name='all-MiniLM-L6-v2', cache_path='memory_embeddings.pkl'):
        self.db_path = db_path
        self.cache_path = cache_path
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.memory_ids = []
        self.memory_cache = []
        
        if TRANSFORMERS_AVAILABLE:
            print(f"Initializing Semantic Memory Engine with {model_name}...")
            self.model = SentenceTransformer(model_name)
            self.load_memories_and_embeddings()
        else:
            raise RuntimeError("Semantic Memory Engine requires sentence-transformers.")

    def load_memories_and_embeddings(self):
        """Load memories from DB and either load cached embeddings or compute new ones."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Fetch all memories
        # Currently targeting problem_solution_memory
        try:
            cursor.execute("SELECT id, problem, solution, tags, context FROM problem_solution_memory")
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            print("Table problem_solution_memory not found. Initializing empty.")
            rows = []
        
        conn.close()
        
        current_memories = []
        texts_to_embed = []
        ids = []
        
        for row in rows:
            mem_id, problem, solution, tags, context = row
            # Construct a rich semantic representation
            full_text = f"Problem: {problem}. Context: {context}. Tags: {tags}. Solution: {solution}"
            
            current_memories.append({
                'id': mem_id,
                'problem': problem,
                'solution': solution,
                'tags': tags,
                'context': context,
                'full_text': full_text
            })
            texts_to_embed.append(full_text)
            ids.append(mem_id)
            
        self.memory_cache = current_memories
        self.memory_ids = ids
        
        # Check cache
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                    
                # Verify cache validity (simple count check for now, can be improved to hash)
                if len(cached_data['ids']) == len(ids) and cached_data['ids'] == ids:
                    print("Loaded embeddings from cache.")
                    self.embeddings = cached_data['embeddings']
                    return
                else:
                    print("Cache stale. Recomputing embeddings...")
            except Exception as e:
                print(f"Cache load failed: {e}. Recomputing...")
        
        if not texts_to_embed:
            print("No memories to embed.")
            self.embeddings = np.array([])
            return

        # Compute embeddings
        print(f"Computing embeddings for {len(texts_to_embed)} memories...")
        self.embeddings = self.model.encode(texts_to_embed)
        
        # Save cache
        with open(self.cache_path, 'wb') as f:
            pickle.dump({
                'ids': ids,
                'embeddings': self.embeddings
            }, f)
        print("Embeddings computed and cached.")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for memories semantically similar to the query.
        Returns list of memory dicts with 'score'.
        """
        if not self.memory_cache:
            return []
            
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score < 0.1: # Filter low relevance
                continue
                
            mem = self.memory_cache[idx].copy()
            mem['similarity_score'] = float(score)
            results.append(mem)
            
        return results

    def add_memory(self, problem, solution, tags='', context=''):
        """Add a memory and update embeddings incrementally."""
        # 1. Save to DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        ts = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO problem_solution_memory (timestamp, problem, solution, tags, context) VALUES (?, ?, ?, ?, ?)",
            (ts, problem, solution, tags, context)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 2. Update local state
        full_text = f"Problem: {problem}. Context: {context}. Tags: {tags}. Solution: {solution}"
        new_mem = {
            'id': new_id,
            'problem': problem,
            'solution': solution,
            'tags': tags,
            'context': context,
            'full_text': full_text
        }
        self.memory_cache.append(new_mem)
        self.memory_ids.append(new_id)
        
        # 3. Update embeddings
        new_embedding = self.model.encode([full_text])
        if self.embeddings is None or len(self.embeddings) == 0:
            self.embeddings = new_embedding
        else:
            self.embeddings = np.vstack([self.embeddings, new_embedding])
            
        # 4. Update cache
        with open(self.cache_path, 'wb') as f:
            pickle.dump({
                'ids': self.memory_ids,
                'embeddings': self.embeddings
            }, f)
            
        return new_id

if __name__ == "__main__":
    # Test the engine
    print("Initializing Semantic Memory Engine...")
    engine = SemanticMemoryEngine()
    
    print(f"Total memories: {len(engine.memory_cache)}")
    for m in engine.memory_cache:
        print(f"ID: {m['id']} | Problem: {m['problem']}")

    # Add a test memory if not present
    test_problem = "Python script is slow"
    if not any(m['problem'] == test_problem for m in engine.memory_cache):
        print("Adding test memory...")
        engine.add_memory(
            test_problem, 
            "Use vectorization with numpy instead of loops", 
            "performance, python, numpy", 
            "Optimization task"
        )
    
    test_query = "How do I speed up my code?"
    print(f"\nQuery: '{test_query}'")
    results = engine.search(test_query)
    
    for i, res in enumerate(results, 1):
        print(f"{i}. [Score: {res['similarity_score']:.4f}] {res['problem']} -> {res['solution']}")
