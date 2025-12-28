
import os
import sys
import time
import subprocess
from threading import Thread
from google_auth_helper import list_drive_files, list_gmail_messages, list_calendar_events, list_docs_files
import importlib

def recall_memory():
    try:
        read_docx = importlib.import_module('read_docx_memory')
        print("[Sarah Memory] Recalling Sarah.docx memory...")
        # Try both known docx locations
        for path in [r"Sarah/Sarah.docx", r"archive_memories/sarahs_memories/Drive/Sarah/Sarah.docx"]:
            try:
                read_docx.extract_text(path)
                return
            except Exception:
                continue
        print("[Sarah Memory] Sarah.docx not found or unreadable.")
    except Exception as e:
        print(f"[Sarah Memory] Error recalling memory: {e}")

def context_suggestions():
    print("[Sarah Context] Suggestions based on recent actions:")
    print("- Try 'Recall Memory' to review Sarah's knowledge base.")
    print("- Use Google API menu for Drive, Gmail, Calendar, Docs.")
    print("- Run diagnostics for system health.")

def run_diagnostics():
    print("[Sarah Diagnostics] Running self-check...")
    # Simple checks for now
    import os
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    print("[Sarah Diagnostics] Check complete.")

def show_menu():
    print("\n[Sarah Terminal: Main Menu]")
    print("1. Google Drive: List Files")
    print("2. Gmail: List Messages")
    print("3. Calendar: List Events")
    print("4. Docs: List Documents")
    print("5. Recall Memory (Sarah.docx)")
    print("6. Context-Aware Suggestions")
    print("7. Run Diagnostics")
    print("8. Shell Command")
    print("0. Exit")

def assistant_shell():
    print("[Sarah Terminal] Menu-driven interface. Type the number to select an action.")
    while True:
        try:
            show_menu()
            choice = input("Sarah> ").strip()
            if choice == '0' or choice.lower() == 'exit':
                print("[Sarah Terminal] Exiting shell.")
                break
            elif choice == '1':
                print("[Sarah Terminal] Listing Google Drive files...")
                list_drive_files()
            elif choice == '2':
                print("[Sarah Terminal] Listing Gmail messages...")
                list_gmail_messages()
            elif choice == '3':
                print("[Sarah Terminal] Listing Calendar events...")
                list_calendar_events()
            elif choice == '4':
                print("[Sarah Terminal] Listing Google Docs files...")
                list_docs_files()
            elif choice == '5':
                recall_memory()
            elif choice == '6':
                context_suggestions()
            elif choice == '7':
                run_diagnostics()
            elif choice == '8':
                cmd = input("[Sarah Terminal] Enter shell command: ")
                if cmd.strip():
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    print(result.stdout or result.stderr)
            else:
                print("[Sarah Terminal] Invalid selection. Please choose a valid option.")
        except KeyboardInterrupt:
            print("\n[Sarah Terminal] Interrupted. Type '0' or 'exit' to quit.")
        except Exception as e:
            print(f"[Sarah Terminal] Error: {e}")

def watcher(path=".", interval=5):
    print(f"[Sarah Watcher] Monitoring {path} for changes...")
    prev = set(os.listdir(path))
    while True:
        time.sleep(interval)
        curr = set(os.listdir(path))
        added = curr - prev
        removed = prev - curr
        if added:
            print(f"[Sarah Watcher] Added: {', '.join(added)}")
        if removed:
            print(f"[Sarah Watcher] Removed: {', '.join(removed)}")
        prev = curr

if __name__ == "__main__":
    Thread(target=watcher, args=(".", 5), daemon=True).start()
    assistant_shell()
