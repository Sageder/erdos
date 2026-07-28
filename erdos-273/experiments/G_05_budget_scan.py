"""
G_05_budget_scan.py -- Route G, step 5 (rewritten: exact subset-sum DP with denominator M).

CLAIM TESTED: for which "lcm candidates" M (the HALVED-world lcm; the E-world lcm is L = 2M)
is the necessary budget condition for an E-covering satisfiable?

STRUCTURE LEMMA (proved in FINDINGS.md).  Every n in E is even.  Hence an E-covering system
with lcm L = 2M is EXACTLY a pair of DISJOINT covering systems of Z with distinct moduli
drawn from  D_H(M) = {m : m | M, 2m+1 prime, m >= 2}  (one for each parity class).

  NECESSARY CONDITION (budget):  D_H(M) admits a partition (A,B) with
        sum_{m in A} 1/m > 1   and   sum_{m in B} 1/m > 1;
  in particular  s(M) := sum_{m in D_H(M)} 1/m  >  2.

All m divide M, so every subset sum is an integer multiple of 1/M: the partition question is
an exact subset-sum problem on integers M/m with total <= 3M.  Solved exactly by DP.

CONCLUSION: printed tables; recorded in attempts/route-G-selfridge/FINDINGS.md.
"""
from fractions import Fraction
from sympy import isprime, divisors, factorint
import numpy as np
import sys

def DH(M):
    return [d for d in divisors(M) if d >= 2 and isprime(2*d + 1)]

def s(P):
    return sum(Fraction(1, m) for m in P)

def best_balanced(pool, M):
    """EXACT max over 2-partitions (A,B) of min(sum_A 1/m, sum_B 1/m), denominator M."""
    w = [M // m for m in pool]
    tot = sum(w)
    reach = np.zeros(tot + 1, dtype=bool); reach[0] = True
    for x in w:
        reach[x:] |= reach[:-x].copy()
    idx = np.nonzero(reach)[0]
    vals = np.minimum(idx, tot - idx)
    b = int(vals.max())
    return Fraction(b, M), Fraction(tot, M)

def recover_partition(pool, M, target_lo):
    """find a subset A with sum_A 1/m > 1 and sum_B 1/m > 1, if one exists (greedy DP walk)."""
    w = [M // m for m in pool]; tot = sum(w)
    lo, hi = M + 1, tot - M - 1     # need lo <= sumA <= hi (strict > 1 both sides)
    if lo > hi:
        return None
    n = len(w)
    reach = [np.zeros(tot + 1, dtype=bool) for _ in range(n + 1)]
    reach[0][0] = True
    for i, x in enumerate(w):
        reach[i+1] |= reach[i]
        reach[i+1][x:] |= reach[i][:-x]
    tgt = None
    for v in range(lo, hi + 1):
        if reach[n][v]:
            tgt = v; break
    if tgt is None:
        return None
    A = []; v = tgt
    for i in range(n - 1, -1, -1):
        if v >= w[i] and reach[i][v - w[i]]:
            A.append(pool[i]); v -= w[i]
    return sorted(A)

def smooth_numbers(primes, limit):
    out = [1]
    for p in primes:
        new = []
        for x in out:
            y = x
            while y <= limit:
                new.append(y); y *= p
        out = new
    return sorted(set(out))

def fac(M):
    f = factorint(M)
    return "*".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))

def main():
    print(__doc__)
    LIMIT = 3 * 10**6
    prime_sets = {
        "7-smooth":  [2,3,5,7],
        "11-smooth": [2,3,5,7,11],
        "13-smooth": [2,3,5,7,11,13],
        "17-smooth": [2,3,5,7,11,13,17],
        "23-smooth": [2,3,5,7,11,13,17,19,23],
    }
    allc = set()
    for name, ps in prime_sets.items():
        allc |= set(smooth_numbers(ps, LIMIT))
    cands = sorted(allc)
    print(f"scanning {len(cands)} smooth M <= {LIMIT} (primes up to 23)")
    rows = []
    for M in cands:
        P = DH(M)
        if len(P) < 8: continue
        t = s(P)
        if t > Fraction(19,10):
            rows.append((t, M, P))
    rows.sort(key=lambda r: (-r[0], r[1]))
    print(f"\n{len(rows)} of them have s(M) > 1.9.\n")
    print("TOP 25 by s(M):")
    print(f"{'M':>10} {'factorisation':>22} {'#D_H':>5} {'s(M)':>8} {'bal':>8} {'partition?':>11}")
    for t, M, P in rows[:25]:
        bal, tot = best_balanced(P, M)
        A = recover_partition(P, M, 1) if tot > 2 else None
        print(f"{M:>10} {fac(M):>22} {len(P):>5} {float(t):>8.5f} {float(bal):>8.5f} "
              f"{'YES' if A else 'no':>11}")
    print()
    over2 = sorted([(M,P,t) for t,M,P in rows if t > 2], key=lambda r: r[0])
    print(f"SMALLEST M with s(M) > 2 : {len(over2)} found in range; first 8:")
    for M, P, t in over2[:8]:
        bal, tot = best_balanced(P, M)
        A = recover_partition(P, M, 1)
        B = [m for m in P if m not in A] if A else None
        print(f"\n  M = {M} = {fac(M)}   L = 2M = {2*M}")
        print(f"     D_H(M) = {P}")
        print(f"     s(M) = {t} = {float(t):.6f}   best balanced min-half = {bal} = {float(bal):.6f}")
        if A:
            print(f"     a legal budget split:  A = {A}  (sum {float(s(A)):.6f})")
            print(f"                            B = {B}  (sum {float(s(B)):.6f})")
        else:
            print(f"     NO partition with both halves > 1  ==> M is dead.")
    print()
    print("REMARK.  s(M) > 2 is only the *density* necessary condition.  Selfridge's system")
    print("shows a covering with least modulus 2 can need reciprocal sum as low as 23/18 =")
    print("1.2778; a covering with least modulus >= 3 needs much more.  Since one of the two")
    print("halves cannot contain m = 2, the real requirement is  s(M) > sigma_2 + sigma_3,")
    print("where sigma_t is the minimal reciprocal sum of a covering with distinct moduli and")
    print("least modulus >= t.  See G_08 for measurements of sigma_t.")

main()
