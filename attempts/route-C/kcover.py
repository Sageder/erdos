#!/usr/bin/env python3
"""
kcover.py N_list -- for each N, find legal solutions with as MANY elements as
possible (binary search on the minelts constraint of dfs2), and report the
k-interval [r, M] each one realises (splitting lemma).  P(k) is true for every k
in the union of these intervals.
"""
import sys, subprocess
sys.path.insert(0, '/home/user/erdos/attempts/route-C')
from prune import prune
from fractions import Fraction

BIN = '/home/user/erdos/attempts/route-C/dfs2'


def search(N, minelts, maxsol=1, tmo=600):
    A = prune(N, True)
    if not A:
        return []
    inp = f"{N} 0 {maxsol} 0 {minelts}\n{len(A)}\n{' '.join(map(str,A))}\n"
    try:
        r = subprocess.run([BIN], input=inp, capture_output=True, text=True, timeout=tmo)
    except subprocess.TimeoutExpired:
        return None
    return [[int(x) for x in l.split()[1:]] for l in r.stdout.split('\n') if l.startswith('SOL')]


def stats(U):
    U = sorted(U)
    assert sum(Fraction(1, n) for n in U) == 1
    S = set(U)
    assert all((n - 1) in S or (n + 1) in S for n in U)
    runs = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur); cur = [x]
    runs.append(cur)
    return len(runs), sum(len(R) // 2 for R in runs), len(U)


if __name__ == "__main__":
    allk = set()
    for N in [int(x) for x in sys.argv[1:]]:
        lo, hi = 0, 80
        best = None
        while lo < hi:
            mid = (lo + hi + 1) // 2
            s = search(N, mid)
            if s:
                lo = mid; best = s[0]
            else:
                hi = mid - 1
        if best is None:
            print(f"N={N}: none"); continue
        r, M, sz = stats(best)
        allk |= set(range(r, M + 1))
        print(f"N={N:4d} max|U|={lo:3d}  witness r={r} M={M} |U|={sz}  k-range=[{r},{M}]")
        print("   U =", best, flush=True)
    print("union of k realised here:", sorted(allk))
