#!/usr/bin/env python3
"""
SELF-SIMILARITY ACROSS SCALES.  (efficient version)

Is a solution at scale ~2T ever close to the image of one at scale T under
   D_+(U) = union of {2n, 2n+1}   or   D_-(U) = union of {2n-1, 2n} ?
And more generally: is any solution close to a c-fold rescaling of another?

All arithmetic exact.
"""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat

S = load()
SET = [frozenset(U) for U in S]
byT = defaultdict(list)
for i, U in enumerate(S):
    byT[U[0]].append(i)

# ---------- (a) exact deficit of the doubling image ------------------
print("=== (a) doubling image D_+(U) = U_{n in U}{2n,2n+1}: exact reciprocal-sum deficit")
print("    Sigma(D_+(U)) = 1 - sum_{n in U} 1/(2n(2n+1)).   D_+(U) is ALWAYS legal,")
print("    has cap = |U| and run count = #runs(U) + #(proper prefixes) -- capacity DOUBLES.")
print("  T    |U|   deficit          1/deficit   smallest single atom 1/(2N)+1/(2N+1)")
seen = set()
for U in sorted(S, key=lambda u: u[0]):
    T = U[0]
    if T in seen or T < 20:
        continue
    seen.add(T)
    d = sum(Fraction(1, 2 * n * (2 * n + 1)) for n in U)
    N = U[-1]
    small = Fraction(1, 2 * N) + Fraction(1, 2 * N + 1)
    print("%4d %5d   %.7f      %8.2f     %.7f   (deficit / smallest atom = %.3f)"
          % (T, len(U), float(d), 1 / float(d), float(small), float(d / small)))

# ---------- (b) is a real solution close to a doubling image? --------
print("\n=== (b) best overlap of D_sigma(U) with an actual corpus solution ===")


def dbl(U, shift=0):
    out = set()
    for n in U:
        out.add(2 * n - shift)
        out.add(2 * n + 1 - shift)
    return frozenset(out)


best = []
for i, U in enumerate(S):
    for sh in (0, 1):
        D = dbl(U, sh)
        lo = min(D)
        for t in range(max(3, lo - 2), lo + 3):
            for j in byT.get(t, ()):
                V = SET[j]
                inter = len(D & V)
                if inter * 2 < len(D):
                    continue
                best.append((inter / len(D | V), len(D), len(V), inter, sh, S[i][0], t))
best.sort(reverse=True)
print("  pairs with |D&V| >= |D|/2 :", len(best))
print("  top 15 (jaccard, |D|, |V|, |D&V|, shift, T(U), T(V)):")
for b in best[:15]:
    print("    J=%.4f  |D|=%3d |V|=%3d  common=%3d  shift=%d  T(U)=%2d  T(V)=%2d"
          % b)
if not best:
    print("    NONE -- no doubling image shares even half its elements with a solution")

# ---------- (c) twin-atom parity signature --------------------------
print("\n=== (c) parity signature of runs ===")
c = Counter()
for U in S:
    for run in runs_of(list(U)):
        c[(run[0] % 2, len(run) % 2)] += 1
tot = sum(c.values())
for k in sorted(c):
    print("    run start parity %d, run length parity %d : %6.2f%%" % (k[0], k[1], 100.0 * c[k] / tot))
print("    A pure D_+ image would be 100%% at (start even, length even) = (0,0).")

# ---------- (d) exact doubling images that are solutions ------------
allsets = set(SET)
hit = sum(1 for U in S for sh in (0, 1) if dbl(U, sh) in allsets)
print("\n=== (d) doubling images that are themselves solutions:", hit,
      "(must be 0: Sigma drops by a positive amount)")

# ---------- (e) does a solution CONTAIN a full doubling image? -------
print("\n=== (e) does a corpus solution V contain a full doubling image D_sigma(U)? ===")
# index solutions by their element set; test containment via a bitmask over [2,400]
MAXEL = 400
def mask(s):
    m = 0
    for x in s:
        if x <= MAXEL:
            m |= 1 << x
    return m
Vmask = [mask(v) for v in SET]
found = 0
examples = []
for i, U in enumerate(S):
    for sh in (0, 1):
        D = dbl(U, sh)
        if max(D) > MAXEL:
            continue
        dm = mask(D)
        for j, vm in enumerate(Vmask):
            if dm & vm == dm:
                found += 1
                if len(examples) < 5:
                    examples.append((S[i], sorted(D), S[j]))
                break
print("    count:", found)
for e in examples:
    print("      U =", e[0])
    print("      D =", e[1])
    print("      V =", e[2])

# ---------- (f) general rescaling: U' approx c*U ---------------------
print("\n=== (f) multiplicative self-similarity: for pairs of solutions U,V with")
print("    T(V) approx c*T(U), how many elements of V lie in c*U + {0,..,c-1}? ===")
for c in (2, 3):
    bestf = []
    for i, U in enumerate(S):
        band = set()
        for n in U:
            band |= set(range(c * n, c * n + c))
        for j, V in enumerate(SET):
            if abs(min(V) - c * S[i][0]) > c:
                continue
            k = len(V & band)
            bestf.append((k / len(V), len(V), k, S[i][0], min(V)))
    bestf.sort(reverse=True)
    print("  c=%d : best share of V inside the band c*U+[0,c) :" % c)
    for b in bestf[:6]:
        print("     %.4f   |V|=%3d  inside=%3d  T(U)=%2d T(V)=%3d" % b)
    if not bestf:
        print("     (no comparable pairs)")
