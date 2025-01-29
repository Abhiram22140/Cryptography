import math

def analyze_dlp_security(g, p, y):
    if not (isinstance(g, int) and isinstance(p, int) and isinstance(y, int)):
        raise ValueError("All inputs must be integers.")
    if p <= 2:
        raise ValueError("Prime number p must be greater than 2.")
    if not (0 < g < p and 0 < y < p):
        raise ValueError("Values of g and y must be in the range (0, p).")

    def is_primitive_root(g, p):
        required_set = set(num for num in range(1, p) if math.gcd(num, p) == 1)
        actual_set = set(pow(g, powers, p) for powers in range(1, p))
        return required_set == actual_set

    
    security_level = "High" if is_primitive_root(g, p) else "Low"
    return f"Security Level: {security_level}"

g, p, y = 6, 41, 9
print(analyze_dlp_security(g, p, y))
