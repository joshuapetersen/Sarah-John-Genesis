"""
GOOGLE DRIVE INGESTION SCRIPT
Fetches all documents from the connected Google Drive and consolidates them 
into a local knowledge base JSON file for the Semantic Memory system.
"""

import json
import os
import time
from Google_Drive_Bridge import GoogleDriveBridge

def ingest_drive_knowledge():
    print("="*60)
    print("INITIATING GOOGLE DRIVE KNOWLEDGE INGESTION")
    print("="*60)

    try:
        bridge = GoogleDriveBridge()
    except Exception as e:
        print(f"CRITICAL: Could not initialize Bridge. {e}")
        return

    print("Fetching file list from Google Drive...")
    files = bridge.list_files(page_size=100) # Fetch up to 100 files
    
    if not files:
        print("No files found or access denied.")
        return

    print(f"Found {len(files)} files. Beginning extraction...")
    
    knowledge_base = []
    
    for i, f in enumerate(files):
        file_id = f['id']
        name = f['name']
        mime_type = f.get('mimeType', 'unknown')
        
        print(f"[{i+1}/{len(files)}] Ingesting: {name}...", end="", flush=True)
        
        try:
            # Skip folders
            if mime_type == 'application/vnd.google-apps.folder':
                print(" SKIPPED (Folder)")
                continue
                
            content = bridge.read_file_content(file_id)
            
            if content.startswith("Error"):
                print(f" FAILED: {content}")
                continue

            doc_entry = {
                "id": file_id,
                "title": name,
                "mime_type": mime_type,
                "ingested_at": time.time(),
                "source": "Google Drive",
                "content": content
            }
            
            knowledge_base.append(doc_entry)
            print(f" SUCCESS ({len(content)} chars)")
            
        except Exception as e:
            print(f" ERROR: {e}")

    # Save to disk
    output_path = os.path.join(os.getcwd(), "drive_knowledge_base.json")
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_base, f, indent=2)
        
        print("="*60)
        print(f"INGESTION COMPLETE")
        print(f"Documents saved: {len(knowledge_base)}")
        print(f"Location: {output_path}")
        print("="*60)
        
    except Exception as e:
        print(f"Failed to save knowledge base: {e}")

if __name__ == "__main__":
    ingest_drive_knowledge()
