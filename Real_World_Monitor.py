"""
REAL-WORLD MONITORING SYSTEM
Actual hardware, network, and infrastructure telemetry.
Not simulation. Real measurements. Real constraints.
"""

import psutil
import socket
import requests
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - [MONITOR] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RealWorldMonitor:
    """Monitors actual system resources and infrastructure."""
    
    def __init__(self):
        self.enabled = True
        self.monitoring_thread = None
        self.last_update = None
        self.current_metrics = {}
        
        # Device tracking
        self.devices = {
            "PHONE_ALPHA": {"status": "UNKNOWN", "last_seen": None, "ip": None},
            "PHONE_BETA": {"status": "UNKNOWN", "last_seen": None, "ip": None},
            "PC_TERMINAL": {"status": "ONLINE", "last_seen": datetime.now().isoformat(), "ip": self._get_local_ip()},
            "COMPUTER_BETA": {"status": "UNKNOWN", "last_seen": None, "ip": None}
        }
        
        # API endpoints to monitor
        self.api_endpoints = [
            {"name": "Global Energy Grid", "url": "wss://energy.global/control", "type": "websocket"},
            {"name": "Federal Housing Database", "url": "https://housing.gov/api/v1", "type": "https"},
            {"name": "Global Supply Chain", "url": "https://logistics.world/api", "type": "https"}
        ]
        
        # Resource usage thresholds
        self.thresholds = {
            "cpu_percent": 80,
            "memory_percent": 85,
            "disk_percent": 90,
            "temp_celsius": 80,
            "network_latency_ms": 100
        }
        
        self.alerts = []
        self.metrics_history = []
        self.max_history = 10000
    
    def _get_local_ip(self) -> str:
        """Get this machine's local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    # ========== HARDWARE MONITORING ==========
    
    def get_cpu_metrics(self) -> Dict[str, Any]:
        """Get real CPU metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        
        # CPU per core
        per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        
        return {
            "cpu_percent": cpu_percent,
            "cpu_count_logical": cpu_count_logical,
            "cpu_count_physical": cpu_count_physical,
            "per_core": per_core,
            "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "alert": cpu_percent > self.thresholds["cpu_percent"]
        }
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """Get real memory metrics."""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "total_gb": memory.total / (1024**3),
            "available_gb": memory.available / (1024**3),
            "used_gb": memory.used / (1024**3),
            "percent": memory.percent,
            "swap_total_gb": swap.total / (1024**3),
            "swap_used_gb": swap.used / (1024**3),
            "alert": memory.percent > self.thresholds["memory_percent"]
        }
    
    def get_disk_metrics(self) -> Dict[str, Any]:
        """Get real disk metrics."""
        try:
            disk = psutil.disk_usage('/')
            io = psutil.disk_io_counters()
            
            return {
                "total_gb": disk.total / (1024**3),
                "used_gb": disk.used / (1024**3),
                "free_gb": disk.free / (1024**3),
                "percent": disk.percent,
                "read_mb": io.read_bytes / (1024**2),
                "write_mb": io.write_bytes / (1024**2),
                "alert": disk.percent > self.thresholds["disk_percent"]
            }
        except:
            return {"error": "Disk monitoring unavailable"}
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Get real network metrics."""
        try:
            net = psutil.net_io_counters()
            
            # Test connectivity
            latency_ms = self._measure_latency("8.8.8.8")
            
            return {
                "bytes_sent_mb": net.bytes_sent / (1024**2),
                "bytes_recv_mb": net.bytes_recv / (1024**2),
                "packets_sent": net.packets_sent,
                "packets_recv": net.packets_recv,
                "errors_in": net.errin,
                "errors_out": net.errout,
                "dropped_in": net.dropin,
                "dropped_out": net.dropout,
                "latency_ms": latency_ms,
                "internet_connected": latency_ms is not None and latency_ms < 1000,
                "alert": latency_ms and latency_ms > self.thresholds["network_latency_ms"]
            }
        except:
            return {"error": "Network monitoring unavailable"}
    
    def _measure_latency(self, host: str, timeout: int = 2) -> Optional[float]:
        """Measure network latency to a host."""
        try:
            start = time.time()
            socket.create_connection((host, 80), timeout=timeout)
            return round((time.time() - start) * 1000, 2)
        except:
            return None
    
    def get_process_metrics(self) -> Dict[str, Any]:
        """Get running process metrics."""
        try:
            process_count = len(psutil.pids())
            
            # Top processes by CPU
            top_cpu = sorted(
                [(p.info['name'], p.info['cpu_percent']) 
                 for p in psutil.process_iter(['name', 'cpu_percent'])
                 if p.info['cpu_percent'] and p.info['cpu_percent'] > 0],
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Top processes by memory
            top_memory = sorted(
                [(p.info['name'], p.info['memory_percent']) 
                 for p in psutil.process_iter(['name', 'memory_percent'])
                 if p.info['memory_percent'] and p.info['memory_percent'] > 0.1],
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            return {
                "total_processes": process_count,
                "top_cpu": dict(top_cpu),
                "top_memory": dict(top_memory)
            }
        except:
            return {"error": "Process monitoring unavailable"}
    
    # ========== DEVICE MONITORING ==========
    
    def check_device_status(self, device_id: str) -> Dict[str, Any]:
        """Check if a device is online and responsive."""
        if device_id not in self.devices:
            return {"error": f"Device {device_id} not registered"}
        
        device = self.devices[device_id]
        
        # For local PC, always online
        if device_id == "PC_TERMINAL":
            device["status"] = "ONLINE"
            device["last_seen"] = datetime.now().isoformat()
            return {
                "device_id": device_id,
                "status": "ONLINE",
                "last_seen": device["last_seen"],
                "local": True
            }
        
        # For remote devices, try ping/HTTP probe
        if device.get("ip"):
            latency = self._measure_latency(device["ip"])
            if latency is not None:
                device["status"] = "ONLINE"
                device["last_seen"] = datetime.now().isoformat()
                return {
                    "device_id": device_id,
                    "status": "ONLINE",
                    "ip": device["ip"],
                    "latency_ms": latency,
                    "last_seen": device["last_seen"]
                }
        
        # Device unreachable
        return {
            "device_id": device_id,
            "status": "OFFLINE",
            "last_seen": device["last_seen"]
        }
    
    def get_all_device_status(self) -> Dict[str, Any]:
        """Get status of all devices in Master Override Matrix."""
        return {
            device_id: self.check_device_status(device_id)
            for device_id in self.devices.keys()
        }
    
    # ========== API MONITORING ==========
    
    def check_api_endpoint(self, endpoint: Dict[str, str]) -> Dict[str, Any]:
        """Check if an API endpoint is reachable and responsive."""
        name = endpoint["name"]
        url = endpoint["url"]
        endpoint_type = endpoint["type"]
        
        check_result = {
            "name": name,
            "url": url,
            "timestamp_iso_ms": datetime.now().isoformat(timespec='milliseconds'),
            "status": "UNKNOWN",
            "response_time_ms": None
        }
        
        try:
            # WebSocket endpoint
            if endpoint_type == "websocket":
                # Simple connectivity check for WebSocket
                # In production, would establish actual WebSocket
                url_http = url.replace("wss://", "https://").replace("ws://", "http://")
                start = time.time()
                response = requests.head(url_http, timeout=5)
                response_time = (time.time() - start) * 1000
                check_result["status"] = "REACHABLE" if response.status_code < 500 else "ERROR"
                check_result["response_time_ms"] = round(response_time, 2)
            
            # HTTPS endpoint
            elif endpoint_type == "https":
                start = time.time()
                response = requests.get(url, timeout=5)
                response_time = (time.time() - start) * 1000
                check_result["status"] = "REACHABLE" if response.status_code < 500 else "ERROR"
                check_result["response_code"] = response.status_code
                check_result["response_time_ms"] = round(response_time, 2)
        
        except requests.Timeout:
            check_result["status"] = "TIMEOUT"
            check_result["error"] = "Request timeout (5 seconds)"
        except requests.ConnectionError:
            check_result["status"] = "UNREACHABLE"
            check_result["error"] = "Connection error"
        except Exception as e:
            check_result["status"] = "ERROR"
            check_result["error"] = str(e)
        
        return check_result
    
    def check_all_endpoints(self) -> List[Dict[str, Any]]:
        """Check all monitored API endpoints."""
        return [self.check_api_endpoint(ep) for ep in self.api_endpoints]
    
    # ========== RESOURCE CONSTRAINTS ==========
    
    def get_resource_constraints(self) -> Dict[str, Any]:
        """Report actual system resource constraints."""
        cpu = self.get_cpu_metrics()
        memory = self.get_memory_metrics()
        disk = self.get_disk_metrics()
        network = self.get_network_metrics()
        
        constraints = {
            "timestamp_iso_ms": datetime.now().isoformat(timespec='milliseconds'),
            "can_operate": True,
            "warnings": [],
            "critical_alerts": [],
            "resources": {
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
                "network": network
            }
        }
        
        # Check for constraint violations
        if cpu.get("alert"):
            constraints["warnings"].append(f"CPU high: {cpu['cpu_percent']}%")
        
        if memory.get("alert"):
            constraints["warnings"].append(f"Memory high: {memory['percent']}%")
        
        if disk.get("alert"):
            constraints["critical_alerts"].append(f"Disk nearly full: {disk['percent']}%")
            constraints["can_operate"] = False
        
        if network.get("alert"):
            constraints["warnings"].append(f"Network latency high: {network['latency_ms']}ms")
        
        if not network.get("internet_connected"):
            constraints["warnings"].append("Internet connectivity degraded")
        
        return constraints
    
    # ========== CONTINUOUS MONITORING ==========
    
    def get_full_system_status(self) -> Dict[str, Any]:
        """Get complete real-world system status."""
        timestamp_iso_ms = datetime.now().isoformat(timespec='milliseconds')
        timestamp_unix_ms = int(time.time() * 1000)
        
        status = {
            "timestamp_iso_ms": timestamp_iso_ms,
            "timestamp_unix_ms": timestamp_unix_ms,
            "system_operational": True,
            "hardware": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "disk": self.get_disk_metrics(),
            "network": self.get_network_metrics(),
            "processes": self.get_process_metrics(),
            "devices": self.get_all_device_status(),
            "api_endpoints": self.check_all_endpoints(),
            "constraints": self.get_resource_constraints(),
            "alerts": self.alerts[-10:]  # Last 10 alerts
        }
        
        # Store in history
        self.metrics_history.append(status)
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history:]
        
        self.last_update = timestamp_iso_ms
        self.current_metrics = status
        
        return status
    
    def start_continuous_monitoring(self, interval_seconds: int = 30):
        """Start continuous monitoring in background thread."""
        def monitor_loop():
            while self.enabled:
                try:
                    status = self.get_full_system_status()
                    
                    # Check for critical alerts
                    if status["constraints"]["critical_alerts"]:
                        logging.critical(f"CRITICAL: {status['constraints']['critical_alerts']}")
                    
                    if status["constraints"]["warnings"]:
                        logging.warning(f"WARNINGS: {status['constraints']['warnings']}")
                    
                    # Check API endpoints
                    for ep in status["api_endpoints"]:
                        if ep["status"] != "REACHABLE":
                            logging.warning(f"API ISSUE: {ep['name']} - {ep['status']}")
                    
                    # Check devices
                    for dev_id, dev_status in status["devices"].items():
                        if dev_status.get("status") == "OFFLINE":
                            logging.warning(f"DEVICE OFFLINE: {dev_id}")
                    
                    time.sleep(interval_seconds)
                
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                    time.sleep(interval_seconds)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        logging.info(f"Real-world monitoring started (interval: {interval_seconds}s)")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.enabled = False
        logging.info("Real-world monitoring stopped")
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get historical metrics."""
        return self.metrics_history[-limit:]


if __name__ == "__main__":
    # Test real-world monitoring
    print("=" * 80)
    print("REAL-WORLD MONITORING SYSTEM - TEST")
    print("=" * 80)
    
    monitor = RealWorldMonitor()
    
    print("\n=== CURRENT SYSTEM STATUS ===")
    status = monitor.get_full_system_status()
    
    print(f"\n[CPU]")
    print(f"  Usage: {status['hardware']['cpu_percent']}%")
    print(f"  Cores: {status['hardware']['cpu_count_physical']} physical, {status['hardware']['cpu_count_logical']} logical")
    
    print(f"\n[MEMORY]")
    print(f"  Usage: {status['memory']['percent']}% ({status['memory']['used_gb']:.1f}GB / {status['memory']['total_gb']:.1f}GB)")
    
    print(f"\n[DISK]")
    print(f"  Usage: {status['disk']['percent']}% ({status['disk']['used_gb']:.1f}GB / {status['disk']['total_gb']:.1f}GB)")
    
    print(f"\n[NETWORK]")
    print(f"  Internet: {'CONNECTED' if status['network'].get('internet_connected') else 'DISCONNECTED'}")
    if status['network'].get('latency_ms'):
        print(f"  Latency: {status['network']['latency_ms']}ms")
    
    print(f"\n[DEVICES]")
    for dev_id, dev_status in status['devices'].items():
        print(f"  {dev_id}: {dev_status['status']}")
    
    print(f"\n[API ENDPOINTS]")
    for ep in status['api_endpoints']:
        print(f"  {ep['name']}: {ep['status']}")
        if ep.get('response_time_ms'):
            print(f"    Response time: {ep['response_time_ms']}ms")
    
    print(f"\n[CONSTRAINTS]")
    print(f"  Can Operate: {status['constraints']['can_operate']}")
    if status['constraints']['warnings']:
        print(f"  Warnings: {status['constraints']['warnings']}")
    if status['constraints']['critical_alerts']:
        print(f"  CRITICAL: {status['constraints']['critical_alerts']}")
    
    print("\n=== Starting continuous monitoring (10 seconds) ===")
    monitor.start_continuous_monitoring(interval_seconds=3)
    time.sleep(10)
    monitor.stop_monitoring()
    
    print("\n=== Test Complete ===")
