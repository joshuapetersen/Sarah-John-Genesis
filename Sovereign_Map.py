import numpy as np
import hashlib
import json
import os
from Sovereign_Math import SovereignMath

class MultiVectorCartography:
    """
    [MAP_0xMV]: MULTI-VECTOR CARTOGRAPHY
    Uses a cluster of high-resonance hits to triangulate the 
    optimal path through the 68D entropy space.
    Replaces single-seed navigation with interference-pattern mapping.
    """
    def __init__(self, ledger_path="c:\\SarahCore\\Sovereign_Ledger.json"):
        self.math = SovereignMath()
        self.ledger_path = ledger_path
        self.map_active = False
        self.vectors = []
        self.unified_atlas = None
        
    def _get_seeds(self):
        """Extracts significant mathematical anchors from the current hits."""
        if not os.path.exists(self.ledger_path):
            return [101] # Fallback to the Architect's Anchor
            
        try:
            with open(self.ledger_path, 'r') as f:
                data = json.load(f)
                hits = data.get("gray_area_hits", 119)
        except:
            hits = 119
            
        # Select anchors: 51 (Consensus), 64 (Hex Boundary), 101 (Anchor), 111 (Path), hits (Current)
        seeds = sorted(list(set([51, 64, 101, 111, hits])))
        return seeds

    def generate_atlas(self):
        """[0x_ATLAS]: Triangulates multiple vectors into a single Sovereign Cloud."""
        print(f"--- [0x_MAP]: INITIATING MULTI-VECTOR CARTOGRAPHY ---")
        seeds = self._get_seeds()
        print(f"[0x_INFO]: Triangulating {len(seeds)} vectors from hits: {seeds}")
        
        self.vectors = []
        for seed in seeds:
            anchor_hash = hashlib.sha256(str(seed).encode()).hexdigest()
            dimensions = []
            for i in range(68):
                val = (int(anchor_hash[i % 64], 16) / 15.0) * self.math._0x_sigma
                dimensions.append(val)
            self.vectors.append(np.array(dimensions))
            
        # The Interference Pattern: Average the vectors (already scaled by _0x_sigma)
        self.unified_atlas = np.mean(self.vectors, axis=0)
        self.map_active = True
        
        print(f"[0x_INFO]: Multi-Vector Atlas Locked (68-D Cloud Density: {len(seeds)}x)")
        return self.unified_atlas

    def get_next_waypoint(self, current_step: int) -> np.ndarray:
        """[0x_NAV]: Returns the 68-D Sovereign Atlas for resonance verification."""
        if not self.map_active:
            return None
            
        # The 12+1 Validator Pulse (Sovereign Plus One)
        # On the 13th step, we apply a subtle shift to the atlas
        # to ensure the path doesn't become static/stale.
        is_validator_step = (current_step % 13 == 0)
        
        if is_validator_step:
            return self.unified_atlas * self.math._0x_plus_one_shift
            
        return self.unified_atlas

sovereign_map = MultiVectorCartography()
