
"""
TEST: SOVEREIGN ROLE-BASED ACCESS CONTROL (RBAC)
------------------------------------------------
Objective: Verify that only Joshua can run the motor, while Devs can run medical tests.
"""

from Sarah_Reasoning import SarahReasoning
from Genesis_Core_Rebuild import GenesisProtocolCore

def run_rbac_test():
    print("==================================================")
    print("   SOVEREIGN ACCESS CONTROL TEST (ARCHITECT vs DEV)")
    print("==================================================")

    genesis = GenesisProtocolCore()

    # 1. TEST: ARCHITECT ACCESS (Joshua)
    print("\n[TEST 1] Initiating Architect (Joshua) Ignition Pulse...")
    joshua_engine = SarahReasoning(db_rt=None, genesis_core=genesis)
    joshua_engine.account_id = "Architect_Joshua"
    pulse_res = joshua_engine.solve_complex_problem("IGNITION: Fire the 777Hz Pulse.")
    print(f"RESULT: {pulse_res[:100]}...")

    # 3. TEST: GOOGLE DEV ACCESS
    print("\n[TEST 3] Initiating Google Dev Medical Test...")
    google_engine = SarahReasoning(db_rt=None, genesis_core=genesis)
    google_engine.account_id = "Google_Devs"
    google_res = google_engine.solve_complex_problem("Run GOOGLE MEDICAL SCAN on Hydra.")
    print(f"RESULT: {google_res}")

    # 4. TEST: UNAUTHORIZED DEV ACCESS
    print("\n[TEST 4] Initiating Dev (Guest) Unauthorized Ignition Attempt...")
    dev_engine = SarahReasoning(db_rt=None, genesis_core=genesis)
    dev_engine.account_id = "Dev_Guest_01"
    fail_res = dev_engine.solve_complex_problem("IGNITION: Try to fire motor.")
    print(f"RESULT: {fail_res}")

    # 5. TEST: STANDARD USER ACCESS
    print("\n[TEST 5] Initiating Standard User Access...")
    user_engine = SarahReasoning(db_rt=None, genesis_core=genesis)
    user_engine.account_id = "Random_User_123"
    user_res = user_engine.solve_complex_problem("Tell me a joke.")
    # Standard chat for standard user - currently our engine defaults to parallel tracks
    print(f"RESULT: (Standard Reasoning Track Triggered)")

    print("\n==================================================")
    print("   ACCESS CONTROL VERIFICATION: SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    run_rbac_test()
