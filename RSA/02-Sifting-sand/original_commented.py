# Public parameters copied from the supplied JSON.
n = 34664911185892166593
e = 65537
import sympy

factors = sympy.factorint(n)
# Iterating over a dictionary gives its keys. The values are multiplicities.
# After this assignment, the name list shadows Python's built-in list type.
list = list(factors)
# These indices assume there are exactly two distinct prime factors.
p = list[0]
q = list[1]
# Each print displays an intermediate result for inspection.
print(p)
print(q)

# Euler's totient formula here assumes both prime factors occur once.
euler = (p-1)*(q-1)
print(euler)

# The exponent -1 requests a modular inverse. It exists if gcd(e, euler) = 1.
d = pow(e, -1 , euler)
print(d)