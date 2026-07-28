"""
Q4 -- greedy theory for block sums.

(1) THE NAIVE GREEDY.  For rho = u/v let a be least with H(a,a+1) <= rho and
    put rho' = rho - H(a,a+1).  We record num(rho') vs u.  (Prompt's warning.)

(2) DOES ANY BLOCK DECREASE THE NUMERATOR?  For each rho and each block [a,b]
    with a >= T and H(a,b) <= rho we test num(rho - H(a,b)) < num(rho).
    (Exhaustive over a <= AMAX, length <= K.)

(3) THE ENDGAME IS DIOPHANTINE.  rho = u/v is a length-2 block sum
    H(a,a+1) = (2a+1)/(a(a+1))  iff  u a^2 + (u-2v) a - v = 0 has a positive
    integer root, which forces  u^2 + 4 v^2  to be a perfect square.
    We verify this and count how rare it is.

(4) LENGTH BOUND THEOREM (route-D).  If H(c,d) = u/v in lowest terms, k=d-c+1,
    t = -v_2(u/v), then
          2^t * C(d,k)  <=  v * d^{pi(k)}          and     k v/u <= d <= k(v/u+1).
    Verified numerically here; it is the engine behind blocks.blocks_with_sum.
"""

import sys
from fractions import Fraction
from math import comb, isqrt

from blocks import H, blocks_with_sum, v2, min_start_for_target, _pi


def naive_greedy_step(rho):
    a = min_start_for_target(rho)
    return a, rho - H(a, a + 1)


def experiment_naive(targets, steps=3):
    rows = []
    for rho in targets:
        r = Fraction(rho)
        seq = [r]
        for _ in range(steps):
            a, r = naive_greedy_step(r)
            seq.append(r)
            if r == 0:
                break
        rows.append((rho, [(x.numerator if x.numerator.bit_length() < 60
                            else "~2^%d" % x.numerator.bit_length()) for x in seq]))
    return rows


def unit_fraction_greedy_theorem(NMAX):
    """
    THEOREM Q4.1.  For every N >= 1 the largest length-2 block sum <= 1/N is
    H(2N,2N+1), and  1/N - H(2N,2N+1) = 1/(2N(2N+1)).
    So the greedy maps a unit fraction to a unit fraction: the numerator is
    stuck at 1 forever and the algorithm never terminates.
    """
    bad = []
    for N in range(1, NMAX + 1):
        rho = Fraction(1, N)
        a = min_start_for_target(rho)
        if a != 2 * N:
            bad.append(("start", N, a))
        if rho - H(2 * N, 2 * N + 1) != Fraction(1, 2 * N * (2 * N + 1)):
            bad.append(("rem", N))
        if H(2 * N - 1, 2 * N) <= rho:
            bad.append(("maximality", N))
    return bad


def no_largest_block_sum(rho, tries=6):
    """
    The greedy is ill-posed if all lengths are allowed: for each start a the
    best block sum <= rho is H(a,b(a)) with rho - H(a,b(a)) < 1/(b(a)+1) -> 0,
    so sup{H(I) : H(I) <= rho} = rho is NOT attained (Theorem Q1).
    """
    out = []
    a = min_start_for_target(rho)
    for _ in range(tries):
        h = Fraction(1, a)
        b = a
        while h + Fraction(1, b + 1) <= rho:
            b += 1
            h += Fraction(1, b)
        out.append((a, b, rho - h))
        a = 2 * a + 1
    return out


def any_block_decreases(rho, T, AMAX, K):
    """returns list of blocks [a,b] with num(rho-H) < num(rho) (and rho-H>=0)"""
    u = Fraction(rho).numerator
    good = []
    for k in range(2, K + 1):
        for a in range(T, AMAX + 1):
            b = a + k - 1
            h = H(a, b)
            if h > rho:
                continue
            d = Fraction(rho) - h
            if d == 0:
                good.append((a, b, 0))
            elif d.numerator < u:
                good.append((a, b, d.numerator))
    return good


def pythagorean_test(u, v):
    """is u^2+4v^2 a square?  and does the quadratic have a positive integer root?"""
    D = u * u + 4 * v * v
    s = isqrt(D)
    if s * s != D:
        return None
    num = (2 * v - u) + s
    if num % (2 * u):
        return None
    a = num // (2 * u)
    return a if a >= 1 else None


def verify_length_bound(AMAX, KMAX):
    bad = []
    for a in range(2, AMAX + 1):
        for k in range(2, KMAX + 1):
            b = a + k - 1
            h = H(a, b)
            u, v = h.numerator, h.denominator
            t = -v2(h)
            if (1 << t) * comb(b, k) > v * b ** _pi(k):
                bad.append(("bound", a, b))
            if not (k * v <= u * b and u * b <= k * (v + u)):
                bad.append(("range", a, b))
    return bad


if __name__ == "__main__":
    print("== (0) THEOREM Q4.1: greedy on a unit fraction is a fixed point ==")
    bad = unit_fraction_greedy_theorem(3000)
    print("   for 1<=N<=3000: greedy block = [2N,2N+1] and remainder = "
          "1/(2N(2N+1)) :", "OK" if not bad else bad[:5])
    r = Fraction(1, 6)
    chain = []
    for _ in range(4):
        a = min_start_for_target(r)
        chain.append((a, a + 1))
        r = r - H(a, a + 1)
    print("   1/6 greedy chain of blocks:", chain, " remainder", r)

    print("== (0b) the 'largest block sum <= rho' does NOT exist (sup not attained) ==")
    for (a, b, gap) in no_largest_block_sum(Fraction(1, 6), 6):
        print("   start %-8d block [%d,%d]  rho-H = %s" % (a, a, b, gap))

    print("== (1) naive length-2 greedy: numerators along the run ==")
    tg = [Fraction(1, 2), Fraction(1, 20), Fraction(5, 12), Fraction(3, 7),
          Fraction(1), Fraction(6, 5)]
    for rho, nums in experiment_naive(tg):
        print("   rho=%-10s numerators: %s" % (rho, nums))

    print("== (2) is there ANY block that lowers the numerator? ==")
    for rho in [Fraction(1, 2), Fraction(1, 6), Fraction(1, 20), Fraction(5, 12),
                Fraction(3, 7), Fraction(7, 30), Fraction(11, 2520)]:
        g = any_block_decreases(rho, 2, 400, 6)
        print("   rho=%-10s  #blocks lowering num: %d   e.g. %s"
              % (rho, len(g), g[:3]))

    print("== (3) endgame: rho is a length-2 block sum iff u^2+4v^2 is a square ==")
    hits = []
    tot = 0
    for v in range(2, 200):
        for u in range(1, v):
            f = Fraction(u, v)
            if f.numerator != u:
                continue
            tot += 1
            a = pythagorean_test(u, v)
            if a is not None and H(a, a + 1) == f:
                hits.append((u, v, a))
    print("   among %d reduced u/v in (0,1) with v<200: %d are 2-block sums"
          % (tot, len(hits)))
    print("   they are exactly (2a+1)/(a(a+1)):", hits[:8])

    print("== (4) length-bound theorem check ==")
    bad = verify_length_bound(300, 14)
    print("   2^t C(d,k) <= v d^pi(k)  and  kv/u <= d <= k(v+u)/u for all blocks "
          "a<=300,k<=14 :", "OK" if not bad else bad[:5])
