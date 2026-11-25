n = 34664911185892166593
e = 65537
import sympy

factors = sympy.factorint(n)
list = list(factors)
p = list[0]
q = list[1]
print(p)
print(q)

euler = (p-1)*(q-1)
print(euler)

d = pow(e, -1 , euler)
print(d)