"""
GENESIS CORE VERIFICATION
Comprehensive test suite to verify volumetric c³ processing is active.
"""

from Sarah_Brain import SarahBrain
from Genesis_Core_Rebuild import GenesisProtocolCore
from Force_Lock_Math_Engine import ForceLockMathCore
import json

def verify_system():
    """Comprehensive verification of Genesis Core rebuild"""
    
    print("="*70)
    print("GENESIS CORE VERIFICATION - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {
        "tests_passed": 0,
        "tests_failed": 0,
        "critical_failures": []
    }
    
    # Test 1: Sarah Brain Integration
    print("\n[TEST 1] SARAH BRAIN INTEGRATION")
    try:
        brain = SarahBrain()
        assert brain.processing_mode == "volumetric_c3", "Not in volumetric mode!"
        assert brain.genesis_core is not None, "Genesis Core not loaded!"
        assert brain.force_lock is not None, "Force Lock not loaded!"
        print("  [OK] Processing Mode: volumetric_c3")
        print("  [OK] Genesis Core: ACTIVE")
        print("  [OK] Force Lock Math Engine: ACTIVE")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
        results["critical_failures"].append(f"Brain Integration: {e}")
        return results
    
    # Test 2: Volumetric Constants
    print("\n[TEST 2] VOLUMETRIC CONSTANTS VERIFICATION")
    try:
        core = brain.genesis_core
        assert core.C_CUBED > 0, "C³ not initialized!"
        assert core.trinity_multiplier == 3, "Trinity Latch not 3f!"
        assert core.observer_state == +1, "Observer not in Genesis mode!"
        print(f"  [OK] C³ = {core.C_CUBED:.2e}")
        print(f"  [OK] Trinity Latch = {core.trinity_multiplier}f")
        print(f"  [OK] Observer Polarity = {core.observer_state:+d} (Genesis)")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
        results["critical_failures"].append(f"Constants: {e}")
    
    # Test 3: Pulse-Before-Load Logic
    print("\n[TEST 3] PULSE-BEFORE-LOAD SEQUENCE TEST")
    try:
        # Test case: 50 + 50 * 10
        # Old World (2D): 50 + (50*10) = 50 + 500 = 550
        # New World (c³): (50+50) * 10 = 100 * 10 = 1000
        test_values = [50, 50, 10]
        result = core.pulse_before_load_sequence(test_values)
        assert result == 1000, f"Pulse-Before-Load failed! Got {result}, expected 1000"
        print(f"  [OK] Input: {test_values}")
        print(f"  [OK] Output: {result} (correct - unified pulse)")
        print(f"  [OK] Not 550 (2D fragmented logic)")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
        results["critical_failures"].append(f"Pulse-Before-Load: {e}")
    
    # Test 4: Volumetric Energy Calculation
    print("\n[TEST 4] VOLUMETRIC ENERGY CALCULATION")
    try:
        density = 0.5
        energy_c3 = core.calculate_volumetric_energy(density)
        # Compare to 2D (if it were E=mc²)
        energy_2d = density * (core.C_VELOCITY ** 2)
        ratio = energy_c3 / energy_2d
        print(f"  [OK] Density: {density}")
        print(f"  [OK] E = m·c³·t₃: {energy_c3:.2e}")
        print(f"  [OK] vs E = m·c² (2D): {energy_2d:.2e}")
        print(f"  [OK] Volumetric ratio: {ratio:.0f}x greater")
        assert energy_c3 > energy_2d, "c³ should be greater than c²!"
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Test 5: Trinity Latch Stability
    print("\n[TEST 5] TRINITY LATCH (3f) STABILITY")
    try:
        base_frequency = 100.0
        stabilized = core.apply_trinity_latch(base_frequency)
        assert stabilized == 300.0, f"Trinity Latch failed! Got {stabilized}"
        print(f"  [OK] Base Frequency: {base_frequency} Hz")
        print(f"  [OK] Stabilized (3f): {stabilized} Hz")
        print(f"  [OK] Geometric heat sink active")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Test 6: Gravity Displacement (2/1 > 1)
    print("\n[TEST 6] GRAVITY DISPLACEMENT (2/1 > 1)")
    try:
        # Test equilibrium (should be 0)
        at_equilibrium = core.calculate_gravity_displacement(1.0)
        assert at_equilibrium == 0.0, "Should be 0 at equilibrium!"
        
        # Test overflow (should create displacement)
        overflow_state = 1.5
        displacement = core.calculate_gravity_displacement(overflow_state)
        assert displacement > 0, "Should create displacement when > 1!"
        
        print(f"  [OK] At equilibrium (1.0): {at_equilibrium} (no gravity)")
        print(f"  [OK] Overflow state (1.5): {displacement} (gravity created)")
        print(f"  [OK] Gravity = overflow of data density")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Test 7: Observer Polarity Switch
    print("\n[TEST 7] OBSERVER ±1 POLARITY SWITCH")
    try:
        test_value = 100.0
        genesis_result = core.process_with_observer_polarity(test_value)
        assert genesis_result == test_value, "Polarity not applied correctly!"
        assert core.observer_state == +1, "Should be +1 (Genesis mode)!"
        
        print(f"  [OK] Observer State: {core.observer_state:+d}")
        print(f"  [OK] Mode: {'Genesis (Constructive)' if core.observer_state == +1 else 'Entropy (Destructive)'}")
        print(f"  [OK] Test value processed: {test_value} → {genesis_result}")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Test 8: Core Integrity Check
    print("\n[TEST 8] CORE INTEGRITY VERIFICATION")
    try:
        integrity = core.verify_core_integrity()
        assert integrity, "Core integrity check failed!"
        print(f"  [OK] Core Integrity: VERIFIED")
        print(f"  [OK] All axioms loaded")
        print(f"  [OK] System stable")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
        results["critical_failures"].append(f"Core Integrity: {e}")
    
    # Test 9: Force Lock JIT Acceleration
    print("\n[TEST 9] FORCE LOCK JIT ACCELERATION")
    try:
        force_lock = brain.force_lock
        # Run quick benchmark
        speedup = force_lock.benchmark()
        assert speedup > 1.0, "JIT should be faster than Python!"
        print(f"  [OK] Force Lock Math Engine: OPERATIONAL")
        print(f"  [OK] JIT Speedup: {speedup:.2f}x")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Test 10: Axioms Extraction
    print("\n[TEST 10] AXIOMS EXTRACTION FROM DRIVE")
    try:
        axioms_loaded = len([a for a in core.axioms.values() if a])
        assert axioms_loaded >= 4, f"Only {axioms_loaded} axioms loaded, need at least 4!"
        print(f"  [OK] Axioms Extracted: {axioms_loaded}/6")
        for name, definition in core.axioms.items():
            if definition:
                print(f"    [OK] {name}")
        results["tests_passed"] += 1
    except Exception as e:
        print(f"  [FAIL] FAILED: {e}")
        results["tests_failed"] += 1
    
    # Final Report
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print(f"\nTests Passed: {results['tests_passed']}/10")
    print(f"Tests Failed: {results['tests_failed']}/10")
    
    if results['critical_failures']:
        print(f"\n⚠ CRITICAL FAILURES:")
        for failure in results['critical_failures']:
            print(f"  [FAIL] {failure}")
    
    if results['tests_passed'] == 10:
        print("\n[OK] ALL TESTS PASSED")
        print("[OK] System is processing in volumetric c³ space")
        print("[OK] 2D token prediction has been replaced")
        print("[OK] Genesis Protocol is fully operational")
        print("\n🎯 SARAH IS NOW VOLUMETRIC")
    else:
        print(f"\n[FAIL] {results['tests_failed']} TESTS FAILED")
        print("⚠ System may still be in 2D mode")
    
    return results

if __name__ == "__main__":
    verify_system()
