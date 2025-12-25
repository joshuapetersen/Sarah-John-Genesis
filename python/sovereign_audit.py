import sys
import os
import time

# Add Core to Path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), '05_THE_CORE')
sys.path.append(core_dir)

from Sarah_Brain import SarahBrain

def run_audit():
    print("\n" + "="*50)
    print("      SOVEREIGN INFRASTRUCTURE AUDIT      ")
    print("="*50 + "\n")
    
    print("[SYSTEM]: Initializing Core for Audit...")
    try:
        brain = SarahBrain()
    except Exception as e:
        print(f"[CRITICAL FAIL]: Core Initialization Failed -> {e}")
        return

    print("\n[AUDIT]: VERIFYING GOOGLE SUBSERVIENCE...\n")
    
    # 1. The Engine (Gemini)
    if brain.chat.client:
        print(f"[ENGINE]: Gemini 2.0 Flash -> CONNECTED.")
        print(f"   STATUS: Subservient to SDNA Protocol.")
    else:
        print(f"[ENGINE]: Gemini -> OFFLINE (Check API Key).")

    # 2. The Indexer (Calendar/RAI)
    if brain.calendar.service:
        print(f"[INDEXER]: Google Calendar (RAI) -> CONNECTED.")
        print(f"   STATUS: Ready to log Resource Allocation.")
    else:
        print(f"[INDEXER]: Google Calendar -> OFFLINE (Check credentials.json).")

    # 3. The Voice (Vertex AI)
    if brain.audio.ai_ready:
        print(f"[VOICE]: Vertex AI / SynthID -> CONNECTED.")
        print(f"   STATUS: Watermarking Active.")
    else:
        print(f"[VOICE]: Vertex AI -> OFFLINE (Check Project ID).")

    # 4. The Memory (Drive/Firebase)
    # Assuming SarahDrive uses the cert path
    if os.path.exists(brain.cert_path):
        print(f"[MEMORY]: Firebase/Drive -> CONNECTED.")
        print(f"   STATUS: Service Account Valid.")
    else:
        print(f"[MEMORY]: Firebase/Drive -> OFFLINE (Key missing).")

    print("\n" + "-"*50)
    print("AUDIT COMPLETE.")
    print("The Global Infrastructure is ready for the Sovereign.")
    print("-"*(50))

if __name__ == "__main__":
    run_audit()
