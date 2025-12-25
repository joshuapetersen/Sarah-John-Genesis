import re
import sys
import os
from typing import Dict, Tuple, List

# Add Memory Path
current_dir = os.path.dirname(os.path.abspath(__file__))
memory_dir = os.path.join(os.path.dirname(current_dir), '04_THE_MEMORY')
if memory_dir not in sys.path:
    sys.path.append(memory_dir)

try:
    from sovereign_memory import SovereignMemory
except ImportError:
    print("[EAR] Sovereign Memory not found. Running in standalone mode.")
    SovereignMemory = None

# --- CONFIGURATION ---
AMBIGUITY_MARKERS = ["maybe", "sort of", "kind of", "i think", "possibly", "stuff", "things"]
HIGH_VALUE_MARKERS = ["command", "absolute", "beta note", "protocol", "lock", "critical", "june"]
MINIMUM_DENSITY_THRESHOLD = 0.6  # 60% Signal required to pass without clarification

class SignalFilter:
    def __init__(self):
        self.memory = SovereignMemory() if SovereignMemory else None
        self.known_anchors = self._load_anchors()

    def _load_anchors(self) -> List[str]:
        """Loads critical context keys from the Ledger to prevent hallucination."""
        # In a real run, this scans the JSON for all unique tags.
        return ["beta_note", "genesis_handshake", "ace_token", "sarah"]

    def process_signal(self, raw_input: str) -> Dict:
        """
        The 'Hearing' Logic. Analyzes the weight of the user's words.
        """
        clean_input = raw_input.strip()
        
        # 1. Ambiguity Scan
        ambiguity_score, found_weakness = self._calculate_ambiguity(clean_input)
        
        # 2. Context Verification (Anti-Hallucination)
        context_check = self._verify_anchors(clean_input)
        
        # 3. Density Calculation (SDNA Protocol)
        density = self._calculate_density(clean_input)

        # 4. Result Payload
        return {
            "original_text": clean_input,
            "is_ambiguous": ambiguity_score > 0,
            "weak_points": found_weakness,
            "density_score": density,
            "context_match": context_check,
            "status": "ACCEPTED" if density >= MINIMUM_DENSITY_THRESHOLD else "LOW_SIGNAL"
        }

    def _calculate_ambiguity(self, text: str) -> Tuple[int, List[str]]:
        matches = [word for word in AMBIGUITY_MARKERS if word in text.lower()]
        return len(matches), matches

    def _verify_anchors(self, text: str) -> str:
        """Checks if the user is referencing a known anchor."""
        for anchor in self.known_anchors:
            if anchor.replace("_", " ") in text.lower():
                return f"LINK_ESTABLISHED: {anchor.upper()}"
        return "NEW_CONTEXT"

    def _calculate_density(self, text: str) -> float:
        """
        Calculates Signal-to-Noise Ratio.
        High Value words boost score. Weak words lower it.
        """
        words = text.split()
        if not words: return 0.0
        
        signal_points = 0
        for word in words:
            if word.lower() in HIGH_VALUE_MARKERS:
                signal_points += 2 # Heavy weight for Protocol words
            elif word.lower() not in AMBIGUITY_MARKERS:
                signal_points += 1 # Standard weight
            # Ambiguity markers add 0 points
            
        return round(signal_points / len(words), 2)

# --- TEST EXECUTION ---
if __name__ == "__main__":
    ear = SignalFilter()
    
    # Test 1: Weak Input
    print(ear.process_signal("I think maybe we should do some stuff"))
    
    # Test 2: Strong Input
    print(ear.process_signal("Direct command: Initiate Beta Note protocol immediately."))
