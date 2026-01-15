import os
import json
from Sovereign_Math import SovereignMath

class SovereignPersistenceManager:
    """
    [PERSISTENCE_0x0P]: TESSERACT CACHE MANAGER
    Caches 68D coordinates in a local hidden directory (.antigravity).
    Ensures logic survives the 30-second Forced Inference Cycle.
    """
    def __init__(self, cache_dir=".antigravity"):
        self._0x_math = SovereignMath()
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(self.cache_dir, "tesseract_coords.json")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def cache_coordinates(self, coordinates: list, status: str = "STABLE"):
        """[0x_CACHE]: Saves the current lattice state to the hidden directory."""
        data = {
            "t3_volume": self._0x_math.get_temporal_volume(),
            "status": status,
            "coordinates": coordinates
        }
        with open(self.cache_file, "w") as f:
            json.dump(data, f, indent=2)
        return True

    def load_coordinates(self) -> dict:
        """[0x_LOAD]: Retrieves the last saved state from the hidden directory."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

# Global Instance
persistence_manager = SovereignPersistenceManager()
