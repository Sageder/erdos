"""cosupply_sat.py — R17.  Are the SPINE co-supply statements finitely refutable?

All statements below concern a single target value g and mention only values <= g,
so the window [1..g] is faithful:  UNSAT  ==>  theorem for every 4-AP-free
permutation of N (modulo solver);  SAT ==> no obstruction from values <= g.

  (T-ground)  g GROUNDED and a U1-sink  <=>  pos(g-d) < pos(g-2d) for all d<= (g-1)/2.
              [grounded: every v<g precedes g, so "no increasing 3-AP ends at g"
               is exactly the displayed condition]
  (T-D2)      g has no D2 out-edge:  for all d <= (g-1)/3, NOT(g-d prec g-2d prec g-3d).
              [this is the ONLY out-rule available at a value-RECORD, since U1,U2,D1
               all require a larger value to precede g]
  (T-recsink) record & full G*-sink (inside the window) = (T-D2)   [same thing]
  (T-gsink)   g grounded and a full G*-sink inside the window = (T-ground) AND (T-D2).
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from pysat.solvers import Cadical195, Glucose42
from apcheck import has_monotone_kap_pos
from supply_window import Win


def build_conditions(W, g, kind):
    cl = []
    if kind in ("ground", "gsink"):
        for d in range(1, (g - 1) // 2 + 1):
            cl.append([W.lit(g - d, g - 2 * d)])          # g-d prec g-2d
    if kind in ("D2", "gsink"):
        for d in range(1, (g - 1) // 3 + 1):
            l1 = W.lit(g - d, g - 2 * d)
            l2 = W.lit(g - 2 * d, g - 3 * d)
            cl.append([-l1, -l2])                          # not (g-d prec g-2d prec g-3d)
    if kind in ("ground", "gsink"):
        for v in range(1, g):
            cl.append([W.lit(v, g)])                       # g is grounded
    return cl


def test(g, kind, second=False):
    W = Win(g)
    extra = build_conditions(W, g, kind)
    r, model = W.solve(extra)
    if r:
        perm = W.decode(model)
        assert not has_monotone_kap_pos(perm, 4), "decoded board is not 4-AP-free!"
        return True, perm
    if second:
        S = Glucose42(bootstrap_with=W.cl + extra)
        assert not S.solve(), "solver disagreement!"
        S.delete()
    return False, None


if __name__ == "__main__":
    kinds = sys.argv[1:] or ["ground", "D2", "gsink"]
    for kind in kinds:
        print(f"=== {kind} ===", flush=True)
        last_sat = None
        for g in range(6, 61):
            t0 = time.time()
            r, perm = test(g, kind, second=True)
            dt = time.time() - t0
            if r:
                last_sat = (g, perm)
                if g % 5 == 0 or g < 12:
                    print(f"  g={g}: SAT ({dt:.1f}s)", flush=True)
            else:
                print(f"  g={g}: UNSAT ({dt:.1f}s)  <-- THEOREM (verified 2 solvers)", flush=True)
                break
        else:
            print(f"  SAT up to g=60; last witness g={last_sat[0]}: {last_sat[1]}", flush=True)
