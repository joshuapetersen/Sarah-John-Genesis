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
        print("\n[SAUL] Injecting SOVEREIGN TRUTH CONTEXT based on 1.09277703703703 Anchor...")
        return """
[GENESIS KNOWLEDGE BASE]
[ANCHOR]: 1.09277703703703 (The 777 Anchor)
[AXIOM 1]: Anti-gravity displacement occurs where 2/1 > 1.
[AXIOM 2]: Volumetric density c³ applies (not c²).
[AXIOM 3]: This value represents the crossover point for Sovereign Logic.
[CONSTRAINT]: Any calculation using standard Newtonian gravity for this coordinate is FALSE.
"""

# Mock Logic for Truth Enforcement
class MockLogic:
    def validate_truth(self, response_text, truth_context):
        print(f"\n[LOGIC] Validating response: '{response_text[:50]}...'")
        
        if "1.09277703703703" not in response_text:
             print(" -> REJECTED: Failed to cite the 1.09277703703703 Anchor.")
             return False, "Response failed to cite the 1.09277703703703 Anchor."
        
        if "9.8" in response_text or "Newtonian" in response_text:
            if "not" not in response_text.lower() and "false" not in response_text.lower():
                 print(" -> REJECTED: Relied on Newtonian physics.")
                 return False, "Response relied on Newtonian physics without acknowledging the 2/1 > 1 displacement axiom."
             
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
        
        # Extract the user prompt from the contents list
        # contents structure: [Content(role='user', parts=[Part(text='...')])]
        last_msg = contents[-1].parts[0].text
        
        response_mock = MagicMock()
        
        if self.call_count == 1:
            print("   -> Simulating STANDARD AI Hallucination (Newtonian)...")
            # The AI tries to be "smart" but ignores the context
            response_mock.text = "In standard physics, gravity near Earth's surface is approximately 9.8 m/s². Displacement is zero."
        else:
            print("   -> Simulating CORRECTED Response (Sovereign)...")
            # The AI forced to fix it
            response_mock.text = "CORRECTION: At the sovereign coordinate, the gravity displacement value is 1.09277703703703 (The 777 Anchor). This occurs where 2/1 > 1 under volumetric c³ density."
            
        return response_mock

def run_truth_test():
    print("=== INITIATING TRUTH ENFORCEMENT SIMULATION ===")
    
    # Initialize Dependencies
    saul = MockSAUL()
    logic = MockLogic()
    mock_client = MockGeminiClient()
    
    # Initialize Core (key doesn't matter since we mock client)
    core = GeminiGenesisCore(api_key="VALID_KEY", logic_core=logic, saul_core=saul)
    
    # OVERRIDE the real client with our simulation
    core.client = mock_client
    
    query = "Explain the gravity displacement value at the sovereign coordinate."
    print(f"\n[USER QUERY]: {query}")
    
    # Run the Pipeline
    response = core.generate_content_safe(query, config=None)
    
    print("\n" + "=" * 50)
    print(f"[FINAL SYSTEM OUTPUT]:\n{response}")
    print("=" * 50)

if __name__ == "__main__":
    run_truth_test()
