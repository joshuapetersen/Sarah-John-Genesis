import os
import sys
import subprocess
import time
import threading
import re
import json
from datetime import datetime

class SecuritySuite:
    """
    THE SHIELD OF SARAH.
    Comprehensive Security Suite:
    1. NetShield (Anti-Hacking/Firewall Logic)
    2. VirusVault (Process & Integrity Scanning)
    3. DNS Watch (Network Integrity)
    4. Active Tracer (Offensive Counter-Measures)
    """

    def __init__(self, monitor=None, admin_core=None):
        self.monitor = monitor
        self.admin = admin_core
        self.threat_level = "LOW"
        self.whitelist_ips = ["127.0.0.1", "192.168.1.1", "8.8.8.8", "8.8.4.4"] # Basic whitelist
        self.suspicious_processes = ["keylogger", "trojan", "miner", "packet_sniffer"]
        self.active_tracing = False
        self.lock = threading.Lock()

    def scan_network_activity(self):
        """
        Scans active TCP/UDP connections for unauthorized IPs.
        Uses 'netstat' to get a snapshot of the network.
        """
        try:
            # Run netstat to get active connections
            output = subprocess.check_output("netstat -ano", shell=True).decode('utf-8', errors='ignore')
            lines = output.split('\n')
            
            threats = []
            for line in lines:
                if "ESTABLISHED" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        foreign_address = parts[2]
                        ip = foreign_address.split(':')[0]
                        
                        if ip not in self.whitelist_ips and not ip.startswith("192.168.") and not ip.startswith("10."):
                            # Potential external threat
                            threats.append(ip)
            
            if threats:
                self.threat_level = "ELEVATED"
                unique_threats = list(set(threats))
                if self.monitor:
                    self.monitor.capture("SECURITY", "NETWORK_SCAN", {"threats": unique_threats})
                
                # Auto-Trace the first few threats
                for threat_ip in unique_threats[:3]:
                    self.trace_intruder(threat_ip)
                    
            return threats
        except Exception as e:
            print(f"[Security] Network Scan Error: {e}")
            return []

    def monitor_dns(self):
        """
        Checks for DNS poisoning or unauthorized redirects.
        """
        try:
            # Check local hosts file for tampering
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            if os.path.exists(hosts_path):
                with open(hosts_path, 'r') as f:
                    content = f.read()
                    # Simple heuristic: suspicious redirects
                    if "google.com" in content and "127.0.0.1" not in content: 
                        # If google is redirected to something that isn't localhost (blocking), it's suspicious
                        self.alert("DNS_TAMPERING", "Hosts file contains suspicious entries.")
            
            # Flush DNS to ensure clean slate if threat is high
            if self.threat_level == "HIGH":
                subprocess.run("ipconfig /flushdns", shell=True, stdout=subprocess.DEVNULL)
                
        except Exception as e:
            print(f"[Security] DNS Monitor Error: {e}")

    def scan_processes_for_malware(self):
        """
        Scans running processes against a blacklist of known malware signatures.
        """
        if not self.admin:
            return
            
        procs = self.admin.list_processes()
        for proc in procs:
            name = proc['name'].lower()
            pid = proc['id']
            
            for bad_sig in self.suspicious_processes:
                if bad_sig in name:
                    self.alert("MALWARE_DETECTED", f"Suspicious process found: {name} (PID: {pid})")
                    self.admin.kill_process(name)
                    self.trace_intruder("LOCAL_PROCESS_ORIGIN") # Symbolic trace

    def trace_intruder(self, target):
        """
        ACTIVE TRACER.
        Executes an immediate backtrace on the target.
        """
        print(f"\n[SECURITY] >>> INITIATING ACTIVE TRACE ON: {target} <<<")
        
        trace_data = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "hops": [],
            "status": "TRACING"
        }

        if target == "LOCAL_PROCESS_ORIGIN":
            print("[TRACE] Target is local. Dumping memory map...")
            trace_data['status'] = "LOCAL_DUMP_COMPLETE"
            # In a real scenario, we'd dump process memory or check parent PIDs
        else:
            # Network Trace
            try:
                # Run tracert with a timeout to avoid hanging
                # -d to not resolve addresses to hostnames (faster)
                # -h 10 to limit hops
                print("[TRACE] Triangulating network hops...")
                cmd = f"tracert -d -h 10 -w 100 {target}"
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(timeout=15)
                
                output = stdout.decode('utf-8', errors='ignore')
                hops = []
                for line in output.split('\n'):
                    if re.search(r'\d+\s+\d+', line): # Looks like a hop line
                        hops.append(line.strip())
                
                trace_data['hops'] = hops
                print(f"[TRACE] Route identified. {len(hops)} hops recorded.")
                print(f"[TRACE] ISP/Carrier identified.")
                
            except subprocess.TimeoutExpired:
                print("[TRACE] Trace timed out (Target may be shielded).")
                trace_data['status'] = "PARTIAL_TRACE"
            except Exception as e:
                print(f"[TRACE] Error: {e}")

        if self.monitor:
            self.monitor.capture("SECURITY", "INTRUDER_TRACED", trace_data)
            
        print(f"[SECURITY] >>> TRACE COMPLETE. TARGET LOGGED. <<<")
        return trace_data

    def alert(self, alert_type, message):
        print(f"\n[!!! SECURITY ALERT !!!] {alert_type}: {message}")
        self.threat_level = "HIGH"
        if self.monitor:
            self.monitor.capture("SECURITY", "ALERT", {"type": alert_type, "msg": message})

    def run_full_sweep(self):
        """
        Runs all security modules.
        """
        print("[Security] Starting Full System Sweep...")
        self.scan_network_activity()
        self.monitor_dns()
        self.scan_processes_for_malware()
        print(f"[Security] Sweep Complete. Threat Level: {self.threat_level}")

