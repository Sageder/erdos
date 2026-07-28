"""geometry.py — pure combinatorics (no SAT): the forced-chain dead zone.

If W < U < V are cuts of a permutation a of N, then for every x,d with
      x <= W < x+d <= U < x+2d <= V < x+3d
the quadruple (x, x+d, x+2d, x+3d) is positionally increasing, hence a monotone
increasing 4-AP.  So no monotone-4-AP-free permutation can have all three cuts.
This script decides, for every (W,U,V), whether such (x,d) exists.
"""
import sys


def forced(W, U, V):
    """Is there x,d>=1 with x<=W< x+d<=U< x+2d<=V< x+3d?"""
    for d in range(1, U):
        lo = max(1, W + 1 - d, U - 2 * d + 1, V - 3 * d + 1)
        hi = min(W, U - d, V - 2 * d)
        if lo <= hi:
            return (lo, d)
    return None


if __name__ == "__main__":
    MAXU = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    bad = []
    for U in range(2, MAXU + 1):
        for W in range(1, U):
            for V in range(U + 1, 3 * U - 2):        # the claimed dead zone (U, 3U-3]
                if forced(W, U, V) is None:
                    bad.append((W, U, V))
    print(f"# dead-zone check for all 1<=W<U<=%d, U<V<=3U-3" % MAXU)
    print(f"# uncovered (W,U,V) triples: {len(bad)}")
    if bad:
        print(f"# first 30: {bad[:30]}")
    # and the sharp boundary: V = 3U-2 must NOT be forced (that is the shoulder)
    sh = [(W, U) for U in range(2, MAXU + 1) for W in range(1, U)
          if forced(W, U, 3 * U - 2) is not None]
    print(f"# (W,U) with V=3U-2 ALSO forced (should be none): {len(sh)} {sh[:10]}")
