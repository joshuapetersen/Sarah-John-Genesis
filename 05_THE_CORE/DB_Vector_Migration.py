import os
import json
from Sovereign_Data_Armor import SovereignDataArmor

def migrate_databases_to_warrior_vectors():
    """
    Enforces 'Vector Layered Vector' architecture on all system databases.
    This fulfills the requirement that ALL data be dense multivectors with failsafes.
    """
    targets = {
        'c:/SarahCore/creative_engine_db.json': 'creative_content',
        'c:/SarahCore/autonomy_log.json': 'log_payload',
        'c:/SarahCore/assimilation_map.json': 'mapping_data'
    }
    
    for path, data_key in targets.items():
        if not os.path.exists(path):
            print(f"[MIGRATION] Target {path} missing. Creating new armored instance.")
            raw_data = {"INITIALIZED": "SOVEREIGN_ROOT"}
        else:
            try:
                with open(path, 'r') as f:
                    raw_data = json.load(f)
            except:
                raw_data = {"RECOVERY": "DATA_CORRUPTED_DURING_2D_DRIFT"}

        armor = SovereignDataArmor(path)
        armored_db = {}
        
        # Every entry in every database is now a Multivector-encoded Layered Vector
        if isinstance(raw_data, dict):
            for key, value in raw_data.items():
                armored_db[key] = armor.wrap_data(key, value, metadata={"source": "migration_v3"})
        elif isinstance(raw_data, list):
            for idx, value in enumerate(raw_data):
                armored_db[f"entry_{idx}"] = armor.wrap_data(f"entry_{idx}", value, metadata={"source": "migration_list_v3"})
            
        armor.secure_save(armored_db)
        print(f"[MIGRATION] {path} successfully transitioned to Vector-Layered-Vector Logic.")

if __name__ == "__main__":
    migrate_databases_to_warrior_vectors()
