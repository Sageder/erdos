#!/usr/bin/env python3
"""
Scaling laws.  All underlying quantities are exact integers; the least-squares
fits at the end are float and are labelled as FITS, not facts.
"""
import sys
from fractions import Fraction
from collections import defaultdict, Counter

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, stat

S = load()
rows = [stat(U) for U in S]

# ---- envelope of |U|, cap, r as functions of T = min U --------------
byT = defaultdict(list)
for r in rows:
    byT[r["T"]].append(r)

print("=== envelope by T = min(U)  (all EXACT maxima/minima over the corpus) ===")
print("  T  #sols  max|U|  maxCap  minR  maxR  minN  argmax-cap: (|U|,r,cap,N)")
data = []
for T in sorted(byT):
    g = byT[T]
    mc = max(x["cap"] for x in g)
    b = min((x for x in g if x["cap"] == mc), key=lambda x: x["r"])
    print("%4d %6d %6d %6d %5d %5d %6d   (%d,%d,%d,%d)"
          % (T, len(g), max(x["m"] for x in g), mc, min(x["r"] for x in g),
             max(x["r"] for x in g), min(x["N"] for x in g),
             b["m"], b["r"], b["cap"], b["N"]))
    data.append((T, max(x["m"] for x in g), mc, b["r"], b["N"]))

# ---- envelope by N = max U -----------------------------------------
byN = defaultdict(list)
for r in rows:
    byN[r["N"] // 20 * 20].append(r)
print("\n=== envelope by N bucket (max U rounded down to 20) ===")
print("  Nbucket  #sols  max|U|  maxCap  minR   maxT")
for nb in sorted(byN):
    g = byN[nb]
    print("%7d %7d %6d %6d %5d %6d"
          % (nb, len(g), max(x["m"] for x in g), max(x["cap"] for x in g),
             min(x["r"] for x in g), max(x["T"] for x in g)))

# ---- (r,cap) pairs realised ----------------------------------------
print("\n=== realised (r, cap) pairs: for each cap, the minimum r ===")
minr = {}
for x in rows:
    c = x["cap"]
    if c not in minr or x["r"] < minr[c]:
        minr[c] = x["r"]
print("  cap : min r   (interval [r,cap] length)")
for c in sorted(minr):
    print("  %3d : %3d      %d" % (c, minr[c], c - minr[c]))

# how the intervals chain
cov = set()
for x in rows:
    cov |= set(range(x["r"], x["cap"] + 1))
print("\n k realised:", min(cov), "..", max(cov), " missing:",
      sorted(set(range(min(cov), max(cov) + 1)) - cov))

# ---- least squares fits (FLOAT, labelled as fits) -------------------
import math
print("\n=== FITS (least squares, float -- these are extrapolations, not facts) ===")


def fit(xs, ys, label):
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    d = n * sxx - sx * sx
    a = (n * sxy - sx * sy) / d
    b = (sy - a * sx) / n
    resid = max(abs(a * x + b - y) for x, y in zip(xs, ys))
    print("   %-28s  y = %.4f x + %.3f     (max |residual| = %.2f, n=%d)"
          % (label, a, b, resid, n))
    return a, b


# use only T >= 20 (the far-out, purpose-built searches)
D = [d for d in data if d[0] >= 20]
fit([d[0] for d in D], [d[1] for d in D], "max |U|  vs  T")
fit([d[0] for d in D], [d[2] for d in D], "max cap  vs  T")
fit([d[0] for d in D], [d[3] for d in D], "r at max cap  vs  T")
fit([d[0] for d in D], [d[4] for d in D], "N at max cap  vs  T")
fit([d[2] for d in D], [d[3] for d in D], "r  vs  cap  (far-out)")
fit([d[1] for d in D], [d[2] for d in D], "cap  vs  |U|  (far-out)")

# whole corpus versions
allrows = [(x["T"], x["m"], x["cap"], x["r"], x["N"]) for x in rows]
fit([x[2] for x in allrows], [x[3] for x in allrows], "r vs cap (whole corpus)")
fit([x[1] for x in allrows], [x[2] for x in allrows], "cap vs |U| (whole corpus)")

print("\n   ratio table (exact rationals):")
for T, m, c, r, N in D:
    print("     T=%2d  |U|/T=%s=%.3f  cap/T=%s=%.3f  r/cap=%s=%.3f  N/T=%s=%.3f"
          % (T, Fraction(m, T), m / T, Fraction(c, T), c / T,
             Fraction(r, c), r / c, Fraction(N, T), N / T))
