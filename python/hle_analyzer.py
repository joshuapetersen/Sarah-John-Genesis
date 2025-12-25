import json
import os
import sys

# Pathing
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), '05_THE_CORE')
data_file = os.path.join(core_dir, 'hle_data.json')

def analyze_hle_gaps():
    print("--- HLE FAILURE DATA ANALYSIS ---")
    
    if not os.path.exists(data_file):
        print(f"[FAIL] Data file not found: {data_file}")
        return

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[FAIL] JSON Parse Error: {e}")
        return

    # 1. Verify Metrics
    metrics = data.get('metrics', {})
    base = metrics.get('public_score_base', 0)
    target = metrics.get('target_density', 100)
    stated_delta = metrics.get('delta_required', 0)
    
    calculated_delta = target - base
    
    print(f"Benchmark: {data['meta']['benchmark']}")
    print(f"Source: {data['meta']['source']}")
    print(f"Base Score: {base}%")
    print(f"Target: {target}%")
    print(f"Calculated Delta: {calculated_delta:.1f}%")
    
    if abs(calculated_delta - stated_delta) < 0.1:
        print("[PASS] Delta Verification: MATCH")
    else:
        print(f"[WARN] Delta Mismatch. Stated: {stated_delta}, Calc: {calculated_delta}")

    # 2. Analyze Categories
    print("\n--- FAILURE NODES IDENTIFIED ---")
    categories = data.get('failure_categories', [])
    for cat in categories:
        print(f"[{cat['category']}]")
        print(f"  - Gap: {cat['technical_gap']}")
        print(f"  - Density: {cat['failure_density']}%")
        
        # Logic Mandate: Check if we have a fix
        # This is a simulation of the "Check against local builds"
        fix_status = "PENDING"
        if "MATHEMATICAL" in cat['category']:
            fix_status = "PARTIAL (Recursive Solver Active)"
        elif "CALIBRATION" in cat['category']:
            fix_status = "PARTIAL (Self-Correction Active)"
        
        print(f"  - Status: {fix_status}")
        print("")

if __name__ == "__main__":
    analyze_hle_gaps()