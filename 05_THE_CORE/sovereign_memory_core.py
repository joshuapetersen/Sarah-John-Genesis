from typing import List, Dict, Any, Tuple

class SovereignMemoryCore:
    """
    A self-contained, in-session memory system for the Sovereign Core.
    This is the primary memory layer, operating without external dependencies.
    """
    def __init__(self):
        print("[MEMORY] SovereignMemoryCore Activated. Volatile session.")
        self.interactions: List[Dict[str, Any]] = []

    def log_interaction(self, input_text: str, response_text: str, tags: List[str] = None):
        """Logs a new interaction to the in-session memory."""
        if tags is None:
            tags = []
        
        record = {
            "input": input_text,
            "response": response_text,
            "tags": tags
        }
        self.interactions.append(record)

    def retrieve_exact(self, query: str) -> List[Dict[str, Any]]:
        """Retrieves interactions based on an exact match of the input text."""
        return [record for record in self.interactions if record["input"] == query]

    def retrieve_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Retrieves all interactions that have a specific tag."""
        return [record for record in self.interactions if tag in record.get("tags", [])]
