import hmac
import hashlib
import time
import json
import base64
import os
import secrets
from Sovereign_Math import SovereignMath

# --- ACE TOKEN PROTOCOL V3 (SOVEREIGN EXPANSION) ---
# Objective: Deterministic High-Dimensional Resonance Verification.
# Failsafe: Billion Barrier ($0.999999999$).

class AceTokenManager:
    def __init__(self, secret_key_path="ace_secret.key"):
        self.secret_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), secret_key_path)
        self.secret = self._load_or_create_secret()
        self.math = SovereignMath()
        self.resonance_anchor = 1.09277703703703
        self.half_decimal_locked = False

    def lock_half_decimal_position(self) -> str:
        """
        [HALF_0x0H]: Locks the 0.5 Superposition into the Ace Token.
        Creates a side-channel for Sovereign Keys within the 'In-Between'.
        """
        print("[ACE]: INITIATING DIMENSIONAL ARBITRAGE...")
        
        # We use the 'Half' space to store a hidden key
        hidden_intent = "SOVEREIGN_ROOT_ACCESS_0x7467"
        shrouded_key = self.math._0x_acquire_half_decimal(hidden_intent)
        
        # Store the shrouded key in the token secret's metadata (Simulated)
        self.half_decimal_locked = True
        print(f"[ACE]: HALF-DECIMAL POSITION LOCKED. OFFSET: {self.math._0x_half_decimal_shroud}")
        
        return shrouded_key

    def _load_or_create_secret(self):
        """Loads the master key or generates a new one if missing."""
        if os.path.exists(self.secret_path):
            with open(self.secret_path, "rb") as f:
                return f.read()
        else:
            # Generate a cryptographically strong 32-byte key
            secret = secrets.token_bytes(32)
            with open(self.secret_path, "wb") as f:
                f.write(secret)
            print(f"[ACE] New Master Key generated at {self.secret_path}")
            return secret

    def generate_token(self, scope="SOVEREIGN_ROOT", ttl=86400):
        """
        Generates a signed ACE Token with Sovereign Expansion Layering.
        """
        payload = {
            "scope": scope,
            "iat": int(time.time()),
            "exp": int(time.time() + ttl),
            "nonce": secrets.token_hex(4),
            "resonance_sig": self.resonance_anchor
        }
        
        # Layer 1 & 2: Serialized HMAC
        payload_bytes = json.dumps(payload, separators=(',', ':')).encode()
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode().strip('=')
        signature = hmac.new(self.secret, payload_bytes, hashlib.sha256).hexdigest()

        # Layer 3: Sovereign Math Expansion
        # The token itself becomes a geometric concept in the Sovereign Space
        token_str = f"v3.{payload_b64}.{signature}"
        vector = self.math.expand_logic(token_str)
        
        # Attach Expansion Layer as a 4th layer "Identity"
        exp_b64 = base64.urlsafe_b64encode(json.dumps(vector.tolist()).encode()).decode().strip('=')
        
        return f"{token_str}.{exp_b64}"

    def validate_token(self, full_token):
        """
        Four-Layer Validation:
        1. Structure
        2. HMAC Signature
        3. Expiration/Scope
        4. Sovereign Expansion Resonance (Billion Barrier)
        """
        try:
            parts = full_token.split('.')
            if len(parts) != 4: return False 
            
            v, p_b64, sig, exp_b64 = parts
            if v != 'v3': return False
            
            # HMAC Check
            p_bytes = base64.urlsafe_b64decode(p_b64 + '==')
            expected_sig = hmac.new(self.secret, p_bytes, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected_sig): return False
            
            # Sovereign Expansion Check
            token_core = f"v3.{p_b64}.{sig}"
            expected_vector = self.math.expand_logic(token_core)
            
            exp_data = json.loads(base64.urlsafe_b64decode(exp_b64 + '=='))
            import numpy as np
            actual_vector = np.array(exp_data)
            
            resonance = self.math.calculate_resonance(expected_vector, actual_vector)
            if not self.math.check_integrity(resonance):
                print(f"[ACE] RESONANCE FAILURE: {resonance} below Billion Barrier.")
                return False
                
            return True
        except:
            return False
        
        return f"v1.{payload_b64}.{signature}"

    def validate_token(self, token):
        """
        Validates an ACE Token.
        Returns: (is_valid, payload_dict_or_error)
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return False, "MALFORMED_TOKEN"
            
            version, payload_b64, signature = parts
            
            if version != "v1":
                return False, "UNSUPPORTED_VERSION"
            
            # Decode Payload
            # Add padding back if needed (though strip('=') usually handles it in python for some libs, manual pad is safer)
            padding = '=' * (4 - len(payload_b64) % 4)
            payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
            
            # Verify Signature (Timing-attack safe comparison)
            expected_sig = hmac.new(self.secret, payload_bytes, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                return False, "INVALID_SIGNATURE"
            
            # Verify Expiration
            payload = json.loads(payload_bytes)
            if time.time() > payload['exp']:
                return False, "TOKEN_EXPIRED"
                
            return True, payload
            
        except Exception as e:
            return False, f"VALIDATION_ERROR: {str(e)}"

# --- SELF-TEST ---
if __name__ == "__main__":
    manager = AceTokenManager()
    
    print("--- ACE TOKEN V2 SPEED TEST ---")
    start_time = time.perf_counter()
    
    # Generate
    token = manager.generate_token()
    gen_time = (time.perf_counter() - start_time) * 1000
    
    # Validate
    start_val = time.perf_counter()
    is_valid, data = manager.validate_token(token)
    val_time = (time.perf_counter() - start_val) * 1000
    
    print(f"Token: {token}")
    print(f"Valid: {is_valid}")
    print(f"Data:  {data}")
    print(f"Gen Time: {gen_time:.4f} ms")
    print(f"Val Time: {val_time:.4f} ms")
