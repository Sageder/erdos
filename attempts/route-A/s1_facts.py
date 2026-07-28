#!/usr/bin/env python3
"""
s1_facts.py -- re-verification of the background facts I am allowed to use.

Claims tested (all with exact Fraction arithmetic):
  (F1) Kuerschak: H(a,b) = sum_{n=a}^b 1/n is never an integer for b > a >= 1.
       Checked exhaustively for 1 <= a < b <= 400, plus the structural reason
       (unique maximal 2-power in every block of length >= 2).
  (F2) Two-attainer condition: for any legal U with sum 1, every prime p whose
       maximal valuation e among elements of U is >= 1 must be attained twice.
       (Verified as a *theorem check* on random sets: whenever exactly one
        element attains the max p-valuation, nu_p(sum) = -e.)
  (F3) The identities quoted in the prompt.
  (F4) Independent re-run of the exhaustive search "no legal U with max(U) <= N"
       for N up to 60 (small, in pure Python, to double-check the C search).

Conclusion is printed at the end.
"""
from fractions import Fraction
import random


def H(a, b):
    s = Fraction(0)
    for n in range(a, b + 1):
        s += Fraction(1, n)
    return s


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def f1(NMAX=400):
    print("--- F1 Kuerschak: H(a,b) never an integer, 1<=a<b<=%d ---" % NMAX)
    bad = []
    for a in range(1, NMAX + 1):
        s = Fraction(1, a)
        for b in range(a + 1, NMAX + 1):
            s += Fraction(1, b)
            if s.denominator == 1:
                bad.append((a, b, s))
    print("   integer block sums found:", bad if bad else "NONE")
    # structural reason: unique element of maximal 2-adic valuation
    v2 = [0] * (NMAX + 2)
    for n in range(1, NMAX + 1):
        v2[n] = nu(n, 2)
    viol = []
    for a in range(1, NMAX + 1):
        e, cnt = v2[a], 1
        for b in range(a + 1, NMAX + 1):
            if v2[b] > e:
                e, cnt = v2[b], 1
            elif v2[b] == e:
                cnt += 1
            if cnt != 1 or e < 1:
                viol.append((a, b, e, cnt))
    print("   blocks with non-unique / zero maximal 2-power:",
          viol[:5] if viol else "NONE")
    return not bad and not viol


def f2(trials=20000, seed=12345):
    print("--- F2 two-attainer: unique max nu_p => nu_p(sum) = -e < 0 ---")
    rnd = random.Random(seed)
    checked = 0
    for _ in range(trials):
        k = rnd.randint(2, 8)
        U = sorted(rnd.sample(range(2, 200), k))
        s = sum((Fraction(1, n) for n in U), Fraction(0))
        for p in (2, 3, 5, 7, 11, 13):
            e = max(nu(n, p) for n in U)
            if e < 1:
                continue
            cnt = sum(1 for n in U if nu(n, p) == e)
            if cnt == 1:
                checked += 1
                v = nu(s.numerator, p) - nu(s.denominator, p)
                assert v == -e, (U, p, e, v)
    print("   verified on %d (set,prime) instances: nu_p(sum) = -e exactly" % checked)
    return True


def f3():
    print("--- F3 identities ---")
    ok = True
    for n in range(1, 60):
        ok &= (Fraction(1, n) == Fraction(1, 2 * n) + Fraction(1, 2 * n + 1)
               + Fraction(1, 2 * n * (2 * n + 1)))
        ok &= (Fraction(1, n) == Fraction(1, n + 1) + Fraction(1, n * (n + 1)))
        for d in range(1, n + 1):
            if (n * n) % d == 0:
                ok &= (Fraction(1, n) == Fraction(1, n + d) + Fraction(1, n + n * n // d))
    for m in range(1, 60):
        ok &= (Fraction(1, 2 * m) + Fraction(1, 2 * m + 1)
               == Fraction(1, m) - Fraction(1, 2 * m * (2 * m + 1)))
        ok &= (Fraction(1, 2 * m - 1) + Fraction(1, 2 * m)
               == Fraction(1, m) + Fraction(1, 2 * m * (2 * m - 1)))
        if 3 * m - 1 >= 1:
            ok &= (H(3 * m - 1, 3 * m + 1)
                   == Fraction(1, m) + Fraction(2, 3 * m * (3 * m - 1) * (3 * m + 1)))
    print("   all quoted identities hold:", ok)
    # the two classical Egyptian representations
    print("   1/3+1/4+1/5+1/6+1/20 =",
          Fraction(1,3)+Fraction(1,4)+Fraction(1,5)+Fraction(1,6)+Fraction(1,20))
    print("   1/2+1/3+1/10+1/15   =",
          Fraction(1,2)+Fraction(1,3)+Fraction(1,10)+Fraction(1,15))
    return ok


def f4(N=60):
    print("--- F4 exhaustive: legal U subset [2,%d] with sum 1 ---" % N)
    tail = [Fraction(0)] * (N + 3)
    for n in range(N, 1, -1):
        tail[n] = tail[n + 1] + Fraction(1, n)
    sols = []
    nodes = [0]

    def dfs(pos, rem, runlen):
        nodes[0] += 1
        if rem == 0:
            if runlen != 1:
                sols.append(1)
            return
        if pos > N or rem > tail[pos]:
            return
        f = Fraction(1, pos)
        if f <= rem:
            dfs(pos + 1, rem - f, runlen + 1)
        elif runlen == 1:
            return
        if runlen != 1:
            dfs(pos + 1, rem, 0)

    dfs(2, Fraction(1), 0)
    print("   solutions:", len(sols), " nodes:", nodes[0])
    return len(sols) == 0


if __name__ == "__main__":
    r1 = f1()
    r2 = f2()
    r3 = f3()
    r4 = f4(60)
    print()
    print("SUMMARY: F1=%s F2=%s F3=%s F4(no solution with max<=60)=%s"
          % (r1, r2, r3, r4))
