"""verify_construction.py — machine verification of Construction A.

Checks (all exact integer arithmetic):
 V1  bijectivity of prefixes: values {1..4^k-1} occur exactly once, k<=8.
     (Restriction principle: since blocks are increasing intervals concatenated
     in order, the values {1..M} in position order coincide with the first M
     positions whenever M = 4^k - 1; for other M they are the order-preserving
     restriction, whose monotone APs are a subset of those of any larger
     restriction — so checking M = 65535 covers every M <= 65535.)
 V2  NO monotone 5-AP (both orientations) in the prefix N = 65535.
 V3  NO monotone DEscending 3-AP in the prefix N = 65535 (stronger claim).
 V4  monotone ascending 3-APs and 4-APs DO exist (as they must, DEGS77(a)).
 V5  enumerate ALL monotone 4-APs for N = 16383 and verify each matches the
     predicted structure:
       - orientation 'inc';
       - block pattern S1: (x | x+d | x+2d,x+3d) with block(x)<block(x+d)=m-1,
         pair in B_m,  or
         block pattern S2: (x | x+d,x+2d | x+3d) with block(x)<m, tail in B_{m+1};
       - the within-block pair (u,u+d) satisfies bit_{v2(d)}(u) = m mod 2.
Writes a summary to verify_output.txt and the 4-AP list to fourAPs_16383.txt.
"""

import sys
import time

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from checkers import find_monotone_kap, enumerate_monotone_kaps
from construction import prefix, block_of


def v2(d):
    l = 0
    while d % 2 == 0:
        d //= 2
        l += 1
    return l


def bit(u, l):
    return (u >> l) & 1


def main():
    lines = []

    def log(s):
        print(s, flush=True)
        lines.append(s)

    t0 = time.time()
    N8 = 4 ** 8 - 1
    p8 = prefix(8)
    assert sorted(p8) == list(range(1, N8 + 1))
    log("V1 OK: prefix N=%d is a permutation of [1..%d] (bijectivity of "
        "restriction prefixes for all M <= %d)" % (N8, N8, N8))

    w5 = find_monotone_kap(p8, 5)
    log("V2: monotone 5-AP search on N=%d: %s   [%.1fs]"
        % (N8, "NONE FOUND" if w5 is None else "FOUND %r" % (w5,),
           time.time() - t0))
    assert w5 is None, w5

    t0 = time.time()
    w3d = find_monotone_kap(p8, 3, orientation="dec")
    log("V3: monotone DESCENDING 3-AP search on N=%d: %s   [%.1fs]"
        % (N8, "NONE FOUND" if w3d is None else "FOUND %r" % (w3d,),
           time.time() - t0))
    assert w3d is None, w3d

    w3i = find_monotone_kap(p8, 3, orientation="inc")
    w4 = find_monotone_kap(p8, 4)
    log("V4: ascending 3-AP exists: %r ; a monotone 4-AP exists: %r"
        % (w3i, w4))
    assert w3i is not None and w4 is not None

    # ---- V5: full 4-AP census on N = 16383 -----------------------------
    t0 = time.time()
    N7 = 4 ** 7 - 1
    p7 = prefix(7)
    aps = enumerate_monotone_kaps(p7, 4)
    log("V5: N=%d: %d monotone 4-APs total   [%.1fs]"
        % (N7, len(aps), time.time() - t0))

    shape_counts = {}
    bad = []
    rows = []
    for (x, d, o) in aps:
        terms = [x, x + d, x + 2 * d, x + 3 * d]
        blocks = [block_of(t) for t in terms]
        if o != "inc":
            bad.append((x, d, o, blocks, "orientation"))
            continue
        b0, b1, b2, b3 = blocks
        l = v2(d)
        if b2 == b3 and b0 < b1 < b2:                       # S1
            shape, m, u = "S1", b2, x + 2 * d
            ok = (b1 == m - 1) and bit(u, l) == m % 2
        elif b1 == b2 and b0 < b1 and b3 == b1 + 1:          # S2
            shape, m, u = "S2", b1, x + d
            ok = bit(u, l) == m % 2
        else:
            shape, ok, m, u = "OTHER", False, -1, -1
        if not ok:
            bad.append((x, d, o, blocks, shape))
        key = (shape, m)
        shape_counts[key] = shape_counts.get(key, 0) + 1
        rows.append((x, d, o, shape, m, tuple(blocks)))

    assert not bad, bad[:10]
    log("V5 OK: every monotone 4-AP is ascending and of shape S1 "
        "(x|x+d|PAIR) or S2 (x|PAIR|x+3d) with the predicted block "
        "adjacency and bit condition bit_{v2(d)}(pair-min) = m mod 2.")
    tot = {}
    for (shape, m), c in sorted(shape_counts.items()):
        log("    shape %s, pair in B_%d: %6d" % (shape, m, c))
        tot[shape] = tot.get(shape, 0) + c
    log("    totals: %s" % tot)

    small = sorted(aps, key=lambda t: (t[0] + 3 * t[1], t[1]))[:12]
    log("    12 smallest 4-APs (x,d,orient): %s" % small)

    with open("/home/user/erdos/attempts/route-R2/fourAPs_16383.txt", "w") as f:
        f.write("# all monotone 4-APs of Construction A prefix N=16383\n")
        f.write("# x d orientation shape m(blockpair) blocks\n")
        for r in sorted(rows):
            f.write("%d %d %s %s %d %s\n" % r)
    log("full 4-AP list written to fourAPs_16383.txt")

    with open("/home/user/erdos/attempts/route-R2/verify_output.txt", "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
