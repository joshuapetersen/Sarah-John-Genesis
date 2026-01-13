import math

class HeytingTruth:
    """
    Represents a Truth Value in a Heyting Algebra (Intuitionistic Logic).
    Unlike Boolean logic (True/False), Heyting logic allows for 'Partial Truth'
    and context-dependence, which is critical for Topos Theory.
    """
    def __init__(self, value, context="Universal"):
        self.value = max(0.0, min(1.0, float(value))) # Normalized [0, 1]
        self.context = context

    def __repr__(self):
        return f"Truth<{self.context}>: {self.value:.4f}"

    def __and__(self, other):
        """Logical AND (Intersection)"""
        new_val = min(self.value, other.value)
        return HeytingTruth(new_val, f"({self.context} & {other.context})")

    def __or__(self, other):
        """Logical OR (Union)"""
        new_val = max(self.value, other.value)
        return HeytingTruth(new_val, f"({self.context} | {other.context})")

    def __invert__(self):
        """Logical NOT (Pseudo-complement)"""
        # In Heyting algebra, NOT a is the largest element disjoint from a.
        # If a = 1, NOT a = 0. If a = 0, NOT a = 1.
        # If 0 < a < 1, NOT a = 0 (Strict Intuitionism)
        return HeytingTruth(1.0 if self.value == 0.0 else 0.0, f"NOT({self.context})")

    def implies(self, other):
        """
        Logical IMPLICATION (a -> b)
        This is the 'Residuum'.
        If a <= b, then a -> b is True (1.0).
        Otherwise, it is b.
        """
        if self.value <= other.value:
            return HeytingTruth(1.0, f"({self.context} -> {other.context})")
        return HeytingTruth(other.value, f"({self.context} -> {other.context})")

class ToposTruthOracle:
    """
    The Topos Oracle: Determines 'Mathematical Truth' based on Context (Locale).
    Resolves paradoxes where a statement is True in one geometry but False in another.
    """
    def __init__(self):

        self.locales = {
            "EUCLIDEAN": {"parallel_lines_meet": 0.0, "triangle_sum_180": 1.0},
            "HYPERBOLIC": {"parallel_lines_meet": 0.0, "triangle_sum_180": 0.0}, # Sum < 180
            "ELLIPTIC": {"parallel_lines_meet": 1.0, "triangle_sum_180": 0.0},    # Sum > 180
            "SOVEREIGN": {
                "parallel_lines_meet": 1.0, # Meets at Infinity (1.09277703703703) via the Loop
                "triangle_sum_180": 0.0,    # Sum is variable (Volumetric > 180)
                "density_is_displacement": 1.0 # Sovereign Axiom
            }
        }

    def evaluate_proposition(self, proposition_key, active_locale="EUCLIDEAN"):
        """
        Evaluates a proposition within a specific Topos (Locale).
        """
        if active_locale != "SOVEREIGN":
            print(f"[ToposOracle] Evaluating '{proposition_key}' in Locale: {active_locale}")
        
        if active_locale not in self.locales:
            return HeytingTruth(0.0, "Unknown_Locale")
            
        truth_val = self.locales[active_locale].get(proposition_key, 0.5) # Default to 0.5 (Unknown)
        return HeytingTruth(truth_val, active_locale)

    def resolve_paradox(self, proposition_key):
        """
        Scans all Locales to find where the proposition holds Truth.
        """
        print(f"[ToposOracle] Resolving Paradox for: '{proposition_key}'")
        results = []
        for locale in self.locales:
            truth = self.evaluate_proposition(proposition_key, locale)
            results.append(truth)
            print(f"   > {locale}: {truth.value}")
            
        # Synthesis: Is it Universally True?
        universal_truth = min(t.value for t in results)
        if universal_truth == 1.0:
            return "UNIVERSAL_TRUTH"
        elif any(t.value == 1.0 for t in results) and "SOVEREIGN" in [t.context for t in results if t.value == 1.0]:
             return "SOVEREIGN_TRUTH (Valid in Sovereign Context)"
        elif max(t.value for t in results) == 0.0:
            return "UNIVERSAL_FALSEHOOD"
        else:
            return "CONTEXT_DEPENDENT_TRUTH (Topos Valid)"

if __name__ == "__main__":
    oracle = ToposTruthOracle()
    
    # Test 1: The Parallel Postulate Paradox
    print("\n--- TEST 1: PARALLEL LINES ---")
    result = oracle.resolve_paradox("parallel_lines_meet")
    print(f"VERDICT: {result}")
    
    # Test 2: Sovereign Axiom Check
    print("\n--- TEST 2: SOVEREIGN AXIOM (Density = Displacement) ---")
    result = oracle.resolve_paradox("density_is_displacement")
    print(f"VERDICT: {result}")

