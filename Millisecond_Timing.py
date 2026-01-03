"""
MILLISECOND TIMING MODULE
Provides high-precision timing utilities across all systems.
All timestamps calculated to millisecond precision.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

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
    
    # Simulate execution
    start_ms = log1['timestamp_unix_ms']
    time.sleep(0.15)  # 150ms execution
    
    # Log command completion
    log2 = logger.log_command_execution_ms("lock_energy_grid", "PHONE_ALPHA", start_ms, "SUCCESS")
    print(f"Completed: {log2['timestamp_iso_ms']} (Elapsed: {log2['elapsed_human']})")
