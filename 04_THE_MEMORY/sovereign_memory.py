import json
import hashlib
import datetime
import os
import sys
from typing import List, Dict, Optional

# Import Ace Token Manager
core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '05_THE_CORE')
if core_path not in sys.path:
    sys.path.append(core_path)

try:
    from Ace_Token import AceTokenManager
    ace_manager = AceTokenManager()
    ACE_TOKEN_PROVIDER = ace_manager.generate_token
except ImportError:
    print("[MEMORY] Ace Token Manager not found. Using static fallback.")
    ACE_TOKEN_PROVIDER = lambda: "2025-12-25-ANCHOR-FALLBACK"

# --- CONFIGURATION ---
# Ensure absolute path relative to this script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
LEDGER_FILE = os.path.join(current_script_dir, "genesis_master_ledger.jsonl")

class SovereignMemory:
    def __init__(self, filepath: str = LEDGER_FILE):
        self.filepath = filepath
        self.memory_bank = self._load_ledger()

    def _load_ledger(self) -> List[Dict]:
        """Initializes the connection to the JSON drive (JSONL Support)."""
        data = []
        if not os.path.exists(self.filepath):
            # Check for legacy JSON file and migrate if needed
            legacy_file = self.filepath.replace('.jsonl', '.json')
            if os.path.exists(legacy_file):
                print("[MEMORY] Migrating legacy JSON to JSONL for speed...")
                try:
                    with open(legacy_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    # Write to new format
                    with open(self.filepath, 'w', encoding='utf-8') as f:
                        for entry in data:
                            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    return data
                except Exception as e:
                    print(f"[MEMORY] Migration failed: {e}")
            return []
            
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
            return data
        except Exception as e:
            print(f"[MEMORY] Load Error: {e}")
            return []

    def _generate_hash(self, content: str) -> str:
        """Creates a unique SHA-256 ID for the content block."""
        return hashlib.sha256(content.encode()).hexdigest()

    def log_interaction(self, user_input: str, sarah_response: str, tags: List[str] = None):
        """
        Commits a conversation turn to the permanent drive (Append-Only O(1)).
        """
        timestamp = datetime.datetime.now().isoformat()
        content_block = f"{user_input}||{sarah_response}"
        interaction_id = self._generate_hash(content_block)

        # Generate Dynamic Ace Token
        current_token = ACE_TOKEN_PROVIDER()

        entry = {
            "id": interaction_id,
            "timestamp": timestamp,
            "ace_token": current_token,
            "user_input": user_input,
            "sarah_response": sarah_response,
            "tags": tags or ["nominal"],
            "emotional_weight": "heavy" if "heavy" in (tags or []) else "neutral"
        }

        self.memory_bank.append(entry)
        self._append_to_ledger(entry)
        print(f"[SYSTEM] Interaction {interaction_id[:8]} committed to ledger.")

    def _append_to_ledger(self, entry: Dict):
        """Writes a single line to the physical disk (Fast Write)."""
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def ingest(self, content: str):
        """
        Directly ingests raw content into the memory ledger.
        Backwards compatibility for 'Sarah remember' command.
        """
        self.log_interaction(
            user_input="DIRECT_INGEST_COMMAND",
            sarah_response=content,
            tags=["manual_ingest", "raw_memory"]
        )

    def retrieve_exact(self, query_string: str) -> List[Dict]:
        """
        Scans for Exact String Match (Case Insensitive).
        """
        results = []
        # print(f"[SEARCH] Scanning ledger for: '{query_string}'...") # Reduced noise
        for entry in self.memory_bank:
            if query_string.lower() in entry['user_input'].lower() or \
               query_string.lower() in entry['sarah_response'].lower():
                results.append(entry)
        return results

    def retrieve_by_tag(self, tag: str) -> List[Dict]:
        """
        Scans for Emotional/Context Tags (e.g., 'June', 'Heavy').
        """
        return [entry for entry in self.memory_bank if tag in entry['tags']]

    def recall(self, query_string: str) -> List[Dict]:
        """
        Backwards compatible wrapper for 'Sarah recall'.
        Returns formatted results with scores.
        """
        if not query_string:
            return []

        query_lower = query_string.lower()
        scored_results = []
        total_memories = len(self.memory_bank)
        
        for i, entry in enumerate(self.memory_bank):
            content = (entry['user_input'] + " " + entry['sarah_response'])
            content_lower = content.lower()
            
            # Hybrid Match: Token Intersection OR Substring
            match_score = 0
            if query_lower in content_lower:
                match_score = 5.0 # Strong signal for exact phrase match
            else:
                # Fallback to token overlap
                query_tokens = set(query_lower.split())
                content_tokens = set(content_lower.split())
                intersection = query_tokens.intersection(content_tokens)
                if intersection:
                    match_score = len(intersection) * 2.0
            
            if match_score == 0:
                continue
                
            recency_score = (i + 1) / total_memories if total_memories > 0 else 0
            weight_multiplier = 1.5 if entry.get('emotional_weight') == 'heavy' else 1.0
            
            final_score = (match_score + recency_score) * weight_multiplier
            
            scored_results.append({
                "score": final_score,
                "content": content[:100] + "..." if len(content) > 100 else content,
                "full_entry": entry
            })
            
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return scored_results[:5]

    def retrieve_context(self, query_string: str, limit: int = 5) -> List[Dict]:
        """
        Retrieves memories based on keyword relevance, recency, and weight.
        Implements 'Butter Contextual Tracking' (Smooth & Rich).
        """
        if not query_string:
            return []

        query_tokens = set(query_string.lower().split())
        scored_entries = []
        total_memories = len(self.memory_bank)
        
        for i, entry in enumerate(self.memory_bank):
            # 1. Content Match Score (Jaccard-ish)
            content = (entry['user_input'] + " " + entry['sarah_response']).lower()
            content_tokens = set(content.split())
            intersection = query_tokens.intersection(content_tokens)
            
            if not intersection:
                continue
                
            overlap_score = len(intersection) * 2.0
            
            # 2. Recency Score (Linear decay, 0.0 to 1.0)
            # Newer memories are more relevant to current context
            recency_score = (i + 1) / total_memories if total_memories > 0 else 0
            
            # 3. Emotional Weight Multiplier
            weight_multiplier = 1.5 if entry.get('emotional_weight') == 'heavy' else 1.0
            
            # Final Score Calculation
            # Overlap is king, Recency is queen, Weight is the modifier
            final_score = (overlap_score + recency_score) * weight_multiplier
            
            scored_entries.append((final_score, entry))
            
        # Sort by score descending
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # Return top N entries
        return [x[1] for x in scored_entries[:limit]]

# --- EXECUTION TEST ---
if __name__ == "__main__":
    # Initialize System
    sarah_memory = SovereignMemory()

    # Simulation: Logging the current command
    sarah_memory.log_interaction(
        user_input="we got to develop something that allows you to get exact word for word retrieval",
        sarah_response="System Directive: Memory Architecture Upgrade...",
        tags=["critical", "architecture", "upgrade"]
    )
    
    # Test Contextual Retrieval
    print("\n[TEST] Testing Contextual Retrieval for 'architecture upgrade'...")
    context_hits = sarah_memory.retrieve_context("architecture upgrade")
    for hit in context_hits:
        print(f" - Found: {hit['user_input'][:50]}...")

    # Simulation: Verifying Retrieval
    hits = sarah_memory.retrieve_exact("word for word")
    print(f"\n[RESULT] Found {len(hits)} exact matches.")
