"""
STRENGTHENED FORM of Route A's Theorem A3, using Lemma A2 in full.

Setting.  Fix L (a candidate lcm, E-world) and let D_H = {m : m | L/2, 2m+1 prime} be the pool of
available H-moduli, B = sum_{m in D_H} 1/m = 2 B_E(L).  By Lemma M3 a covering system with all
moduli in E is a partition of some M subset D_H into two DISJOINT sets M_0, M_1, each a covering
system of Z.  Write X_c = sum_{m in M_c} 1/m - 1.  Then

    (i)  X_0 + X_1 = sum_{m in M_0 u M_1} 1/m - 2  <=  B - 2 ;
    (ii) X_c > 0 strictly for each c (Davenport-Mirsky-Newman-Rado);
    (iii) [Lemma A2]  X_c >= f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1 - 1/m)
         for EVERY pairwise coprime T contained in M_c -- residue-free, by CRT independence.

FORCED MODULI.  m in D_H must be used (in one of the two halves) whenever B - 1/m < 2, since
otherwise the total reciprocal mass of the two halves would fall below 2.  Let F be the set of
forced moduli.  Every valid configuration induces a 2-colouring of F.

THE TEST.  For a 2-colouring (F_0, F_1) of F put g(F_c) = max over pairwise coprime T subset F_c
of f(T).  By (iii), X_c >= g(F_c); with (i),

    if   min over 2-colourings of [ g(F_0) + g(F_1) ]  >  B - 2 ,   then L is IMPOSSIBLE.

Theorem A3 is the special case F superset {2,3,5}, pairs only.  This version uses ALL forced
moduli and ALL pairwise coprime subsets, so it is at least as strong, and strictly stronger
whenever more than three moduli are forced.

CONCLUSION: printed; used inside M_eliminate.py's successor.
"""
import sys, os
from fractions import Fraction
from math import gcd
from itertools import combinations
from sympy import isprime


def f(T):
    s = sum(Fraction(1, m) for m in T) - 1
    p = Fraction(1)
    for m in T:
        p *= Fraction(m - 1, m)
    return s + p


def best_coprime_f(S):
    """max of f(T) over pairwise coprime T subset S (S is small: only forced moduli)."""
    S = sorted(S)
    best = Fraction(0)
    n = len(S)

    def rec(i, cur):
        nonlocal best
        if cur:
            v = f(cur)
            if v > best:
                best = v
        for j in range(i, n):
            if all(gcd(S[j], x) == 1 for x in cur):
                rec(j + 1, cur + [S[j]])
    rec(0, [])
    return best


def pool_H(LH):
    ds, i = [], 1
    while i * i <= LH:
        if LH % i == 0:
            for x in (i, LH // i):
                if x >= 2 and x not in ds and isprime(2 * x + 1):
                    ds.append(x)
        i += 1
    return sorted(ds)


def test(L, verbose=False):
    """returns ('KILL', data) or ('SURVIVE', data)."""
    LH = L // 2
    S = pool_H(LH)
    B = sum(Fraction(1, m) for m in S)
    if B < 2:
        return ('KILL', ('budget', float(B)))
    forced = [m for m in S if B - Fraction(1, m) < 2]
    if not forced:
        return ('SURVIVE', ('no forced moduli', float(B)))
    if len(forced) > 22:
        return ('SURVIVE', ('too many forced moduli to enumerate colourings', len(forced)))
    slack = B - 2
    best_min = None
    for mask in range(1 << len(forced)):
        F0 = [forced[i] for i in range(len(forced)) if not (mask >> i) & 1]
        F1 = [forced[i] for i in range(len(forced)) if (mask >> i) & 1]
        tot = best_coprime_f(F0) + best_coprime_f(F1)
        if best_min is None or tot < best_min:
            best_min = tot
            if best_min <= slack:
                break                       # a colouring survives; no contradiction
    if best_min > slack:
        return ('KILL', ('A2+', forced, float(best_min), float(slack)))
    return ('SURVIVE', ('A2+ insufficient', forced, float(best_min), float(slack)))


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:]]
    if not Ls:
        # the 27 lcm candidates <= 1e6 that survive Theorem A3
        Ls = [55440, 110880, 166320, 221760, 262080, 277200, 327600, 332640, 388080, 393120,
              443520, 498960, 524160, 554400, 589680, 609840, 655200, 665280, 720720, 776160,
              786240, 831600, 887040, 917280, 942480, 982800, 997920]
    nk = 0
    for L in Ls:
        v, data = test(L)
        if v == 'KILL':
            nk += 1
        print(f"L = {L:<9} {v:8s} {data}")
    print(f"\nkilled by the strengthened A2+ test: {nk} of {len(Ls)}")
