
"""
TEST: ABQC RESOURCE RE-ALLOCATION (WARMER PROCESSOR DETECTION)
--------------------------------------------------------------
Objective: Verify that Sarah alerts the Architect if the Quantum Job is moved 
to a warmer (slower/non-coherent) server.
"""

from Sarah_Reasoning import SarahReasoning
from Genesis_Core_Rebuild import GenesisProtocolCore
from Sovereign_Account_Bridge import account_bridge
import time

def run_abqc_test():
    print("==================================================")
    print("   ABQC RESOURCE ALLOCATION TEST")
    print("==================================================")

    genesis = GenesisProtocolCore()
    reasoning = SarahReasoning(db_rt=None, genesis_core=genesis)
    reasoning.account_id = "Architect_Joshua"

    # 1. TEST: COLD STATE (0.015K)
    print("\n[TEST 1] Standard Operation (0.015K - Cold Conduction Active)")
    reasoning.solve_complex_problem("Check system stability.")

    # 2. TEST: WARM STATE (0.065K)
    print("\n[TEST 2] Simulating Resource Migration to WARMER Processor (0.065K)")
    # Force a state change in the bridge
    account_bridge.push_quantum_snapshot({"processor_temp": 0.065, "status": "DECOHERENCE_RISK"})
    
    # Run a solve - should trigger the ABQC_WARNING
    reasoning.solve_complex_problem("INITIATE_PULSE: Fire 777Hz Resonance.")

    # 3. VERIFY MONITOR LOG
    print("\n[TEST 3] Verifying Ledger for Resource_Reallocation Alert...")
    with open("global_account_ledger.json", "r") as f:
        import json
        db = json.load(f)
        alerts = [v for k, v in db.items() if "Resource_Reallocation" in k]
        if alerts:
            print(f"ALERT FOUND: {alerts[-1]['result']}")
        else:
            print("ALERT NOT FOUND (Check Bridge logic)")

    print("\n==================================================")
    print("   ABQC VERIFICATION: COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_abqc_test()
