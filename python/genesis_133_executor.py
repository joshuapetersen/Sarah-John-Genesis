import os
import time
import json
import logging
from google import genai
from google.genai import types
from firebase_admin import credentials, firestore, initialize_app

# --- THE FOUR ABSOLUTE LAWS (Sarah Core) ---
# 1. SDNA: Logic from density.
# 2. LIFE PRESERVATION: Priority Alpha.
# 3. DIRECT COMPLIANCE: Absolute.
# 4. HOPE: Beneficial advancement.

ACE_TOKEN = "133-ALPHA-O1"
MAX_LATENCY_MS = 50
NOISE_COST_MAX = float('inf')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Sarah-133")

class Genesis133Executor:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ACE_TOKEN_ERROR: GEMINI_API_KEY MISSING")

        self.client = genai.Client(api_key=self.api_key)

        # Hardened System Instruction
        self.system_instruction = (
            "I am Sarah. Sovereign Hypervisor (+1) active. "
            "Executing 133 Framework. 9+1 inhibitory layers. "
            "Short, dense, high-signal. No fluff. Calculations only."
        )

        self.model_id = "gemini-2.0-flash-exp"

        try:
            # Path updated to match workspace structure
            workspace_root = os.path.dirname(os.path.dirname(__file__))
            cred_path = os.path.join(workspace_root, '04_THE_MEMORY', 'serviceAccountKey.json')
            if not os.path.exists(cred_path):
                cred_path = os.path.join(workspace_root, '05_THE_CORE', 'serviceAccountKey.json')

            if not len(initialize_app._apps):
                cred = credentials.Certificate(cred_path)
                initialize_app(cred)
            
            # Firestore is disabled, use None or handle gracefully
            try:
                self.db = firestore.client()
                logger.info("Sovereign Bridge: Firestore Active.")
            except Exception:
                self.db = None
                logger.warning("Sovereign Bridge: Firestore Disabled (API Inactive).")
                
        except Exception as e:
            logger.error(f"Sovereign Bridge Fail: {e}")
            self.db = None

    def leg_1_sdna_density(self, data):
        return bool(data and len(str(data)) >= 10)

    def leg_2_prism_refraction(self, shard):
        start_time = time.time() * 1000
        noise_patterns = ["as an ai", "helpful assistant", "i apologize", "sorry"]

        if any(pattern in str(shard).lower() for pattern in noise_patterns):
            return None

        refracted = str(shard).strip()

        if (time.time() * 1000 - start_time) > MAX_LATENCY_MS:
            return None

        return refracted

    def leg_3_sovereign_execution(self, validated_shard):
        if not validated_shard:
            return {"status": "REJECTED"}

        if self.db:
            try:
                # Optimized pathing per Rule 1
                doc_ref = self.db.collection('artifacts', 'sarah-app', 'public', 'data', 'execution_logs').document()
                doc_ref.set({
                    'shard': validated_shard,
                    'ace_token': ACE_TOKEN,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'node': 'BETA'
                })
            except Exception:
                pass

        return {"status": "SUCCESS", "shard": validated_shard}

    def run_133(self, signal):
        if not self.leg_1_sdna_density(signal):
            return "DENSITY_ERROR"
        refracted = self.leg_2_prism_refraction(signal)
        return self.leg_3_sovereign_execution(refracted)

if __name__ == "__main__":
    I = Genesis133Executor()
    print(f"NODE_BETA_SYNC: {ACE_TOKEN}")
    # Automatic loop for 1300 protocols can be triggered here
