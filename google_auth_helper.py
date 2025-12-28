import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/documents.readonly'
]
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

# --- Gmail ---
def list_gmail_messages():
    try:
        service = get_google_service('gmail', 'v1', ['https://www.googleapis.com/auth/gmail.readonly'])
        if not service:
            print("[Google API] Could not authenticate. Aborting Gmail list.")
            return
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        if not messages:
            print("[Google API] No messages found in Gmail.")
        else:
            print("[Google API] Gmail messages (IDs):")
            for msg in messages:
                print(f"- {msg['id']}")
    except Exception as e:
        print(f"[Google API] Gmail list failed: {e}")

# --- Calendar ---
def list_calendar_events():
    try:
        service = get_google_service('calendar', 'v3', ['https://www.googleapis.com/auth/calendar.readonly'])
        if not service:
            print("[Google API] Could not authenticate. Aborting Calendar list.")
            return
        now = '2025-01-01T00:00:00Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print("[Google API] No upcoming events found.")
        else:
            print("[Google API] Upcoming events:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"- {start}: {event.get('summary', 'No Title')}")
    except Exception as e:
        print(f"[Google API] Calendar list failed: {e}")

# --- Docs ---
def list_docs_files():
    try:
        service = get_google_service('drive', 'v3', ['https://www.googleapis.com/auth/drive.metadata.readonly'])
        if not service:
            print("[Google API] Could not authenticate. Aborting Docs list.")
            return
        results = service.files().list(q="mimeType='application/vnd.google-apps.document'", pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print("[Google API] No Google Docs found.")
        else:
            print("[Google API] Google Docs:")
            for item in items:
                print(f"- {item['name']} ({item['id']})")
    except Exception as e:
        print(f"[Google API] Docs list failed: {e}")

if __name__ == "__main__":
    list_drive_files()
