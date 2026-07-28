#!/usr/bin/env python3
"""
mkprob.py -- write a problem file for esearchB with an ARBITRARY rational
target (the stock engine is limited to 64-bit numerator/denominator).

The extension is exact: we compute in Python
    X0   = target * lcm(A)                (an integer; the engine's root state)
    tg_p = (target * p^{E_p}) mod p^{E_p} , E_p = max_{n in A} v_p(n)
(the p-adic target residues that padic.h would otherwise derive from u/v) and
hand both to the engine.  No floating point.

usage (as a library):  write_prob(path, T, N, A, target)
"""
import sys, os
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import primes_upto, nu


def write_prob(path, T, N, A, target):
    A = sorted(A)
    L = 1
    for n in A:
        L = L * n // gcd(L, n)
    X0f = target * L
    assert X0f.denominator == 1, "target denominator does not divide lcm(A)"
    X0 = X0f.numerator
    assert X0 >= 0
    num, den = target.numerator, target.denominator
    ovr = []
    for p in primes_upto(N):
        E = 0
        for n in A:
            e = nu(n, p)
            if e > E:
                E = e
        if E == 0:
            continue
        f = nu(den, p)
        if f > E:
            raise ValueError(f"target denominator has p={p} to the power {f} > E={E}")
        M = p ** E
        vv = den // p ** f
        tg = (num % M) * pow(p, E - f, M) % M * pow(vv % M, -1, M) % M
        ovr.append((p, tg))
    with open(path, "w") as fh:
        fh.write(f"{T} {N} 1 1\n{len(A)}\n")
        fh.write(" ".join(map(str, A)) + "\n")
        fh.write("BIG\n")
        fh.write(f"{X0}\n{len(ovr)}\n")
        for p, tg in ovr:
            fh.write(f"{p} {tg}\n")
    return L, X0


def main():
    # self-test: rebuild a known .prob (target 1/2) in BIG form
    import build as B
    from design import rulep_fixpoint
    T, N, z0 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tgt = Fraction(sys.argv[4]) if len(sys.argv) > 4 else Fraction(1, 2)
    out = sys.argv[5] if len(sys.argv) > 5 else "big.prob"
    A, S0, rough = B.designed_universe(T, N, z0)
    A = rulep_fixpoint(A, N, tgt.numerator, tgt.denominator)
    L, X0 = write_prob(out, T, N, A, tgt)
    print(f"wrote {out}: |A|={len(A)} lcm bits={L.bit_length()} X0 bits={X0.bit_length()}")


if __name__ == "__main__":
    main()
