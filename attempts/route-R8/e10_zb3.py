"""e10_zb3.py (generated from e4_zjoint.py) — JOINT SAT over all blocks up to M for the Z alternating-scale macro.

Same conventions as e4_zsat.py: blocks D_0' = {-1,0,1}, D_m = {v: 2^m <= |v| < 2^(m+1)};
slots: D_0' at 0, D_2, D_4, ... rightward, D_1, D_3, ... leftward.  All within-block pair
orders are free variables simultaneously; clauses over every k-AP inside the universe
[-(2^(M+1)-1), 2^(M+1)-1].  SAT => extract tau's, verify assembled window independently.
UNSAT / macro-refuted => report (theorem for this macro at that M).

Optional: 'sym' mode adds central symmetry constraint tau(-v) mirrors tau(v) to guide
structure hunting (halves the search space; may cost satisfiability).
"""

import sys
import os
import functools
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import has_kap_vals_np  # noqa: E402
from zcheck import find_monotone_kaps, covered_centered_interval  # noqa: E402

from pysat.solvers import Cadical153  # noqa: E402


BASE = 3


def block_index(v):
    a = abs(v)
    if a < BASE:
        return 0
    m = 0
    x = 1
    while a >= x * BASE:
        x *= BASE
        m += 1
    return m


def slot_of_block(m):
    return (m // 2) if m % 2 == 0 else -((m + 1) // 2)


def block_values(m):
    if m == 0:
        return list(range(-(BASE - 1), BASE))
    lo, hi = BASE ** m, BASE ** (m + 1)
    return list(range(-hi + 1, -lo + 1)) + list(range(lo, hi))


def solve_joint(M, k=5, verbose=True, mirror_sym=False):
    Vmax = BASE ** (M + 1) - 1
    vid = {}
    ctr = [0]

    def var(u, v):
        a, b = (u, v) if u < v else (v, u)
        if (a, b) not in vid:
            ctr[0] += 1
            vid[(a, b)] = ctr[0]
        lit = vid[(a, b)]
        return lit if (u, v) == (a, b) else -lit

    solver = Cadical153()
    nclauses = 0
    for m in range(M + 1):
        vals = block_values(m)
        for a, b, c in combinations(vals, 3):
            solver.add_clause([-var(a, b), -var(b, c), var(a, c)])
            solver.add_clause([var(a, b), var(b, c), -var(a, c)])
            nclauses += 2
    refuted = []
    for d in range(1, (2 * Vmax) // (k - 1) + 1):
        for t in range(-Vmax, Vmax - (k - 1) * d + 1):
            terms = [t + j * d for j in range(k)]
            inc_clause, dec_clause = [], []
            inc_ok = dec_ok = True
            for j in range(k - 1):
                u, v = terms[j], terms[j + 1]
                mu, mv = block_index(u), block_index(v)
                if mu == mv:
                    inc_clause.append(-var(u, v))
                    dec_clause.append(var(u, v))
                else:
                    if slot_of_block(mu) < slot_of_block(mv):
                        dec_ok = False
                    else:
                        inc_ok = False
            if inc_ok:
                if inc_clause:
                    solver.add_clause(inc_clause)
                    nclauses += 1
                else:
                    refuted.append((t, d, "inc"))
            if dec_ok:
                if dec_clause:
                    solver.add_clause(dec_clause)
                    nclauses += 1
                else:
                    refuted.append((t, d, "dec"))
    if refuted:
        print(f"  M={M} k={k}: MACRO REFUTED, APs with all-constant monotone comparisons: "
              f"{refuted[:8]}{' ...' if len(refuted) > 8 else ''}  "
              f"(total {len(refuted)})")
        solver.delete()
        return None
    if mirror_sym:
        for (a, b), lit in list(vid.items()):
            # symmetry v -> -v maps pair (a,b) to (-b,-a); tie orientations:
            # pos(a)<pos(b)  <=>  pos(-a)>pos(-b)... choose: central antisymmetry
            l2 = var(-b, -a)
            solver.add_clause([-lit, -l2])
            solver.add_clause([lit, l2])
            nclauses += 2
    ok = solver.solve()
    if not ok:
        print(f"  M={M} k={k}{' sym' if mirror_sym else ''}: UNSAT  ({nclauses} clauses)")
        solver.delete()
        return None
    model = set(l for l in solver.get_model() if l > 0)
    solver.delete()

    def cmp(u, v):
        if u == v:
            return 0
        a, b = (u, v) if u < v else (v, u)
        before = ((a, b) not in vid) or (vid[(a, b)] in model)
        if (u, v) == (a, b):
            return -1 if before else 1
        return 1 if before else -1

    taus = {}
    for m in range(M + 1):
        taus[m] = sorted(block_values(m), key=functools.cmp_to_key(cmp))
    slots = sorted((slot_of_block(m), m) for m in taus)
    seq = []
    for s_, m in slots:
        seq.extend(taus[m])
    bad = has_kap_vals_np(seq, k)
    cov = covered_centered_interval(seq)
    print(f"  M={M} k={k}{' sym' if mirror_sym else ''}: SAT ({nclauses} clauses); window "
          f"|{len(seq)}| covers [-{cov},{cov}]; independent check monotone {k}-AP present: "
          f"{bad}")
    assert not bad, "SAT solution failed independent verification!"
    if verbose:
        for m in range(min(M, 5) + 1):
            print(f"    tau_{m}: {taus[m]}")
    return taus


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--Mmax", type=int, default=6)
    ap.add_argument("--sym", action="store_true")
    args = ap.parse_args()
    for M in range(2, args.Mmax + 1):
        solve_joint(M, k=args.k, mirror_sym=args.sym)
