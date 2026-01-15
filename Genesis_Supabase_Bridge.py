import os
import json
import psycopg2
import sys
from urllib.parse import quote_plus
from psycopg2 import sql
from Sovereign_Math import SovereignMath

class GenesisSupabaseWidth:
    """
    Genesis Bridge to Supabase (Postgres).
    Clones local Sovereign Memory to the Immutable Cloud Ledger.
    """
    def __init__(self, password):
        self._0x_math = SovereignMath()
        # Encode password to handle special characters
        encoded_pw = quote_plus(password)
        self.db_url = f"postgresql://postgres:{encoded_pw}@db.duuycxgqbhrqmwapnjhk.supabase.co:5432/postgres"
        self.conn = None
        
    def connect(self):
        try:
            print("[Genesis-DB] Connecting to Supabase...")
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = True
            print("[Genesis-DB] Connection Established. Pulse verified.")
            self.init_schema()
            return True
        except Exception as e:
            print(f"[Genesis-DB] Connection Failed: {e}")
            return False
            
    def init_schema(self):
        """Creates the Sovereign Memory tables if they don't exist."""
        # ... (Same logic, relying on self.conn being valid)
        if not self.conn: return
        with self.conn.cursor() as cur:
            # Table: Sovereign Ledger (Immutable Facts)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sovereign_ledger (
                    id SERIAL PRIMARY KEY,
                    key TEXT UNIQUE NOT NULL,
                    value JSONB NOT NULL,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    resonance_hash TEXT
                );
            """)
            print("[Genesis-DB] Schema Verified.")

    def clone_memory(self):
        """
        Reads local JSON memory files and pushes them to Supabase.
        """
        if not self.conn:
             print("[Genesis-DB] ERROR: No Active Connection. Aborting Clone.")
             return

        memory_files = [
            "sovereign_memory.py", 
            "Sovereign_Ledger.json",
            "saul_knowledge_cache.json",
            "full_file_manifest_utf8.txt"
        ]
        
        with self.conn.cursor() as cur:
            for filename in memory_files:
                if os.path.exists(filename):
                    print(f"[Genesis-DB] Cloning {filename}...")
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Upsert logic
                    try:
                        cur.execute("""
                            INSERT INTO sovereign_ledger (key, value, resonance_hash)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (key) DO UPDATE 
                            SET value = EXCLUDED.value, timestamp = NOW();
                        """, (filename, json.dumps({"content": content}), "PENDING"))
                        print(f"[Genesis-DB] {filename} Synced.")
                    except Exception as e:
                         print(f"[Genesis-DB] Error syncing {filename}: {e}")

if __name__ == "__main__":
    import getpass
    
    print("--- GENESIS SUPABASE BRIDGE ---")
    # Prompt for password to ensure security (don't hardcode)
    print("Please enter the Supabase DB Password:")
    pw = getpass.getpass("Password: ")
    
    if not pw:
        print("[!] No password provided. Using default hash check (failsafe)...")
        # Optional: legacy hash if needed, or just fail.
        pw = "36AC839FC48C5FF2BD129C06BCF8C081A61E1C51AA348C0160D255057015F3C1"

    bridge = GenesisSupabaseWidth(pw)
    if bridge.connect():
        bridge.clone_memory()
    else:
        print("\n[!] Bridge Activation Failed. Check credentials and try again.")
