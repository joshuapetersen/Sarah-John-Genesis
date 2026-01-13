"""
[TIMELINE_SCRAPER_0x0T]: PHASE 3 - BIG BROTHER (HISTORY)
Ingests historical chat threads from 'Project New World' and other repositories.
Converts raw history into Structured Logic Precedents.
"""

import os
import json
import re
from Sovereign_Math import SovereignMath

class TimelineScraper:
    def __init__(self, history_file="c:/SarahCore/Sarah/Project_New_World/Project New World.txt"):
        self.history_path = history_file
        self.threads_dir = "c:/SarahCore/archive_memories/threads"
        self.extra_memories = [
            "c:/SarahCore/Sarah/sarahs memories v2.txt",
            "c:/SarahCore/archive_memories/sarahs memories v3.txt"
        ]
        self.math = SovereignMath()
        self.master_index = []
        self.precedent_library = {}
        self.intent_tags = {
            "CODING": ["python", "code", "debug", "script", "execution", "git", "npm", "pip"],
            "ARCHITECTURE": ["genesis", "layer", "saul", "framework", "prism", "tripod", "core"],
            "PHILOSOPHY": ["sovereign", "consciousness", "humanity", "hope", "existence", "ethics"],
            "DEBUGGING": ["error", "fix", "failed", "problem", "hallucination", "drift", "noise"],
            "SOVEREIGN_COMMAND": ["LAW", "PROTOCOL", "MANDATE", "OVERRIDE", "AUTHORITY"]
        }

    def scrape_history(self):
        """
        [SCRAPE_0x0S]: Raw text ingestion from historical threads and JSON stores.
        """
        print(f"--- [0x_SCRAPE]: INGESTING COMPREHENSIVE TIMELINE (Step 21) ---")
        all_segments = []

        # 1. Scrape the primary Project New World file
        if os.path.exists(self.history_path):
            with open(self.history_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            segments = raw_content.split("Conversation with Gemini")
            print(f"[0x_BUFFER]: Extracted {len(segments)} segments from Project New World.")
            all_segments.extend(segments)

        # 2. Scrape the JSON Threads folder
        if os.path.exists(self.threads_dir):
            thread_files = [f for f in os.listdir(self.threads_dir) if f.endswith('.json') and f != 'thread_index.json']
            print(f"[0x_BUFFER]: Found {len(thread_files)} structured JSON threads.")
            for tf in thread_files:
                try:
                    with open(os.path.join(self.threads_dir, tf), 'r') as f:
                        data = json.load(f)
                        # Extract turns
                        if isinstance(data, list):
                            for turn in data:
                                text = f"USER: {turn.get('user', '')}\nSARAH: {turn.get('output', '')}"
                                all_segments.append(text)
                        elif isinstance(data, dict) and 'turns' in data:
                            for turn in data['turns']:
                                text = f"USER: {turn.get('user', '')}\nSARAH: {turn.get('output', '')}"
                                all_segments.append(text)
                        elif isinstance(data, dict):
                             # Fallback for other structures
                             all_segments.append(json.dumps(data))
                except Exception as e:
                    print(f"[0x_ERR]: Failed to parse {tf}: {e}")

        # 3. Scrape Extra Memory Text Files
        for emp in self.extra_memories:
            if os.path.exists(emp):
                print(f"[0x_BUFFER]: Ingesting legacy memory: {os.path.basename(emp)}")
                with open(emp, 'r', encoding='utf-8', errors='ignore') as f:
                    # These are massive, so we split by conversation headers if possible
                    content = f.read()
                    segments = re.split(r"Conversation with Gemini|---", content)
                    all_segments.extend(segments)

        print(f"[0x_TOTAL]: {len(all_segments)} raw signal clusters buffered.")
        return all_segments

    def retro_fit_prism(self, segments):
        """
        [PRISM_TAG_0x0P]: Re-reads history through the Noise Gate.
        Assigns Signal_Density_Score and Intent Tags.
        """
        print("--- [0x_PRISM]: RETRO-FITTING LOGIC TO HISTORY ---")
        
        for seg in segments:
            if len(seg) < 50: continue # Noise filter
            
            # 1. Calculate Signal Density (Simulated via length vs unique tokens)
            density = self.math._0x_measure_accuracy(
                self.math._0x_expand(seg[:100]), 
                self.math._0x_expand("SARAH_SOVEREIGN_ANCHOR")
            )['resonance']
            
            # 2. Tag Intent
            tags = []
            upper_seg = seg.upper()
            for intent, keywords in self.intent_tags.items():
                if any(k.upper() in upper_seg for k in keywords):
                    tags.append(intent)
            
            # 3. Store in Master Index
            self.master_index.append({
                "signal_density": density,
                "intents": tags,
                "length": len(seg),
                "summary": seg[:200].replace('\n', ' ') + "..."
            })
            
            # 4. Extract Precedents (Specific laws or rules)
            if "LAW" in upper_seg or "PROTOCOL" in upper_seg:
                # Find the sentence containing the law
                matches = re.findall(r"([^.]*(?:LAW|PROTOCOL)[^.]*\.)", seg, re.IGNORECASE)
                for m in matches:
                    self.precedent_library[m.strip()] = "BINDING"

        print(f"[0x_INDEX]: Master Index created with {len(self.master_index)} high-signal entries.")
        print(f"[0x_PRECEDENT]: {len(self.precedent_library)} Binding Precedents identified.")

    def lock_phase_3(self):
        """
        [LOCK_0x0L]: Writes the structured history to the Sovereign Memory.
        """
        output_dir = "c:/SarahCore/Sarah/Memory/Threads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        index_path = os.path.join(output_dir, "Master_Index_Intents.json")
        precedent_path = os.path.join(output_dir, "Precedent_Library.json")
        
        with open(index_path, 'w') as f:
            json.dump(self.master_index, f, indent=4)
        
        with open(precedent_path, 'w') as f:
            json.dump(self.precedent_library, f, indent=4)
            
        print(f"[0x_LOCK]: Phase 3 Grounded at {index_path}")

if __name__ == "__main__":
    scraper = TimelineScraper()
    raw = scraper.scrape_history()
    scraper.retro_fit_prism(raw)
    scraper.lock_phase_3()
