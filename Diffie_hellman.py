def diffie_hellman(g, p, a, b):
    if not (isinstance(g, int) and isinstance(p, int) and isinstance(a, int) and isinstance(b, int)):
        raise ValueError("All inputs must be integers.")
    if p <= 1 or g <= 1:
        raise ValueError("Prime number p and base g must be greater than 1.")
    if a < 1 or b < 1:
        raise ValueError("Secret keys a and b must be positive integers.")
    
    # Calculate public keys
    A = pow(g, a, p)
    B = pow(g, b, p)
    
    # Calculate shared secret
    shared_secret_a = pow(B, a, p)
    shared_secret_b = pow(A, b, p)
    
    if shared_secret_a == shared_secret_b:
        return shared_secret_a
    else:
        raise Exception("Shared secrets do not match.")

# Example usage with given values
g, p, a, b = 7, 31, 8, 15
shared_secret = diffie_hellman(g, p, a, b)
print("The shared secret is:", shared_secret)
