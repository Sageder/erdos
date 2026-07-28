#!/usr/bin/env python3
"""
BALANCE, retried on LARGE solutions with a branch-and-bound DFS (the earlier
meet-in-the-middle version only reached ~18 runs; these have ~40).

For a solution V with runs [u_j,v_j], an admissible colouring assigns each run a
PREFIX [u_j,c_j] of gammas (atoms {2n-1,2n}); the rest get betas ({2n,2n+1}).
The image A_sigma(V) is legal with |A| = 2|V|, cap(A) = |V|, and

    r(A) = r(V) + #{runs whose prefix is PROPER (neither empty nor full)},
    Sigma(A) = 1 + sum_j ( 1/(2u_j-1) - 1/(2c_j+1) ) - Delta_V,
    Delta_V = sum_{n in V} 1/(2n(2n+1)).

So A is a solution iff  sum_j ( ... ) = Delta_V   (BALANCE).

Why this matters: BALANCE would DOUBLE the capacity (cap goes from cap(V) to |V|)
while adding only one run per PROPER prefix.  Iterating with a bounded number of
proper prefixes gives capacity ~ 2^t and run count ~ linear, hence P(k) for all
large k.  We therefore also minimise the number of proper prefixes.
"""
import sys
from fractions import Fraction as F


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def solve(V, maxproper=None):
    R = runs_of(V)
    Delta = sum(F(1, 2 * n * (2 * n + 1)) for n in V)
    opts = []
    for run in R:
        u, v = run[0], run[-1]
        o = [(None, F(0), 0)]                                   # empty prefix
        for c in range(u, v + 1):
            proper = 0 if c == v else 1
            o.append((c, F(1, 2 * u - 1) - F(1, 2 * c + 1), proper))
        o.sort(key=lambda x: x[1])
        opts.append(o)
    # order runs by decreasing max contribution -> strong pruning
    order = sorted(range(len(opts)), key=lambda i: -opts[i][-1][1])
    opts = [opts[i] for i in order]
    suffmax = [F(0)] * (len(opts) + 1)
    for i in range(len(opts) - 1, -1, -1):
        suffmax[i] = suffmax[i + 1] + opts[i][-1][1]
    best = None

    def dfs(i, rem, prop, chosen):
        nonlocal best
        if rem < 0 or rem > suffmax[i]:
            return
        if maxproper is not None and prop > maxproper:
            return
        if i == len(opts):
            if rem == 0:
                best = (list(chosen), prop, order)
                return True
            return
        for (c, val, pr) in opts[i]:
            if val > rem: break
            chosen.append((c, pr))
            if dfs(i + 1, rem - val, prop + pr, chosen):
                return True
            chosen.pop()
        return False

    dfs(0, Delta, 0, [])
    return best, Delta, R, order


def build(V, R, order, chosen):
    ends = [None] * len(R)
    for pos, i in enumerate(order):
        ends[i] = chosen[pos][0]
    out = set()
    for run, c in zip(R, ends):
        for n in run:
            out |= {2 * n - 1, 2 * n} if (c is not None and n <= c) else {2 * n, 2 * n + 1}
    return sorted(out)


if __name__ == "__main__":
    import glob
    paths = sys.argv[1:] or (glob.glob('attempts/route-B/pool/*.txt') +
                             glob.glob('attempts/route-B/*.txt'))
    seen = set(); tested = 0
    cands = []
    for p in paths:
        try: lines = open(p).read().splitlines()
        except OSError: continue
        for ln in lines:
            if not ln.startswith("SOL"): continue
            V = tuple(int(x) for x in ln.split()[1:])
            if V in seen: continue
            seen.add(V)
            if sum(F(1, n) for n in V) != 1: continue
            cands.append(V)
    cands.sort(key=lambda V: -len(V))          # biggest first: most entropy
    print(f"{len(cands)} distinct solutions; testing the largest first")
    for V in cands[:400]:
        tested += 1
        best, Delta, R, order = solve(V)
        if best:
            chosen, prop, order = best
            W = build(V, R, order, chosen)
            s = sum(F(1, n) for n in W); S = set(W)
            ok = s == 1 and all(n - 1 in S or n + 1 in S for n in W) and min(W) >= 2
            L = [len(r) for r in runs_of(W)]
            print(f"*** BALANCE SOLVED: |V|={len(V)} runs={len(R)} proper={prop}")
            print(f"    -> |W|={len(W)} sum={s} legal={ok} r={len(L)} cap={sum(x//2 for x in L)} "
                  f"min={min(W)} max={max(W)}")
            print(f"    W={W}")
            sys.exit(0)
    print(f"tested {tested} solutions (largest first): BALANCE not solvable for any")
