"""Validate supply_window.py results:
   (a) every SAT model decodes to a genuine 4-AP-free permutation satisfying the
       asserted order constraints (the shipped script never checks this);
   (b) every UNSAT is confirmed by a second, independent solver (Glucose42);
   (c) the UNSAT set equals exactly {e, e/2} predicted by Prop R17.3."""
import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from pysat.solvers import Glucose42
from apcheck import has_monotone_kap_pos
from supply_window import Win

bad = 0
for w in (1, 2, 3):
    for e in (2, 3, 4, 6, 8):
        N = w + 5 * e
        W = Win(N)
        base = [[l] for l in W.chain([w, w + e, w + 2 * e])]
        for name, u in (("w+2e", w + 2 * e), ("w+3e", w + 3 * e)):
            sats, unsats = [], []
            for f in range(1, (u - 1) // 2 + 1):
                extra = base + [[l] for l in W.chain([u - 2 * f, u - f, u])]
                r, model = W.solve(extra)
                if r:
                    perm = W.decode(model)
                    pos = {v: i + 1 for i, v in enumerate(perm)}
                    assert sorted(perm) == list(range(1, N + 1)), "not a permutation"
                    assert not has_monotone_kap_pos(perm, 4), ("model has a 4-AP!", perm)
                    assert pos[w] < pos[w + e] < pos[w + 2 * e], "base constraint violated"
                    assert pos[u - 2 * f] < pos[u - f] < pos[u], "open constraint violated"
                    sats.append(f)
                else:
                    S = Glucose42(bootstrap_with=W.cl + extra)
                    assert not S.solve(), ("SOLVER DISAGREEMENT", w, e, name, f)
                    S.delete()
                    unsats.append(f)
            if name == "w+3e":
                pred = sorted({e} | ({e // 2} if e % 2 == 0 else set()))
                pred = [f for f in pred if f >= 1 and u - 2 * f >= 1]
                ok = (unsats == pred)
                bad += (not ok)
                print(f"w={w} e={e} {name}: UNSAT={unsats} predicted(R17.3)={pred} "
                      f"{'MATCH' if ok else '*** MISMATCH ***'}  SAT={sats}", flush=True)
            else:
                bad += (len(unsats) > 0)
                print(f"w={w} e={e} {name}: UNSAT={unsats} (report claims none) SAT={sats}",
                      flush=True)
print("ALL CHECKS PASS" if bad == 0 else f"{bad} MISMATCHES")
