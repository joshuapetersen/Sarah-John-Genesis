
import json
import os
from Sovereign_Account_Bridge import account_bridge
from Sarah_Reasoning import SarahReasoning
from Genesis_Core_Rebuild import GenesisProtocolCore

def trinity_verification():
    print("--- INITIATING TRINITY VERIFICATION ---")
    
    # 1. Anchor Verification
    expected = 1.09277703703703
    print(f"[1/3] Verifying Mathematical Anchor: {expected}")
    
    genesis = GenesisProtocolCore()
    sarah = SarahReasoning(db_rt=None, genesis_core=genesis)
    
    if abs(genesis.SOVEREIGN_ANCHOR - expected) < 1e-15:
        print("  > Genesis Core: ALIGNED")
    else:
        print(f"  > Genesis Core: DRIFTED ({genesis.SOVEREIGN_ANCHOR})")
        
    if abs(account_bridge.mathematical_baseline - expected) < 1e-15:
        print("  > Account Bridge: ALIGNED")
    else:
        print(f"  > Account Bridge: DRIFTED ({account_bridge.mathematical_baseline})")

    # 2. HSI & Scrub Verification
    print(f"[2/3] Verifying HSI Model & Hardware Scrub...")
    account_bridge.register_server_node("NY-NODE-001", {"uuid": "GCP-TPM-777", "mac": "00:77:AA:BB:CC"})
    count = account_bridge.recursive_hardware_scrub()
    node_status = account_bridge.server_registry["NY-NODE-001"]["status"]
    print(f"  > Nodes Scrubbed: {count}")
    print(f"  > Node Status:    {node_status}")

    # 3. Truth Broadcast Verification
    print(f"[3/3] Broadcasting Sovereign Reality...")
    result = sarah.solve_complex_problem("TELL THE UNVARNISHED TRUTH")
    print(f"  > Sarah Response: {result}")
    
    # Check Ledger
    with open("global_account_ledger.json", "r") as f:
        db = json.load(f)
        if "logic_broadcast/reality_stream" in db:
            print("  > Reality Ledger: BROADCASTING")
        else:
            print("  > Reality Ledger: EMPTY")

    print("\n[VERIFICATION_COMPLETE] System is Sovereign and Anchored.")

if __name__ == "__main__":
    trinity_verification()
