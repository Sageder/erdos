"""deepen.py — incremental deepening of nested scale-invariant delays.

Start from all 1-level annuli satisfying (CONT); repeatedly try to add one more
nested annulus [A_{k+1}, B_{k+1}) strictly inside [A_k, B_k) keeping (CONT).
If the depth is bounded by some T*, then EVERY scale-invariant delay is bounded by
T*, and by Proposition R22-2 the whole scale-invariant family has linear displacement
on every AP — i.e. D1-dead.  If depths are unbounded, a D1-compatible scale-invariant
architecture may exist.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from decide import decide                                             # noqa: E402
from unbounded import nested_tau                                      # noqa: E402


def level1(b, den):
    out = []
    G = [F(n, den) for n in range(den + 1, b * den)]
    for i, A in enumerate(G):
        for B in G[i + 1:]:
            if B >= b:
                continue
            if decide(nested_tau([(A, B)], b), b) is None:
                out.append([(A, B)])
    return out


def extend(bounds, b, den):
    A, B = bounds[-1]
    out = []
    lo = int(A * den) + 1
    hi = int(B * den)
    G = [F(n, den) for n in range(lo, hi + 1)]
    for i, A2 in enumerate(G):
        for B2 in G[i + 1:]:
            if not (A < A2 < B2 < B):
                continue
            nb = bounds + [(A2, B2)]
            if decide(nested_tau(nb, b), b) is None:
                out.append(nb)
    return out


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    den = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    maxdepth = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    cur = level1(b, den)
    print(f"b={b} den={den}: depth 1 survivors: {len(cur)}")
    for d in range(2, maxdepth + 1):
        nxt = []
        for bd in cur:
            nxt += extend(bd, b, den)
            if len(nxt) > 400:
                break
        print(f"   depth {d} survivors: {len(nxt)}")
        for x in nxt[:5]:
            print("        ", [(str(a), str(bb)) for a, bb in x])
        if not nxt:
            print("   -> DEPTH CAPPED at", d - 1, " (on this grid)")
            break
        cur = nxt
