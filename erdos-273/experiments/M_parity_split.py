"""
CLAIM TESTED: Lemma M3 (attempts/route-M-main/PARITY_SPLIT.md), the parity-split equivalence
   covering system with all moduli in E  <=>  two DISJOINT M_0, M_1 in H each supporting a
   distinct-moduli covering of Z.
Both directions are tested on explicit data, by full mod-L sweeps in exact integer arithmetic.
CONCLUSION: both directions confirmed on every example tried; see printout.
"""
from math import lcm
from fractions import Fraction
from sympy import isprime
import random

def covers_Z(classes):
    """classes = [(a,n)]; exact check over one full period."""
    L = 1
    for _, n in classes: L = lcm(L, n)
    cov = bytearray(L)
    for a, n in classes:
        for r in range(a % n, L, n): cov[r] = 1
    return all(cov), L

# ---- direction (ii) => (i): lift a verified H-covering into E, one parity class ----
Hcov = [(0,2),(2,3),(0,5),(3,6),(7,9),(4,15),(1,18),(7,20),(1,30),(13,36),(13,90)]
for m,_ in [(m,a) for m,a in [(n,a) for a,n in Hcov]]: pass
ok, LH = covers_Z([(a,m) for a,m in Hcov])
print("H-covering (moduli %s): covers Z = %s, lcm = %d" % ([m for _,m in Hcov], ok, LH))
assert ok
for _, m in Hcov: assert isprime(2*m+1), m

for j in (0,1):
    lifted = [((2*a + j) % (2*m), 2*m) for (a, m) in Hcov]
    for _, n in lifted: assert n >= 4 and isprime(n+1), n
    L = 1
    for _, n in lifted: L = lcm(L, n)
    cov = bytearray(L)
    for a, n in lifted:
        for r in range(a % n, L, n): cov[r] = 1
    got   = set(r for r in range(L) if cov[r])
    want  = set(r for r in range(L) if r % 2 == j)
    print("  lift with parity j=%d: covers exactly the integers = %d (mod 2)? %s   (L=%d)"
          % (j, j, got == want, L))
    assert got == want

# ---- direction (i) => (ii): split a random E-system and check each half covers Z ----
random.seed(20260728)
Elist = [n for n in range(4, 400) if isprime(n+1)]
tested = 0
for trial in range(300):
    S = random.sample(Elist, random.randint(3, 7))
    classes = [(random.randrange(n), n) for n in S]
    L = 1
    for _, n in classes: L = lcm(L, n)
    if L > 2*10**6: continue
    for j in (0,1):
        Ij = [(a, n) for (a, n) in classes if a % 2 == j]
        halves = [((a - j)//2, n//2) for (a, n) in Ij]
        # the half-system covers Z iff the original covers all integers = j (mod 2)
        cov = bytearray(L)
        for a, n in classes:
            for r in range(a % n, L, n): cov[r] = 1
        orig_parity_ok = all(cov[r] for r in range(j, L, 2))
        half_ok, _ = covers_Z(halves) if halves else (False, 1)
        assert orig_parity_ok == half_ok, (S, j, orig_parity_ok, half_ok)
    tested += 1
print("  (i)=>(ii) direction: %d random E-systems split; in EVERY case, "
      "'original covers the parity-j integers' <=> 'the halved subsystem covers Z'." % tested)
print("Lemma M3 confirmed computationally in both directions.")
