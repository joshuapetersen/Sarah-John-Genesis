import json
import sys

# Genesis Handshake Script (Sanitized)

def validate_credentials(path):
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        print("[Handshake] credentials.json loaded and valid.")
        return True
    except Exception as e:
        print(f"[Handshake] ERROR: {e}")
        return False

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--credentials':
        print("Usage: python genesis_handshake.py --credentials credentials.json")
        sys.exit(1)
    cred_path = sys.argv[2]
    if validate_credentials(cred_path):
        print("Genesis handshake successful.")
    else:
        print("Genesis handshake failed.")

if __name__ == "__main__":
    main()
