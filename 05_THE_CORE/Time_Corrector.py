"""
TIME CORRECTOR MODULE
Detects and automatically corrects system time drift.
Integrates with Millisecond_Timing and audit logging.
"""

import logging
import platform
import socket
import struct
import subprocess
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple

from Millisecond_Timing import MillisecondTimer


class TimeCorrector:
    """Detects and corrects system time drift using multiple NTP sources."""
    
    NTP_SERVERS = [
        "time.windows.com",
        "time.nist.gov",
        "pool.ntp.org",
        "time.google.com",
    ]
    
    NTP_PORT = 123
    NTP_PACKET_FORMAT = "!12I"
    NTP_DELTA = 2208988800  # Seconds between 1900 and 1970
    
    @staticmethod
    def query_ntp_server(server: str, timeout: float = 2.0) -> Optional[float]:
        """
        Query an NTP server and return the Unix timestamp.
        Returns None if the query fails.
        """
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(timeout)
            
            # NTP request packet (mode 3, version 3)
            data = b'\x1b' + 47 * b'\0'
            client.sendto(data, (server, TimeCorrector.NTP_PORT))
            
            response, _ = client.recvfrom(1024)
            client.close()
            
            if len(response) >= 48:
                # Extract transmit timestamp (bytes 40-47)
                unpacked = struct.unpack(TimeCorrector.NTP_PACKET_FORMAT, response[:48])
                ntp_time = unpacked[10] + float(unpacked[11]) / 2**32
                return ntp_time - TimeCorrector.NTP_DELTA
            
            return None
        except Exception as exc:
            logging.warning(f"NTP query to {server} failed: {exc}")
            return None
    
    @staticmethod
    def get_consensus_ntp_time() -> Optional[Tuple[float, List[str]]]:
        """
        Query multiple NTP servers and return consensus time.
        Returns (unix_timestamp, list_of_responding_servers) or None.
        """
        results = []
        responding = []
        
        for server in TimeCorrector.NTP_SERVERS:
            ntp_time = TimeCorrector.query_ntp_server(server)
            if ntp_time:
                results.append(ntp_time)
                responding.append(server)
        
        if not results:
            return None
        
        # Use median to avoid outliers
        results.sort()
        median = results[len(results) // 2]
        return median, responding
    
    @staticmethod
    def check_drift(drift_threshold_ms: int = 250) -> Dict[str, Any]:
        """
        Check current system time drift against NTP consensus.
        Returns drift report with magnitude and recommendation.
        """
        system_time = time.time()
        ntp_result = TimeCorrector.get_consensus_ntp_time()
        
        if not ntp_result:
            return {
                "drift_detected": False,
                "error": "Could not reach NTP servers",
                "system_unix": system_time,
                "ntp_unix": None,
                "drift_ms": None,
            }
        
        ntp_time, responding_servers = ntp_result
        drift_seconds = system_time - ntp_time
        drift_ms = int(drift_seconds * 1000)
        drift_exceeds = abs(drift_ms) > drift_threshold_ms
        
        return {
            "drift_detected": drift_exceeds,
            "system_unix": system_time,
            "ntp_unix": ntp_time,
            "drift_ms": drift_ms,
            "drift_threshold_ms": drift_threshold_ms,
            "responding_servers": responding_servers,
            "correction_needed": drift_exceeds,
            "timestamp": MillisecondTimer.get_iso_ms(),
        }
    
    @staticmethod
    def attempt_windows_time_sync() -> Dict[str, Any]:
        """
        Attempt to sync time using Windows w32tm.
        Returns status report.
        """
        if platform.system() != "Windows":
            return {"success": False, "method": "w32tm", "error": "Not Windows"}
        
        try:
            # Try resync
            result = subprocess.run(
                ["w32tm", "/resync", "/rediscover"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "method": "w32tm",
                    "output": result.stdout.strip(),
                }
            else:
                return {
                    "success": False,
                    "method": "w32tm",
                    "error": result.stderr.strip() or result.stdout.strip(),
                }
        except subprocess.TimeoutExpired:
            return {"success": False, "method": "w32tm", "error": "Timeout"}
        except Exception as exc:
            return {"success": False, "method": "w32tm", "error": str(exc)}
    
    @staticmethod
    def correct_drift_auto(drift_threshold_ms: int = 250) -> Dict[str, Any]:
        """
        Automatically detect and correct time drift.
        Returns correction report with actions taken.
        """
        drift_report = TimeCorrector.check_drift(drift_threshold_ms)
        
        if not drift_report.get("correction_needed"):
            return {
                **drift_report,
                "correction_attempted": False,
                "correction_success": False,
                "message": "No correction needed",
            }
        
        logging.warning(f"Time drift detected: {drift_report['drift_ms']}ms. Attempting correction...")
        
        # Try Windows Time sync first
        sync_result = TimeCorrector.attempt_windows_time_sync()
        
        if sync_result["success"]:
            # Verify correction
            time.sleep(1)
            verify_report = TimeCorrector.check_drift(drift_threshold_ms)
            return {
                **verify_report,
                "correction_attempted": True,
                "correction_method": "w32tm",
                "correction_success": not verify_report.get("correction_needed"),
                "sync_output": sync_result.get("output"),
            }
        
        # If w32tm failed, log it and return status
        logging.warning(f"w32tm sync failed: {sync_result.get('error')}")
        return {
            **drift_report,
            "correction_attempted": True,
            "correction_method": "w32tm",
            "correction_success": False,
            "sync_error": sync_result.get("error"),
            "message": "Correction failed. Manual intervention needed or run as admin.",
        }
    
    @staticmethod
    def periodic_check_and_correct(
        interval_seconds: int = 300,
        drift_threshold_ms: int = 250,
        callback: Optional[callable] = None,
    ):
        """
        Periodically check and correct time drift.
        Runs in foreground; use threading for background operation.
        """
        logging.info(f"Starting periodic time correction (every {interval_seconds}s, threshold {drift_threshold_ms}ms)")
        
        while True:
            try:
                report = TimeCorrector.correct_drift_auto(drift_threshold_ms)
                
                if callback:
                    callback(report)
                
                if report.get("correction_attempted"):
                    logging.info(f"Time correction: {report.get('message', 'completed')}")
                
            except Exception as exc:
                logging.error(f"Time correction error: {exc}")
            
            time.sleep(interval_seconds)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [TIME_CORRECTOR] - %(message)s',
    )
    
    print("=== TIME DRIFT CHECK ===\n")
    
    drift = TimeCorrector.check_drift(drift_threshold_ms=250)
    print(f"System Time: {datetime.fromtimestamp(drift['system_unix']).isoformat()}")
    if drift['ntp_unix']:
        print(f"NTP Time:    {datetime.fromtimestamp(drift['ntp_unix']).isoformat()}")
        print(f"Drift:       {drift['drift_ms']}ms")
        print(f"Threshold:   {drift['drift_threshold_ms']}ms")
        print(f"Servers:     {', '.join(drift['responding_servers'])}")
        print(f"Action:      {'CORRECTION NEEDED' if drift['correction_needed'] else 'OK'}")
    else:
        print(f"Error: {drift.get('error')}")
    
    if drift.get("correction_needed"):
        print("\n=== ATTEMPTING CORRECTION ===\n")
        result = TimeCorrector.correct_drift_auto(drift_threshold_ms=250)
        print(f"Method:      {result.get('correction_method', 'N/A')}")
        print(f"Success:     {result.get('correction_success', False)}")
        if result.get("sync_output"):
            print(f"Output:      {result['sync_output']}")
        if result.get("sync_error"):
            print(f"Error:       {result['sync_error']}")
        print(f"Message:     {result.get('message', 'N/A')}")
