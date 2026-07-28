#!/usr/bin/env python3
"""
Search for finite U subset of Z_{>=2}, no isolated points, sum 1/n = 1,
max element <= N.   Exact arithmetic.  Strong p-adic pruning.

PRUNE (proved in PROBLEM.md / NOTES.md):
  if sum_{n in U} 1/n = 1 and p is a prime with e := max_{n in U} nu_p(n) >= 1,
  then at least TWO elements of U attain nu_p = e.
  (Otherwise the unique term 1/n_0 has nu_p = -e < 0 = nu_p(1), and since all
   other terms have nu_p > -e the valuation of the sum is exactly -e.)

Static consequences used to shrink the universe:
  * a prime power p^e <= N whose only multiple in [2,N] is p^e itself cannot be
    the top p-power, so any n with nu_p(n) = e is banned unless another multiple
    of p^e exists;  applied iteratively.
Dynamic prune: with remaining target u/v at position pos, every prime power
  p^e || v needs a multiple of p^e inside [pos, N].
"""
import sys
from fractions import Fraction


def primes_upto(N):
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]


def build_universe(N):
    """Iteratively remove n in [2,N] that cannot appear in any solution."""
    P = primes_upto(N)
    allowed = set(range(2, N + 1))
    changed = True
    while changed:
        changed = False
        for p in P:
            # group allowed numbers by nu_p
            byval = {}
            for n in allowed:
                e = 0
                m = n
                while m % p == 0:
                    m //= p
                    e += 1
                if e:
                    byval.setdefault(e, []).append(n)
            if not byval:
                continue
            emax = max(byval)
            # the top level must be attainable twice; else nobody can sit there
            while emax >= 1 and len(byval.get(emax, [])) < 2:
                for n in byval[emax]:
                    allowed.discard(n)
                    changed = True
                del byval[emax]
                emax = max(byval) if byval else 0
    return sorted(allowed)


def search(N, cap=10 ** 7, want=None, verbose=True):
    universe = build_universe(N)
    if verbose:
        banned = sorted(set(range(2, N + 1)) - set(universe))
        print(f"  universe |{len(universe)}| of {N-1}; banned: {banned}")
    allowed = [False] * (N + 2)
    for n in universe:
        allowed[n] = True
    # tail[pos] = sum of 1/n over allowed n >= pos
    tail = [Fraction(0)] * (N + 3)
    for n in range(N, 1, -1):
        tail[n] = tail[n + 1] + (Fraction(1, n) if allowed[n] else 0)
    P = primes_upto(N)

    def padic_ok(v, pos):
        for p in P:
            if v % p:
                continue
            e = 0
            while v % p == 0:
                v //= p
                e += 1
            pe = p ** e
            if pe > N:
                return False
            # smallest multiple of pe that is >= pos
            m = ((pos + pe - 1) // pe) * pe
            if m > N:
                return False
        return v == 1

    sols = []
    nodes = 0

    def dfs(pos, rem, runlen, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > cap:
            raise KeyboardInterrupt
        if rem == 0:
            if runlen != 1:
                sols.append(tuple(chosen))
                if want and len(sols) >= want:
                    raise KeyboardInterrupt
            return
        if pos > N or rem > tail[pos]:
            return
        if not padic_ok(rem.denominator, pos):
            return
        f = Fraction(1, pos)
        if allowed[pos] and f <= rem:
            chosen.append(pos)
            dfs(pos + 1, rem - f, runlen + 1, chosen)
            chosen.pop()
        elif runlen == 1:
            return
        if runlen != 1:
            dfs(pos + 1, rem, 0, chosen)

    try:
        dfs(2, Fraction(1), 0, [])
    except KeyboardInterrupt:
        pass
    return sols, nodes


def runs_of(U):
    U = sorted(U)
    runs, cur = [], [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur)
            cur = [x]
    runs.append(cur)
    return runs


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 7
    sols, nodes = search(N, cap=cap)
    print(f"N={N}  nodes={nodes}  solutions={len(sols)}")
    ks = {}
    for U in sols:
        assert sum(Fraction(1, n) for n in U) == Fraction(1)
        L = [len(r) for r in runs_of(U)]
        r, M = len(L), sum(l // 2 for l in L)
        for k in range(r, M + 1):
            ks.setdefault(k, (U, L))
    print("achievable k:", sorted(ks))
    for k in sorted(ks):
        U, L = ks[k]
        print(f"  k={k}: runlens={L}  U={list(U)}")
