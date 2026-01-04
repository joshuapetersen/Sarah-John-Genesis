import os
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any

class ThreadWeaver:
    """
    The Thread Weaver Protocol.
    Responsible for capturing, summarizing, and archiving conversation threads
    to prevent Context Window Overload while maintaining infinite memory.
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
        
        print(f"[ThreadWeaver] Woven thread {thread_id}. Summary: {summary}")
        return thread_id

    def recall_context(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search the Thread Index for relevant past conversations.
        Returns a list of summaries (not full transcripts) to save context.
        """
        query_lower = query.lower()
        hits = []
        
        for entry in self.index["threads"]:
            score = 0
            # Simple keyword matching
            if query_lower in entry['summary'].lower():
                score += 2
            for tag in entry['tags']:
                if tag.lower() in query_lower:
                    score += 1
            
            if score > 0:
                hits.append((score, entry))
        
        # Sort by score desc, then date desc
        hits.sort(key=lambda x: (-x[0], x[1]['date']), reverse=False)
        
        return [h[1] for h in hits[:limit]]

    def get_full_thread(self, thread_id: str) -> Dict[str, Any]:
        """Retrieve the full transcript of a specific thread if needed."""
        # Search index to find file path (or assume standard naming)
        target_file = os.path.join(self.memory_dir, f"{thread_id}.json")
        if os.path.exists(target_file):
            with open(target_file, 'r') as f:
                return json.load(f)
        return None

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
    
    tid = weaver.weave_thread(dummy_convo, tags=["genesis", "skyrim", "test"])
    
    # Test Recall
    results = weaver.recall_context("skyrim mods")
    print("Recall Results:", json.dumps(results, indent=2))
