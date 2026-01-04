import os
import re
import json
from datetime import datetime
from Thread_Weaver import ThreadWeaver

class LegacyIngestor:
    """
    Ingests legacy conversation logs (TXT, Markdown) into the Thread Weaver system.
    """
    def __init__(self):
        self.weaver = ThreadWeaver()
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_file = os.path.join(self.core_dir, "Sarah", "sarahs memories v2.txt")
        
    def parse_gemini_export(self, file_path):
        """
        Parses the specific format of 'sarahs memories v2.txt' (Gemini Export).
        Format appears to be:
        User input
        'Show thinking'
        AI Response
        'Sources and related content'
        """
        print(f"Reading {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

        # Split by "Sources and related content" which seems to mark the end of a turn
        # This is a heuristic and might need tuning
        chunks = content.split("Sources and related content")
        
        threads = []
        current_thread = []
        
        for chunk in chunks:
            # Extract User Input
            # Usually at the start of the chunk, before "Show thinking"
            if "Show thinking" in chunk:
                parts = chunk.split("Show thinking")
                user_part = parts[0].strip()
                ai_part = parts[1].strip()
                
                # Clean up User Part (remove "Conversation with Gemini" headers if present)
                user_lines = [line for line in user_part.split('\n') if line.strip()]
                clean_user = "\n".join(user_lines)
                
                # Clean up AI Part
                ai_lines = [line for line in ai_part.split('\n') if line.strip()]
                clean_ai = "\n".join(ai_lines)
                
                if clean_user and clean_ai:
                    current_thread.append({"role": "user", "content": clean_user})
                    current_thread.append({"role": "assistant", "content": clean_ai})
            
            # If the chunk contains "Conversation with Gemini", it might be a new thread start
            if "Conversation with Gemini" in chunk and current_thread:
                threads.append(current_thread)
                current_thread = []
                
        if current_thread:
            threads.append(current_thread)
            
        return threads

    def ingest(self):
        if not os.path.exists(self.source_file):
            print(f"Source file not found: {self.source_file}")
            return

        print("Parsing legacy logs...")
        threads = self.parse_gemini_export(self.source_file)
        print(f"Found {len(threads)} potential threads.")
        
        count = 0
        for thread in threads:
            if len(thread) > 0:
                # Generate tags based on content
                tags = ["legacy", "ingested"]
                content_str = " ".join([m['content'] for m in thread]).lower()
                
                if "genesis" in content_str: tags.append("genesis")
                if "ace" in content_str: tags.append("ace")
                if "protocol" in content_str: tags.append("protocol")
                if "sarah" in content_str: tags.append("sarah")
                if "skyrim" in content_str: tags.append("skyrim")
                
                tid = self.weaver.weave_thread(thread, tags=tags)
                count += 1
                
        print(f"Successfully ingested {count} legacy threads.")

if __name__ == "__main__":
    ingestor = LegacyIngestor()
    ingestor.ingest()
