"""e8_zeta.py — (1) test explicit ZETA-realizable slot orders (legal two-sided macros: some
scales go left of the origin, some right, each side omega-ordered outward) against the
pure-cross pattern sets for Z; (2) extract a minimal UNSAT core of patterns for k=3
(basis of the hand-proved impossibility theorem in REPORT.md).

A zeta slot order is given by side eps: N -> {L,R} plus a bijection of each side onto omega
(outward rank).  Slot value: R-scales get +1, +2, ...; L-scales get -1, -2, ... (position
blocks outward).  slot(m) < slot(m') iff the m-block is left of the m'-block.
"""

import sys
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e5_scaleorder import pure_cross_patterns  # noqa: E402
from pysat.solvers import Cadical153  # noqa: E402


def slot_from_sides(eps_func, S):
    """eps_func(m) in {'L','R'}; outward rank = order of appearance among same side by
    increasing m (natural for annulus growth).  Returns dict m -> slot int."""
    slot = {}
    nl = nr = 0
    for m in range(S + 1):
        if eps_func(m) == "R":
            slot[m] = nr
            nr += 1
        else:
            nl += 1
            slot[m] = -nl
    return slot


def test_order(pats, slot):
    bad = []
    for ss, wit in pats.items():
        vals = [slot[s] for s in ss]
        if all(vals[j] < vals[j + 1] for j in range(len(vals) - 1)) or \
           all(vals[j] > vals[j + 1] for j in range(len(vals) - 1)):
            bad.append((ss, wit))
    return bad


def minimal_core(pats, S):
    """Greedy deletion: find a minimal sub-collection of patterns still UNSAT."""
    def is_unsat(patset):
        vid = {}
        ctr = [0]

        def var(a, b):
            x, y = (a, b) if a < b else (b, a)
            if (x, y) not in vid:
                ctr[0] += 1
                vid[(x, y)] = ctr[0]
            lit = vid[(x, y)]
            return lit if (a, b) == (x, y) else -lit
        cnf = []
        for a, b, c in combinations(range(S + 1), 3):
            cnf.append([-var(a, b), -var(b, c), var(a, c)])
            cnf.append([var(a, b), var(b, c), -var(a, c)])
        for ss in patset:
            cnf.append([-var(ss[j], ss[j + 1]) for j in range(len(ss) - 1)])
            cnf.append([var(ss[j], ss[j + 1]) for j in range(len(ss) - 1)])
        with Cadical153(bootstrap_with=cnf) as s:
            return not s.solve()

    core = list(pats.keys())
    assert is_unsat(core), "expected UNSAT overall"
    i = 0
    while i < len(core):
        trial = core[:i] + core[i + 1:]
        if is_unsat(trial):
            core = trial
        else:
            i += 1
    return core


EPS = {
    "alt_R0": lambda m: "R" if m % 2 == 0 else "L",          # R L R L ...
    "alt_L0": lambda m: "L" if m % 2 == 0 else "R",
    "RRLL": lambda m: "R" if m % 4 in (0, 1) else "L",
    "RLLR": lambda m: "R" if m % 4 in (0, 3) else "L",
    "RRLL_s1": lambda m: "R" if (m + 1) % 4 in (0, 1) else "L",
    "RRRLLL": lambda m: "R" if m % 6 in (0, 1, 2) else "L",
    "R0_then_alt": lambda m: "R" if m == 0 or m % 2 == 1 else "L",  # 0R,1R,2L,3R,4L...
}

if __name__ == "__main__":
    for b, S in ((2, 9), (3, 6)):
        for k in (4, 5):
            pats = pure_cross_patterns(k, b, "Z", S)
            print(f"Z base {b} k={k}: {len(pats)} pure-cross patterns (scales <= {S})")
            for name, eps in EPS.items():
                slot = slot_from_sides(eps, S)
                bad = test_order(pats, slot)
                status = "PASSES" if not bad else f"fails {len(bad)} e.g. {bad[:2]}"
                print(f"   zeta order {name:12s}: {status}")
    # minimal UNSAT core for k=3
    for b, S in ((2, 8), (3, 6)):
        pats = pure_cross_patterns(3, b, "Z", S)
        core = minimal_core(pats, S)
        print(f"Z base {b} k=3: minimal UNSAT core ({len(core)} patterns):")
        for ss in core:
            print(f"    {ss}   witness (t,d) = {pats[ss]}")
