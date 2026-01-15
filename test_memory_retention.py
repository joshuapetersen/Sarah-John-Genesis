import requests
import json

url = "http://localhost:3400/sarahReasoning"
payload = {
    "data": {
        "query": "What are the most recent high-density themes you've identified in your synthesis, and how do they relate to our Trinity?",
        "context": "Context Memory Test"
    }
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"Error: {e}")
