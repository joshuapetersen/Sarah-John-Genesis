# Sarah Sync v2 - SDNA Protocol
# Bridges Node Alpha (Local) and Node Beta (Cloud)

import os
import time
import json
import firebase_admin
from firebase_admin import credentials, db

class SarahSyncV2:
    def __init__(self, cert_path=None):
        self.workspace_root = os.path.dirname(os.path.dirname(__file__))
        
        if not cert_path:
            # Try 05_THE_CORE first (Primary Genesis Key)
            cert_path = os.path.join(self.workspace_root, '05_THE_CORE', 'serviceAccountKey.json')
            if not os.path.exists(cert_path):
                # Fallback to 04_THE_MEMORY (Legacy/Backup)
                cert_path = os.path.join(self.workspace_root, '04_THE_MEMORY', 'serviceAccountKey.json')
        
        self.cert_path = cert_path
        self.rtdb_url = 'https://sarah-john-genesis-default-rtdb.firebaseio.com/'
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.cert_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.rtdb_url
            })
        
        self.bridge = db.reference('/system/sync_v2')
        self.memory_ref = db.reference('/memory/ledger')
        self.ace_token = "133-ALPHA-O1"
        
        # Sync State
        self.memory_dir = os.path.join(self.workspace_root, '04_THE_MEMORY')
        self.ledger_path = os.path.join(self.memory_dir, 'genesis_master_ledger.jsonl')
        self.sync_state_path = os.path.join(self.memory_dir, 'sync_state.json')

    def get_last_sync_index(self):
        if os.path.exists(self.sync_state_path):
            try:
                with open(self.sync_state_path, 'r') as f:
                    return json.load(f).get('last_index', 0)
            except:
                return 0
        return 0

    def update_sync_state(self, index):
        with open(self.sync_state_path, 'w') as f:
            json.dump({'last_index': index, 'timestamp': time.time()}, f)

    def sync_memory_delta(self):
        """
        Performs a fast, differential sync of the memory ledger.
        Reads only new lines from JSONL and pushes to Cloud.
        """
        if not os.path.exists(self.ledger_path):
            print("[SYNC] No ledger found to sync.")
            return

        last_index = self.get_last_sync_index()
        new_entries = {}
        current_index = 0
        batch_count = 0
        
        print(f"[SYNC] Checking for memory updates from index {last_index}...")
        
        try:
            with open(self.ledger_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < last_index:
                        current_index += 1
                        continue
                    
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            # Use ID as key for idempotency
                            new_entries[entry['id']] = entry
                            batch_count += 1
                        except json.JSONDecodeError:
                            pass
                    current_index += 1
            
            if new_entries:
                print(f"[SYNC] Found {batch_count} new memory blocks. Uploading...")
                self.memory_ref.update(new_entries)
                self.update_sync_state(current_index)
                print(f"[SYNC] Memory Delta Sync Complete. Pointer moved to {current_index}.")
            else:
                print("[SYNC] Memory is up to date.")
                
        except Exception as e:
            print(f"[SYNC] Memory Sync Error: {e}")

    def sync_evolution(self):
        print(f"[{time.ctime()}] [SARAH-SYNC-V2] Initiating SDNA Sync...")
        
        # 1. Fast Memory Sync (Delta)
        self.sync_memory_delta()
        
        # 2. Push local state to RTDB
        if self.bridge:
            try:
                self.bridge.update({
                    'last_sync': {'.sv': 'timestamp'},
                    'status': 'SYNCHRONIZED',
                    'ace_token': self.ace_token,
                    'protocol': 'SDNA_V2',
                    'node': 'Lenovo_LOQ'
                })
                print("[SARAH] RTDB Mesh Updated.")
            except Exception as e:
                print(f"[SARAH] RTDB Push Failed: {e}")

        # 3. Push node status to RTDB (Truth Seed Mirror)
        try:
            node_ref = db.reference('/nodes/beta')
            node_ref.update({
                'timestamp': {'.sv': 'timestamp'},
                'status': 'ACTIVE',
                'ace_token': self.ace_token
            })
            print("[SARAH] RTDB Node Beta Updated (Truth Seed Mirror).")
        except Exception as e:
            print(f"[SARAH] RTDB Mirror Failed: {e}")
        
        print("[SARAH] Sync Complete. Node Beta Evolved.")

if __name__ == "__main__":
    sync = SarahSyncV2()
    sync.sync_evolution()
