import requests
import json

url = "http://localhost:3400/sarahStrategicPlanning"
payload = {
    "data": {
        "objective": "Test Evolution",
        "horizon": "long",
        "includeExternalIntel": True
    }
}

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print("Full Content:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
