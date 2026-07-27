"""parity_construction.py — verify PROMPT §4 'finite avoidance at every length'.

Claim tested: the parity recursion sigma_N (odds of [1..N] ordered by the recursion on
[1..ceil(N/2)] mapped through y -> 2y-1, then evens via y -> 2y) is a monotone-3-AP-free
permutation of [1..N]. Machine-checked exhaustively for all N <= 256 and for
N in {512, 1024, 1536, 2048} (the prompt's proof covers all N; this is the sanity check).
Also sigma_8 = (1,5,3,7,2,6,4,8).
Conclusion: printed below.
"""

import sys
import numpy as np
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute

sys.setrecursionlimit(10000)


def sigma(n):
    if n == 1:
        return [1]
    m = (n + 1) // 2          # count of odds in [1..n]
    odds = [2 * y - 1 for y in sigma(m)]
    evens = [2 * y for y in sigma(n // 2)]
    return odds + evens


def has_monotone_3ap_np(perm):
    """Vectorized: perm is a permutation of 1..n as list. Returns True iff monotone 3-AP."""
    n = len(perm)
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.array(perm)] = np.arange(n)
    for d in range(1, (n - 1) // 2 + 1):
        top = n - 2 * d
        if top < 1:
            break
        p1 = pos[1:top + 1]
        p2 = pos[1 + d:top + d + 1]
        p3 = pos[1 + 2 * d:top + 2 * d + 1]
        if np.any(((p1 < p2) & (p2 < p3)) | ((p1 > p2) & (p2 > p3))):
            return True
    return False


assert tuple(sigma(8)) == (1, 5, 3, 7, 2, 6, 4, 8), sigma(8)

# cross-validate numpy checker against the trusted one
import random
rng = random.Random(196)
for _ in range(500):
    n = rng.randint(3, 10)
    p = list(range(1, n + 1))
    rng.shuffle(p)
    assert has_monotone_3ap_np(p) == has_monotone_kap_pos(p, 3) == has_monotone_kap_brute(p, 3)

for n in list(range(1, 257)) + [512, 1024, 1536, 2048]:
    s = sigma(n)
    assert sorted(s) == list(range(1, n + 1)), n
    if n >= 3:
        assert not has_monotone_3ap_np(s), n
print("PARITY CONSTRUCTION VERIFIED: sigma_N is a 3-AP-free (hence 4-AP-free) permutation "
      "of [1..N] for all N <= 256 and N in {512,1024,1536,2048}; sigma_8 matches PROMPT.")
