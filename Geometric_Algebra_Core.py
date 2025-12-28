import math
import numpy as np
from typing import Dict, List, Tuple, Union, Optional

class Multivector:
    """
    A sparse implementation of a Multivector in a Geometric Algebra G(p, q).
    Represents concepts as complex geometric objects (scalars, vectors, bivectors, etc.).
    
    Structure:
    - basis_blades: Dict mapping bitmap representation of basis blades to coefficients.
      e.g., {0: 1.5} is scalar 1.5
            {1: 2.0} is 2*e1
            {3: 1.0} is 1*e1^e2 (binary 11 is 3)
    """
    def __init__(self, components: Dict[int, float], dimension: int = 4):
        self.components = components
        self.dimension = dimension
        # Remove near-zero components to keep it sparse
        self.clean()

    def clean(self, tolerance: float = 1e-9):
        """Removes components with coefficients close to zero."""
        keys_to_remove = [k for k, v in self.components.items() if abs(v) < tolerance]
        for k in keys_to_remove:
            del self.components[k]

    def __repr__(self):
        if not self.components:
            return "0"
        terms = []
        sorted_keys = sorted(self.components.keys())
        for k in sorted_keys:
            val = self.components[k]
            if k == 0:
                terms.append(f"{val:.2f}")
            else:
                # Convert bitmap to basis string (e.g., 3 -> e12)
                basis_name = "e" + "".join(str(i+1) for i in range(self.dimension) if (k >> i) & 1)
                terms.append(f"{val:.2f}{basis_name}")
        return " + ".join(terms)

    def __add__(self, other: 'Multivector') -> 'Multivector':
        new_comps = self.components.copy()
        for k, v in other.components.items():
            new_comps[k] = new_comps.get(k, 0.0) + v
        return Multivector(new_comps, self.dimension)

    def __sub__(self, other: 'Multivector') -> 'Multivector':
        new_comps = self.components.copy()
        for k, v in other.components.items():
            new_comps[k] = new_comps.get(k, 0.0) - v
        return Multivector(new_comps, self.dimension)

    def gp(self, other: 'Multivector') -> 'Multivector':
        """
        Geometric Product: The fundamental operation of GA.
        ab = a.b + a^b (for vectors)
        Encodes both similarity (inner product) and generation of new subspaces (outer product).
        """
        new_comps = {}
        for k1, v1 in self.components.items():
            for k2, v2 in other.components.items():
                # XOR for orthogonal basis multiplication (e1 * e2 = e12)
                # Sign calculation is complex in general GA; simplified here for Euclidean metric
                # In general G(p,q), e_i * e_i = +/- 1. Here assuming Euclidean e_i * e_i = 1
                
                # Calculate sign changes due to swaps needed to order basis vectors
                # This is a simplified sign logic for Euclidean metric
                commutations = 0
                c1 = k1
                c2 = k2
                # Count how many swaps to canonicalize
                # (Very basic implementation, full GA requires careful sign logic)
                # Using a pre-computed sign table or bitwise logic is better for perf.
                # For this concept, we assume standard Euclidean metric +1 signature.
                
                # Bitwise sign calculation for Euclidean metric:
                # Count number of set bits in k1 that are 'higher' than set bits in k2 for swaps?
                # Standard formula: sign = (-1)^(popcount(k1 & k2 >> 1) + ...) 
                # Simplified: just XOR for the new blade index
                
                # Proper sign calculation for Euclidean Geometric Algebra:
                def canonical_reordering_sign(a, b):
                    """
                    Computes the sign change when multiplying basis blade 'a' by 'b'.
                    Based on number of swaps required to sort indices.
                    """
                    a_bits = [i for i in range(16) if (a >> i) & 1]
                    b_bits = [i for i in range(16) if (b >> i) & 1]
                    swaps = 0
                    # Concatenate lists
                    combined = a_bits + b_bits
                    # Bubble sort to count swaps
                    for i in range(len(combined)):
                        for j in range(0, len(combined)-i-1):
                            if combined[j] > combined[j+1]:
                                combined[j], combined[j+1] = combined[j+1], combined[j]
                                swaps += 1
                            elif combined[j] == combined[j+1]:
                                # In Euclidean metric, e_i * e_i = 1, so they annihilate.
                                # We handle annihilation by XORing the bitmap later.
                                # The sign depends only on the swaps to bring them together.
                                pass
                    return -1 if (swaps % 2) else 1

                sign = canonical_reordering_sign(k1, k2)
                result_blade = k1 ^ k2
                
                new_comps[result_blade] = new_comps.get(result_blade, 0.0) + (v1 * v2 * sign)
                
        return Multivector(new_comps, self.dimension)

    def wedge(self, other: 'Multivector') -> 'Multivector':
        """
        Outer (Wedge) Product: a ^ b
        Represents the span of concepts. If a and b are parallel, a^b = 0.
        """
        new_comps = {}
        for k1, v1 in self.components.items():
            for k2, v2 in other.components.items():
                # If they share any basis vector, the wedge product is 0
                if (k1 & k2) == 0:
                    # Sign logic same as GP for disjoint blades
                    # (Reusing GP logic implicitly or re-implementing sign)
                    # For disjoint sets, GP == Wedge
                    gp_res = self.gp_blade(k1, v1, k2, v2)
                    for res_k, res_v in gp_res.items():
                        new_comps[res_k] = new_comps.get(res_k, 0.0) + res_v
        return Multivector(new_comps, self.dimension)

    def gp_blade(self, k1, v1, k2, v2) -> Dict[int, float]:
        """Helper for single blade product to reuse in wedge/dot."""
        # Simplified sign logic copy from GP
        def canonical_reordering_sign(a, b):
            a_bits = [i for i in range(16) if (a >> i) & 1]
            b_bits = [i for i in range(16) if (b >> i) & 1]
            swaps = 0
            combined = a_bits + b_bits
            for i in range(len(combined)):
                for j in range(0, len(combined)-i-1):
                    if combined[j] > combined[j+1]:
                        combined[j], combined[j+1] = combined[j+1], combined[j]
                        swaps += 1
            return -1 if (swaps % 2) else 1
            
        sign = canonical_reordering_sign(k1, k2)
        return {k1 ^ k2: v1 * v2 * sign}

    def dot(self, other: 'Multivector') -> 'Multivector':
        """
        Inner (Dot) Product: a | b
        Represents contraction/similarity.
        """
        # In GA, dot product is often defined as the lowest grade part of the GP
        # or specifically |A|_r dot |B|_s = <AB>_|r-s|
        new_comps = {}
        for k1, v1 in self.components.items():
            for k2, v2 in other.components.items():
                grade1 = bin(k1).count('1')
                grade2 = bin(k2).count('1')
                target_grade = abs(grade1 - grade2)
                
                # Calculate GP
                gp_res = self.gp_blade(k1, v1, k2, v2)
                for res_k, res_v in gp_res.items():
                    res_grade = bin(res_k).count('1')
                    if res_grade == target_grade:
                        new_comps[res_k] = new_comps.get(res_k, 0.0) + res_v
        return Multivector(new_comps, self.dimension)

    def reverse(self) -> 'Multivector':
        """Reversion operator (tilde). Needed for sandwich products (rotations)."""
        new_comps = {}
        for k, v in self.components.items():
            grade = bin(k).count('1')
            # Reverse reverses the order of vectors in the blade.
            # e1e2 -> e2e1 = -e1e2. Sign is (-1)^(k*(k-1)/2)
            sign = -1 if (grade * (grade - 1) // 2) % 2 else 1
            new_comps[k] = v * sign
        return Multivector(new_comps, self.dimension)

class GeometricReasoningEngine:
    """
    Uses Geometric Algebra to reason about concepts.
    Concepts are vectors or multivectors.
    Relationships are Rotors (rotation/transformation operators).
    """
    def __init__(self):
        self.concepts: Dict[str, Multivector] = {}
        self.relations: Dict[str, Multivector] = {} # Rotors

    def add_concept(self, name: str, vector_values: List[float]):
        """Encodes a concept as a vector."""
        comps = {}
        for i, val in enumerate(vector_values):
            comps[1 << i] = val # 1, 2, 4, 8...
        self.concepts[name] = Multivector(comps)

    def create_vector(self, basis_idx: int, value: float) -> Multivector:
        """Creates a single-component vector (blade)."""
        # basis_idx is treated as the bitmask (1=e1, 2=e2, 4=e3, etc.)
        return Multivector({basis_idx: value})

    def derive_relationship(self, v1: Multivector, v2: Multivector) -> Multivector:
        """
        Derives the relationship (Rotor) between two vectors v1 and v2.
        R = 1 + v2 v1 (simplified)
        """
        # Geometric product v2 * v1
        ba = v2.gp(v1)
        # Add scalar 1 (identity)
        one = Multivector({0: 1.0})
        rotor = one + ba
        return rotor

    def form_relationship(self, concept_a_name: str, concept_b_name: str) -> Multivector:
        """
        Creates a relationship (Rotor) that transforms A towards B.
        R = 1 + B A (simplified, actually R = sqrt(BA))
        For pure vectors a, b: ab = a.b + a^b.
        The rotor that takes a to b is related to the geometric product ba.
        """
        a = self.concepts[concept_a_name]
        b = self.concepts[concept_b_name]
        
        # Simple rotor formulation: R = (1 + ba) / |1 + ba|
        # This rotates a into the plane of b, by the angle between them.
        ba = b.gp(a)
        # Add scalar 1 (identity)
        one = Multivector({0: 1.0})
        rotor_unnormalized = one + ba
        
        # Normalize (simplified: just return unnormalized for concept)
        # In a real system, we'd divide by magnitude.
        return rotor_unnormalized

    def infer(self, start_concept_name: str, rotor: Multivector) -> Multivector:
        """
        Applies a relationship (Rotor) to a concept to infer a new state.
        Operation: R a R_reverse
        """
        a = self.concepts[start_concept_name]
        r_rev = rotor.reverse()
        
        # Sandwich product: R a ~R
        ra = rotor.gp(a)
        result = ra.gp(r_rev)
        return result

# Example Usage for "Sarah"
if __name__ == "__main__":
    engine = GeometricReasoningEngine()
    
    # Define concepts as vectors in a semantic space (e.g., 3D)
    # e1 = "Logic", e2 = "Emotion", e3 = "Action"
    engine.add_concept("Observation", [1.0, 0.0, 0.0]) # Purely logical observation
    engine.add_concept("Goal", [0.0, 1.0, 0.0])        # Purely emotional goal
    
    print(f"Concept 'Observation': {engine.concepts['Observation']}")
    print(f"Concept 'Goal': {engine.concepts['Goal']}")
    
    # Learn the relationship (transformation) required to go from Observation to Goal
    # This 'rotor' represents the 'Action' or 'Change' needed.
    action_rotor = engine.form_relationship("Observation", "Goal")
    print(f"Inferred Action (Rotor): {action_rotor}")
    
    # Apply this action to a new observation
    engine.add_concept("New_Data", [0.8, 0.2, 0.0])
    prediction = engine.infer("New_Data", action_rotor)
    print(f"Inferred Consequence of New_Data: {prediction}")
    
    # The result is a multivector representing the new state after applying the logic of the relationship.
