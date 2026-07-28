#!/usr/bin/env python3
"""
Fast (meet-in-the-middle) test of the BALANCE equation of the atom-doubling map.

For a finite V with runs [u_j, v_j], an admissible colouring picks in each run a
PREFIX [u_j, c_j] to receive gamma_n = {2n-1,2n} (the rest get beta_n = {2n,2n+1}).
Then A_sigma(V) is legal, |A|=2|V|, cap(A)=|V|, and

    Sigma(A) = Sigma(V) + sum_j ( 1/(2u_j-1) - 1/(2c_j+1) ) - sum_{n in V} 1/(2n(2n+1)).

So for a solution V (Sigma(V)=1), A is a solution iff

    sum_j ( 1/(2u_j-1) - 1/(2c_j+1) )  =  Delta_V := sum_{n in V} 1/(2n(2n+1)).   (BALANCE)

Solving BALANCE would DOUBLE the capacity while adding at most one run per run of V,
so iterating would drive the block count to infinity.  This script decides BALANCE
exactly for every solution in the corpus, by splitting the runs into two halves and
matching exact Fractions through a dictionary.
"""
import sys
from fractions import Fraction as F
from itertools import product


def runs_of(U):
    U = sorted(U); out = []; cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1: cur.append(x)
        else: out.append(cur); cur = [x]
    out.append(cur); return out


def options(run):
    u, v = run[0], run[-1]
    o = [(None, F(0))]
    for c in range(u, v + 1):
        o.append((c, F(1, 2 * u - 1) - F(1, 2 * c + 1)))
    return o


def balance(V):
    R = runs_of(V)
    Delta = sum(F(1, 2 * n * (2 * n + 1)) for n in V)
    opts = [options(r) for r in R]
    h = len(opts) // 2
    left, right = opts[:h], opts[h:]
    tab = {}
    for combo in product(*left):
        tab.setdefault(sum(x[1] for x in combo), combo)
    for combo in product(*right):
        need = Delta - sum(x[1] for x in combo)
        if need in tab:
            return [x[0] for x in tab[need]] + [x[0] for x in combo], Delta
    return None, Delta


def build(V, ends):
    R = runs_of(V); out = set()
    for run, c in zip(R, ends):
        for n in run:
            out |= {2 * n - 1, 2 * n} if (c is not None and n <= c) else {2 * n, 2 * n + 1}
    return sorted(out)


if __name__ == "__main__":
    paths = sys.argv[1:] or ["attempts/route-C/allsols_le105.txt",
                             "experiments/s130.out", "experiments/s150.out"]
    seen = set(); tested = 0; solved = 0
    for p in paths:
        try: lines = open(p).read().splitlines()
        except OSError: continue
        for ln in lines:
            if not ln.startswith("SOL"): continue
            V = tuple(int(x) for x in ln.split()[1:])
            if V in seen: continue
            seen.add(V)
            tested += 1
            sol, Delta = balance(V)
            if sol:
                solved += 1
                W = build(V, sol); S = set(W)
                s = sum(F(1, n) for n in W)
                ok = (s == 1) and all(n - 1 in S or n + 1 in S for n in W) and min(W) >= 2
                L = [len(r) for r in runs_of(W)]
                print(f"*** BALANCE SOLVED  V(max={max(V)}, |V|={len(V)})")
                print(f"    -> W: |W|={len(W)} sum={s} legal={ok} runs={L}")
                print(f"    r={len(L)} cap={sum(l//2 for l in L)}  W={W}")
                sys.stdout.flush()
    print(f"\ntested {tested} distinct solutions; BALANCE solvable for {solved}")
