import wmi
import os
import sys
import subprocess
import ctypes
import json
from datetime import datetime

class SystemAdminCore:
    """
    The Hand of the Sovereign.
    Provides deep integration with Windows Management Instrumentation (WMI)
    to monitor, control, and update hardware and system processes.
    REQUIRES: Administrator Privileges.
    """
    def __init__(self, monitor=None):
        self.monitor = monitor
        self.wmi = wmi.WMI()
        self.is_admin = self._check_admin()
        
        if not self.is_admin:
            print("[ADMIN CORE]: WARNING -> Insufficient Privileges. Read-Only Mode.")
            if self.monitor:
                self.monitor.capture("ADMIN", "PRIVILEGE_CHECK", {"status": "FAILED", "message": "Run as Admin required"})

    def _check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_hardware_telemetry(self):
        """
        Scans all critical hardware components.
        """
        telemetry = {}
        
        # CPU
        for cpu in self.wmi.Win32_Processor():
            telemetry['cpu'] = {
                'name': cpu.Name,
                'load': cpu.LoadPercentage,
                'cores': cpu.NumberOfCores
            }
            
        # RAM
        for mem in self.wmi.Win32_OperatingSystem():
            total = int(mem.TotalVisibleMemorySize) / 1024
            free = int(mem.FreePhysicalMemory) / 1024
            telemetry['ram'] = {
                'total_mb': round(total, 2),
                'free_mb': round(free, 2),
                'usage_percent': round(((total - free) / total) * 100, 2)
            }
            
        # GPU (If available via CIM)
        try:
            gpus = []
            for gpu in self.wmi.Win32_VideoController():
                gpus.append({'name': gpu.Name, 'status': gpu.Status})
            telemetry['gpu'] = gpus
        except:
            telemetry['gpu'] = "Not Detected"

        if self.monitor:
            self.monitor.capture("ADMIN", "HARDWARE_SCAN", telemetry)
            
        return telemetry

    def list_processes(self):
        """
        Returns a list of running processes.
        """
        procs = []
        for process in self.wmi.Win32_Process():
            procs.append({
                'id': process.ProcessId,
                'name': process.Name,
                'memory': process.WorkingSetSize
            })
        return procs

    def kill_process(self, process_name):
        """
        Terminates a process by name.
        """
        if not self.is_admin:
            return False, "PERMISSION_DENIED"
            
        count = 0
        for process in self.wmi.Win32_Process(Name=process_name):
            try:
                process.Terminate()
                count += 1
            except:
                pass
        
        if self.monitor:
            self.monitor.capture("ADMIN", "KILL_PROCESS", {"target": process_name, "count": count})
            
        return True, f"Terminated {count} instances of {process_name}"

    def check_system_updates(self):
        """
        Checks for Windows Updates via PowerShell.
        """
        if not self.is_admin:
            return "PERMISSION_DENIED"
            
        print("[ADMIN CORE]: Scanning for Windows Updates...")
        # Uses the PSWindowsUpdate module logic or standard USOClient
        try:
            # Simple check command
            cmd = "usoclient StartScan"
            subprocess.run(cmd, shell=True)
            return "Update Scan Initiated (Background)"
        except Exception as e:
            return f"Update Check Failed: {e}"

    def scan_new_hardware(self):
        """
        Forces a Plug and Play device scan.
        """
        if not self.is_admin:
            return "PERMISSION_DENIED"
            
        subprocess.run("pnputil /scan-devices", shell=True)
        return "Hardware Scan Complete"
