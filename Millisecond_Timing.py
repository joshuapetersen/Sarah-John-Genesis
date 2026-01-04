"""
MILLISECOND TIMING MODULE
Provides high-precision timing utilities across all systems.
All timestamps calculated to millisecond precision.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional, List

class MillisecondTimer:
    """High-precision timer for system operations."""
    
    @staticmethod
    def get_iso_ms() -> str:
        """ISO 8601 timestamp with milliseconds. Example: 2026-01-02T23:15:47.341Z"""
        return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    
    @staticmethod
    def get_unix_ms() -> int:
        """Unix timestamp in milliseconds. Example: 1735862147341"""
        return int(time.time() * 1000)
    
    @staticmethod
    def get_local_iso_ms() -> str:
        """Local ISO 8601 timestamp with milliseconds."""
        return datetime.now().isoformat(timespec='milliseconds')
    
    @staticmethod
    def get_dual_timestamp() -> Dict[str, Any]:
        """Returns both ISO and Unix millisecond timestamps."""
        return {
            "iso_ms": MillisecondTimer.get_iso_ms(),
            "unix_ms": MillisecondTimer.get_unix_ms(),
            "local_iso_ms": MillisecondTimer.get_local_iso_ms()
        }

    @staticmethod
    def get_redundant_time_sources() -> Dict[str, Any]:
        """
        Collects multiple time readings to detect drift.
        Intended for redundancy checks across:
        - System clock (local)
        - UTC (from timezone-aware datetime)
        - Monotonic clock (drift-safe since boot)
        - perf_counter (high-res)
        Note: Monotonic/perf_counter are relative, used for consistency checks only.
        """
        monotonic_ms = int(time.monotonic() * 1000)
        perf_ms = int(time.perf_counter() * 1000)
        return {
            "system_iso_ms": MillisecondTimer.get_iso_ms(),
            "system_unix_ms": MillisecondTimer.get_unix_ms(),
            "local_iso_ms": MillisecondTimer.get_local_iso_ms(),
            "monotonic_ms": monotonic_ms,
            "perf_counter_ms": perf_ms,
            "captured_at": MillisecondTimer.get_iso_ms()
        }

    @staticmethod
    def check_time_redundancy(drift_threshold_ms: int = 250) -> Dict[str, Any]:
        """
        Performs a redundancy check across multiple time sources and reports drift.
        - Compares system clock vs monotonic/perf_counter deltas captured near-simultaneously
        - Flags if drift exceeds drift_threshold_ms
        """
        snapshot1 = MillisecondTimer.get_redundant_time_sources()
        time.sleep(0.01)  # 10ms gap to compare deltas
        snapshot2 = MillisecondTimer.get_redundant_time_sources()

        delta_system = snapshot2["system_unix_ms"] - snapshot1["system_unix_ms"]
        delta_mono = snapshot2["monotonic_ms"] - snapshot1["monotonic_ms"]
        delta_perf = snapshot2["perf_counter_ms"] - snapshot1["perf_counter_ms"]

        drift_report = {
            "snapshot_1": snapshot1,
            "snapshot_2": snapshot2,
            "delta_system_ms": delta_system,
            "delta_monotonic_ms": delta_mono,
            "delta_perf_ms": delta_perf,
            "system_vs_monotonic_drift_ms": abs(delta_system - delta_mono),
            "system_vs_perf_drift_ms": abs(delta_system - delta_perf),
            "drift_threshold_ms": drift_threshold_ms,
            "drift_ok": abs(delta_system - delta_mono) <= drift_threshold_ms and abs(delta_system - delta_perf) <= drift_threshold_ms
        }

        return drift_report

    @staticmethod
    def sovereign_time_reality_check(
        device_id: str,
        allowed_devices: Optional[List[str]] = None,
        drift_threshold_ms: int = 250
    ) -> Dict[str, Any]:
        """
        Applies a sovereign device check and time redundancy validation together.
        - Verifies the requesting device is in the Master Override set (or provided allowed list)
        - Runs time redundancy drift detection
        - Returns a consolidated answer for "device is sovereign AND time is sane"
        """
        allowed = allowed_devices or ["PHONE_ALPHA", "PHONE_BETA", "PC_TERMINAL", "COMPUTER_BETA", "USB_ROOT"]
        device_allowed = device_id in allowed
        drift_report = MillisecondTimer.check_time_redundancy(drift_threshold_ms=drift_threshold_ms)

        return {
            "device_id": device_id,
            "device_allowed": device_allowed,
            "drift_report": drift_report,
            "sovereign_and_time_ok": device_allowed and drift_report.get("drift_ok", False)
        }
    
    @staticmethod
    def measure_operation_ms(func, *args, **kwargs) -> Tuple[Any, int]:
        """
        Measures execution time of a function in milliseconds.
        Returns: (result, elapsed_ms)
        """
        start_ms = time.time() * 1000
        result = func(*args, **kwargs)
        end_ms = time.time() * 1000
        elapsed = int(end_ms - start_ms)
        return result, elapsed
    
    @staticmethod
    def format_delta_ms(delta_ms: int) -> str:
        """
        Formats millisecond delta as human-readable string.
        Example: 1234 -> "1.234 seconds"
        """
        if delta_ms < 1000:
            return f"{delta_ms}ms"
        elif delta_ms < 60000:
            seconds = delta_ms / 1000
            return f"{seconds:.3f}s"
        else:
            minutes = delta_ms / 60000
            return f"{minutes:.2f}m"
    
    @staticmethod
    def elapsed_since_ms(start_unix_ms: int) -> int:
        """Calculate milliseconds elapsed since start timestamp."""
        return MillisecondTimer.get_unix_ms() - start_unix_ms
    
    @staticmethod
    def sleep_ms(milliseconds: int) -> None:
        """Sleep for exact milliseconds."""
        time.sleep(milliseconds / 1000.0)

    @staticmethod
    def reconcile_predictive_time(predictive_unix_ms: int, buffer_ms: int = 500) -> Dict[str, Any]:
        """
        Enforces that predictive time cannot override actual time outside a safety buffer.
        - predictive_unix_ms: predicted Unix timestamp in milliseconds
        - buffer_ms: allowable deviation window (default 500ms)
        Returns a reconciliation report with the authoritative time.
        """
        actual_ms = MillisecondTimer.get_unix_ms()
        delta_ms = predictive_unix_ms - actual_ms

        predictive_within_buffer = abs(delta_ms) <= buffer_ms
        authoritative_ms = actual_ms if not predictive_within_buffer else predictive_unix_ms

        return {
            "actual_unix_ms": actual_ms,
            "predictive_unix_ms": predictive_unix_ms,
            "delta_ms": delta_ms,
            "buffer_ms": buffer_ms,
            "predictive_within_buffer": predictive_within_buffer,
            "authoritative_unix_ms": authoritative_ms,
            "authoritative_source": "predictive" if predictive_within_buffer else "actual"
        }


class CommandLogger:
    """Logs commands with precise millisecond timing."""
    
    def __init__(self):
        self.commands = []
    
    def log_command_ms(self, 
                       command: str, 
                       origin: str, 
                       status: str = "RECEIVED") -> Dict[str, Any]:
        """
        Log a command with millisecond precision.
        """
        log_entry = {
            "timestamp_iso_ms": MillisecondTimer.get_iso_ms(),
            "timestamp_unix_ms": MillisecondTimer.get_unix_ms(),
            "command": command,
            "origin": origin,
            "status": status
        }
        self.commands.append(log_entry)
        return log_entry
    
    def log_command_execution_ms(self,
                                 command: str,
                                 origin: str,
                                 start_unix_ms: int,
                                 result: str = "SUCCESS") -> Dict[str, Any]:
        """
        Log command execution with elapsed time in milliseconds.
        """
        end_unix_ms = MillisecondTimer.get_unix_ms()
        elapsed_ms = end_unix_ms - start_unix_ms
        
        log_entry = {
            "timestamp_iso_ms": MillisecondTimer.get_iso_ms(),
            "timestamp_unix_ms": end_unix_ms,
            "command": command,
            "origin": origin,
            "start_unix_ms": start_unix_ms,
            "end_unix_ms": end_unix_ms,
            "elapsed_ms": elapsed_ms,
            "elapsed_human": MillisecondTimer.format_delta_ms(elapsed_ms),
            "result": result
        }
        self.commands.append(log_entry)
        return log_entry
    
    def get_command_history_ms(self) -> list:
        """Returns command history with all millisecond timestamps."""
        return self.commands


if __name__ == "__main__":
    # Test millisecond timing
    print("=== MILLISECOND TIMING TEST ===\n")
    
    timer = MillisecondTimer()
    
    print(f"ISO (UTC): {timer.get_iso_ms()}")
    print(f"Unix (ms): {timer.get_unix_ms()}")
    print(f"Local ISO: {timer.get_local_iso_ms()}")
    
    print("\n=== Dual Timestamp ===")
    dual = timer.get_dual_timestamp()
    for key, val in dual.items():
        print(f"{key}: {val}")
    
    print("\n=== Measuring Operation ===")
    def test_operation():
        time.sleep(0.1)  # 100ms
        return "done"
    
    result, elapsed = timer.measure_operation_ms(test_operation)
    print(f"Result: {result}, Elapsed: {elapsed}ms")
    
    print("\n=== Delta Formatting ===")
    test_deltas = [100, 1000, 5000, 60000, 125000]
    for delta in test_deltas:
        print(f"{delta}ms -> {timer.format_delta_ms(delta)}")
    
    print("\n=== Command Logging ===")
    logger = CommandLogger()
    
    # Log command reception
    log1 = logger.log_command_ms("lock_energy_grid", "PHONE_ALPHA", "RECEIVED")
    print(f"Received: {log1['timestamp_iso_ms']}")
    
    # execute execution
    start_ms = log1['timestamp_unix_ms']
    time.sleep(0.15)  # 150ms execution
    
    # Log command completion
    log2 = logger.log_command_execution_ms("lock_energy_grid", "PHONE_ALPHA", start_ms, "SUCCESS")
    print(f"Completed: {log2['timestamp_iso_ms']} (Elapsed: {log2['elapsed_human']})")
