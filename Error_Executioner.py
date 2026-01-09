"""
ERROR EXECUTIONER - DEDICATED ERROR DETECTION AGENT
Scans code for errors without execution
Static analysis, syntax validation, type checking, dependency verification
January 2, 2026
"""

import ast
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import importlib.util
import sys


class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "CRITICAL"  # Blocks execution
    HIGH = "HIGH"  # Major issue, likely to cause runtime errors
    MEDIUM = "MEDIUM"  # Potential issue
    LOW = "LOW"  # Minor issue, code smell
    INFO = "INFO"  # Informational


@dataclass
class CodeError:
    """Represents a detected error"""
    error_id: str
    severity: ErrorSeverity
    error_type: str  # SYNTAX, TYPE_MISMATCH, IMPORT_ERROR, LOGIC_ERROR, etc.
    file_path: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    message: str = ""
    context: str = ""  # Surrounding code
    suggestion: str = ""  # How to fix
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())


class SyntaxErrorDetector:
    """
    Detects syntax errors without executing code
    """
    
    def __init__(self):
        self.errors: List[CodeError] = []
    
    def scan_file(self, file_path: str) -> List[CodeError]:
        """Scan file for syntax errors"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Try to parse the code as AST
            try:
                ast.parse(code)
            except SyntaxError as e:
                error = CodeError(
                    error_id=f"SYNTAX_{file_path}_{e.lineno}",
                    severity=ErrorSeverity.CRITICAL,
                    error_type="SYNTAX_ERROR",
                    file_path=file_path,
                    line_number=e.lineno,
                    column=e.offset,
                    message=str(e.msg),
                    context=self._extract_context(code, e.lineno) if e.lineno else "",
                    suggestion="Fix syntax error before proceeding"
                )
                errors.append(error)
        
        except FileNotFoundError:
            error = CodeError(
                error_id=f"FILE_NOT_FOUND_{file_path}",
                severity=ErrorSeverity.CRITICAL,
                error_type="FILE_ERROR",
                file_path=file_path,
                message=f"File not found: {file_path}",
                suggestion="Verify file path is correct"
            )
            errors.append(error)
        
        self.errors.extend(errors)
        return errors
    
    def _extract_context(self, code: str, line_number: int, context_lines: int = 3) -> str:
        """Extract surrounding code for context"""
        lines = code.split('\n')
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        context = []
        for i in range(start, end):
            marker = ">>> " if i == line_number - 1 else "    "
            context.append(f"{marker}{i+1}: {lines[i]}")
        
        return '\n'.join(context)


class TypeMismatchDetector:
    """
    Detects type mismatches and type errors
    """
    
    def __init__(self):
        self.errors: List[CodeError] = []
    
    def scan_code(self, code: str, file_path: str) -> List[CodeError]:
        """Scan for common type mismatches"""
        errors = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Detect string + number concatenation
            if re.search(r'["\'].*["\']\s*\+\s*\d+|["\'].*["\']\s*\+\s*\w+\.\w+\(\)', line):
                error = CodeError(
                    error_id=f"TYPE_MISMATCH_{file_path}_{line_num}",
                    severity=ErrorSeverity.HIGH,
                    error_type="TYPE_MISMATCH",
                    file_path=file_path,
                    line_number=line_num,
                    message="Potential string + number concatenation",
                    context=line.strip(),
                    suggestion="Use f-string or str() conversion: f'{value}' or str(value)"
                )
                errors.append(error)
            
            # Detect float + str operations
            if re.search(r'float\([^)]+\)\s*\+\s*["\']|["\'].*["\']\s*\+\s*float\(', line):
                error = CodeError(
                    error_id=f"TYPE_MISMATCH_FLOAT_{file_path}_{line_num}",
                    severity=ErrorSeverity.HIGH,
                    error_type="TYPE_MISMATCH",
                    file_path=file_path,
                    line_number=line_num,
                    message="Float and string concatenation detected",
                    context=line.strip(),
                    suggestion="Convert to string before concatenation"
                )
                errors.append(error)
            
            # Detect list/dict index type errors
            if re.search(r'\[["\'][^"\']*["\']\]', line) and 'dict' not in line.lower():
                # Check if it's likely a list being indexed with string
                if re.search(r'\w+\[["\']', line) and not re.search(r'(dict|Dict|Mapping)', code[:code.find(line)]):
                    error = CodeError(
                        error_id=f"INDEX_TYPE_{file_path}_{line_num}",
                        severity=ErrorSeverity.MEDIUM,
                        error_type="TYPE_MISMATCH",
                        file_path=file_path,
                        line_number=line_num,
                        message="Possible string index on list (should be integer)",
                        context=line.strip(),
                        suggestion="Use integer index for lists, or verify data structure is dict"
                    )
                    errors.append(error)
        
        self.errors.extend(errors)
        return errors


class ImportErrorDetector:
    """
    Detects missing imports and dependency issues
    """
    
    def __init__(self):
        self.errors: List[CodeError] = []
    
    def scan_imports(self, file_path: str) -> List[CodeError]:
        """Scan for import errors"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Parse AST to find imports
            try:
                tree = ast.parse(code)
            except SyntaxError:
                # Already caught by SyntaxErrorDetector
                return errors
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not self._module_exists(alias.name):
                            error = CodeError(
                                error_id=f"IMPORT_{file_path}_{node.lineno}_{alias.name}",
                                severity=ErrorSeverity.HIGH,
                                error_type="IMPORT_ERROR",
                                file_path=file_path,
                                line_number=node.lineno,
                                message=f"Module '{alias.name}' not found or not installed",
                                context=f"import {alias.name}",
                                suggestion=f"Install with: pip install {alias.name}"
                            )
                            errors.append(error)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module and not self._module_exists(node.module):
                        error = CodeError(
                            error_id=f"IMPORT_FROM_{file_path}_{node.lineno}_{node.module}",
                            severity=ErrorSeverity.HIGH,
                            error_type="IMPORT_ERROR",
                            file_path=file_path,
                            line_number=node.lineno,
                            message=f"Module '{node.module}' not found or not installed",
                            context=f"from {node.module} import ...",
                            suggestion=f"Install with: pip install {node.module}"
                        )
                        errors.append(error)
        
        except FileNotFoundError:
            pass  # Already handled by SyntaxErrorDetector
        
        self.errors.extend(errors)
        return errors
    
    def _module_exists(self, module_name: str) -> bool:
        """Check if module exists/is installed"""
        # Check if it's a standard library module
        if module_name in sys.builtin_module_names:
            return True
        
        # Check if it can be imported
        spec = importlib.util.find_spec(module_name)
        return spec is not None


class LogicErrorDetector:
    """
    Detects logical errors and code smells
    """
    
    def __init__(self):
        self.errors: List[CodeError] = []
    
    def scan_logic(self, code: str, file_path: str) -> List[CodeError]:
        """Scan for logical errors"""
        errors = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Detect division by zero potential
            if re.search(r'/\s*0(?:\s|$|\))', line) and '//' not in line and 'http' not in line.lower():
                error = CodeError(
                    error_id=f"DIVISION_ZERO_{file_path}_{line_num}",
                    severity=ErrorSeverity.CRITICAL,
                    error_type="LOGIC_ERROR",
                    file_path=file_path,
                    line_number=line_num,
                    message="Division by zero detected",
                    context=line.strip(),
                    suggestion="Add zero check before division"
                )
                errors.append(error)
            
            # Detect comparison with = instead of ==
            if re.search(r'if\s+\w+\s*=\s*[^=]', line):
                error = CodeError(
                    error_id=f"ASSIGNMENT_IN_IF_{file_path}_{line_num}",
                    severity=ErrorSeverity.HIGH,
                    error_type="LOGIC_ERROR",
                    file_path=file_path,
                    line_number=line_num,
                    message="Assignment (=) in if condition instead of comparison (==)",
                    context=line.strip(),
                    suggestion="Use == for comparison, = for assignment"
                )
                errors.append(error)
            
            # Detect empty except blocks
            if line.strip() == 'except:' or line.strip().startswith('except '):
                next_line_num = line_num + 1
                if next_line_num < len(lines):
                    next_line = lines[next_line_num].strip()
                    if next_line == 'pass' or next_line == '':
                        error = CodeError(
                            error_id=f"EMPTY_EXCEPT_{file_path}_{line_num}",
                            severity=ErrorSeverity.MEDIUM,
                            error_type="CODE_SMELL",
                            file_path=file_path,
                            line_number=line_num,
                            message="Empty except block - errors silently ignored",
                            context=line.strip(),
                            suggestion="Log the error or handle it explicitly"
                        )
                        errors.append(error)
            
            # Detect unused variables (simple heuristic)
            match = re.match(r'\s*(\w+)\s*=\s*.+', line)
            if match and line_num < len(lines) - 1:
                var_name = match.group(1)
                # Check if variable is used in next 10 lines
                following_code = '\n'.join(lines[line_num:min(line_num+10, len(lines))])
                if var_name not in following_code and not var_name.startswith('_'):
                    error = CodeError(
                        error_id=f"UNUSED_VAR_{file_path}_{line_num}_{var_name}",
                        severity=ErrorSeverity.LOW,
                        error_type="CODE_SMELL",
                        file_path=file_path,
                        line_number=line_num,
                        message=f"Variable '{var_name}' assigned but potentially unused",
                        context=line.strip(),
                        suggestion="Remove unused variable or prefix with _ if intentional"
                    )
                    errors.append(error)
        
        self.errors.extend(errors)
        return errors


class ErrorExecutioner:
    """
    Master error detection agent
    Coordinates all error detectors without executing code
    """
    
    def __init__(self):
        self.syntax_detector = SyntaxErrorDetector()
        self.type_detector = TypeMismatchDetector()
        self.import_detector = ImportErrorDetector()
        self.logic_detector = LogicErrorDetector()
        self.scan_history: List[Dict[str, Any]] = []
    
    def execute_error_scan(self, file_path: str, scan_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute comprehensive error scan without running code
        scan_types: ['syntax', 'type', 'import', 'logic'] or None for all
        """
        timestamp = datetime.now().isoformat()
        scan_types = scan_types or ['syntax', 'type', 'import', 'logic']
        
        all_errors = []
        scan_results = {}
        
        # Read file once
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            return {
                'timestamp': timestamp,
                'file_path': file_path,
                'scan_completed': False,
                'error': 'File not found',
                'errors': []
            }
        
        # Syntax scan (must pass before other scans make sense)
        if 'syntax' in scan_types:
            syntax_errors = self.syntax_detector.scan_file(file_path)
            scan_results['syntax'] = {
                'errors_found': len(syntax_errors),
                'errors': syntax_errors
            }
            all_errors.extend(syntax_errors)
            
            # If critical syntax errors, skip other scans
            if any(e.severity == ErrorSeverity.CRITICAL for e in syntax_errors):
                return self._build_scan_result(timestamp, file_path, scan_results, all_errors, 
                                               blocked_by='SYNTAX_ERROR')
        
        # Type mismatch scan
        if 'type' in scan_types:
            type_errors = self.type_detector.scan_code(code, file_path)
            scan_results['type'] = {
                'errors_found': len(type_errors),
                'errors': type_errors
            }
            all_errors.extend(type_errors)
        
        # Import scan
        if 'import' in scan_types:
            import_errors = self.import_detector.scan_imports(file_path)
            scan_results['import'] = {
                'errors_found': len(import_errors),
                'errors': import_errors
            }
            all_errors.extend(import_errors)
        
        # Logic scan
        if 'logic' in scan_types:
            logic_errors = self.logic_detector.scan_logic(code, file_path)
            scan_results['logic'] = {
                'errors_found': len(logic_errors),
                'errors': logic_errors
            }
            all_errors.extend(logic_errors)
        
        result = self._build_scan_result(timestamp, file_path, scan_results, all_errors)
        self.scan_history.append(result)
        
        return result
    
    def _build_scan_result(self, timestamp: str, file_path: str, 
                          scan_results: Dict, all_errors: List[CodeError],
                          blocked_by: Optional[str] = None) -> Dict[str, Any]:
        """Build comprehensive scan result"""
        
        critical_errors = [e for e in all_errors if e.severity == ErrorSeverity.CRITICAL]
        high_errors = [e for e in all_errors if e.severity == ErrorSeverity.HIGH]
        
        return {
            'timestamp': timestamp,
            'file_path': file_path,
            'scan_completed': True,
            'blocked_by': blocked_by,
            'verdict': self._determine_verdict(all_errors),
            'total_errors': len(all_errors),
            'critical_errors': len(critical_errors),
            'high_errors': len(high_errors),
            'errors_by_type': self._categorize_errors(all_errors),
            'errors': [self._serialize_error(e) for e in all_errors],
            'execution_safe': len(critical_errors) == 0,
            'recommendations': self._generate_recommendations(all_errors)
        }
    
    def _determine_verdict(self, errors: List[CodeError]) -> str:
        """Determine overall verdict"""
        critical = any(e.severity == ErrorSeverity.CRITICAL for e in errors)
        high = any(e.severity == ErrorSeverity.HIGH for e in errors)
        
        if critical:
            return "BLOCKED - Critical errors prevent execution"
        elif high:
            return "WARNING - High severity errors likely to cause runtime issues"
        elif len(errors) > 0:
            return "CAUTION - Minor issues detected"
        else:
            return "CLEAR - No errors detected"
    
    def _categorize_errors(self, errors: List[CodeError]) -> Dict[str, int]:
        """Categorize errors by type"""
        categories = {}
        for error in errors:
            categories[error.error_type] = categories.get(error.error_type, 0) + 1
        return categories
    
    def _serialize_error(self, error: CodeError) -> Dict[str, Any]:
        """Convert error to dict for JSON serialization"""
        return {
            'error_id': error.error_id,
            'severity': error.severity.value,
            'type': error.error_type,
            'line': error.line_number,
            'column': error.column,
            'message': error.message,
            'context': error.context,
            'suggestion': error.suggestion
        }
    
    def _generate_recommendations(self, errors: List[CodeError]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        if critical_errors:
            recommendations.append(f"URGENT: Fix {len(critical_errors)} critical errors before execution")
        
        syntax_errors = [e for e in errors if e.error_type == 'SYNTAX_ERROR']
        if syntax_errors:
            recommendations.append(f"Fix syntax errors at lines: {', '.join(str(e.line_number) for e in syntax_errors[:5])}")
        
        type_errors = [e for e in errors if e.error_type == 'TYPE_MISMATCH']
        if type_errors:
            recommendations.append(f"Review type conversions - {len(type_errors)} potential type mismatches")
        
        import_errors = [e for e in errors if e.error_type == 'IMPORT_ERROR']
        if import_errors:
            missing_modules = []
            for e in import_errors[:5]:
                parts = e.message.split("'")
                if len(parts) > 1:
                    missing_modules.append(parts[1])
            if missing_modules:
                recommendations.append(f"Install missing dependencies: {', '.join(set(missing_modules))}")
        
        if not recommendations:
            recommendations.append("Code passes all error checks - safe to execute")
        
        return recommendations
    
    def scan_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Scan multiple files in batch"""
        results = {}
        total_errors = 0
        blocked_files = []
        
        for file_path in file_paths:
            result = self.execute_error_scan(file_path)
            results[file_path] = result
            total_errors += result['total_errors']
            
            if not result['execution_safe']:
                blocked_files.append(file_path)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'files_scanned': len(file_paths),
            'total_errors': total_errors,
            'blocked_files': blocked_files,
            'results': results
        }
    
    def get_error_report(self) -> str:
        """Generate comprehensive error report"""
        if not self.scan_history:
            return "No scans performed yet"
        
        report = {
            'total_scans': len(self.scan_history),
            'files_with_errors': len([s for s in self.scan_history if s['total_errors'] > 0]),
            'total_errors_found': sum(s['total_errors'] for s in self.scan_history),
            'recent_scans': self.scan_history[-5:]
        }
        
        return json.dumps(report, indent=2, default=str)


# Example Usage
if __name__ == "__main__":
    executioner = ErrorExecutioner()
    
    # Test files
    test_files = [
        'Unified_Query_Intelligence.py',
        'Self_Optimizing_Data_Pipeline.py',
        'Security_Hardened_DAX_Executor.py'
    ]
    
    print("=== ERROR EXECUTIONER - DEDICATED ERROR DETECTION ===\n")
    
    for file_path in test_files:
        print(f"Scanning: {file_path}")
        result = executioner.execute_error_scan(file_path)
        
        print(f"  Verdict: {result['verdict']}")
        print(f"  Total Errors: {result['total_errors']}")
        print(f"  Critical: {result['critical_errors']}, High: {result['high_errors']}")
        print(f"  Execution Safe: {'[OK]' if result['execution_safe'] else '[FAIL]'}")
        
        if result['errors']:
            print(f"  Top Errors:")
            for error in result['errors'][:3]:
                print(f"    - [{error['severity']}] {error['type']}: {error['message']}")
        
        print()
    
    # Full report
    print("Error Detection Report:")
    print(executioner.get_error_report())
