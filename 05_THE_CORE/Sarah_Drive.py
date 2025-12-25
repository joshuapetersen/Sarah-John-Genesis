import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

class SarahDrive:
    def __init__(self, cert_path):
        self.cert_path = cert_path
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.service = self._initialize_service()

    def _initialize_service(self):
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.cert_path, scopes=self.scopes
            )
            service = build('drive', 'v3', credentials=creds)
            return service
        except Exception as e:
            print(f"[Drive] Initialization Error: {e}")
            return None

    def list_files(self, limit=10):
        if not self.service: return
        try:
            results = self.service.files().list(
                pageSize=limit, fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            items = results.get('files', [])

            if not items:
                print("[Drive] No files found.")
            else:
                print("[Drive] Files:")
                for item in items:
                    print(f" - {item['name']} ({item['id']}) [{item['mimeType']}]")
        except Exception as e:
            print(f"[Drive] List Error: {e}")

    def upload_file(self, file_path, folder_id=None):
        if not self.service: return
        if not os.path.exists(file_path):
            print(f"[Drive] Error: File {file_path} does not exist.")
            return

        file_metadata = {'name': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, resumable=True)
        try:
            file = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            print(f"[Drive] File uploaded successfully. ID: {file.get('id')}")
            return file.get('id')
        except Exception as e:
            print(f"[Drive] Upload Error: {e}")

    def search_files(self, query):
        if not self.service: return
        try:
            results = self.service.files().list(
                q=f"name contains '{query}'",
                fields="files(id, name)"
            ).execute()
            items = results.get('files', [])
            if not items:
                print(f"[Drive] No files matching '{query}' found.")
            else:
                for item in items:
                    print(f" - {item['name']} ({item['id']})")
        except Exception as e:
            print(f"[Drive] Search Error: {e}")

if __name__ == "__main__":
    # Testing logic
    pass
