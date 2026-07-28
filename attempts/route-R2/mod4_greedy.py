"""mod4_greedy.py — Modification idea 4: greedy least-value 4-AP-avoider.

At position n = 1, 2, 3, ... place the SMALLEST unused value v such that no
monotone 4-AP is completed among the already-placed values plus v.  (A value
placed at the current last position can only complete a pattern as its final
element: either as largest term of an ascending 4-AP, or as smallest term of a
descending one.)

Questions: does the greedy sequence stay onto (min-unused value keeps being
placed), i.e. does it look like a permutation of N?  Or do small values get
permanently blocked (evidence for YES-side pressure)?  Run to N steps, track
the deficiency profile, then re-verify the whole prefix with the validated
checker.
"""

import sys
import time

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from checkers import find_monotone_kap


def completes_4ap(v, pos, maxval):
    """Would placing v at the next position complete a monotone 4-AP?"""
    # ascending: v-3e, v-2e, v-e placed at ascending positions
    e = 1
    while v - 3 * e >= 1:
        a = pos.get(v - 3 * e)
        if a is not None:
            b = pos.get(v - 2 * e)
            if b is not None and b > a:
                c = pos.get(v - e)
                if c is not None and c > b:
                    return True
        e += 1
    # descending: v+3e, v+2e, v+e placed at ascending positions (values desc)
    e = 1
    while v + 3 * e <= maxval:
        a = pos.get(v + 3 * e)
        if a is not None:
            b = pos.get(v + 2 * e)
            if b is not None and b > a:
                c = pos.get(v + e)
                if c is not None and c > b:
                    return True
        e += 1
    return False


def greedy(N):
    pos = {}
    seq = []
    maxv = 0
    stats = []
    for n in range(1, N + 1):
        v = 1
        while True:
            if v not in pos and not completes_4ap(v, pos, maxv):
                break
            v += 1
        pos[v] = n
        seq.append(v)
        maxv = max(maxv, v)
        if n % 250 == 0 or n == N:
            unused = [u for u in range(1, maxv + 1) if u not in pos]
            stats.append((n, v, maxv, len(unused),
                          unused[0] if unused else maxv + 1))
    return seq, stats


if __name__ == "__main__":
    outlines = []

    def log(s):
        print(s, flush=True)
        outlines.append(s)

    N = 3000
    t0 = time.time()
    seq, stats = greedy(N)
    log("greedy least-value 4-AP-avoiding sequence, %d steps (%.1fs)"
        % (N, time.time() - t0))
    log("step | value placed | max value so far | #unused<=max | min unused")
    for (n, v, mx, nun, mnu) in stats:
        log("  %5d | %6d | %6d | %5d | %6d" % (n, v, mx, nun, mnu))

    # verify no monotone 4-AP in the built prefix (general checker: the value
    # set need not be [1..N])
    sys.path.insert(0, "/home/user/erdos/experiments")
    from apcheck import has_monotone_kap_general
    t0 = time.time()
    bad = has_monotone_kap_general(seq, 4)
    log("validated general checker on greedy prefix: monotone 4-AP present: %s"
        " (%.0fs)" % (bad, time.time() - t0))
    assert not bad

    with open("/home/user/erdos/attempts/route-R2/mod4_output.txt", "w") as f:
        f.write("\n".join(outlines) + "\n")
