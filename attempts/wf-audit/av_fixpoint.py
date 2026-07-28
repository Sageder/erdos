#!/usr/bin/env python3
"""
Recon-3 independent re-derivation of the "Rule (P) + legality fixpoint" prune.

Derivation (mine, from the definitions):
  Let U be legal with sum 1/n = 1 and U subseteq [2,N].
  (L)  every n in U has n-1 in U or n+1 in U.
  (P)  for every prime p and every n in U with e = nu_p(n) >= 1 there is a SECOND
       element m in U, m != n, with p^e | m.
       [Proof: E := max nu_p over U >= e.  If E = e, Rule (P) forces >= 2 elements
        at level E = e, so a second multiple of p^e.  If E > e, an element with
        nu_p = E > e is itself a multiple of p^e and differs from n.]
  Hence, if V is any set known to contain U, the set of n in V that satisfy (L) and
  (P) *relative to V* also contains U.  Iterating from V = [2,N] to a fixpoint gives
  a set containing every solution with max <= N; if the fixpoint is empty there is
  no such solution.

Prints the fixpoint size for each N and the largest N with empty fixpoint.
"""
import sys

def fixpoint(N, verbose=False):
    V = set(range(2, N + 1))
    while True:
        # prime-power data
        drop = set()
        for n in V:
            # (L)
            if (n - 1) not in V and (n + 1) not in V:
                drop.add(n); continue
            # (P)
            m = n
            p = 2
            bad = False
            while p * p <= m:
                if m % p == 0:
                    e = 0
                    while m % p == 0:
                        m //= p; e += 1
                    q = p ** e
                    if not any((x % q == 0) for x in V if x != n):
                        bad = True; break
                p += 1 if p == 2 else 2
            if not bad and m > 1:
                q = m
                if not any((x % q == 0) for x in V if x != n):
                    bad = True
            if bad:
                drop.add(n)
        if not drop:
            return V
        V -= drop

if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    lastempty = None
    for N in range(2, hi + 1):
        V = fixpoint(N)
        if not V:
            lastempty = N
        if N >= 70 or not V:
            print("N=%3d  fixpoint size %3d  %s" % (N, len(V), sorted(V) if len(V) <= 30 else ""))
    print("largest N with EMPTY fixpoint:", lastempty)
