"""
GOOGLE DRIVE BRIDGE
Integrates Sarah Prime with the Google Drive Knowledge Base.
Allows reading of Sovereign Documents and Genesis Core equations.
"""

import os
import pickle
import logging
from typing import List, Dict, Optional, Any
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [GDRIVE] - %(message)s')

class GoogleDriveBridge:
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    CREDENTIALS_PATH = os.path.join('04_THE_MEMORY', 'credentials.json')
    TOKEN_PATH = 'token.pickle'

    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticates with Google API using OAuth2."""
        creds = None
        try:
            if os.path.exists(self.TOKEN_PATH):
                with open(self.TOKEN_PATH, 'rb') as token:
                    creds = pickle.load(token)
                    logging.info(f"Loaded credentials with scopes: {creds.scopes}")
            
            # Check if scopes match
            if creds and not set(self.SCOPES).issubset(set(creds.scopes)):
                logging.warning(f"Scopes mismatch. Required: {self.SCOPES}, Found: {creds.scopes}. Forcing re-authentication.")
                creds = None

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.CREDENTIALS_PATH):
                        logging.error(f"Credentials file not found at {self.CREDENTIALS_PATH}")
                        return

                    flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_PATH, self.SCOPES)
                    # Use fixed port 8080 to match Google Cloud Console configuration
                    creds = flow.run_local_server(port=8080)
                
                with open(self.TOKEN_PATH, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('drive', 'v3', credentials=creds)
            logging.info("Authentication successful.")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")

    def list_files(self, page_size: int = 10) -> List[Dict[str, str]]:
        """Lists files from Google Drive."""
        if not self.service:
            logging.warning("Service not initialized. Attempting re-auth.")
            self.authenticate()
            if not self.service:
                return []

        try:
            results = self.service.files().list(
                pageSize=page_size, 
                fields="files(id, name, mimeType)"
            ).execute()
            return results.get('files', [])
        except Exception as e:
            logging.error(f"List files failed: {e}")
            return []

    def read_file_content(self, file_id: str) -> str:
        """
        Reads content of a file. 
        Exports Google Docs to plain text.
        Downloads text/markdown files directly.
        """
        if not self.service:
            return "Error: Service not initialized."

        try:
            # Get file metadata to check mimeType
            file_meta = self.service.files().get(fileId=file_id).execute()
            mime_type = file_meta.get('mimeType')

            if mime_type == 'application/vnd.google-apps.document':
                # Export Google Doc to plain text
                request = self.service.files().export_media(
                    fileId=file_id,
                    mimeType='text/plain'
                )
            else:
                # Download binary/text content
                request = self.service.files().get_media(fileId=file_id)

            content = request.execute()
            return content.decode('utf-8')
        except Exception as e:
            logging.error(f"Read file failed: {e}")
            return f"Error reading file: {str(e)}"

    def search_files(self, query: str) -> List[Dict[str, str]]:
        """Searches for files by name."""
        if not self.service:
            return []
        
        try:
            # Escape single quotes in query
            safe_query = query.replace("'", "\\'")
            q = f"name contains '{safe_query}' and trashed = false"
            results = self.service.files().list(
                q=q,
                pageSize=10,
                fields="files(id, name, mimeType)"
            ).execute()
            return results.get('files', [])
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []

if __name__ == "__main__":
    bridge = GoogleDriveBridge()
    files = bridge.list_files()
    print("Files found:")
    for f in files:
        print(f"- {f['name']} ({f['id']})")
