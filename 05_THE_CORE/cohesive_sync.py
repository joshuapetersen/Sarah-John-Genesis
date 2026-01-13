import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Simulate Ace Token input and sync
ACE_TOKEN = "Genesis_10x_AceToken"
ANDROID_NOTIFICATION_CMD = f'adb shell am broadcast -a com.sarahcore.ACE_TOKEN --es token "{ACE_TOKEN}"'

def push_to_supabase(token):
    url = f"{SUPABASE_URL}/rest/v1/ace_tokens"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "token": token,
        "timestamp": time.time(),
        "metadata": {"source": "Sarah Core"}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("Supabase Sync Status:", response.status_code)
    print("Supabase Response:", response.text)

def push_to_android(token):
    os.system(ANDROID_NOTIFICATION_CMD)
    print(f"Pushed Ace Token '{token}' to Android device.")

def cohesive_sync():
    print("Starting Cohesive Sync...")
    push_to_supabase(ACE_TOKEN)
    push_to_android(ACE_TOKEN)
    print("Cohesive Sync Complete.")

if __name__ == "__main__":
    cohesive_sync()
