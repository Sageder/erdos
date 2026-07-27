"""probe_cases.py — finer probes of the k-minimal window beyond the backbone.

P(c) denotes the position of value x+c*d in a 4-AP-free permutation whose k-minimal
increasing 3-AP is (x, x+d, x+2d) (grid window, valid for every d).  The backbone
computation (solver_minimal.py) shows the only forced pairwise relations are
P(3)<P(2) and (with x>d) P(0)<P(-1).  Here:

 P1: which JOINT placements of P(3) and P(4) among the base intervals are consistent?
     (a combination could be excluded even when no single pair is forced)
 P2: same for (P(3), P(5)) and for (P(-1), P(3)) on the window with negatives.
 P3: sanity — dropping kmin must strictly enlarge the model count on a small window
     (checks the kmin clauses actually bite).
"""

from solver_minimal import OrderSAT
from game_anchor import sat_count


def region_probe(offsets, base, targets, kmin=True, note=""):
    """For each target offset t, and each way of interleaving with base positions,
    check consistency of joint cases for all targets simultaneously (cartesian)."""
    import itertools
    a, b, c = base
    # regions relative to the base triple: 0: before P(a), 1: (P(a),P(b)),
    # 2: (P(b),P(c)), 3: after P(c)
    def region_constraints(S, t, r):
        v = S.var
        if r == 0:
            return [[v(t, a)]]
        if r == 1:
            return [[v(a, t)], [v(t, b)]]
        if r == 2:
            return [[v(b, t)], [v(t, c)]]
        return [[v(c, t)]]

    print(f"-- joint region probe {targets} on {offsets[0]}..{offsets[-1]} {note}")
    results = {}
    for regs in itertools.product(range(4), repeat=len(targets)):
        S = OrderSAT(offsets)
        S.add_blocked4()
        S.add_base(base)
        if kmin:
            S.add_kmin(base[2])
        for t, r in zip(targets, regs):
            for cl in region_constraints(S, t, r):
                S.clauses.append(cl)
        results[regs] = S.solve()
    names = {0: "<Pa", 1: "a..b", 2: "b..c", 3: ">Pc"}
    for regs, sat in sorted(results.items()):
        tag = ", ".join(f"P({t})~{names[r]}" for t, r in zip(targets, regs))
        print(f"    {tag}: {'SAT' if sat else 'UNSAT'}")
    return results


if __name__ == "__main__":
    offs = list(range(0, 10))
    r = region_probe(offs, (0, 1, 2), [3, 4])
    r2 = region_probe(offs, (0, 1, 2), [3, 5])
    offs_neg = list(range(-4, 10))
    r3 = region_probe(offs_neg, (0, 1, 2), [-1, 3], note="[assumes x>4d]")

    # P3: kmin must bite
    small = list(range(0, 7))
    with_k = sat_count(small, [(0, 1, 2)], kmin_top=2)
    no_k = sat_count(small, [(0, 1, 2)], kmin_top=None)
    print(f"P3: model counts on [0..6]: with kmin={with_k}, without={no_k} "
          f"(must be strictly smaller with kmin)")
    assert with_k < no_k
