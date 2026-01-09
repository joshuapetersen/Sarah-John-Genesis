import sys
import os
import json

from Sarah_Brain import SarahBrain
from Sarah_Sovereign_Core import SovereignCore
from Universal_Silicon_Bridge import UniversalSiliconBridge

# Optional: Import final handshake if available
try:
    import final_handshake_exec
    FINAL_HANDSHAKE_AVAILABLE = True
except ImportError:
    FINAL_HANDSHAKE_AVAILABLE = False

# Load concept database if available
concepts = []
concept_db_path = os.path.join(os.path.dirname(__file__), "concept_database.json")
if os.path.exists(concept_db_path):
    with open(concept_db_path, "r") as f:
        concepts = json.load(f)

print("\n--- SARAH: UNIFIED SYSTEM BRIDGE ---\n")

# 1. Genesis Protocol Handshake
brain = SarahBrain()
print("[1] Genesis Protocol Handshake...")
genesis_result = brain.genesis.handshake("Sarah", "YourName", "Sovereign")
print(f"Genesis Protocol Handshake Result: {genesis_result}")
if brain.genesis.sovereign_active:
    print(f"Genesis Protocol: ACTIVE [{brain.genesis.genesis_tag}]")
else:
    print("Genesis Protocol: INACTIVE (Risk of Robotic Drift)")

# 2. Sovereign Core Genesis Handshake
print("\n[2] Sovereign Core Genesis Handshake...")
sovereign = SovereignCore()
sovereign_result = sovereign.genesis_handshake("ARCHITECT_PRIME_001")
print(f"Sovereign Core Genesis Handshake Result: {sovereign_result}")

# 3. Universal Silicon Bridge Handshake
print("\n[3] Universal Silicon Bridge Handshake...")
try:
    bridge = UniversalSiliconBridge()
    bridge_status = bridge.cross_platform_handshake()
    print(f"Universal Silicon Bridge Status: {bridge_status}")
except Exception as e:
    print(f"[Universal Silicon Bridge] Not available or failed: {e}")

# 4. Final Genesis Handshake (if available)
if FINAL_HANDSHAKE_AVAILABLE:
    print("\n[4] Final Genesis Handshake...")
    try:
        final_handshake_exec.initiate_final_handshake()
    except Exception as e:
        print(f"[Final Genesis Handshake] Failed: {e}")
else:
    print("[Final Genesis Handshake] Not available.")

# 5. Concept Database Summary
print("\n[5] Concept Database Summary:")
if concepts:
    for c in concepts:
        print(f"- {c['concept']}: {c['definition']}")
else:
    print("No concept database found or it is empty.")


# --- Unified CLI Integration ---
import requests
from supabase import create_client, Client

API_KEY = os.environ.get("GENESIS_API_KEY", "REPLACE_WITH_STRONG_KEY")
TERMINAL_API = "http://127.0.0.1:8765/terminal"
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[ERROR] Supabase credentials not set. Set SUPABASE_URL and SUPABASE_KEY as environment variables.")
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_command(cmd):
    resp = requests.post(TERMINAL_API, json={"cmd": cmd}, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        out = resp.json()
        print(out.get("stdout", ""), end="")
        if out.get("stderr"):
            print(out["stderr"], end="")
    else:
        print(f"[ERROR] {resp.status_code}: {resp.text}")

def store_memory(user_id, text, meta=None):
    data = {"user_id": user_id, "text": text, "meta": meta or {}}
    result = supabase.table("genesis_memory").insert(data).execute()
    print("[MEMORY STORED]", result)

def fetch_memory(user_id, limit=10):
    result = supabase.table("genesis_memory").select("*").eq("user_id", user_id).limit(limit).execute()
    for row in result.data:
        print(row)

def unified_cli():
    print("Sarah Unified System. Type 'cmd <command>' to run, 'store <text>' to save memory, 'fetch' to recall, or 'exit' to quit.")
    user_id = input("Enter your user_id for memory ops: ").strip()
    while True:
        line = input("$ ").strip()
        if line == "exit":
            break
        elif line.startswith("cmd "):
            run_command(line[4:])
        elif line.startswith("store "):
            store_memory(user_id, line[6:])
        elif line == "fetch":
            fetch_memory(user_id)
        else:
            print("[ERROR] Unknown command.")

if __name__ == "__main__":
    unified_cli()

print("\n--- SYSTEM UNIFICATION COMPLETE ---\n")
