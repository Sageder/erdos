"""
G_04_selfridge_structure.py -- Route G, step 4.

CLAIMS TESTED (all exact; bitmask arithmetic mod 360 / mod 180, integer only):

 (1) INDEPENDENT VERIFICATION of the Selfridge-style covering found by G_02_dfs:
        0(2) 1(4) 3(6) 7(10) 11(12) 1(18) 1(30) 7(36) 23(40) 19(60) 67(72) 175(180)
     -- every modulus n has n+1 prime, moduli pairwise distinct and >1, and the union is
     ALL of Z/360 (exhaustive sweep of the 360 residues).

 (2) STRUCTURE LEMMA (proved in FINDINGS.md, re-verified here on this system):
     all moduli of E are even, hence every class of an E-system lies inside one parity
     class; the modulus-2 class therefore carries an entire parity class.

 (3) Exactly which residues mod 360 the modulus-2 class carries, and exactly which residues
     become uncovered if it is deleted.

 (4) The MINIMUM possible "exclusive load" of the modulus-2 class, over ALL coverings using
     moduli among the divisors of 360 of the form p-1:  i.e. the minimum, over all such
     coverings containing a class mod 2, of #{r : r covered by the mod-2 class only}.

 (5) Enumeration of all subsets of D_H(180) = {2,3,5,6,9,15,18,20,30,36,90} that support a
     covering of Z (the "halved" world), with the inclusion-minimal ones listed.

CONCLUSION: see printed output; recorded in attempts/route-G-selfridge/FINDINGS.md.
"""
from fractions import Fraction
from itertools import combinations
from sympy import isprime, divisors

# ---------------------------------------------------------------- helpers
def mask_of(a, m, L):
    """bitmask (as python int) of the class a mod m inside Z/L"""
    x = 0
    for r in range(a % m, L, m):
        x |= 1 << r
    return x

FULL = lambda L: (1 << L) - 1

def covers(classes, L):
    u = 0
    for a, m in classes:
        u |= mask_of(a, m, L)
    return u == FULL(L), u

def uncovered_list(u, L):
    return [r for r in range(L) if not (u >> r) & 1]

# ---------------------------------------------------------------- (1)(2)(3)
SYS = [(0,2),(1,4),(3,6),(7,10),(11,12),(1,18),(1,30),(7,36),(23,40),(19,60),(67,72),(175,180)]
L = 360

print("="*78)
print("(1) INDEPENDENT VERIFICATION of the Selfridge-style system (p >= 3)")
mods = [m for _, m in SYS]
print("  moduli:", sorted(mods))
assert len(set(mods)) == len(mods), "moduli not distinct"
assert all(m > 1 for m in mods)
for m in sorted(mods):
    assert isprime(m + 1), m
    assert 360 % m == 0, m
print("  distinct, all > 1, all divide 360                              OK")
print("  n -> n+1 :", {m: m + 1 for m in sorted(mods)})
print("  every n+1 prime                                                OK")
ok, u = covers(SYS, L)
print("  exhaustive sweep of Z/360 : covered =", bin(u).count('1'), "/ 360 ->", ok)
assert ok
# also verify directly on a raw integer range, second independent method
bad = [x for x in range(-3600, 3601) if not any((x - a) % m == 0 for a, m in SYS)]
print("  brute force over x in [-3600,3600] : uncovered =", len(bad), "        OK")
assert not bad
print("  ==> VERIFIED covering system, all moduli of the form p-1, p prime >= 3.")
print("      (p = 3,5,7,11,13,19,31,37,41,61,73,181)")
print("      reciprocal sum =", sum(Fraction(1, m) for m in mods))

print()
print("="*78)
print("(2)/(3) the load of the modulus-2 class")
c2 = [(a, m) for a, m in SYS if m == 2][0]
rest = [(a, m) for a, m in SYS if m != 2]
m2mask = mask_of(*c2, L)
_, urest = covers(rest, L)
carried = [r for r in range(L) if (m2mask >> r) & 1]
exclusive = [r for r in range(L) if (m2mask >> r) & 1 and not (urest >> r) & 1]
print("  mod-2 class is", c2, "-> carries the", len(carried), "residues r = 0 mod 2")
print("  parities of the other 11 classes:", sorted(set(a % 2 for a, m in rest)),
      "(all ODD -- the structure lemma in action)")
print("  residues uncovered after deleting the mod-2 class:", len(exclusive))
assert exclusive == carried == list(range(0, 360, 2))
print("  they are EXACTLY the 180 even residues mod 360.")
print("  => in this system the modulus-2 class is doing a full parity class of work.")

print()
print("="*78)
print("(4)/(5) halved world:  D_H(180) and its covering subsets")
DH180 = [d for d in divisors(180) if d >= 2 and isprime(2*d + 1)]
print("  D_H(180) =", DH180, " sum =", sum(Fraction(1,m) for m in DH180))
M = 180

import subprocess, os
BIN02 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G_02_dfs")
BIN03 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G_03_maxcov")

def supports_covering(pool, M):
    """exact (delegated to the C DFS G_02_dfs): does `pool` admit a covering of Z/M?"""
    r = subprocess.run([BIN02, str(M), ",".join(map(str, sorted(pool)))],
                       capture_output=True, text=True)
    if "BEST deficiency = 0" in r.stdout:
        line = [l for l in r.stdout.splitlines() if l.startswith("CLASSES:")][0]
        import re
        return [(int(a), int(m)) for a, m in re.findall(r"(\d+)\(mod (\d+)\)", line)]
    return None

def maxcov(pool, M):
    """exact maximum number of residues of Z/M coverable by distinct moduli from pool
       (delegated to the C branch-and-bound G_03_maxcov)."""
    if not pool:
        return 0, []
    r = subprocess.run([BIN03, str(M), ",".join(map(str, sorted(pool)))],
                       capture_output=True, text=True)
    import re
    mc = int(re.search(r"MAX COVERED = (\d+)", r.stdout).group(1))
    line = [l for l in r.stdout.splitlines() if l.startswith("CLASSES:")][0]
    cls = [(int(a), int(m)) for a, m in re.findall(r"(\d+)\(mod (\d+)\)", line)]
    assert "EXHAUSTIVE" in r.stdout
    return mc, cls

from itertools import combinations
cov_sets = []
for k in range(1, len(DH180)+1):
    for S in combinations(DH180, k):
        if sum(Fraction(1,m) for m in S) <= 1: continue
        if any(set(T) <= set(S) for T in cov_sets):   # only keep inclusion-minimal
            continue
        if supports_covering(list(S), M) is not None:
            cov_sets.append(S)
print("  inclusion-MINIMAL subsets of D_H(180) supporting a covering of Z:", len(cov_sets))
for S in cov_sets:
    w = supports_covering(list(S), M)
    print("     ", list(S), " sum =", sum(Fraction(1,m) for m in S),
          " witness:", sorted(w, key=lambda t:t[1]))

print()
print("  --- minimum exclusive load of the modulus-2 class over ALL divisor-of-360 systems ---")
print("  A covering of Z/360 containing a class mod 2 consists of: the mod-2 class (one whole")
print("  parity), an H-covering A of the opposite parity, and optional extra classes B on the")
print("  mod-2 side, with A,B disjoint subsets of D_H(180).  The residues carried ONLY by the")
print("  mod-2 class number  180 - maxcov(B).  maxcov is monotone, so it suffices to let A run")
print("  over the inclusion-minimal covering subsets and take B = D_H(180) \\ A.")
bestload=None
for S in cov_sets:
    comp=[m for m in DH180 if m not in S]
    mc, mcls = maxcov(comp, M)
    load = 180 - mc
    print(f"     A={list(S)}  ->  B={comp}  maxcov(B)={mc}  exclusive load={load}")
    if bestload is None or load < bestload[0]:
        bestload=(load, list(S), comp, sorted(mcls,key=lambda t:t[1]) if mcls else [])
print()
print("  MINIMUM exclusive load of the mod-2 class =", bestload[0], "residues mod 360")
print("     achieved with H-covering A =", bestload[1])
print("     leftover pool B =", bestload[2])
print("     optimal B-classes (in Z/180) =", bestload[3])
