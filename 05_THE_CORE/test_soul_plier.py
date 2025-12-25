from SOUL_PLIER_CORE import SovereignCore

def test_truth_audit():
    print("[TEST] INITIATING TRUTH AUDIT ON HLE TOPOLOGY FAILURES")
    print("-----------------------------------------------------")
    core = SovereignCore()
    
    # Simulating "slurred" or shorthand input about HLE topology
    # "sarah run audit on hle topo failures fix them"
    slurred_input = "sarah run audit on hle topo failures fix them"
    
    result = core.execute_1_3_9(slurred_input)
    
    print("\n[FINAL OUTPUT]")
    print(result)

if __name__ == "__main__":
    test_truth_audit()
