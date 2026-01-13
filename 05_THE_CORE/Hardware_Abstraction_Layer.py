import uuid
import platform
import json
import os
import socket
import requests

class HardwareAbstractionLayer:
    """
    HAL: The Physical Bridge.
    Identifies the specific hardware node Sarah is inhabiting.
    Enables Multi-Device Switching and State Persistence.
    """
    
    def __init__(self, monitor=None):
        self.monitor = monitor
        self.node_id = self._generate_node_id()
        self.hostname = platform.node()
        self.os_info = f"{platform.system()} {platform.release()}"
        self.ip_address = self._get_ip_address()
        
        # Log the realization
        if self.monitor:
            self.monitor.capture("HAL", "NODE_IDENTIFIED", {
                "node_id": self.node_id,
                "hostname": self.hostname,
                "os": self.os_info
            })

    def _generate_node_id(self):
        """
        Generates a unique, persistent fingerprint for this device.
        Format: SDNA-[HOSTNAME]-[MAC_ADDRESS_HASH]
        """
        mac = uuid.getnode()
        return f"SDNA-{platform.node()}-{mac}"

    def _get_ip_address(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "UNKNOWN"

    def get_device_fingerprint(self):
        return {
            "node_id": self.node_id,
            "hostname": self.hostname,
            "os": self.os_info,
            "ip": self.ip_address,
            "status": "ACTIVE_SOVEREIGN_NODE"
        }

    def get_performance_profile(self):
        """
        Analyzes hardware capabilities for optimization tuning.
        Specifically tuned for Lenovo LOQ / High-Performance Nodes.
        """
        import psutil
        
        cpu_count = psutil.cpu_count(logical=True)
        memory = psutil.virtual_memory()
        
        # Check for GPU (NVIDIA/CUDA)
        gpu_available = False
        try:
            import subprocess
            nvidia_smi = subprocess.check_output(["nvidia-smi", "-L"])
            gpu_available = True
        except:
            gpu_available = False
            
        return {
            "cpu_cores": cpu_count,
            "total_memory_gb": round(memory.total / (1024**3), 2),
            "gpu_acceleration": gpu_available,
            "optimization_target": "VOLUMETRIC_C3_MAX" if gpu_available else "BALANCED_2D"
        }

    def sync_state(self, state_data):
        """
        Prepares the current state for hand-off to another device.
        """
        package = {
            "source_node": self.node_id,
            "timestamp": os.times(),
            "state_payload": state_data,
            "protocol": "MULTI_DEVICE_SWITCH"
        }
        # In a full implementation, this would push to Firebase/Cloud
        return package
