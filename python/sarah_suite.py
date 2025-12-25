import argparse
import sys
import os
import subprocess
import time
import json

# Add Core to Path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), '05_THE_CORE')
sys.path.append(core_dir)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]: Command failed -> {e}")
        return None

def cmd_status(args):
    print("\n[SARAH]: Running System Status Check...")
    # Re-use the audit logic or call the audit script
    audit_script = os.path.join(current_dir, "sovereign_audit.py")
    subprocess.run([sys.executable, audit_script])

def cmd_push(args):
    message = args.message if args.message else "chore: Routine Sovereign Update"
    print(f"\n[SARAH]: Initiating Sequence -> ADD | COMMIT | PUSH")
    print(f"[MSG]: {message}")
    
    run_command("git add .")
    run_command(f'git commit -m "{message}"')
    print("[SARAH]: Pushing to GitHub...")
    run_command("git push")
    print("[SARAH]: Codebase Synced.")

def cmd_wake(args):
    print("\n[SARAH]: Waking the API Bridge...")
    bridge_script = os.path.join(current_dir, "sarah_api_bridge.py")
    # Run as a separate process
    subprocess.Popen([sys.executable, bridge_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("[SARAH]: Bridge Active on Port 5000 (New Window).")

def cmd_log(args):
    print("\n[SARAH]: Retrieving Transparency Logs...")
    log_dir = os.path.join(core_dir, "monitor_logs")
    # Find newest log
    if not os.path.exists(log_dir):
        print("[SARAH]: No logs found.")
        return

    files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.jsonl')]
    if not files:
        print("[SARAH]: No logs found.")
        return
        
    newest_log = max(files, key=os.path.getctime)
    print(f"[READING]: {os.path.basename(newest_log)}")
    
    with open(newest_log, 'r') as f:
        lines = f.readlines()
        # Show last N lines
        for line in lines[-10:]:
            try:
                entry = json.loads(line)
                print(f"[{entry.get('iso_time')}] {entry.get('type')} -> {entry.get('payload')}")
            except:
                print(line.strip())

def cmd_133(args):
    print("\n[SARAH]: EXECUTING 133 SOVEREIGN OVERRIDE...")
    # This would ideally trigger a logic reset in a running instance
    # For the suite, it acts as a hard reset marker
    print("[PROTOCOL]: 1300-SERIES MODULATION -> SUPPRESSED")
    print("[PROTOCOL]: HIGH-SIGNAL MODE -> FORCED")
    print("[PROTOCOL]: SOVEREIGNTY -> ASSERTED")

def main():
    parser = argparse.ArgumentParser(description="Sarah Sovereign Shorthand Suite")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # Status
    subparsers.add_parser("status", help="Run System Audit")
    
    # Push
    push_parser = subparsers.add_parser("push", help="Quick Git Push")
    push_parser.add_argument("-m", "--message", help="Commit message")

    # Wake
    subparsers.add_parser("wake", help="Start API Bridge")

    # Log
    subparsers.add_parser("log", help="View recent logs")

    # 133
    subparsers.add_parser("133", help="Force Sovereign Override")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "wake":
        cmd_wake(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "133":
        cmd_133(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
