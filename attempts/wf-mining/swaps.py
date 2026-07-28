#!/usr/bin/env python3
"""
LOCAL MOVES between solutions.

If U and V are both solutions then X = U-minus-V and Y = V-minus-U have EQUAL reciprocal sums
(exactly), because Sigma(U)=Sigma(V)=1 and they share U∩V.  So every pair of
solutions yields a "swap gadget" (X -> Y).  Interesting gadgets are those with
|X|+|Y| small, and especially those whose effect on the run count / capacity is
nonzero -- these are the moves that could shift k.

Also computes the harmonic centroid  1/Sigma(1/n^2)  and the doubling deficit law.
"""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat

S = load()
rows = [stat(U) for U in S]

# ---------- harmonic centroid ---------------------------------------
print("=== harmonic centroid  n* := 1 / sum_{n in U} 1/n^2   (since sum 1/n = 1) ===")
print("    and the doubling deficit  delta(U) = sum 1/(2n(2n+1))")
seen = set()
for U, st in sorted(zip(S, rows), key=lambda z: z[1]["T"]):
    T = st["T"]
    if T in seen:
        continue
    seen.add(T)
    s2 = sum(Fraction(1, n * n) for n in U)
    d = sum(Fraction(1, 2 * n * (2 * n + 1)) for n in U)
    print("  T=%3d N=%3d |U|=%3d  n* = %8.3f  (n*/T = %.3f)   delta = %.7f  1/(delta*T) = %.3f"
          % (T, st["N"], st["m"], 1 / float(s2), 1 / float(s2) / T, float(d), 1 / (float(d) * T)))

# ---------- minimal symmetric differences ---------------------------
print("\n=== minimal symmetric differences among far-out solutions (min U >= 20) ===")
FAR = [(U, st) for U, st in zip(S, rows) if st["T"] >= 20]
print("    far-out pool:", len(FAR), " pairs:", len(FAR) * (len(FAR) - 1) // 2)
sets = [frozenset(U) for U, _ in FAR]
best = []
for i in range(len(FAR)):
    for j in range(i + 1, len(FAR)):
        X = sets[i] - sets[j]
        Y = sets[j] - sets[i]
        n = len(X) + len(Y)
        if n <= 10:
            best.append((n, i, j, tuple(sorted(X)), tuple(sorted(Y))))
best.sort()
print("    pairs with |X|+|Y| <= 10 :", len(best))
seenpair = set()
shown = 0
for n, i, j, X, Y in best:
    if (X, Y) in seenpair:
        continue
    seenpair.add((X, Y))
    sx = sum(Fraction(1, a) for a in X)
    sy = sum(Fraction(1, a) for a in Y)
    assert sx == sy
    dr = FAR[j][1]["r"] - FAR[i][1]["r"]
    dc = FAR[j][1]["cap"] - FAR[i][1]["cap"]
    print("      X=%-34s -> Y=%-34s  sum=%s   d(r)=%+d d(cap)=%+d"
          % (str(X), str(Y), sx, dr, dc))
    shown += 1
    if shown >= 25:
        break

# ---------- the same over the whole corpus, restricted to tiny diffs --
print("\n=== tiny swap gadgets over the WHOLE corpus (|X|+|Y| <= 7), bucketed by sum ===")
# index by the complement fingerprint is too costly; instead bucket solutions by
# their top part and compare within buckets
buck = defaultdict(list)
for idx, U in enumerate(S):
    buck[U[:6]].append(idx)
gad = {}
for key, idxs in buck.items():
    if len(idxs) < 2 or len(idxs) > 400:
        continue
    ss = [frozenset(S[i]) for i in idxs]
    for a in range(len(idxs)):
        for b in range(a + 1, len(idxs)):
            X = ss[a] - ss[b]
            Y = ss[b] - ss[a]
            if len(X) + len(Y) <= 7 and X and Y:
                k = (tuple(sorted(X)), tuple(sorted(Y)))
                if k not in gad:
                    gad[k] = (sum(Fraction(1, x) for x in k[0]),
                              None)
print("    distinct tiny gadgets found:", len(gad))
shown = 0
for (X, Y), (s, _) in sorted(gad.items(), key=lambda kv: (len(kv[0][0]) + len(kv[0][1]), kv[0])):
    print("      %s -> %s   (sum %s)" % (X, Y, s))
    shown += 1
    if shown >= 30:
        break
