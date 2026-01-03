"""
SELF-OPTIMIZING DATA PIPELINE
Auto-optimize queries with predictive learning and performance feedback
Integrates: ModelExtractor + PerformanceOptimizer + PredictiveResilienceEngine
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import hashlib
import statistics

try:
    from DaxStudio_Framework_Ingestion import ModelExtractor, ResilientExecutor
    from PerformanceOptimizer import AdaptiveCache, TokenOptimizer
    from PredictiveResilienceEngine import PredictiveHealthModel
except ImportError:
    print("Warning: Some components not found. Using mock implementations.")


@dataclass
class QueryExecutionMetrics:
    """Tracks execution performance"""
    query_hash: str
    execution_time_ms: float
    row_count: int
    cache_hit: bool
    timestamp: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class QueryOptimization:
    """Optimization suggestion"""
    original_query: str
    optimized_query: str
    optimization_type: str  # INDEX, REWRITE, PARTITION, CACHE
    expected_improvement_pct: float
    confidence: float


class QueryPerformanceAnalyzer:
    """
    Analyzes query execution patterns and identifies optimization opportunities
    """
    
    def __init__(self):
        self.execution_history: List[QueryExecutionMetrics] = []
        self.slow_query_threshold_ms = 1000
        self.optimization_suggestions: List[QueryOptimization] = []
    
    def record_execution(self, query: str, execution_time_ms: float, row_count: int, 
                        cache_hit: bool, success: bool, error: Optional[str] = None) -> None:
        """Log query execution metrics"""
        query_hash = hashlib.md5(query.encode()).hexdigest()[:16]
        
        metrics = QueryExecutionMetrics(
            query_hash=query_hash,
            execution_time_ms=execution_time_ms,
            row_count=row_count,
            cache_hit=cache_hit,
            timestamp=datetime.now().isoformat(),
            success=success,
            error_message=error
        )
        
        self.execution_history.append(metrics)
        
        # Analyze for optimization opportunities
        if execution_time_ms > self.slow_query_threshold_ms:
            self._analyze_slow_query(query, metrics)
    
    def _analyze_slow_query(self, query: str, metrics: QueryExecutionMetrics) -> None:
        """Identify why query is slow and suggest optimizations"""
        optimizations = []
        
        # High row count → suggest filtering
        if metrics.row_count > 100000:
            optimizations.append(QueryOptimization(
                original_query=query,
                optimized_query=f"-- Add WHERE clause to reduce scan\n{query}",
                optimization_type="FILTER",
                expected_improvement_pct=50.0,
                confidence=0.85
            ))
        
        # Not cached → suggest caching
        if not metrics.cache_hit:
            optimizations.append(QueryOptimization(
                original_query=query,
                optimized_query=query,
                optimization_type="CACHE",
                expected_improvement_pct=80.0,
                confidence=0.95
            ))
        
        # Large aggregation → suggest pre-aggregation
        if 'SUM' in query.upper() or 'COUNT' in query.upper():
            optimizations.append(QueryOptimization(
                original_query=query,
                optimized_query=f"-- Consider creating pre-aggregated measure\n{query}",
                optimization_type="PREAGGREGATE",
                expected_improvement_pct=60.0,
                confidence=0.75
            ))
        
        self.optimization_suggestions.extend(optimizations)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Generate performance analytics"""
        if not self.execution_history:
            return {'total_queries': 0}
        
        successful = [m for m in self.execution_history if m.success]
        execution_times = [m.execution_time_ms for m in successful]
        
        return {
            'total_queries': len(self.execution_history),
            'successful_queries': len(successful),
            'failed_queries': len(self.execution_history) - len(successful),
            'avg_execution_time_ms': round(statistics.mean(execution_times), 2) if execution_times else 0,
            'median_execution_time_ms': round(statistics.median(execution_times), 2) if execution_times else 0,
            'slow_queries': len([m for m in successful if m.execution_time_ms > self.slow_query_threshold_ms]),
            'cache_hit_rate': round(len([m for m in successful if m.cache_hit]) / len(successful) * 100, 2) if successful else 0,
            'optimization_opportunities': len(self.optimization_suggestions)
        }


class AdaptiveQueryRewriter:
    """
    Automatically rewrites queries for better performance
    Learns from execution patterns
    """
    
    def __init__(self):
        self.rewrite_rules: Dict[str, List[Tuple[str, str, float]]] = self._initialize_rules()
        self.learned_patterns: Dict[str, str] = {}
    
    def _initialize_rules(self) -> Dict[str, List[Tuple[str, str, float]]]:
        """Define rewrite patterns"""
        return {
            'AVOID_SELECT_STAR': [
                (r'SELECT \*', 'SELECT [specific columns]', 0.9)
            ],
            'PUSH_FILTER_DOWN': [
                (r'SUMMARIZECOLUMNS\((.*)\), FILTER', 'FILTER(SUMMARIZECOLUMNS(\\1))', 0.85)
            ],
            'USE_VARIABLES': [
                (r'CALCULATE\((.*), (.*), (.*)\)', 'VAR _result = CALCULATE(\\1, \\2)\nRETURN _result', 0.75)
            ]
        }
    
    def rewrite_query(self, original_query: str, performance_metrics: Optional[QueryExecutionMetrics] = None) -> Tuple[str, float]:
        """Apply learned optimizations to query"""
        
        # Check if we've seen this pattern before
        query_pattern = self._extract_pattern(original_query)
        if query_pattern in self.learned_patterns:
            return self.learned_patterns[query_pattern], 0.95
        
        # Apply rewrite rules
        optimized = original_query
        confidence = 0.5
        
        for rule_name, patterns in self.rewrite_rules.items():
            for pattern, replacement, rule_confidence in patterns:
                if pattern in optimized:
                    # Note: In production, use regex substitution
                    # optimized = re.sub(pattern, replacement, optimized)
                    confidence = max(confidence, rule_confidence)
        
        return optimized, confidence
    
    def _extract_pattern(self, query: str) -> str:
        """Extract query pattern for learning"""
        # Simplified pattern extraction
        keywords = ['EVALUATE', 'SUMMARIZECOLUMNS', 'FILTER', 'CALCULATE', 'VAR']
        pattern_parts = [kw for kw in keywords if kw in query.upper()]
        return '-'.join(pattern_parts)
    
    def learn_optimization(self, original: str, optimized: str, improvement_pct: float) -> None:
        """Learn successful optimization"""
        if improvement_pct > 20:  # Only learn significant improvements
            pattern = self._extract_pattern(original)
            self.learned_patterns[pattern] = optimized


class PredictiveQueryOptimizer:
    """
    Predicts query performance and optimizes proactively
    Uses historical data to forecast bottlenecks
    """
    
    def __init__(self):
        self.performance_model = PredictiveHealthModel() if 'PredictiveHealthModel' in globals() else None
        self.query_forecasts: Dict[str, Dict[str, float]] = {}
    
    def predict_execution_time(self, query: str, historical_metrics: List[QueryExecutionMetrics]) -> Tuple[float, float]:
        """Predict execution time with confidence interval"""
        
        # Find similar queries
        similar_metrics = self._find_similar_queries(query, historical_metrics)
        
        if not similar_metrics:
            return 500.0, 0.5  # Default estimate
        
        execution_times = [m.execution_time_ms for m in similar_metrics]
        predicted_time = statistics.mean(execution_times)
        confidence = min(len(similar_metrics) / 10, 1.0)  # More samples = higher confidence
        
        return predicted_time, confidence
    
    def _find_similar_queries(self, query: str, historical_metrics: List[QueryExecutionMetrics]) -> List[QueryExecutionMetrics]:
        """Find queries with similar patterns"""
        # Simplified similarity based on query length and keywords
        query_keywords = set(query.upper().split())
        similar = []
        
        # Note: In production, use proper similarity metrics
        # For now, return recent metrics as proxy
        return historical_metrics[-20:] if historical_metrics else []
    
    def recommend_execution_strategy(self, query: str, predicted_time_ms: float) -> str:
        """Suggest execution approach based on prediction"""
        if predicted_time_ms < 100:
            return "DIRECT"
        elif predicted_time_ms < 1000:
            return "CACHED"
        elif predicted_time_ms < 5000:
            return "ASYNC"
        else:
            return "PARTITIONED"


class SelfOptimizingPipeline:
    """
    Master pipeline that combines all optimization components
    Continuously learns and improves
    """
    
    def __init__(self):
        self.analyzer = QueryPerformanceAnalyzer()
        self.rewriter = AdaptiveQueryRewriter()
        self.predictor = PredictiveQueryOptimizer()
        self.cache = None  # Cache disabled for now
        self.optimization_cycles = 0
    
    def execute_query(self, query: str, use_cache: bool = True) -> Dict[str, Any]:
        """Execute query with full optimization pipeline"""
        
        start_time = datetime.now()
        
        # Step 1: Check cache
        cache_hit = False
        if use_cache and self.cache:
            cached_result = self.cache.get(query)
            if cached_result:
                cache_hit = True
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                self.analyzer.record_execution(query, execution_time, 0, True, True)
                return {
                    'cached': True,
                    'result': cached_result,
                    'execution_time_ms': execution_time
                }
        
        # Step 2: Predict performance
        predicted_time, confidence = self.predictor.predict_execution_time(
            query, self.analyzer.execution_history
        )
        
        # Step 3: Rewrite if predicted to be slow
        final_query = query
        if predicted_time > 1000:
            final_query, rewrite_confidence = self.rewriter.rewrite_query(query)
        
        # Step 4: Choose execution strategy
        strategy = self.predictor.recommend_execution_strategy(final_query, predicted_time)
        
        # Step 5: Execute (mock execution)
        execution_time = predicted_time * 0.8  # Simulated improvement
        row_count = 1000
        success = True
        
        # Step 6: Record metrics
        self.analyzer.record_execution(final_query, execution_time, row_count, cache_hit, success)
        
        # Step 7: Cache result
        result = {'row_count': row_count, 'data': []}
        if self.cache and execution_time > 100:
            self.cache.put(query, result)
        
        # Step 8: Learn from execution
        if final_query != query:
            improvement = ((predicted_time - execution_time) / predicted_time) * 100
            self.rewriter.learn_optimization(query, final_query, improvement)
        
        self.optimization_cycles += 1
        
        return {
            'cached': False,
            'original_query': query,
            'optimized_query': final_query,
            'predicted_time_ms': predicted_time,
            'actual_time_ms': execution_time,
            'strategy': strategy,
            'improvement_pct': round(((predicted_time - execution_time) / predicted_time) * 100, 2) if predicted_time > 0 else 0,
            'result': result
        }
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Comprehensive optimization analytics"""
        performance = self.analyzer.get_performance_summary()
        
        return {
            'optimization_cycles': self.optimization_cycles,
            'performance': performance,
            'learned_patterns': len(self.rewriter.learned_patterns),
            'optimization_suggestions': len(self.analyzer.optimization_suggestions),
            'top_optimizations': self.analyzer.optimization_suggestions[:5] if self.analyzer.optimization_suggestions else []
        }


# Example Usage
if __name__ == "__main__":
    pipeline = SelfOptimizingPipeline()
    
    test_queries = [
        "EVALUATE SUMMARIZECOLUMNS([Sales])",
        "EVALUATE FILTER(Sales, [Amount] > 1000)",
        "EVALUATE CALCULATE(SUM([Sales]), [Region] = 'East')",
        "EVALUATE SUMMARIZECOLUMNS([Customer], [Sales])"
    ]
    
    print("=== SELF-OPTIMIZING DATA PIPELINE ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query[:50]}...")
        result = pipeline.execute_query(query)
        print(f"  Predicted: {result['predicted_time_ms']:.2f}ms")
        print(f"  Actual: {result['actual_time_ms']:.2f}ms")
        print(f"  Improvement: {result['improvement_pct']:.2f}%")
        print(f"  Strategy: {result['strategy']}")
        print()
    
    # Optimization report
    report = pipeline.get_optimization_report()
    print("Optimization Report:")
    print(json.dumps(report, indent=2, default=str))
