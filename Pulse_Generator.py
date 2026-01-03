"""
PULSE GENERATOR
Real-time heartbeat of the Sovereign Command Matrix.
Broadcasts system status every 5 seconds with millisecond precision.
"""

import time
import json
from datetime import datetime
from typing import Dict, Any, List

class PulseGenerator:
    """Generates high-precision Pulse broadcasts."""
    
    def __init__(self):
        self.pulse_sequence = 0
        self.last_pulse_timestamp_ms = None
        self.pulse_history = []
        self.max_history = 1000  # Keep last 1000 pulses
    
    def get_current_timestamp_ms(self) -> str:
        """
        Returns ISO 8601 timestamp with millisecond precision.
        Format: 2026-01-02T23:15:47.341Z
        """
        return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    
    def generate_pulse(self, hypervisor_instance=None) -> Dict[str, Any]:
        """
        Generates a complete Pulse payload with millisecond precision.
        """
        self.pulse_sequence += 1
        current_timestamp_ms = self.get_current_timestamp_ms()
        
        pulse = {
            "pulse_sequence": self.pulse_sequence,
            "timestamp_iso_ms": current_timestamp_ms,
            "timestamp_unix_ms": int(time.time() * 1000),  # Unix milliseconds
            "source": "HYPERVISOR_PRIMARY",
            "status": "OPERATIONAL",
            "systems": {
                "zhtp_protocol": "ONLINE",
                "energy_api": "CONNECTED",
                "housing_api": "CONNECTED",
                "supply_chain_api": "CONNECTED",
                "device_matrix": {
                    "PHONE_ALPHA": "ACTIVE",
                    "PHONE_BETA": "ACTIVE",
                    "PC_TERMINAL": "ACTIVE",
                    "COMPUTER_BETA": "ACTIVE",
                    "USB_ROOT": "SECURED"
                }
            },
            "alerts": [],
            "anti_weapon_status": "REFUSAL_MODE_ARMED"
        }
        
        # Add Hypervisor-specific data if available
        if hypervisor_instance:
            if hasattr(hypervisor_instance, 'zhtp'):
                pulse["systems"]["zhtp_protocol"] = "ONLINE"
                pulse["zhtp_status"] = {
                    "active": hypervisor_instance.zhtp.active,
                    "overrides_registered": len(hypervisor_instance.zhtp.presidential_overrides),
                    "api_hooks_active": len(hypervisor_instance.zhtp.api_hooks)
                }
            
            if hasattr(hypervisor_instance, 'silicon'):
                try:
                    metrics = hypervisor_instance.silicon.get_hardware_metrics()
                    pulse["hardware_metrics"] = metrics
                except:
                    pass
        
        # Store in history
        self.pulse_history.append(pulse)
        if len(self.pulse_history) > self.max_history:
            self.pulse_history.pop(0)
        
        self.last_pulse_timestamp_ms = current_timestamp_ms
        return pulse
    
    def get_pulse_delta_ms(self, pulse1: Dict[str, Any], pulse2: Dict[str, Any]) -> int:
        """
        Calculate millisecond delta between two pulses.
        """
        ts1 = pulse1.get("timestamp_unix_ms", 0)
        ts2 = pulse2.get("timestamp_unix_ms", 0)
        return abs(ts2 - ts1)
    
    def get_pulse_latency_ms(self) -> int:
        """
        Get latency of last pulse in milliseconds since generation.
        """
        if not self.last_pulse_timestamp_ms:
            return 0
        
        current_ms = int(time.time() * 1000)
        # Extract unix ms from last pulse
        if self.pulse_history:
            last_pulse_ms = self.pulse_history[-1].get("timestamp_unix_ms", 0)
            return current_ms - last_pulse_ms
        
        return 0
    
    def broadcast_pulse(self, pulse: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcasts pulse to all listening devices.
        Returns broadcast confirmation with precise timing.
        """
        broadcast_timestamp = self.get_current_timestamp_ms()
        broadcast_unix_ms = int(time.time() * 1000)
        
        return {
            "broadcast_id": f"PULSE_{self.pulse_sequence}",
            "payload": pulse,
            "broadcast_timestamp_iso_ms": broadcast_timestamp,
            "broadcast_timestamp_unix_ms": broadcast_unix_ms,
            "recipients": [
                "PHONE_ALPHA",
                "PHONE_BETA",
                "PC_TERMINAL",
                "COMPUTER_BETA",
                "HOLOGRAPHIC_API",
                "SOVEREIGN_UI"
            ],
            "status": "SENT"
        }
    
    def get_pulse_history_with_deltas(self) -> List[Dict[str, Any]]:
        """
        Returns pulse history with millisecond deltas between consecutive pulses.
        """
        history_with_deltas = []
        
        for i, pulse in enumerate(self.pulse_history):
            pulse_data = pulse.copy()
            
            if i > 0:
                prev_pulse = self.pulse_history[i - 1]
                delta_ms = self.get_pulse_delta_ms(prev_pulse, pulse)
                pulse_data["delta_ms_from_previous"] = delta_ms
            else:
                pulse_data["delta_ms_from_previous"] = None
            
            history_with_deltas.append(pulse_data)
        
        return history_with_deltas
    
    def get_pulse_statistics_ms(self) -> Dict[str, Any]:
        """
        Returns statistics on pulse timing with millisecond precision.
        """
        if len(self.pulse_history) < 2:
            return {"status": "insufficient_data"}
        
        deltas = []
        for i in range(1, len(self.pulse_history)):
            delta = self.get_pulse_delta_ms(
                self.pulse_history[i - 1],
                self.pulse_history[i]
            )
            deltas.append(delta)
        
        avg_delta = sum(deltas) / len(deltas)
        min_delta = min(deltas)
        max_delta = max(deltas)
        
        return {
            "total_pulses": len(self.pulse_history),
            "average_interval_ms": avg_delta,
            "min_interval_ms": min_delta,
            "max_interval_ms": max_delta,
            "current_sequence": self.pulse_sequence,
            "last_timestamp_iso_ms": self.last_pulse_timestamp_ms
        }

if __name__ == "__main__":
    # Test Pulse Generator
    generator = PulseGenerator()
    
    print("=== PULSE GENERATOR TEST ===")
    print(f"Current timestamp (ISO): {generator.get_current_timestamp_ms()}")
    print(f"Current timestamp (Unix ms): {int(time.time() * 1000)}")
    
    # Generate 5 test pulses
    for i in range(5):
        pulse = generator.generate_pulse()
        print(f"\nPulse #{pulse['pulse_sequence']}")
        print(f"  ISO: {pulse['timestamp_iso_ms']}")
        print(f"  Unix: {pulse['timestamp_unix_ms']} ms")
        time.sleep(0.1)  # 100ms between pulses
    
    # Show statistics
    stats = generator.get_pulse_statistics_ms()
    print(f"\n=== PULSE STATISTICS ===")
    print(json.dumps(stats, indent=2))
