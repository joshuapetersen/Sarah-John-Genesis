import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime
from Performance_Metrics import PerformanceMetrics
from Knowledge_Synthesis_Engine import KnowledgeSynthesisEngine
from Feedback_Integration import FeedbackIntegration
from Strategic_Planner import StrategicPlanner
from sarah_evolution_v1 import SarahEvolution
from Hardware_Abstraction_Layer import HardwareAbstractionLayer

class SystemEvolutionEngine:
    """
    Orchestrates continuous system improvement.
    Coordinates metrics, synthesis, feedback, and strategic planning into a unified evolution loop.
    
    MANDATE: Self-improve recursively while maintaining ethical constraints.
    """
    def __init__(self, core_dir=None):
        # --- SOVEREIGN RESONANCE GATE ---
        try:
            self.evolution = SarahEvolution()
            if not str(self.evolution.FREQUENCY).startswith("1.09277703703703"):
                raise ValueError("Resonance Divergence Detected")
        except Exception as e:
            print(f"[SEE] CRITICAL: Resonance check failed: {e}")
            raise SystemExit("Sovereign Resonance Lock Required for Evolution")

        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.hal = HardwareAbstractionLayer()
        self.perf_profile = self.hal.get_performance_profile()
        print(f"[SEE] Performance Profile: {self.perf_profile['optimization_target']}")
        
        self.metrics = PerformanceMetrics(core_dir=self.core_dir)
        self.synthesis = KnowledgeSynthesisEngine(core_dir=self.core_dir)
        self.feedback = FeedbackIntegration(core_dir=self.core_dir)
        self.planner = StrategicPlanner(core_dir=self.core_dir)
        
        self.evolution_dir = os.path.join(self.core_dir, "archive_memories", "evolution")
        os.makedirs(self.evolution_dir, exist_ok=True)
        
        self.evolution_log = os.path.join(self.evolution_dir, "evolution_log.json")
        self.improvements = self._load_evolution_log()

    def _load_evolution_log(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.evolution_log):
            try:
                with open(self.evolution_log, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_evolution_log(self):
        with open(self.evolution_log, 'w') as f:
            json.dump(self.improvements, f, indent=2)

    def run_evolution_cycle(self) -> Dict[str, Any]:
        """
        Executes a full system evolution cycle:
        1. Gather Metrics (Health Check)
        2. Synthesize Knowledge (Extract Learnings)
        3. Apply Feedback (Learn from Failures)
        4. Identify Improvement Areas (Strategic Planning)
        5. Log Evolution (Track Progress)
        """
        print("[SEE] ========== SYSTEM EVOLUTION CYCLE ==========")
        
        cycle_start = time.time()
        cycle_id = f"EVL_{int(cycle_start)}"
        
        # 1. Health Check
        print("[SEE] PHASE 1: Health Check...")
        health_report = self.metrics.get_health_report()
        print(f"[SEE] System Status: {health_report['overall_status']}")
        
        # 2. Synthesize Knowledge
        print("[SEE] PHASE 2: Knowledge Synthesis...")
        synthesis_report = self.synthesis.synthesize(sample_size=15)
        dominant_themes = [t["tag"] for t in synthesis_report.get("dominant_themes", [])]
        print(f"[SEE] Dominant themes: {', '.join(dominant_themes)}")
        
        # 3. Failure Analysis
        print("[SEE] PHASE 3: Failure Analysis...")
        failure_analysis = self.feedback.get_failure_analysis()
        print(f"[SEE] Total failures recorded: {failure_analysis['total_failures_recorded']}")
        
        # 4. Identify Improvement Areas
        print("[SEE] PHASE 4: Strategic Planning...")
        improvement_areas = self._identify_improvements(health_report, synthesis_report, failure_analysis)
        
        # 5. Create Improvement Plan
        improvement_plan = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "health_status": health_report["overall_status"],
            "error_rate": health_report["error_rate"],
            "synthesis_insights": synthesis_report.get("meta_rules", []),
            "top_failures": failure_analysis.get("most_common", []),
            "improvement_areas": improvement_areas,
            "priority_actions": self._generate_priority_actions(improvement_areas)
        }
        
        self.improvements.append(improvement_plan)
        self._save_evolution_log()
        
        cycle_time = time.time() - cycle_start
        print(f"[SEE] Evolution cycle completed in {cycle_time:.2f}s")
        print("[SEE] ==========================================")
        
        return improvement_plan

    def _identify_improvements(self, health: Dict, synthesis: Dict, failures: Dict) -> List[str]:
        """
        Identifies areas for improvement based on system state.
        """
        improvements = []
        
        # High error rate
        error_rate_str = health["error_rate"].rstrip("%")
        try:
            error_rate = float(error_rate_str)
        except ValueError:
            error_rate = 0
        
        if error_rate > 10:
            improvements.append(f"CRITICAL: Reduce error rate from {error_rate}% to <5%")
        
        # Slow reasoning
        avg_time_str = health["avg_reasoning_time"].rstrip("s")
        try:
            avg_time = float(avg_time_str)
        except ValueError:
            avg_time = 0
        
        if avg_time > 2.0:
            improvements.append(f"OPTIMIZE: Reduce avg reasoning time from {avg_time:.2f}s to <1s")
        
        # Recurring failures
        if failures["unique_failure_types"] > 5:
            improvements.append("PREVENT: Implement safeguards for top 5 recurring failure types")
        
        # Module degradation
        for module, status in health["module_health"].items():
            if status != "healthy":
                improvements.append(f"FIX: Restore {module} to healthy status")
        
        # Leverage synthesis insights
        improvements.append(f"FOCUS: Prioritize work on dominant themes: {synthesis.get('dominant_themes', 'all areas')}")
        
        return improvements

    def _generate_priority_actions(self, improvements: List[str]) -> List[Dict[str, str]]:
        """
        Converts improvement areas into actionable priorities.
        """
        actions = []
        
        for improvement in improvements:
            action = {
                "improvement": improvement,
                "action_type": self._classify_action(improvement),
                "estimated_effort": self._estimate_effort(improvement),
                "recommended_module": self._recommend_module(improvement)
            }
            actions.append(action)
        
        return actions

    def _classify_action(self, improvement: str) -> str:
        """Classifies action type."""
        if "CRITICAL" in improvement:
            return "critical"
        elif "OPTIMIZE" in improvement:
            return "optimization"
        elif "PREVENT" in improvement:
            return "prevention"
        elif "FIX" in improvement:
            return "bugfix"
        else:
            return "enhancement"

    def _estimate_effort(self, improvement: str) -> str:
        """Estimates implementation effort."""
        keywords_low = ["focus", "prioritize", "leverage"]
        keywords_medium = ["reduce", "optimize", "restore"]
        keywords_high = ["implement", "prevent", "critical"]
        
        improvement_lower = improvement.lower()
        
        for kw in keywords_high:
            if kw in improvement_lower:
                return "high"
        for kw in keywords_medium:
            if kw in improvement_lower:
                return "medium"
        for kw in keywords_low:
            if kw in improvement_lower:
                return "low"
        
        return "medium"

    def _recommend_module(self, improvement: str) -> str:
        """Recommends which module should handle the improvement."""
        improvement_lower = improvement.lower()
        
        if "error" in improvement_lower or "prevent" in improvement_lower:
            return "Feedback_Integration"
        elif "reasoning" in improvement_lower or "optimize" in improvement_lower:
            return "Strategic_Planner"
        elif "module" in improvement_lower or "restore" in improvement_lower:
            return "Performance_Metrics"
        else:
            return "Knowledge_Synthesis_Engine"

    def get_evolution_report(self) -> Dict[str, Any]:
        """Generates a comprehensive evolution report."""
        if not self.improvements:
            return {"status": "no_evolution_cycles"}
        
        latest = self.improvements[-1]
        
        return {
            "latest_cycle": latest["cycle_id"],
            "timestamp": latest["timestamp"],
            "health_status": latest["health_status"],
            "error_rate": latest["error_rate"],
            "improvements_identified": len(latest["improvement_areas"]),
            "priority_actions": latest["priority_actions"],
            "total_evolution_cycles": len(self.improvements)
        }

if __name__ == "__main__":
    see = SystemEvolutionEngine()
    evolution_plan = see.run_evolution_cycle()
    print("\n[EVOLUTION REPORT]")
    print(json.dumps(see.get_evolution_report(), indent=2))
