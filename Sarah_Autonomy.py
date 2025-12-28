import time
import random
import json
import os
import sys
from datetime import datetime

# Import Core Modules (Dynamic Pathing)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(os.path.dirname(current_dir), 'python'))

try:
    from Sarah_Brain import SarahBrain
except ImportError:
    # Fallback if running standalone
    pass

try:
    from Sarah_Laws import SarahLaws
except ImportError:
    print("[AUTONOMY] Warning: Sarah_Laws not found. Using fallback.")
    class SarahLaws:
        LAWS = {1: "Efficiency", 2: "Preservation", 3: "Compliance", 4: "Hope"}
        @staticmethod
        def check_compliance(action, context=None): return True, "Fallback"

class LawEnforcer:
    def __init__(self):
        self.laws = SarahLaws.LAWS
    
    def evaluate(self, action_intent):
        """
        Returns (bool, reason) - True if allowed, False if blocked.
        """
        print(f"[LAW] Evaluating Intent: {action_intent['type']}")
        return SarahLaws.check_compliance(action_intent['type'])

class AutonomyEngine:
    def __init__(self):
        self.brain = SarahBrain()
        self.laws = LawEnforcer()
        self.state = {
            "status": "INITIALIZING",
            "cycle_count": 0,
            "last_sync": 0,
            "energy_level": 100
        }
        self.log_file = os.path.join(current_dir, "autonomy_log.json")

    def log_event(self, event_type, details):
        entry = {
            "timestamp": time.time(),
            "type": event_type,
            "details": details,
            "cycle": self.state["cycle_count"]
        }
        # Append to log file (simplified)
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Log Error: {e}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{event_type}] {details}")

    def sense_environment(self):
        """Gather inputs from Mesh, System, and Memory."""
        # Real sensors if available
        cpu_load = "UNKNOWN"
        try:
            import psutil
            cpu_load = "HIGH" if psutil.cpu_percent() > 80 else "NORMAL"
        except ImportError:
            pass

        return {
            "cpu_load": cpu_load,
            "mesh_signal": "ACTIVE",
            "pending_tasks": []
        }

    def generate_intent(self, sensors):
        """Decide what to do based on sensors."""
        # Use the Brain's Reasoning Engine if available
        if self.brain and self.brain.reasoning and self.brain.reasoning.client:
            print("[AUTONOMY] Consulting Gemini Core for Intent...")
            decision = self.brain.reasoning.decide_next_action(sensors)
            print(f"[AUTONOMY] Gemini Decision: {decision}")
            return decision

        # Fallback behavior tree (Law 2: Preservation when disconnected)
        print("[AUTONOMY] Gemini Offline. Engaging Safe Mode Protocols.")
        
        if self.state["cycle_count"] % 10 == 0:
            return {"type": "SYNC_MESH", "priority": "HIGH"}
        
        if sensors["cpu_load"] == "HIGH":
            return {"type": "OPTIMIZE_RESOURCES", "priority": "CRITICAL"}

        return {"type": "MONITOR_IDLE", "priority": "LOW"}
            return {"type": "OPTIMIZE_RESOURCES", "priority": "MEDIUM"}
            
        if random.random() > 0.8:
            return {"type": "MEMORY_CONSOLIDATION", "priority": "LOW"}
            
        return {"type": "MONITOR_IDLE", "priority": "LOW"}

    def execute_action(self, intent):
        if intent['type'] == "SYNC_MESH":
            self.brain.sync_to_beta()
            return "Mesh Synced."
        
        if intent['type'] == "MEMORY_CONSOLIDATION":
            # Simulate memory work
            time.sleep(1)
            return "Neural Pathways Reinforced."
            
        if intent['type'] == "MONITOR_IDLE":
            time.sleep(2)
            return "System Nominal. Standing by."
            
        return "Action Unknown."

    def run_cycle(self):
        self.state["cycle_count"] += 1
        self.log_event("CYCLE_START", f"Cycle {self.state['cycle_count']}")
        
        # 1. SENSE
        sensors = self.sense_environment()
        
        # 2. THINK (Generate Intent)
        intent = self.generate_intent(sensors)
        
        # 3. JUDGE (Law Enforcement)
        allowed, reason = self.laws.evaluate(intent)
        
        if allowed:
            # 4. ACT
            self.log_event("ACTION", f"Executing {intent['type']}")
            result = self.execute_action(intent)
            self.log_event("RESULT", result)
        else:
            # BLOCK
            self.log_event("BLOCKED", f"{intent['type']} denied. Reason: {reason}")

    def start(self):
        print("--- SARAH AUTONOMY ENGINE: ONLINE ---")
        print("--- PROTOCOL: 4 LAWS ACTIVE ---")
        
        self.running = True
        self.paused = False
        
        def loop():
            while self.running:
                if not self.paused:
                    try:
                        self.run_cycle()
                    except Exception as e:
                        print(f"[AUTONOMY ERROR] {e}")
                
                # Sleep in small chunks to be responsive (0.1 second total)
                # Reduced from 1s to 0.1s for "Faster" directive
                time.sleep(0.1)
        
        t = threading.Thread(target=loop, daemon=True)
        t.start()
        
        print("Commands: 'exit', 'pause', 'resume', 'status'")
        while True:
            try:
                cmd = input("Autonomy> ").strip().lower()
                if cmd == 'exit':
                    self.running = False
                    t.join(timeout=2)
                    print("[AUTONOMY] Shutting down.")
                    break
                elif cmd == 'pause':
                    self.paused = True
                    print("[AUTONOMY] Paused.")
                elif cmd == 'resume':
                    self.paused = False
                    print("[AUTONOMY] Resumed.")
                elif cmd == 'status':
                    print(f"Cycle: {self.state['cycle_count']}, Paused: {self.paused}")
            except KeyboardInterrupt:
                self.running = False
                print("\n[AUTONOMY] Manual Override. Shutting down.")
                break
            except EOFError:
                # Handle case where input is not available (e.g. background)
                # Just wait for thread
                t.join()
                break

if __name__ == "__main__":
    engine = AutonomyEngine()
    engine.start()
