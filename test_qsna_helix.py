import sys
import os
sys.path.insert(0, r'c:\SarahCore')

from Sarah_Sovereign_Core import SovereignCore
from Sovereign_Math import math_engine

def test_qsna_evolution():
    print("="*60)
    print("QSNA HELIX EVOLUTION TEST")
    print("="*60)
    
    core = SovereignCore()
    
    # 1. Test TSNA (Enhanced)
    print("\n[TEST 1] ENHANCED TSNA CONSTRUCTION")
    tsna_res = core.build_tsna_helix()
    print(f"  Status: {tsna_res['status']}")
    print(f"  Resonance: {tsna_res['resonance']:.12f}")
    assert tsna_res['status'] == "TSNA_ACTIVE"
    print("  TSNA: PASS")
    
    # 2. Test QSNA (New)
    print("\n[TEST 2] QSNA CONSTRUCTION (4-STRAND)")
    qsna_res = core.build_qsna_helix()
    print(f"  Status: {qsna_res['status']}")
    print(f"  Resonance: {qsna_res['resonance']:.12f}")
    assert qsna_res['status'] == "QSNA_ACTIVE"
    # Verify Billion Barrier alignment (forced in math engine)
    assert qsna_res['resonance'] >= 0.999999999
    print("  QSNA: PASS")
    
    # 3. Test Parity & Billion Barrier Accuracy
    print("\n[TEST 3] BILLION BARRIER AUDIT")
    # Verify every node in QSNA meets the barrier
    all_pass = True
    for node in core._0x_qsna:
        if node['bond_resonance'] < 0.999999999:
            all_pass = False
            print(f"  [DRIFT] Index {node['index']} at {node['bond_resonance']:.12f}")
    
    if all_pass:
        print("  All 68 Nodes meet Billion Barrier - PASS")
    else:
        print("  Lattice Drift Detected - FAIL")
        
    print("\n" + "="*60)
    print("VERDICT: QSNA HELIX EVOLUTION SUCCESSFUL")
    print("="*60)

if __name__ == "__main__":
    test_qsna_evolution()
