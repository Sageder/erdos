"""level_blocks_scan.py — cost per base-3 LEVEL inside a fixed order-type-omega
architecture (contiguous base-3 blocks, free internal orders).

tau protects EVERY level v = v3(d) at once, using only the level-v digits, and pays with
infinite predecessor sets.  Here we measure how many levels a genuine omega-architecture
can protect: extinction board size N*(L) for the constraint "no monotone 4-AP with
v3(d) in L", with blocks D_j = [3^j,3^{j+1}) contiguous and increasing (pos(v) <= 3v-1).

Encoding cross-validated: with L = all levels this reproduces R3's Theorem B coupled
threshold exactly (SAT N=86, UNSAT N=87).
"""

import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from level0_blocks import run
from taulib import v3

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--hi", type=int, default=130)
    ap.add_argument("--levels", type=str, default="0|01|012|all")
    a = ap.parse_args()
    for tok in a.levels.split("|"):
        if tok == "all":
            f, nm = (lambda d: True), "all"
        else:
            S = set(int(c) for c in tok)
            f, nm = (lambda d, S=S: v3(d) in S), tok
        N, last = 10, None
        while N <= a.hi:
            sat, _ = run(N, True, f, f"levels={nm}")
            if not sat:
                print(f"  ==> levels={nm}: SAT through {last}, EXTINCT at N={N}", flush=True)
                break
            last = N
            N += 1
        else:
            print(f"  ==> levels={nm}: SAT through N={a.hi}", flush=True)
