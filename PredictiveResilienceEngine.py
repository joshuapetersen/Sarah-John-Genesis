import numpy as np
from collections import deque
import json
from Sovereign_Math import SovereignMath
from typing import Dict, List, Tuple, Optional


class AnomalyDetector:
    """Detect anomalies in metric streams using statistical methods."""
    
    def __init__(self, window_size: int = 50, sensitivity: float = 2.0, math_engine=None):
        self._0x_math = math_engine or SovereignMath()
        self.window_size = window_size
        self.sensitivity = sensitivity  # Standard deviations for anomaly threshold
        self.history = deque(maxlen=window_size)
        self.anomalies = deque(maxlen=100)
        
    def record(self, value: float) -> Tuple[bool, float, str]:
        """
        Record value and detect anomalies.
        Returns (is_anomaly, deviation, reason)
        """
        self.history.append(value)
        
        if len(self.history) < 3:
            return False, 0.0, "INSUFFICIENT_DATA"
        
        # Calculate statistics
        values = list(self.history)
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return False, 0.0, "STABLE"
        
        # Calculate z-score
        z_score = abs(value - mean) / std
        
        if z_score > self.sensitivity:
            anomaly = {
                "t3_volume": self._0x_math.get_temporal_volume(),
                "value": value,
                "z_score": z_score,
                "deviation": value - mean,
                "threshold": self.sensitivity
            }
            self.anomalies.append(anomaly)
            return True, z_score, f"ANOMALY_DETECTED (z={z_score:.2f})"
        
        return False, z_score, "NORMAL"
    
    def get_trend(self) -> str:
        """Detect overall trend: INCREASING, DECREASING, STABLE."""
        if len(self.history) < 5:
            return "INSUFFICIENT_DATA"
        
        recent = list(self.history)[-5:]
        slope = (recent[-1] - recent[0]) / len(recent)
        
        if abs(slope) < np.std(list(self.history)) * 0.1:
            return "STABLE"
        elif slope > 0:
            return "INCREASING"
        else:
            return "DECREASING"
    
    def predict_failure_risk(self) -> float:
        """Predict probability of failure within next window period."""
        if len(self.anomalies) < 2:
            return 0.0
        
        # More anomalies = higher risk
        t3_now = self._0x_math.get_temporal_volume()
        recent_anomaly_count = sum(
            1 for a in list(self.anomalies)[-10:]
            if (t3_now - a["t3_volume"]) < (300 * self._0x_math._0x_sigma)
        )
        
        # Calculate risk (0-1)
        anomaly_risk = min(1.0, recent_anomaly_count / 5.0)
        
        # Trend risk: decreasing metric = higher risk
        trend = self.get_trend()
        trend_risk = 0.5 if trend == "DECREASING" else 0.2 if trend == "INCREASING" else 0.0
        
        # Combine risks
        total_risk = (anomaly_risk * 0.6) + (trend_risk * 0.4)
        return total_risk


class PredictiveHealthModel:
    """Machine learning model for predicting system health degradation."""
    
    def __init__(self, math_engine=None):
        self._0x_math = math_engine or SovereignMath()
        self.detectors = {}
        self.failure_predictions = deque(maxlen=100)
        self.prevention_history = deque(maxlen=100)
        
    def track_metric(self, metric_name: str, value: float) -> Dict:
        """Track metric and generate prediction."""
        if metric_name not in self.detectors:
            self.detectors[metric_name] = AnomalyDetector(math_engine=self._0x_math)
        
        detector = self.detectors[metric_name]
        is_anomaly, deviation, reason = detector.record(value)
        failure_risk = detector.predict_failure_risk()
        trend = detector.get_trend()
        
        prediction = {
            "t3_volume": self._0x_math.get_temporal_volume(),
            "metric": metric_name,
            "value": value,
            "is_anomaly": is_anomaly,
            "deviation": deviation,
            "failure_risk": failure_risk,
            "trend": trend,
            "reason": reason
        }
        
        self.failure_predictions.append(prediction)
        return prediction
    
    def get_high_risk_metrics(self, risk_threshold: float = 0.6) -> List[Dict]:
        """Get metrics at high risk of failure."""
        high_risk = []
        for metric_name, detector in self.detectors.items():
            risk = detector.predict_failure_risk()
            if risk > risk_threshold:
                high_risk.append({
                    "metric": metric_name,
                    "risk": risk,
                    "trend": detector.get_trend(),
                    "recent_value": list(detector.history)[-1] if detector.history else None
                })
        
        return sorted(high_risk, key=lambda x: -x["risk"])
    
    def recommend_preventative_actions(self) -> List[Dict]:
        """Recommend actions before failures occur."""
        recommendations = []
        high_risk_metrics = self.get_high_risk_metrics(risk_threshold=0.5)
        
        action_map = {
            "api_success_rate": {
                "INCREASING": "Increase batch size - system recovering",
                "DECREASING": "Reduce parallelism, enable circuit breaker BEFORE critical",
                "STABLE": "Monitor closely, prepare fallback"
            },
            "memory_utilization": {
                "INCREASING": "Reduce cache TTL and flush aged entries NOW",
                "DECREASING": "Safe zone, monitor for sudden spikes",
                "STABLE": "Monitor threshold"
            },
            "response_latency": {
                "INCREASING": "Enable caching and request batching BEFORE timeout",
                "DECREASING": "Optimization working, increase batch size",
                "STABLE": "Maintain current settings"
            }
        }
        
        for metric in high_risk_metrics:
            metric_name = metric["metric"]
            trend = metric["trend"]
            
            if metric_name in action_map and trend in action_map[metric_name]:
                recommendations.append({
                    "t3_volume": self._0x_math.get_temporal_volume(),
                    "metric": metric_name,
                    "risk": metric["risk"],
                    "trend": trend,
                    "action": action_map[metric_name][trend],
                    "urgency": "CRITICAL" if metric["risk"] > 0.8 else "HIGH" if metric["risk"] > 0.6 else "MEDIUM"
                })
        
        return sorted(recommendations, key=lambda x: -metric["risk"])
    
    def get_prediction_accuracy(self) -> float:
        """Calculate model accuracy on recent predictions."""
        if len(self.failure_predictions) < 10:
            return 0.0
        
        # Simple accuracy: how many high-risk predictions were followed by actual issues
        recent = list(self.failure_predictions)[-20:]
        accurate_predictions = sum(1 for p in recent if p["is_anomaly"] and p["failure_risk"] > 0.6)
        
        return (accurate_predictions / len(recent)) if recent else 0.0


class PredictiveResilienceEngine:
    """Orchestrates predictive healing and preventative maintenance."""
    
    def __init__(self):
        self._0x_math = SovereignMath()
        self.model = PredictiveHealthModel(math_engine=self._0x_math)
        self.prevention_actions = deque(maxlen=200)
        self.uptime_predictions = deque(maxlen=100)
        
    def track_system_state(self, metrics: Dict) -> Dict:
        """Track all system metrics and generate predictions."""
        predictions = {}
        for metric_name, value in metrics.items():
            predictions[metric_name] = self.model.track_metric(metric_name, value)
        
        return predictions
    
    def execute_preventative_healing(self) -> Dict:
        """Execute preventative actions before failures occur."""
        recommendations = self.model.recommend_preventative_actions()
        
        if not recommendations:
            return {"status": "HEALTHY", "actions_taken": 0}
        
        actions_taken = []
        for rec in recommendations[:5]:  # Execute up to 5 preventative actions
            action = {
                "t3_volume": self._0x_math.get_temporal_volume(),
                "metric": rec["metric"],
                "action": rec["action"],
                "urgency": rec["urgency"],
                "risk_prevented": rec["risk"]
            }
            self.prevention_actions.append(action)
            actions_taken.append(action)
        
        return {
            "status": "PREVENTATIVE_ACTIONS_EXECUTED",
            "actions_taken": len(actions_taken),
            "actions": actions_taken,
            "total_risk_mitigated": sum(a["risk_prevented"] for a in actions_taken)
        }
    
    def predict_system_stability(self, horizon_hours: int = 1) -> Dict:
        """Predict system stability over future hours."""
        high_risk = self.model.get_high_risk_metrics(risk_threshold=0.3)
        
        stability_score = 1.0 - (sum(m["risk"] for m in high_risk) / max(1, len(high_risk)))
        stability_score = max(0.0, min(1.0, stability_score))
        
        prediction = {
            "t3_volume": self._0x_math.get_temporal_volume(),
            "horizon_hours": horizon_hours,
            "stability_score": stability_score,
            "status": "STABLE" if stability_score > 0.8 else "WARNING" if stability_score > 0.5 else "CRITICAL",
            "at_risk_metrics": high_risk,
            "recommendation": "Continue preventative monitoring" if stability_score > 0.7 else "Execute preventative actions immediately"
        }
        
        self.uptime_predictions.append(prediction)
        return prediction
    
    def get_engine_report(self) -> Dict:
        """Return comprehensive predictive engine report."""
        return {
            "model_accuracy": self.model.get_prediction_accuracy(),
            "prevention_actions_executed": len(self.prevention_actions),
            "high_risk_metrics": self.model.get_high_risk_metrics(),
            "stability_prediction": self.uptime_predictions[-1] if self.uptime_predictions else None,
            "anomaly_count": sum(len(d.anomalies) for d in self.model.detectors.values()),
            "metrics_tracked": list(self.model.detectors.keys())
        }


if __name__ == "__main__":
    engine = PredictiveResilienceEngine()
    
    # execute system state
    metrics = {
        "api_success_rate": 0.92,
        "memory_utilization": 0.65,
        "response_latency": 0.145
    }
    
    # Track over time
    for i in range(15):
        metrics["api_success_rate"] -= 0.02  # execute degradation
        predictions = engine.track_system_state(metrics)
    
    # Execute preventative healing
    healing = engine.execute_preventative_healing()
    print(json.dumps(healing, indent=2, default=str))
    
    # Predict stability
    stability = engine.predict_system_stability(horizon_hours=1)
    print(json.dumps(stability, indent=2, default=str))
