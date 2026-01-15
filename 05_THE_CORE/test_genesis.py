
import os
import sys
try:
    from dotenv import load_dotenv
    load_dotenv("c:\\SarahCore\\.env")
except ImportError:
    pass

from Gemini_Genesis_Core import GeminiGenesisCore

def test():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("No Key found.")
        return

    core = GeminiGenesisCore(key, model_id="gemini-1.5-flash")
    print("Sending request 'ping' to gemini-1.5-flash...")
    # Add manual sleep to respect rate limit if previous calls failed
    import time
    time.sleep(2) 
    response = core.generate_content_safe("ping")
    print(f"Response: {response}")

if __name__ == "__main__":
    test()
