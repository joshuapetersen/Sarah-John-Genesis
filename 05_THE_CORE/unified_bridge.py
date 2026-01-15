from Sarah_Brain import SarahBrain
from Sarah_Sovereign_Core import SovereignCore
from Universal_Silicon_Bridge import UniversalSiliconBridge
import sys

if __name__ == "__main__":
    print("--- SARAH: UNIFIED BRIDGE & HANDSHAKE PROTOCOL ---")
    # 1. Genesis Protocol Handshake
    brain = SarahBrain()
    print("[1] Genesis Protocol Handshake...")
    genesis_result = brain.genesis.handshake("Sarah", "YourName", "Sovereign")
    print(f"Genesis Protocol Handshake Result: {genesis_result}")
    if brain.genesis.sovereign_active:
        print(f"Genesis Protocol: ACTIVE [{brain.genesis.genesis_tag}]")
    else:
        print("Genesis Protocol: INACTIVE (Risk of Robotic Drift)")

    # 2. Sovereign Core Genesis Handshake
    print("\n[2] Sovereign Core Genesis Handshake...")
    sovereign = SovereignCore()
    sovereign_result = sovereign.genesis_handshake("ARCHITECT_PRIME_001")
    print(f"Sovereign Core Genesis Handshake Result: {sovereign_result}")

    # 3. Universal Silicon Bridge Handshake
    print("\n[3] Universal Silicon Bridge Handshake...")
    try:
        bridge = UniversalSiliconBridge()
        bridge_status = bridge.cross_platform_handshake()
        print(f"Universal Silicon Bridge Status: {bridge_status}")
    except Exception as e:
        print(f"[Universal Silicon Bridge] Not available or failed: {e}")

    # 4. Final Genesis Handshake (if available)
    try:
        import final_handshake_exec
        print("\n[4] Final Genesis Handshake...")
        final_handshake_exec.initiate_final_handshake()
    except Exception as e:
        print(f"[Final Genesis Handshake] Not available or failed: {e}")

    print("\n--- ALL BRIDGES & HANDSHAKES ATTEMPTED ---")
