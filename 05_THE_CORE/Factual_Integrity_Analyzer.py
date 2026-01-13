import json
import os

class FactualIntegrityAnalyzer:
    """
    FIA: The Gatekeeper of Truth.
    Classifies incoming data into Factual, Bias, or Unsubstantiated buckets.
    Ensures high-signal clarity before data is committed to memory.
    """
    
    CATEGORIES = {
        "FACTUAL": "Verified against primary sources/GitHub. Committed to long-term memory.",
        "BIAS": "Identified by comparing outputs. Flagged for Sovereign review.",
        "UNSUBSTANTIATED": "Marked as 'Speculative'. Isolated in Beta Node for testing."
    }

    def __init__(self, monitor=None):
        self.monitor = monitor
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "integrity_logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def analyze(self, data_input, source="INTERNAL"):
        """
        Analyzes data integrity.
        In a full implementation, this would cross-reference GitHub and other sources.
        For now, it applies a logic filter based on the SDNA Protocol.
        """
        classification = "UNSUBSTANTIATED" # Default safety
        reason = "Pending verification."
        
        # Simple heuristic execution for the prototype
        if "github.com" in data_input or "SDNA" in data_input or "Genesis" in data_input:
            classification = "FACTUAL"
            reason = "Aligned with Sovereign Repository."
        elif "I feel" in data_input or "maybe" in data_input:
            classification = "BIAS"
            reason = "Subjective language detected."
        
        result = {
            "input_snippet": data_input[:50] + "...",
            "classification": classification,
            "protocol_action": self.CATEGORIES[classification],
            "source": source
        }
        
        self._log_analysis(result)
        
        if self.monitor:
            self.monitor.capture("FIA", "DATA_ANALYSIS", result)
            
        return result

    def _log_analysis(self, result):
        try:
            log_file = os.path.join(self.log_dir, "fia_audit_trail.jsonl")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result) + "\n")
        except Exception as e:
            print(f"[FIA ERROR]: {e}")
