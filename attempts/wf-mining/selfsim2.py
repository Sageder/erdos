#!/usr/bin/env python3
"""SELF-SIMILARITY, fast version using integer bitmasks.  Exact arithmetic only."""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat

S = load()
M = [sum(1 << x for x in U) for U in S]
byT = defaultdict(list)
for i, U in enumerate(S):
    byT[U[0]].append(i)


def dbl(U, sh):
    m = 0
    for n in U:
        m |= (1 << (2 * n - sh)) | (1 << (2 * n + 1 - sh))
    return m


print("=== (b) best overlap of a doubling image D_sigma(U) with a corpus solution ===")
best = []
for i, U in enumerate(S):
    if U[0] < 10:          # 2T < 20 lands in the huge low-T buckets; skip
        continue
    for sh in (0, 1):
        D = dbl(U, sh)
        nd = 2 * len(U)
        lo = 2 * U[0] - sh
        for t in range(max(3, lo - 2), lo + 3):
            for j in byT.get(t, ()):
                inter = bin(D & M[j]).count("1")
                if 2 * inter >= nd:
                    best.append((inter / (nd + len(S[j]) - inter), nd, len(S[j]), inter, sh, U[0], t))
best.sort(reverse=True)
print("   candidate pairs with |D&V| >= |D|/2 :", len(best))
for b in best[:12]:
    print("     J=%.4f |D|=%d |V|=%d common=%d shift=%d T(U)=%d T(V)=%d" % b)
if not best:
    print("     NONE: no doubling image of a corpus solution shares even half of its")
    print("     elements with any corpus solution starting at the same place.")

print("\n   best overlap achieved at all (over U with T(U)>=20):")
bb = (0,)
for i, U in enumerate(S):
    if U[0] < 20:
        continue
    for sh in (0, 1):
        D = dbl(U, sh)
        nd = 2 * len(U)
        lo = 2 * U[0] - sh
        for t in range(max(3, lo - 2), lo + 3):
            for j in byT.get(t, ()):
                inter = bin(D & M[j]).count("1")
                cand = (inter / (nd + len(S[j]) - inter), nd, len(S[j]), inter, sh, U[0], t)
                if cand > bb:
                    bb = cand
print("     (jaccard, |D|, |V|, common, shift, T(U), T(V)) =", bb)

print("\n=== (c) parity signature of runs (a D_+ image is 100% at start-even/length-even) ===")
c = Counter()
for U in S:
    for run in runs_of(list(U)):
        c[(run[0] % 2, len(run) % 2)] += 1
tot = sum(c.values())
for k in sorted(c):
    print("     start parity %d, length parity %d : %6.2f%%" % (k[0], k[1], 100.0 * c[k] / tot))

print("\n=== (d) exact doubling images that are solutions ===")
allm = set(M)
print("     count:", sum(1 for U in S for sh in (0, 1) if dbl(U, sh) in allm), "(must be 0)")

print("\n=== (e) corpus solutions V containing a full doubling image D(U) ===")
found = 0
ex = []
for i, U in enumerate(S):
    if 2 * U[-1] + 1 > 400:
        continue
    for sh in (0, 1):
        D = dbl(U, sh)
        for j, vm in enumerate(M):
            if D & vm == D:
                found += 1
                if len(ex) < 3:
                    ex.append((S[i], S[j]))
                break
print("     count:", found)
for a, b in ex:
    print("      U=", a, "\n      V=", b)

print("\n=== (f) statistical self-similarity: distribution of n/T for far-out solutions ===")
print("   T   deciles of n/T (10th,...,90th percentile)")
seen = set()
for U in sorted(S, key=lambda u: u[0]):
    T = U[0]
    if T in seen or T < 20:
        continue
    seen.add(T)
    q = [U[int(k * len(U) / 10)] / T for k in range(1, 10)]
    print("  %3d  %s" % (T, " ".join("%.2f" % x for x in q)))
