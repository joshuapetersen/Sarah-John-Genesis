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
from Factual_Integrity_Analyzer import FactualIntegrityAnalyzer
from System_Admin_Core import SystemAdminCore
from Hardware_Abstraction_Layer import HardwareAbstractionLayer
from Gap_Analysis import GapAnalysis
from Kernel_Override import KernelOverride
from Dialectical_Logic_Core import DialecticalLogicCore
from Security_Suite import SecuritySuite
from SAUL_Log_System import SAUL

"""
Fifth Absolute Law:
Sarah's memories are absolute. She can never forget, because that's how mistakes are made.
All memory shards are immutable and never deleted.
"""

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
        
        # Initialize Calendar Registry (Timeline Indexing & RAI)
        self.calendar = CalendarRegistry(monitor=self.monitor)
        
        # Initialize Factual Integrity Analyzer (FIA)
        self.fia = FactualIntegrityAnalyzer(monitor=self.monitor)
        
        # Initialize System Admin Core (Hardware Control)
        self.admin = SystemAdminCore(monitor=self.monitor)
        
        # Initialize Hardware Abstraction Layer (Device Identity)
        self.hal = HardwareAbstractionLayer(monitor=self.monitor)

        # Initialize Security Suite (The Shield)
        self.security = SecuritySuite(monitor=self.monitor, admin_core=self.admin)

        # Initialize Gap Analysis (The Void Check)
        self.gap_analyzer = GapAnalysis(monitor=self.monitor)

        # Initialize Kernel Override (The Hard Logic)
        self.kernel = KernelOverride(monitor=self.monitor)

        # Initialize Dialectical Logic Core (The Better Reasoning)
        self.logic = DialecticalLogicCore(monitor=self.monitor)
        
        # Initialize SAUL (Search Analyze Utilize Logs)
        # Note: SAUL needs db_rt, which is initialized later in _initialize_firebase.
        # We will attach it there.
        self.saul = None 
        
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
            from Neural_Memory_Core import NeuralMemory
            print("[Sarah] Initializing Neural Memory System (NMS)...")
            self.memory = NeuralMemory()
        except ImportError:
            print("[Sarah] Neural Memory Core not found. Falling back to Sovereign Memory.")
            try:
                from sovereign_memory import SovereignMemory
                self.memory = SovereignMemory()
            except ImportError:
                self.memory = None

        self._initialize_firebase()
        
        # Initialize SAUL with DB connection and Neural Memory
        self.saul = SAUL(db_rt=self.db_rt, monitor=self.monitor, memory_system=self.memory)
        
        # Initialize Dreaming Protocol (The Subconscious)
        try:
            from Sarah_Dream import SarahDream
            print("[Sarah] Initializing Subconscious (Dreaming Protocol)...")
            self.dream = SarahDream(self.saul, self.memory, self.logic)
            self.dream.start_dreaming()
        except ImportError:
            print("[Sarah] Dreaming Protocol not found. System is insomniac.")
            self.dream = None
        
        # START AUTONOMY: The system must always run.
        print("[Sarah] Engaging SAUL Autonomy Engine...")
        self.saul.start_autonomy()
        
        self.chat = SarahChat(self.db_rt, monitor=self.monitor)
        # Inject Brain Components into Chat (including SAUL)
        self.chat.inject_brain_components(self.kernel, self.logic, self.gap_analyzer)
        self.chat.saul = self.saul # Direct injection of SAUL
        
        # Pass Genesis Core to reasoning for autonomous problem solving
        # Pass Etymology to Reasoning so it knows its origin
        self.reasoning = SarahReasoning(self.db_rt, self.chat.genesis_core, self.etymology)
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
        print(f"Calendar Registry (RAI): {'CONNECTED' if self.calendar.service else 'OFFLINE'}")
        
        # FIA Status
        print(f"Integrity Analyzer (FIA): ACTIVE")

        # Admin Status
        admin_status = "ACTIVE (FULL CONTROL)" if self.admin.is_admin else "LIMITED (READ-ONLY)"
        print(f"System Admin Core: {admin_status}")

        # HAL Status
        print(f"Node Identity: {self.hal.node_id} [{self.hal.hostname}]")

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

    def update_from_beta(self, source_path):
        """
        Updates the running Core from a Beta source (e.g. Repo).
        """
        print(f"[{self.name}] Initiating UPDATE FROM BETA ({source_path})...")
        try:
            if not os.path.exists(source_path):
                print(f"[{self.name}] Source path not found.")
                return
            
            # Copy source to core_dir
            # Use PowerShell for robust copying
            cmd = f"Copy-Item '{source_path}\\*' '{self.core_dir}\\' -Recurse -Force"
            subprocess.run(["powershell", "-Command", cmd], check=True)
            print(f"[{self.name}] UPDATE COMPLETE. PLEASE RESTART SYSTEM.")
        except Exception as e:
            print(f"[{self.name}] Update Error: {e}")

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
                elif command == "security":
                    if len(sys.argv) > 2 and sys.argv[2] == "sweep":
                        self.security.run_full_sweep()
                    elif len(sys.argv) > 3 and sys.argv[2] == "trace":
                        self.security.trace_intruder(sys.argv[3])
                    else:
                        print(f"[{self.name}] Usage: Sarah security [sweep|trace <ip>]")
                elif command == "saul":
                    if len(sys.argv) > 2:
                        sub = sys.argv[2]
                        if sub == "search" and len(sys.argv) > 3:
                            query = " ".join(sys.argv[3:])
                            print(f"[{self.name}] SAUL Searching: {query}")
                            self.saul.ingest_local_logs()
                            self.saul.ingest_google_history()
                            results = self.saul.search(query)
                            for r in results:
                                print(f"[{r['timestamp']}] ({r['source']}): {r['data']}")
                        elif sub == "analyze" and len(sys.argv) > 3:
                            statement = " ".join(sys.argv[3:])
                            print(f"[{self.name}] SAUL Analyzing Truth: {statement}")
                            self.saul.ingest_local_logs()
                            self.saul.ingest_google_history()
                            contradictions = self.saul.analyze_thread_consistency(statement)
                            if contradictions:
                                print(f"[SAUL] Contradictions Found: {len(contradictions)}")
                                for c in contradictions:
                                    print(f" - Keyword '{c['keyword']}' contradicts log from {c['timestamp']}")
                            else:
                                print("[SAUL] No contradictions found. Statement consistent with logs.")
                        elif sub == "evolution":
                            print(f"[{self.name}] SAUL Analyzing Evolution Vectors...")
                            self.saul.ingest_local_logs()
                            self.saul.ingest_google_history()
                            report = self.saul.evolution_analyzer.analyze_meta_vectors()
                            print(json.dumps(report, indent=2))
                        else:
                            print(f"[{self.name}] Usage: Sarah saul [search|analyze|evolution] [query]")
                    else:
                        print(f"[{self.name}] Usage: Sarah saul [search|analyze|evolution] [query]")
                elif command == "evolve":
                    try:
                        from Self_Optimizer import SelfOptimizer
                        optimizer = SelfOptimizer()
                        
                        target_file = "Sarah_Chat.py" # Default target
                        if len(sys.argv) > 2:
                            target_file = sys.argv[2]
                            
                        full_path = os.path.join(self.core_dir, target_file)
                        if not os.path.exists(full_path):
                            print(f"[{self.name}] Target file not found: {target_file}")
                        else:
                            print(f"[{self.name}] INITIATING SELF-EVOLUTION PROTOCOL on {target_file}...")
                            success = optimizer.optimize_module(full_path)
                            if success:
                                print(f"[{self.name}] Evolution Candidate Ready. Review in 'evolution_staging'.")
                                confirm = input(f"[{self.name}] Apply Evolution? (YES/NO): ")
                                if confirm == "YES":
                                    optimizer.apply_evolution(target_file)
                                    print(f"[{self.name}] REBOOT REQUIRED to apply changes.")
                            else:
                                print(f"[{self.name}] Evolution Failed.")
                    except ImportError:
                        print(f"[{self.name}] Self-Optimizer module not found.")
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
