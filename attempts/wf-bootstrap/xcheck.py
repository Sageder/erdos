#!/usr/bin/env python3
"""xcheck.py -- verify universe2.build == universe.build_with_banned on random inputs."""
import random
from fractions import Fraction
import universe as U1, universe2 as U2

random.seed(1)
bad = 0
for trial in range(8):
    T = random.randint(2, 40)
    N = T + random.randint(15, 45)
    q = Fraction(random.randint(1, 5), random.randint(2, 40))
    ban = set(random.sample(range(T, N + 1), random.randint(0, 5)))
    a = U1.build_with_banned(T, N, q, ban)
    b = U2.build(T, N, q, ban)
    a = a if a else None
    b = b if b else None
    print("  trial", trial, T, N, q, "ok" if a==b else "MISMATCH", flush=True)
    if a != b:
        bad += 1
        print("MISMATCH", T, N, q, sorted(ban), a, b)
print("trials 8, mismatches", bad)
