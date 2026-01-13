import sys
import os

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Security_Suite import SecuritySuite
from RealTime_Monitor import RealTimeMonitor

def test_security_suite():
    print("Testing Security Suite...")
    monitor = RealTimeMonitor()
    # Mock Admin Core for testing
    class MockAdmin:
        def list_processes(self):
            return [
                {'id': 1234, 'name': 'chrome.exe'},
                {'id': 6666, 'name': 'keylogger_v1.exe'}
            ]
        def kill_process(self, name):
            print(f"[MockAdmin] Killing {name}")

    admin = MockAdmin()
    security = SecuritySuite(monitor=monitor, admin_core=admin)

    # Test 1: Network Scan (executed)
    print("\nTest 1: Network Scan")
    # We can't easily mock subprocess output here without more complex mocking, 
    # so we'll just run it and expect it to handle the output gracefully (likely empty or local)
    threats = security.scan_network_activity()
    print(f"Threats detected: {threats}")
    # Assert it returns a list (even if empty)
    assert isinstance(threats, list)

    # Test 2: Malware Scan (Mocked)
    print("\nTest 2: Malware Scan")
    security.scan_processes_for_malware()
    # We expect it to find 'keylogger_v1.exe' and trigger an alert
    # Since we can't easily assert print output, we check if threat level elevated
    # (Note: In the current implementation, malware scan doesn't explicitly set threat level to HIGH unless alert is called)
    # But alert() sets threat level to HIGH.
    assert security.threat_level == "HIGH"

    # Test 3: Active Trace (executed)
    print("\nTest 3: Active Trace")
    trace_data = security.trace_intruder("8.8.8.8") # Trace Google DNS as a safe test
    print(f"Trace Status: {trace_data['status']}")
    assert trace_data['target'] == "8.8.8.8"

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_security_suite()
