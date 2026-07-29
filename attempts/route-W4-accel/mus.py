"""mus.py -- anatomy of the pair obstruction N(10,28,82).

Splits the constraint set into named families by the BLOCK SIGNATURE of the 4-AP
that produced each clause, then finds which families are needed (family-level
core), then a clause-level MUS inside the surviving families.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys
from pysat.solvers import Solver


def families(S):
    """returns dict name -> list of clauses, plus the forced-relation list."""
    M, Vk = S.M, S.Vk
    fam = {}
    forced = []
    for d in range(1, (M - 1) // 3 + 1):
        for x in range(1, M - 3 * d + 1):
            q = (x, x + d, x + 2 * d, x + 3 * d)
            sig = tuple(S.blk[t] for t in q)
            for seq, orient in ((q, '+'), (q[::-1], '-')):
                c = S.chain(seq)
                if c is None or c == 'DROP':
                    continue
                key = f"{orient}{sig}"
                if not c:
                    forced.append((key, seq))
                else:
                    fam.setdefault(key, []).append(c)
    for d in range(1, Vk // 2 + 1):
        for x in range(max(1, M - 3 * d + 1), Vk - 2 * d + 1):
            if x + 3 * d <= M:
                continue
            c = S.chain((x, x + d, x + 2 * d))
            if c is None or c == 'DROP':
                continue
            fam.setdefault('C2', []).append(c)
    return fam, forced


def solve_with(S, chosen, fam):
    cls = list(S.trans_clauses())
    for k in chosen:
        cls.extend(fam[k])
    with Solver(name='cadical195', bootstrap_with=cls) as s:
        return s.solve()


if __name__ == '__main__':
    W, U, M = 10, 28, 82
    S = wsys.Sys((W, U), M)
    fam, forced = families(S)
    print(f"# N({W},{U},{M}) families (clause counts):")
    for k in sorted(fam, key=lambda z: -len(fam[z])):
        print(f"    {k:22s} {len(fam[k])}")
    print(f"# forced (unit-chain) items: {len(forced)}")

    # family-level minimisation by deletion
    keys = sorted(fam, key=lambda z: -len(fam[z]))
    keep = list(keys)
    for k in keys:
        trial = [z for z in keep if z != k]
        if not solve_with(S, trial, fam):
            keep = trial
    print(f"# family-level UNSAT core: {keep}")
    for k in keep:
        print(f"    {k}: {len(fam[k])} clauses")

    # which values actually occur in the core families
    vals = set()
    id2 = {t: p for p, t in S.vid.items()}
    for k in keep:
        for c in fam[k]:
            for l in c:
                vals.update(id2[abs(l)])
    print(f"# values touched by the core families: min={min(vals)} max={max(vals)} "
          f"count={len(vals)}")
    byblk = {}
    for v in vals:
        byblk.setdefault(S.blk[v], []).append(v)
    for b in sorted(byblk):
        print(f"    block {b}: {len(byblk[b])} values "
              f"[{min(byblk[b])},{max(byblk[b])}]")
