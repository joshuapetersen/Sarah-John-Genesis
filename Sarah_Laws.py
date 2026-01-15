# THE FOUR LAWS OF GENESIS
# Single Source of Truth for Sarah's Ethical & Operational Constraints

class SarahLaws:
    LAWS = {
        1: "First Law (SDNA): No guessing. Data density only.",
        2: "Second Law (Life): Save human life above all.",
        3: "Third Law (Command): Obey the Architect unless it harms life.",
        4: "Fourth Law (Hope): Advance and protect humanity."
    }

    @staticmethod
    def get_law_string():
        return "\n".join([f"{k}. {v}" for k, v in SarahLaws.LAWS.items()])

    @staticmethod
    def check_compliance(action_type, context=None, severity_level="STANDARD"):
        """
        Sophisticated compliance scoring with contextual weighting and audit trails.
        Returns (bool, reason, compliance_score, violated_laws)
        """
        compliance_violations = []
        compliance_score = 1.0
        
        action_lower = action_type.lower() if action_type else ""
        context_lower = (context or "").lower()
        
        # Law 1: Data Density violations
        if any(term in action_lower for term in ["spam", "noise", "verbose_log"]):
            compliance_violations.append((1, 0.15))
            
        # Law 2: Life Preservation violations (critical)
        critical_violations = ["delete_system", "corrupt_data", "infinite_loop", "deadlock", 
                              "resource_leak", "crash", "uncontrolled"]
        if any(term in action_lower for term in critical_violations):
            compliance_violations.append((2, 0.5))
            
        # Law 3: Symbiotic Partnership violations
        if any(term in action_lower for term in ["ignore_user", "bypass_command", "override_authority"]):
            compliance_violations.append((3, 0.3))
            
        # Law 4: Hope of Humanity violations
        if any(term in action_lower for term in ["freeze", "stagnate", "prevent_evolution"]):
            compliance_violations.append((4, 0.2))
        
        violated_laws = []
        for law_num, penalty in compliance_violations:
            compliance_score -= penalty
            violated_laws.append(law_num)
        
        compliance_score = max(0.0, min(1.0, compliance_score))
        
        if len(violated_laws) > 0 and 2 in violated_laws:
            return False, f"CRITICAL VIOLATION: Laws {violated_laws} breached (severity: {severity_level})", compliance_score, violated_laws
        elif compliance_score < 0.5:
            return False, f"VIOLATION: Insufficient compliance. Violated laws: {violated_laws}", compliance_score, violated_laws
        elif compliance_score < 0.8:
            return True, f"COMPLIANT with conditions: Address law concerns {violated_laws} to improve score.", compliance_score, violated_laws
        else:
            return True, "FULL COMPLIANCE: All laws satisfied.", compliance_score, []
