import sqlite3
from datetime import datetime
import sys
import os

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Semantic_Memory_Search import SemanticMemoryEngine
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    print("Warning: Semantic Memory Engine not available. Falling back to SQL search.")

class GenesisMemoryBridge:
    def __init__(self, db_path='genesis_core.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_schema()
        
        self.semantic_engine = None
        if SEMANTIC_AVAILABLE:
            try:
                self.semantic_engine = SemanticMemoryEngine(db_path=db_path)
                print("Genesis Memory Bridge: Semantic Engine Linked.")
            except Exception as e:
                print(f"Genesis Memory Bridge: Semantic Engine Init Failed: {e}")

    def _init_schema(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS problem_solution_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            problem TEXT,
            solution TEXT,
            tags TEXT,
            context TEXT
        )''')
        self.conn.commit()

    def store_problem_solution(self, problem, solution, tags='', context=''):
        ts = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO problem_solution_memory (timestamp, problem, solution, tags, context) VALUES (?, ?, ?, ?, ?)",
            (ts, problem, solution, tags, context)
        )
        self.conn.commit()
        
        if self.semantic_engine:
            try:
                self.semantic_engine.add_memory(problem, solution, tags, context)
            except Exception as e:
                print(f"Semantic Index Update Failed: {e}")

    def search_similar_problems(self, problem, limit=5):
        if self.semantic_engine:
            try:
                results = self.semantic_engine.search(problem, top_k=limit)
                if results:
                    # Convert back to tuple format expected by caller: (problem, solution, tags, context)
                    return [(r['problem'], r['solution'], r['tags'], r['context']) for r in results]
            except Exception as e:
                print(f"Semantic Search Failed: {e}. Falling back to SQL.")
        
        # Fallback to Simple LIKE search
        self.cursor.execute(
            "SELECT problem, solution, tags, context FROM problem_solution_memory WHERE problem LIKE ? ORDER BY id DESC LIMIT ?",
            (f'%{problem}%', limit)
        )
        return self.cursor.fetchall()

class ProblemSolver:
    def __init__(self, memory_bridge):
        self.memory = memory_bridge

    def solve(self, problem, context=''):
        # Search for similar problems
        matches = self.memory.search_similar_problems(problem)
        if matches:
            print("Found similar problems in memory:")
            for i, (p, s, t, c) in enumerate(matches, 1):
                print(f"{i}. Problem: {p}\n   Solution: {s}\n   Tags: {t}\n   Context: {c}\n")
            # Use the best match or synthesize a new solution
            return matches[0][1]  # Return the solution of the best match
        else:
            print("No similar problems found. Please provide a solution.")
            solution = input("Enter solution: ")
            tags = input("Enter tags (comma-separated): ")
            self.memory.store_problem_solution(problem, solution, tags, context)
            return solution

if __name__ == "__main__":
    bridge = GenesisMemoryBridge()
    solver = ProblemSolver(bridge)
    print("Genesis Memory-Reasoning Bridge Ready.")
    while True:
        problem = input("Describe your problem (or 'exit'): ")
        if problem.lower() == 'exit':
            break
        context = input("Context (optional): ")
        solution = solver.solve(problem, context)
        print(f"Solution: {solution}\n")
