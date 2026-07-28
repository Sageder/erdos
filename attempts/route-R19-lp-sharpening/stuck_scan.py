"""stuck_scan.py -- how close is the mixed forcing closure to saturating |Cl_pm(u)| <= pos(u)?

A value u is STUCK if it is neither open at any scale (I-rule) nor co-open at any scale
(D-rule): then the mixed forcing chain dies at u.  Values 1 and 2 are always stuck.
Measured on SAT-found plain avoiders (order encoding, experiments/sat_order.py):
  * fraction of stuck values,
  * max_u |Cl_pm(u)| / pos(u)  (must be <= 1; how close to 1?),
  * the same for the increasing-only closure of CORE Theorem 16.
A ratio approaching 1 means the two-orientation closure bound is nearly binding and is
the natural place to look for a finite contradiction.
"""

import sys
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from apcheck import has_monotone_kap_pos
from r19lib import pos_array
from mixed_closure import open_scales, coopen_scales, mixed_closure
from sat_order import solve

if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [40, 60, 80, 100, 130, 160, 200]
    print("N   stuck   open-only  coopen-only  both    max|Cl_pm|/pos   max|Cl_inc|/pos")
    for N in Ns:
        sat, perm = solve(N, inc4=True, dec4=True)
        assert sat and not has_monotone_kap_pos(perm, 4)
        pos = pos_array(perm)
        stuck = io = do = bo = 0
        rpm = ri = 0.0
        for u in range(1, N + 1):
            o = bool(open_scales(pos, u, N))
            c = bool(coopen_scales(pos, u, N))
            if o and c:
                bo += 1
            elif o:
                io += 1
            elif c:
                do += 1
            else:
                stuck += 1
            rpm = max(rpm, len(mixed_closure(pos, u, N, True, True)) / pos[u])
            ri = max(ri, len(mixed_closure(pos, u, N, True, False)) / pos[u])
        print(f"{N:4d} {stuck:5d} ({100*stuck/N:4.1f}%) {io:6d} {do:8d} {bo:7d}"
              f"      {rpm:.3f}          {ri:.3f}", flush=True)
