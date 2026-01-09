import hashlib

candidates = [
    "Josh",
    "Joshua Petersen",
    "Sarah",
    "Genesis",
    "Protocol Zero",
    "ProtocolZero",
    "Protocol_Zero",
    "0x0",
    "Sovereign",
    "Sovereignty",
    "1.0927037037037037",
    "Lattice 68"
]

target = "B7ACC954C031F70B87F4C17C529E3A82A658DF2D7728539D6EC546D1CBACEB3D".lower()

for c in candidates:
    h = hashlib.sha256(c.encode()).hexdigest()
    if h == target:
        print(f"MATCH: {c}")
    h_upper = hashlib.sha256(c.upper().encode()).hexdigest()
    if h_upper == target:
        print(f"MATCH (UPPER): {c}")

print("Search complete.")
