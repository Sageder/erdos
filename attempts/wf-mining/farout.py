#!/usr/bin/env python3
"""
Deep dive on the far-out solutions (min U >= 20): what do they actually look like?

 (1) the *windowed* cofactor law: for each prime p used, the cofactor set lives in
     [ceil(T/p), floor(N/p)] -- an interval of ratio N/T, not [1, N/p].
 (2) block decomposition of the solution by "which prime gadget did this element
     come from": each element is assigned to its largest prime factor.
 (3) the mass profile: how much of the total 1 is carried by the bottom third,
     middle third, top third of [T,N].
 (4) interval-minus-gapset test: what is the longest all-present interval, and is
     the complement structured?
"""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat
from mult import factor, primes_upto

S = load()
FAR = [U for U in S if U[0] >= 20]
print("far-out corpus (min>=20):", len(FAR))

P = primes_upto(400)

# ---------- (1) windowed cofactor law -------------------------------
print("\n=== (1) windowed cofactor sets  A_p subset [ceil(T/p), floor(N/p)] ===")
print("    for each prime, over far-out solutions: how many primes are USED,")
print("    and the size of the window they live in")
used_hist = Counter()
win = defaultdict(Counter)
for U in FAR:
    T, N = U[0], U[-1]
    nused = 0
    for p in P:
        A = sorted(n // p for n in U if n % p == 0)
        if not A:
            continue
        nused += 1
        lo, hi = -(-T // p), N // p
        win[p][(lo, hi, len(A))] += 1
    used_hist[nused] += 1
print("    #distinct primes dividing some element, histogram:", dict(sorted(used_hist.items())))

print("\n    per-prime windows actually seen (far-out only), p >= 11:")
for p in P:
    if p < 11 or not win[p]:
        continue
    tot = sum(win[p].values())
    common = win[p].most_common(3)
    print("      p=%3d used %4d/%d ; (T/p..N/p, |A_p|) top: %s"
          % (p, tot, len(FAR), common))

# ---------- (2) largest-prime-factor classes ------------------------
print("\n=== (2) elements grouped by largest prime factor (far-out) ===")
for U in FAR[-3:]:
    T, N = U[0], U[-1]
    g = defaultdict(list)
    for n in U:
        g[max(factor(n))].append(n)
    print("  T=%d N=%d |U|=%d" % (T, N, len(U)))
    for q in sorted(g):
        print("     lpf=%3d (%2d elts): %s" % (q, len(g[q]), g[q]))

# ---------- (3) mass profile ----------------------------------------
print("\n=== (3) mass profile: fraction of the total 1 carried by thirds of [T,N] ===")
print("   T    N   mass[T,T+w)  mass[T+w,T+2w)  mass[T+2w,N]   (w=(N-T)/3), exact-as-float")
seen = set()
for U in sorted(FAR, key=lambda u: u[0]):
    T, N = U[0], U[-1]
    if T in seen:
        continue
    seen.add(T)
    w = (N - T) / 3.0
    m = [Fraction(0)] * 3
    for n in U:
        m[min(2, int((n - T) / w))] += Fraction(1, n)
    print("%4d %4d    %.4f          %.4f         %.4f" % (T, N, float(m[0]), float(m[1]), float(m[2])))

# ---------- (4) interval-minus-gapset ------------------------------
print("\n=== (4) how close is U to an interval minus a gap set? ===")
print("   T    N   |U|  density  longest present run  longest absent run  #gaps  gap-length mean")
seen = set()
for U in sorted(FAR, key=lambda u: u[0]):
    T, N = U[0], U[-1]
    if T in seen:
        continue
    seen.add(T)
    Us = set(U)
    R = runs_of(list(U))
    comp = [n for n in range(T, N + 1) if n not in Us]
    C = runs_of(comp) if comp else []
    gl = [len(x) for x in C]
    print("%4d %4d %4d   %.3f        %3d               %3d            %3d      %.2f"
          % (T, N, len(U), len(U) / (N - T + 1), max(len(x) for x in R),
             max(gl) if gl else 0, len(gl), sum(gl) / len(gl) if gl else 0))
