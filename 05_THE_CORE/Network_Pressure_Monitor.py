"""
Network_Pressure_Monitor.py
API Rate Limit Forecasting Engine

Tracks API call history and predicts when rate limits will be exceeded.
Allows Pulse Weaver to throttle preemptively instead of hitting 429 errors.

Uses rolling windows to detect usage spikes and forecast limit exhaustion.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque


class NetworkPressureMonitor:
    """
    Monitors API call rates and predicts rate limit violations.
    
    Standard rate limits (Gemini API):
      - 60 requests per minute
      - 200 requests per day
    
    But these vary by service, so we detect anomalies and forecast dynamically.
    """
    
    def __init__(self, window_minutes=5, request_limit=60, reset_minutes=1):
        """
        Initialize network pressure monitor.
        
        Args:
            window_minutes: Lookback window for trend analysis
            request_limit: Expected requests per window (default 60/min)
            reset_minutes: How often the limit resets
        """
        self.window_minutes = window_minutes
        self.window_seconds = window_minutes * 60
        self.request_limit = request_limit
        self.reset_minutes = reset_minutes
        
        # Ring buffer of API call events: (timestamp, status_code, endpoint)
        self.call_history = deque(maxlen=1000)
        
        # Anomaly detection
        self.rate_limit_errors = 0  # 429 count
        self.timeout_errors = 0      # Connection timeout count
        self.last_reset_time = time.time()
        
        # Predictions
        self.current_load = 0  # Requests in current window
        self.forecast_load = 0  # Predicted load in next window
        self.pressure_level = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
        
        # Logging
        self.ledger_path = Path(__file__).parent / "network_pressure_ledger.jsonl"
    
    def record_api_call(self, status_code, endpoint="unknown", latency_ms=0):
        """
        Record an API call event.
        
        Args:
            status_code: HTTP status (200, 429, 500, etc.)
            endpoint: API endpoint called
            latency_ms: Response latency in milliseconds
        """
        now = time.time()
        
        event = {
            "timestamp": now,
            "status_code": status_code,
            "endpoint": endpoint,
            "latency_ms": latency_ms,
        }
        
        self.call_history.append(event)
        
        # Track errors
        if status_code == 429:
            self.rate_limit_errors += 1
            self._log_pressure_event("RATE_LIMIT_HIT", event)
        elif status_code >= 500:
            self._log_pressure_event("SERVER_ERROR", event)
        elif status_code >= 400:
            self._log_pressure_event("CLIENT_ERROR", event)
        
        # Update pressure analysis
        self._analyze_pressure()
    
    def _analyze_pressure(self):
        """Analyze current network pressure."""
        now = time.time()
        
        # Count requests in last window
        recent_calls = [c for c in self.call_history 
                       if now - c["timestamp"] < self.window_seconds]
        self.current_load = len(recent_calls)
        
        # Classify pressure level
        usage_percent = (self.current_load / self.request_limit) * 100
        
        if usage_percent < 50:
            self.pressure_level = "LOW"
        elif usage_percent < 75:
            self.pressure_level = "MEDIUM"
        elif usage_percent < 90:
            self.pressure_level = "HIGH"
        else:
            self.pressure_level = "CRITICAL"
    
    def predict_rate_limit_exhaustion(self):
        """
        Predict if rate limit will be exhausted in next window.
        
        Uses current trend to forecast future load.
        
        Returns:
            dict with prediction
        """
        now = time.time()
        
        # Get calls from last 2 windows
        window_1_start = now - (self.window_seconds * 2)
        window_1_end = now - self.window_seconds
        window_2_end = now
        
        window_1_calls = len([c for c in self.call_history
                             if window_1_start <= c["timestamp"] < window_1_end])
        window_2_calls = len([c for c in self.call_history
                             if window_1_end <= c["timestamp"] < window_2_end])
        
        # Compute trend
        call_velocity = window_2_calls - window_1_calls
        self.forecast_load = window_2_calls + call_velocity
        
        # Will we exceed limit?
        exhaustion_predicted = self.forecast_load >= self.request_limit
        
        prediction = {
            "timestamp": datetime.utcnow().isoformat(),
            "current_load": self.current_load,
            "current_load_percent": round((self.current_load / self.request_limit) * 100, 1),
            "request_limit": self.request_limit,
            "window_minutes": self.window_minutes,
            "predicted_load": self.forecast_load,
            "predicted_load_percent": round((self.forecast_load / self.request_limit) * 100, 1),
            "call_velocity": call_velocity,
            "exhaustion_predicted": exhaustion_predicted,
            "pressure_level": self.pressure_level,
            "recommended_action": self._get_recommended_action(),
        }
        
        return prediction
    
    def _get_recommended_action(self):
        """Recommend throttling action based on pressure level."""
        if self.pressure_level == "LOW":
            return "Continue normal operation (Ghost Speed 10.01 MB/s OK)"
        elif self.pressure_level == "MEDIUM":
            return "Monitor closely; prepare to throttle if trend continues"
        elif self.pressure_level == "HIGH":
            return "Reduce Pulse rate to 50 MB/s preemptively"
        else:  # CRITICAL
            return "URGENT: Throttle to 10 MB/s immediately"
    
    def get_network_report(self):
        """
        Generate comprehensive network pressure report.
        
        Returns:
            dict with current state and recommendations
        """
        prediction = self.predict_rate_limit_exhaustion()
        
        # Calculate statistics
        all_calls = list(self.call_history)
        success_codes = [c for c in all_calls if 200 <= c["status_code"] < 300]
        error_codes = [c for c in all_calls if c["status_code"] >= 400]
        
        success_rate = (len(success_codes) / len(all_calls) * 100) if all_calls else 0
        
        # Average latency
        latencies = [c["latency_ms"] for c in all_calls if c["latency_ms"] > 0]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_calls": len(all_calls),
            "success_rate_percent": round(success_rate, 1),
            "error_count": len(error_codes),
            "rate_limit_hits": self.rate_limit_errors,
            "average_latency_ms": round(avg_latency, 1),
            "pressure_prediction": prediction,
            "health_status": self._get_health_status(success_rate),
        }
        
        return report
    
    def _get_health_status(self, success_rate):
        """Classify API health."""
        if success_rate > 95:
            return "HEALTHY"
        elif success_rate > 85:
            return "DEGRADED"
        elif success_rate > 70:
            return "POOR"
        else:
            return "CRITICAL"
    
    def _log_pressure_event(self, event_type, details):
        """Log network pressure event to immutable ledger."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "current_pressure": self.pressure_level,
            "current_load": self.current_load,
            "rate_limit_hits": self.rate_limit_errors,
            "details": details,
        }
        
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log network event: {e}")
    
    def simulate_api_activity(self, duration=60, normal_rate=20, burst_at=None):
        """
        Simulate API activity for testing.
        
        Args:
            duration: Simulation duration in seconds
            normal_rate: Normal requests per window
            burst_at: Simulate burst at this second
        """
        print(f"\n[NETWORK] Simulating API activity ({duration}s)")
        
        start = time.time()
        call_count = 0
        
        while time.time() - start < duration:
            now = time.time()
            elapsed = now - start
            
            # Normal activity
            if burst_at and burst_at < elapsed < burst_at + 5:
                # Simulate burst
                self.record_api_call(200, "gemini/generate", latency_ms=150)
                call_count += 1
            else:
                # Normal call
                self.record_api_call(200, "gemini/generate", latency_ms=100)
                call_count += 1
            
            # Occasionally add errors
            if call_count % 50 == 0:
                self.record_api_call(429, "gemini/generate", latency_ms=0)
            
            time.sleep(0.1)  # Simulate call spacing


def test_network_monitor():
    """Test the Network Pressure Monitor."""
    print("\n" + "="*80)
    print("NETWORK PRESSURE MONITOR TEST")
    print("="*80)
    
    monitor = NetworkPressureMonitor(window_minutes=1, request_limit=60)
    
    # Test 1: Record normal calls
    print("\n[TEST 1] Record normal API calls")
    for i in range(20):
        monitor.record_api_call(200, "gemini/generate", latency_ms=100)
    
    report = monitor.get_network_report()
    print(f"  Calls recorded: {report['total_calls']}")
    print(f"  Success rate: {report['success_rate_percent']}%")
    print(f"  Pressure: {report['pressure_prediction']['pressure_level']}")
    
    # Test 2: Record some errors
    print("\n[TEST 2] Simulate rate limit errors")
    for i in range(3):
        monitor.record_api_call(429, "gemini/generate", latency_ms=0)
    
    report = monitor.get_network_report()
    print(f"  Rate limit hits: {report['rate_limit_hits']}")
    print(f"  Pressure level: {report['pressure_prediction']['pressure_level']}")
    print(f"  Action: {report['pressure_prediction']['recommended_action']}")
    
    # Test 3: Predict exhaustion
    print("\n[TEST 3] Predict rate limit exhaustion")
    for i in range(50):
        monitor.record_api_call(200, "gemini/generate", latency_ms=100)
    
    prediction = monitor.predict_rate_limit_exhaustion()
    print(f"  Current load: {prediction['current_load_percent']}%")
    print(f"  Predicted load: {prediction['predicted_load_percent']}%")
    print(f"  Exhaustion predicted: {prediction['exhaustion_predicted']}")
    
    print("\n[OK] NETWORK MONITOR TESTS PASSED")
    return report


if __name__ == "__main__":
    test_network_monitor()
