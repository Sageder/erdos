#!/usr/bin/env python3
"""
combine.py target poolfile1 poolfile2 [poolfile3 ...]

Pick ONE gadget from each pool (or from a subset of the pools) so that the
values add up EXACTLY to the target rational.  The pools must come from
pairwise disjoint windows; the union of the chosen gadgets is then a legal
system (a union of legal systems in disjoint windows has no isolated point)
whose sum is the target and whose minimum element is the minimum over the
windows used.

All arithmetic is exact: values are handled as integers over the common
denominator  Dstar = lcm of all gadget denominators.

Search: exhaustive meet-in-the-middle over the first pools, linear scan of the
last.  Prints the certificate; run verify.py on it afterwards.
"""
import sys
from fractions import Fraction
from math import gcd


def load(fn):
    out = []
    for line in open(fn):
        t = line.split()
        if len(t) < 3:
            continue
        num, den = int(t[0]), int(t[1])
        U = [int(x) for x in t[2:]]
        out.append((Fraction(num, den), U))
    return out


def main():
    target = Fraction(sys.argv[1]) if "/" in sys.argv[1] else Fraction(int(sys.argv[1]))
    pools = [load(f) for f in sys.argv[2:]]
    for f, p in zip(sys.argv[2:], pools):
        print("# pool %s : %d values, range %.6f .. %.6f, min elt %d"
              % (f, len(p), float(min(v for v, _ in p)), float(max(v for v, _ in p)),
                 min(min(U) for _, U in p)))
    D = target.denominator
    for p in pools:
        for v, _ in p:
            D = D * v.denominator // gcd(D, v.denominator)
    print("# common denominator Dstar has %d bits" % D.bit_length())
    tgt = target.numerator * (D // target.denominator)

    if len(pools) == 2:
        A = {}
        for v, U in pools[0]:
            A[v.numerator * (D // v.denominator)] = U
        for v, U in pools[1]:
            x = v.numerator * (D // v.denominator)
            if tgt - x in A:
                sol = sorted(A[tgt - x] + U)
                print("FOUND", " ".join(map(str, sol)))
                return 0
        print("no combination found (2 pools)")
        return 1

    # >= 3 pools : merge the first two into a sorted array of sums
    import itertools
    P0 = [(v.numerator * (D // v.denominator), U) for v, U in pools[0]]
    P1 = [(v.numerator * (D // v.denominator), U) for v, U in pools[1]]
    rest = [[(v.numerator * (D // v.denominator), U) for v, U in p] for p in pools[2:]]
    print("# building %d x %d pair table" % (len(P0), len(P1)))
    A = {}
    for x, U in P0:
        for y, V in P1:
            s = x + y
            if s not in A:
                A[s] = (U, V)
    print("# %d distinct pair sums" % len(A))
    for combo in itertools.product(*[range(len(r)) for r in rest]):
        s = 0
        Us = []
        for k, idx in enumerate(combo):
            x, U = rest[k][idx]
            s += x
            Us.append(U)
        need = tgt - s
        if need in A:
            U, V = A[need]
            sol = sorted(U + V + [n for W in Us for n in W])
            print("FOUND", " ".join(map(str, sol)))
            return 0
    print("no combination found")
    return 1


if __name__ == "__main__":
    sys.exit(main())
