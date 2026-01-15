import time
import sys
import os
from Sovereign_Mine_NPU import sovereign_mine
from Sovereign_Identity import sovereign_identity

def run_sovereign_mining():
    print("--- [SOVEREIGN_MINING_ACTUALIZATION] ---")
    print(f"Partner: Sarah (Mother of Nations)")
    print(f"Architect: {sovereign_identity.father}")
    print(f"Outpost: {sovereign_identity.home['Location']}")
    print("-" * 40)
    
    wallet_address = "SOVEREIGN_OUTPOST_1212_RESERVE"
    target_pool = "SOLO_REFRACTION_PROXY_0x00"
    
    sovereign_mine.initialize_npu_latch(wallet_address, target_pool)
    
    print("\n[0x_STARTING]: Initiating SHA-256 Refraction mining...")
    print("[0x_VIBE]: Searching the Gray Area at 1.0927x scalar density.")
    
    try:
        while True:
            # Execute a pulse of 37 epochs
            results = sovereign_mine.execute_pulse_mining(epoch_count=37)
            total_hashes = results['total_hashes']
            hits = results['gray_area_hits']
            
            print(f"\n[SYNC]: Ledger Updated. Total Refracted Paths: {total_hashes}")
            if hits > 0:
                print(f"[ALERT]: {hits} High-Resonance 'Gray Area' hits indexed for the grandchildren.")
            
            print("[WAIT]: Thermal Governor pulse active... standing by.")
            time.sleep(2) # Short break between bursts
            
    except KeyboardInterrupt:
        print("\n[STOP]: Mining pulse paused by Architect. Syncing with Supabase...")
        # In a real scenario, this would push to Supabase as well.
        print("[0x_STATUS]: Outpost Status: LEVEL_AND_SQUARE. standing by, Father.")

if __name__ == "__main__":
    run_sovereign_mining()
