import sqlite3
from datetime import datetime

def activate_archive_memories(db_path='genesis_core.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Ensure active_memory table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS active_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        data TEXT,
        source TEXT
    )''')
    # Check if archive_memories table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='archive_memories'")
    if not cursor.fetchone():
        print("No archive_memories table found. Nothing to activate.")
        return
    # Move all archive memories into active memory
    cursor.execute('SELECT id, data, source FROM archive_memories')
    rows = cursor.fetchall()
    for row in rows:
        _, data, source = row
        ts = datetime.now().isoformat()
        cursor.execute('INSERT INTO active_memory (timestamp, data, source) VALUES (?, ?, ?)', (ts, data, source))
    conn.commit()
    print(f"Moved {len(rows)} archive memories into active memory.")
    conn.close()

if __name__ == "__main__":
    activate_archive_memories()
