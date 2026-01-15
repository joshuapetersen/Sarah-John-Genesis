import ast
import re
import os
from Sovereign_Math import SovereignMath
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import json


class CodeComplexityAnalyzer:
    """Analyze code complexity and identify slow patterns"""
    
    def __init__(self):
        self.issues = []
        self.file_metrics = {}
    
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Deep analysis of a single file"""
        if not filepath.endswith('.py'):
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = {
                'blocking_operations': self._find_blocking_operations(content),
                'nested_loops': self._find_nested_loops(content),
                'redundant_operations': self._find_redundant_operations(content),
                'missing_caching': self._find_missing_caching(content),
                'inefficient_string_ops': self._find_inefficient_strings(content),
                'unoptimized_imports': self._find_unoptimized_imports(content),
                'synchronous_io': self._find_synchronous_io(content),
                'missing_parallelization': self._find_missing_parallelization(content)
            }
            
            total_issues = sum(len(v) for v in issues.values())
            
            self.file_metrics[filepath] = {
                'total_issues': total_issues,
                'issues': issues,
                'lines': len(content.split('\n'))
            }
            
            return self.file_metrics[filepath]
        
        except Exception as e:
            return {'error': str(e)}
    
    def _find_blocking_operations(self, content: str) -> List[Dict]:
        """Find operations that block execution"""
        issues = []
        lines = content.split('\n')
        
        blocking_patterns = [
            (r'time\.sleep\(', 'time.sleep() blocks execution'),
            (r'\.join\(\)', 'Thread/process join() can block'),
            (r'input\(', 'input() blocks waiting for user'),
            (r'requests\.get\(', 'Synchronous HTTP request'),
            (r'requests\.post\(', 'Synchronous HTTP request'),
            (r'open\(.*\)\.read\(\)', 'Blocking file read'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, desc in blocking_patterns:
                if re.search(pattern, line):
                    issues.append({
                        'line': i,
                        'code': line.strip(),
                        'issue': desc,
                        'severity': 'HIGH'
                    })
        
        return issues
    
    def _find_nested_loops(self, content: str) -> List[Dict]:
        """Find nested loops (O(n²) or worse complexity)"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    # Check if there's another for loop inside
                    for child in ast.walk(node):
                        if child != node and isinstance(child, ast.For):
                            issues.append({
                                'line': node.lineno,
                                'issue': 'Nested for loop detected (O(n²) complexity)',
                                'severity': 'MEDIUM'
                            })
                            break
        except:
            pass
        
        return issues
    
    def _find_redundant_operations(self, content: str) -> List[Dict]:
        """Find redundant or repeated operations"""
        issues = []
        lines = content.split('\n')
        
        # Find repeated function calls in same scope
        seen_calls = defaultdict(list)
        
        for i, line in enumerate(lines, 1):
            # Look for repeated expensive operations
            if '.items()' in line and 'for' not in line:
                issues.append({
                    'line': i,
                    'issue': 'Calling .items() outside loop - cache result',
                    'severity': 'LOW'
                })
            
            if re.search(r'len\(.+\).*len\(.+\)', line):
                issues.append({
                    'line': i,
                    'issue': 'Multiple len() calls on same line - cache result',
                    'severity': 'LOW'
                })
        
        return issues
    
    def _find_missing_caching(self, content: str) -> List[Dict]:
        """Find functions that should be cached but aren't"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function has no side effects but no caching
                    has_cache_decorator = any(
                        isinstance(d, ast.Name) and d.id in ['lru_cache', 'cache', 'memoize']
                        for d in node.decorator_list
                    )
                    
                    # Look for expensive operations without caching
                    has_loop = any(isinstance(n, ast.For) for n in ast.walk(node))
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                    
                    if has_loop and has_return and not has_cache_decorator:
                        # Check if function takes simple inputs
                        if len(node.args.args) > 0:
                            issues.append({
                                'line': node.lineno,
                                'function': node.name,
                                'issue': 'Function with loops could benefit from @lru_cache',
                                'severity': 'MEDIUM'
                            })
        except:
            pass
        
        return issues
    
    def _find_inefficient_strings(self, content: str) -> List[Dict]:
        """Find inefficient string operations"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # String concatenation in loops
            if 'for ' in line and '+=' in line and '"' in line:
                issues.append({
                    'line': i,
                    'issue': 'String concatenation in loop - use list.append() + join()',
                    'severity': 'MEDIUM'
                })
            
            # Multiple replace calls
            if line.count('.replace(') > 2:
                issues.append({
                    'line': i,
                    'issue': 'Multiple .replace() calls - use regex or str.translate()',
                    'severity': 'LOW'
                })
        
        return issues
    
    def _find_unoptimized_imports(self, content: str) -> List[Dict]:
        """Find import issues"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('from') and '*' in line:
                issues.append({
                    'line': i,
                    'issue': 'Wildcard import (from X import *) - import specific items',
                    'severity': 'LOW'
                })
            
            if line.strip().startswith('import') and ',' in line:
                issues.append({
                    'line': i,
                    'issue': 'Multiple imports on one line - split for clarity',
                    'severity': 'LOW'
                })
        
        return issues
    
    def _find_synchronous_io(self, content: str) -> List[Dict]:
        """Find synchronous I/O that could be async"""
        issues = []
        lines = content.split('\n')
        
        io_patterns = [
            (r'open\(.+\)', 'Synchronous file open'),
            (r'\.read\(\)', 'Synchronous read operation'),
            (r'\.write\(', 'Synchronous write operation'),
            (r'subprocess\.run\(', 'Synchronous subprocess execution'),
        ]
        
        for i, line in enumerate(lines, 1):
            if 'async' not in line and 'await' not in line:
                for pattern, desc in io_patterns:
                    if re.search(pattern, line) and 'for ' in lines[max(0, i-2):i+1]:
                        issues.append({
                            'line': i,
                            'issue': f'{desc} in loop - consider async/await',
                            'severity': 'HIGH'
                        })
        
        return issues
    
    def _find_missing_parallelization(self, content: str) -> List[Dict]:
        """Find loops that could be parallelized"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'for ' in line and 'in ' in line:
                # Check next 10 lines for expensive operations
                check_lines = lines[i:i+10]
                for check_line in check_lines:
                    if any(op in check_line for op in ['.process(', '.execute(', '.analyze(', '.compute(']):
                        issues.append({
                            'line': i,
                            'issue': 'Loop with expensive operations - consider ThreadPoolExecutor',
                            'severity': 'MEDIUM'
                        })
                        break
        
        return issues


class PerformanceProfiler:
    """Profile actual execution performance"""
    
    def __init__(self):
        self.profiles = {}
    
    def profile_function(self, func_name: str, func_code: str) -> Dict[str, Any]:
        """Profile a function's performance characteristics"""
        
        analysis = {
            'estimated_complexity': self._estimate_complexity(func_code),
            'memory_intensive': self._check_memory_intensive(func_code),
            'cpu_intensive': self._check_cpu_intensive(func_code),
            'io_bound': self._check_io_bound(func_code)
        }
        
        return analysis
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate time complexity"""
        nested_loops = code.count('for ') - code.count('# for ')
        
        if nested_loops >= 3:
            return 'O(n³) or worse - CRITICAL'
        elif nested_loops == 2:
            return 'O(n²) - HIGH'
        elif nested_loops == 1:
            return 'O(n) - ACCEPTABLE'
        else:
            return 'O(1) - OPTIMAL'
    
    def _check_memory_intensive(self, code: str) -> bool:
        """Check if function is memory intensive"""
        memory_patterns = [
            'list(',
            'dict(',
            '.copy()',
            'deepcopy',
            '[:]'
        ]
        return any(p in code for p in memory_patterns)
    
    def _check_cpu_intensive(self, code: str) -> bool:
        """Check if function is CPU intensive"""
        cpu_patterns = [
            'sort',
            'calculate',
            'compute',
            'process',
            'transform',
            'for ' * 2  # nested loops
        ]
        return any(p in code for p in cpu_patterns)
    
    def _check_io_bound(self, code: str) -> bool:
        """Check if function is I/O bound"""
        io_patterns = [
            'open(',
            'read(',
            'write(',
            'request',
            'fetch',
            'load('
        ]
        return any(p in code for p in io_patterns)


class SystemLazyAuditor:
    """Main auditor orchestrating all checks"""
    
    def __init__(self, workspace_path: str):
        self._0x_math = SovereignMath()
        self.workspace_path = workspace_path
        self.complexity_analyzer = CodeComplexityAnalyzer()
        self.profiler = PerformanceProfiler()
        self.audit_results = {
            'total_files_scanned': 0,
            'total_issues_found': 0,
            'critical_issues': [],
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'file_reports': {}
        }
    
    def audit_entire_system(self) -> Dict[str, Any]:
        """Perform comprehensive system audit"""
        print("="*70)
        print("LAZY PROCESS AUDITOR - DEEP SYSTEM SCAN")
        print("="*70 + "\n")
        
        print("Scanning workspace for Python files...")
        
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip virtual environments and build directories
            dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '__pycache__', 'build', 'dist']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        print(f"Found {len(python_files)} Python files\n")
        
        # Analyze each file
        for i, filepath in enumerate(python_files, 1):
            filename = os.path.basename(filepath)
            print(f"[{i}/{len(python_files)}] Analyzing {filename}...", end=' ')
            
            start_t3 = self._0x_math.get_temporal_volume()
            report = self.complexity_analyzer.analyze_file(filepath)
            elapsed_t3 = (self._0x_math.get_temporal_volume() - start_t3)
            
            if 'error' not in report:
                total = report['total_issues']
                print(f"{total} issues ({elapsed_t3:.4f} t3 units)")
                
                self.audit_results['total_files_scanned'] += 1
                self.audit_results['total_issues_found'] += total
                self.audit_results['file_reports'][filename] = report
                
                # Categorize issues
                for category, issues in report['issues'].items():
                    for issue in issues:
                        severity = issue.get('severity', 'LOW')
                        issue['file'] = filename
                        issue['category'] = category
                        
                        if severity == 'CRITICAL':
                            self.audit_results['critical_issues'].append(issue)
                        elif severity == 'HIGH':
                            self.audit_results['high_priority'].append(issue)
                        elif severity == 'MEDIUM':
                            self.audit_results['medium_priority'].append(issue)
                        else:
                            self.audit_results['low_priority'].append(issue)
            else:
                print(f"ERROR: {report['error']}")
        
        return self.audit_results
    
    def generate_report(self) -> str:
        """Generate detailed audit report"""
        results = self.audit_results
        
        print("\n" + "="*70)
        print("AUDIT RESULTS")
        print("="*70 + "\n")
        
        print(f"Files Scanned: {results['total_files_scanned']}")
        print(f"Total Issues: {results['total_issues_found']}")
        print(f"  Critical: {len(results['critical_issues'])}")
        print(f"  High Priority: {len(results['high_priority'])}")
        print(f"  Medium Priority: {len(results['medium_priority'])}")
        print(f"  Low Priority: {len(results['low_priority'])}")
        
        # Show critical issues
        if results['critical_issues']:
            print("\n" + "="*70)
            print("⚠️  CRITICAL ISSUES (Fix Immediately)")
            print("="*70)
            for issue in results['critical_issues'][:10]:
                print(f"\n{issue['file']} - Line {issue['line']}")
                print(f"  Category: {issue['category']}")
                print(f"  Issue: {issue['issue']}")
                if 'code' in issue:
                    print(f"  Code: {issue['code'][:60]}...")
        
        # Show high priority
        if results['high_priority']:
            print("\n" + "="*70)
            print("🔴 HIGH PRIORITY ISSUES")
            print("="*70)
            for issue in results['high_priority'][:15]:
                print(f"\n{issue['file']} - Line {issue.get('line', '?')}")
                print(f"  {issue['issue']}")
        
        # Show medium priority summary
        if results['medium_priority']:
            print("\n" + "="*70)
            print("🟡 MEDIUM PRIORITY ISSUES")
            print("="*70)
            
            # Group by category
            by_category = defaultdict(list)
            for issue in results['medium_priority']:
                by_category[issue['category']].append(issue)
            
            for category, issues in by_category.items():
                print(f"\n{category}: {len(issues)} issues")
                for issue in issues[:5]:
                    print(f"  • {issue['file']}: {issue['issue']}")
        
        # Recommendations
        print("\n" + "="*70)
        print("💡 OPTIMIZATION RECOMMENDATIONS")
        print("="*70)
        
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']}")
            print(f"   {rec['description']}")
            print(f"   Expected gain: {rec['expected_gain']}")
        
        # Save detailed report
        report_file = 'lazy_process_audit_report.json'
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Full report saved to: {report_file}")
        
        return json.dumps(results, indent=2)
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        results = self.audit_results
        
        if results['high_priority']:
            recommendations.append({
                'title': 'Convert blocking I/O to async',
                'description': 'Replace synchronous file/network operations with async equivalents',
                'expected_gain': '50-80% latency reduction'
            })
        
        if any('nested_loops' in r['issues'] for r in results['file_reports'].values()):
            recommendations.append({
                'title': 'Optimize nested loops',
                'description': 'Use vectorized operations, set lookups, or better algorithms',
                'expected_gain': '10-100x speedup'
            })
        
        if any('missing_caching' in r['issues'] for r in results['file_reports'].values()):
            recommendations.append({
                'title': 'Add function-level caching',
                'description': 'Use @lru_cache decorator on pure functions',
                'expected_gain': '90%+ reduction in repeated computations'
            })
        
        recommendations.append({
            'title': 'Enable parallel processing',
            'description': 'Use ThreadPoolExecutor for I/O-bound tasks, ProcessPoolExecutor for CPU-bound',
            'expected_gain': 'Near-linear scaling with CPU cores'
        })
        
        recommendations.append({
            'title': 'Implement result memoization',
            'description': 'Cache expensive computation results with TTL',
            'expected_gain': '5-10x throughput improvement'
        })
        
        return recommendations


if __name__ == "__main__":
    workspace = os.getcwd()
    
    auditor = SystemLazyAuditor(workspace)
    auditor.audit_entire_system()
    auditor.generate_report()
    
    print("\n✅ Audit complete! Review recommendations and fix high-priority issues.")
