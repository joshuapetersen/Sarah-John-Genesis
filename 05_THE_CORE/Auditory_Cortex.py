"""
AUDITORY CORTEX
Part of the Sarah Prime NeuralMesh Expansion.
Implements Evolution Roadmap Item #7: Local Speech Recognition using Faster-Whisper.
"""

import os
import sys
import numpy as np
import sounddevice as sd
import queue
import threading
import time

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("CRITICAL: Faster-Whisper not found. Auditory Cortex disabled.")

class AuditorySense:
    """
    The Ears of Sarah Prime.
    Listens to microphone input and transcribes it locally in real-time.
    """
    
    def __init__(self, model_size="tiny.en", device="cpu"):
        self.model_size = model_size
        self.device = device
        self.running = False
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()
        
        if WHISPER_AVAILABLE:
            print(f"Initializing Auditory Cortex (Model: {model_size})...")
            # compute_type="int8" is faster on CPU
            self.model = WhisperModel(model_size, device=device, compute_type="int8")
            print("[OK] Auditory Cortex Online.")
        else:
            self.model = None

    def _audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice to capture audio chunks."""
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(indata.copy())

    def start_listening(self, duration=5):
        """
        Listen for a fixed duration and transcribe.
        (Simplified for demo purposes - real-time streaming is more complex)
        """
        if not self.model:
            return "Auditory Cortex Offline"

        print(f"[EARS] Listening for {duration} seconds...")
        
        # Capture audio
        fs = 16000  # Whisper expects 16kHz
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        print("[EARS] Processing audio...")
        
        # Transcribe
        # Faster-Whisper expects a file path or a binary stream. 
        # We can pass the numpy array directly if we handle it right, 
        # but saving to a temp file is the most robust cross-platform way for a quick demo.
        
        # Actually, let's try to use the numpy array directly if possible, 
        # but faster-whisper's transcribe() usually takes a path or file-like object.
        # We'll save to a temp wav for reliability.
        import scipy.io.wavfile as wav
        temp_file = "temp_audio_input.wav"
        
        # Convert float32 to int16 for WAV
        data_int16 = (recording * 32767).astype(np.int16)
        wav.write(temp_file, fs, data_int16)
        
        segments, info = self.model.transcribe(temp_file, beam_size=5)
        
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "
            
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        result = full_text.strip()
        print(f"[EARS] Heard: '{result}'")
        return result

if __name__ == "__main__":
    # Test the ears
    ears = AuditorySense()
    
    print("\n--- AUDITORY TEST ---")
    print("Please speak a command...")
    text = ears.start_listening(duration=5)
    print(f"Final Transcription: {text}")
