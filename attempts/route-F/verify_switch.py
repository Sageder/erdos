#!/usr/bin/env python3
"""INDEPENDENT exact verifier for switches.
Input lines:  a1 a2 ... | b1 b2 ...
Checks A and B are legal (no isolated point, elements >= 2), A != B, and that
D*(Sigma(B)-Sigma(A)) is an integer c; reports the distribution of |c|.
usage: verify_switch.py D file [--minelt T]
"""
import sys
from fractions import Fraction

D = int(sys.argv[1]); fn = sys.argv[2]
minelt = None
if "--minelt" in sys.argv:
    minelt = int(sys.argv[sys.argv.index("--minelt") + 1])


def legal(U):
    S = set(U)
    if len(S) != len(U):
        return False
    if any(n < 2 for n in S):
        return False
    return all((n - 1) in S or (n + 1) in S for n in S)


cs = {}
bad = 0
tot = 0
lo = hi = None
for line in open(fn):
    if "|" not in line:
        continue
    l, r = line.split("|")
    A = [int(t) for t in l.split()]
    B = [int(t) for t in r.split()]
    tot += 1
    if not legal(A) or not legal(B) or sorted(A) == sorted(B):
        bad += 1
        continue
    if minelt is not None and (min(A + B) < minelt):
        bad += 1
        continue
    d = sum(Fraction(1, n) for n in B) - sum(Fraction(1, n) for n in A)
    v = d * D
    if v.denominator != 1:
        bad += 1
        continue
    c = int(v)
    if c == 0:
        bad += 1
        continue
    m = max(A + B); mn = min(A + B)
    lo = mn if lo is None else min(lo, mn)
    hi = m if hi is None else max(hi, m)
    if abs(c) not in cs:
        cs[abs(c)] = (A, B, c)
print("pairs read %d, valid switches %d, rejected %d" % (tot, tot - bad, bad))
if cs:
    ks = sorted(cs)
    print("distinct |c| values: %d ; smallest |c| = %d ; support in [%d,%d]"
          % (len(ks), ks[0], lo, hi))
    print("smallest 12 |c|:", ks[:12])
    A, B, c = cs[ks[0]]
    print("witness  c=%d" % c)
    print("  A =", " ".join(map(str, sorted(A))))
    print("  B =", " ".join(map(str, sorted(B))))
