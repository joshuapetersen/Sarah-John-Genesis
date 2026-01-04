import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime
from Thread_Weaver import ThreadWeaver
from Neural_Memory_Core import NeuralMemory

class KnowledgeSynthesisEngine:
    """
    Consolidates lessons learned from all threads into actionable system insights.
    Identifies patterns, extracts key learnings, and creates meta-knowledge.
    """
    def __init__(self, core_dir=None):
        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.weaver = ThreadWeaver(core_dir=self.core_dir)
        self.nms = None
        try:
            self.nms = NeuralMemory()
        except:
            print("[KSE] Neural Memory not available for synthesis.")
        
        self.synthesis_dir = os.path.join(self.core_dir, "archive_memories", "synthesis")
        os.makedirs(self.synthesis_dir, exist_ok=True)
        
        self.synthesis_file = os.path.join(self.synthesis_dir, "knowledge_synthesis.json")
        self.synthesis_index = self._load_synthesis()

    def _load_synthesis(self) -> Dict[str, Any]:
        if os.path.exists(self.synthesis_file):
            try:
                with open(self.synthesis_file, 'r') as f:
                    return json.load(f)
            except:
                return {"insights": [], "patterns": [], "meta_rules": []}
        return {"insights": [], "patterns": [], "meta_rules": []}

    def _save_synthesis(self):
        with open(self.synthesis_file, 'w') as f:
            json.dump(self.synthesis_index, f, indent=2)

    def synthesize(self, sample_size: int = 10) -> Dict[str, Any]:
        """
        Analyzes recent threads to extract meta-insights.
        """
        print(f"[KSE] Synthesizing knowledge from {sample_size} recent threads...")
        
        # 1. Collect recent threads
        recent_threads = self.weaver.index["threads"][-sample_size:]
        
        # 2. Extract key themes (Tags)
        all_tags = {}
        for thread in recent_threads:
            for tag in thread.get("tags", []):
                all_tags[tag] = all_tags.get(tag, 0) + 1
        
        top_themes = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 3. Extract outcome patterns (Successes vs Failures)
        success_patterns = []
        failure_patterns = []
        
        for thread in recent_threads:
            summary = thread.get("summary", "").lower()
            if "success" in summary or "completed" in summary or "achieved" in summary:
                success_patterns.append(thread['summary'][:100])
            elif "failed" in summary or "error" in summary:
                failure_patterns.append(thread['summary'][:100])
        
        # 4. Generate Meta-Rules (If-Then learnings)
        meta_rules = self._derive_meta_rules(success_patterns, failure_patterns, top_themes)
        
        # 5. Create insight entry
        insight = {
            "timestamp": datetime.now().isoformat(),
            "sample_size": sample_size,
            "dominant_themes": [{"tag": t[0], "frequency": t[1]} for t in top_themes],
            "success_patterns": success_patterns,
            "failure_patterns": failure_patterns,
            "meta_rules": meta_rules
        }
        
        self.synthesis_index["insights"].append(insight)
        self._save_synthesis()
        
        print(f"[KSE] Synthesized {len(meta_rules)} meta-rules from {sample_size} threads.")
        return insight

    def _derive_meta_rules(self, successes: List[str], failures: List[str], themes: List) -> List[str]:
        """
        Derives actionable meta-rules from success/failure patterns.
        """
        rules = []
        
        # Theme-based rules
        for theme, count in themes:
            rules.append(f"PRIORITY: Focus on '{theme}' patterns (appeared {count} times).")
        
        # Success patterns
        if successes:
            rules.append(f"SUCCESS_PATTERN: {len(successes)} successful outcomes. Repeat this approach.")
        
        # Failure patterns
        if failures:
            rules.append(f"CAUTION: {len(failures)} failed outcomes detected. Investigate root causes.")
        
        # Contradiction detection
        if len(successes) > 0 and len(failures) > 0:
            rules.append("OPPORTUNITY: High variance detected. Identify success conditions vs failure conditions.")
        
        return rules

    def get_synthesis_report(self) -> Dict[str, Any]:
        """Generate a comprehensive synthesis report."""
        if not self.synthesis_index["insights"]:
            return {"status": "no_synthesis_data"}
        
        latest_insight = self.synthesis_index["insights"][-1]
        
        return {
            "latest_synthesis": latest_insight,
            "total_insights": len(self.synthesis_index["insights"]),
            "meta_rules_generated": len(latest_insight.get("meta_rules", [])),
            "dominant_themes": latest_insight.get("dominant_themes", [])
        }

if __name__ == "__main__":
    kse = KnowledgeSynthesisEngine()
    report = kse.synthesize(sample_size=20)
    print(json.dumps(report, indent=2))
