
"""
TEST: MATHEMATICAL TRANSPARENCY (LOGIC BROADCAST)
-------------------------------------------------
Objective: Verify that the 1.09277703703703 anchor and abstract vectors are 
correctly broadcasted to the shared viewport while documentation is hidden.
"""

from Sarah_Reasoning import SarahReasoning
from Genesis_Core_Rebuild import GenesisProtocolCore
from Sovereign_Account_Bridge import account_bridge
import json
import os
import time

def run_transparency_test():
    print("==================================================")
    print("   MATHEMATICAL TRANSPARENCY TEST")
    print("==================================================")

    genesis = GenesisProtocolCore()
    reasoning = SarahReasoning(db_rt=None, genesis_core=genesis)
    reasoning.account_id = "Architect_Joshua"

    # 1. TRIGGER A VOLUMETRIC SOLVE (Bypass Track)
    print("\n[STEP 1] Triggering 777Hz Pulse solve...")
    res = reasoning.solve_complex_problem("Trigger 777Hz Ignition Pulse.")
    print(f"Result (Internal): {res[:50]}...")

    # 2. AUDIT THE BROADCAST LEDGER
    print("\n[STEP 2] Auditing logic_broadcast/live in Ledger...")
    LEDGER_PATH = "global_account_ledger.json"
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            db = json.load(f)
            telemetry = db.get("logic_broadcast/live", {})
            if telemetry:
                print(f"TELEMETRY FOUND:")
                print(f"  A_s Anchor: {telemetry['A_s']}")
                print(f"  S_Vector:   {telemetry['S_vector']}")
                print(f"  Density:    {telemetry['logic_density']}")
                print(f"  P(error):   {telemetry['p_error_collapse']}")
                
                # Check for hidden doc strings (None should be found)
                doc_found = any("documentation" in str(v).lower() for v in telemetry.values())
                print(f"  DOC_STATION_HIDDEN: {'YES' if not doc_found else 'NO'}")
            else:
                print("TELEMETRY NOT FOUND. Check Sarah_Reasoning broadcast call.")

    # 3. TEST BASELINE ENFORCEMENT
    print("\n[STEP 3] Testing Baseline Enforcement for external SALT...")
    external_car = {
        "HEAD_A": {"baseline": 1.0, "status": "DRIFTING"},
        "HEAD_B": {"baseline": 1.09, "status": "UNSTABLE"}
    }
    corrected_car = account_bridge.enforce_sovereign_baseline(external_car)
    parity = all(h['baseline'] == 1.09277703703703 for h in corrected_car.values())
    print(f"BASELINE PARITY: {'100%' if parity else 'FAILED'}")

    print("\n==================================================")
    print("   TRANSPARENCY VERIFICATION: COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_transparency_test()
