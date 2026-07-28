"""
F_scan_worlds.py -- Route F, Erdos 273, task (c) preliminaries.

CLAIM TESTED: which L have enough admissible divisors to permit a covering
system with distinct moduli in
    H = {m : 2m+1 prime}     (an E-covering splits by parity into two DISJOINT
                              H-coverings, so H is the natural "half world"), and
    E = {p-1 : p >= 5 prime} = {n : n>=4, n+1 prime}   (all such n are even).
Necessary reciprocal-budget conditions for a covering with moduli dividing L:
    B_H(L) := sum_{d | L, d in H} 1/d  >  1
    B_E(L) := sum_{d | L, d in E} 1/d  >  1
and, for E, the parity split gives the equivalent stronger condition on L/2:
    B_H(L/2) > 2   (two DISJOINT H-coverings by divisors of L/2 are needed).

CONCLUSION: printed table; recorded in attempts/route-F-efficiency/FINDINGS.md.
"""
import sys
from fractions import Fraction

LIM = 400000


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return s


PR = sieve(2 * LIM + 3)
from F_mincost import _is_prime

def inH(d):
    if d < 2:
        return False
    n = 2 * d + 1
    return bool(PR[n]) if n < len(PR) else _is_prime(n)

def inE(d):
    if d < 4:
        return False
    n = d + 1
    return bool(PR[n]) if n < len(PR) else _is_prime(n)
PRED = {"H": inH, "E": inE}


def divisors(L):
    ds, i = [], 1
    while i * i <= L:
        if L % i == 0:
            ds.append(i)
            if i != L // i:
                ds.append(L // i)
        i += 1
    return sorted(ds)


def budget(L, world):
    ds = [d for d in divisors(L) if d > 1 and PRED[world](d)]
    return sum(Fraction(1, d) for d in ds), ds


def smallest_with_budget(world, thresh, limit):
    acc = [0.0] * (limit + 1)
    pred = PRED[world]
    for d in range(2, limit + 1):
        if pred(d):
            inv = 1.0 / d
            for m in range(d, limit + 1, d):
                acc[m] += inv
    for L in range(2, limit + 1):
        if acc[L] > thresh - 1e-9:
            b, ds = budget(L, world)
            if b > thresh:
                return L, b, ds
    return None


def smooth_numbers(pmax, limit):
    ps = [p for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43) if p <= pmax]
    out = [1]
    for p in ps:
        new = []
        for v in out:
            w = v
            while w <= limit:
                new.append(w)
                w *= p
        out = new
    return sorted(set(out))


def main():
    for world, thresh, lim in (("H", 1, LIM), ("E", 1, LIM)):
        r = smallest_with_budget(world, thresh, lim)
        if r:
            L, b, ds = r
            print(f"smallest L <= {lim} with {world}-budget > {thresh}: L={L} "
                  f"budget={b}={float(b):.5f}", flush=True)
            print(f"    {world}-divisors: {ds}", flush=True)
        else:
            print(f"NO L <= {lim} has {world}-budget > {thresh}", flush=True)

    print("\n=== best H-budget among p-smooth L (L <= bound) ===", flush=True)
    for pmax, bound in ((3, 10 ** 12), (5, 10 ** 12), (7, 10 ** 12),
                        (11, 10 ** 13), (13, 10 ** 14), (17, 10 ** 15),
                        (19, 10 ** 16), (23, 10 ** 17)):
        vals = smooth_numbers(pmax, bound)
        bb, bL, bn = 0, None, 0
        for L in vals:
            b, ds = budget(L, "H")
            if b > bb:
                bb, bL, bn = b, L, len(ds)
        print(f"  {pmax:2}-smooth, L<={bound:.0e}: max B_H = {float(bb):.5f} "
              f"at L={bL} (#H-div={bn}) [#cand={len(vals)}]", flush=True)

    print("\n=== best E-budget among p-smooth L ===", flush=True)
    for pmax, bound in ((3, 10 ** 12), (5, 10 ** 12), (7, 10 ** 13),
                        (11, 10 ** 14), (13, 10 ** 15), (17, 10 ** 16)):
        vals = smooth_numbers(pmax, bound)
        bb, bL, bn = 0, None, 0
        for L in vals:
            b, ds = budget(L, "E")
            if b > bb:
                bb, bL, bn = b, L, len(ds)
        print(f"  {pmax:2}-smooth, L<={bound:.0e}: max B_E = {float(bb):.5f} "
              f"at L={bL} (#E-div={bn})", flush=True)


if __name__ == "__main__":
    main()
