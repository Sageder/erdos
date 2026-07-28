"""local_search.py -- heuristic witnesses minimising sum_j tau_j among increasing-4-AP-free
permutations, to certify small values of C_ledger(N) at N where CP-SAT is too slow.

Every improvement is re-verified exactly (r19lib.has_inc_4ap, cross-validated against
experiments/apcheck.py), so the resulting bound C_ledger(N) <= N(N+1)/(2(N^2+N-sum tau))
is CERTIFIED by an explicit permutation regardless of how it was found.
"""

import sys, random, json, os
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from r19lib import has_inc_4ap, taus, triadic
from min_tau import C_ledger


def obj(perm):
    return sum(taus(perm)[1:])


def improve(perm, iters, rng):
    N = len(perm)
    best = obj(perm)
    cur = list(perm)
    for it in range(iters):
        i = rng.randrange(N)
        j = rng.randrange(N)
        if i == j:
            continue
        cand = list(cur)
        if rng.random() < 0.5:
            cand[i], cand[j] = cand[j], cand[i]
        else:                                   # move
            v = cand.pop(i)
            cand.insert(j, v)
        o = obj(cand)
        if o < best and not has_inc_4ap(cand):
            cur, best = cand, o
    return cur, best


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [40, 48, 56, 64, 80, 96, 112, 128, 160]
    iters = int(os.environ.get("ITERS", "60000"))
    rng = random.Random(196196)
    out = open("/home/user/erdos/attempts/route-R19-lp-sharpening/witnesses.txt", "a")
    worst = 0.0
    for N in Ns:
        base = triadic(N)
        assert not has_inc_4ap(base)
        bestperm, best = base, obj(base)
        for restart in range(3):
            start = list(bestperm) if restart else base
            p, o = improve(start, iters, rng)
            if o < best:
                bestperm, best = p, o
        assert sorted(bestperm) == list(range(1, N + 1))
        assert not has_inc_4ap(bestperm), "witness has an increasing 4-AP"
        assert obj(bestperm) == best
        cb = C_ledger(N, best)
        worst = max(worst, float(cb))
        print(f"N={N:4d}: sum tau <= {best:8d}  gamma <= {best/N**2:.5f}   "
              f"C_ledger(N) <= {float(cb):.5f} = {cb}   (triadic gave {obj(base)})",
              flush=True)
        out.write(json.dumps({"N": N, "sum_tau": best, "perm": bestperm}) + "\n")
        out.flush()
    print(f"\nMAX over scanned N: C_ledger(N) <= {worst:.5f}")
