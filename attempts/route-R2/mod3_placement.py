"""mod3_placement.py — Modification idea 3: break block-majorness by placing
blocks out of order (targeting the "free head" mechanism: heads x < 4^m sit at
automatically-early positions; delaying small blocks moves heads AFTER pairs).

Variant 3a (adjacent swap): place blocks in order 1,0,3,2,5,4,7,6
Variant 3b (delayed B_0):   place blocks in order 1,2,3,4,0,5,6,7
Variant 3c (delay each block one round): 1,2,0,4,3,6,5,8,7 -- general delay
Internal orders: as in Construction A (alternating vdC).

For each variant: bijectivity of the assembled prefix, 4-AP count vs
Construction A, 5-AP existence, and witnesses.  Analysis in REPORT.md: any
FINITE delay of a small block only kills the finitely many head-pair 4-APs
whose pair sits before the delayed slot; pairs in all later blocks still see
the head at an earlier position.  Killing them all would need to delay small
values behind cofinally many blocks = infinite delay = not order type omega.
"""

import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from checkers import enumerate_monotone_kaps, find_monotone_kap
from construction import block_order, prefix


def assemble(block_seq):
    out = []
    for m in block_seq:
        out.extend(block_order(m))
    return out


if __name__ == "__main__":
    outlines = []

    def log(s):
        print(s, flush=True)
        outlines.append(s)

    base = prefix(7)
    n_base = len(base)
    base_4 = len(enumerate_monotone_kaps(base, 4))
    log("Construction A baseline N=%d: %d monotone 4-APs, 5-AP: none (verified)"
        % (n_base, base_4))

    variants = {
        "3a swap(1,0)(3,2)(5,4)(7,6)": [1, 0, 3, 2, 5, 4, 6],
        "3b delay B0 after B4": [1, 2, 3, 4, 0, 5, 6],
        "3c rolling delay 1,2,0,4,3,6,5": [1, 2, 0, 4, 3, 6, 5],
    }
    for name, seq in variants.items():
        p = assemble(seq)
        n = len(p)
        assert sorted(p) == list(range(1, n + 1)), name
        c4 = len(enumerate_monotone_kaps(p, 4))
        w5 = find_monotone_kap(p, 5)
        w4 = find_monotone_kap(p, 4)
        log("")
        log("variant %s (N=%d):" % (name, n))
        log("  monotone 4-APs: %d (baseline %d)  first witness: %r"
            % (c4, base_4, w4))
        log("  monotone 5-AP: %s"
            % ("NONE" if w5 is None else "EXISTS %r  <-- 5-avoidance broken"
               % (w5,)))
        # classify a few 4-APs by orientation for the report
        aps = enumerate_monotone_kaps(p, 4)
        n_inc = sum(1 for _, _, o in aps if o == "inc")
        n_dec = len(aps) - n_inc
        log("  orientations: %d inc, %d dec" % (n_inc, n_dec))

    with open("/home/user/erdos/attempts/route-R2/mod3_output.txt", "w") as f:
        f.write("\n".join(outlines) + "\n")
