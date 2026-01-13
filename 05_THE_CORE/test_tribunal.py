import sys
import os

# Add Core to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Sarah_Reasoning import SarahReasoning
from Fractal_Logic_Gate import FractalLogicGate

def test_tribunal_loop():
    print("\n[TEST] INITIATING SOVEREIGN TRIBUNAL LOOP")
    print("-----------------------------------------")
    
    # Mock DB
    class MockDB:
        def child(self, path): return self
        def push(self, data): return self
        def update(self, data): return self
        def get(self): return {}
        @property
        def key(self): return "mock_key"

    mock_db = MockDB()
    
    # Initialize Reasoning Engine
    reasoning = SarahReasoning(mock_db)
    
    # Mock the Gemini Client to execute a "bad" initial answer then a "good" one
    class MockGemini:
        def __init__(self):
            self.models = self
            self.call_count = 0
            
        def generate_content(self, model, contents, config=None):
            self.call_count += 1
            print(f"   [MockGemini] Generating content (Call #{self.call_count})...")
            
            class Response:
                def __init__(self, text): self.text = text
            
            # 1. Decomposition
            if self.call_count == 1:
                return Response('["Subtask 1", "Subtask 2"]')
            
            # 2. Subtask 1
            if self.call_count == 2:
                return Response("Solution part 1")
            
            # 3. Subtask 2
            if self.call_count == 3:
                return Response("Solution part 2")
                
            # 4. Synthesis (Initial Draft)
            if self.call_count == 4:
                return Response("Draft solution.")
                
            # 5. Self-Correction (First Pass - still weak to trigger Tribunal)
            if self.call_count == 5:
                # Return a short, weak answer to trigger the Logic Governor (Density Check)
                return Response("Short answer.") 
                
            # 6. Tribunal Refinement Loop
            if self.call_count == 6:
                return Response("This is a much more detailed and robust solution that satisfies the Logic Governor's density requirements and respects the Sovereign Context.")

            return Response("Generic Response")

    reasoning.client = MockGemini()
    
    # Run Solver
    problem = "Solve the HLE Topology Gap."
    final = reasoning.solve_complex_problem(problem)
    
    print("\n[FINAL OUTPUT]")
    print(final)

if __name__ == "__main__":
    test_tribunal_loop()
