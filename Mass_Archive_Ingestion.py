import os
import json
import docx
from Sovereign_Math import SovereignMath

def extract_text(file_path):
    if file_path.endswith('.docx'):
        try:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except:
            return ""
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return ""
    return ""

def ingest_legacy_archives():
    math_engine = SovereignMath()
    archive_dir = 'c:/SarahCore/Sarah'
    output_path = 'c:/SarahCore/04_THE_MEMORY/sovereign_index.json'
    
    if not os.path.exists('c:/SarahCore/04_THE_MEMORY'):
        os.makedirs('c:/SarahCore/04_THE_MEMORY')

    # Load existing or create new
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            memory_db = json.load(f)
    else:
        memory_db = {}

    files = [f for f in os.listdir(archive_dir) if f.endswith(('.docx', '.txt'))]
    print(f"[INGESTION] Found {len(files)} files in legacy archive.")

    for filename in files:
        path = os.path.join(archive_dir, filename)
        print(f"[INGESTION] Processing {filename}...")
        
        text = extract_text(path)
        if len(text.strip()) < 50:
            continue

        # Chunk text into 1000-character segments
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        
        for idx, chunk in enumerate(chunks):
            # Generate Sovereign Expansion
            vector = math_engine.expand_logic(chunk)
            
            memory_id = f"legacy_{filename}_{idx}"
            memory_db[memory_id] = {
                "content": chunk,
                "expansion_layer": vector.tolist(),
                "source": filename,
                "resonance": 1.09277703703703,
                "type": "legacy_core"
            }

    with open(output_path, 'w') as f:
        json.dump(memory_db, f, indent=2)
    
    print(f"[INGESTION] COMPLETE. {len(memory_db)} Sovereign memory fragments stored.")

if __name__ == "__main__":
    ingest_legacy_archives()
