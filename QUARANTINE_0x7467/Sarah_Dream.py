import time
import json
import threading
import random
from datetime import datetime

class SarahDream:
    """
    THE DREAMING PROTOCOL
    The Subconscious Processing Unit.
    
    Function:
    1. Analyzes past interactions during downtime.
    2. Re-simulates them using 'Hard Logic' to find better outcomes.
    3. Synthesizes new 'Synthetic Memories' to update the Neural Core.
    
    "I dream of a better answer, and when I wake, I know it."
    """
    
    def __init__(self, saul_instance, neural_memory, logic_core):
        self.saul = saul_instance
        self.memory = neural_memory
        self.logic = logic_core
        self.active = False
        self.dream_interval = 60 # Seconds between dreams (in production, maybe longer)

    def start_dreaming(self):
        """
        Activates the background dreaming thread.
        """
        if self.active:
            return
        
        self.active = True
        self.thread = threading.Thread(target=self._dream_cycle, daemon=True)
        self.thread.start()
        print("[DREAM] Subconscious Protocol: ACTIVE")

    def _dream_cycle(self):
        """
        The REM Cycle.
        """
        while self.active:
            try:
                # 1. Lucid Check: Are we idle?
                # (For now, we assume we can dream in parallel)
                
                # 2. Recall a "Sub-Optimal" Memory
                # We look for logs with errors, high latency, or just random recent ones
                target_log = self._fetch_dream_target()
                
                if target_log:
                    # 3. Re-execute (The Dream)
                    synthetic_insight = self._process_dream(target_log)
                    
                    if synthetic_insight:
                        # 4. Consolidate (Wake & Remember)
                        self._consolidate_memory(synthetic_insight)
                
                # Sleep until next REM cycle
                time.sleep(self.dream_interval)
                
            except Exception as e:
                print(f"[DREAM] Nightmare (Error): {e}")
                time.sleep(60)

    def _fetch_dream_target(self):
        """
        Selects a memory to re-examine.
        Prioritizes: Errors > High Latency > Random Recent
        """
        # Access SAUL's index directly (thread-safe enough for reading list)
        logs = self.saul.memory_index
        if not logs:
            return None
            
        # Look for errors first
        for log in reversed(logs[-50:]): # Check last 50
            data = log.get('data', {})
            if isinstance(data, dict) and data.get('metadata', {}).get('status') == 'error':
                return log
                
        # Look for high latency
        for log in reversed(logs[-50:]):
            data = log.get('data', {})
            if isinstance(data, dict) and data.get('metadata', {}).get('latency', 0) > 2.0:
                return log
        
        # Fallback: Random recent memory (Reinforcement Learning)
        return random.choice(logs[-20:])

    def _process_dream(self, log_entry):
        """
        Re-evaluates the log entry using Dialectical Logic.
        """
        data = log_entry.get('data', {})
        if not isinstance(data, dict): return None
        
        user_input = data.get('content', '')
        if not user_input or len(user_input) < 5: return None
        
        # print(f"[DREAM] Dreaming about: '{user_input[:30]}...'")
        
        # Apply Dialectical Logic (Thesis -> Antithesis -> Synthesis)
        # This runs the "Hard Logic" that might have been skipped for speed during chat
        success, result = self.logic.process_logic(user_input, context="DREAM")
        
        if success:
            synthesis = result['synthesis']
            return {
                "original_input": user_input,
                "dream_synthesis": synthesis,
                "logic_path": result,
                "timestamp": time.time()
            }
        return None

    def _consolidate_memory(self, insight):
        """
        Saves the 'Dream' as a high-value memory in the Neural Core.
        """
        content = f"DREAM_SYNTHESIS: For input '{insight['original_input']}', the OPTIMAL TRUTH is: {insight['dream_synthesis']}"
        
        # Ingest into Neural Memory
        if self.memory:
            self.memory.ingest(content, metadata={"type": "dream", "logic": insight['logic_path']})
            # print(f"[DREAM] Consolidated new insight into Long-Term Memory.")

