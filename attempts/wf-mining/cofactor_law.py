#!/usr/bin/env python3
"""
THE COFACTOR LAW.

Let U be a solution, N = max U, p an odd prime with p | n for some n in U, and
E = max nu_p(n).  Rule (P) gives  v_p( sum_{p|n} p^E/n ) >= E.
In the (overwhelmingly common) case E = 1 this reads

      A_p(U) := { n/p : n in U, p | n }  subset of [1, floor(N/p)],
      p  |  numerator( sum_{a in A_p} 1/a ).                       (*)

Define  m(p) = min { m : some nonempty A subset of [1,m] has p | num(sum_{a in A} 1/a) }.
Then (E=1 and) p | some element of U forces  floor(N/p) >= m(p),  i.e.  N >= p*m(p).

This script computes m(p) exactly (subset sums over lcm(1..m), pure integers) and
checks the resulting bound against the whole corpus.
"""
import sys
from math import gcd
from fractions import Fraction
from collections import Counter

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load
from mult import factor, primes_upto


def achievable_numerators(m):
    """All numerators (over the common denominator L=lcm(1..m)) of subset sums of
    {1/1,...,1/m}.  Pure integer arithmetic."""
    L = 1
    for a in range(1, m + 1):
        L = L * a // gcd(L, a)
    w = [L // a for a in range(1, m + 1)]
    S = {0}
    for x in w:
        S |= {s + x for s in S}
    S.discard(0)
    return L, S


def m_of_p(p, mmax=12):
    """Least m such that some A subset [1,m] has p | numerator(sum 1/a) (in lowest terms)."""
    for m in range(1, mmax + 1):
        L, S = achievable_numerators(m)
        for s in S:
            # numerator in lowest terms is s/gcd(s,L)
            if (s // gcd(s, L)) % p == 0:
                return m
    return None


if __name__ == "__main__":
    P = primes_upto(400)
    print("=== m(p): least m with a valid cofactor set inside [1,m] ===")
    print(" p    m(p)   p*m(p)   witness")
    tab = {}
    for p in P:
        if p == 2:
            continue
        m = m_of_p(p)
        tab[p] = m
        # find a witness
        wit = None
        if m:
            L, _ = achievable_numerators(m)
            best = None
            for mask in range(1, 1 << m):
                A = [a for a in range(1, m + 1) if mask >> (a - 1) & 1]
                s = sum(Fraction(1, a) for a in A)
                if s.numerator % p == 0:
                    if best is None or len(A) < len(best):
                        best = A
            wit = best
        print("%4d  %4s  %6s   %s" % (p, m, (p * m) if m else "-", wit))

    # ---- check the bound on the corpus ------------------------------
    S = load()
    print("\n=== corpus check:  p | some element  =>  N >= p*m(p)  (E=1 case) ===")
    viol = 0
    tight = Counter()
    maxratio = {}
    for U in S:
        N = U[-1]
        for p in P:
            if p == 2:
                continue
            mults = [n for n in U if n % p == 0]
            if not mults:
                continue
            E = max(factor(n)[p] for n in mults)
            if E != 1:
                continue
            m = tab[p]
            if N < p * m:
                viol += 1
            tight[N - p * m >= 0] += 1
            r = Fraction(N, p)
            if p not in maxratio or r < maxratio[p]:
                maxratio[p] = r
    print("violations:", viol)
    print("\n p   m(p)  min over corpus of floor(N/p) among solutions using p")
    for p in sorted(maxratio):
        print("%4d  %3s   %s   (N/p >= %.3f)" % (p, tab[p], maxratio[p], float(maxratio[p])))

    # ---- and the observed max prime factor vs N ---------------------
    print("\n=== max_{n in U} lpf(n) / N over the corpus ===")
    worst = 0.0
    arg = None
    for U in S:
        N = U[-1]
        q = max(max(factor(n)) for n in U)
        if q / N > worst:
            worst = q / N
            arg = (q, N, U[:4])
    print("largest ratio lpf/N observed:", worst, arg)
