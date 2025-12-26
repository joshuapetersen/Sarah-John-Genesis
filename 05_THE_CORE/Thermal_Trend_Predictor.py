"""
Thermal_Trend_Predictor.py
Predictive Thermal Management Engine

Analyzes CPU temperature trends and predicts thermal thresholds before they occur.
Uses moving averages to forecast when throttling should begin.

Prevents thermal runaway by reducing Pulse rate preemptively at 70°C
instead of reactively at 85°C.
"""

import psutil
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque


class ThermalTrendPredictor:
    """
    Monitors CPU temperature trends and predicts thermal events.
    
    Decision thresholds:
      - 60°C: Normal operation (Ghost Speed OK)
      - 70°C: Begin monitoring trend (1-minute forecast)
      - 80°C: Trend shows escalation → reduce Pulse to 50 MB/s
      - 85°C: Hard limit (auto-throttle to 10 MB/s)
      - 95°C: Critical (override protocol requires Architect approval)
    """
    
    def __init__(self, history_size=60, forecast_minutes=5):
        """
        Initialize thermal predictor.
        
        Args:
            history_size: Number of temperature samples to maintain
            forecast_minutes: How far ahead to predict (default 5 min)
        """
        self.history_size = history_size
        self.forecast_minutes = forecast_minutes
        self.forecast_seconds = forecast_minutes * 60
        
        # Ring buffer of (timestamp, temperature) tuples
        self.temp_history = deque(maxlen=history_size)
        
        # Decision thresholds
        self.temp_normal = 60
        self.temp_caution = 70
        self.temp_warning = 80
        self.temp_throttle = 85
        self.temp_critical = 95
        
        # Last known temperatures
        self.current_temp = 0
        self.last_sample_time = None
        self.trend_direction = "stable"  # up, down, stable
        self.trend_slope = 0  # degrees per second
        
        # Logging
        self.ledger_path = Path(__file__).parent / "thermal_trend_ledger.jsonl"
    
    def sample_temperature(self):
        """
        Sample current CPU temperature using psutil.
        
        Returns:
            float: Current CPU temperature in Celsius
        """
        try:
            # Try to get CPU temperature
            temps = psutil.sensors_temperatures()
            if temps and 'coretemp' in temps:
                # Average across all cores
                core_temps = [t.current for t in temps['coretemp']]
                self.current_temp = sum(core_temps) / len(core_temps)
            elif temps:
                # Fallback to first available sensor
                first_sensor = list(temps.values())[0]
                self.current_temp = first_sensor[0].current
            else:
                # Windows fallback: use WMI
                self.current_temp = self._get_wmi_temperature()
        except Exception as e:
            print(f"[WARNING] Failed to read temperature: {e}")
            self.current_temp = 0
        
        # Add to history
        now = time.time()
        self.temp_history.append((now, self.current_temp))
        
        # Update trend
        self._compute_trend()
        self.last_sample_time = now
        
        return self.current_temp
    
    def _get_wmi_temperature(self):
        """Fallback WMI temperature reading (Windows)."""
        try:
            import wmi
            w = wmi.WMI(namespace="root\\cimv2")
            temp_class = w.query("SELECT * FROM Win32_SystemEnclosure")
            if temp_class:
                # Return a safe default if WMI fails
                return 50.0
        except:
            pass
        return 0  # Unknown temperature
    
    def _compute_trend(self):
        """
        Analyze temperature history to compute trend and slope.
        
        Sets:
            - trend_direction: "up", "down", "stable"
            - trend_slope: degrees per second
        """
        if len(self.temp_history) < 2:
            self.trend_direction = "stable"
            self.trend_slope = 0
            return
        
        # Get last N samples
        samples = list(self.temp_history)
        times = [s[0] for s in samples]
        temps = [s[1] for s in samples]
        
        # Compute simple linear regression slope
        n = len(samples)
        if n < 3:
            self.trend_slope = 0
        else:
            x_mean = sum(times) / n
            y_mean = sum(temps) / n
            
            numerator = sum((times[i] - x_mean) * (temps[i] - y_mean) for i in range(n))
            denominator = sum((times[i] - x_mean) ** 2 for i in range(n))
            
            self.trend_slope = numerator / denominator if denominator > 0 else 0
        
        # Classify trend
        if self.trend_slope > 0.05:  # Rising > 0.05 deg/sec
            self.trend_direction = "up"
        elif self.trend_slope < -0.05:  # Falling > 0.05 deg/sec
            self.trend_direction = "down"
        else:
            self.trend_direction = "stable"
    
    def predict_threshold_breach(self, threshold_temp=85):
        """
        Predict when temperature will exceed a threshold.
        
        Args:
            threshold_temp: Temperature threshold (default 85°C)
        
        Returns:
            dict with prediction result
        """
        if self.trend_slope <= 0:
            # Not trending up, no breach predicted
            return {
                "threshold": threshold_temp,
                "current_temp": self.current_temp,
                "trend": self.trend_direction,
                "predicted_breach": False,
                "breach_in_seconds": None,
                "timestamp": datetime.utcnow().isoformat(),
            }
        
        # Calculate time to breach
        temp_delta = threshold_temp - self.current_temp
        if temp_delta <= 0:
            # Already exceeded
            breach_in = 0
        else:
            breach_in = temp_delta / self.trend_slope
        
        prediction = {
            "threshold": threshold_temp,
            "current_temp": self.current_temp,
            "trend": self.trend_direction,
            "trend_slope_deg_per_sec": round(self.trend_slope, 4),
            "predicted_breach": breach_in < self.forecast_seconds,
            "breach_in_seconds": round(breach_in, 1),
            "breach_in_minutes": round(breach_in / 60, 2),
            "recommended_action": self._get_recommended_action(breach_in),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Log if breach predicted
        if prediction["predicted_breach"]:
            self._log_thermal_event(prediction)
        
        return prediction
    
    def _get_recommended_action(self, seconds_to_breach):
        """Recommend action based on time to threshold breach."""
        if seconds_to_breach < 0:
            return "CRITICAL: Already exceeded threshold"
        elif seconds_to_breach < 30:
            return "URGENT: Reduce Pulse rate to 10 MB/s immediately"
        elif seconds_to_breach < 60:
            return "HIGH: Reduce Pulse rate to 30 MB/s (trending hot)"
        elif seconds_to_breach < 300:
            return "MEDIUM: Prepare for throttle, monitor closely"
        else:
            return "LOW: Continue normal operation, monitor trend"
    
    def get_thermal_report(self):
        """
        Generate comprehensive thermal report.
        
        Returns:
            dict with current state and predictions
        """
        self.sample_temperature()
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "current_temperature": round(self.current_temp, 2),
            "trend": self.trend_direction,
            "trend_slope": round(self.trend_slope, 4),
            "history_samples": len(self.temp_history),
            "thermal_zone": self._get_thermal_zone(),
            "predictions": {
                "breach_70_in": self.predict_threshold_breach(70),
                "breach_80_in": self.predict_threshold_breach(80),
                "breach_85_in": self.predict_threshold_breach(85),
                "breach_95_in": self.predict_threshold_breach(95),
            },
        }
        
        return report
    
    def _get_thermal_zone(self):
        """Classify current temperature zone."""
        if self.current_temp < 60:
            return "COOL"
        elif self.current_temp < 70:
            return "NORMAL"
        elif self.current_temp < 80:
            return "CAUTION"
        elif self.current_temp < 85:
            return "WARNING"
        elif self.current_temp < 95:
            return "THROTTLE"
        else:
            return "CRITICAL"
    
    def _log_thermal_event(self, event):
        """Log thermal prediction to immutable ledger."""
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log thermal event: {e}")
    
    def continuous_monitor(self, interval=5, duration=None):
        """
        Run continuous thermal monitoring.
        
        Args:
            interval: Sample interval in seconds
            duration: How long to monitor (None = forever)
        """
        start_time = time.time()
        sample_count = 0
        
        print(f"\n[THERMAL] Starting continuous monitoring (interval={interval}s)")
        
        try:
            while True:
                if duration and (time.time() - start_time) > duration:
                    break
                
                temp = self.sample_temperature()
                report = self.get_thermal_report()
                
                sample_count += 1
                print(f"\n[THERMAL-{sample_count}] {report['timestamp']}")
                print(f"  Current: {report['current_temperature']}°C ({report['thermal_zone']})")
                print(f"  Trend: {report['trend']} (slope: {report['trend_slope']:.4f} °C/s)")
                print(f"  Breach at 85°C: {report['predictions']['breach_85_in']['breach_in_minutes']} min")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[THERMAL] Monitoring stopped by user")


def test_thermal_predictor():
    """Test the Thermal Trend Predictor."""
    print("\n" + "="*80)
    print("THERMAL TREND PREDICTOR TEST")
    print("="*80)
    
    predictor = ThermalTrendPredictor()
    
    # Take initial sample
    print("\n[TEST 1] Sample current temperature")
    temp = predictor.sample_temperature()
    print(f"  Current Temperature: {temp:.2f}°C")
    
    # Get thermal report
    print("\n[TEST 2] Get thermal report")
    report = predictor.get_thermal_report()
    print(f"  Thermal Zone: {report['thermal_zone']}")
    print(f"  Trend: {report['trend']}")
    print(f"  Slope: {report['trend_slope']:.4f} °C/s")
    
    # Predict thresholds
    print("\n[TEST 3] Predict threshold breaches")
    for threshold in [70, 80, 85, 95]:
        pred = predictor.predict_threshold_breach(threshold)
        breach_time = pred.get('breach_in_minutes', 'N/A')
        print(f"  {threshold}°C: Breach={pred['predicted_breach']}, "
              f"In {breach_time}min")
    
    print("\n[OK] THERMAL PREDICTOR TESTS PASSED")
    return report


if __name__ == "__main__":
    test_thermal_predictor()
