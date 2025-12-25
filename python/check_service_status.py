import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_service_status():
    print("[SARAH] Checking Service Status: geminicloudassist.googleapis.com")
    
    workspace_root = os.path.dirname(os.path.dirname(__file__))
    cred_path = os.path.join(workspace_root, '04_THE_MEMORY', 'serviceAccountKey.json')
    if not os.path.exists(cred_path):
        cred_path = os.path.join(workspace_root, '05_THE_CORE', 'serviceAccountKey.json')
    
    if not os.path.exists(cred_path):
        print("[ERROR] No service account key found.")
        return

    try:
        # Load credentials to get project ID
        with open(cred_path, 'r') as f:
            key_data = json.load(f)
            project_id = key_data.get('project_id')
            
        print(f"[INFO] Project ID: {project_id}")

        creds = service_account.Credentials.from_service_account_file(
            cred_path, 
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        service = build('serviceusage', 'v1', credentials=creds)
        
        service_name = f"projects/{project_id}/services/geminicloudassist.googleapis.com"
        
        try:
            request = service.services().get(name=service_name)
            response = request.execute()
            
            state = response.get('state')
            print(f"[RESULT] Service: {response.get('config', {}).get('name', 'Unknown')}")
            print(f"[RESULT] State: {state}")
            
            if state == 'ENABLED':
                print("[SUCCESS] Gemini Cloud Assist is ACTIVE.")
            else:
                print("[INFO] Service is NOT enabled.")
                
        except Exception as e:
            print(f"[FAIL] Could not check service status: {e}")

    except Exception as e:
        print(f"[CRITICAL] Execution failed: {e}")

if __name__ == "__main__":
    check_service_status()
