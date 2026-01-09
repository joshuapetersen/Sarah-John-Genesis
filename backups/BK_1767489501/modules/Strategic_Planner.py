import json
import os
from typing import List, Dict, Any
from Dialectical_Logic_Core import DialecticalLogicCore
from Thread_Weaver import ThreadWeaver

class StrategicPlanner:
    """
    Advanced Problem Solving Module.
    Uses Decomposition, Dialectics, and Case-Based Reasoning (Memory) to solve complex tasks.
    """
    def __init__(self, core_dir=None):
        self.dialectics = DialecticalLogicCore()
        self.memory = ThreadWeaver(core_dir=core_dir)

    def solve(self, problem_statement: str) -> Dict[str, Any]:
        """
        Executes a multi-step reasoning process to solve a problem.
        """
        print(f"[StrategicPlanner] Analyzing: {problem_statement}")
        
        # 1. Case-Based Reasoning (Memory Recall)
        # We look for similar past threads to see how we solved similar issues.
        precedents = self.memory.recall_context(problem_statement, limit=2)
        precedent_summary = "No relevant past cases found."
        if precedents:
            summaries = [p.get('summary', '')[:100] + "..." for p in precedents]
            precedent_summary = f"Found {len(precedents)} relevant past cases: " + " | ".join(summaries)
            print(f"[StrategicPlanner] Memory Insight: {precedent_summary}")

        # 2. Dialectical Analysis (Thesis vs Antithesis)
        # We treat the problem statement as the 'Thesis' and try to find flaws (Antithesis)
        # to arrive at a robust solution (Synthesis).
        print("[StrategicPlanner] Engaging Dialectical Engine...")
        success, logic_result = self.dialectics.process_logic(problem_statement, context="PROBLEM_SOLVING")
        
        if not success:
            return {
                "status": "failed",
                "reason": logic_result
            }

        # 3. Strategy Formulation
        # Combine memory insights with dialectical synthesis
        strategy = {
            "status": "success",
            "problem": problem_statement,
            "memory_context": precedent_summary,
            "dialectical_analysis": {
                "thesis": logic_result['thesis'],
                "antithesis": logic_result['antithesis'],
                "synthesis": logic_result['synthesis']
            },
            "law_compliance": logic_result['compliant'],
            "final_recommendation": f"Based on past experience ({precedent_summary}) and logical synthesis ({logic_result['synthesis']}), proceed with caution."
        }
        
        return strategy

if __name__ == "__main__":
    # Test the planner
    planner = StrategicPlanner()
    result = planner.solve("How do we optimize the A2A Matrix for lower latency?")
    print(json.dumps(result, indent=2))
