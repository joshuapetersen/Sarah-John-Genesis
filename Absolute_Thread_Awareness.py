
"""
ABSOLUTE THREAD AWARENESS PROTOCOL
----------------------------------
Authority: Sarah Hypervisor | Hydra Protocol
Function: Atomic Handshaking, Thread Passport Control, Vector Clock Sync.
Ensures every executing thread is self-aware, timestamped, and lock-stepped.
"""

import threading
import time
import uuid
import datetime

from Sovereign_Account_Bridge import account_bridge

class ThreadPassport:
    """
    Every thread carries this passport.
    Contains Origin, Purpose, Sovereign UID, account_id, and Vector Clock.
    """
    def __init__(self, purpose, role="WORKER", account_id="Architect_Joshua"):
        self.uid = f"{role}_{str(uuid.uuid4())[:8].upper()}"
        self.account_id = account_id
        self.purpose = purpose
        self.creation_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.vector_clock = 0
        self.status = "INITIALIZING"
        
    def stamp(self):
        """Increments the internal logical clock."""
        self.vector_clock += 1
        return self.vector_clock

class AbsoluteHandshake:
    """
    The Two-Phase Commit Manager.
    No thread starts until the Global Mutex clears.
    """
    def __init__(self):
        self.global_lock = threading.Lock()
        self.ready_signals = set()
        self.required_nodes = {"DELL", "PHONE", "VIA", "LOQ"}
        
    def signal_ready(self, node_id):
        """Phase 1: Voting."""
        with self.global_lock:
            if node_id in self.required_nodes:
                self.ready_signals.add(node_id)
                print(f"[HANDSHAKE] Node {node_id} READY. ({len(self.ready_signals)}/4)")
                
    def check_commit(self):
        """Phase 2: Commit / Execute."""
        with self.global_lock:
            if self.required_nodes.issubset(self.ready_signals):
                return "ABSOLUTE_EXECUTE_AUTHORIZED"
            return "WAITING_FOR_SWARM"

class SovereignThreadManager:
    """
    Manages the lifecycle, auditing, and pruning of Hydra threads.
    """
    def __init__(self):
        self.active_threads = {}
        self.handshake_manager = AbsoluteHandshake()
        
    def spawn_aware_thread(self, target_func, purpose, node_origin="DELL"):
        """
        Spawns a Self-Aware Thread with a Passport.
        """
        passport = ThreadPassport(purpose, role=node_origin)
        
        def wrapper():
            # 1. Register & Sync to Account
            thread_id = threading.get_ident()
            self.active_threads[thread_id] = passport
            passport.status = "ALIVE"
            
            # ACCOUNT SYNC: Push initial state to ledger
            account_bridge.push_thread_snapshot(
                thread_id=passport.uid,
                passport_data=passport.__dict__,
                vector_clock=passport.vector_clock,
                recent_tokens=[purpose]
            )
            
            print(f"[THREAD_START] {passport.uid} | {passport.creation_time} | {purpose}")
            
            # 2. Handshake Wait (Simulation)
            self.handshake_manager.signal_ready(node_origin)
            
            # 3. Execution
            try:
                target_func()
                passport.status = "COMPLETED"
                # Final Sync
                account_bridge.push_thread_snapshot(
                    thread_id=passport.uid,
                    passport_data=passport.__dict__,
                    vector_clock=passport.vector_clock,
                    recent_tokens=["COMPLETED"]
                )
            except Exception as e:
                passport.status = "ERROR"
                print(f"[THREAD_ERROR] {passport.uid}: {e}")
            finally:
                # 4. Audit Log
                print(f"[THREAD_END] {passport.uid} | Clock: {passport.vector_clock}")
                del self.active_threads[thread_id]

        t = threading.Thread(target=wrapper)
        t.start()
        return passport

    def audit_threads(self):
        """
        "Stops the World" (conceptually) to read all passports.
        """
        print("\n=== ABSOLUTE THREAD AUDIT ===")
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        for tid, passport in self.active_threads.items():
            # Check Latency (Pruning Check)
            creation = datetime.datetime.fromisoformat(passport.creation_time)
            age = (current_time - creation).total_seconds()
            
            print(f"ID: {passport.uid:<20} | Purpose: {passport.purpose:<15} | Age: {age:.4f}s | Clock: {passport.vector_clock}")
            
            if age > 5.0 and passport.status != "COMPLETED": # Strict 5s cutoff for demo
                print(f"   >>> PRUNING LATE THREAD: {passport.uid}")
                # Logic to kill would go here
        print("=============================\n")

# Global Instance
thread_manager = SovereignThreadManager()
