"""tower_extend.py — the TOWER question behind CORE.md Lemma 6.

196-NO requires a COMPATIBLE tower: avoiders sigma_N of [1..N] with sigma_{N+1}
restricting to sigma_N, and pos_{sigma_N}(v) bounded uniformly in N for each fixed v.
Every individual avoider is easy to find; what matters is extendability.

This script measures, for avoiders produced under a displacement profile:
  (E1) given an avoider of [1..M], can it be EXTENDED to [1..N] (N > M) with the
       relative order of the values [1..M] held fixed?  (SAT over the extension only)
  (E2) how far can a chain of successive extensions be driven from a fixed seed
       (greedy tower building with backtracking at the SAT level)?
  (E3) does holding a profile pos(v) <= C*v on the whole board change (E1)?

A "no" at (E1) for typical avoiders means most finite avoiders are dead ends, i.e. the
extension tree is thin — evidence about how constrained any NO-witness is. A "yes"
that persists is the shape a NO-witness needs.

Order-encoded SAT with the fixed prefix asserted as unit clauses.
"""

import sys, time, random
sys.path.insert(0, '/home/user/erdos/experiments')
from sat_order import build, decode, check_perm
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def extend(prefix_perm, N, C=None, timeout_note=None):
    """prefix_perm: a 4-AP-free permutation of [1..M] (list of values in position order).
    Try to find a 4-AP-free permutation of [1..N] whose restriction to [1..M] equals it.
    Optional profile pos(v) <= C*v on the whole board. Returns perm or None."""
    M = len(prefix_perm)
    assert sorted(prefix_perm) == list(range(1, M + 1))
    cl, pool, var = build(N, inc4=True, dec4=True, dec3=False)
    ppos = {v: i for i, v in enumerate(prefix_perm)}
    for u in range(1, M + 1):
        for w in range(u + 1, M + 1):
            lit = var(u, w)
            cl.append([lit] if ppos[u] < ppos[w] else [-lit])
    if C is not None:
        for v in range(1, N + 1):
            bound = int(C * v)
            if bound >= N:
                continue
            lits = []
            for w in range(1, N + 1):
                if w == v:
                    continue
                lits.append(var(min(v, w), max(v, w)) * (1 if w < v else -1))
            enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool, encoding=EncType.seqcounter)
            cl.extend(enc.clauses)
    S = Cadical195(bootstrap_with=cl)
    sat = S.solve()
    perm = decode(S.get_model(), N, var) if sat else None
    S.delete()
    if perm is not None:
        assert not has_monotone_kap_pos(perm, 4)
        # verify the restriction really equals the prefix
        rest = [v for v in perm if v <= M]
        assert rest == list(prefix_perm), "restriction mismatch!"
    return perm


def random_avoider(M, seed=0):
    from sat_order import solve
    sat, perm = solve(M, inc4=True, dec4=True)
    assert sat
    return perm


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "e1"
    if mode == "e1":
        # E1: extendability of a SAT-found avoider, M -> N
        for M, N in [(20, 30), (30, 45), (40, 60), (60, 90), (80, 120)]:
            seed_perm = random_avoider(M)
            t0 = time.time()
            out = extend(seed_perm, N)
            dt = time.time() - t0
            print(f"E1 M={M} -> N={N}: {'EXTENDS' if out else 'DEAD END'} ({dt:.0f}s)", flush=True)
    elif mode == "tower":
        # E2: build a tower by successive extension from a small seed
        C = float(sys.argv[2]) if len(sys.argv) > 2 else None
        cur = random_avoider(12)
        M = 12
        while M < 400:
            N = M + max(4, M // 4)
            t0 = time.time()
            out = extend(cur, N, C=C)
            dt = time.time() - t0
            if out is None:
                print(f"TOWER STOPPED: {M} -> {N} has no extension ({dt:.0f}s)", flush=True)
                break
            print(f"tower {M} -> {N}: ok ({dt:.0f}s)", flush=True)
            cur, M = out, N
        else:
            print(f"TOWER reached M={M}", flush=True)
