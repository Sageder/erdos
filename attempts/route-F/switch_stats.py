#!/usr/bin/env python3
"""Exhaustive statistics of switch values c on a window, for fixed D.

For window [x,y] and modulus D:
  F = free elements (Lemma F1)
  L = lcm(F), g = gcd(L,D), M = L/g
  a sign vector eps in {-1,0,1}^F gives S = sum eps_n (L/n); the pair is a switch
  iff M | S, and then c = (D/g)*(S/M).
Reports min |c| over nonzero switches and the multiset of small |c|.

usage: switch_stats.py x y D [maxF]
"""
import sys
from math import gcd
from lib import smallest_prime_factors, lcm_list
from switch_search import free_elements


def enumerate_switch_c(F, D, halfcap=None):
    """returns dict c -> one representative (Aprime, Bprime), exhaustive."""
    L = lcm_list(F)
    g = gcd(L, D)
    M = L // g
    wts = [L // n for n in F]
    k = len(F)
    h = k // 2
    left = list(range(h)); right = list(range(h, k))

    table = {}
    for code in range(3 ** len(right)):
        c = code; S = 0
        for i in right:
            t = c % 3; c //= 3
            if t == 1: S -= wts[i]
            elif t == 2: S += wts[i]
        table.setdefault(S % M, []).append((code, S))

    res = {}
    for code in range(3 ** len(left)):
        c = code; S = 0
        for i in left:
            t = c % 3; c //= 3
            if t == 1: S -= wts[i]
            elif t == 2: S += wts[i]
        r = (-S) % M
        for rcode, RS in table.get(r, ()):
            tot = S + RS
            if tot == 0:
                continue
            assert tot % M == 0
            cv = (D // g) * (tot // M)
            if cv in res:
                continue
            eps = [0] * k
            cc = code
            for i in left:
                eps[i] = cc % 3; cc //= 3
            cc = rcode
            for i in right:
                eps[i] = cc % 3; cc //= 3
            Ap = [F[i] for i in range(k) if eps[i] == 1]
            Bp = [F[i] for i in range(k) if eps[i] == 2]
            res[cv] = (Ap, Bp)
    return res, L, g, M


if __name__ == "__main__":
    x = int(sys.argv[1]); y = int(sys.argv[2]); D = int(sys.argv[3])
    maxF = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    spf = smallest_prime_factors(y + 2)
    F = free_elements(x, y, D, spf)
    print("window [%d,%d] w=%d D=%d  |F|=%d" % (x, y, y - x, D, len(F)))
    print("F =", F)
    if len(F) > maxF:
        print("SKIP (|F| too large for exhaustive)")
        sys.exit(0)
    res, L, g, M = enumerate_switch_c(F, D)
    print("gcd(lcm F, D) = %d ;  D/g = %d  (every c is a multiple of D/g)" % (g, D // g))
    if not res:
        print("NO nonzero switch")
        sys.exit(0)
    cs = sorted(res, key=abs)
    print("number of distinct c: %d ; min|c| = %d" % (len(res), abs(cs[0])))
    for cv in cs[:6]:
        Ap, Bp = res[cv]
        print("   c=%d  A'=%s B'=%s" % (cv, Ap, Bp))
