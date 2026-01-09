from Sovereign_Alpha_Numeric_Codec import codec
import os

def ingest_chrome():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        
    print(f"--- [SARAH_0x0I]: INGESTING CHROME ---")
    if os.path.exists(chrome_path):
        try:
            print(f"Ingesting binary: {chrome_path}")
            _0x_code = codec.encode_file(chrome_path)
            codec.define_logic("CHROME_BINARY_CORE", _0x_code)
            
            # Save the new manifest
            codec.write_manifest("c:/SarahCore/sovereign_logic_manifest.json")
            print(f"INGESTION SUCCESSFUL: {_0x_code[:32]}...")
            
            # Translate to Context Modality
            translation = codec.translate(_0x_code, "context")
            print(f"TRANSLATION: {translation}")
            
        except Exception as e:
            print(f"INGESTION FAILED: {e}")
    else:
        print("CHROME NOT FOUND AT DESIGNATED COORDINATES.")

if __name__ == "__main__":
    ingest_chrome()
