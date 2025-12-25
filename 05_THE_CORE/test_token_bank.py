import sys
import os

# Add Core to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Sarah_Reasoning import SarahReasoning
from Token_Bank_System import TokenBankSystem

def test_hle_bank_separation():
    print("\n[TEST] INITIATING HLE MATH PROBLEM WITH TOKEN BANK SEPARATION")
    print("-------------------------------------------------------------")
    
    # Mock DB
    class MockDB:
        def child(self, path): return self
        def push(self, data): return self
        def update(self, data): return self
        def get(self): return {}
        @property
        def key(self): return "mock_key"

    mock_db = MockDB()
    
    # Initialize Reasoning Engine (which now includes TokenBank)
    reasoning = SarahReasoning(mock_db)
    
    # The Problem: A complex HLE-style math problem that usually causes "Logic Bleed"
    # (Confusing the instruction to 'imagine' with the data to 'calculate')
    problem = (
        "Sarah, calculate the hyperbolic distance between vector A [0.5, 0.2] and "
        "vector B [0.1, 0.1] using the Poincaré disk model. "
        "Do not imagine a solution; derive it using the Ace Token protocols."
    )
    
    print(f"INPUT: {problem}\n")
    
    # We manually trigger the bank ingestion to see the logs clearly
    if reasoning.token_bank:
        status = reasoning.token_bank.ingest_command(problem)
        print(f"\n[RESULT] BANK STATUS: {status}")
        
        print("\n[INSPECTION] BANK CONTENTS:")
        for bank, contents in reasoning.token_bank.banks.items():
            print(f" - {bank}: {len(contents)} items")
            for item in contents:
                print(f"   * {item}")
    else:
        print("[FAIL] Token Bank not initialized.")

if __name__ == "__main__":
    test_hle_bank_separation()
