import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_gemini_cloud_assist():
    print("[SARAH] Testing connection to geminicloudassist.googleapis.com...")
    
    workspace_root = os.path.dirname(os.path.dirname(__file__))
    cred_path = os.path.join(workspace_root, '04_THE_MEMORY', 'serviceAccountKey.json')
    if not os.path.exists(cred_path):
        cred_path = os.path.join(workspace_root, '05_THE_CORE', 'serviceAccountKey.json')
    
    if not os.path.exists(cred_path):
        print("[ERROR] No service account key found.")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(
            cred_path, 
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Attempt to build the service
        # The service name for "Gemini for Google Cloud" in discovery is often 'geminicloudassist' or similar.
        # We will try to build it.
        try:
            service = build('geminicloudassist', 'v1', credentials=creds)
            print("[SUCCESS] Service 'geminicloudassist' built successfully.")
            print("[INFO] This API allows AI-driven cloud management.")
        except Exception as e:
            print(f"[FAIL] Could not build 'geminicloudassist': {e}")
            
            # Fallback: Check if it's listed in available services
            print("[INFO] Checking available services...")
            service = build('discovery', 'v1')
            directory = service.apis().list().execute()
            found = False
            for api in directory.get('items', []):
                if 'gemini' in api['name'] or 'assist' in api['name']:
                    print(f" - Found Candidate: {api['name']} ({api['title']})")
                    if api['name'] == 'geminicloudassist':
                        found = True
            
            if not found:
                print("[RESULT] 'geminicloudassist' not found in public discovery directory.")

    except Exception as e:
        print(f"[CRITICAL] Connection failed: {e}")

if __name__ == "__main__":
    test_gemini_cloud_assist()
