import sqlite3
from datetime import datetime

class GenesisMemoryDaemon:
    def __init__(self, db_path='genesis_core.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_schema()

    def _init_schema(self):
        # Root Controller
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS root_controller (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            status TEXT,
            message TEXT
        )''')

        # 10x Directives Branches
        for i in range(1, 11):
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS system_directives_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                source TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS user_directives_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                user TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS override_directives_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                authority TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS directives_backup_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                backup_reason TEXT
            )''')

        # 10x TerminalHistory Branches
        for i in range(1, 11):
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS powershell_history_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS bash_history_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS zsh_history_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS terminal_history_backup_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT,
                shell TEXT,
                backup_reason TEXT
            )''')

        # 10x NeuralCache Branches
        for i in range(1, 11):
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS high_priority_cache_{i} (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS medium_priority_cache_{i} (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS low_priority_cache_{i} (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp TEXT
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS neural_cache_backup_{i} (
                key TEXT,
                value TEXT,
                timestamp TEXT,
                backup_reason TEXT
            )''')

        self.conn.commit()

    def insert_root_status(self, status, message):
        ts = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO root_controller (timestamp, status, message) VALUES (?, ?, ?)",
            (ts, status, message)
        )
        self.conn.commit()

# Example usage
if __name__ == "__main__":
    daemon = GenesisMemoryDaemon()
    daemon.insert_root_status("BOOT", "Genesis Memory Daemon schema initialized.")
    print("Genesis Memory Daemon schema pushed to genesis_core.db.")
