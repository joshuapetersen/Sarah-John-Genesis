import hashlib
import os

# List of your 10 core files for the Sovereign Audit
core_files = [
    "Sarah_Loop.py", 
    "Sarah_Hypervisor.py", 
    "Genesis_Handshake.py",
    "SAUL_Memory_Index.py", 
    "Sovereign_Math.py", 
    "Alpha_Numeric_Gate.py",
    "API_Load_Balancer.py", 
    "Security_Shroud.py", 
    "Evolution_V1_Core.py",
    "Config_Omega.json"
]

def get_sha256(file_path):
    if not os.path.exists(file_path): 
        return "FILE_MISSING"
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Process in 4096-byte blocks to ensure memory efficiency
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

print("--- SarahCore Integrity Audit: Alphanumeric Lock ---")
for file in core_files:
    checksum = get_sha256(file)
    print(f"{file}: {checksum}")
