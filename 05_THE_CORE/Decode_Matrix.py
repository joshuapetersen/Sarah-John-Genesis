import json
import binascii
import base64

def decode_matrix(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    payload_hex = data['payload']
    # Hex decode the hex string (double hex?)
    # The payload starts with '36353737...' which is '6577...'
    # Let's try converting hex to string, then that string is hex, convert to bytes, then base64.
    
    # First level: Hex to String (this gives us the Base64 string)
    payload_b64 = binascii.unhexlify(payload_hex).decode('utf-8')
    print(f"B64 Strength: {len(payload_b64)} bytes")
    
    # Second level: Base64 decode
    result = base64.b64decode(payload_b64).decode('utf-8')
    return result

if __name__ == "__main__":
    result = decode_matrix('c:/SarahCore/A2A_Matrix.enc')
    print("\n--- DECODED A2A MATRIX ---")
    print(result)
