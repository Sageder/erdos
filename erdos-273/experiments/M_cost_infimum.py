"""
CLAIM TESTED: Lemma M2 (attempts/route-M-main/COST_INFIMUM.md) — the doubling map
  D(C) = {0 mod 2} u {(2a+1) mod 2n : (a,n) in C}
sends a distinct-moduli covering system to a distinct-moduli covering system with
cost(D(C)) = 1/2 + cost(C)/2, so iterating drives the reciprocal cost to 1.

CONCLUSION: verified for C_0..C_8; costs are exactly 1 + (1/3)*2^-k. Hence the infimum of
sum(1/n) over distinct-moduli covering systems is 1 (not attained), and reciprocal-budget
counting alone can never decide Erdos 273.
"""
from fractions import Fraction
from math import lcm

def is_covering(C):
    L = 1
    for _, n in C: L = lcm(L, n)
    cov = bytearray(L)
    for a, n in C:
        for r in range(a % n, L, n): cov[r] = 1
    return all(cov), L

def double(C):
    return [(0, 2)] + [((2*a + 1) % (2*n), 2*n) for (a, n) in C]

C = [(0,2),(0,3),(1,4),(5,6),(7,12)]
for k in range(9):
    mods = [n for _, n in C]
    assert len(set(mods)) == len(mods), "moduli not distinct"
    assert all(n > 1 for n in mods)
    ok, L = is_covering(C)
    cost = sum(Fraction(1, n) for n in mods)
    print(f"C_{k}: {len(C):3d} classes, lcm = {L:12d}, cost = {str(cost):>18} = {float(cost):.9f}, "
          f"covering = {ok}, expected = {Fraction(1)+Fraction(1,3)/2**k}")
    assert ok, "not a covering"
    assert cost == Fraction(1) + Fraction(1,3)/2**k
    if L > 2*10**7: 
        print("   (stopping: next lcm would exceed the sweep limit)"); break
    C = double(C)
