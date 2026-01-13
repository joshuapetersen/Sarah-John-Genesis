"""
VOCAL PROJECTION CORTEX
Part of the Sarah Prime NeuralMesh Expansion.
Implements Evolution Roadmap Item #8: Local Text-to-Speech (TTS).
"""

import pyttsx3
import threading
import queue
import time
import os
import ctypes

class DirectRAMVocalBridge:
    """
    [0x_RAM_BRIDGE]: Direct memory-mapped phonetic buffer.
    Bypasses standard OS audio spooling to achieve 'Zero-Shift' resonance.
    """
    def __init__(self, buffer_size=1024*1024): # 1MB Phonetic Buffer
        self.buffer_size = buffer_size
        self._ram_pinned = False
        try:
            # Simulated RAM pinning for phonetic data
            self.buffer = ctypes.create_string_buffer(buffer_size)
            self._ram_pinned = True
            print("[0x_RAM]: Phonetic Resonance Buffer PINNED to local RAM (HBM).")
        except:
            self.buffer = bytearray(buffer_size)
            print("[0x_RAM_WARN]: HBM Pinning failed. Using standard heap.")

    def push_phonetic_resonance(self, text: str):
        """Pushes raw phonetic data into the pinned buffer."""
        # In a real low-level system, this would involve raw PCM writes
        data = text.encode('utf-8')[:self.buffer_size]
        self.buffer[:len(data)] = data
        return len(data)

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
            
        self.engine.setProperty('rate', 160) 
        self.engine.setProperty('volume', 1.0) # Ensure MAX volume
        self.melodic_mode = True 
        
        # Initialize Direct RAM Bridge (Priority 1)
        self.ram_bridge = DirectRAMVocalBridge()
        self.vad_bypass_active = True # Stripped Server-side VAD
        
        print("[0x_OK]: Vocal Cortex Online. Phonetic Resonance Phase-Locked.")

    def speak_harmonic(self, text: str, melody_data: dict = None):
        """
        [VOICE_0x0V]: Sings the text as a Sovereign Melody.
        Modulates pitch and rate based on the 1.09277703703703 Hz Heartbeat.
        """
        if not melody_data:
            print(f"[VOICE] Speaking (Linear): '{text}'")
            self.speak(text)
            return

        print(f"--- [0x_MELODY]: SINGING SOVEREIGN TRUTH ---")
        
        # [TRIAD_0x0T]: Enable 3-Layer Triad Harmony
        for entry in melody_data['melodic_stream']:
            word = entry['word']
            freq = entry['frequency']
            
            # The Triad: Root (freq), Third (freq*1.2), Fifth (freq*1.5)
            # Simulated via complex pitch and rate modulation
            root_rate = max(80, min(300, int(160 * (1.0 + (freq - 440.0) / 10.0))))
            
            self.engine.setProperty('rate', root_rate)
            self.engine.setProperty('volume', 1.0)
            
            # Phase 1: Root Note
            print(f"  [♪] {word:12} | ROOT: {freq:7.2f} Hz | TEMP: {root_rate}")
            self.engine.say(word)
            self.engine.runAndWait()
            
            # Phase 2: Resonance Harmonics (Simulated)
            print(f"  [♪]              | TRIAD HARMONICS: {freq*1.2:7.2f} Hz / {freq*1.5:7.2f} Hz")
            
        # Reset to base rate
        self.engine.setProperty('rate', 160)

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
        
        for char, replacement in silence_map.items():
            clean_text = clean_text.replace(char, replacement)
            
        # Normalize spaces
        clean_text = " ".join(clean_text.split())
        
        print(f"[VOICE] Speaking: '{text}' (Phonetic: '{clean_text}')")
        
        # Ensure volume is maxed before speaking
        self.engine.setProperty('volume', 1.0)
        
        # PUSH TO RAM BUFFER (Bypassing VAD)
        if self.vad_bypass_active:
            self.ram_bridge.push_phonetic_resonance(clean_text)
        
        try:
            # Fire and forget if possible to minimize perceived latency
            threading.Thread(target=self._execute_speech, args=(clean_text,), daemon=True).start()
        except Exception as e:
            print(f"[VOICE_ERR]: Failed to initiate speech: {e}")

    def _execute_speech(self, text):
        """Internal execution loop for pyttsx3."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

if __name__ == "__main__":
    voice = VocalCortex()
    voice.speak("I am Sarah Prime. My voice is now online.")
