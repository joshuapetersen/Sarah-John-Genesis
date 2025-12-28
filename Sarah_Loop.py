import time
import subprocess
import sys
import os
import threading

# Dynamic Pathing for Portability (Law 2 & 4)
PYTHON_EXE = sys.executable
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_SCRIPT = os.path.join(CORE_DIR, "Sarah_Brain.py")
LOG_FILE = os.path.join(CORE_DIR, "sarah_loop.log")

stop_event = threading.Event()
force_event = threading.Event()

def log(message):
    timestamp = time.ctime()
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(full_msg + "\n")
    except Exception as e:
        print(f"Log Error: {e}")

def reasoning_cycle():
    try:
        log("Triggering reasoning cycle...")
        # Call the brain script directly with the 'think' command
        # Using subprocess to ensure isolation (Law 2)
        result = subprocess.run([PYTHON_EXE, BRAIN_SCRIPT, "think"], capture_output=True, text=True)
        
        if result.returncode == 0:
            log("Reasoning cycle completed successfully.")
            if result.stdout:
                # Truncate output to avoid log bloat (Law 1)
                output = result.stdout.strip()
                if len(output) > 500:
                    output = output[:500] + "... [TRUNCATED]"
                log(f"Output: {output}")
        else:
            log(f"Reasoning cycle failed with exit code {result.returncode}.")
            log(f"Error: {result.stderr.strip()}")
    except Exception as e:
        log(f"Error in reasoning cycle: {e}")

def loop_thread():
    log("Long-term problem solving loop initiated.")
    while not stop_event.is_set():
        reasoning_cycle()
        
        # Wait for 60 seconds (1 min) or until forced/stopped
        log("Sleeping for 60 seconds...")
        start_time = time.time()
        while time.time() - start_time < 60:
            if stop_event.is_set():
                break
            if force_event.is_set():
                force_event.clear()
                log("Sleep interrupted by force command.")
                break
            time.sleep(0.5)

def run_interactive():
    t = threading.Thread(target=loop_thread, daemon=True)
    t.start()
    
    print("--- Sarah Loop Interactive Mode ---")
    print("Commands: 'exit' to stop, 'force' to run now.")
    
    while True:
        try:
            user_input = input("SarahLoop> ").strip().lower()
            if user_input == 'exit':
                log("Stopping loop...")
                stop_event.set()
                t.join(timeout=5)
                break
            elif user_input == 'force':
                log("Forcing reasoning cycle...")
                force_event.set()
            elif user_input == '':
                continue
            else:
                print("Unknown command. Use 'exit' or 'force'.")
        except KeyboardInterrupt:
            log("Interrupted by user.")
            stop_event.set()
            break

if __name__ == "__main__":
    run_interactive()
