#!/usr/bin/env python3
"""
Shape mining: run-length distribution, recurring atoms, local density profile,
and "interval minus gap set" vs "sparse atoms" diagnosis.
"""
import sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat
from mult import factor

S = load()
rows = [(U, stat(U)) for U in S]
FAR = [(U, s) for U, s in rows if s["T"] >= 30]
NEAR = [(U, s) for U, s in rows if s["T"] <= 12]

print("corpus %d ; far-out (min>=30) %d ; near (min<=12) %d" % (len(S), len(FAR), len(NEAR)))

# ---------- run length distribution ---------------------------------
print("\n=== run-length distribution ===")


def rl(group, name):
    c = Counter()
    for U, s in group:
        c.update(s["L"])
    tot = sum(c.values())
    print(" %-22s runs=%6d  " % (name, tot) +
          "  ".join("L=%d:%5.2f%%" % (l, 100.0 * c[l] / tot) for l in sorted(c) if l <= 12))
    print("      max run length = %d ; mean = %.3f ; share L=2 = %.3f ; share L odd = %.3f"
          % (max(c), sum(l * v for l, v in c.items()) / tot,
             c[2] / tot, sum(v for l, v in c.items() if l % 2) / tot))


rl(rows, "ALL")
rl(NEAR, "min(U)<=12")
rl(FAR, "min(U)>=30")

# ---------- capacity efficiency -------------------------------------
print("\n=== capacity vs run count ===")
for name, g in (("ALL", rows), ("min<=12", NEAR), ("min>=30", FAR)):
    rr = [s["r"] for U, s in g]
    cc = [s["cap"] for U, s in g]
    mm = [s["m"] for U, s in g]
    print(" %-9s  mean r/cap = %.4f  mean cap/|U| = %.4f  mean |U|/r = %.4f  max cap-r = %d"
          % (name, sum(a / b for a, b in zip(rr, cc)) / len(g),
             sum(a / b for a, b in zip(cc, mm)) / len(g),
             sum(a / b for a, b in zip(mm, rr)) / len(g),
             max(c - r for r, c in zip(rr, cc))))

# ---------- recurring atoms -----------------------------------------
print("\n=== most frequent consecutive pairs {n,n+1} contained in U ===")
pair = Counter()
for U in S:
    Us = set(U)
    for n in U:
        if n + 1 in Us:
            pair[n] += 1
tot = len(S)
print(" (n, n+1) : share of solutions containing BOTH n and n+1")
for n, c in pair.most_common(40):
    print("   %4d,%4d : %6.2f%%   n=%s  n+1=%s" %
          (n, n + 1, 100.0 * c / tot, factor(n), factor(n + 1)))

print("\n=== most frequent ELEMENTS ===")
el = Counter()
for U in S:
    el.update(U)
for n, c in el.most_common(30):
    print("   %4d : %6.2f%%   %s" % (n, 100.0 * c / tot, factor(n)))

# ---------- local density profile ------------------------------------
print("\n=== local density profile: share of [T,N] occupied, by decile of position ===")


def profile(group, name):
    acc = [0.0] * 10
    for U, s in group:
        T, N = s["T"], s["N"]
        W = N - T + 1
        cnt = [0] * 10
        for n in U:
            cnt[min(9, (10 * (n - T)) // W)] += 1
        for i in range(10):
            acc[i] += cnt[i] / (W / 10.0)
    print(" %-12s %s" % (name, "  ".join("%.3f" % (a / len(group)) for a in acc)))


profile(rows, "ALL")
profile(NEAR, "min<=12")
profile(FAR, "min>=30")

# ---------- gap structure of far-out solutions ----------------------
print("\n=== gap structure (complement runs) of the far-out solutions ===")
for U, s in sorted(FAR, key=lambda x: -x[1]["T"])[:6]:
    T, N = s["T"], s["N"]
    comp = [n for n in range(T, N + 1) if n not in set(U)]
    cr = runs_of(comp) if comp else []
    gl = Counter(len(x) for x in cr)
    print(" T=%d N=%d |U|=%d r=%d cap=%d  density=%.3f  gap-run lengths %s"
          % (T, N, s["m"], s["r"], s["cap"], s["m"] / (N - T + 1), dict(sorted(gl.items()))))
    print("     run lengths: %s" % (s["L"],))
