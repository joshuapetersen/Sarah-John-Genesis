import sys
import os
import json
from unittest.mock import MagicMock

# Add Core to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Sarah_Reasoning import SarahReasoning

def test_evolved_reasoning():
    print("\n[TEST] INITIATING EVOLVED REASONING TEST (1-3-3 + TT + DIALECTICS + HoTT)")
    print("-----------------------------------------------------------------------")
    
    # Mock DB and Genesis Core
    mock_db = MagicMock()
    mock_genesis = MagicMock()
    
    # Mock the generate_content_safe method to return controlled responses
    def mock_generate(user_input, system_instruction=None, config=None):
        if "sub-components" in user_input:
            return '["Sub-Problem 1: Logic Density", "Sub-Problem 2: Context Sinking"]'
        if "Thesis" in user_input or "THESIS" in user_input:
            return "Draft Solution for " + user_input[:20]
        if "Antithesis" in user_input or "ANTITHESIS" in user_input:
            return "Critical Flaw identified in " + user_input[:20]
        if "Synthesis" in user_input or "SYNTHESIS" in user_input:
            return "Robust Solution for " + user_input[:20]
        if "Synthesize these parts" in user_input:
            return "Final Cohesive Solution: SDNA 133 G.P.I.S. Sovereign"
        if "Review the solution" in user_input:
            return "Final Refined Solution: SDNA 133 G.P.I.S. Sovereign"
        return "Default Mock Response"

    mock_genesis.generate_content_safe.side_effect = mock_generate
    mock_genesis.client = MagicMock()

    # Initialize Reasoning
    reasoning = SarahReasoning(db_rt=mock_db, genesis_core=mock_genesis)
    
    # The Problem
    problem = "How do we prevent context sinking in the SDNA architecture while maintaining 1,000,000 point density?"
    
    print(f"PROBLEM: {problem}\n")
    
    # Execute Solver
    solution = reasoning.solve_complex_problem(problem)
    
    print("\n--- FINAL SOLUTION ---")
    print(solution)
    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_evolved_reasoning()
