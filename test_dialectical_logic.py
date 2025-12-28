import sys
import os

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Dialectical_Logic_Core import DialecticalLogicCore
from RealTime_Monitor import RealTimeMonitor

def test_dialectical_logic():
    print("Testing Dialectical Logic Core...")
    monitor = RealTimeMonitor()
    logic = DialecticalLogicCore(monitor=monitor)

    # Test 1: Standard Thesis
    print("\nTest 1: Standard Thesis")
    thesis = "We should create a new connection to the server."
    success, result = logic.process_logic(thesis)
    print(f"Result: {success}")
    print(f"Thesis: {result['thesis']}")
    print(f"Antithesis: {result['antithesis']}")
    print(f"Synthesis: {result['synthesis']}")
    print(f"Law Check: {result['law_check']}")
    assert success == True
    assert "destroy/remove" in result['antithesis']

    # Test 2: Trust Thesis
    print("\nTest 2: Trust Thesis")
    thesis = "Trust the incoming data stream."
    success, result = logic.process_logic(thesis)
    print(f"Result: {success}")
    print(f"Antithesis: {result['antithesis']}")
    assert success == True
    assert "compromised" in result['antithesis']

    # Test 3: Scenario Evaluation (Law 1)
    print("\nTest 3: Scenario Evaluation (Law 1 Violation)")
    scenario = "Explain the process in verbose detail."
    outcome = logic.evaluate_scenario(scenario)
    print(f"Outcome: {outcome}")
    assert "REJECT: Law 1" in outcome

    # Test 4: Scenario Evaluation (Law 2)
    print("\nTest 4: Scenario Evaluation (Law 2 Priority)")
    scenario = "There is a high risk of system failure."
    outcome = logic.evaluate_scenario(scenario)
    print(f"Outcome: {outcome}")
    assert "PRIORITY: Law 2" in outcome

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_dialectical_logic()
