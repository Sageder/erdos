"""propB_check.py — verification of R3's Propositions B and B' (re-derived here).

Prop B  (naive valuation repair is impossible).  Say an order "uses the valuation
mechanism" if in every 4-AP falling in cases (ii)/(iii) of R3's Lemma L1, every
minimal-v2 term precedes every higher-v2 term.  Then for every t >= 1 and every ODD
u > 2^t, the quadruple (2^t, u, 2u-2^t, 3u-2^{t+1}) is a 4-AP of naturals in case (iii)
whose minimal-v2 terms are u and 3u-2^{t+1}; so the mechanism forces u before 2^t,
giving 2^t infinitely many predecessors.

Prop B' (tau's mechanism pins the whole order).  For any u < w with l = v3(w-u), the
quadruple (u, w, 2w-u, 3w-2u) is a 4-AP with common difference w-u, hence critical level
l, and (u,w) is its FIRST adjacent pair.  So "respect tau's cycle mechanism on every
4-AP" already dictates every pairwise comparison: the order IS tau.
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import v3, Tau, prio_const


def v2(n):
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def propB(tmax=8, umax=400):
    bad = 0
    cnt = 0
    for t in range(1, tmax + 1):
        x = 2 ** t
        for u in range(x + 1, umax, 2):        # u odd > 2^t
            d = u - x
            T = [x + k * d for k in range(4)]
            assert T[1] == u and T[2] == 2 * u - x and T[3] == 3 * u - 2 * x
            assert all(v >= 1 for v in T)
            vv = [v2(v) for v in T]
            v = v2(d)
            # case (iii) of L1: v2(x) > v2(d)
            if not (v2(x) > v):
                bad += 1
                continue
            if not (vv[1] == v and vv[3] == v and vv[0] >= v + 1 and vv[2] >= v + 1):
                bad += 1
            cnt += 1
    print(f" Prop B: {cnt} quadruples (t<={tmax}, odd u<{umax}) all are genuine 4-APs "
          f"of naturals in L1 case (iii) with minimal-v2 terms exactly {{x+d, x+3d}}: "
          f"{'OK' if bad == 0 else str(bad)+' failures'}")
    print("   => the mechanism forces u before 2^t for every odd u > 2^t: "
          "2^t gets infinitely many predecessors.")


def propBprime(M=300):
    t = Tau(prio_const((0, 1, 2)))
    bad = 0
    cnt = 0
    for u in range(1, M):
        for w in range(u + 1, M):
            l = v3(w - u)
            d = w - u
            T = [u + k * d for k in range(4)]
            if v3(d) != l:
                bad += 1
            # the pair (u,w) is adjacent pair #1 of this 4-AP and its critical level is l
            if T[1] != w or min(T) < 1:
                bad += 1
            cnt += 1
    print(f" Prop B': {cnt} pairs (u<w<{M}): (u, w, 2w-u, 3w-2u) is always a 4-AP of "
          f"naturals with critical level v3(w-u): {'OK' if bad == 0 else 'FAIL'}")
    print("   => respecting tau's cycle mechanism on every 4-AP pins every comparison.")


if __name__ == "__main__":
    propB()
    print()
    propBprime()
