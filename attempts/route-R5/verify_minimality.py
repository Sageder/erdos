"""verify_minimality.py — finite-avoider verification of the k-minimality lemmas
M1/M2 (lemmas_4apfree.md) and a realization census of the SAT-consistent cells.

For each finite 4-AP-free permutation of [1..N] that contains at least one increasing
3-AP, compute the k-minimal increasing 3-AP (x, d): the one whose top position
k = pos(x+2d) is smallest (ties impossible: tops at equal position coincide in value;
among same top value pick smallest d — irrelevant to the lemmas).  Check:

 M1: if x-d >= 1 and x+3d <= N:
        pos(x-d) > pos(x+d)  OR  pos(x+3d) < pos(x+d).
 M2: if x-3d >= 1 and x+3d <= N:
        pos(x-3d) > pos(x)   OR  pos(x+3d) < pos(x).

Census: joint region cell of (pos(x-d), pos(x+3d)) relative to i=pos(x), j=pos(x+d),
k=pos(x+2d), regions 0:<i, 1:(i,j), 2:(j,k), 3:>k — compared against the SAT window
predictions of probe_cases.py (cells UNSAT there must be empty here; SAT cells that
stay empty here are candidates for missing global lemmas).
"""

import sys
from collections import Counter
sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
from enum_avoiders import gen_avoiders

CELLS = Counter()
FAIL = []
STATS = Counter()


def kmin_triple(perm, pos):
    n = len(perm)
    best = None
    for d in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * d + 1):
            if pos[x] < pos[x + d] < pos[x + 2 * d]:
                key = (pos[x + 2 * d], d)
                if best is None or key < best[0]:
                    best = (key, x, d)
    return best


def check(perm):
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i
    b = kmin_triple(perm, pos)
    if b is None:
        STATS['no_inc_3ap'] += 1
        return
    STATS['has_inc_3ap'] += 1
    (_, x, d) = b[0][0], b[1], b[2]
    i, j, k = pos[x], pos[x + d], pos[x + 2 * d]

    def region(p):
        if p < i:
            return 0
        if p < j:
            return 1
        if p < k:
            return 2
        return 3

    if x - d >= 1 and x + 3 * d <= n:
        STATS['M1_fired'] += 1
        if not (pos[x - d] > j or pos[x + 3 * d] < j):
            FAIL.append(('M1', perm, x, d))
        CELLS[(region(pos[x - d]), region(pos[x + 3 * d]))] += 1
    if x - 3 * d >= 1 and x + 3 * d <= n:
        STATS['M2_fired'] += 1
        if not (pos[x - 3 * d] > i or pos[x + 3 * d] < i):
            FAIL.append(('M2', perm, x, d))


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for n in range(3, nmax + 1):
        gen_avoiders(n, check)
        print(f"N={n} done; stats={dict(STATS)}; failures={len(FAIL)}", flush=True)
    print()
    print("realization census of (region pos(x-d), region pos(x+3d)) for the "
          "k-minimal triple:")
    names = {0: "<i", 1: "i..j", 2: "j..k", 3: ">k"}
    for (r1, r3), c in sorted(CELLS.items()):
        print(f"  pos(x-d)~{names[r1]:4s}  pos(x+3d)~{names[r3]:4s}: {c}")
    # SAT-window predictions from probe_cases.py ([-1,3] probe):
    sat_cells = {(1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)}
    empty_sat = sat_cells - set(CELLS)
    bad = set(CELLS) - sat_cells
    print(f"cells realized but predicted UNSAT (MUST be empty): {sorted(bad)}")
    print(f"SAT-predicted cells never realized by finite avoiders: "
          f"{sorted(empty_sat)}")
    if FAIL:
        print("FAILURES:", FAIL[:10])
    else:
        print(f"M1, M2 PASS on all 4-AP-free permutations up to N={nmax}.")
