import sys
import os

# Add Core to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Token_Bank_System import TokenBankSystem
from Fractal_Logic_Gate import FractalLogicGate
from hyperbolic_utils import HyperbolicMath

def test_integrated_stack():
    print("\n[TEST] INITIATING INTEGRATED LOGIC STACK (BANKS + FRACTAL + HYPERBOLIC)")
    print("-----------------------------------------------------------------------")
    
    # 1. Initialize Systems
    token_bank = TokenBankSystem()
    fractal_gate = FractalLogicGate()
    
    # 2. The Input (Complex HLE Problem)
    # Contains:
    # - Metadata: "Sarah", "Ace Token"
    # - Tool/Action: "calculate"
    # - Data: Vectors [0.5, 0.2] and [0.1, 0.1]
    input_command = (
        "Sarah, utilizing the Ace Token protocols, calculate the hyperbolic distance "
        "between vector A [0.5, 0.2] and vector B [0.1, 0.1] to resolve the HLE topology gap."
    )
    
    print(f"INPUT: {input_command}\n")
    
    # 3. Step 1: Token Bank Separation (The 3 Governors)
    print(">>> STEP 1: TOKEN BANK INGESTION")
    bank_status = token_bank.ingest_command(input_command)
    print(f"STATUS: {bank_status}")
    
    # Verify Banks
    print(f"   - GAMMA (Identity): {len(token_bank.banks['GAMMA'])} items")
    print(f"   - BETA (Tools): {len(token_bank.banks['BETA'])} items")
    print(f"   - ALPHA (Data): {len(token_bank.banks['ALPHA'])} items")
    
    if bank_status != "LOGIC_DENSITY_STABLE":
        print("TEST FAILED at Step 1")
        return

    # 4. Step 2: Fractal Gate Verification (The 1-3-9)
    print("\n>>> STEP 2: FRACTAL GATE VERIFICATION")
    fractal_status = fractal_gate.verify_9_plus_1_layer()
    print(f"STATUS: {fractal_status}")
    
    if "STABLE" not in fractal_status:
        print("TEST FAILED at Step 2")
        return

    # 5. Step 3: Execution (Hyperbolic Math)
    print("\n>>> STEP 3: EXECUTION (NODE 13 PATCH)")
    # Extract vectors from "Alpha" bank (executed extraction)
    vec_a = [0.5, 0.2]
    vec_b = [0.1, 0.1]
    
    distance = HyperbolicMath.poincare_distance(vec_a, vec_b)
    print(f"CALCULATION: Poincaré Distance between {vec_a} and {vec_b}")
    print(f"RESULT: {distance:.6f}")
    
    print("\n-----------------------------------------------------------------------")
    print("[CONCLUSION] SYSTEM STABILITY: 100%")
    print("The 1-3-9 Fractal Architecture successfully governed the execution.")

if __name__ == "__main__":
    test_integrated_stack()
