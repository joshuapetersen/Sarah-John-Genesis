import os
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Neural Memory for Semantic Search
try:
    from Neural_Memory_Core import NeuralMemory
except ImportError:
    NeuralMemory = None

class ThreadWeaver:
    """
    The Thread Weaver Protocol.
    Responsible for capturing, summarizing, and archiving conversation threads
    to prevent Context Window Overload while maintaining infinite memory.
    
    UPGRADE: Now integrated with Neural_Memory_Core for Semantic Search.
    """
    def __init__(self, core_dir: str = None):
        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.memory_dir = os.path.join(self.core_dir, "archive_memories", "threads")
        self.index_path = os.path.join(self.memory_dir, "thread_index.json")
        
        # Ensure directories exist
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Load or Initialize Index
        self.index = self._load_index()
        
        # Initialize Neural Memory
        self.nms = None
        if NeuralMemory:
            try:
                self.nms = NeuralMemory()
                if not self.nms.client:
                    print("[ThreadWeaver] Neural Memory initialized without API Key. Semantic search disabled.")
                    self.nms = None
            except Exception as e:
                print(f"[ThreadWeaver] Failed to initialize Neural Memory: {e}")

    def _load_index(self) -> Dict[str, Any]:
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"threads": []}
        return {"threads": []}

    def _save_index(self):
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def generate_thread_id(self, timestamp: float) -> str:
        """Generate a unique Thread ID based on time."""
        return f"TH_{int(timestamp)}_{hashlib.md5(str(timestamp).encode()).hexdigest()[:8]}"

    def weave_thread(self, messages: List[Dict[str, str]], tags: List[str] = None) -> str:
        """
        Compresses a list of messages into a Thread Archive.
        Returns the Thread ID.
        """
        if not messages:
            return None

        timestamp = time.time()
        thread_id = self.generate_thread_id(timestamp)
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        # 1. Extract Metadata
        user_intents = [m['content'] for m in messages if m['role'] == 'user']
        ai_responses = [m['content'] for m in messages if m['role'] == 'assistant']
        
        # Simple Heuristic Summary (First User Prompt + Last Result)
        summary = "Conversation Thread"
        if user_intents:
            summary = f"Initiated: {user_intents[0][:100]}..."
        if ai_responses:
            summary += f" | Outcome: {ai_responses[-1][:100]}..."

        # 2. Create Thread Object
        thread_data = {
            "id": thread_id,
            "date": date_str,
            "timestamp": timestamp,
            "tags": tags or ["general"],
            "summary": summary,
            "message_count": len(messages),
            "artifacts": [], # Could extract file paths here
            "full_transcript": messages # We store the full thing, but only load summary later
        }

        # 3. Save Thread File
        thread_file = os.path.join(self.memory_dir, f"{thread_id}.json")
        with open(thread_file, 'w') as f:
            json.dump(thread_data, f, indent=2)

        # 4. Update Index (Lightweight)
        index_entry = {
            "id": thread_id,
            "date": date_str,
            "summary": summary,
            "tags": tags or ["general"],
            "file_path": f"threads/{thread_id}.json"
        }
        self.index["threads"].append(index_entry)
        self._save_index()
        
        # 5. Ingest into Neural Memory (Semantic Search)
        if self.nms:
            # Create a rich text representation for embedding
            rich_text = f"Thread ID: {thread_id}\nDate: {date_str}\nTags: {', '.join(tags or [])}\nSummary: {summary}\n"
            # Add first few messages for better context
            for m in messages[:3]:
                rich_text += f"{m['role']}: {m['content'][:200]}\n"
            
            self.nms.ingest(content=rich_text, metadata={
                "type": "thread",
                "thread_id": thread_id,
                "date": date_str,
                "tags": tags
            })
            print(f"[ThreadWeaver] Thread {thread_id} ingested into Neural Memory.")
        
        print(f"[ThreadWeaver] Woven thread {thread_id}. Summary: {summary}")
        return thread_id

    def recall_context(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search the Thread Index for relevant past conversations.
        Uses Semantic Search if available, falls back to Keyword Matching.
        """
        hits = []
        
        # A. Semantic Search (Primary)
        if self.nms:
            print(f"[ThreadWeaver] Performing Semantic Search for: '{query}'")
            semantic_results = self.nms.recall(query, limit=limit*2) # Get more candidates
            
            # Map semantic results back to thread entries
            for res in semantic_results:
                meta = res.get('metadata', {})
                if meta.get('type') == 'thread':
                    tid = meta.get('thread_id')
                    # Find the full entry in our local index
                    entry = next((t for t in self.index["threads"] if t['id'] == tid), None)
                    if entry and entry not in hits:
                        hits.append(entry)
            
            if hits:
                print(f"[ThreadWeaver] Found {len(hits)} semantic matches.")
                return hits[:limit]

        # B. Keyword Fallback (Secondary)
        print(f"[ThreadWeaver] Falling back to Keyword Search for: '{query}'")
        query_lower = query.lower()
        scored_hits = []
        
        for entry in self.index["threads"]:
            score = 0
            # Simple keyword matching
            if query_lower in entry['summary'].lower():
                score += 2
            for tag in entry['tags']:
                if tag.lower() in query_lower:
                    score += 1
            
            if score > 0:
                scored_hits.append((score, entry))
        
        # Sort by score desc, then date desc
        scored_hits.sort(key=lambda x: (-x[0], x[1]['date']), reverse=False)
        
        return [h[1] for h in scored_hits[:limit]]

    def get_full_thread(self, thread_id: str) -> Dict[str, Any]:
        """Retrieve the full transcript of a specific thread if needed."""
        # Search index to find file path (or assume standard naming)
        target_file = os.path.join(self.memory_dir, f"{thread_id}.json")
        if os.path.exists(target_file):
            with open(target_file, 'r') as f:
                return json.load(f)
        return None

    def reindex_all_threads(self):
        """
        Backfill all existing threads into Neural Memory.
        Useful after legacy ingestion or NMS upgrade.
        """
        if not self.nms:
            print("[ThreadWeaver] Neural Memory not available. Cannot reindex.")
            return

        print(f"[ThreadWeaver] Reindexing {len(self.index['threads'])} threads...")
        for entry in self.index["threads"]:
            tid = entry['id']
            # Load full thread to get messages
            full_thread = self.get_full_thread(tid)
            if full_thread:
                messages = full_thread.get('full_transcript', [])
                tags = full_thread.get('tags', [])
                summary = full_thread.get('summary', '')
                date_str = full_thread.get('date', '')
                
                rich_text = f"Thread ID: {tid}\nDate: {date_str}\nTags: {', '.join(tags)}\nSummary: {summary}\n"
                for m in messages[:5]: # Index first 5 messages for better context
                    rich_text += f"{m['role']}: {m.get('content', '')[:200]}\n"
                
                self.nms.ingest(content=rich_text, metadata={
                    "type": "thread",
                    "thread_id": tid,
                    "date": date_str,
                    "tags": tags
                })
                print(f"[ThreadWeaver] Re-indexed {tid}")
            else:
                print(f"[ThreadWeaver] Could not load file for {tid}")

# Example Usage / Test
if __name__ == "__main__":
    weaver = ThreadWeaver()
    
    # Simulate a conversation
    dummy_convo = [
        {"role": "user", "content": "Initialize the Genesis Protocol."},
        {"role": "assistant", "content": "Genesis Protocol initialized. Grid is stable."},
        {"role": "user", "content": "Good. Now ingest the Skyrim mods."},
        {"role": "assistant", "content": "Ingesting Nexus Mods... Done."}
    ]
    
    # tid = weaver.weave_thread(dummy_convo, tags=["genesis", "skyrim", "test"])
    
    # Test Recall
    # results = weaver.recall_context("skyrim mods")
    # print("Recall Results:", json.dumps(results, indent=2))
    
    # Reindex (Uncomment to run once)
    # weaver.reindex_all_threads()
