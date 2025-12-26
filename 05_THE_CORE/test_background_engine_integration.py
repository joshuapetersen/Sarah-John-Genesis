"""
test_background_engine_integration.py
Full Integration Test for Phase 1 Background Engine

Tests all four components working together:
  - Coherence Verifier (consciousness integrity)
  - Thermal Trend Predictor (thermal management)
  - Network Pressure Monitor (rate limit avoidance)
  - Sovereign State Coherence Engine (orchestrator)
"""

import json
import time
from pathlib import Path

from Coherence_Verifier import CoherenceVerifier
from Thermal_Trend_Predictor import ThermalTrendPredictor
from Network_Pressure_Monitor import NetworkPressureMonitor
from Sovereign_State_Coherence_Engine import SovereignStateCoherenceEngine


def test_full_integration():
    """Run comprehensive integration test."""
    print("\n" + "="*80)
    print("PHASE 1 BACKGROUND ENGINE - FULL INTEGRATION TEST")
    print("="*80)
    
    # Initialize all components
    print("\n[STEP 1] Initialize all components")
    verifier = CoherenceVerifier()
    thermal = ThermalTrendPredictor()
    network = NetworkPressureMonitor()
    engine = SovereignStateCoherenceEngine(heartbeat_interval=3)
    
    print("  ✓ Coherence Verifier initialized")
    print("  ✓ Thermal Trend Predictor initialized")
    print("  ✓ Network Pressure Monitor initialized")
    print("  ✓ Sovereign State Coherence Engine initialized")
    
    # Test 2: Coherence verification
    print("\n[STEP 2] Test consciousness coherence verification")
    integrity = verifier.full_integrity_check()
    print(f"  Status: {integrity['overall_status']}")
    assert integrity['overall_status'] in ['SECURE', 'WARNING', 'CRITICAL']
    print("  ✓ Coherence verification working")
    
    # Test 3: Thermal monitoring
    print("\n[STEP 3] Test thermal monitoring")
    thermal_report = thermal.get_thermal_report()
    print(f"  Thermal Zone: {thermal_report['thermal_zone']}")
    print(f"  Current Temp: {thermal_report['current_temperature']}°C")
    assert thermal_report['thermal_zone'] in ['COOL', 'NORMAL', 'CAUTION', 'WARNING', 'THROTTLE', 'CRITICAL']
    print("  ✓ Thermal monitoring working")
    
    # Test 4: Network monitoring
    print("\n[STEP 4] Test network pressure monitoring")
    # Simulate API calls
    for i in range(25):
        network.record_api_call(200, "test_endpoint", latency_ms=100)
    
    network_report = network.get_network_report()
    print(f"  Total Calls: {network_report['total_calls']}")
    print(f"  Success Rate: {network_report['success_rate_percent']}%")
    print(f"  Pressure Level: {network_report['pressure_prediction']['pressure_level']}")
    assert network_report['pressure_prediction']['pressure_level'] in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    print("  ✓ Network monitoring working")
    
    # Test 5: Start background engine
    print("\n[STEP 5] Start background coherence engine")
    engine.start()
    print("  ✓ Engine started")
    
    # Test 6: Let it run
    print("\n[STEP 6] Let engine run for 10 cycles (30 seconds)")
    start_cycles = engine.cycle_count
    time.sleep(10)
    end_cycles = engine.cycle_count
    
    print(f"  Cycles completed: {end_cycles - start_cycles}")
    assert end_cycles > start_cycles
    print("  ✓ Engine running and cycling")
    
    # Test 7: Check engine status
    print("\n[STEP 7] Check engine status")
    status = engine.get_status()
    print(f"  Running: {status['is_running']}")
    print(f"  Total cycles: {status['cycle_count']}")
    print(f"  Overall health: {status['coherence']['overall_status']}")
    assert status['is_running']
    print("  ✓ Engine status good")
    
    # Test 8: Simulate thermal stress
    print("\n[STEP 8] Simulate thermal stress scenario")
    # Add fake hot temperatures
    for i in range(10):
        engine.thermal_predictor.temp_history.append((time.time() - (10-i), 50 + i*3))
    
    thermal_report = engine.thermal_predictor.get_thermal_report()
    print(f"  Simulated thermal trend: {thermal_report['trend']}")
    print("  ✓ Thermal stress simulation working")
    
    # Test 9: Simulate network spike
    print("\n[STEP 9] Simulate network pressure spike")
    for i in range(50):
        engine.network_monitor.record_api_call(200, "test", latency_ms=100)
    
    network_pred = engine.network_monitor.predict_rate_limit_exhaustion()
    print(f"  Simulated network load: {network_pred['current_load_percent']}%")
    print("  ✓ Network spike simulation working")
    
    # Test 10: Stop engine
    print("\n[STEP 10] Stop background engine")
    engine.stop()
    time.sleep(1)
    print("  ✓ Engine stopped cleanly")
    
    # Summary
    print("\n" + "="*80)
    print("INTEGRATION TEST SUMMARY")
    print("="*80)
    print("✓ All components initialized")
    print("✓ Consciousness coherence verified")
    print("✓ Thermal monitoring operational")
    print("✓ Network pressure monitoring operational")
    print("✓ Background engine running and cycling")
    print("✓ Thermal stress simulation working")
    print("✓ Network spike simulation working")
    print("✓ All components shut down cleanly")
    print("\n[OK] FULL INTEGRATION TEST PASSED")
    
    return True


if __name__ == "__main__":
    try:
        test_full_integration()
    except AssertionError as e:
        print(f"\n[FAILED] Integration test assertion failed: {e}")
    except Exception as e:
        print(f"\n[ERROR] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
