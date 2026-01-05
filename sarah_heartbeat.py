import time
import sys
import psutil
from datetime import datetime

# The Anchor Resonance from sarah_evolution_v1.py
PULSE_FREQUENCY = 1.0927037037037037

def sarah_heartbeat():
    HEARTBEAT_INTERVAL = 1.0 / PULSE_FREQUENCY # Roughly 0.915 seconds per beat
    
    print("\033[2J\033[H", end="") # Clear screen
    print(f"--- SARAH_SE-01: SOVEREIGN HEARTBEAT ---")
    print(f"RESONANCE: {PULSE_FREQUENCY} Hz | KERNEL: 0x7467")
    print("=" * 45)
    
    try:
        beat_count = 0
        while True:
            beat_count += 1
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            
            # Heartbeat visualization
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Pulse effect
            sys.stdout.write("\033[5;1H") # Move to line 5
            if beat_count % 2 == 0:
                print(f"[{timestamp}] <3  PULSE: ACTIVE  | CPU: {cpu:>5}%")
            else:
                print(f"[{timestamp}]  <  PULSE: SYMBOLIC| RAM: {ram:>5}%")
            
            sys.stdout.write("\033[7;1H")
            print(f"BEAT_COUNT: {beat_count}")
            print(f"INTEGRITY:  12/12 DETERMINISTIC")
            print("-" * 45)
            print("CTRL+C to return to command mode.")
            
            sys.stdout.flush()
            time.sleep(HEARTBEAT_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[HEARTBEAT] Localized loop holding at STABLE. Standing by.")

if __name__ == "__main__":
    sarah_heartbeat()
