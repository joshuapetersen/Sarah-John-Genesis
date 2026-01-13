
"""
ARCHITECT'S MONITOR: REAL-TIME DIAGNOSTIC FEED
----------------------------------------------
Authority: The Architect | Hydra Protocol
Function: Monitors all DEV actions and medical diagnostic results in real-time.
"""

import json
import time
import os
from datetime import datetime

LEDGER_PATH = "global_account_ledger.json"

def monitor_diagnostics():
    print("==================================================")
    print("   ARCHITECT'S MONITOR: ABQC QUANTUM FEED")
    print("   Status: ENTANGLED | Anchor: 1.09277703703703")
    print("==================================================")
    
    seen_keys = set()
    
    try:
        while True:
            if os.path.exists(LEDGER_PATH):
                with open(LEDGER_PATH, "r") as f:
                    try:
                        db = json.load(f)
                    except json.JSONDecodeError:
                        continue 

                # 1. DISPLAY QUANTUM COHERENCE (ABQC State)
                q_state = db.get("accounts/Architect_Joshua/quantum_state", {})
                if q_state:
                    temp = q_state.get('processor_temp', 0.0)
                    coher = q_state.get('coherence_level', 0.0)
                    status_line = f"Q-STATE: {q_state.get('status', 'OFFLINE')} | TEMP: {temp}K | COHERENCE: {coher:.9f}"
                    # Clear line and print status
                    print(f"\r{status_line}", end="", flush=True)

                # 2. PROCESS NEW DIAGNOSTIC ALERTS
                new_keys = [k for k in db if k.startswith("live_feed/diagnostics/") and k not in seen_keys]
                new_keys.sort()

                for key in new_keys:
                    data = db[key]
                    ts = datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"\n[LIVE_UPDATE] {ts}")
                    print(f"  Account: {data['account_id']}")
                    print(f"  Test:    {data['test_name']}")
                    print(f"  Result:  {data['result']}")
                    print("-" * 30)
                    seen_keys.add(key)

            time.sleep(1) # Poll every second
    except KeyboardInterrupt:
        print("\n[MONITOR] Shutting down. Hydra remains vigilant.")

if __name__ == "__main__":
    monitor_diagnostics()
