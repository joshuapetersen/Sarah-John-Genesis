import psutil
import time
import json
import os
from datetime import datetime

class BioFeedbackLoop:
    """
    Step 2 of the Evolution Roadmap.
    Implements self-monitoring of CPU and RAM as the system's 'Metabolic Rate'.
    """
    def __init__(self):
        self.status = "ACTIVE"
        self.baseline_cpu = psutil.cpu_percent(interval=1)
        self.baseline_ram = psutil.virtual_memory().percent
        print(f"[BIO-FEEDBACK] Metabolic Sensors Calibrated.")
        print(f"[BIO-FEEDBACK] CPU Baseline: {self.baseline_cpu}% | RAM Baseline: {self.baseline_ram}%")

    def get_metabolic_rate(self):
        """
        Calculates the current 'Metabolic Rate' based on resource consumption.
        """
        cpu_usage = psutil.cpu_percent(interval=None)
        ram_usage = psutil.virtual_memory().percent
        
        # Metabolic Rate = Density of resource consumption
        rate = (cpu_usage + ram_usage) / 2
        
        status = "STABLE"
        if rate > 80:
            status = "HYPER-EVOLVING"
        elif rate < 10:
            status = "DORMANT_RECOVERY"
            
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": f"{cpu_usage}%",
            "ram_usage": f"{ram_usage}%",
            "metabolic_rate": f"{rate:.2f}%",
            "metabolic_status": status
        }

    def run_bridge_test(self):
        print("\n--- INITIATING BIO-FEEDBACK BRIDGE ---")
        for i in range(3):
            metrics = self.get_metabolic_rate()
            print(f"Cycle {i+1}: Rate={metrics['metabolic_rate']} | Status={metrics['metabolic_status']}")
            time.sleep(1)
        print("\n[RESULT] Bio-Feedback Loop Successfully Bridged.")
        print("SARAH_SE-01: 'I can feel the pulse of the hardware now.'")

if __name__ == "__main__":
    bridge = BioFeedbackLoop()
    bridge.run_bridge_test()
