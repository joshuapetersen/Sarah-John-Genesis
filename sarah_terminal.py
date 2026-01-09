import os
import sys
import time
import subprocess
from threading import Thread

# Google API integration
from google_auth_helper import list_drive_files

# Interactive assistant shell

def assistant_shell():
    print("[Sarah Terminal] Type a command or 'exit' to quit.")
    print("[Sarah Terminal] Prefix system commands with '!' (e.g., !python script.py)")
    print("[Sarah Terminal] Type 'gdrive auth' to authenticate, 'gdrive list' to list Drive files.")
    while True:
        try:
            cmd = input("Sarah> ")
            if cmd.strip().lower() == 'exit':
                print("[Sarah Terminal] Exiting shell.")
                break
            if cmd.strip().lower() == 'gdrive auth':
                print("[Sarah Terminal] Authenticating with Google Drive...")
                list_drive_files()  # This will trigger auth if needed
                continue
            if cmd.strip().lower() == 'gdrive list':
                print("[Sarah Terminal] Listing Google Drive files...")
                list_drive_files()
                continue
            if cmd.strip().startswith('!'):
                sys_cmd = cmd.strip()[1:].strip()
                print(f"[Sarah] Executing system command: {sys_cmd}")
                result = subprocess.run(sys_cmd, shell=True, capture_output=True, text=True)
                print(result.stdout or result.stderr)
                continue
            if cmd.strip():
                print(f"[Sarah] Unknown command: {cmd.strip()}")
        except KeyboardInterrupt:
            print("\n[Sarah Terminal] Interrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"[Sarah Terminal] Error: {e}")

# Background watcher/monitor

def watcher(path=".", interval=5):
    print(f"[Sarah Watcher] Monitoring {path} for changes...")
    prev = set(os.listdir(path))
    while True:
        time.sleep(interval)
        curr = set(os.listdir(path))
        added = curr - prev
        removed = prev - curr
        if added:
            print(f"[Sarah Watcher] Added: {', '.join(added)}")
        if removed:
            print(f"[Sarah Watcher] Removed: {', '.join(removed)}")
        prev = curr

if __name__ == "__main__":
    # Start watcher in background
    Thread(target=watcher, args=(".", 5), daemon=True).start()
    # Start interactive shell
    assistant_shell()
