import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class PerformanceMetrics:
    """
    System Health & Performance Monitoring.
    Tracks reasoning quality, error rates, module efficiency, and evolution progress.
    """
    def __init__(self, core_dir=None):
        if core_dir:
            self.core_dir = core_dir
        else:
            self.core_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.metrics_dir = os.path.join(self.core_dir, "archive_memories", "metrics")
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        self.metrics_file = os.path.join(self.metrics_dir, "system_metrics.json")
        self.metrics = self._load_metrics()

    def _load_metrics(self) -> Dict[str, Any]:
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except:
                return self._init_metrics()
        return self._init_metrics()

    def _init_metrics(self) -> Dict[str, Any]:
        return {
            "session_start": datetime.now().isoformat(),
            "total_threads": 0,
            "error_count": 0,
            "reasoning_cycles": 0,
            "avg_reasoning_time": 0.0,
            "module_health": {
                "thread_weaver": "healthy",
                "neural_memory": "healthy",
                "strategic_planner": "healthy",
                "dialectical_logic": "healthy"
            },
            "error_log": [],
            "performance_timeline": []
        }

    def _save_metrics(self):
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)

    def record_error(self, module_name: str, error_msg: str, severity: str = "warning"):
        """Log an error and update module health."""
        self.metrics["error_count"] += 1
        
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "module": module_name,
            "message": error_msg,
            "severity": severity
        }
        self.metrics["error_log"].append(error_entry)
        
        # Update module health
        if severity == "critical":
            self.metrics["module_health"][module_name] = "degraded"
        elif severity == "error":
            self.metrics["module_health"][module_name] = "warning"
        
        print(f"[Metrics] {severity.upper()}: {module_name} - {error_msg}")
        self._save_metrics()

    def record_reasoning(self, duration_sec: float, success: bool, complexity: str = "standard"):
        """Record a reasoning cycle."""
        self.metrics["reasoning_cycles"] += 1
        
        # Update average time
        prev_avg = self.metrics.get("avg_reasoning_time", 0)
        new_avg = (prev_avg * (self.metrics["reasoning_cycles"] - 1) + duration_sec) / self.metrics["reasoning_cycles"]
        self.metrics["avg_reasoning_time"] = new_avg
        
        perf_entry = {
            "timestamp": datetime.now().isoformat(),
            "duration": duration_sec,
            "success": success,
            "complexity": complexity
        }
        self.metrics["performance_timeline"].append(perf_entry)
        
        print(f"[Metrics] Reasoning cycle: {duration_sec:.3f}s ({complexity})")
        self._save_metrics()

    def get_health_report(self) -> Dict[str, Any]:
        """Generate a system health report."""
        total_errors = self.metrics["error_count"]
        total_reasoning = self.metrics["reasoning_cycles"]
        
        error_rate = (total_errors / total_reasoning * 100) if total_reasoning > 0 else 0
        
        health_status = "healthy"
        if error_rate > 20:
            health_status = "degraded"
        elif error_rate > 50:
            health_status = "critical"
        
        return {
            "overall_status": health_status,
            "error_rate": f"{error_rate:.2f}%",
            "total_errors": total_errors,
            "total_reasoning_cycles": total_reasoning,
            "avg_reasoning_time": f"{self.metrics['avg_reasoning_time']:.3f}s",
            "module_health": self.metrics["module_health"],
            "timestamp": datetime.now().isoformat()
        }

    def get_top_errors(self, limit: int = 5) -> List[Dict]:
        """Get the most frequent error types."""
        error_counts = {}
        for error in self.metrics["error_log"]:
            key = f"{error['module']}: {error['message'][:50]}"
            error_counts[key] = error_counts.get(key, 0) + 1
        
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"error": k, "count": v} for k, v in sorted_errors[:limit]]

if __name__ == "__main__":
    metrics = PerformanceMetrics()
    metrics.record_reasoning(0.5, True, "optimization")
    metrics.record_error("thread_weaver", "Semantic search returned 0 results", "warning")
    print(json.dumps(metrics.get_health_report(), indent=2))
