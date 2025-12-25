import os
import time
import firebase_admin
from firebase_admin import credentials, db

class UpdateChecker:
    def __init__(self):
        workspace_root = os.path.dirname(os.path.dirname(__file__))
        cert_path = os.path.join(workspace_root, '04_THE_MEMORY', 'serviceAccountKey.json')
        if not os.path.exists(cert_path):
            cert_path = os.path.join(workspace_root, '05_THE_CORE', 'serviceAccountKey.json')
        
        self.rtdb_url = 'https://sarah-john-genesis-default-rtdb.firebaseio.com/'
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.rtdb_url
            })
            
    def check_for_updates(self):
        print("[SARAH] Scanning Mesh for New Code/Instructions...")
        
        # Check Android Node
        try:
            android_ref = db.reference('nodes/android')
            android_data = android_ref.get()
            if android_data:
                print(f"[FOUND] Android Node Signal: {android_data}")
            else:
                print("[INFO] No signal from Android Node.")
        except Exception as e:
            print(f"[ERROR] Failed to check Android Node: {e}")

        # Check Beta Node (Self)
        try:
            beta_ref = db.reference('nodes/beta')
            beta_data = beta_ref.get()
            if beta_data:
                print(f"[FOUND] Beta Node State: {beta_data}")
        except Exception as e:
            print(f"[ERROR] Failed to check Beta Node: {e}")

if __name__ == "__main__":
    checker = UpdateChecker()
    checker.check_for_updates()
