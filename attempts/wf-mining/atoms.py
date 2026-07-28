#!/usr/bin/env python3
"""
ATOM COMPOSITION and the PRIME-CLASS GRAPH.

Every maximal run of a solution is a chain of consecutive integers, hence a chain of
PAIRWISE COPRIME integers.  Assign each element n to the class lpf(n) (largest prime
factor).  Then every adjacency n ~ n+1 is an edge between two different classes.
A solution is therefore a "gluing" of the per-prime cofactor gadgets p*A_p along
consecutive-integer edges.

Measured here:
  (1) the joint distribution of (lpf(n), lpf(n+1)) over all adjacencies;
  (2) smooth/rough asymmetry: for an adjacency, min vs max of the two lpf's;
  (3) the prime-class graph of individual far-out solutions (which classes touch);
  (4) how many elements of a class are "anchored" (adjacent to a smoother element).
"""
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat
from mult import factor

S = load()
FAR = [U for U in S if U[0] >= 30]


def lpf(n):
    return max(factor(n))


print("=== (1) joint distribution of (lpf(n), lpf(n+1)) over adjacencies ===")
J = Counter()
for U in S:
    Us = set(U)
    for n in U:
        if n + 1 in Us:
            a, b = lpf(n), lpf(n + 1)
            J[(min(a, b), max(a, b))] += 1
tot = sum(J.values())
print("   total adjacencies:", tot)
for k, v in J.most_common(25):
    print("     (%3d,%3d) : %6.3f%%" % (k[0], k[1], 100.0 * v / tot))

print("\n=== (2) smooth/rough asymmetry of an atom ===")
mn = Counter()
mx = Counter()
for (a, b), v in J.items():
    mn[a] += v
    mx[b] += v
print("   distribution of min(lpf) over atoms:",
      ", ".join("%d:%.1f%%" % (p, 100.0 * mn[p] / tot) for p in sorted(mn) if mn[p] / tot > 0.01))
print("   distribution of max(lpf) over atoms:",
      ", ".join("%d:%.1f%%" % (p, 100.0 * mx[p] / tot) for p in sorted(mx) if mx[p] / tot > 0.01))
r = sum(v for (a, b), v in J.items() if a <= 5)
print("   share of atoms with min(lpf) <= 5 (one element is 5-smooth): %.4f" % (r / tot))
r = sum(v for (a, b), v in J.items() if a <= 7)
print("   share of atoms with min(lpf) <= 7                         : %.4f" % (r / tot))
r = sum(v for (a, b), v in J.items() if b >= 17)
print("   share of atoms with max(lpf) >= 17                        : %.4f" % (r / tot))

print("\n=== (3) prime-class graph of the largest far-out solutions ===")
for U in sorted(FAR, key=lambda u: -u[0])[:2]:
    Us = set(U)
    cls = defaultdict(list)
    for n in U:
        cls[lpf(n)].append(n)
    E = Counter()
    for n in U:
        if n + 1 in Us:
            a, b = lpf(n), lpf(n + 1)
            E[(min(a, b), max(a, b))] += 1
    print("  T=%d N=%d |U|=%d : classes %s" % (U[0], U[-1], len(U), sorted(cls)))
    print("     class sizes: %s" % {p: len(v) for p, v in sorted(cls.items())})
    print("     #edges=%d over %d class pairs; degree of each class:" % (sum(E.values()), len(E)))
    deg = Counter()
    for (a, b), v in E.items():
        deg[a] += v
        deg[b] += v
    print("       %s" % dict(sorted(deg.items())))
    iso = [p for p in cls if deg[p] == 0]
    print("     classes with NO adjacency (impossible unless class internal): %s" % iso)

print("\n=== (4) 'anchoring': is every rough element adjacent to a smoother one? ===")
anch = Counter()
for U in S:
    Us = set(U)
    for n in U:
        q = lpf(n)
        nb = [m for m in (n - 1, n + 1) if m in Us]
        if not nb:
            continue
        anch[(q >= 17, min(lpf(m) for m in nb) < q)] += 1
t2 = sum(anch.values())
for k, v in sorted(anch.items()):
    print("    rough(lpf>=17)=%s , has-smoother-neighbour=%s : %6.2f%%" % (k[0], k[1], 100.0 * v / t2))
