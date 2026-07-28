"""
F_budget_growth.py -- Route F, Erdos 273: how fast can the admissible reciprocal
budget grow?

CLAIM TESTED: how large can
   B_H(L) = sum_{m | L, 2m+1 prime} 1/m        (H world)
   B_E(L) = sum_{n | L, n>=4, n+1 prime} 1/n   (E world)
be for L below a given size?  An E-covering with lcm 2L needs TWO DISJOINT
H-coverings with moduli dividing L, hence needs B_H(L) > 2 (in fact
> mu_1 + mu_2, and every H-covering measured so far costs >= 1.35).  So this
tabulates the SIZE of L needed before any given budget target is reachable.

Method: hill-climbing over the exponent vector of L (multiply/divide by a prime,
accept if B_H increases and L stays under the bound), restarted from many seeds.
This gives LOWER bounds on the achievable budget (i.e. it is a search, not a
proof of maximality) -- reported as MEASURED.

CONCLUSION: printed; see FINDINGS.md.
"""
import sys, random
from fractions import Fraction
from F_mincost import _is_prime

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

CACHE = {}


def inW(d, world):
    key = (d, world)
    v = CACHE.get(key)
    if v is None:
        v = _is_prime(2 * d + 1) if world == "H" else (d >= 4 and _is_prime(d + 1))
        CACHE[key] = v
    return v


def budget_from_exps(exps, world):
    """exps: dict prime->exponent.  Returns (L, budget as float, #admissible)."""
    L = 1
    ds = [1]
    for p, e in exps.items():
        if e == 0:
            continue
        L *= p ** e
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    b, n = 0.0, 0
    for d in ds:
        if d > 1 and inW(d, world):
            b += 1.0 / d
            n += 1
    return L, b, n


def climb(bound, world, iters=4000, seed=0, start=None):
    rng = random.Random(seed)
    exps = {p: 0 for p in PRIMES}
    exps[2] = 1
    if start:
        for p, e in start.items():
            exps[p] = e
    L, b, n = budget_from_exps(exps, world)
    while L > bound:                       # repair an over-large seed
        p = max((p for p in PRIMES if exps[p]), key=lambda q: q)
        exps[p] -= 1
        L, b, n = budget_from_exps(exps, world)
    for _ in range(iters):
        p = rng.choice(PRIMES)
        for delta in (1, -1):
            if exps[p] + delta < 0:
                continue
            trial = dict(exps)
            trial[p] += delta
            L2, b2, n2 = budget_from_exps(trial, world)
            if L2 <= bound and (b2 > b + 1e-15):
                exps, L, b, n = trial, L2, b2, n2
                break
    return L, b, n, {p: e for p, e in exps.items() if e}


def main():
    world = sys.argv[1] if len(sys.argv) > 1 else "H"
    print(f"world = {world};  best budget found by hill-climbing (MEASURED "
          f"lower bounds on the max)")
    carry = None
    for expo in range(2, 41):
        bound = 10 ** expo
        best = (0, None, None, None)
        for s in range(10):
            L, b, n, e = climb(bound, world, 4000, s,
                               start=(carry if s % 2 == 0 else None))
            if b > best[0]:
                best = (b, L, n, e)
        b, L, n, e = best
        carry = e
        print(f"  L <= 1e{expo:<2}: max B_{world} ~ {b:.5f}  at L={L}  "
              f"(#adm div={n})  factorisation {e}", flush=True)


if __name__ == "__main__":
    main()
