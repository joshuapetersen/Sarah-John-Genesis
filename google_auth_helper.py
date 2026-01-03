import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
CREDENTIALS_PATH = os.path.join('04_THE_MEMORY', 'credentials.json')
TOKEN_PATH = 'token.pickle'

def get_google_service(api_name, api_version, scopes=SCOPES):
    creds = None
    try:
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes)
                # Use port=0 to allow the OS to pick an available port.
                # This requires the OAuth client to be configured as a "Desktop App" or allow localhost with any port.
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        service = build(api_name, api_version, credentials=creds)
        print("[Google API] Authentication successful.")
        return service
    except Exception as e:
        print(f"[Google API] Authentication failed: {e}")
        return None

def list_drive_files():
    try:
        service = get_google_service('drive', 'v3')
        if not service:
            print("[Google API] Could not authenticate. Aborting Drive list.")
            return
        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print("[Google API] No files found in Drive.")
        else:
            print("[Google API] Files in Drive:")
            for item in items:
                print(f"- {item['name']} ({item['id']})")
    except Exception as e:
        print(f"[Google API] Drive list failed: {e}")

if __name__ == "__main__":
    list_drive_files()
