#!/usr/bin/env python3
"""
Correct Rule-(P) check and mining of the COFACTOR PATTERNS.

Rule (P):  if sum_{n in U} 1/n = 1 and E = max nu_p(n) over n in U with p|n, then
           v_p( sum_{n in U, p|n} p^E/n ) >= E,
i.e. the p-adic valuation of the rational number  S_p = sum_{p|n} p^E / n  is >= E.
(The complementary sum has v_p >= 0, so this is forced.)

Then: for each prime p, record the *cofactor set*  A_p(U) = { n/p : n in U, p | n }
sorted.  These are the combinatorial atoms that Rule (P) constrains:
   sum_{a in A_p} 1/a  must have v_p >= 0  (E=1 case: sum 1/a == 0 mod p).
"""
import sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load
from mult import factor, primes_upto


def vp(x, p):
    """p-adic valuation of a Fraction (x != 0)."""
    if x == 0:
        return 10 ** 9
    n, d = x.numerator, x.denominator
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


if __name__ == "__main__":
    S = load()
    P = primes_upto(400)
    print("=== Rule (P), corrected check (v_p of S_p >= E) ===")
    bad = 0
    slack = Counter()
    for U in S:
        for p in P:
            mults = [n for n in U if n % p == 0]
            if not mults:
                continue
            E = max(factor(n)[p] for n in mults)
            Sp = sum(Fraction(p ** E, n) for n in mults)
            v = vp(Sp, p)
            if v < E:
                bad += 1
            slack[min(v - E, 4)] += 1
    print("violations over the whole corpus:", bad)
    print("slack v_p(S_p)-E histogram (capped at 4):", dict(sorted(slack.items())))

    # ---------- cofactor patterns -------------------------------------
    print("\n=== cofactor sets A_p = {n/p : p|n, n in U}, for the LARGE primes ===")
    for p in [17, 19, 23, 29, 31, 37, 41, 43, 47, 61]:
        pat = Counter()
        for U in S:
            A = tuple(sorted(n // p for n in U if n % p == 0))
            if A:
                pat[A] += 1
        tot = sum(pat.values())
        print("\n p=%d : %d solutions use p, %d distinct cofactor sets" % (p, tot, len(pat)))
        for A, c in pat.most_common(8):
            s = sum(Fraction(1, a) for a in A)
            print("    %-42s %6d (%5.1f%%)  sum=%s  v_%d=%d"
                  % (str(A), c, 100.0 * c / tot, s, p, vp(s, p)))
