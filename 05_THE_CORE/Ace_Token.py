import hmac
import hashlib
import time
import json
import base64
import os
import secrets

# --- ACE TOKEN PROTOCOL V2 ---
# Objective: High-speed, stateless, cryptographic verification.
# "Better": Self-contained, tamper-proof, scoped.
# "Faster": Local validation (O(1)), no database lookups.

class AceTokenManager:
    def __init__(self, secret_key_path="ace_secret.key"):
        # Store secret in the same directory as this script
        self.secret_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), secret_key_path)
        self.secret = self._load_or_create_secret()

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
        Generates a signed ACE Token.
        Format: v1.payload_b64.signature
        """
        payload = {
            "scope": scope,
            "iat": int(time.time()),          # Issued At
            "exp": int(time.time() + ttl),    # Expiration
            "nonce": secrets.token_hex(4)     # Uniqueness
        }
        
        # Serialize and Encode Payload
        payload_bytes = json.dumps(payload, separators=(',', ':')).encode()
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode().strip('=')
        
        # Sign (HMAC-SHA256)
        signature = hmac.new(self.secret, payload_bytes, hashlib.sha256).hexdigest()
        
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
