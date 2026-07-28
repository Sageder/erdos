"""census.py — exhaustive forcing-digraph census of finite 4-AP-free boards, plus the
VACUITY CHECK that motivates everything else in route R18.

(A) For N <= 10: over ALL monotone-4-AP-free permutations of [1..N], tabulate
    max forcing height, #open values, and how many boards satisfy
      W  :  "every forcing target is closed"  (== no forcing path with 2 edges
             == max height <= 1),
      Z  :  "no open value at all"            (== max height 0).

(B) VACUITY: the parity permutation sigma_N has NO monotone 3-AP, hence NO open value,
    hence every closure is a singleton and every height is 0, for EVERY N.
    => any finite criterion phrased purely in the forcing digraph is satisfiable at
    every N and can never yield a YES-side theorem. Measured here for N <= 512.
"""

import sys
from itertools import permutations
from collections import Counter

sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from apcheck import has_monotone_kap_pos                      # noqa: E402
from parity_construction import sigma                          # noqa: E402
from forcing_tools import board_stats, closures_and_heights, positions, open_scales  # noqa: E402


def part_A():
    print("=== (A) exhaustive census of 4-AP-free boards ===")
    print(" N  #avoiders  height-distribution           #Z(h=0)  #W(h<=1)  maxCl")
    for N in range(4, 11):
        hd = Counter()
        nZ = nW = 0
        cnt = 0
        maxcl = 0
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            cnt += 1
            st = board_stats(list(p))
            hd[st['max_height']] += 1
            if st['max_height'] == 0:
                nZ += 1
            if st['max_height'] <= 1:
                nW += 1
            maxcl = max(maxcl, st['max_closure'])
        dist = " ".join(f"{h}:{hd[h]}" for h in sorted(hd))
        print(f"{N:2d} {cnt:9d}  {dist:28s}  {nZ:6d}  {nW:7d}  {maxcl:4d}", flush=True)


def part_B():
    print("\n=== (B) VACUITY: parity board sigma_N has an EMPTY forcing digraph ===")
    for N in (10, 20, 40, 80, 160, 320, 512):
        s = sigma(N)
        assert sorted(s) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(s, 3), N          # no monotone 3-AP at all
        st = board_stats(s)
        print(f"  N={N:4d}: monotone-3-AP-free, open values = {st['n_open']}, "
              f"max height = {st['max_height']}, max closure = {st['max_closure']}, "
              f"pos(1)={positions(s)[1]}, max_v pos(v)/v = "
              f"{max(positions(s)[v] / v for v in range(1, N + 1)):.1f}", flush=True)
    print("  => 'all closures singletons' is SAT at every N; forcing-only finite criteria")
    print("     are vacuous. Displacement (Lemma 6 phi-bound) MUST be imposed alongside.")


if __name__ == "__main__":
    part_A()
    part_B()
