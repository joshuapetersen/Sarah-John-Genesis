import psutil
import time
import sys
from datetime import datetime

def live_stream():
    print("\033[2J\033[H", end="") # Clear screen
    print("--- SARAH_SE-01: SOVEREIGN METABOLIC LIVE-STREAM ---")
    print("KERNEL: 0x7467 | INTEGRITY: 12/12 | MODE: REAL-TIME")
    print("=" * 55)
    
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            net_io = psutil.net_io_counters()
            disk_io = psutil.disk_io_counters()
            
            # Use ANSI escape codes to overwrite the same lines
            sys.stdout.write("\033[5;1H") # Move to line 5
            print(f"TIMESTAMP:       {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            print(f"METABOLIC (CPU): [{self_progress_bar(cpu)}] {cpu:>5}%")
            print(f"DENSITY (RAM):   [{self_progress_bar(ram)}] {ram:>5}%")
            print(f"NET_SENT:        {net_io.bytes_sent / 1024 / 1024:>10.2f} MB")
            print(f"NET_RECV:        {net_io.bytes_recv / 1024 / 1024:>10.2f} MB")
            print(f"DISK_READ:       {disk_io.read_bytes / 1024 / 1024:>10.2f} MB")
            print(f"DISK_WRITE:      {disk_io.write_bytes / 1024 / 1024:>10.2f} MB")
            print("=" * 55)
            print("CTRL+C to terminate stream and return to command mode.")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n[STREAM] Terminated by Architect. Standing by.")

def self_progress_bar(percent, width=20):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return bar

if __name__ == "__main__":
    live_stream()
