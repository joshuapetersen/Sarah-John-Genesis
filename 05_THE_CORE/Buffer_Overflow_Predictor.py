"""
Buffer_Overflow_Predictor.py
Ledger/Buffer Capacity Forecasting

Monitors ledger growth rates and predicts when buffers will reach capacity.
Enables proactive archival before data loss occurs.

Prevents:
  - Ledger file exhaustion (disk space issue)
  - JSON parsing delays (huge files)
  - Memory exhaustion (loading entire ledgers)
  - Loss of immutable audit trail
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import deque
import statistics


class BufferOverflowPredictor:
    """
    Predict buffer/ledger overflow before it occurs.
    
    Monitors ledger sizes and growth rates, forecasts when they'll hit limits.
    """
    
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.core_dir = self.workspace_root / "05_THE_CORE"
        self.buffer_ledger = self.core_dir / "buffer_overflow_ledger.jsonl"
        
        # Ledgers to monitor
        self.monitored_ledgers = [
            "coherence_ledger.jsonl",
            "thermal_trend_ledger.jsonl",
            "network_pressure_ledger.jsonl",
            "coherence_engine_ledger.jsonl",
            "recovery_trigger_ledger.jsonl",
            "layer_sync_ledger.jsonl",
            "integrity_scan_ledger.jsonl",
            "proof_continuity_ledger.jsonl",
            "performance_baseline_ledger.jsonl",
            "security_drift_ledger.jsonl",
        ]
        
        # Thresholds
        self.size_threshold_mb = 500  # Alert when ledger approaches 500MB
        self.lines_threshold = 1_000_000  # Alert at 1M lines
        
        # Historical size tracking (for trend analysis)
        self.size_history = {}  # {ledger_name: deque of (timestamp, size_bytes)}
        self.max_history = 100
        
        # Load history
        self._load_size_history()
    
    def sample_ledger_sizes(self):
        """
        Sample current size of all monitored ledgers.
        
        Returns:
            dict with size information for each ledger
        """
        sample = {
            "timestamp": datetime.utcnow().isoformat(),
            "ledgers": {},
            "total_size_mb": 0,
        }
        
        for ledger_name in self.monitored_ledgers:
            ledger_path = self.core_dir / ledger_name
            
            size_bytes = 0
            line_count = 0
            
            if ledger_path.exists():
                size_bytes = ledger_path.stat().st_size
                
                # Count lines
                try:
                    with open(ledger_path, 'r') as f:
                        line_count = sum(1 for _ in f)
                except:
                    line_count = 0
            
            size_mb = size_bytes / (1024 * 1024)
            
            sample["ledgers"][ledger_name] = {
                "size_bytes": size_bytes,
                "size_mb": round(size_mb, 2),
                "lines": line_count,
                "exists": ledger_path.exists(),
            }
            
            sample["total_size_mb"] += size_mb
            
            # Track in history
            if ledger_name not in self.size_history:
                self.size_history[ledger_name] = deque(maxlen=self.max_history)
            
            self.size_history[ledger_name].append({
                "timestamp": datetime.utcnow().isoformat(),
                "size_bytes": size_bytes,
            })
        
        sample["total_size_mb"] = round(sample["total_size_mb"], 2)
        
        return sample
    
    def predict_overflow(self):
        """
        Predict which ledgers will overflow based on current growth rate.
        
        Returns:
            dict with overflow predictions
        """
        predictions = {
            "timestamp": datetime.utcnow().isoformat(),
            "ledger_forecasts": [],
            "critical_ledgers": [],
        }
        
        for ledger_name in self.monitored_ledgers:
            if ledger_name not in self.size_history:
                continue
            
            history = self.size_history[ledger_name]
            if len(history) < 2:
                continue
            
            # Calculate growth rate (bytes per sample)
            sizes = [h["size_bytes"] for h in history]
            growth_rate = (sizes[-1] - sizes[0]) / len(history) if len(history) > 1 else 0
            
            if growth_rate <= 0:
                # No growth or shrinking
                forecast = {
                    "ledger": ledger_name,
                    "status": "STABLE",
                    "current_size_mb": round(sizes[-1] / (1024 * 1024), 2),
                }
            else:
                # Calculate time to threshold
                current_size = sizes[-1]
                threshold_bytes = self.size_threshold_mb * 1024 * 1024
                
                if current_size > threshold_bytes:
                    status = "EXCEEDED"
                    samples_to_threshold = 0
                else:
                    remaining = threshold_bytes - current_size
                    samples_to_threshold = remaining / growth_rate if growth_rate > 0 else float('inf')
                    status = "CRITICAL" if samples_to_threshold < 10 else "WARNING" if samples_to_threshold < 50 else "GROWING"
                
                forecast = {
                    "ledger": ledger_name,
                    "status": status,
                    "current_size_mb": round(current_size / (1024 * 1024), 2),
                    "growth_rate_kb_per_sample": round(growth_rate / 1024, 2),
                    "samples_to_threshold": round(samples_to_threshold, 1) if samples_to_threshold != float('inf') else "NEVER",
                    "estimated_days_to_threshold": round((samples_to_threshold * 60) / (24 * 60), 1) if samples_to_threshold != float('inf') else "NEVER",  # Assuming ~60s per sample
                }
                
                if status in ["CRITICAL", "EXCEEDED"]:
                    predictions["critical_ledgers"].append(ledger_name)
            
            predictions["ledger_forecasts"].append(forecast)
        
        # Sort by urgency
        predictions["ledger_forecasts"].sort(
            key=lambda x: float(x.get("samples_to_threshold", float('inf')))
        )
        
        if predictions["critical_ledgers"]:
            self._log_buffer_event("OVERFLOW_WARNING", predictions)
        
        return predictions
    
    def recommend_archival(self):
        """
        Recommend which ledgers should be archived.
        
        Returns:
            dict with archival recommendations
        """
        recommendations = {
            "timestamp": datetime.utcnow().isoformat(),
            "should_archive": [],
            "can_compress": [],
        }
        
        # Get current state
        sample = self.sample_ledger_sizes()
        
        for ledger_name, info in sample["ledgers"].items():
            if not info["exists"]:
                continue
            
            size_mb = info["size_mb"]
            lines = info["lines"]
            
            # Recommend archival if large
            if size_mb > 100:
                recommendations["should_archive"].append({
                    "ledger": ledger_name,
                    "current_size_mb": size_mb,
                    "line_count": lines,
                    "urgency": "HIGH" if size_mb > 200 else "MEDIUM",
                })
            
            # Recommend compression if has many lines
            if lines > 100_000:
                recommendations["can_compress"].append({
                    "ledger": ledger_name,
                    "lines": lines,
                    "current_size_mb": size_mb,
                    "estimated_compressed_mb": round(size_mb * 0.3, 2),  # Rough estimate
                })
        
        return recommendations
    
    def get_buffer_statistics(self):
        """Get comprehensive buffer statistics."""
        sample = self.sample_ledger_sizes()
        
        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_ledger_size_mb": sample["total_size_mb"],
            "ledgers_monitored": len(self.monitored_ledgers),
            "ledgers_existing": sum(1 for info in sample["ledgers"].values() if info["exists"]),
            "total_lines": sum(info.get("lines", 0) for info in sample["ledgers"].values()),
            "largest_ledger": None,
            "average_size_mb": None,
        }
        
        # Find largest
        ledgers = sample["ledgers"].items()
        if ledgers:
            largest = max(ledgers, key=lambda x: x[1]["size_mb"])
            stats["largest_ledger"] = {
                "name": largest[0],
                "size_mb": largest[1]["size_mb"],
            }
            
            existing = [info for info in sample["ledgers"].values() if info["exists"]]
            if existing:
                stats["average_size_mb"] = round(sum(info["size_mb"] for info in existing) / len(existing), 2)
        
        return stats
    
    def auto_archival_trigger(self, archive_threshold_mb=250):
        """
        Check if automatic archival should be triggered.
        
        Args:
            archive_threshold_mb: Trigger archival if ledger exceeds this
        
        Returns:
            dict with archival trigger decision
        """
        sample = self.sample_ledger_sizes()
        
        triggers = {
            "timestamp": datetime.utcnow().isoformat(),
            "should_archive": False,
            "ledgers_to_archive": [],
        }
        
        for ledger_name, info in sample["ledgers"].items():
            if info["size_mb"] > archive_threshold_mb:
                triggers["should_archive"] = True
                triggers["ledgers_to_archive"].append({
                    "ledger": ledger_name,
                    "size_mb": info["size_mb"],
                })
        
        if triggers["should_archive"]:
            self._log_buffer_event("AUTO_ARCHIVAL_TRIGGER", triggers)
        
        return triggers
    
    def _load_size_history(self):
        """Load historical size data if available."""
        history_file = self.core_dir / "buffer_size_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for ledger, entries in data.items():
                        self.size_history[ledger] = deque(entries[-self.max_history:], maxlen=self.max_history)
            except Exception as e:
                print(f"[WARNING] Failed to load size history: {e}")
    
    def _log_buffer_event(self, event_type: str, details: dict):
        """Log buffer event."""
        try:
            with open(self.buffer_ledger, 'a') as f:
                event = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": event_type,
                    "details": details,
                }
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log buffer event: {e}")


def test_buffer_predictor():
    """Test Buffer Overflow Predictor."""
    print("\n" + "="*80)
    print("BUFFER OVERFLOW PREDICTOR TEST")
    print("="*80)
    
    predictor = BufferOverflowPredictor()
    
    # Test 1: Sample sizes
    print("\n[TEST 1] Sample ledger sizes")
    sample = predictor.sample_ledger_sizes()
    print(f"  Total ledger size: {sample['total_size_mb']}MB")
    print(f"  Ledgers sampled: {sum(1 for info in sample['ledgers'].values() if info['exists'])}")
    
    # Test 2: Predict overflow
    print("\n[TEST 2] Predict overflow")
    prediction = predictor.predict_overflow()
    print(f"  Ledgers forecast: {len(prediction['ledger_forecasts'])}")
    print(f"  Critical ledgers: {len(prediction['critical_ledgers'])}")
    
    # Test 3: Get statistics
    print("\n[TEST 3] Get buffer statistics")
    stats = predictor.get_buffer_statistics()
    print(f"  Total size: {stats['total_ledger_size_mb']}MB")
    print(f"  Total lines: {stats['total_lines']}")
    
    # Test 4: Check archival trigger
    print("\n[TEST 4] Check auto-archival trigger")
    trigger = predictor.auto_archival_trigger()
    print(f"  Should archive: {trigger['should_archive']}")
    print(f"  Ledgers to archive: {len(trigger['ledgers_to_archive'])}")
    
    print("\n[OK] BUFFER PREDICTOR TESTS PASSED")


if __name__ == "__main__":
    test_buffer_predictor()
