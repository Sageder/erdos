#!/usr/bin/env python3
"""
s3_target.py -- complete DFS for:  legal U subset [A,M] with sum_{n in U} 1/n = T.

"legal" = no isolated point = disjoint union of blocks of length >= 2.

Exact Fraction arithmetic throughout.  Prunes:
  P1  remaining > H(pos,M)                       -> dead
  P2  1/pos > remaining and we are inside a run  -> dead (the run must continue)
  P3  p-adic:  with remaining u/v, every prime power p^k || v needs a multiple of
      p^k inside [pos,M]   (otherwise nu_p(future sum) > -k is impossible)

Usage:  python3 s3_target.py A M num den [maxnodes]
"""
import sys
from fractions import Fraction


def primes_upto(N):
    s = [True] * (N + 1)
    s[0:2] = [False, False]
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = [False] * len(s[i * i::i])
    return [i for i in range(2, N + 1) if s[i]]


def build_Q(A, M):
    """Q[pos] = prod_p p^{e_p(pos)} where e_p(pos) = max nu_p over [pos,M].
       Remaining u/v is feasible from pos only if v | Q[pos]."""
    P = primes_upto(M)
    Q = [1] * (M + 3)
    for pos in range(M + 1, A - 1, -1):
        pass
    # compute max nu_p over [pos,M] for each p, by scanning pos downward
    maxe = {p: 0 for p in P}
    Qv = [1] * (M + 3)
    cur = 1
    for pos in range(M, A - 1, -1):
        n = pos
        for p in P:
            if p * p > n and n > 1:
                p = n
            if n % p == 0:
                e = 0
                while n % p == 0:
                    n //= p
                    e += 1
                if e > maxe.get(p, 0):
                    cur = cur // (p ** maxe.get(p, 0)) * (p ** e)
                    maxe[p] = e
            if n == 1:
                break
        Qv[pos] = cur
    return Qv


def search(A, M, T, maxnodes=10 ** 9, want=1, verbose=True):
    tail = [Fraction(0)] * (M + 3)
    for n in range(M, A - 1, -1):
        tail[n] = tail[n + 1] + Fraction(1, n)
    Qv = build_Q(A, M)
    sols = []
    nodes = 0

    def dfs(pos, rem, runlen, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > maxnodes:
            raise KeyboardInterrupt
        if rem == 0:
            if runlen != 1:
                sols.append(tuple(chosen))
                if len(sols) >= want:
                    raise KeyboardInterrupt
            return
        if pos > M:
            return
        if rem > tail[pos]:
            return
        if Qv[pos] % rem.denominator != 0:
            return
        f = Fraction(1, pos)
        if f <= rem:
            chosen.append(pos)
            dfs(pos + 1, rem - f, runlen + 1, chosen)
            chosen.pop()
        elif runlen == 1:
            return
        if runlen != 1:
            dfs(pos + 1, rem, 0, chosen)

    try:
        dfs(A, T, 0, [])
    except KeyboardInterrupt:
        pass
    if verbose:
        print("A=%d M=%d T=%s  nodes=%d  solutions=%d" % (A, M, T, nodes, len(sols)))
        for s in sols[:20]:
            print("   ", s)
    return sols, nodes


if __name__ == "__main__":
    A = int(sys.argv[1]); M = int(sys.argv[2])
    T = Fraction(int(sys.argv[3]), int(sys.argv[4]))
    mn = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
    search(A, M, T, mn)
