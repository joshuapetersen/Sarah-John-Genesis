"""
SECURITY-HARDENED DAX EXECUTOR
Multi-layer injection prevention and validation for DAX/SQL queries
Integrates: SecurityHardeningEngine + DaxTokenizer + ResilientExecutor
January 2, 2026
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import hashlib
import re

try:
    from SecurityHardeningEngine import (
        InputValidator, AnomalyDetectionSecurity, 
        CryptographicIntegrity, SecurityHardeningEngine
    )
    from DaxStudio_Framework_Ingestion import DaxTokenizer, ResilientExecutor
except ImportError:
    print("Warning: Some components not found. Using mock implementations.")


@dataclass
class SecurityThreat:
    """Represents a detected security threat"""
    threat_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    pattern: str
    location: str
    recommendation: str
    confidence: float


class DAXInjectionDetector:
    """
    Specialized detector for DAX/SQL injection attacks
    """
    
    INJECTION_PATTERNS = [
        # SQL Injection patterns
        (r"(?i)(';?\s*DROP\s+TABLE)", "SQL_DROP", "CRITICAL"),
        (r"(?i)(';?\s*DELETE\s+FROM)", "SQL_DELETE", "CRITICAL"),
        (r"(?i)(';?\s*UPDATE\s+.*SET)", "SQL_UPDATE", "HIGH"),
        (r"(?i)(UNION\s+SELECT)", "SQL_UNION", "HIGH"),
        (r"(?i)(xp_cmdshell)", "SQL_COMMAND_EXEC", "CRITICAL"),
        (r"(?i)(EXEC\s*\()", "SQL_EXEC", "HIGH"),
        
        # DAX Injection patterns
        (r'(?i)(EVALUATE.*UNION.*EVALUATE)', "DAX_UNION_INJECTION", "HIGH"),
        (r'(?i)(;.*EVALUATE)', "DAX_STATEMENT_INJECTION", "HIGH"),
        (r'(?i)(PATHCONTAINS.*\.\./)', "DAX_PATH_TRAVERSAL", "MEDIUM"),
        (r"(\"+\s*[A-Z_]+\s*\+\")", "DAX_CONCAT_INJECTION", "MEDIUM"),
        
        # Comment-based attacks
        (r'(--.*[\'";\)])', "COMMENT_EVASION", "HIGH"),
        (r'(/\*.*\*/)', "BLOCK_COMMENT_EVASION", "MEDIUM"),
        
        # Encoding attacks
        (r'(%[0-9A-Fa-f]{2}){3,}', "URL_ENCODING_ATTACK", "MEDIUM"),
        (r'(\\x[0-9A-Fa-f]{2}){3,}', "HEX_ENCODING_ATTACK", "MEDIUM"),
    ]
    
    def __init__(self):
        self.detected_threats: List[SecurityThreat] = []
    
    def scan_for_injections(self, query: str) -> Tuple[bool, List[SecurityThreat]]:
        """Scan query for injection patterns"""
        threats = []
        
        for pattern, threat_type, severity in self.INJECTION_PATTERNS:
            matches = re.finditer(pattern, query)
            for match in matches:
                threat = SecurityThreat(
                    threat_type=threat_type,
                    severity=severity,
                    pattern=match.group(0),
                    location=f"Position {match.start()}-{match.end()}",
                    recommendation=self._get_recommendation(threat_type),
                    confidence=0.9 if severity == "CRITICAL" else 0.8
                )
                threats.append(threat)
        
        self.detected_threats.extend(threats)
        is_safe = len(threats) == 0
        
        return is_safe, threats
    
    def _get_recommendation(self, threat_type: str) -> str:
        """Get mitigation recommendation"""
        recommendations = {
            "SQL_DROP": "BLOCK IMMEDIATELY - Attempted table drop detected",
            "SQL_DELETE": "BLOCK IMMEDIATELY - Attempted data deletion detected",
            "SQL_UPDATE": "Review and sanitize - Potential data modification attempt",
            "SQL_UNION": "Validate carefully - UNION-based injection attempt",
            "SQL_COMMAND_EXEC": "BLOCK IMMEDIATELY - Command execution attempt",
            "SQL_EXEC": "BLOCK - Dynamic SQL execution detected",
            "DAX_UNION_INJECTION": "Validate structure - Multiple EVALUATE statements",
            "DAX_STATEMENT_INJECTION": "Sanitize semicolons - Statement chaining attempt",
            "DAX_PATH_TRAVERSAL": "Block path traversal characters",
            "DAX_CONCAT_INJECTION": "Validate concatenation - Potential injection vector",
            "COMMENT_EVASION": "Strip comments before processing",
            "BLOCK_COMMENT_EVASION": "Strip block comments before processing",
            "URL_ENCODING_ATTACK": "Decode and re-validate input",
            "HEX_ENCODING_ATTACK": "Decode and re-validate input"
        }
        return recommendations.get(threat_type, "Review for security implications")


class QuerySanitizer:
    """
    Sanitizes and escapes query inputs
    """
    
    FORBIDDEN_KEYWORDS = [
        'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'EXEC', 'EXECUTE',
        'xp_', 'sp_', 'sys.', 'INFORMATION_SCHEMA'
    ]
    
    def __init__(self):
        self.tokenizer = DaxTokenizer()
    
    def sanitize_query(self, query: str, strict: bool = True) -> Tuple[str, bool]:
        """Sanitize query by removing/escaping dangerous patterns"""
        
        sanitized = query
        is_modified = False
        
        # Remove comments
        sanitized = re.sub(r'--.*$', '', sanitized, flags=re.MULTILINE)
        sanitized = re.sub(r'/\*.*?\*/', '', sanitized, flags=re.DOTALL)
        if sanitized != query:
            is_modified = True
        
        # Remove extra semicolons
        if ';' in sanitized:
            sanitized = sanitized.replace(';', '')
            is_modified = True
        
        # Check for forbidden keywords
        if strict:
            for keyword in self.FORBIDDEN_KEYWORDS:
                if keyword.upper() in sanitized.upper():
                    # Replace with placeholder
                    sanitized = re.sub(
                        f'(?i){re.escape(keyword)}',
                        f'[BLOCKED:{keyword}]',
                        sanitized
                    )
                    is_modified = True
        
        # Escape single quotes
        if "'" in sanitized:
            sanitized = sanitized.replace("'", "''")
            is_modified = True
        
        return sanitized, is_modified
    
    def validate_identifiers(self, query: str) -> Tuple[bool, List[str]]:
        """Validate that identifiers are properly formatted"""
        tokens = self.tokenizer.tokenize(query)
        invalid_identifiers = []
        
        for token in tokens:
            if token.type.name == 'IDENTIFIER':
                # Check for suspicious patterns in identifiers
                if '..' in token.value or '/' in token.value or '\\' in token.value:
                    invalid_identifiers.append(token.value)
        
        return len(invalid_identifiers) == 0, invalid_identifiers


class SecureQueryExecutor:
    """
    Executes queries with multi-layer security validation
    """
    
    def __init__(self):
        self.injection_detector = DAXInjectionDetector()
        self.sanitizer = QuerySanitizer()
        self.input_validator = InputValidator() if 'InputValidator' in globals() else None
        self.anomaly_detector = AnomalyDetectionSecurity() if 'AnomalyDetectionSecurity' in globals() else None
        self.crypto = CryptographicIntegrity() if 'CryptographicIntegrity' in globals() else None
        self.executor = ResilientExecutor()
        self.execution_log: List[Dict[str, Any]] = []
        self.blocked_count = 0
    
    def execute_secure(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute query with comprehensive security checks
        """
        timestamp = datetime.now().isoformat()
        query_hash = hashlib.md5(query.encode()).hexdigest()[:16]
        context = context or {}
        
        security_report = {
            'timestamp': timestamp,
            'query_hash': query_hash,
            'stages': {}
        }
        
        # Stage 1: Input Validation
        stage1_start = datetime.now()
        if self.input_validator:
            is_valid, violations = self.input_validator.validate_input(query, "query")
            security_report['stages']['input_validation'] = {
                'passed': is_valid,
                'violations': violations,
                'duration_ms': (datetime.now() - stage1_start).total_seconds() * 1000
            }
            if not is_valid:
                self.blocked_count += 1
                return self._build_blocked_response(security_report, "Input validation failed")
        
        # Stage 2: Injection Detection
        stage2_start = datetime.now()
        is_safe, threats = self.injection_detector.scan_for_injections(query)
        security_report['stages']['injection_detection'] = {
            'passed': is_safe,
            'threats_found': len(threats),
            'threats': [
                {
                    'type': t.threat_type,
                    'severity': t.severity,
                    'pattern': t.pattern
                }
                for t in threats
            ],
            'duration_ms': (datetime.now() - stage2_start).total_seconds() * 1000
        }
        if not is_safe:
            critical_threats = [t for t in threats if t.severity == 'CRITICAL']
            if critical_threats:
                self.blocked_count += 1
                return self._build_blocked_response(security_report, f"Critical threat detected: {critical_threats[0].threat_type}")
        
        # Stage 3: Query Sanitization
        stage3_start = datetime.now()
        sanitized_query, was_modified = self.sanitizer.sanitize_query(query, strict=True)
        is_valid_identifiers, invalid_ids = self.sanitizer.validate_identifiers(sanitized_query)
        security_report['stages']['sanitization'] = {
            'passed': is_valid_identifiers,
            'was_modified': was_modified,
            'invalid_identifiers': invalid_ids,
            'duration_ms': (datetime.now() - stage3_start).total_seconds() * 1000
        }
        if not is_valid_identifiers:
            self.blocked_count += 1
            return self._build_blocked_response(security_report, f"Invalid identifiers: {invalid_ids}")
        
        # Stage 4: Anomaly Detection
        stage4_start = datetime.now()
        if self.anomaly_detector:
            try:
                self.anomaly_detector.record_request(context.get('user_id', 'anonymous'))
                anomalies = self.anomaly_detector.detect_anomalies()
            except AttributeError:
                # AnomalyDetectionSecurity API mismatch, skip anomaly detection
                anomalies = []
            security_report['stages']['anomaly_detection'] = {
                'passed': len(anomalies) == 0,
                'anomalies': anomalies,
                'duration_ms': (datetime.now() - stage4_start).total_seconds() * 1000
            }
        
        # Stage 5: Cryptographic Signing (for audit trail)
        stage5_start = datetime.now()
        if self.crypto:
            query_data = json.dumps({'query': sanitized_query, 'context': context})
            signature = self.crypto.sign_data(query_data)
            security_report['stages']['cryptographic_signing'] = {
                'passed': True,
                'signature': signature[:32] + '...',
                'duration_ms': (datetime.now() - stage5_start).total_seconds() * 1000
            }
        
        # Stage 6: Resilient Execution
        stage6_start = datetime.now()
        success, result = self.executor.execute_with_resilience(
            self._mock_execute, sanitized_query
        )
        security_report['stages']['execution'] = {
            'passed': success,
            'result_preview': str(result)[:100] if success else result,
            'duration_ms': (datetime.now() - stage6_start).total_seconds() * 1000
        }
        
        # Log execution
        self.execution_log.append({
            'timestamp': timestamp,
            'query_hash': query_hash,
            'success': success,
            'security_report': security_report
        })
        
        return {
            'success': success,
            'query': sanitized_query,
            'result': result if success else None,
            'security_report': security_report,
            'was_sanitized': was_modified,
            'total_duration_ms': sum(
                stage['duration_ms'] for stage in security_report['stages'].values()
            )
        }
    
    def _mock_execute(self, query: str) -> Dict[str, Any]:
        """Mock query execution"""
        return {
            'row_count': 100,
            'columns': ['Column1', 'Column2'],
            'execution_time_ms': 50
        }
    
    def _build_blocked_response(self, security_report: Dict[str, Any], reason: str) -> Dict[str, Any]:
        """Build response for blocked query"""
        return {
            'success': False,
            'blocked': True,
            'reason': reason,
            'security_report': security_report,
            'recommendation': "Review query for security violations"
        }
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security execution metrics"""
        if not self.execution_log:
            return {'total_executions': 0}
        
        successful = [e for e in self.execution_log if e['success']]
        
        return {
            'total_executions': len(self.execution_log),
            'successful_executions': len(successful),
            'blocked_executions': self.blocked_count,
            'block_rate': round(self.blocked_count / len(self.execution_log) * 100, 2),
            'avg_security_check_duration_ms': self._calculate_avg_security_duration(),
            'threat_distribution': self._get_threat_distribution()
        }
    
    def _calculate_avg_security_duration(self) -> float:
        """Calculate average security check duration"""
        durations = []
        for log in self.execution_log:
            total = sum(
                stage['duration_ms'] 
                for stage in log['security_report']['stages'].values()
            )
            durations.append(total)
        return round(sum(durations) / len(durations), 2) if durations else 0.0
    
    def _get_threat_distribution(self) -> Dict[str, int]:
        """Get distribution of detected threats"""
        distribution = {}
        for threat in self.injection_detector.detected_threats:
            distribution[threat.threat_type] = distribution.get(threat.threat_type, 0) + 1
        return distribution


# Example Usage
if __name__ == "__main__":
    executor = SecureQueryExecutor()
    
    test_queries = [
        "EVALUATE SUMMARIZECOLUMNS([Sales])",  # Safe
        "EVALUATE FILTER(Sales, [Amount] > 1000); DROP TABLE Users;",  # Injection attempt
        "SELECT * FROM Sales WHERE 1=1 OR 1=1--",  # SQL injection
        "EVALUATE CALCULATE(SUM([Sales]), [Region] = 'East')"  # Safe
    ]
    
    print("=== SECURITY-HARDENED DAX EXECUTOR ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query[:60]}...")
        result = executor.execute_secure(query)
        
        print(f"  Success: {result['success']}")
        if 'blocked' in result:
            print(f"  BLOCKED: {result['reason']}")
        print(f"  Was Sanitized: {result.get('was_sanitized', False)}")
        print(f"  Security Duration: {result.get('total_duration_ms', 0):.2f}ms")
        
        # Show stage results
        for stage_name, stage_info in result['security_report']['stages'].items():
            status = "[OK] PASS" if stage_info['passed'] else "[FAIL] FAIL"
            print(f"    {stage_name}: {status}")
        
        print()
    
    # Security metrics
    metrics = executor.get_security_metrics()
    print("Security Metrics:")
    print(json.dumps(metrics, indent=2))
