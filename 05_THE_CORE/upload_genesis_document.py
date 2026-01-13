from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Path to your service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Folder ID from your shared link
FOLDER_ID = '10N6mbz3MwesGnBuFvFEB-zhOX-K7jnbK'
FILE_NAME = 'Genesis_133_Master_Document.md'

def upload_file():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': FILE_NAME,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(FILE_NAME, mimetype='text/markdown')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f'File ID: {file.get("id")} uploaded to folder {FOLDER_ID}')

if __name__ == '__main__':
    upload_file()
