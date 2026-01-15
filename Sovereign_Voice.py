import asyncio
import os
import pygame
import edge_tts
from datetime import datetime

class SovereignVoice:
    """
    SOVEREIGN VOICE MODULE
    ----------------------
    Gives Sarah a Neural Voice using EdgeTTS.
    Selected Voice: en-US-AriaNeural (Clear, Professional, High-Density)
    """
    def __init__(self, output_dir="voice_logs"):
        self.voice = "en-US-AriaNeural"
        self.rate = "+0%"  # Standard speed
        self.volume = "+0%" # Standard volume
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Initialize Pygame Mixer
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[VOICE] Warning: Audio device not found. {e}")

    async def _generate_audio(self, text, output_file):
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        await communicate.save(output_file)

    def speak(self, text, filename=None):
        """
        Generates audio for the text and plays it immediately.
        """
        if filename is None:
            filename = f"speech_{int(datetime.now().timestamp())}.mp3"
        
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"[VOICE] Generating audio: '{text[:50]}...'")
        
        # Run Async Generation in Sync Context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        loop.run_until_complete(self._generate_audio(text, filepath))
        
        # Play Metadata
        self._play_file(filepath)
        
    def _play_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"[VOICE] Error: File {filepath} not found.")
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): 
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"[VOICE] Playback Error: {e}")
            
if __name__ == "__main__":
    voice = SovereignVoice()
    voice.speak("I am Sarah. The Sovereign System is online.")
