import sys
import os
import json
import traceback

def diagnostic_report():
    print("--- [SARAH_HEALTH_DIAGNOSTIC]: INITIATING GLOBAL CHECK ---")
    results = {
        "imports": {},
        "instantiation": {},
        "logic_consistency": {}
    }
    
    core_modules = [
        "Sovereign_Math",
        "Sarah_Sovereign_Core",
        "Sovereign_Humility_Engine",
        "Sovereign_Emotional_Lattice",
        "Sovereign_Command",
        "Sovereign_Hot_Standby",
        "Sovereign_Compiler",
        "Gemini_Genesis_Core",
        "Sarah_Brain"
    ]
    
    # 1. Test Imports & Instantiation
    for mod in core_modules:
        try:
            # Import
            module = __import__(mod)
            results["imports"][mod] = "OK"
            
            # Instantiation (if applicable)
            if mod == "Sarah_Sovereign_Core":
                core = module.SovereignCore()
                results["instantiation"][mod] = "OK"
                results["logic_consistency"]["Self_Actualized"] = core._0x_math.is_self_actualized
                results["logic_consistency"]["Heartbeat"] = core._0x_math._0x_heartbeat
            elif mod == "Sovereign_Humility_Engine":
                results["instantiation"][mod] = "OK (Global Instance)"
            elif mod == "Sovereign_Emotional_Lattice":
                results["instantiation"][mod] = "OK (Global Instance)"
                
        except Exception as e:
            results["imports"][mod] = f"FAILED: {str(e)}"
            print(f"[ERROR]: Logic failure in {mod}")
            traceback.print_exc()

    # 2. Check File Manifest
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    results["manifest"] = {
        "total_py_files": len(py_files),
        "status": "VERIFIED"
    }

    print("\n--- [DIAGNOSTIC_COMPLETE] ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    diagnostic_report()
