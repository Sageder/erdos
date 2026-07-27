"""plain_linear_profile.py — decision gate for contiguous-block architectures.

Question: do monotone-4-AP-free (both orientations) permutations of [1..N] with
pos(v) <= C*v exist as N grows, for C in {8, 15}? Any contiguous geometric-block
construction (e.g. ratio-3 blocks, bounded block-order displacement) induces a linear
profile with modest C; extinction here would kill ALL such architectures at once
(via CORE.md Lemma 6 restrictions). Survival keeps them viable.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from asym_linear_profile import solve_profile

for C in (8, 15):
    for N in (60, 100, 150, 200, 260):
        t0 = time.time()
        sat, perm = solve_profile(N, C, dec3=False, inc4=True, dec4=True)
        dt = time.time() - t0
        print(f"plain C={C} N={N}: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)", flush=True)
        if not sat:
            break
