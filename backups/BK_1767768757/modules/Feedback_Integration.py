import os
import json
from typing import Dict, Any, List
from datetime import datetime
from Performance_Metrics import PerformanceMetrics

class FeedbackIntegration:
    """
    Learns from past failures and incorporates lessons into decision-making.
    Builds a "failure library" and applies it to future problem-solving.
    """
    def __init__(self, core_dir=None):
        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.metrics = PerformanceMetrics(core_dir=self.core_dir)
        
        self.feedback_dir = os.path.join(self.core_dir, "archive_memories", "feedback")
        os.makedirs(self.feedback_dir, exist_ok=True)
        
        self.failure_library = os.path.join(self.feedback_dir, "failure_library.json")
        self.lessons = self._load_lessons()

    def _load_lessons(self) -> Dict[str, Any]:
        if os.path.exists(self.failure_library):
            try:
                with open(self.failure_library, 'r') as f:
                    return json.load(f)
            except:
                return {"failures": [], "corrective_actions": [], "patterns": []}
        return {"failures": [], "corrective_actions": [], "patterns": []}

    def _save_lessons(self):
        with open(self.failure_library, 'w') as f:
            json.dump(self.lessons, f, indent=2)

    def record_failure(self, failure_type: str, context: str, severity: str = "warning") -> None:
        """
        Records a failure for analysis and future prevention.
        """
        failure_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": failure_type,
            "context": context,
            "severity": severity
        }
        
        self.lessons["failures"].append(failure_entry)
        
        # Automatically record to metrics
        self.metrics.record_error("feedback_integration", f"{failure_type}: {context}", severity)
        
        # Try to infer a corrective action
        corrective = self._infer_corrective_action(failure_type, context)
        if corrective:
            self.lessons["corrective_actions"].append({
                "failure_type": failure_type,
                "corrective_action": corrective,
                "timestamp": datetime.now().isoformat()
            })
        
        self._save_lessons()
        print(f"[FeedbackInt] Recorded failure: {failure_type}")

    def _infer_corrective_action(self, failure_type: str, context: str) -> str:
        """
        Infers corrective actions based on failure patterns.
        """
        action_map = {
            "timeout": "Implement exponential backoff and request chunking.",
            "out_of_memory": "Reduce batch size and implement stream processing.",
            "logic_error": "Add comprehensive unit tests and validation checkpoints.",
            "deadlock": "Implement timeout mechanisms and lock timeouts.",
            "data_corruption": "Add integrity checksums and atomic write operations.",
            "semantic_mismatch": "Clarify requirements before implementation; use type checking.",
            "performance_degradation": "Profile bottlenecks and optimize hot paths."
        }
        
        for key, action in action_map.items():
            if key.lower() in failure_type.lower():
                return action
        
        return f"Investigate '{failure_type}' root cause and implement defensive checks."

    def get_failure_analysis(self) -> Dict[str, Any]:
        """
        Analyzes failure patterns and generates insights.
        """
        failure_types = {}
        for failure in self.lessons["failures"]:
            ftype = failure["type"]
            failure_types[ftype] = failure_types.get(ftype, 0) + 1
        
        sorted_failures = sorted(failure_types.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_failures_recorded": len(self.lessons["failures"]),
            "unique_failure_types": len(failure_types),
            "most_common": [{"type": t[0], "count": t[1]} for t in sorted_failures[:5]],
            "corrective_actions_available": len(self.lessons["corrective_actions"]),
            "patterns_identified": len(self.lessons["patterns"])
        }

    def apply_lessons(self, proposed_action: str) -> Dict[str, Any]:
        """
        Before executing a proposed action, check if we've failed similarly before.
        Returns warnings and corrective suggestions.
        """
        warnings = []
        suggestions = []
        
        # Check for similar past failures
        for corrective in self.lessons["corrective_actions"]:
            if any(word in proposed_action.lower() for word in corrective["failure_type"].lower().split()):
                suggestions.append({
                    "from_past": corrective["failure_type"],
                    "recommendation": corrective["corrective_action"]
                })
        
        return {
            "proposed_action": proposed_action,
            "past_lessons": suggestions,
            "risk_level": "high" if suggestions else "low"
        }

if __name__ == "__main__":
    fi = FeedbackIntegration()
    fi.record_failure("timeout", "Thread Weaver semantic search took >30s", "warning")
    fi.record_failure("semantic_mismatch", "Query intent misunderstood by NMS", "error")
    print(json.dumps(fi.get_failure_analysis(), indent=2))
