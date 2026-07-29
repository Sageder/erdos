"""pairverify.py -- hard verification of the load-bearing PAIR UNSATs.
Second solver (glucose4 / minisat22) and second ENCODING (CP-SAT integer ranks),
plus the exact bracketing SAT/UNSAT horizon.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
import wsys


def bracket(W, U, Mhi):
    """least horizon M with N(W,U,M) UNSAT, reported as (last SAT, first UNSAT)."""
    lastsat, firstunsat = None, None
    for M in range(U + 1, Mhi + 1):
        S = wsys.Sys((W, U), M)
        v, o = wsys.solve_lazy(S, time_cap=600)
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        if v == 'UNSAT':
            firstunsat = M
            break
        lastsat = M
    return lastsat, firstunsat


if __name__ == '__main__':
    for (W, U, Mhi) in [(10, 28, 90), (11, 31, 100), (9, 26, 90), (12, 34, 110)]:
        t0 = time.time()
        a, b = bracket(W, U, Mhi)
        print(f"# pair {{{W},{U}}}: N SAT at M={a}, N UNSAT at M={b} "
              f"[{time.time()-t0:.0f}s]", flush=True)
        if b is None:
            continue
        S = wsys.Sys((W, U), b)
        for eng in ('cadical195', 'glucose42', 'minisat22'):
            t1 = time.time()
            v, _ = wsys.solve_eager(S, solver=eng)
            print(f"    eager/{eng}: {v} [{time.time()-t1:.0f}s]", flush=True)
        t1 = time.time()
        v, _ = wsys.solve_cpsat(S, tlimit=900)
        print(f"    cpsat(int ranks): {v} [{time.time()-t1:.0f}s]", flush=True)
        # and the SAT side one below, witness verified against apcheck
        S2 = wsys.Sys((W, U), b - 1)
        v2, o2 = wsys.solve_eager(S2)
        if v2 == 'SAT':
            wsys.verify((W, U), b - 1, o2)
            print(f"    control N({W},{U},{b-1}) = SAT, witness verified", flush=True)
        else:
            print(f"    control N({W},{U},{b-1}) = {v2}", flush=True)
