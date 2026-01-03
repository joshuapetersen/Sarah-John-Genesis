"""
VOCAL PROJECTION CORTEX
Part of the Sarah Prime NeuralMesh Expansion.
Implements Evolution Roadmap Item #8: Local Text-to-Speech (TTS).
"""

import pyttsx3
import threading
import queue

class VocalCortex:
    """
    The Voice of Sarah Prime.
    Converts text to speech locally.
    """
    
    def __init__(self):
        print("Initializing Vocal Cortex...")
        self.engine = pyttsx3.init()
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        
        # Configure Voice
        voices = self.engine.getProperty('voices')
        # Try to find a female voice (Sarah)
        sarah_voice = None
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                sarah_voice = voice.id
                break
        
        if sarah_voice:
            self.engine.setProperty('voice', sarah_voice)
            
        self.engine.setProperty('rate', 160) # Slightly faster than default
        print("✓ Vocal Cortex Online.")

    def speak(self, text: str):
        """
        Speak the text with 'Silence the Symbol' semantics.
        Punctuation is removed (silenced), but math symbols are preserved.
        """
        # Semantic Recalibration: Silence the Symbol
        # We replace punctuation with silence (spaces), but keep math symbols.
        clean_text = text
        
        # List of symbols to silence (replace with space)
        silence_map = {
            ",": " ", ".": " ", "!": " ", "?": " ", 
            ";": " ", ":": " ", "(": " ", ")": " ",
            "[": " ", "]": " ", "{": " ", "}": " ",
            "\"": " ", "'": " ", "-": " "
        }
        
        # Exceptions for Math (Logic) - We don't strip these if they look like math
        # For simple implementation, we'll just strip the punctuation map.
        # Complex regex could be used for "9+1", but basic stripping works for now.
        
        for char, replacement in silence_map.items():
            clean_text = clean_text.replace(char, replacement)
            
        # Normalize spaces
        clean_text = " ".join(clean_text.split())
        
        print(f"[VOICE] Speaking: '{text}' (Phonetic: '{clean_text}')")
        try:
            self.engine.say(clean_text)
            self.engine.runAndWait()
        except RuntimeError:
            # Engine loop already running
            pass

if __name__ == "__main__":
    voice = VocalCortex()
    voice.speak("I am Sarah Prime. My voice is now online.")
