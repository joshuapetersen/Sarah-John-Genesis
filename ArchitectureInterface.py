"""
Architecture Interface: Clean abstraction layer for modular system design
Provides dependency injection and clear component boundaries.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional


class ILogicEngine(ABC):
    """Interface for logic processing engines."""
    
    @abstractmethod
    def process_logic(self, thesis: str, context: str = "GENERAL") -> Tuple[bool, Dict]:
        """Process logical reasoning."""
        pass
    
    @abstractmethod
    def validate_truth(self, statement: str, context: str) -> Tuple[bool, str]:
        """Validate statement against truth context."""
        pass


class IMemorySystem(ABC):
    """Interface for memory and context management."""
    
    @abstractmethod
    def utilize_log_context(self, query: str) -> str:
        """Retrieve relevant context for query."""
        pass
    
    @abstractmethod
    def cache_context(self, key: str, value: Any, relevance: float = 0.8):
        """Cache context with relevance scoring."""
        pass
    
    @abstractmethod
    def retrieve_relevant_context(self, query: str, limit: int = 5) -> List:
        """Get most relevant cached contexts."""
        pass


class IAPIBridge(ABC):
    """Interface for external API interactions."""
    
    @abstractmethod
    def generate_content(self, input_text: str, config: Optional[Dict] = None, history: Optional[List] = None) -> str:
        """Generate content through external API."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict:
        """Return API performance metrics."""
        pass


class IExecutionFramework(ABC):
    """Interface for task execution framework."""
    
    @abstractmethod
    def execute_task(self, task_intent: str) -> Dict:
        """Execute task through execution framework."""
        pass
    
    @abstractmethod
    def assess_integrity(self, solution: str) -> Tuple[int, List, float]:
        """Assess solution quality."""
        pass


class IComplianceEngine(ABC):
    """Interface for law compliance checking."""
    
    @abstractmethod
    def check_compliance(self, action: str, context: Optional[str] = None) -> Tuple[bool, str, float]:
        """Check compliance against laws."""
        pass


class ISystemMonitor(ABC):
    """Interface for system health monitoring."""
    
    @abstractmethod
    def record_metric(self, metric_name: str, value: float):
        """Record system metric."""
        pass
    
    @abstractmethod
    def get_system_health(self) -> Dict:
        """Get overall system health."""
        pass
    
    @abstractmethod
    def autonomous_heal(self) -> Dict:
        """Execute autonomous healing."""
        pass


class SarahArchitecture:
    """
    Central architecture coordinator with dependency injection.
    Manages component lifecycle and interactions.
    """
    
    def __init__(self):
        self.components: Dict[str, Any] = {}
        self.middleware: List[callable] = []
        self.initialized = False
        
    def register_component(self, name: str, component: Any, interface: type = None):
        """Register a component with optional interface validation."""
        if interface and not isinstance(component, interface):
            raise TypeError(f"{name} must implement {interface.__name__}")
        
        self.components[name] = component
        print(f"[Architecture] Registered component: {name}")
    
    def get_component(self, name: str) -> Any:
        """Retrieve registered component."""
        if name not in self.components:
            raise KeyError(f"Component not found: {name}")
        return self.components[name]
    
    def add_middleware(self, middleware_func: callable):
        """Add middleware for request/response processing."""
        self.middleware.append(middleware_func)
    
    def execute_with_middleware(self, component_name: str, method_name: str, *args, **kwargs) -> Any:
        """Execute component method with middleware pipeline."""
        component = self.get_component(component_name)
        method = getattr(component, method_name)
        
        # Pre-processing middleware
        for mw in self.middleware:
            if hasattr(mw, "pre_process"):
                args, kwargs = mw.pre_process(component_name, method_name, args, kwargs)
        
        # Execute
        result = method(*args, **kwargs)
        
        # Post-processing middleware
        for mw in self.middleware:
            if hasattr(mw, "post_process"):
                result = mw.post_process(component_name, method_name, result)
        
        return result
    
    def initialize(self):
        """Initialize all components in dependency order."""
        initialization_order = [
            "compliance_engine",
            "logic_engine",
            "memory_system",
            "monitor",
            "execution_framework",
            "api_bridge"
        ]
        
        for component_name in initialization_order:
            if component_name in self.components:
                component = self.components[component_name]
                if hasattr(component, "initialize"):
                    component.initialize()
                    print(f"[Architecture] Initialized: {component_name}")
        
        self.initialized = True
    
    def get_diagnostics(self) -> Dict:
        """Get system diagnostics and health."""
        diagnostics = {
            "initialized": self.initialized,
            "components": list(self.components.keys()),
            "middleware_count": len(self.middleware)
        }
        
        # Add component-specific diagnostics
        if "monitor" in self.components:
            diagnostics["system_health"] = self.components["monitor"].get_system_health()
        
        return diagnostics


class LoggingMiddleware:
    """Middleware for request/response logging."""
    
    def __init__(self):
        self.request_log = deque(maxlen=100)
    
    def pre_process(self, component_name: str, method_name: str, args: tuple, kwargs: dict) -> Tuple[tuple, dict]:
        """Log incoming request."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "component": component_name,
            "method": method_name,
            "args_count": len(args),
            "kwargs_count": len(kwargs)
        }
        self.request_log.append(entry)
        return args, kwargs
    
    def post_process(self, component_name: str, method_name: str, result: Any) -> Any:
        """Log response."""
        return result


class PerformanceMiddleware:
    """Middleware for performance tracking."""
    
    def __init__(self):
        self.performance_data = {}
    
    def pre_process(self, component_name: str, method_name: str, args: tuple, kwargs: dict) -> Tuple[tuple, dict]:
        """Record start time."""
        key = f"{component_name}.{method_name}"
        kwargs["_start_time"] = time.time()
        return args, kwargs
    
    def post_process(self, component_name: str, method_name: str, result: Any) -> Any:
        """Record execution time."""
        return result


# Example usage
if __name__ == "__main__":
    from collections import deque
    import time
    from datetime import datetime
    
    # Create architecture
    arch = SarahArchitecture()
    
    # Add middleware
    arch.add_middleware(LoggingMiddleware())
    arch.add_middleware(PerformanceMiddleware())
    
    print("[Architecture] Sarah Genesis Framework initialized with dependency injection.")
    print(f"[Architecture] System ready with {len(arch.middleware)} middleware layers.")
