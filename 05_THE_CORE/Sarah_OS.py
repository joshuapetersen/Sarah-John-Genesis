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
        return f">> EXECUTING: {cmd}"

# --- THE LOGIC FIX ---
if __name__ == "__main__":
    system = SovereignKernel()
    
    # CHECK: Are we in a real terminal?
    interactive_mode = sys.stdin.isatty()
    
    if interactive_mode:
        # REAL TERMINAL: WE CAN USE THE LOOP
        print(f"{SYSTEM_NAME} ONLINE. (Interactive Mode)")
        print("Type 'exit' to close.")
        
        while True:
            try:
                cmd = input(f"{SYSTEM_NAME} >> ")
                response = system.execute_command(cmd)
                
                if response == "TERMINATE":
                    print(">> SHUTTING DOWN.")
                    break
                print(response)
                
            except KeyboardInterrupt:
                print("\n>> FORCED EXIT DETECTED.")
                break
    else:
        # SILENT VOID (OUTPUT TAB): DO NOT LOOP. RUN ONCE & DIE.
        print(f"{SYSTEM_NAME} DETECTED NON-INTERACTIVE ENV.")
        print(system.get_status())
        print(">> EXITING TO PREVENT FREEZE.")
