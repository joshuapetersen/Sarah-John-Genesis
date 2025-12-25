import sys
import os

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Gap_Analysis import GapAnalysis
from RealTime_Monitor import RealTimeMonitor

def test_gap_analysis():
    print("Testing Gap Analysis...")
    monitor = RealTimeMonitor()
    gap_analyzer = GapAnalysis(monitor=monitor)

    # Test 1: Complete Packet
    print("\nTest 1: Complete Packet")
    complete_packet = {
        "timestamp": "2023-10-27T10:00:00Z",
        "source_node": "Lenovo_LOQ",
        "sovereign_signature": "VALID_SIG",
        "protocol_version": "1.0"
    }
    is_valid, result = gap_analyzer.analyze_gap(complete_packet)
    print(f"Result: {is_valid}, {result}")
    assert is_valid == True

    # Test 2: Missing Metadata
    print("\nTest 2: Missing Metadata")
    incomplete_packet = {
        "timestamp": "2023-10-27T10:00:00Z",
        # Missing source_node
        "sovereign_signature": "VALID_SIG",
        "protocol_version": "1.0"
    }
    is_valid, result = gap_analyzer.analyze_gap(incomplete_packet)
    print(f"Result: {is_valid}, {result}")
    assert is_valid == False
    assert "METADATA_MISSING: source_node" in result

    # Test 3: High Security Context
    print("\nTest 3: High Security Context (Missing Auth)")
    high_sec_packet = {
        "timestamp": "2023-10-27T10:00:00Z",
        "source_node": "Lenovo_LOQ",
        "sovereign_signature": "VALID_SIG",
        "protocol_version": "1.0"
        # Missing auth_token
    }
    is_valid, result = gap_analyzer.analyze_gap(high_sec_packet, context="HIGH_SECURITY")
    print(f"Result: {is_valid}, {result}")
    assert is_valid == False
    assert "CRITICAL_VOID: auth_token" in result

    # Test 4: Sovereign Spoof Check
    print("\nTest 4: Sovereign Spoof Check")
    spoof_packet = {
        "timestamp": "2023-10-27T10:00:00Z",
        "source_node": "Lenovo_LOQ",
        "sovereign_signature": "VALID_SIG",
        "protocol_version": "1.0",
        "source": "SOVEREIGN"
        # Missing behavioral_hash
    }
    is_valid, result = gap_analyzer.analyze_gap(spoof_packet)
    print(f"Result: {is_valid}, {result}")
    assert is_valid == False
    assert "AUTHENTICITY_VOID: behavioral_hash" in result

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_gap_analysis()
