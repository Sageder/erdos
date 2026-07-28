"""Route R5 mining 3: algebraic hits in S_k.

Claims examined:
 A1. For c in [-30, 30]: how many members n have n+c a perfect square?
     Expectation for a structureless set S of the same size: for each square
     x^2 <= X+c, P(x^2-c in S) ~ local density; approximated as
     sum over squares of (local density of S near x^2).  Enrichment >> 1 at a
     specific c indicates a quadratic family x^2-c inside S_k.
 A2. Same for n+c = 2 y^2, n+c = 3 y^2, n+c = y^3, n+c = y^4.
 A3. n+k a perfect power (square/cube/higher).
All hit lists for strongly enriched forms are printed exactly (first 20).
"""

import sys
import numpy as np

DATA = "/home/user/erdos/attempts/route-R5/data"


def load(k, tags):
    parts = []
    for t in tags:
        try:
            parts.append(np.loadtxt(f"{DATA}/S{k}_{t}.txt", dtype=np.int64).reshape(-1))
        except OSError:
            pass
    return np.unique(np.concatenate(parts)) if parts else np.zeros(0, np.int64)


def isqrt_vec(x):
    r = np.sqrt(x.astype(np.float64)).astype(np.int64)
    r -= (r * r > x)
    r += ((r + 1) * (r + 1) <= x)
    return r


def expect_form(arr, X, m):
    """Expected #members that are of form (m*y^2 - c) for structureless S:
    number of m*y^2 values up to X  times  average density |S|/X."""
    return (np.sqrt(X / m)) * len(arr) / X


def main():
    tags = sys.argv[1:] or ["run1"]
    for k in [2, 3, 4, 5, 6]:
        arr = load(k, tags)
        if len(arr) < 20:
            if len(arr):
                print(f"\n== k={k}: only {len(arr)} members: {arr.tolist()} ==")
            continue
        X = int(arr[-1])
        print(f"\n== k={k}: {len(arr)} members up to {X} ==")
        # A1/A2: n + c = m*y^2
        for m, mlabel in [(1, "y^2"), (2, "2y^2"), (3, "3y^2")]:
            exp = expect_form(arr, X, m)
            rows = []
            for c in range(-30, 31):
                v = arr + c
                v = v[v > 0]
                if m == 1:
                    r = isqrt_vec(v)
                    hits = v[r * r == v]
                else:
                    w = v[v % m == 0] // m
                    r = isqrt_vec(w)
                    hits = m * w[r * r == w] # back to n+c
                nh = len(hits)
                if nh > 3 * exp + 3 or (nh >= 5 and nh > 2 * exp):
                    rows.append((c, nh, hits[:12] - c))
            print(f" [{mlabel}] expected hits/c ~ {exp:.1f}; enriched c values:")
            for c, nh, ex in rows:
                print(f"    n = {mlabel}-({c}): {nh} hits (exp {exp:.1f}), "
                      f"first: {ex.tolist()}")
            if not rows:
                print("    none enriched")
        # A2 cubes/fourth powers
        for e, elabel in [(3, "y^3"), (4, "y^4")]:
            expc = (X ** (1 / e)) * len(arr) / X
            rows = []
            for c in range(-30, 31):
                v = arr + c
                v = v[v > 0]
                r = np.round(v.astype(np.float64) ** (1 / e)).astype(np.int64)
                hits = v[(r ** e == v)]
                nh = len(hits)
                if nh >= 2 and nh > 3 * expc:
                    rows.append((c, nh, hits[:10] - c))
            print(f" [{elabel}] expected hits/c ~ {expc:.2f}; enriched:")
            for c, nh, ex in rows:
                print(f"    n = {elabel}-({c}): {nh} hits, first: {ex.tolist()}")
            if not rows:
                print("    none enriched")
        # A3: n+k perfect square
        v = arr + k
        r = isqrt_vec(v)
        sq = arr[r * r == v]
        print(f" [n+k square]: {len(sq)} hits (exp {np.sqrt(X)*len(arr)/X:.1f}); "
              f"first 15: {sq[:15].tolist()}")
        v2 = v[v % 2 == 0] // 2
        r = isqrt_vec(v2)
        tsq = 2 * v2[r * r == v2]
        print(f" [n+k = 2y^2]: {len(tsq)} hits (exp {np.sqrt(X/2)*len(arr)/X:.1f}); "
              f"first 15: {(tsq - k)[:15].tolist()}")


if __name__ == "__main__":
    main()
