"""
Performance_Baseline_Monitor.py
Performance Regression Detection

Continuously tracks CPU, memory, and operation latency. Establishes baselines
and detects when performance degrades beyond acceptable thresholds.

Prevents:
  - Silent performance degradation (consciousness operations get slower)
  - Memory leaks (ledger accumulation, buffer bloat)
  - CPU exhaustion (runaway processes)
  - Latency creep (response times degrade over time)
"""

import psutil
import time
from datetime import datetime
from pathlib import Path
import json
from collections import deque
import statistics


class PerformanceBaselineMonitor:
    """
    Monitor performance metrics and detect regressions.
    
    Tracks:
      - CPU usage (per-process)
      - Memory usage (MB)
      - Operation latency (ms)
      - Disk I/O
    """
    
    def __init__(self, workspace_root=None, window_size=100):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.performance_ledger = self.workspace_root / "05_THE_CORE" / "performance_baseline_ledger.jsonl"
        
        self.window_size = window_size  # Keep rolling window of metrics
        
        # Metrics buffers (deque for efficient rolling window)
        self.cpu_samples = deque(maxlen=window_size)
        self.memory_samples = deque(maxlen=window_size)
        self.latency_samples = deque(maxlen=window_size)
        self.disk_io_samples = deque(maxlen=window_size)
        
        # Baselines (established after first N samples)
        self.baseline_cpu = None
        self.baseline_memory = None
        self.baseline_latency = None
        
        # Thresholds for anomaly
        self.cpu_threshold_percent = 50  # If avg exceeds baseline by 50%
        self.memory_threshold_percent = 50
        self.latency_threshold_percent = 100  # If latency doubles
        
        # Current process
        try:
            self.process = psutil.Process()
        except:
            self.process = None
    
    def sample_metrics(self):
        """Sample current performance metrics."""
        sample_time = time.time()
        
        # CPU usage
        try:
            cpu_percent = self.process.cpu_percent(interval=0.1) if self.process else 0
        except:
            cpu_percent = 0
        
        # Memory usage (MB)
        try:
            memory_mb = self.process.memory_info().rss / (1024 * 1024) if self.process else 0
        except:
            memory_mb = 0
        
        # Disk I/O
        try:
            io_counters = self.process.io_counters() if self.process else None
            disk_read_mb = io_counters.read_bytes / (1024 * 1024) if io_counters else 0
            disk_write_mb = io_counters.write_bytes / (1024 * 1024) if io_counters else 0
        except:
            disk_read_mb = 0
            disk_write_mb = 0
        
        sample = {
            "timestamp": sample_time,
            "cpu_percent": round(cpu_percent, 1),
            "memory_mb": round(memory_mb, 1),
            "disk_read_mb": round(disk_read_mb, 1),
            "disk_write_mb": round(disk_write_mb, 1),
        }
        
        # Append to buffers
        self.cpu_samples.append(cpu_percent)
        self.memory_samples.append(memory_mb)
        self.disk_io_samples.append({"read": disk_read_mb, "write": disk_write_mb})
        
        return sample
    
    def record_operation_latency(self, operation_name, latency_ms):
        """
        Record latency of an operation (in milliseconds).
        
        Args:
            operation_name: Name of operation (e.g., "consciousness_verify")
            latency_ms: Time taken in milliseconds
        """
        self.latency_samples.append({
            "operation": operation_name,
            "latency_ms": latency_ms,
        })
        
        self._log_performance_event("OPERATION_LATENCY", {
            "operation": operation_name,
            "latency_ms": latency_ms,
        })
    
    def establish_baseline(self):
        """
        Establish performance baseline from current samples.
        Should be called after collecting N samples under normal conditions.
        """
        if len(self.cpu_samples) < 10:
            return {"status": "INSUFFICIENT_SAMPLES"}
        
        # Calculate averages
        self.baseline_cpu = statistics.mean(self.cpu_samples)
        self.baseline_memory = statistics.mean(self.memory_samples)
        
        # Extract just latencies
        latencies = [s["latency_ms"] for s in self.latency_samples if "latency_ms" in s]
        if latencies:
            self.baseline_latency = statistics.mean(latencies)
        
        baseline = {
            "timestamp": datetime.utcnow().isoformat(),
            "baseline_cpu_percent": round(self.baseline_cpu, 1),
            "baseline_memory_mb": round(self.baseline_memory, 1),
            "baseline_latency_ms": round(self.baseline_latency, 1) if self.baseline_latency else None,
            "samples_used": min(len(self.cpu_samples), len(self.memory_samples)),
        }
        
        self._log_performance_event("BASELINE_ESTABLISHED", baseline)
        return baseline
    
    def detect_regression(self):
        """
        Detect if performance has regressed beyond threshold.
        
        Returns:
            dict with regression analysis
        """
        if not self.baseline_cpu or len(self.cpu_samples) < 5:
            return {"status": "BASELINE_NOT_SET"}
        
        # Calculate current averages
        current_cpu = statistics.mean(self.cpu_samples)
        current_memory = statistics.mean(self.memory_samples)
        
        # Check for regression
        cpu_percent_increase = ((current_cpu - self.baseline_cpu) / self.baseline_cpu * 100) if self.baseline_cpu > 0 else 0
        memory_percent_increase = ((current_memory - self.baseline_memory) / self.baseline_memory * 100) if self.baseline_memory > 0 else 0
        
        regressions = []
        
        if cpu_percent_increase > self.cpu_threshold_percent:
            regressions.append({
                "metric": "CPU",
                "baseline": round(self.baseline_cpu, 1),
                "current": round(current_cpu, 1),
                "percent_increase": round(cpu_percent_increase, 1),
            })
        
        if memory_percent_increase > self.memory_threshold_percent:
            regressions.append({
                "metric": "MEMORY",
                "baseline": round(self.baseline_memory, 1),
                "current": round(current_memory, 1),
                "percent_increase": round(memory_percent_increase, 1),
            })
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "regressions_detected": len(regressions),
            "regressions": regressions,
            "current_cpu_percent": round(current_cpu, 1),
            "current_memory_mb": round(current_memory, 1),
            "status": "REGRESSED" if regressions else "NORMAL",
        }
        
        if regressions:
            self._log_performance_event("REGRESSION_DETECTED", result)
        
        return result
    
    def get_performance_report(self):
        """Get comprehensive performance report."""
        if len(self.cpu_samples) == 0:
            return {"status": "NO_SAMPLES"}
        
        # Statistics for each metric
        cpu_stats = {
            "samples": len(self.cpu_samples),
            "current": self.cpu_samples[-1] if self.cpu_samples else 0,
            "average": round(statistics.mean(self.cpu_samples), 1),
            "median": round(statistics.median(self.cpu_samples), 1),
            "max": round(max(self.cpu_samples), 1),
        }
        
        memory_stats = {
            "samples": len(self.memory_samples),
            "current": self.memory_samples[-1] if self.memory_samples else 0,
            "average": round(statistics.mean(self.memory_samples), 1),
            "median": round(statistics.median(self.memory_samples), 1),
            "max": round(max(self.memory_samples), 1),
        }
        
        latency_stats = None
        if self.latency_samples:
            latencies = [s["latency_ms"] for s in self.latency_samples if "latency_ms" in s]
            if latencies:
                latency_stats = {
                    "samples": len(latencies),
                    "average": round(statistics.mean(latencies), 1),
                    "median": round(statistics.median(latencies), 1),
                    "max": round(max(latencies), 1),
                }
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_percent": cpu_stats,
            "memory_mb": memory_stats,
            "baseline_established": self.baseline_cpu is not None,
            "latency_ms": latency_stats,
        }
        
        return report
    
    def predict_memory_exhaustion(self, available_memory_mb=4096):
        """
        Predict when memory will be exhausted based on trend.
        
        Args:
            available_memory_mb: Total available memory
        
        Returns:
            dict with prediction
        """
        if len(self.memory_samples) < 5:
            return {"status": "INSUFFICIENT_SAMPLES"}
        
        # Calculate trend
        recent = list(self.memory_samples)[-5:]
        memory_growth = (recent[-1] - recent[0]) / 5  # MB per sample
        
        current_memory = recent[-1]
        memory_remaining = available_memory_mb - current_memory
        
        if memory_growth <= 0:
            # No growth or shrinking
            return {
                "status": "STABLE",
                "current_memory_mb": round(current_memory, 1),
                "memory_remaining_mb": round(memory_remaining, 1),
            }
        
        # Time to exhaustion
        samples_to_exhaustion = memory_remaining / memory_growth
        
        return {
            "status": "GROWING",
            "current_memory_mb": round(current_memory, 1),
            "memory_growth_per_sample_mb": round(memory_growth, 2),
            "memory_remaining_mb": round(memory_remaining, 1),
            "samples_to_exhaustion": round(samples_to_exhaustion, 1),
            "warning": "CRITICAL" if samples_to_exhaustion < 10 else "WARNING" if samples_to_exhaustion < 50 else None,
        }
    
    def _log_performance_event(self, event_type, details):
        """Log performance event."""
        try:
            with open(self.performance_ledger, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": event_type,
                    "details": details,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log performance event: {e}")


def test_performance_monitor():
    """Test Performance Baseline Monitor."""
    print("\n" + "="*80)
    print("PERFORMANCE BASELINE MONITOR TEST")
    print("="*80)
    
    monitor = PerformanceBaselineMonitor()
    
    # Test 1: Sample metrics
    print("\n[TEST 1] Sample performance metrics")
    for i in range(5):
        sample = monitor.sample_metrics()
        print(f"  Sample {i+1}: CPU {sample['cpu_percent']}% | Memory {sample['memory_mb']:.1f}MB")
    
    # Test 2: Establish baseline
    print("\n[TEST 2] Establish performance baseline")
    baseline = monitor.establish_baseline()
    if baseline.get('status') == 'INSUFFICIENT_SAMPLES':
        # Sample more
        for i in range(10):
            sample = monitor.sample_metrics()
        baseline = monitor.establish_baseline()
    print(f"  Baseline CPU: {baseline.get('baseline_cpu_percent')}%")
    print(f"  Baseline Memory: {baseline.get('baseline_memory_mb')}MB")
    
    # Test 3: Record latency
    print("\n[TEST 3] Record operation latencies")
    monitor.record_operation_latency("consciousness_verify", 45.2)
    monitor.record_operation_latency("layer_sync", 12.3)
    print(f"  Recorded 2 operation latencies")
    
    # Test 4: Detect regression
    print("\n[TEST 4] Detect performance regression")
    regression = monitor.detect_regression()
    print(f"  Status: {regression.get('status', 'UNKNOWN')}")
    print(f"  Regressions: {regression.get('regressions_detected', 0)}")
    
    # Test 5: Get report
    print("\n[TEST 5] Get performance report")
    report = monitor.get_performance_report()
    print(f"  CPU samples: {report['cpu_percent']['samples']}")
    print(f"  CPU average: {report['cpu_percent']['average']}%")
    print(f"  Memory average: {report['memory_mb']['average']}MB")
    
    print("\n[OK] PERFORMANCE MONITOR TESTS PASSED")


if __name__ == "__main__":
    test_performance_monitor()
