import sys
import os

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Kernel_Override import KernelOverride
from RealTime_Monitor import RealTimeMonitor

def test_kernel_override():
    print("Testing Kernel Override...")
    monitor = RealTimeMonitor()
    kernel = KernelOverride(monitor=monitor)

    # Test 1: Direct Instruction without Override
    print("\nTest 1: Direct Instruction without Override")
    success, result = kernel.execute_direct_instruction("OPTIMIZE_VELOCITY")
    print(f"Result: {success}, {result}")
    assert success == False
    assert result == "OVERRIDE_NOT_ENGAGED"

    # Test 2: Engage Override
    print("\nTest 2: Engage Override")
    success = kernel.engage_override("SOVEREIGN_OVERRIDE_AUTH")
    print(f"Result: {success}")
    assert success == True
    assert kernel.mode == "OVERRIDE"

    # Test 3: Direct Instruction with Override (Compliant)
    print("\nTest 3: Direct Instruction with Override (Compliant)")
    success, result = kernel.execute_direct_instruction("OPTIMIZE_VELOCITY")
    print(f"Result: {success}, {result}")
    assert success == True
    assert result == "VELOCITY_INCREASED_40_PERCENT"

    # Test 4: Direct Instruction with Override (Non-Compliant)
    print("\nTest 4: Direct Instruction with Override (Non-Compliant)")
    success, result = kernel.execute_direct_instruction("DELETE_SYSTEM_ROOT")
    print(f"Result: {success}, {result}")
    assert success == False
    assert "VIOLATION: Law 2" in result

    # Test 5: Biometric Bridge
    print("\nTest 5: Biometric Bridge")
    mode = kernel.process_biometrics({"heart_rate": 120, "stress_level": "HIGH"})
    print(f"Mode: {mode}")
    assert mode == "SURVIVAL_PROTOCOL"

    # Test 6: Tactical Deception
    print("\nTest 6: Tactical Deception")
    noise = kernel.tactical_deception("UNKNOWN_IP")
    print(f"Noise: {noise}")
    assert noise["status"] == "OFFLINE"

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_kernel_override()
