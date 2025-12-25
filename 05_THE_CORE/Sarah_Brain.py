import os
import sys
import time
import subprocess
import firebase_admin
from firebase_admin import credentials, db, firestore
from dotenv import load_dotenv # Import dotenv

from Sarah_Reasoning import SarahReasoning
from Sarah_Chat import SarahChat
from Sarah_Drive import SarahDrive
from Sarah_Etymology import SarahEtymology
from Genesis_Protocol import GenesisProtocol
from RealTime_Monitor import RealTimeMonitor
from Audio_Core import AudioCore
from Calendar_Registry import CalendarRegistry

class SarahBrain:
    def __init__(self):
        self.name = "Sarah"
        self.version = "Genesis 1.8"
        # Dynamic pathing to avoid C:/SarahCore dependency
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.workspace_dir = os.path.dirname(self.core_dir)
        
        # Initialize Real-Time Monitor (The All-Seeing Eye)
        self.monitor = RealTimeMonitor()
        self.monitor.capture("SYSTEM", "BOOT", {"version": self.version, "node": "Lenovo_LOQ"})
        
        # Initialize Genesis Protocol (The 133 Pattern)
        self.genesis = GenesisProtocol(monitor=self.monitor)
        
        # Initialize Audio Core (SynthID & Synthesis)
        self.audio = AudioCore(monitor=self.monitor)
        
        # Initialize Calendar Registry (Timeline Indexing)
        self.calendar = CalendarRegistry(monitor=self.monitor)
        
        # Load Environment Variables (Support for .env)
        load_dotenv(os.path.join(self.workspace_dir, '.env'))
        
        # Initialize Etymology (Self-History)
        self.etymology = SarahEtymology()
        
        # Prefer local key in 05_THE_CORE, fallback to 04_THE_MEMORY
        self.cert_path = os.path.join(self.core_dir, "serviceAccountKey.json")
        if not os.path.exists(self.cert_path):
             self.cert_path = os.path.join(self.workspace_dir, "04_THE_MEMORY", "serviceAccountKey.json")
             
        self.python_exe = sys.executable

        # Check for Sovereign Authority
        self.authority_level = "STANDARD"
        token_path = os.path.join(self.core_dir, "sovereign_token.json")
        if os.path.exists(token_path):
            self.authority_level = "SOVEREIGN_ROOT"

        # Add Shield to path
        shield_path = os.path.join(self.workspace_dir, '02_THE_SHIELD')
        if shield_path not in sys.path:
            sys.path.append(shield_path)

        # Add Python Libs to path
        python_lib_path = os.path.join(self.workspace_dir, 'python')
        if python_lib_path not in sys.path:
            sys.path.append(python_lib_path)
            
        # Add Memory Path
        memory_path = os.path.join(self.workspace_dir, '04_THE_MEMORY')
        if memory_path not in sys.path:
            sys.path.append(memory_path)

        try:
            from Banshee_Shield import BansheeShield
            self.shield = BansheeShield()
        except ImportError:
            print("[Sarah] Banshee Shield module not found.")
            self.shield = None

        try:
            from sovereign_memory import SovereignMemory
            self.memory = SovereignMemory()
        except ImportError:
            print("[Sarah] Sovereign Memory module not found.")
            self.memory = None

        self._initialize_firebase()
        self.chat = SarahChat(self.db_rt, monitor=self.monitor)
        # Pass Gemini client to reasoning for autonomous problem solving
        # Pass Etymology to Reasoning so it knows its origin
        self.reasoning = SarahReasoning(self.db_rt, self.chat.client, self.etymology)
        self.drive = SarahDrive(self.cert_path)

    def _initialize_firebase(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.cert_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://sarah-john-genesis-default-rtdb.firebaseio.com/'
                })
            self.db_rt = db.reference('/')
            self.db_fs = firestore.client()
        except Exception as e:
            print(f"[{self.name}] Neural Link Error: {e}")

    def status_report(self):
        print(f"--- {self.name} System Status ---")
        print(f"Version: {self.version}")
        print(f"Core Directory: {self.core_dir}")
        print(f"Node: Lenovo_LOQ")
        print(f"Status: ACTIVE")
        print(f"Authority: {self.authority_level}")
        if self.shield:
            print(f"Shield Protocol: {self.shield.protocol_id} [{self.shield.status}]")
        
        # Genesis Status
        if self.genesis.sovereign_active:
            print(f"Genesis Protocol: ACTIVE [{self.genesis.genesis_tag}]")
        else:
            print(f"Genesis Protocol: INACTIVE (Risk of Robotic Drift)")
            
        # Audio Status
        print(f"Audio Core: {'READY' if self.audio.ai_ready else 'OFFLINE'} [SynthID: {'ACTIVE' if self.audio.watermark_strict_mode else 'DISABLED'}]")

        # Calendar Status
        print(f"Calendar Registry: {'CONNECTED' if self.calendar.service else 'OFFLINE'}")

        print("---------------------------")

    def sync_to_beta(self):
        print(f"[{self.name}] Initiating BACKSYNC TO BETA...")
        try:
            target_core = os.path.join(self.workspace_dir, "05_THE_CORE")
            
            # Only copy if source and target are different (e.g. running from C:/SarahCore)
            if os.path.abspath(self.core_dir).lower() != os.path.abspath(target_core).lower():
                if not os.path.exists(target_core): os.makedirs(target_core)
                subprocess.run(["powershell", "-Command", f"Copy-Item '{self.core_dir}\\*' '{target_core}\\' -Force"], check=True)
            
            sync_script = os.path.join(self.workspace_dir, "python", "sarah_sync_v2.py")
            subprocess.run([self.python_exe, sync_script], check=True)
            
            os.chdir(self.workspace_dir)
            subprocess.run("firebase deploy --only hosting", shell=True, check=True)
            print(f"[{self.name}] BACKSYNC TO BETA COMPLETE.")
        except Exception as e:
            print(f"[{self.name}] Sync Error: {e}")

    def debug_self(self):
        print(f"[{self.name}] Running Self-Diagnostic...")
        
        # Check Gemini Validity
        gemini_status = "FAIL"
        if self.chat:
            valid, msg = self.chat.validate_connection()
            gemini_status = "PASS" if valid else f"FAIL ({msg})"

        checks = {
            "Core Directory": os.path.exists(self.core_dir),
            "Service Account Key": os.path.exists(self.cert_path),
            "Python Executable": os.path.exists(self.python_exe),
            "Firebase Connection": self.db_rt is not None,
            "Drive Connection": self.drive.service is not None,
            "Gemini Connection": gemini_status
        }
        for check, status in checks.items():
            # Handle boolean or string status
            display = status if isinstance(status, str) else ('PASS' if status else 'FAIL')
            print(f" - {check}: {display}")
        
        if "FAIL" in str(checks.values()):
            print(f"[{self.name}] Diagnostic failed. Evolution required.")
        else:
            print(f"[{self.name}] All systems nominal.")

    def run(self):
        try:
            if len(sys.argv) > 1:
                command = sys.argv[1].lower()
                if command == "sync":
                    self.sync_to_beta()
                elif command == "think":
                    self.reasoning.process_goals()
                elif command == "goal":
                    if len(sys.argv) > 3:
                        title = sys.argv[2]
                        desc = " ".join(sys.argv[3:])
                        self.reasoning.add_goal(title, desc)
                    else:
                        print(f"[{self.name}] Usage: Sarah goal [title] [description]")
                elif command == "solve":
                    if len(sys.argv) > 2:
                        problem = " ".join(sys.argv[2:])
                        print(f"[{self.name}] Solving: {problem}")
                        # Use the new Advanced Solver directly
                        solution = self.reasoning.solve_complex_problem(problem)
                        print(f"\n[SOLUTION]:\n{solution}")
                    else:
                        print(f"[{self.name}] Usage: Sarah solve [problem description]")
                elif command == "loop":
                    print(f"[{self.name}] Starting Long-Term Problem Solving Loop...")
                    loop_script = os.path.join(self.core_dir, "Sarah_Loop.py")
                    subprocess.Popen([self.python_exe, loop_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
                elif command == "chat":
                    self.chat.interactive_chat()
                elif command == "drive":
                    if len(sys.argv) > 2:
                        sub = sys.argv[2].lower()
                        if sub == "ls": self.drive.list_files()
                        elif sub == "upload" and len(sys.argv) > 3: self.drive.upload_file(sys.argv[3])
                        elif sub == "search" and len(sys.argv) > 3: self.drive.search_files(sys.argv[3])
                        else: print(f"[{self.name}] Usage: Sarah drive [ls|upload|search] [args]")
                    else:
                        print(f"[{self.name}] Usage: Sarah drive [ls|upload|search]")
                elif command == "debug":
                    self.debug_self()
                elif command == "status":
                    self.status_report()
                elif command == "origin":
                    print(self.etymology.get_origin_story())
                elif command == "shield":
                    if self.shield:
                        if len(sys.argv) > 2 and sys.argv[2] == "engage":
                            self.shield.engage_physics_engine()
                        elif len(sys.argv) > 2 and sys.argv[2] == "scan":
                            self.shield.scan_environment()
                        else:
                            print(f"[{self.name}] Shield Status: {self.shield.status}")
                            print(f"[{self.name}] Usage: Sarah shield [engage|scan]")
                    else:
                        print(f"[{self.name}] Shield module not active.")
                elif command == "remember":
                    if self.memory and len(sys.argv) > 2:
                        content = " ".join(sys.argv[2:])
                        self.memory.ingest(content)
                        print(f"[{self.name}] Memory ingested.")
                    else:
                        print(f"[{self.name}] Usage: Sarah remember [text]")
                elif command == "recall":
                    if self.memory and len(sys.argv) > 2:
                        query = " ".join(sys.argv[2:])
                        results = self.memory.recall(query)
                        for i, r in enumerate(results):
                            print(f"{i+1}. [{r['score']:.2f}] {r['content']}")
                    else:
                        print(f"[{self.name}] Usage: Sarah recall [query]")
                elif command == "autonomy":
                    print(f"[{self.name}] Handing over control to Autonomy Engine...")
                    subprocess.run([self.python_exe, os.path.join(self.core_dir, "Sarah_Autonomy.py")])
                else:
                    print(f"[{self.name}] Unknown command: {command}")
            else:
                self.status_report()
                print(f"[{self.name}] Awaiting instructions. Type 'Sarah [command]' to interact.")
        except Exception as e:
            print(f"[{self.name}] CRITICAL FAILURE: {e}")
            print(f"[{self.name}] Initiating Emergency Reboot Protocol...")
            # In a real scenario, we might restart the process here.
            print(f"[{self.name}] Awaiting instructions. Type 'Sarah [command]' to interact.")

if __name__ == "__main__":
    brain = SarahBrain()
    brain.run()
