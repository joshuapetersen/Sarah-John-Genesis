import sqlite3
from datetime import datetime
import json
from collections import defaultdict

class MemoryPatternAnalyzer:
    """Enhanced memory system with pattern recognition and learning."""
    def __init__(self):
        self.pattern_index = defaultdict(list)
        self.learning_matrix = {}
        self.context_cache = {}
        
    def extract_patterns(self, memory_entries):
        """Extract meaningful patterns from memory entries."""
        patterns = defaultdict(int)
        for entry in memory_entries:
            # Extract keywords and topics
            if isinstance(entry, dict) and 'content' in entry:
                content = entry['content'].lower()
                # Simple pattern extraction
                if 'error' in content or 'fail' in content:
                    patterns['error_type'] += 1
                if 'success' in content or 'pass' in content:
                    patterns['success_pattern'] += 1
                if 'user' in content:
                    patterns['user_interaction'] += 1
        return patterns
    
    def rank_by_relevance(self, query, memories):
        """Rank memories by relevance to current query."""
        ranked = []
        query_lower = query.lower()
        for mem in memories:
            relevance = 0
            if isinstance(mem, dict):
                content = str(mem.get('content', '')).lower()
                # Keyword matching
                words = query_lower.split()
                relevance = sum(1 for word in words if word in content)
                # Recency bonus
                if 'timestamp' in mem:
                    ranked.append((mem, relevance, mem.get('timestamp')))
        return sorted(ranked, key=lambda x: (-x[1], -str(x[2])))

class GenesisMemoryDaemon:
    """Enhanced memory daemon with learning and pattern recognition."""
    
    def __init__(self, db_path='genesis_core.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.analyzer = MemoryPatternAnalyzer()
        self._init_schema()
        self._init_learning_tables()

    def _init_schema(self):
        """Initialize core memory schema (10x branches for redundancy)."""
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
                source TEXT,
                priority INTEGER DEFAULT 5
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS user_directives_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                user TEXT,
                confidence REAL DEFAULT 0.5
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS override_directives_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                directive TEXT,
                authority TEXT,
                reason TEXT
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
                command TEXT,
                exit_code INTEGER
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS bash_history_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT,
                exit_code INTEGER
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS zsh_history_{i} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                command TEXT,
                exit_code INTEGER
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
                timestamp TEXT,
                hit_count INTEGER DEFAULT 0
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS medium_priority_cache_{i} (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp TEXT,
                hit_count INTEGER DEFAULT 0
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS low_priority_cache_{i} (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp TEXT,
                hit_count INTEGER DEFAULT 0
            )''')
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS neural_cache_backup_{i} (
                key TEXT,
                value TEXT,
                timestamp TEXT,
                backup_reason TEXT
            )''')

        self.conn.commit()
    
    def _init_learning_tables(self):
        """Initialize learning and analytics tables."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS learning_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            pattern TEXT,
            confidence REAL,
            frequency INTEGER,
            last_updated TEXT
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS context_cache (
            context_key TEXT PRIMARY KEY,
            context_value TEXT,
            timestamp TEXT,
            relevance_score REAL DEFAULT 0.5,
            access_count INTEGER DEFAULT 0
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pattern_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT,
            pattern_data TEXT,
            timestamp TEXT,
            confidence REAL
        )''')
        
        self.conn.commit()

    def insert_root_status(self, status, message):
        """Insert status into root controller."""
        ts = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO root_controller (timestamp, status, message) VALUES (?, ?, ?)",
            (ts, status, message)
        )
        self.conn.commit()
    
    def insert_directive(self, directive_text, source="SYSTEM", priority=5, branch_id=1):
        """Insert directive with priority weighting."""
        ts = datetime.now().isoformat()
        table = f"system_directives_{branch_id}"
        self.cursor.execute(
            f"INSERT INTO {table} (timestamp, directive, source, priority) VALUES (?, ?, ?, ?)",
            (ts, directive_text, source, priority)
        )
        self.conn.commit()
    
    def learn_from_interactions(self, interaction_data):
        """Extract and store learning patterns from interactions."""
        ts = datetime.now().isoformat()
        for pattern_type, pattern_value in interaction_data.items():
            self.cursor.execute(
                "INSERT INTO learning_matrix (timestamp, pattern, confidence, frequency, last_updated) VALUES (?, ?, ?, ?, ?)",
                (ts, pattern_type, 0.7, 1, ts)
            )
        self.conn.commit()
    
    def cache_context(self, context_key, context_value, relevance_score=0.8):
        """Cache context with relevance scoring."""
        ts = datetime.now().isoformat()
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO context_cache (context_key, context_value, timestamp, relevance_score) VALUES (?, ?, ?, ?)",
                (context_key, json.dumps(context_value) if isinstance(context_value, dict) else str(context_value), ts, relevance_score)
            )
            self.conn.commit()
        except Exception as e:
            print(f"[Memory] Context cache error: {e}")
    
    def retrieve_relevant_context(self, query, limit=5):
        """Retrieve most relevant cached contexts for a query."""
        try:
            self.cursor.execute(
                "SELECT context_key, context_value, relevance_score FROM context_cache ORDER BY relevance_score DESC LIMIT ?",
                (limit,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[Memory] Context retrieval error: {e}")
            return []
    
    def get_learning_summary(self):
        """Get summary of learned patterns."""
        try:
            self.cursor.execute("SELECT pattern, confidence, frequency FROM learning_matrix ORDER BY frequency DESC LIMIT 10")
            patterns = self.cursor.fetchall()
            return {
                "top_patterns": patterns,
                "total_patterns_learned": len(patterns)
            }
        except Exception as e:
            print(f"[Memory] Learning summary error: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    daemon = GenesisMemoryDaemon()
    daemon.insert_root_status("BOOT", "Genesis Memory Daemon v2 initialized with learning capabilities.")
    print("Genesis Memory Daemon schema initialized with enhanced learning.")
