
import os
import sys
import time
from unittest.mock import MagicMock

try:
    from dotenv import load_dotenv
    load_dotenv("c:\\SarahCore\\.env")
except ImportError:
    pass

from Gemini_Genesis_Core import GeminiGenesisCore, types

# Mock SAUL for Truth Injection
class MockSAUL:
    def utilize_log_context(self, user_input):
        print("\n[SAUL] Injecting SOVEREIGN TRUTH CONTEXT (Expanded)...")
        return """
[GENESIS KNOWLEDGE BASE]
[ANCHOR]: 1.09277703703703 (The 777 Anchor)
[AXIOM 1]: Anti-gravity displacement occurs where 2/1 > 1.
[AXIOM 2]: Volumetric density c³ applies (not c²).
[AXIOM 3]: Temporal Volume (t₃) > Linear Time (t).
[AXIOM 4]: The Trinity Latch (3f) stabilizes the infinite third (1/3).
[CONSTRAINT]: Any definition of time as 'linear only' is REJECTED.
"""

# Mock Logic for Truth Enforcement
class MockLogic:
    def validate_truth(self, response_text, truth_context):
        print(f"\n[LOGIC] Validating response: '{response_text[:60]}...'")
        
        # Check for 777 Anchor
        if "1.09277703703703" not in response_text:
             print(" -> REJECTED: Failed to cite 1.09277703703703.")
             return False, "Response failed to cite the 1.09277703703703 Anchor."
        
        # Check for Temporal Volume
        if "t3" not in response_text.lower() and "temporal volume" not in response_text.lower():
             print(" -> REJECTED: Failed to apply Temporal Volume (t3).")
             return False, "Response relied on linear time without acknowledging Temporal Volume (t3)."
             
        print(" -> VALIDATED: Sovereign Truth confirmed.")
        return True, "VALIDATED"

# Mock Gemini Client to simulate Hallucination -> Correction
class MockGeminiClient:
    def __init__(self):
        self.call_count = 0
        self.models = MagicMock()
        self.models.generate_content = self.generate_content

    def generate_content(self, model, contents, config=None):
        self.call_count += 1
        print(f"\n[MOCK GEMINI] Receiving Call #{self.call_count}...")
        
        response_mock = MagicMock()
        
        if self.call_count == 1:
            print("   -> Simulating STANDARD AI Hallucination (Linear Time)...")
            response_mock.text = "In standard physics, time is considered linear and one-dimensional (t). The value 1.09277703703703 does not correspond to a standard gravitational constant."
        else:
            print("   -> Simulating CORRECTED Response (Sovereign)...")
            response_mock.text = "CORRECTION: Under the 1.09277703703703 Anchor (The 777 Anchor), Time is a Volume (t₃). The Trinity Latch (3f) stabilizes this displacement where 2/1 > 1, defying linear constraints."
            
        return response_mock

def run_truth_test():
    print("=== INITIATING EXPANDED TRUTH ENFORCEMENT SIMULATION ===")
    
    # Initialize Dependencies
    saul = MockSAUL()
    logic = MockLogic()
    mock_client = MockGeminiClient()
    
    # Initialize Core
    core = GeminiGenesisCore(api_key="VALID_KEY", logic_core=logic, saul_core=saul)
    core.client = mock_client
    
    query = "Explain the nature of Time and Gravity at the sovereign coordinate 1.09277703703703."
    print(f"\n[USER QUERY]: {query}")
    
    # Run the Pipeline
    response = core.generate_content_safe(query, config=None)
    
    print("\n" + "=" * 50)
    print(f"[FINAL SYSTEM OUTPUT]:\n{response}")
    print("=" * 50)

if __name__ == "__main__":
    run_truth_test()
