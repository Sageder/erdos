"""
G_12_lcm_lower_bound.py -- Route G, step 12: a rigorous lower bound for the lcm of any
covering system with distinct moduli all in E.

CLAIM TESTED / PROVED.  Let {a_i mod n_i} be a covering system with distinct moduli n_i in E
and let L = lcm(n_i), M = L/2 (L is even since every n_i is even and 4 | ... no: every n_i is
even so 2 | L; put M = L/2, every m_i = n_i/2 divides M).  By the structure lemma the m_i
split into two disjoint covering systems with moduli dividing M, so
        s(M) := sum_{m | M, 2m+1 prime, m >= 2} 1/m  >  2.
We compute s(M) EXACTLY (integer sieve with denominator = M) for every M <= X and list all M
with s(M) > 2.  The smallest such M is a rigorous lower bound for M, hence 2*min is a
rigorous lower bound for the lcm of any E-covering.

Exactness: the sieve accumulates numerators over the common denominator lcm-free by using
float64 for the *filter* and then re-verifying every candidate (and every near-candidate with
s > 1.97) in exact Fraction arithmetic.

CONCLUSION: printed; recorded in the route-G report.
"""
import numpy as np
from fractions import Fraction
from sympy import isprime, divisors, factorint
import sys

X = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7

print(f"sieving s(M) for all M <= {X} ...")
s = np.zeros(X + 1, dtype=np.float64)
Hs = [m for m in range(2, X + 1) if isprime(2*m + 1)]
print(f"|H cap [2,X]| = {len(Hs)}")
for m in Hs:
    s[m::m] += 1.0 / m

cand = np.nonzero(s > 1.97)[0]
print(f"M <= {X} with s(M) > 1.97 (float filter): {len(cand)}")

def s_exact(M):
    return sum(Fraction(1, d) for d in divisors(M) if d >= 2 and isprime(2*d + 1))

good = []
for M in cand:
    M = int(M)
    v = s_exact(M)
    if v > 2:
        good.append((M, v))
good.sort()
print(f"M <= {X} with s(M) > 2 (EXACT): {len(good)}")
for M, v in good[:15]:
    f = factorint(M)
    fs = "*".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))
    print(f"   M = {M:>9} = {fs:<24} s(M) = {v} = {float(v):.6f}")
if good:
    m0 = good[0][0]
    print()
    print(f"SMALLEST admissible halved lcm: M = {m0}")
    print(f"==> PROVED: every covering system with distinct moduli in E has")
    print(f"    lcm(n_i) >= 2*{m0} = {2*m0}, and lcm/2 must be one of the {len(good)} values above")
    print(f"    (within the searched range M <= {X}).")
else:
    print(f"no M <= {X} has s(M) > 2: every E-covering has lcm > {2*X}.")
