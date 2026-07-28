#!/usr/bin/env python3
"""table_forced.py -- Corollary 2/3 table: z*(T,N), size and density of the
forced-out set X, and the number of surviving adjacent pairs, for a range of
windows.  Exact computation (sieve + exact integer symmetric functions)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from forced import analyse
from math import isqrt, log

print(f"{'T':>6} {'N':>7} {'sqrtN':>6} {'z*':>7} {'z*/(N-T)':>9} {'|X|':>6} "
      f"{'dens':>7} {'pairs':>7} {'W':>7} {'loglogN/logN':>12}")
for (T, N) in [(104,600),(104,900),(200,1000),(200,1800),(300,2700),(500,4500),
               (1000,9000),(2000,18000),(5000,45000),(10000,90000),(50000,450000)]:
    zs, forced, allowed, X = analyse(T, N)
    W = N - T + 1
    surv = set(range(T, N+1)) - X
    pairs = sum(1 for n in range(T, N) if n in surv and n+1 in surv)
    print(f"{T:>6} {N:>7} {isqrt(N):>6} {zs:>7} {zs/(N-T):>9.4f} {len(X):>6} "
          f"{len(X)/W:>7.4f} {pairs:>7} {W:>7} {log(log(N))/log(N):>12.4f}")
