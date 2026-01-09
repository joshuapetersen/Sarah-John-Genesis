# Zone 0: Kernel - History Ingestion Protocol
# Ingests and archives system history for Sovereign review

import os
import datetime

class HistoryIngest:
    def __init__(self, history_dir="../archive_memories/history"):
        self.history_dir = os.path.abspath(history_dir)
        os.makedirs(self.history_dir, exist_ok=True)
        self.log_file = os.path.join(self.history_dir, f"history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    def ingest(self, data):
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {data}\n")
        return self.log_file

if __name__ == "__main__":
    ingest = HistoryIngest()
    # Example: Ingest a system event
    event = "Genesis Handshake confirmed. System unified."
    log_path = ingest.ingest(event)
    print(f"History ingested and archived at: {log_path}")
