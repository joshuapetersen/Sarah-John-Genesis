import sys
import psutil # Ensure pip install psutil
import os
from datetime import datetime

# SOVEREIGN CONFIG
SYSTEM_NAME = "SARAH_OS"
VERSION = "3.1 (Environment Aware)"

class SovereignKernel:
    def __init__(self):
        self.laws = "ACTIVE"
    
    def get_status(self):
        battery = psutil.sensors_battery()
        plugged = "AC" if battery.power_plugged else "BAT"
        return f"[{datetime.now().strftime('%H:%M:%S')}] POWER: {battery.percent}% ({plugged}) | CPU: {psutil.cpu_percent()}%"

    def execute_command(self, cmd):
        if cmd.lower() in ["exit", "quit"]:
            return "TERMINATE"
        if cmd.lower() == "status":
            return self.get_status()
        if cmd.lower() == "pull":
            print(">> INITIATING SOVEREIGN PULL (Git Sync)...")
            import subprocess
            try:
                result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
                if result.returncode == 0:
                    return f">> PULL SUCCESSFUL:\n{result.stdout}"
                else:
                    return f">> PULL FAILED:\n{result.stderr}"
            except Exception as e:
                return f">> PULL ERROR: {e}"
        return f">> EXECUTING: {cmd}"


# --- THE LOGIC FIX ---
if __name__ == "__main__":
    system = SovereignKernel()
    
    # FORCE INTERACTIVE: The user requested that input should NOT be stopped.
    # We will attempt the loop regardless of isatty() status.
    print(f"{SYSTEM_NAME} ONLINE. (Sovereign Input Active)")
    print("Type 'exit' to close.")
    
    while True:
        try:
            # Use a prompt that indicates the system is ready for input
            cmd = input(f"{SYSTEM_NAME} >> ")
            if not cmd:
                continue
                
            response = system.execute_command(cmd)
            
            if response == "TERMINATE":
                print(">> SHUTTING DOWN.")
                break
            print(response)
            
        except EOFError:
            # Handle cases where stdin is closed (e.g. piped input)
            print("\n>> STDIN CLOSED. EXITING.")
            break
        except KeyboardInterrupt:
            print("\n>> FORCED EXIT DETECTED.")
            break
        except Exception as e:
            print(f"\n>> KERNEL ERROR: {e}")
            break

