"""reslimit.py -- route R22: the RESOLUTION LIMIT of the head-delay counterexample.

For HEAD(b, s_m = m+1, K_m = m), the AP P = {r+qn} first meets a head H_m only when
s_m = m+1 >= q, i.e. m >= q-1, i.e. only at values v >= b^{q-1}.  So on a board of size
M = b^{J+1} the failure of tameness is VISIBLE only for q <= J+1: for every larger q there
is a residue r whose AP looks perfectly tame (t == 0, no descents, coarse displacement 1)
all the way to M.  This is precisely why Conjecture R21-C could not be refuted by a finite
search, and why the standing sanity check (Remark 31(b)) gives no leverage here: the
counterexample is essentially infinite.
"""
import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from arch import delay_head, check_ii_fast
from headdelay import ap_descents, ap_t_profile, coarse_disp

b = 3
print(f"{'M':>8s} " + "".join(f"{'q<=%d' % q:>9s}" for q in (4, 6, 8, 9, 10, 12, 20)))
print("        " + "  (min over all APs of that q-range of: #descents / max t / coarse-disp)")
for J in (5, 6, 7, 8):
    M = b ** (J + 1)
    t, c = delay_head(M, b, lambda m: m + 1, lambda m: m)
    assert check_ii_fast(c, M) is None
    row = f"{M:8d} "
    for Q in (4, 6, 8, 9, 10, 12, 20):
        de = mx = None
        cd = None
        for q in range(1, Q + 1):
            for r in range(q):
                d_, _ = ap_descents(c, M, q, r)
                _, m_, _ = ap_t_profile(t, M, q, r)
                cd_, _ = coarse_disp(c, M, q, r)
                de = d_ if de is None else min(de, d_)
                mx = m_ if mx is None else min(mx, m_)
                cd = cd_ if cd is None else min(cd, cd_)
        row += f"{de}/{mx}/{float(cd):.0f}".rjust(9)
    print(row + f"   [blocks 0..{J}, largest head s_J = {J+1}]")
