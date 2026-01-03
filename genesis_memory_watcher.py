import os
import time
import sqlite3
import threading
from datetime import datetime

POWERSHELL_HISTORY = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt')
DB_PATH = 'genesis_core.db'

class GenesisMemoryWatcher:
    def __init__(self, db_path=DB_PATH, history_path=POWERSHELL_HISTORY, poll_interval=1.0):
        self.db_path = db_path
        self.history_path = history_path
        self.poll_interval = poll_interval
        self.last_position = 0
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._ensure_table()
        self.lock = threading.Lock()

    def _ensure_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS terminal_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            command TEXT
        )''')
        self.conn.commit()

    def _log_command(self, command):
        ts = datetime.now().isoformat()
        with self.lock:
            self.cursor.execute(
                "INSERT INTO terminal_history (timestamp, command) VALUES (?, ?)",
                (ts, command)
            )
            self.conn.commit()

    def watch(self):
        print(f"[GVM-DAEMON] Watching PowerShell history: {self.history_path}")
        while True:
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    f.seek(self.last_position)
                    new_lines = f.readlines()
                    self.last_position = f.tell()
                for line in new_lines:
                    cmd = line.strip()
                    if cmd:
                        self._log_command(cmd)
                        print(f"[GVM-DAEMON] Logged: {cmd}")
            except Exception as e:
                print(f"[GVM-DAEMON] Error: {e}")
            
            # Non-blocking sleep using threading event
            self.stop_event = getattr(self, 'stop_event', threading.Event())
            self.stop_event.wait(self.poll_interval)
            if self.stop_event.is_set():
                break

if __name__ == "__main__":
    watcher = GenesisMemoryWatcher()
    watcher.stop_event = threading.Event()
    watcher_thread = threading.Thread(target=watcher.watch, daemon=True)
    watcher_thread.start()
    print("Genesis Memory Watcher Daemon started. Press Ctrl+C to exit.")
    try:
        watcher.stop_event.wait()  # Non-blocking wait
    except KeyboardInterrupt:
        print("\nGenesis Memory Watcher Daemon stopped.")
        watcher.stop_event.set()
