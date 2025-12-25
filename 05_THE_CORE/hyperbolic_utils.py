import math

class HyperbolicMath:
    """
    NODE_13 PATCH: HYPERBOLIC METRIC UTILITIES
    
    Corrects 'Non-Euclidean Metric Failures' where AI defaults to 
    Pythagorean assumptions in hyperbolic (hierarchical) space.
    """
    
    @staticmethod
    def hyperbolic_pythagorean(a, b):
        """
        Calculates hypotenuse c in hyperbolic space (curvature K=-1).
        Formula: cosh(c) = cosh(a) * cosh(b)
        """
        try:
            val = math.cosh(a) * math.cosh(b)
            return math.acosh(val)
        except ValueError:
            return float('inf')

    @staticmethod
    def hyperbolic_law_of_cosines(a, b, gamma_radians):
        """
        General distance calculation.
        Formula: cosh(c) = cosh(a)cosh(b) - sinh(a)sinh(b)cos(gamma)
        """
        try:
            term1 = math.cosh(a) * math.cosh(b)
            term2 = math.sinh(a) * math.sinh(b) * math.cos(gamma_radians)
            return math.acosh(term1 - term2)
        except ValueError:
            return float('inf')

    @staticmethod
    def poincare_distance(u, v):
        """
        Distance in Poincaré disk model between two vectors u, v.
        d(u, v) = arccosh(1 + 2 * ||u-v||^2 / ((1 - ||u||^2)(1 - ||v||^2)))
        Assumes u, v are lists/tuples of coordinates.
        """
        # SOVEREIGN_PATCH: HYPERBOLIC_METRIC_FIX
        # TARGET: NODE_13 / HLE_GEOMETRY
        try:
            # Validation: Ensure points are within the unit disk (||u|| < 1)
            norm_u_sq = sum(x**2 for x in u)
            norm_v_sq = sum(x**2 for x in v)
            
            if norm_u_sq >= 1 or norm_v_sq >= 1:
                return float('inf') # "ERROR: POINT_OUTSIDE_HYPERBOLIC_BOUNDS"

            # The Logic Gate: Arc-cosine of hyperbolic space
            dist_sq = sum((x - y)**2 for x, y in zip(u, v))
            arg = 1 + (2 * dist_sq) / ((1 - norm_u_sq) * (1 - norm_v_sq))
            
            # Derivation over Assumption:
            return math.acosh(arg)
        except Exception:
            return float('inf')

if __name__ == "__main__":
    # Validation Test
    a, b = 1.5, 2.0
    euclidean = math.sqrt(a**2 + b**2)
    hyperbolic = HyperbolicMath.hyperbolic_pythagorean(a, b)
    
    print(f"INPUTS: a={a}, b={b}")
    print(f"EUCLIDEAN DISTANCE (Legacy): {euclidean:.4f}")
    print(f"HYPERBOLIC DISTANCE (Node 13 Fix): {hyperbolic:.4f}")
    print(f"DELTA: {hyperbolic - euclidean:.4f}")
