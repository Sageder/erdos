#!/usr/bin/env python3
"""
Build the Rule-(P) + legality fixpoint of an element range [T, N], for target 1.

RULE (P):  if Sigma(U) = 1 and p is prime with E = max{nu_p(n) : n in U, p|n},
then  sum_{n in U, p|n} p^E/n  ==  0  (mod p^E)   (all terms are p-adic integers).
Hence an element n (with p|n) may be deleted whenever NO subset of the current
multiples of p that CONTAINS n has residue 0 mod p^E.  Decided exactly by a
forward/backward subset-reachability DP over the p^E residues.

RULE (L):  legality -- if both neighbours of n are deleted, delete n.

Both rules only delete, so iterating to a fixpoint is sound: every legal U with
Sigma(U)=1 and U subset [T,N] survives.

usage: python3 universe_range.py T N [outfile]
"""
import sys
from math import gcd


def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


def nu(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def prune(T, N, verbose=False):
    P = primes_upto(N)
    A = set(range(T, N + 1))
    changed = True
    while changed:
        changed = False
        for p in P:
            M = sorted(n for n in A if n % p == 0)
            if not M: continue
            E = max(nu(n, p) for n in M)
            pe = p ** E
            w = []
            for n in M:
                e = nu(n, p); m = n // p ** e
                w.append((p ** (E - e) * pow(m, -1, pe)) % pe)
            # forward[i] = set of residues reachable from the first i weights
            fwd = [None] * (len(M) + 1)
            cur = {0}
            fwd[0] = cur
            for i, x in enumerate(w):
                cur = cur | {(r + x) % pe for r in cur}
                fwd[i + 1] = cur
            bwd = [None] * (len(M) + 1)
            cur = {0}
            bwd[len(M)] = cur
            for i in range(len(M) - 1, -1, -1):
                cur = cur | {(r + w[i]) % pe for r in cur}
                bwd[i] = cur
            dead = []
            for i, n in enumerate(M):
                # need a subset containing n with total residue 0
                ok = any((a + w[i] + b) % pe == 0 for a in fwd[i] for b in bwd[i + 1])
                if not ok: dead.append(n)
            if dead:
                for n in dead: A.discard(n)
                changed = True
        # legality
        dead = [n for n in A if (n - 1) not in A and (n + 1) not in A]
        if dead:
            for n in dead: A.discard(n)
            changed = True
    return sorted(A)


if __name__ == "__main__":
    T, N = int(sys.argv[1]), int(sys.argv[2])
    A = prune(T, N)
    L = 1
    for n in A: L = L * n // gcd(L, n)
    print(f"[{T},{N}] |universe|={len(A)}  lcm bits={L.bit_length()}  fits128={L < 2**127}")
    if len(sys.argv) > 3:
        open(sys.argv[3], "w").write(" ".join(map(str, A)))
