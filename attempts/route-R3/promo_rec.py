"""promo_rec.py — recursive v2-promotion orderings (superlinear displacement, type omega).

Definition (family OMEGA_h, parameterized by h : N -> N, h(0)=0, h strictly increasing
on s>=1 with h(s) > s):
    rho(1) = 1
    for v = 2^s * u (u odd, s = v2(v)), with utilde = (u+1)/2:
        rho(v) = 2^{h(s)} * (2*rho(utilde) - 1)
Position order = sort by rho.  Facts (proved in REPORT.md):
  * rho is injective (image determined by (s, rho(utilde)) and 2rho-1 odd);
  * rho(v) >= v, and for v = 2^s u:  rho(v) >= 2^{h(s)-s} v  -> superlinear displacement
    along high-v2 values (design constraint from CORE.md Thm 12 / route-R1);
  * order type omega since #{v : rho(v) <= K} <= K.
Heuristic: along a 4-AP with v = v2(d) and v2(x) >= v (cases ii/iii of L1), the two
class-v terms sit at rho ~ value while a higher-class term is promoted by >= 2^{h(v+1)-h(v)}
relative factor, which reverses one adjacent pair whenever placements track values within
a factor < 2; the risk is recursive drift (rho(utilde)/utilde unbounded).

Machine check: restrictions to [1..M], M = 10^4 (and failure diagnosis).
"""

import sys
from functools import lru_cache

sys.path.insert(0, "/home/user/erdos/attempts/route-R3")
sys.path.insert(0, "/home/user/erdos/experiments")
from orderings import find_mono4, restriction, diagnose, v2


def make_rho(h):
    @lru_cache(maxsize=None)
    def rho(vv):
        if vv == 1:
            return 1
        s = v2(vv)
        u = vv >> s
        ut = (u + 1) // 2
        return (1 << h(s)) * (2 * rho(ut) - 1)
    return rho


def check(name, h, M=10 ** 4):
    rho = make_rho(h)
    vals = list(range(1, M + 1))
    keys = {v: rho(v) for v in vals}
    assert len(set(keys.values())) == M, "rho not injective on range!"
    perm = sorted(vals, key=lambda v: keys[v])
    wits = find_mono4(perm, cap=100000)
    if not wits:
        print(f"[SURVIVES M={M}] {name}")
    else:
        minM = min(x + 3 * d for (x, d, o) in wits)
        ninc = sum(1 for w in wits if w[2] == 1)
        print(f"[FAILS] {name}: {len(wits)} wits (inc={ninc}, dec={len(wits)-ninc}), "
              f"min max-term={minM}")
        print(diagnose(wits))
    return wits


if __name__ == "__main__":
    import numpy as np
    check("OM.h=2s   rho-promotion", lambda s: 2 * s)
    check("OM.h=3s   rho-promotion", lambda s: 3 * s)
    check("OM.h=s+1  rho-promotion", lambda s: s + 1 if s else 0)
    check("OM.h=s^2  rho-promotion", lambda s: s * s)
    check("OM.h=2^s  rho-promotion", lambda s: (1 << s) - 1 if s else 0)
