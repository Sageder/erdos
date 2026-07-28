#!/usr/bin/env python3
"""
Recon-3: build a pruned universe for the range [T,N] (my own Rule A + legality
fixpoint, see av_fixpoint2.py for the derivation), emit it for av_far.c.

usage: python3 av_universe.py T N > universe.txt
"""
import sys
from fractions import Fraction
from math import gcd


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]:
            s[i * i:: i] = bytearray(len(s[i * i:: i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def has_zero_subset(res, p):
    reach = set()
    for r in res:
        new = {r} | {(x + r) % p for x in reach}
        reach |= new
        if 0 in reach:
            return True
    return 0 in reach


def fixpoint(A, N):
    A = set(A)
    P = primes_upto(N)
    changed = True
    while changed and A:
        changed = False
        for p in P:
            while True:
                e, C = 0, []
                for n in A:
                    if n % p == 0:
                        v = nu(n, p)
                        if v > e:
                            e, C = v, [n]
                        elif v == e:
                            C.append(n)
                if e == 0:
                    break
                pe = p ** e
                if has_zero_subset([pow(n // pe, -1, p) for n in C], p):
                    break
                A -= set(C)
                changed = True
                if not A:
                    return A
        while True:
            hit = [n for n in A if (n - 1) not in A and (n + 1) not in A]
            if not hit:
                break
            A -= set(hit)
            changed = True
    return A


if __name__ == "__main__":
    T, N = int(sys.argv[1]), int(sys.argv[2])
    A = sorted(fixpoint(range(T, N + 1), N))
    L = 1
    for n in A:
        L = L * n // gcd(L, n)
    tot = sum(Fraction(1, n) for n in A)
    sys.stderr.write("T=%d N=%d  |universe|=%d  lcm bits=%d  sum=%.4f\n"
                     % (T, N, len(A), L.bit_length(), float(tot)))
    print(len(A))
    print(" ".join(map(str, A)))
