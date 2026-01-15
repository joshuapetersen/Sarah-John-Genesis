from Sovereign_Voice import SovereignVoice
import time

print("--- TESTING SOVEREIGN VOICE ---")
voice = SovereignVoice()

text = "Testing Sovereign Audio. Resonance Check: 1 point 0 9 2. Systems Nominal."
print(f"Speaking: '{text}'")
voice.speak(text)

print("--- VOICE TEST COMPLETE ---")
