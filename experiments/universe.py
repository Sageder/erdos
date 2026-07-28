#!/usr/bin/env python3
"""Compute the two-attainer-pruned universe of [T,N] for target denominator v,
and the lcm L of that universe (which must divide 2^127 for the C engine)."""
import sys
from math import gcd


def primes_upto(N):
    s = [True] * (N + 1); s[0] = s[1] = False
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            for j in range(i * i, N + 1, i): s[j] = False
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def universe(T, N, v=1):
    P = primes_upto(N); A = set(range(T, N + 1)); ch = True
    while ch:
        ch = False
        for p in P:
            fv = nu(v, p)
            while True:
                bv = {}
                for n in A:
                    e = nu(n, p)
                    if e: bv.setdefault(e, []).append(n)
                if not bv: break
                em = max(bv)
                if len(bv[em]) < 2 and em != fv:
                    for n in bv[em]: A.discard(n)
                    ch = True
                else: break
    return sorted(A)


def lcm_of(A, v=1):
    L = v
    for n in A:
        L = L * n // gcd(L, n)
    return L


if __name__ == "__main__":
    T, N = int(sys.argv[1]), int(sys.argv[2])
    v = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    A = universe(T, N, v); L = lcm_of(A, v)
    print(f"[{T},{N}] v={v}: |universe|={len(A)}  lcm has {len(str(L))} digits, "
          f"fits u128: {L < 2**127}")
    print("universe:", A)
