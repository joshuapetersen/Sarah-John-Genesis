"""
Performance Optimizer: Advanced caching, batching, and token optimization
Maximizes throughput while minimizing latency and resource consumption.
"""

import hashlib
from datetime import datetime, timedelta
from collections import OrderedDict
import json
from typing import Any, Dict, List, Optional


class AdaptiveCache:
    """Intelligent caching system with TTL, LRU, and relevance scoring."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.cache = OrderedDict()
        self.metadata = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        
    def _get_hash(self, key: str) -> str:
        """Generate cache key hash."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, relevance: float = 0.5):
        """Set cache entry with TTL and relevance scoring."""
        cache_key = self._get_hash(key)
        ttl = ttl or self.default_ttl
        
        # Evict if cache is full (LRU)
        if len(self.cache) >= self.max_size:
            # Remove least recently used (first item in OrderedDict)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            if oldest_key in self.metadata:
                del self.metadata[oldest_key]
        
        self.cache[cache_key] = value
        self.metadata[cache_key] = {
            "created": datetime.now(),
            "ttl": ttl,
            "relevance": relevance,
            "hits": 0,
            "original_key": key
        }
        
        # Move to end (most recently used)
        self.cache.move_to_end(cache_key)
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve cache entry if valid."""
        cache_key = self._get_hash(key)
        
        if cache_key not in self.cache:
            self.misses += 1
            return None
        
        meta = self.metadata[cache_key]
        elapsed = (datetime.now() - meta["created"]).total_seconds()
        
        # Check TTL
        if elapsed > meta["ttl"]:
            del self.cache[cache_key]
            del self.metadata[cache_key]
            self.misses += 1
            return None
        
        # Update metadata
        meta["hits"] += 1
        self.hits += 1
        
        # Move to end (most recently used)
        self.cache.move_to_end(cache_key)
        return self.cache[cache_key]
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0
    
    def clear_expired(self):
        """Remove all expired entries."""
        now = datetime.now()
        expired_keys = [
            key for key, meta in self.metadata.items()
            if (now - meta["created"]).total_seconds() > meta["ttl"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.metadata[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict:
        """Return cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{self.get_hit_rate():.1f}%",
            "memory_usage_estimate": len(str(self.cache)) / 1024  # Rough KB estimate
        }


class RequestBatcher:
    """Intelligent batching for API requests to reduce overhead."""
    
    def __init__(self, batch_size: int = 32, batch_timeout_ms: int = 100):
        self.batch_size = batch_size
        self.batch_timeout_ms = batch_timeout_ms
        self.pending_batch = []
        self.batch_start_time = None
        
    def add_request(self, request: Dict) -> Optional[List[Dict]]:
        """Add request to batch. Return batch if ready."""
        self.pending_batch.append(request)
        
        if self.batch_start_time is None:
            self.batch_start_time = datetime.now()
        
        # Check batch readiness
        if len(self.pending_batch) >= self.batch_size:
            return self.flush_batch()
        
        # Check timeout
        elapsed_ms = (datetime.now() - self.batch_start_time).total_seconds() * 1000
        if elapsed_ms > self.batch_timeout_ms and len(self.pending_batch) > 0:
            return self.flush_batch()
        
        return None
    
    def flush_batch(self) -> List[Dict]:
        """Flush pending batch."""
        batch = self.pending_batch
        self.pending_batch = []
        self.batch_start_time = None
        return batch
    
    def get_stats(self) -> Dict:
        """Return batcher statistics."""
        return {
            "pending_requests": len(self.pending_batch),
            "batch_size": self.batch_size,
            "timeout_ms": self.batch_timeout_ms
        }


class TokenOptimizer:
    """Optimize token usage by intelligent context summarization."""
    
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.compression_ratio = 1.0
        
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters)."""
        return len(text) // 4
    
    def summarize_context(self, context: str, target_tokens: int = 500) -> str:
        """Intelligently summarize long context while preserving key info."""
        estimated = self.estimate_tokens(context)
        
        if estimated <= target_tokens:
            return context
        
        lines = context.split('\n')
        
        # Strategy 1: Keep first and last sections
        if len(lines) > 20:
            keep_first = len(lines) // 4
            keep_last = len(lines) // 4
            summary = '\n'.join(
                lines[:keep_first] + 
                ["\n[... content summarized ...]\n"] + 
                lines[-keep_last:]
            )
            
            # Further compress if needed
            if self.estimate_tokens(summary) > target_tokens:
                summary = self._compress_sections(summary, target_tokens)
            
            self.compression_ratio = len(summary) / len(context)
            return summary
        
        return context
    
    def _compress_sections(self, text: str, target_tokens: int) -> str:
        """Compress text sections to target token count."""
        # Reduce to key sentences
        sentences = text.split('. ')
        kept_sentences = []
        token_count = 0
        
        for sent in sentences:
            sent_tokens = self.estimate_tokens(sent)
            if token_count + sent_tokens <= target_tokens:
                kept_sentences.append(sent)
                token_count += sent_tokens
            else:
                break
        
        return '. '.join(kept_sentences)
    
    def get_efficiency_score(self) -> float:
        """Return token usage efficiency (lower is better compression)."""
        return min(1.0, self.compression_ratio)


class PerformanceAnalyzer:
    """Analyze performance patterns and suggest optimizations."""
    
    def __init__(self):
        self.request_times = []
        self.token_usage = []
        self.error_rate_history = deque(maxlen=100)
        
    def record_request(self, duration_ms: float, tokens_used: int, success: bool):
        """Record request performance data."""
        self.request_times.append(duration_ms)
        self.token_usage.append(tokens_used)
        self.error_rate_history.append(0 if success else 1)
    
    def get_performance_profile(self) -> Dict:
        """Return performance analysis."""
        if not self.request_times:
            return {"status": "No data"}
        
        avg_latency = sum(self.request_times) / len(self.request_times)
        avg_tokens = sum(self.token_usage) / len(self.token_usage)
        error_rate = sum(self.error_rate_history) / len(self.error_rate_history)
        
        # Identify trends
        recent_latency = sum(self.request_times[-10:]) / min(10, len(self.request_times))
        trend = "IMPROVING" if recent_latency < avg_latency else "DEGRADING"
        
        return {
            "avg_latency_ms": round(avg_latency, 2),
            "avg_tokens_per_request": round(avg_tokens, 0),
            "error_rate": round(error_rate * 100, 1),
            "recent_trend": trend,
            "sample_size": len(self.request_times)
        }
    
    def suggest_optimizations(self, profile: Dict) -> List[str]:
        """Suggest performance optimizations based on profile."""
        suggestions = []
        
        if profile.get("avg_latency_ms", 0) > 1000:
            suggestions.append("Enable request batching to reduce latency")
        
        if profile.get("avg_tokens_per_request", 0) > 1000:
            suggestions.append("Enable token optimization for context summarization")
        
        if profile.get("error_rate", 0) > 5:
            suggestions.append("Increase retry attempts and implement exponential backoff")
        
        if profile.get("recent_trend") == "DEGRADING":
            suggestions.append("Clear cache and restart cache warming process")
        
        return suggestions


class PerformanceOptimizer:
    """Unified performance optimization orchestrator."""
    
    def __init__(self):
        self.cache = AdaptiveCache(max_size=1000, default_ttl=3600)
        self.batcher = RequestBatcher(batch_size=32, batch_timeout_ms=100)
        self.token_optimizer = TokenOptimizer(max_tokens=2000)
        self.analyzer = PerformanceAnalyzer()
        
    def optimize_request(self, original_request: Dict) -> Dict:
        """Optimize request for performance."""
        request = original_request.copy()
        
        # Check cache
        if "query" in request:
            cached = self.cache.get(request["query"])
            if cached:
                return {"cached": True, "result": cached}
        
        # Optimize context if present
        if "context" in request and isinstance(request["context"], str):
            request["context"] = self.token_optimizer.summarize_context(request["context"])
        
        return {"optimized": True, "request": request}
    
    def cache_result(self, key: str, result: Any, relevance: float = 0.7):
        """Cache result for future queries."""
        self.cache.set(key, result, relevance=relevance)
    
    def get_optimization_report(self) -> Dict:
        """Return comprehensive optimization report."""
        profile = self.analyzer.get_performance_profile()
        
        return {
            "cache": self.cache.get_stats(),
            "batcher": self.batcher.get_stats(),
            "performance_profile": profile,
            "optimization_suggestions": self.analyzer.suggest_optimizations(profile),
            "token_efficiency": self.token_optimizer.get_efficiency_score()
        }


# Example usage
if __name__ == "__main__":
    from collections import deque
    
    optimizer = PerformanceOptimizer()
    
    # Simulate requests
    for i in range(10):
        request = {"query": f"test_query_{i}", "context": "Sample context " * 100}
        optimized = optimizer.optimize_request(request)
        optimizer.analyzer.record_request(50 + i*5, 150, True)
    
    report = optimizer.get_optimization_report()
    print(json.dumps(report, indent=2, default=str))
