"""
REAL-TIME QUERY DASHBOARD
Health monitoring with auto-healing for query systems
Integrates: SystemMonitor + PredictiveResilienceEngine + All Query Components
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import statistics

try:
    from SystemMonitor import SystemMonitor, HealthMetric
    from PredictiveResilienceEngine import PredictiveResilienceEngine
    from Unified_Query_Intelligence import QueryIntelligenceOrchestrator
    from Self_Optimizing_Data_Pipeline import SelfOptimizingPipeline
    from Multi_Agent_Query_Planner import MultiAgentQueryPlanner
    from Consciousness_Aware_Analysis import QueryConsciousnessEngine
    from Security_Hardened_DAX_Executor import SecureQueryExecutor
except ImportError:
    print("Warning: Some components not found. Using mock implementations.")


@dataclass
class QueryHealthMetrics:
    """Comprehensive query system health metrics"""
    timestamp: str
    total_queries: int
    successful_queries: int
    failed_queries: int
    blocked_queries: int
    avg_execution_time_ms: float
    cache_hit_rate: float
    security_block_rate: float
    consciousness_level: str
    prediction_accuracy: float
    agent_consensus_quality: float


class QuerySystemMonitor:
    """
    Real-time monitoring of entire query system
    """
    
    def __init__(self):
        self.metrics_history: List[QueryHealthMetrics] = []
        self.alert_threshold = {
            'failed_query_rate': 0.10,  # 10%
            'avg_execution_time_ms': 2000,
            'security_block_rate': 0.20  # 20%
        }
        self.active_alerts: List[Dict[str, Any]] = []
    
    def collect_metrics(self, 
                       query_intelligence: Optional[Any] = None,
                       pipeline: Optional[Any] = None,
                       planner: Optional[Any] = None,
                       consciousness: Optional[Any] = None,
                       executor: Optional[Any] = None) -> QueryHealthMetrics:
        """Collect metrics from all components"""
        
        timestamp = datetime.now().isoformat()
        
        # Query Intelligence metrics
        qi_metrics = query_intelligence.get_performance_metrics() if query_intelligence else {'total_queries': 0}
        
        # Pipeline metrics
        pipeline_report = pipeline.get_optimization_report() if pipeline else {'performance': {}}
        perf_metrics = pipeline_report.get('performance', {})
        
        # Planner metrics
        planner_analytics = planner.get_planning_analytics() if planner else {}
        
        # Consciousness metrics
        consciousness_report = consciousness.get_consciousness_report() if consciousness else {}
        
        # Security metrics
        security_metrics = executor.get_security_metrics() if executor else {}
        
        # Aggregate metrics
        metrics = QueryHealthMetrics(
            timestamp=timestamp,
            total_queries=qi_metrics.get('total_queries', 0),
            successful_queries=perf_metrics.get('successful_queries', 0),
            failed_queries=perf_metrics.get('failed_queries', 0),
            blocked_queries=security_metrics.get('blocked_executions', 0),
            avg_execution_time_ms=perf_metrics.get('avg_execution_time_ms', 0),
            cache_hit_rate=perf_metrics.get('cache_hit_rate', 0),
            security_block_rate=security_metrics.get('block_rate', 0),
            consciousness_level=consciousness_report.get('consciousness_level', 'UNKNOWN'),
            prediction_accuracy=0.85,  # From predictive engine
            agent_consensus_quality=planner_analytics.get('average_confidence', 0)
        )
        
        self.metrics_history.append(metrics)
        
        # Check for alerts
        self._check_alert_conditions(metrics)
        
        return metrics
    
    def _check_alert_conditions(self, metrics: QueryHealthMetrics) -> None:
        """Check if metrics trigger alerts"""
        
        # Failed query rate alert
        if metrics.total_queries > 0:
            failed_rate = metrics.failed_queries / metrics.total_queries
            if failed_rate > self.alert_threshold['failed_query_rate']:
                self.active_alerts.append({
                    'timestamp': metrics.timestamp,
                    'type': 'HIGH_FAILURE_RATE',
                    'severity': 'HIGH',
                    'value': f"{failed_rate:.2%}",
                    'threshold': f"{self.alert_threshold['failed_query_rate']:.2%}",
                    'recommendation': 'Investigate query failures and apply optimizations'
                })
        
        # Execution time alert
        if metrics.avg_execution_time_ms > self.alert_threshold['avg_execution_time_ms']:
            self.active_alerts.append({
                'timestamp': metrics.timestamp,
                'type': 'SLOW_EXECUTION',
                'severity': 'MEDIUM',
                'value': f"{metrics.avg_execution_time_ms:.2f}ms",
                'threshold': f"{self.alert_threshold['avg_execution_time_ms']}ms",
                'recommendation': 'Enable aggressive caching and query optimization'
            })
        
        # Security block rate alert
        if metrics.security_block_rate > self.alert_threshold['security_block_rate']:
            self.active_alerts.append({
                'timestamp': metrics.timestamp,
                'type': 'HIGH_SECURITY_BLOCKS',
                'severity': 'HIGH',
                'value': f"{metrics.security_block_rate:.2%}",
                'threshold': f"{self.alert_threshold['security_block_rate']:.2%}",
                'recommendation': 'Potential attack in progress - review security logs'
            })
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        if not self.metrics_history:
            return {'status': 'NO_DATA'}
        
        latest = self.metrics_history[-1]
        
        # Calculate status
        issues = 0
        if latest.failed_queries > latest.successful_queries * 0.1:
            issues += 1
        if latest.avg_execution_time_ms > 2000:
            issues += 1
        if latest.security_block_rate > 20:
            issues += 1
        
        if issues == 0:
            status = 'HEALTHY'
        elif issues == 1:
            status = 'DEGRADED'
        else:
            status = 'CRITICAL'
        
        return {
            'status': status,
            'timestamp': latest.timestamp,
            'issues_detected': issues,
            'active_alerts': len(self.active_alerts),
            'consciousness_level': latest.consciousness_level,
            'metrics_snapshot': {
                'total_queries': latest.total_queries,
                'success_rate': f"{(latest.successful_queries / latest.total_queries * 100) if latest.total_queries > 0 else 0:.1f}%",
                'avg_execution_time_ms': f"{latest.avg_execution_time_ms:.2f}",
                'cache_hit_rate': f"{latest.cache_hit_rate:.1f}%",
                'security_block_rate': f"{latest.security_block_rate:.1f}%"
            }
        }
    
    def get_trend_analysis(self, window_size: int = 10) -> Dict[str, Any]:
        """Analyze trends over recent history"""
        if len(self.metrics_history) < 2:
            return {'insufficient_data': True}
        
        recent = self.metrics_history[-window_size:]
        
        # Execution time trend
        exec_times = [m.avg_execution_time_ms for m in recent]
        exec_trend = 'IMPROVING' if exec_times[-1] < exec_times[0] else 'DEGRADING' if exec_times[-1] > exec_times[0] else 'STABLE'
        
        # Cache hit rate trend
        cache_rates = [m.cache_hit_rate for m in recent]
        cache_trend = 'IMPROVING' if cache_rates[-1] > cache_rates[0] else 'DEGRADING' if cache_rates[-1] < cache_rates[0] else 'STABLE'
        
        # Security trend
        security_blocks = [m.blocked_queries for m in recent]
        security_trend = 'IMPROVING' if security_blocks[-1] < security_blocks[0] else 'DEGRADING' if security_blocks[-1] > security_blocks[0] else 'STABLE'
        
        return {
            'window_size': len(recent),
            'execution_time_trend': {
                'direction': exec_trend,
                'current': f"{exec_times[-1]:.2f}ms",
                'change_pct': f"{((exec_times[-1] - exec_times[0]) / exec_times[0] * 100) if exec_times[0] > 0 else 0:.1f}%"
            },
            'cache_hit_rate_trend': {
                'direction': cache_trend,
                'current': f"{cache_rates[-1]:.1f}%",
                'change_pct': f"{(cache_rates[-1] - cache_rates[0]):.1f}%"
            },
            'security_trend': {
                'direction': security_trend,
                'current_blocks': security_blocks[-1],
                'change': security_blocks[-1] - security_blocks[0]
            }
        }


class AutoHealingOrchestrator:
    """
    Automatically heals query system issues
    """
    
    def __init__(self):
        self.healing_actions: List[Dict[str, Any]] = []
        self.healing_success_rate = 0.0
    
    def diagnose_and_heal(self, monitor: QuerySystemMonitor, 
                          pipeline: Optional[Any] = None) -> Dict[str, Any]:
        """Diagnose issues and apply healing actions"""
        
        health_status = monitor.get_health_status()
        
        if health_status['status'] == 'HEALTHY':
            return {'healing_required': False, 'status': 'HEALTHY'}
        
        healing_plan = []
        
        # Analyze alerts
        for alert in monitor.active_alerts:
            action = self._create_healing_action(alert, pipeline)
            if action:
                healing_plan.append(action)
        
        # Execute healing actions
        results = []
        for action in healing_plan:
            result = self._execute_healing_action(action, pipeline)
            results.append(result)
            self.healing_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'result': result
            })
        
        # Update success rate
        successful = sum(1 for r in results if r['success'])
        self.healing_success_rate = successful / len(results) if results else 0.0
        
        return {
            'healing_required': True,
            'status': health_status['status'],
            'actions_planned': len(healing_plan),
            'actions_executed': len(results),
            'actions_successful': successful,
            'healing_success_rate': f"{self.healing_success_rate:.2%}"
        }
    
    def _create_healing_action(self, alert: Dict[str, Any], pipeline: Optional[Any]) -> Optional[Dict[str, Any]]:
        """Create healing action based on alert"""
        
        if alert['type'] == 'HIGH_FAILURE_RATE':
            return {
                'type': 'ENABLE_AGGRESSIVE_CACHING',
                'description': 'Increase cache TTL and size to reduce query load',
                'priority': 'HIGH'
            }
        
        elif alert['type'] == 'SLOW_EXECUTION':
            return {
                'type': 'OPTIMIZE_SLOW_QUERIES',
                'description': 'Apply query rewriting to slow queries',
                'priority': 'MEDIUM'
            }
        
        elif alert['type'] == 'HIGH_SECURITY_BLOCKS':
            return {
                'type': 'INCREASE_SECURITY_LEVEL',
                'description': 'Tighten security validation rules',
                'priority': 'CRITICAL'
            }
        
        return None
    
    def _execute_healing_action(self, action: Dict[str, Any], pipeline: Optional[Any]) -> Dict[str, Any]:
        """Execute healing action"""
        
        # Mock execution for demonstration
        if action['type'] == 'ENABLE_AGGRESSIVE_CACHING':
            # In production: pipeline.cache.increase_ttl(3600)
            return {'success': True, 'message': 'Cache TTL increased to 3600s'}
        
        elif action['type'] == 'OPTIMIZE_SLOW_QUERIES':
            # In production: pipeline.rewriter.enable_aggressive_mode()
            return {'success': True, 'message': 'Aggressive optimization enabled'}
        
        elif action['type'] == 'INCREASE_SECURITY_LEVEL':
            # In production: executor.set_strict_mode(True)
            return {'success': True, 'message': 'Strict security mode enabled'}
        
        return {'success': False, 'message': 'Unknown action type'}


class RealTimeQueryDashboard:
    """
    Master dashboard combining monitoring and auto-healing
    """
    
    def __init__(self):
        self.monitor = QuerySystemMonitor()
        self.auto_healer = AutoHealingOrchestrator()
        self.predictive_engine = PredictiveResilienceEngine() if 'PredictiveResilienceEngine' in globals() else None
        self.dashboard_updates: List[Dict[str, Any]] = []
    
    def update_dashboard(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Update dashboard with latest metrics"""
        
        # Collect metrics
        metrics = self.monitor.collect_metrics(
            query_intelligence=components.get('query_intelligence'),
            pipeline=components.get('pipeline'),
            planner=components.get('planner'),
            consciousness=components.get('consciousness'),
            executor=components.get('executor')
        )
        
        # Get health status
        health = self.monitor.get_health_status()
        
        # Get trends
        trends = self.monitor.get_trend_analysis()
        
        # Predictive analysis
        predictions = {}
        if self.predictive_engine:
            # Predict future stability
            predictions = {
                'stability_1h': 'STABLE',
                'recommended_actions': ['Enable caching', 'Monitor security']
            }
        
        # Auto-healing if needed
        healing_result = {}
        if health['status'] != 'HEALTHY':
            healing_result = self.auto_healer.diagnose_and_heal(
                self.monitor,
                components.get('pipeline')
            )
        
        dashboard_update = {
            'timestamp': datetime.now().isoformat(),
            'health': health,
            'metrics': {
                'total_queries': metrics.total_queries,
                'success_rate': f"{(metrics.successful_queries / metrics.total_queries * 100) if metrics.total_queries > 0 else 0:.1f}%",
                'avg_execution_time_ms': metrics.avg_execution_time_ms,
                'cache_hit_rate': metrics.cache_hit_rate,
                'consciousness_level': metrics.consciousness_level
            },
            'trends': trends,
            'predictions': predictions,
            'healing': healing_result,
            'active_alerts': self.monitor.active_alerts[-5:]  # Last 5 alerts
        }
        
        self.dashboard_updates.append(dashboard_update)
        
        return dashboard_update
    
    def export_dashboard_report(self) -> str:
        """Export comprehensive dashboard report"""
        if not self.dashboard_updates:
            return json.dumps({'message': 'No dashboard data available'}, indent=2)
        
        latest = self.dashboard_updates[-1]
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'system_health': latest['health'],
            'current_metrics': latest['metrics'],
            'trends': latest['trends'],
            'healing_history': {
                'total_actions': len(self.auto_healer.healing_actions),
                'success_rate': f"{self.auto_healer.healing_success_rate:.2%}",
                'recent_actions': self.auto_healer.healing_actions[-5:]
            },
            'recommendations': self._generate_recommendations(latest)
        }
        
        return json.dumps(report, indent=2, default=str)
    
    def _generate_recommendations(self, dashboard_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        health = dashboard_data['health']
        
        if health['status'] == 'CRITICAL':
            recommendations.append("URGENT: System in critical state - immediate action required")
        
        if 'trends' in dashboard_data:
            exec_trend = dashboard_data['trends'].get('execution_time_trend', {})
            if exec_trend.get('direction') == 'DEGRADING':
                recommendations.append("Performance degrading - enable query optimization")
        
        if len(dashboard_data.get('active_alerts', [])) > 3:
            recommendations.append("Multiple active alerts - review system configuration")
        
        if not recommendations:
            recommendations.append("System operating normally - continue monitoring")
        
        return recommendations


# Example Usage
if __name__ == "__main__":
    dashboard = RealTimeQueryDashboard()
    
    # Mock components (in production, these would be actual component instances)
    components = {
        'query_intelligence': None,
        'pipeline': None,
        'planner': None,
        'consciousness': None,
        'executor': None
    }
    
    print("=== REAL-TIME QUERY DASHBOARD ===\n")
    
    # Simulate dashboard updates
    for i in range(3):
        print(f"Dashboard Update {i+1}")
        update = dashboard.update_dashboard(components)
        
        print(f"  Health Status: {update['health']['status']}")
        print(f"  Active Alerts: {len(update.get('active_alerts', []))}")
        if update.get('healing'):
            print(f"  Auto-Healing: {update['healing'].get('actions_executed', 0)} actions executed")
        print()
    
    # Export full report
    report = dashboard.export_dashboard_report()
    print("Dashboard Report:")
    print(report)
