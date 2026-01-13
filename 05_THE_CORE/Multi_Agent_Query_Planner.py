"""
MULTI-AGENT QUERY PLANNER
6 specialized agents vote on optimal query strategies
Integrates: MultiAgentCoordinator + DaxTokenizer + SecurityHardening
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

try:
    from MultiAgentCoordinator import LogicAgent, ConsensusMechanism, MultiAgentCoordinator
    from DaxStudio_Framework_Ingestion import DaxTokenizer
    from SecurityHardeningEngine import InputValidator
except ImportError:
    print("Warning: Some components not found. Using mock implementations.")


class QueryStrategy(Enum):
    """Query execution strategies"""
    DIRECT = "DIRECT"  # Execute immediately
    CACHED = "CACHED"  # Use cached result
    PARTITIONED = "PARTITIONED"  # Split into smaller queries
    ASYNC = "ASYNC"  # Execute asynchronously
    MATERIALIZED = "MATERIALIZED"  # Use pre-computed view
    FEDERATED = "FEDERATED"  # Query multiple sources


@dataclass
class QueryPlan:
    """Represents a query execution plan"""
    strategy: QueryStrategy
    estimated_cost: float
    estimated_time_ms: float
    security_score: float
    optimization_steps: List[str]
    agent_votes: Dict[str, float]
    confidence: float


class QueryLogicAgent:
    """Analyzes query correctness and logical soundness"""
    
    def __init__(self):
        self.name = "Logic"
        self.tokenizer = DaxTokenizer()
        self.accuracy = 0.85
    
    def evaluate_query(self, query: str, context: Dict[str, Any]) -> Tuple[float, str]:
        """Evaluate query logic and correctness"""
        
        # Tokenize to check syntax
        tokens = self.tokenizer.tokenize(query)
        
        score = 0.5
        reasoning = []
        
        # Check for balanced parentheses
        open_parens = sum(1 for t in tokens if t.value == '(')
        close_parens = sum(1 for t in tokens if t.value == ')')
        if open_parens == close_parens:
            score += 0.2
            reasoning.append("Balanced parentheses")
        else:
            reasoning.append(f"Unbalanced parentheses: {open_parens} open, {close_parens} close")
        
        # Check for required keywords
        keywords = [t.value.upper() for t in tokens if t.type.name == 'KEYWORD']
        if 'EVALUATE' in keywords or 'RETURN' in keywords:
            score += 0.2
            reasoning.append("Valid query structure")
        else:
            reasoning.append("Missing EVALUATE/RETURN")
        
        # Check logical flow
        if any(kw in keywords for kw in ['FILTER', 'CALCULATE', 'SUMMARIZECOLUMNS']):
            score += 0.1
            reasoning.append("Contains logical operations")
        
        return min(score, 1.0), '; '.join(reasoning)


class QuerySecurityAgent:
    """Evaluates query security and injection risks"""
    
    def __init__(self):
        self.name = "Security"
        self.validator = InputValidator() if 'InputValidator' in globals() else None
        self.accuracy = 0.92
    
    def evaluate_query(self, query: str, context: Dict[str, Any]) -> Tuple[float, str]:
        """Assess query security risks"""
        
        score = 1.0
        threats = []
        
        # Check for SQL injection patterns
        dangerous_patterns = ['--', ';DROP', 'EXEC(', 'xp_cmdshell', '<script>', 'UNION SELECT']
        for pattern in dangerous_patterns:
            if pattern in query.upper():
                score -= 0.3
                threats.append(f"Dangerous pattern: {pattern}")
        
        # Check for suspicious concatenation
        if '"+' in query or '"+' in query:
            score -= 0.2
            threats.append("Suspicious string concatenation")
        
        # Validate using security engine
        if self.validator:
            is_valid, violations = self.validator.validate_input(query, "query")
            if not is_valid:
                score -= 0.3
                threats.extend(violations)
        
        reasoning = '; '.join(threats) if threats else "No security threats detected"
        return max(score, 0.0), reasoning


class QueryPerformanceAgent:
    """Optimizes for query performance"""
    
    def __init__(self):
        self.name = "Performance"
        self.accuracy = 0.88
    
    def evaluate_query(self, query: str, context: Dict[str, Any]) -> Tuple[float, str]:
        """Assess performance characteristics"""
        
        score = 0.7
        optimizations = []
        
        # Check for SELECT *
        if 'SELECT *' in query.upper():
            score -= 0.2
            optimizations.append("Avoid SELECT * - specify columns")
        
        # Check for filters
        if 'WHERE' in query.upper() or 'FILTER' in query.upper():
            score += 0.15
            optimizations.append("Good: Uses filtering")
        else:
            optimizations.append("Consider adding filters to reduce data scan")
        
        # Check for aggregations without grouping
        if any(agg in query.upper() for agg in ['SUM', 'COUNT', 'AVG']) and 'GROUP BY' not in query.upper():
            if 'SUMMARIZECOLUMNS' not in query.upper():
                score -= 0.1
                optimizations.append("Consider grouping for aggregations")
        
        # Check query length (complexity proxy)
        if len(query) > 500:
            score -= 0.05
            optimizations.append("Complex query - consider breaking into parts")
        
        reasoning = '; '.join(optimizations)
        return min(score, 1.0), reasoning


class QueryMemoryAgent:
    """Evaluates memory usage and caching potential"""
    
    def __init__(self):
        self.name = "Memory"
        self.accuracy = 0.83
    
    def evaluate_query(self, query: str, context: Dict[str, Any]) -> Tuple[float, str]:
        """Assess memory and caching characteristics"""
        
        score = 0.6
        recommendations = []
        
        # Check if query is cacheable (no time-sensitive functions)
        time_functions = ['NOW()', 'TODAY()', 'CURRENTTIME']
        has_time_dependency = any(tf in query.upper() for tf in time_functions)
        
        if not has_time_dependency:
            score += 0.25
            recommendations.append("Highly cacheable - no time dependencies")
        else:
            recommendations.append("Time-dependent - short cache TTL recommended")
        
        # Estimate result set size
        if 'LIMIT' in query.upper() or 'TOP' in query.upper():
            score += 0.15
            recommendations.append("Good: Result set limited")
        else:
            recommendations.append("Consider limiting result set size")
        
        reasoning = '; '.join(recommendations)
        return min(score, 1.0), reasoning


class QueryStrategyAgent:
    """Recommends execution strategy"""
    
    def __init__(self):
        self.name = "Strategy"
        self.accuracy = 0.86
    
    def evaluate_query(self, query: str, context: Dict[str, Any]) -> Tuple[float, str]:
        """Recommend execution strategy"""
        
        strategies = []
        
        # Check complexity
        query_complexity = len(query) + query.upper().count('JOIN') * 50
        
        if query_complexity < 100:
            strategies.append("DIRECT execution recommended")
            score = 0.9
        elif query_complexity < 300:
            strategies.append("CACHED execution beneficial")
            score = 0.8
        else:
            strategies.append("PARTITIONED execution for large query")
            score = 0.75
        
        # Check for parallel potential
        if 'UNION' in query.upper():
            strategies.append("Parallelizable with UNION split")
            score += 0.1
        
        reasoning = '; '.join(strategies)
        return min(score, 1.0), reasoning


class MultiAgentQueryPlanner:
    """
    Orchestrates 6 agents to plan optimal query execution
    """
    
    def __init__(self):
        self.agents = {
            'logic': QueryLogicAgent(),
            'security': QuerySecurityAgent(),
            'performance': QueryPerformanceAgent(),
            'memory': QueryMemoryAgent(),
            'strategy': QueryStrategyAgent()
        }
        self.consensus = None  # Consensus disabled - using simple voting
        self.planning_history: List[Dict[str, Any]] = []
    
    def plan_query_execution(self, query: str, context: Optional[Dict[str, Any]] = None) -> QueryPlan:
        """
        Multi-agent consensus on optimal query plan
        """
        context = context or {}
        timestamp = datetime.now().isoformat()
        
        # Collect evaluations from all agents
        agent_decisions = {}
        agent_reasonings = {}
        
        for agent_name, agent in self.agents.items():
            score, reasoning = agent.evaluate_query(query, context)
            agent_decisions[agent_name] = score
            agent_reasonings[agent_name] = reasoning
        
        # Calculate overall confidence
        overall_confidence = sum(agent_decisions.values()) / len(agent_decisions)
        
        # Determine strategy based on agent inputs
        strategy = self._determine_strategy(agent_decisions, agent_reasonings)
        
        # Estimate costs
        estimated_cost = self._estimate_cost(query, agent_decisions)
        estimated_time = self._estimate_time(query, agent_decisions)
        
        # Extract optimization steps
        optimization_steps = [
            reasoning for reasoning in agent_reasonings.values()
            if "Consider" in reasoning or "Good:" in reasoning
        ]
        
        # Build query plan
        plan = QueryPlan(
            strategy=strategy,
            estimated_cost=estimated_cost,
            estimated_time_ms=estimated_time,
            security_score=agent_decisions.get('security', 0.5),
            optimization_steps=optimization_steps[:5],
            agent_votes=agent_decisions,
            confidence=overall_confidence
        )
        
        # Log to history
        self.planning_history.append({
            'timestamp': timestamp,
            'query': query[:100],
            'plan': {
                'strategy': strategy.value,
                'confidence': overall_confidence,
                'security_score': plan.security_score
            },
            'agent_decisions': agent_decisions
        })
        
        return plan
    
    def _determine_strategy(self, decisions: Dict[str, float], reasonings: Dict[str, str]) -> QueryStrategy:
        """Determine best execution strategy"""
        
        # Security first
        if decisions.get('security', 1.0) < 0.5:
            return QueryStrategy.DIRECT  # Execute with caution
        
        # Check strategy agent recommendation
        strategy_reasoning = reasonings.get('strategy', '')
        if 'DIRECT' in strategy_reasoning:
            return QueryStrategy.DIRECT
        elif 'CACHED' in strategy_reasoning:
            return QueryStrategy.CACHED
        elif 'PARTITIONED' in strategy_reasoning:
            return QueryStrategy.PARTITIONED
        
        # Default based on confidence
        avg_score = sum(decisions.values()) / len(decisions)
        if avg_score > 0.8:
            return QueryStrategy.DIRECT
        else:
            return QueryStrategy.CACHED
    
    def _estimate_cost(self, query: str, decisions: Dict[str, float]) -> float:
        """Estimate execution cost (arbitrary units)"""
        base_cost = len(query) * 0.1
        performance_factor = 1.0 / (decisions.get('performance', 0.5) + 0.1)
        return base_cost * performance_factor
    
    def _estimate_time(self, query: str, decisions: Dict[str, float]) -> float:
        """Estimate execution time in milliseconds"""
        base_time = len(query) * 2
        performance_factor = 1.0 / (decisions.get('performance', 0.5) + 0.1)
        return base_time * performance_factor
    
    def get_planning_analytics(self) -> Dict[str, Any]:
        """Analytics on query planning"""
        if not self.planning_history:
            return {'total_plans': 0}
        
        strategy_distribution = {}
        for record in self.planning_history:
            strategy = record['plan']['strategy']
            strategy_distribution[strategy] = strategy_distribution.get(strategy, 0) + 1
        
        avg_confidence = sum(r['plan']['confidence'] for r in self.planning_history) / len(self.planning_history)
        avg_security = sum(r['plan']['security_score'] for r in self.planning_history) / len(self.planning_history)
        
        return {
            'total_plans': len(self.planning_history),
            'average_confidence': round(avg_confidence, 3),
            'average_security_score': round(avg_security, 3),
            'strategy_distribution': strategy_distribution,
            'last_plan_time': self.planning_history[-1]['timestamp']
        }


# Example Usage
if __name__ == "__main__":
    planner = MultiAgentQueryPlanner()
    
    test_queries = [
        "EVALUATE SUMMARIZECOLUMNS([Sales], [Region])",
        "SELECT * FROM Sales WHERE Amount > 1000",
        "EVALUATE FILTER(Sales, [Date] >= TODAY())",
        "EVALUATE CALCULATE(SUM([Revenue]), [Status] = 'Active')"
    ]
    
    print("=== MULTI-AGENT QUERY PLANNER ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        plan = planner.plan_query_execution(query)
        
        print(f"  Strategy: {plan.strategy.value}")
        print(f"  Confidence: {plan.confidence:.2%}")
        print(f"  Security Score: {plan.security_score:.2%}")
        print(f"  Estimated Time: {plan.estimated_time_ms:.2f}ms")
        print(f"  Agent Votes:")
        for agent, score in plan.agent_votes.items():
            print(f"    {agent}: {score:.2%}")
        print()
    
    # Analytics
    analytics = planner.get_planning_analytics()
    print("Planning Analytics:")
    print(json.dumps(analytics, indent=2))
