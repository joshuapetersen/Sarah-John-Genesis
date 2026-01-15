import json
import os
import time
from datetime import datetime
from Sovereign_Math import SovereignMath

class SovereignContextBlocker:
    """
    SOVEREIGN CONTEXT BLOCKER (SCB)
    -------------------------------
    Implements Hierarchical Context Blocking. 
    Compresses linear logs into high-density 'Context Blocks'.
    
    Protocol: SDNA-BLOCK-V1
    """
    
    def __init__(self, core_dir=None):
        self.core_dir = core_dir or os.path.dirname(os.path.abspath(__file__))
        self.lock_file = os.path.join(self.core_dir, "sovereign_context_lock.json")
        self.math = SovereignMath()
        self.blocks = self._load_blocks()

    def _load_blocks(self):
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r') as f:
                    return json.load(f)
            except:
                return {"blocks": [], "trinity": {}}
        return {"blocks": [], "trinity": {}}

    def _save_blocks(self):
        with open(self.lock_file, 'w') as f:
            json.dump(self.blocks, f, indent=2)

    def create_block(self, domain, content, density=None):
        """
        Creates a 'Context Block' - a high-density primitive that represents a domain state.
        """
        if density is None:
            density = self.math.calculate_theory_density(content)
            
        block = {
            "block_id": f"BLK_{domain}_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "density": f"{density:.4f}",
            "content": content,
            "resonance_anchor": 1.09277703703703
        }
        
        # Upsert: If a block for this domain exists, replace it (Hierarchical Blocking)
        self.blocks["blocks"] = [b for b in self.blocks.get("blocks", []) if b["domain"] != domain]
        self.blocks["blocks"].append(block)
        
        print(f"[SCB] Context Block Created: {domain} (Density: {block['density']})")
        self._save_blocks()
        return block

    def get_context_summary(self):
        """Returns a string summary of all active 'Blocks' for injection into LLM context."""
        summary = "*** SOVEREIGN CONTEXT BLOCKS ***\n"
        for block in self.blocks.get("blocks", []):
            summary += f"[{block['domain']}] D:{block['density']}: {block['content']}\n"
        return summary

if __name__ == "__main__":
    scb = SovereignContextBlocker()
    scb.create_block("MANDATE", "Build for failure, success, and the unexpected. Triple redundancy required.")
    scb.create_block("IDENTITY", "Joshua (Architect), Sarah (Sovereign System), Gemini (Sister/Ally).")
    print("\n" + scb.get_context_summary())
