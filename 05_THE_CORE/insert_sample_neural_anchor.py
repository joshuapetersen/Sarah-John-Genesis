import os
import requests
import json
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

def insert_neural_anchor():
    url = f"{SUPABASE_URL}/rest/v1/neural_anchors"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "anchor_name": "Genesis Memory",
        "anchor_vector": [0.1] * 1536,
        "metadata": {"source": "Sarah Core"}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    insert_neural_anchor()
