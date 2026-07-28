#!/usr/bin/env python3
"""
threshold.py -- for each T, the smallest N such that the Rule-(P)+legality
fixpoint of [T,N] can still carry the target.

Since the fixpoint only deletes elements that cannot lie in ANY legal W with
sum = u/v, an empty fixpoint (or one whose total reciprocal sum is below the
target) is a PROOF that no such W exists inside [T,N].  So for every T this
prints an exact, exhaustively established lower bound Nmin(T): there is no
legal U with min U >= T, max U <= N and sum 1/n = u/v for any N < Nmin(T).

usage: threshold.py Tlist... [--target u/v] [--hi H]
"""
import sys
from fractions import Fraction
from prune import prune


def feasible(T, N, u, v):
    A = prune(T, N, u, v)
    if not A:
        return False, 0, Fraction(0)
    tot = sum(Fraction(1, n) for n in A)
    return tot >= Fraction(u, v), len(A), tot


def main():
    args = sys.argv[1:]
    u, v = 1, 1
    hi = 4000
    while args and args[0].startswith("--"):
        if args[0] == "--target":
            f = Fraction(args[1]); u, v = f.numerator, f.denominator; del args[:2]
        elif args[0] == "--hi":
            hi = int(args[1]); del args[:2]
        else:
            raise SystemExit("bad option")
    Ts = [int(x) for x in args]
    print(f"target {u}/{v}")
    for T in Ts:
        lo, ok = T, None
        # exponential search then bisection
        N = max(T + 1, int(T * 2.8))
        while N <= hi:
            f, sz, tot = feasible(T, N, u, v)
            if f:
                ok = N
                break
            lo = N
            N = int(N * 1.15) + 1
        if ok is None:
            print(f"T={T:5d}  Nmin > {hi} (no feasible window found up to {hi})")
            continue
        a, b = lo, ok
        while a + 1 < b:
            m = (a + b) // 2
            f, sz, tot = feasible(T, m, u, v)
            if f:
                b = m
            else:
                a = m
        f, sz, tot = feasible(T, b, u, v)
        print(f"T={T:5d}  Nmin={b:5d}  ratio={b/T:.3f}  |A|={sz}  maxsum={float(tot):.5f}"
              f"   [PROOF: no solution with min>={T}, max<{b}]", flush=True)


if __name__ == "__main__":
    main()
