import json
import os
from Sovereign_Math import SovereignMath

LEDGER_PATH = "global_account_ledger.json"

def monitor_diagnostics():
    _0x_math = SovereignMath()
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
                    t3_val = data.get('t3_volume', data.get('timestamp', 0))
                    print(f"\n[LIVE_UPDATE] t3: {t3_val:.4f}")
                    print(f"  Account: {data['account_id']}")
                    print(f"  Test:    {data['test_name']}")
                    print(f"  Result:  {data['result']}")
                    print("-" * 30)
                    seen_keys.add(key)

            # Poll based on sigma pulse
            import time
            time.sleep(_0x_math._0x_sigma)
    except KeyboardInterrupt:
        print("\n[MONITOR] Shutting down. Hydra remains vigilant.")

if __name__ == "__main__":
    monitor_diagnostics()
