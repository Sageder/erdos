"""sparse_anchors.py — can the ADVERSARY keep the two-point anchors arbitrarily far apart?

Route R13's two-point laws (TP1..TP8) all have anchors drawn from the record set Lambda
or the grounded set Gamma.  Both are infinite (CORE Lemma 11), so the Prover can always
demand another anchor -- but the ADVERSARY chooses its value.  If the record set can be
made geometrically sparse, then every two-point law fires only at scales the adversary
picked, and route R5's Generic Escape re-runs with "fresh anchor" in place of
"fresh step".

Test: pin the first k positions to hold prescribed values 1 = W_0 < W_1 < ... < W_{k-1}
(so those are exactly the first k value-records, with prescribed gaps), and ask whether a
monotone-4-AP-free permutation of [1..N] still exists.

SAT  => the adversary can space the anchors that way (barrier evidence).
UNSAT=> record gaps are constrained -- which would be a genuine crack.
"""

import sys
import time

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R13-twopoint")
from apcheck import has_monotone_kap_pos            # noqa: E402
from sat_order import build, decode                 # noqa: E402
from sat_normalforms import pins_clauses            # noqa: E402
from pysat.solvers import Cadical195, Glucose42     # noqa: E402


def run(N, prefix, solver="cadical"):
    cl, pool, var = build(N, inc4=True, dec4=True)
    cl = cl + pins_clauses(N, var, first_pins=prefix, last_pins=())
    S = Cadical195(bootstrap_with=cl) if solver == "cadical" else Glucose42(bootstrap_with=cl)
    t0 = time.time()
    sat = S.solve()
    dt = time.time() - t0
    perm = decode(S.get_model(), N, var) if sat else None
    S.delete()
    return sat, perm, dt


CASES = [
    # (N, prefix)  -- prefix = values at positions 1,2,3,... (hence the first records)
    (100, [1, 2]),
    (100, [1, 10]),
    (100, [1, 50]),
    (100, [1, 100]),
    (100, [1, 3, 9, 27, 81]),
    (100, [1, 4, 16, 64]),
    (100, [1, 5, 25]),
    (128, [1, 2, 4, 8, 16, 32, 64, 128]),
    (128, [1, 3, 9, 27, 81]),
    (160, [1, 4, 16, 64]),
    (160, [1, 6, 36]),
    (160, [1, 7, 49]),
]

if __name__ == "__main__":
    for N, prefix in CASES:
        sat, perm, dt = run(N, prefix)
        if sat:
            assert not has_monotone_kap_pos(perm, 4)
            assert list(perm[:len(prefix)]) == list(prefix), (perm[:8], prefix)
            print(f"N={N:4d} record-prefix {prefix}: SAT   ({dt:6.1f}s)  next={perm[len(prefix):len(prefix)+5]}",
                  flush=True)
        else:
            sat2, _, dt2 = run(N, prefix, solver="glucose")
            print(f"N={N:4d} record-prefix {prefix}: UNSAT ({dt:6.1f}s) [cadical]; "
                  f"glucose sat={sat2} ({dt2:.1f}s)  <== CRACK", flush=True)
