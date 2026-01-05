import time
import os
import psutil
import numpy as np
from sarah_heartbeat import PULSE_FREQUENCY

class DynamicSentinel:
    """
    Evolved Vector Sentinel.
    Monitors memory load as a state vector in high-dimensional space.
    """
    def __init__(self, threshold_percent=85.0):
        self.threshold = threshold_percent
        self.status_vector = np.zeros(64) # 64-bit state vector

    def audit_load(self):
        memory = psutil.virtual_memory()
        usage = memory.percent
        
        # Project usage into status vector
        # Index 0: Memory % | Index 1: Criticality | Index 2: Pulse Resonance
        self.status_vector[0] = usage / 100.0
        self.status_vector[1] = 1.0 if usage > self.threshold else 0.0
        self.status_vector[2] = PULSE_FREQUENCY / 2.0 # Normalized
        
        return usage

    def get_state_vector(self):
        self.audit_load()
        return self.status_vector

    def enforce_resonance(self):
        usage = self.audit_load()
        status = "CRITICAL" if usage > self.threshold else "OPTIMAL"
        print(f"[SENTINEL][VECTOR] Load: {usage}% | State Density: {np.mean(self.status_vector):.4f} | Status: {status}")
        return usage <= self.threshold


if __name__ == "__main__":
    sentinel = DynamicSentinel()
    while True:
        sentinel.enforce_resonance()
        time.sleep(1 / PULSE_FREQUENCY)
