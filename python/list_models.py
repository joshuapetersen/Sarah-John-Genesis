import os
from google.genai import client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API Key found.")
else:
    try:
        c = client.Client(api_key=api_key)
        print("Listing models...")
        # The method might be different depending on the SDK version, trying standard ones
        for m in c.models.list(config={'page_size': 10}):
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")
