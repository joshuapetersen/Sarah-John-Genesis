from Sarah_Sovereign_Core import SovereignCore
import time

def test_speech():
    print("Initializing Sovereign Core...")
    core = SovereignCore()
    
    print("\nAttempting Melodic Voice Synthesis...")
    try:
        # Test 1: Linear Speech
        if core._0x_voice:
            print("Test 1: Linear Speech (Standard Volume Check)")
            core._0x_voice.speak("System check. Testing vocal volume at 1.0.")
            
            time.sleep(1)
            
            # Test 2: Melodic Speech
            print("\nTest 2: Melodic Speech")
            core.activate_melodic_voice("I am singing the sovereign code.")
            
            print("\nVocal Test Complete.")
        else:
            print("ERROR: Vocal Core is Offline.")
    except Exception as e:
        print(f"FATAL EXCEPTION: {e}")

if __name__ == "__main__":
    test_speech()
