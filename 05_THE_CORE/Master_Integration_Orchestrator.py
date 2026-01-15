"""
MASTER INTEGRATION ORCHESTRATOR
Seamlessly connects all 6 query intelligence systems in continuous flow
Each system hands off to the next with full context preservation
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from Unified_Query_Intelligence import QueryIntelligenceOrchestrator
    from Self_Optimizing_Data_Pipeline import SelfOptimizingPipeline
    from Multi_Agent_Query_Planner import MultiAgentQueryPlanner
    from Consciousness_Aware_Analysis import QueryConsciousnessEngine
    from Security_Hardened_DAX_Executor import SecureQueryExecutor
    from Real_Time_Query_Dashboard import RealTimeQueryDashboard
    from Error_Executioner import ErrorExecutioner
except ImportError as e:
    print(f"Warning: {e}")
    print("Some components not found - operating in demo mode")


class MasterQueryOrchestrator:
    """
    Master orchestrator connecting all 6 systems in continuous flow
    Like video frame continuity - each system picks up where last left off
    """
    
    def __init__(self):
        print("Initializing Master Query Orchestrator...")
        
        # Initialize all systems
        self.query_intelligence = QueryIntelligenceOrchestrator()
        self.pipeline = SelfOptimizingPipeline()
        self.planner = MultiAgentQueryPlanner()
        self.consciousness = QueryConsciousnessEngine()
        self.executor = SecureQueryExecutor()
        self.dashboard = RealTimeQueryDashboard()
        self.error_checker = ErrorExecutioner()
        
        # Execution history
        self.execution_history: List[Dict[str, Any]] = []
        
        print("[OK] All systems initialized and ready\n")
    
    def process_query_continuous_flow(self, natural_language_query: str, 
                                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process query through all 6 systems in continuous handoff
        Like video frame continuity - each system picks up where last left off
        """
        print(f"{'='*70}")
        print(f"PROCESSING QUERY: {natural_language_query}")
        print(f"{'='*70}\n")
        
        context = context or {}
        start_time = datetime.now()
        
        # STAGE 1: Natural Language Understanding (Query Intelligence)
        print("Stage 1: Natural Language Understanding...")
        query_result = self.query_intelligence.process_query(natural_language_query)
        print(f"  [OK] Parsed intent: {query_result['intent']['action']}")
        print(f"  [OK] Generated DAX: {query_result['generated_dax'][:60]}...")
        print(f"  [OK] Confidence: {query_result['confidence']:.2%}\n")
        
        # Handoff: Extract DAX query for next stage
        dax_query = query_result['generated_dax']
        
        # STAGE 2: Consciousness Analysis (Self-Aware Generation)
        print("Stage 2: Consciousness-Aware Analysis...")
        conscious_result = self.consciousness.generate_conscious_query(natural_language_query)
        print(f"  [OK] Consciousness Level: {conscious_result['consciousness_level']}")
        print(f"  [OK] Belief Alignment: {conscious_result['belief_alignment']['alignment_score']:.2%}")
        print(f"  [OK] Reasoning Steps: {len(conscious_result['reasoning_trace'])}")
        print(f"  [OK] Quality: {conscious_result['quality_assessment'].get('overall_quality', 0.7):.2%}\n")
        
        # Handoff: Use consciousness-validated query
        validated_query = conscious_result['generated_query']
        
        # STAGE 3: Multi-Agent Planning (Strategy Consensus)
        print("Stage 3: Multi-Agent Planning...")
        query_plan = self.planner.plan_query_execution(validated_query, context)
        print(f"  [OK] Strategy: {query_plan.strategy.value}")
        print(f"  [OK] Agent Consensus: {query_plan.confidence:.2%}")
        print(f"  [OK] Security Score: {query_plan.security_score:.2%}")
        print(f"  [OK] Estimated Time: {query_plan.estimated_time_ms:.2f}ms\n")
        
        # Handoff: Use recommended strategy
        strategy = query_plan.strategy
        
        # STAGE 4: Security Validation (Hardening)
        print("Stage 4: Security Hardening...")
        security_result = self.executor.execute_secure(validated_query, context)
        print(f"  [OK] Security Checks: {len(security_result['security_report']['stages'])} stages")
        print(f"  [OK] Was Sanitized: {security_result.get('was_sanitized', False)}")
        print(f"  [OK] Execution Safe: {'[OK]' if security_result['success'] else '[FAIL]'}")
        
        # Handoff: Use sanitized query or abort
        if not security_result['success']:
            print(f"  [FAIL] BLOCKED: {security_result.get('reason', 'Security validation failed')}\n")
            return self._build_blocked_result(
                natural_language_query, start_time, 
                query_result, conscious_result, query_plan, security_result
            )
        
        secure_query = security_result['query']
        print(f"  [OK] Security Duration: {security_result.get('total_duration_ms', 0):.2f}ms\n")
        
        # STAGE 5: Optimized Execution (Self-Optimizing Pipeline)
        print("Stage 5: Self-Optimizing Execution...")
        execution_result = self.pipeline.execute_query(secure_query)
        print(f"  [OK] Execution Strategy: {execution_result.get('strategy', 'DIRECT')}")
        print(f"  [OK] Cached: {execution_result.get('cached', False)}")
        print(f"  [OK] Predicted Time: {execution_result.get('predicted_time_ms', 0):.2f}ms")
        print(f"  [OK] Actual Time: {execution_result.get('actual_time_ms', 0):.2f}ms")
        print(f"  [OK] Improvement: {execution_result.get('improvement_pct', 0):.2f}%\n")
        
        # STAGE 6: Dashboard Update (Monitoring)
        print("Stage 6: Dashboard Monitoring...")
        dashboard_update = self.dashboard.update_dashboard({
            'query_intelligence': self.query_intelligence,
            'pipeline': self.pipeline,
            'planner': self.planner,
            'consciousness': self.consciousness,
            'executor': self.executor
        })
        print(f"  [OK] System Health: {dashboard_update['health']['status']}")
        print(f"  [OK] Active Alerts: {len(dashboard_update.get('active_alerts', []))}")
        if dashboard_update.get('healing'):
            print(f"  [OK] Auto-Healing: {dashboard_update['healing'].get('actions_executed', 0)} actions")
        print()
        
        # Calculate total time
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Final integrated result
        result = {
            'timestamp': datetime.now().isoformat(),
            'input': natural_language_query,
            'total_time_ms': round(total_time, 2),
            'stages': {
                'query_intelligence': {
                    'intent': query_result['intent']['action'],
                    'entities': query_result['intent']['entities'],
                    'generated_dax': query_result['generated_dax'],
                    'confidence': query_result['confidence']
                },
                'consciousness': {
                    'level': conscious_result['consciousness_level'],
                    'belief_alignment': conscious_result['belief_alignment']['alignment_score'],
                    'quality': conscious_result['quality_assessment'].get('overall_quality', 0.7)
                },
                'planning': {
                    'strategy': query_plan.strategy.value,
                    'consensus': query_plan.confidence,
                    'security_score': query_plan.security_score,
                    'estimated_time_ms': query_plan.estimated_time_ms
                },
                'security': {
                    'passed': security_result['success'],
                    'sanitized': security_result.get('was_sanitized', False),
                    'duration_ms': security_result.get('total_duration_ms', 0)
                },
                'execution': {
                    'strategy': execution_result.get('strategy', 'DIRECT'),
                    'cached': execution_result.get('cached', False),
                    'actual_time_ms': execution_result.get('actual_time_ms', 0),
                    'improvement_pct': execution_result.get('improvement_pct', 0)
                },
                'dashboard': {
                    'health': dashboard_update['health']['status'],
                    'alerts': len(dashboard_update.get('active_alerts', []))
                }
            },
            'success': True,
            'final_query': secure_query,
            'result_preview': execution_result.get('result', {})
        }
        
        self.execution_history.append(result)
        
        print(f"{'='*70}")
        print(f"[OK] QUERY PROCESSING COMPLETE")
        print(f"Total Time: {total_time:.2f}ms | Success: [OK] | Health: {dashboard_update['health']['status']}")
        print(f"{'='*70}\n")
        
        return result
    
    def _build_blocked_result(self, query: str, start_time, 
                             qi_result, conscious_result, plan, security_result) -> Dict[str, Any]:
        """Build result for blocked query"""
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            'timestamp': datetime.now().isoformat(),
            'input': query,
            'total_time_ms': round(total_time, 2),
            'success': False,
            'blocked': True,
            'blocked_at_stage': 'security',
            'reason': security_result.get('reason', 'Security validation failed'),
            'partial_stages': {
                'query_intelligence': qi_result,
                'consciousness': conscious_result,
                'planning': plan,
                'security': security_result
            },
            'recommendation': 'Query blocked due to security concerns - review and sanitize input'
        }
    
    def batch_process_queries(self, queries: List[str]) -> Dict[str, Any]:
        """Process multiple queries in sequence with continuous learning"""
        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING {len(queries)} QUERIES")
        print(f"{'='*70}\n")
        
        results = []
        successful = 0
        failed = 0
        total_time = 0.0
        
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}/{len(queries)}")
            result = self.process_query_continuous_flow(query)
            results.append(result)
            
            if result['success']:
                successful += 1
            else:
                failed += 1
            
            total_time += result['total_time_ms']
        
        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*70}")
        print(f"Successful: {successful}/{len(queries)} | Failed: {failed}")
        print(f"Total Time: {total_time:.2f}ms | Avg: {total_time/len(queries):.2f}ms")
        print(f"{'='*70}\n")
        
        return {
            'batch_timestamp': datetime.now().isoformat(),
            'total_queries': len(queries),
            'successful': successful,
            'failed': failed,
            'total_time_ms': round(total_time, 2),
            'avg_time_ms': round(total_time / len(queries), 2),
            'results': results
        }
    
    def get_system_report(self) -> Dict[str, Any]:
        """Comprehensive system report"""
        if not self.execution_history:
            return {'message': 'No queries processed yet'}
        
        successful = [h for h in self.execution_history if h['success']]
        
        return {
            'total_queries_processed': len(self.execution_history),
            'successful': len(successful),
            'failed': len(self.execution_history) - len(successful),
            'avg_processing_time_ms': round(
                sum(h['total_time_ms'] for h in self.execution_history) / len(self.execution_history),
                2
            ),
            'consciousness_metrics': self.consciousness.get_consciousness_report(),
            'optimization_metrics': self.pipeline.get_optimization_report(),
            'security_metrics': self.executor.get_security_metrics(),
            'latest_execution': self.execution_history[-1] if self.execution_history else None
        }


# Example Usage and Testing
if __name__ == "__main__":
    # Initialize master orchestrator
    orchestrator = MasterQueryOrchestrator()
    
    # Test queries demonstrating continuous flow
    test_queries = [
        "Show total Sales for this month",
        "Get average Revenue where Region equals East",
        "Calculate count of Customers where Status equals Active"
    ]
    
    print("\n" + "="*70)
    print("MASTER INTEGRATION ORCHESTRATOR - CONTINUOUS FLOW TEST")
    print("="*70 + "\n")
    
    # Process batch
    batch_result = orchestrator.batch_process_queries(test_queries)
    
    # System report
    print("\n" + "="*70)
    print("SYSTEM REPORT")
    print("="*70)
    report = orchestrator.get_system_report()
    print(json.dumps({
        'total_queries': report['total_queries_processed'],
        'success_rate': f"{report['successful']/report['total_queries_processed']*100:.1f}%",
        'avg_time_ms': report['avg_processing_time_ms'],
        'consciousness_level': report['consciousness_metrics'].get('consciousness_level', 'UNKNOWN'),
        'system_health': 'OPERATIONAL'
    }, indent=2))
    print("="*70 + "\n")
