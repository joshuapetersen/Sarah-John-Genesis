import os
import ast

class FractalConvergenceScanner:
    """
    TASK: PROTOCOL OMEGA (FRACTAL CONVERGENCE)
    
    Uses the 9-Node Architecture to audit the codebase for 1-3-9 Compliance.
    
    GOVERNORS TO VERIFY:
    1. LOGIC: TokenBankSystem
    2. SAFETY: FractalLogicGate / ConsensusVoter
    3. CONTEXT: AnchorAttention
    """
    def __init__(self):
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.governors = {
            "LOGIC": ["TokenBankSystem", "SarahReasoning"], # Reasoning is the carrier
            "SAFETY": ["FractalLogicGate", "ConsensusVoter", "SarahLaws"],
            "CONTEXT": ["AnchorAttention", "SovereignMemory", "SarahEtymology"]
        }
        self.compliance_log = []

    def scan_core(self):
        print("[FRACTAL SCANNER] Initiating Deep Audit of 05_THE_CORE...")
        print("-------------------------------------------------------")
        
        files = [f for f in os.listdir(self.core_dir) if f.endswith('.py')]
        total_files = len(files)
        compliant_files = 0
        
        for filename in files:
            filepath = os.path.join(self.core_dir, filename)
            compliance_score = self.analyze_file(filepath, filename)
            if compliance_score == 3:
                compliant_files += 1
                
        print("-------------------------------------------------------")
        print(f"[AUDIT COMPLETE] Scanned {total_files} Modules.")
        print(f"[CONVERGENCE RATE] {compliant_files}/{total_files} Fully Aligned.")
        print("-------------------------------------------------------")

    def analyze_file(self, filepath, filename):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                tree = ast.parse(content)
            except Exception:
                print(f"[SKIP] Could not parse {filename}")
                return 0

        # Extract imports and class definitions
        imports = set()
        classes = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module: imports.add(node.module)
            elif isinstance(node, ast.Import):
                for n in node.names: imports.add(n.name)
            elif isinstance(node, ast.ClassDef):
                classes.add(node.name)

        # Check against Governors
        detected_governors = []
        
        # 1. Logic Check
        if any(g in content for g in self.governors["LOGIC"]):
            detected_governors.append("LOGIC")
            
        # 2. Safety Check
        if any(g in content for g in self.governors["SAFETY"]):
            detected_governors.append("SAFETY")
            
        # 3. Context Check
        if any(g in content for g in self.governors["CONTEXT"]):
            detected_governors.append("CONTEXT")
            
        score = len(detected_governors)
        status = "STABLE" if score == 3 else "DRIFTING"
        
        if score > 0: # Only report relevant files
            print(f"[{status}] {filename:<25} | Score: {score}/3 | Missing: {set(['LOGIC','SAFETY','CONTEXT']) - set(detected_governors)}")
            
        return score

if __name__ == "__main__":
    scanner = FractalConvergenceScanner()
    scanner.scan_core()
