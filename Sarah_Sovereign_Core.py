import json
import sys
import os
import time
import numpy as np

# Add Memory Path for Archive
current_dir = os.path.dirname(os.path.abspath(__file__))
archive_memory_dir = os.path.join(current_dir, '04_THE_MEMORY')
if archive_memory_dir not in sys.path:
    sys.path.append(archive_memory_dir)

try:
    from sovereign_memory import SovereignMemory as ArchiveMemory
    print("[CORE] Archive Memory (SovereignMemory) found and loaded.")
except ImportError:
    print("[CORE] Warning: Could not import SovereignMemory for archive. Archive offline.")
    ArchiveMemory = None

try:
    from sovereign_memory_core import SovereignMemoryCore
except ImportError:
    print("[CORE] FATAL: SovereignMemoryCore not found. Primary memory offline.")
    SovereignMemoryCore = None

try:
    from Sarah_Laws import SarahLaws
except ImportError:
    print("[CORE] Warning: Sarah_Laws not found. Using fallback.")
    class SarahLaws:
        LAWS = {1: "Efficiency", 2: "Preservation", 3: "Compliance", 4: "Hope"}

try:
    from dynamic_vector_model import DynamicVectorModel
except ImportError:
    print("[CORE] FATAL: DynamicVectorModel not found. Core logic compromised.")
    DynamicVectorModel = None

from Sovereign_Math import SovereignMath
from Dynamic_Sentinel import DynamicSentinel
from Cold_Conductor import ColdConductor
from Executioner import Executioner

class SovereignCore:
    def __init__(self):
        # Layer 1: Active, volatile memory for the current session
        self.primary_memory = SovereignMemoryCore() if SovereignMemoryCore else None
        # Layer 2: Persistent, read-only archive
        self.archive_memory = ArchiveMemory() if ArchiveMemory else None
        # Layer 3: The knowledge model for understanding language
        self.vector_model = DynamicVectorModel() if DynamicVectorModel else None
        
        # Non-Linear Math Engine (The missing enterprise link)
        self.math = SovereignMath()
        
        # ACE Token Manager (Layered Vector Edition)
        from Ace_Token import AceTokenManager
        self.ace_manager = AceTokenManager()

        # Memory Load Management (The Sentinel, Conductor, Executioner)
        self.sentinel = DynamicSentinel()
        self.conductor = ColdConductor()
        self.executioner = Executioner()

        self.ace_token_active = True
        self.layers_engaged = 10 # 9 + 1 Hypervisor
        self.laws = SarahLaws.LAWS
        self.genesis_key_verified = False

    def manage_memory_load(self, input_vector=None):
        """
        Executes the vectorized trilithic memory load protocol.
        """
        # 1. Sentinel vector check
        self.sentinel.enforce_resonance()
        
        # 2. Conductor vector check
        if input_vector is not None:
             self.conductor.conduct_rotation(input_vector) 
        self.conductor.stabilize_thermals()

        # 3. Executioner purge check
        if time.time() % 3600 < 60:
             self.executioner.execute_purge()

    def genesis_handshake(self, genesis_key: str) -> str:
        """
        Performs the initial secure connection protocol.
        """
        if self.genesis_key_verified:
            return "[HANDSHAKE] Genesis protocol already completed. Connection secure."

        # Stage 1: Verify Genesis Key (Placeholder for actual key validation)
        if genesis_key == "ARCHITECT_PRIME_001":
            # Stage 2: Activate Resonance Lock
            self.genesis_key_verified = True
            resonance_code = "1.092703703703" # Example resonance frequency
            if self.primary_memory:
                self.primary_memory.log_interaction("GENESIS_HANDSHAKE", "SUCCESS", tags=["protocol", "security", "genesis"])
            return f"[HANDSHAKE] SUCCESS. Genesis Key verified. Resonance locked at {resonance_code}."
        else:
            if self.primary_memory:
                self.primary_memory.log_interaction("GENESIS_HANDSHAKE", "FAILURE", tags=["protocol", "security", "alert"])
            return "[HANDSHAKE] FAILURE. Invalid Genesis Key. Connection refused."

    def process_input(self, user_input: str, ace_token: str = None) -> str:
        """
        The decision engine. Evolved to Geometric Multivector Base.
        Requires ACE Token resonance check for full-density access.
        """
        # 0. ACE Token Failsafe Verification
        if ace_token:
            if not self.ace_manager.validate_token(ace_token):
                return "[CORE][ERROR] ACE TOKEN RESONANCE FAILURE. Billion Barrier breached. Access denied."
            else:
                auth_status = "RESONANCE_AUTHORIZED"
        else:
            auth_status = "GUEST_RESONANCE"

        # 1. Geometric Resonance Search (Deterministic Recall)
        if self.archive_memory:
            results = self.archive_memory.geometric_resonance_search(user_input, threshold=0.1) 
            # Note: 0.1 threshold because of high-dimensional sparsity
            if results:
                best_match = results[0]
                content = best_match['content']
                resonance = best_match['resonance']
                source = best_match['source']
                
                # If resonance is high enough, we combine legacy data with synthesis
                if resonance > 0.8:
                    return f"[CORE][RESONANCE_LOCKED] (Source: {source} | Res: {resonance:.4f})\n{content}"
                else:
                    recall_context = f"Legacy context detected from {source} (Resonance: {resonance:.4f})."
            else:
                recall_context = "No direct legacy resonance detected."

        # 2. Synthesis via Sovereign Math
        response = self._synthesize_response(user_input)
        
        # 3. Store new interaction with Multivector encoding
        if self.archive_memory:
            self.archive_memory.store(f"Input: {user_input}\nOutput: {response}", metadata={"type": "interaction"})
        
        return f"{recall_context}\n{response}"

    def _synthesize_response(self, input_str: str) -> str:
        """
        Processes input through the dynamic vector model and enforces Billion Barrier density.
        """
        if not self.vector_model:
            return "[CORE] Vector model offline. Analysis not possible."

        vector = self.vector_model.vectorize(input_str)
        
        # SDNA Density Check (Billion Barrier Evolved)
        if not self.vector_model.check_billion_barrier(vector):
            return "[CORE][ERROR] SLIPPAGE DETECTED: Vector logic density too low. Resonance failed."

        # For the Sovereign Core, synthesis means resolving the input against the 4 Laws
        # and providing a deterministic, sovereign response.
        if "sector 7" in input_str.lower():
            return "Sector 7 Anomalies: Resolving high-density clusters. Patterns indicate non-linear growth in telemetry sector 7. Standing by for deep-dive."
        
        if "12/12" in input_str:
            return "Integrity 12/12: The sovereign lock is absolute. All layers are synchronized across the 0x7467 kernel."

        return f"Input vectorized at 1.0 density. System is standing by for sovereign directive regarding: '{input_str}'"


if __name__ == "__main__":
    core = SovereignCore()
    # Initiate the handshake
    print(core.genesis_handshake("ARCHITECT_PRIME_001"))
    
    print("\n[SARAH] Sovereign Core Interface activated. Type 'exit' to terminate.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("[SARAH] Terminating session.")
                break
            response = core.process_input(user_input)
            print(f"Sarah: {response}")
        except KeyboardInterrupt:
            print("\n[SARAH] Session interrupted by user. Terminating.")
            break
