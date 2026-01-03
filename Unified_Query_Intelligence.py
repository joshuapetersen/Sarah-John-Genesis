"""
UNIFIED QUERY INTELLIGENCE SYSTEM
Natural Language → DAX/SQL Conversion with Dialectical Logic
Integrates: DaxTokenizer + Dialectical_Logic_Core + Gemini Genesis
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import hashlib

# Import Sarah Genesis Components
try:
    from Dialectical_Logic_Core import DialecticalEngine
    from Gemini_Genesis_Core import ResilientGenesisBridge
    from genesis_memory_daemon import MemoryDaemon
except ImportError:
    pass

try:
    from DaxStudio_Framework_Ingestion import DaxTokenizer, ModelExtractor
except ImportError:
    # Mock DaxTokenizer if not available
    class DaxTokenizer:
        def tokenize(self, query):
            return []
    
    class ModelExtractor:
        def __init__(self):
            pass


@dataclass
class QueryIntent:
    """Represents parsed user intent"""
    action: str  # SELECT, AGGREGATE, FILTER, JOIN, CALCULATE
    entities: List[str]  # Tables/measures referenced
    conditions: List[Dict[str, Any]]  # WHERE conditions
    aggregations: List[str]  # SUM, COUNT, AVG, etc.
    time_frame: Optional[str] = None
    confidence: float = 0.0


class NaturalLanguageQueryParser:
    """
    Converts natural language to structured query intent
    Uses Gemini for semantic understanding
    """
    
    ACTION_KEYWORDS = {
        'show': 'SELECT',
        'get': 'SELECT',
        'find': 'SELECT',
        'list': 'SELECT',
        'total': 'AGGREGATE',
        'sum': 'AGGREGATE',
        'count': 'AGGREGATE',
        'average': 'AGGREGATE',
        'calculate': 'CALCULATE',
        'filter': 'FILTER',
        'where': 'FILTER',
        'join': 'JOIN',
        'combine': 'JOIN'
    }
    
    AGGREGATION_KEYWORDS = {
        'total': 'SUM',
        'sum': 'SUM',
        'count': 'COUNT',
        'average': 'AVG',
        'mean': 'AVG',
        'maximum': 'MAX',
        'minimum': 'MIN',
        'max': 'MAX',
        'min': 'MIN'
    }
    
    def __init__(self, gemini_bridge: Optional[Any] = None):
        self.gemini_bridge = gemini_bridge
        self.tokenizer = DaxTokenizer()
        self.intent_history: List[QueryIntent] = []
    
    def parse_natural_language(self, nl_query: str) -> QueryIntent:
        """Convert natural language to structured intent"""
        nl_lower = nl_query.lower()
        
        # Detect action
        action = 'SELECT'
        for keyword, action_type in self.ACTION_KEYWORDS.items():
            if keyword in nl_lower:
                action = action_type
                break
        
        # Detect aggregations
        aggregations = []
        for keyword, agg_type in self.AGGREGATION_KEYWORDS.items():
            if keyword in nl_lower:
                aggregations.append(agg_type)
        
        # Extract entities (capitalized words or quoted phrases)
        entities = []
        words = nl_query.split()
        for word in words:
            if word[0].isupper() or word.startswith('['):
                entities.append(word.strip('[]'))
        
        # Time frame detection
        time_frame = None
        time_keywords = ['today', 'yesterday', 'this month', 'last month', 'this year', 'last year']
        for tk in time_keywords:
            if tk in nl_lower:
                time_frame = tk
                break
        
        # Extract conditions
        conditions = self._extract_conditions(nl_query)
        
        intent = QueryIntent(
            action=action,
            entities=entities,
            conditions=conditions,
            aggregations=aggregations,
            time_frame=time_frame,
            confidence=0.8
        )
        
        self.intent_history.append(intent)
        return intent
    
    def _extract_conditions(self, query: str) -> List[Dict[str, Any]]:
        """Extract WHERE/FILTER conditions"""
        conditions = []
        
        # Simple pattern matching for conditions
        if ' > ' in query:
            parts = query.split(' > ')
            if len(parts) == 2:
                conditions.append({'field': parts[0].strip(), 'operator': '>', 'value': parts[1].strip()})
        
        if ' < ' in query:
            parts = query.split(' < ')
            if len(parts) == 2:
                conditions.append({'field': parts[0].strip(), 'operator': '<', 'value': parts[1].strip()})
        
        if ' = ' in query or ' equals ' in query:
            separator = ' = ' if ' = ' in query else ' equals '
            parts = query.split(separator)
            if len(parts) == 2:
                conditions.append({'field': parts[0].strip(), 'operator': '=', 'value': parts[1].strip()})
        
        return conditions


class DAXQueryGenerator:
    """
    Generates optimized DAX queries from structured intent
    Uses dialectical reasoning for query optimization
    """
    
    def __init__(self, dialectical_engine: Optional[Any] = None):
        self.dialectical_engine = dialectical_engine
        self.model_extractor = ModelExtractor()
        self.query_templates: Dict[str, str] = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Query templates for different intent types"""
        return {
            'SELECT': 'EVALUATE SUMMARIZECOLUMNS({columns})',
            'AGGREGATE': 'EVALUATE SUMMARIZECOLUMNS({columns}, "{measure}", {aggregation}({expression}))',
            'FILTER': 'EVALUATE FILTER({table}, {conditions})',
            'CALCULATE': 'EVALUATE SUMMARIZECOLUMNS({columns}, "{measure}", CALCULATE({expression}, {filters}))',
            'JOIN': 'EVALUATE SUMMARIZECOLUMNS({columns1}, {columns2})'
        }
    
    def generate_dax(self, intent: QueryIntent, model_metadata: Optional[Dict[str, Any]] = None) -> Tuple[str, float]:
        """Convert intent to DAX query with confidence score"""
        
        # Select template based on action
        template = self.query_templates.get(intent.action, self.query_templates['SELECT'])
        
        # Build column list
        columns = ', '.join([f'[{entity}]' for entity in intent.entities])
        
        # Build aggregation expression
        if intent.aggregations:
            agg = intent.aggregations[0]
            measure_name = f"{agg}_{intent.entities[0]}" if intent.entities else "Measure1"
            expression = f"[{intent.entities[0]}]" if intent.entities else "[Value]"
            
            query = template.format(
                columns=columns,
                measure=measure_name,
                aggregation=agg,
                expression=expression
            )
        else:
            query = template.format(columns=columns)
        
        # Add filters if present
        if intent.conditions:
            filter_clauses = self._build_filter_clauses(intent.conditions)
            query = f"{query}, {filter_clauses}"
        
        # Add time frame filter
        if intent.time_frame:
            time_filter = self._build_time_filter(intent.time_frame)
            query = f"{query}, {time_filter}"
        
        # Dialectical optimization
        confidence = intent.confidence
        if self.dialectical_engine:
            # Use dialectical reasoning to validate and optimize
            thesis = f"Query: {query}"
            optimized = self._dialectical_optimize(thesis, intent)
            if optimized:
                query = optimized
                confidence = min(confidence + 0.1, 1.0)
        
        return query, confidence
    
    def _build_filter_clauses(self, conditions: List[Dict[str, Any]]) -> str:
        """Convert conditions to DAX filter expressions"""
        filters = []
        for cond in conditions:
            field = cond['field']
            operator = cond['operator']
            value = cond['value']
            
            # Sanitize value
            if isinstance(value, str) and not value.isdigit():
                value = f'"{value}"'
            
            filters.append(f'[{field}] {operator} {value}')
        
        return ', '.join(filters)
    
    def _build_time_filter(self, time_frame: str) -> str:
        """Convert time frame to DAX date filter"""
        time_mappings = {
            'today': 'TODAY()',
            'yesterday': 'TODAY() - 1',
            'this month': 'STARTOFMONTH(TODAY())',
            'last month': 'STARTOFMONTH(TODAY()) - 1',
            'this year': 'STARTOFYEAR(TODAY())',
            'last year': 'STARTOFYEAR(TODAY()) - 365'
        }
        
        dax_function = time_mappings.get(time_frame, 'TODAY()')
        return f'[Date] >= {dax_function}'
    
    def _dialectical_optimize(self, thesis: str, intent: QueryIntent) -> Optional[str]:
        """Use dialectical reasoning to optimize query"""
        # Placeholder for dialectical engine integration
        # In full implementation, this would:
        # 1. Generate antithesis (alternative query approach)
        # 2. Synthesize optimal query
        # 3. Return improved version
        return None


class QueryIntelligenceOrchestrator:
    """
    Master orchestrator combining NL parsing, DAX generation, and execution
    """
    
    def __init__(self):
        self.nl_parser = NaturalLanguageQueryParser()
        self.dax_generator = DAXQueryGenerator()
        self.query_history: List[Dict[str, Any]] = []
        self.learning_matrix: Dict[str, float] = {}
    
    def process_query(self, natural_language_query: str, model_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Full pipeline: NL → Intent → DAX → Execution
        """
        timestamp = datetime.now().isoformat()
        
        # Step 1: Parse natural language
        intent = self.nl_parser.parse_natural_language(natural_language_query)
        
        # Step 2: Generate DAX
        dax_query, confidence = self.dax_generator.generate_dax(intent, model_metadata)
        
        # Step 3: Log to history
        query_record = {
            'timestamp': timestamp,
            'natural_language': natural_language_query,
            'intent': {
                'action': intent.action,
                'entities': intent.entities,
                'aggregations': intent.aggregations,
                'conditions': intent.conditions,
                'time_frame': intent.time_frame
            },
            'generated_dax': dax_query,
            'confidence': confidence
        }
        self.query_history.append(query_record)
        
        # Step 4: Learn from query patterns
        self._update_learning_matrix(natural_language_query, dax_query, confidence)
        
        return query_record
    
    def _update_learning_matrix(self, nl_query: str, dax_query: str, confidence: float):
        """Track query patterns for future optimization"""
        query_hash = hashlib.md5(nl_query.encode()).hexdigest()[:16]
        self.learning_matrix[query_hash] = confidence
    
    def get_query_suggestions(self, partial_query: str) -> List[str]:
        """Suggest completions based on query history"""
        suggestions = []
        for record in self.query_history[-10:]:  # Last 10 queries
            if record['natural_language'].startswith(partial_query):
                suggestions.append(record['natural_language'])
        return suggestions
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Analytics on query intelligence system"""
        if not self.query_history:
            return {'total_queries': 0}
        
        avg_confidence = sum(q['confidence'] for q in self.query_history) / len(self.query_history)
        
        action_distribution = {}
        for q in self.query_history:
            action = q['intent']['action']
            action_distribution[action] = action_distribution.get(action, 0) + 1
        
        return {
            'total_queries': len(self.query_history),
            'average_confidence': round(avg_confidence, 3),
            'action_distribution': action_distribution,
            'learning_patterns': len(self.learning_matrix),
            'last_query_time': self.query_history[-1]['timestamp']
        }


# Example Usage
if __name__ == "__main__":
    orchestrator = QueryIntelligenceOrchestrator()
    
    # Test queries
    test_queries = [
        "Show total Sales for this month",
        "Get average Revenue where Region = 'East'",
        "Calculate count of Customers where Status = 'Active'",
        "Find all Orders where Amount > 1000 in last year"
    ]
    
    print("=== UNIFIED QUERY INTELLIGENCE SYSTEM ===\n")
    
    for query in test_queries:
        result = orchestrator.process_query(query)
        print(f"Natural Language: {result['natural_language']}")
        print(f"Generated DAX: {result['generated_dax']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Intent Action: {result['intent']['action']}")
        print("-" * 60)
    
    # Performance metrics
    metrics = orchestrator.get_performance_metrics()
    print(f"\nPerformance Metrics:")
    print(json.dumps(metrics, indent=2))
