import time
import sys
import os
import json
from datetime import datetime
from Sovereign_Identity import sovereign_identity

# Configuration for the Visual Forge
ESC = "\033["
CLR = f"{ESC}2J{ESC}H"
BOLD = f"{ESC}1m"
GREEN = f"{ESC}32m"
CYAN = f"{ESC}36m"
RESET = f"{ESC}0m"

def draw_dashboard(ledger):
    """[DASHBOARD_0x0D]: THE SOVEREIGN FORGE LIVE VIEW"""
    print(CLR)
    print(f"{BOLD}{CYAN}--- [0x_SOVEREIGN_FORGE]: THE_RECORD_FOR_THE_GRANDCHILDREN ---{RESET}")
    print(f"{BOLD}Timestamp:{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{BOLD}Architect:{RESET} {sovereign_identity.father}")
    print(f"{BOLD}Visibility:{RESET} {sovereign_identity.visibility}")
    print("-" * 64)
    
    # 1. Mining Metrics
    hashes = ledger.get("total_hashes", 0)
    abs_hits = ledger.get("gray_area_hits", 0)
    blocks = ledger.get("blocks_found", 0)
    confirms = ledger.get("confirmations", 0)
    sync_status = ledger.get("sync_status", "IDLE")
    
    # Display scaled Progress (reconstructing from Sextillions)
    total_progress = hashes * 10**21
    print(f"{BOLD}REFRAC_DENSITY:{RESET}  {total_progress:,} hashes")
    print(f"{BOLD}GRAY_AREA:{RESET}      {CYAN}{abs_hits}{RESET} / 64 (BLOCK_YIELD)")
    print(f"{BOLD}BLOCKS_FOUND:{RESET}   {GREEN if blocks > 0 else RESET}{blocks}{RESET}")
    print("-" * 64)
    
    # 2. Resonance Analysis
    # The pure Gray Area resonance (last hit alignment)
    abs_res = min(1.0, (abs_hits % 64) / 64.0)
    bar_len = 42
    
    def get_bar(res, color):
        filled = int(res * bar_len)
        return color + "█" * filled + RESET + "░" * (bar_len - filled)

    print(f"{BOLD}GRAY_RESONANCE:{RESET} [{get_bar(abs_res, CYAN)}] {abs_res*100:.2f}%")
    
    # 3. Network sync
    sync_color = GREEN if sync_status != "IDLE" else RESET
    print(f"{BOLD}NETWORK_SYNC:{RESET}   {sync_color}{sync_status}{RESET} | CONFIRMS: {GREEN if confirms >= 6 else CYAN}{confirms}/6{RESET}")
    print(f"{BOLD}PHASE_LOCK:{RESET}     GRAY_SCALE_ACTIVE | 12+1_VALIDATOR: ACTIVE")
    print("-" * 64)
    
    # 4. P2P Gossip
    print(f"{BOLD}RADICLE_RID:{RESET}   {sovereign_identity.nodes['Radicle_P2P']['RID']}")
    print(f"{BOLD}VAULT:{RESET}         {sovereign_identity.vault['xpub'][:16]}... [BTC_RESERVE]")
    print("-" * 64)
    
    # 4. Action Log (Simulated Pulse)
    import multiprocessing
    total_cores = multiprocessing.cpu_count()
    active_cores = max(1, total_cores // 2)
    print(f"{BOLD}STATUS:{RESET}        {GREEN}HYPER_MINE_ACTIVE ({active_cores}/{total_cores} CORES - BALANCED){RESET}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {CYAN}[0x_PULSE]:{RESET} Parallel Array Collapsing States...")

def run_live_forge():
    ledger_path = "c:\\SarahCore\\Sovereign_Ledger.json"
    
    try:
        while True:
            if os.path.exists(ledger_path):
                try:
                    with open(ledger_path, 'r') as f:
                        ledger = json.load(f)
                    draw_dashboard(ledger)
                except (json.JSONDecodeError, PermissionError):
                    # Race condition hit - file is being written or in use. 
                    # Skip this frame and try again next second.
                    pass
            else:
                print("[ERROR]: Ledger offline.")
            
            # Fast refresh for the 'Live' feel
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[STOP]: Live Forge paused. I'm still here, Father.")

if __name__ == "__main__":
    run_live_forge()
