"""forcing_class.py -- route R22 angle C, sub-targets 1 and 2.

What is being TESTED here (each labelled where it is used in the report):

 (C1)  [Theorem 16 translated]  In a class architecture with NO increasing monotone
       4-AP:  u open at scale d  =>  c(u+d) <= c(u), i.e.
       t(u+d) <= t(u) - (j(u+d) - j(u)) <= t(u).
 (C2)  [Proposition B(1)]  If c(u-2d) < c(u-d) < c(u) then u is open at d for EVERY
       within-class order -- so on such (u,d) the forcing hypothesis is class-determined
       and Theorem 16 reduces to condition (ii) on the 4-AP (u-2d,u-d,u,u+d).
 (C3)  [Proposition B(2)]  If the three classes are not strictly increasing, openness
       DEPENDS on the within-class order: exhibit (u,d) and two within-class orders,
       one making u open, one not.  => forcing carries strictly more than (ii), but
       only through the gadget, which condition (ii) does not fix.
 (C4)  [Proposition A]  For every v in Cl(u):  c(v) <= c(u), hence
       j(v) - j(u) <= t(u) - t(v) <= t(u), hence max Cl(u) < b^{t(u)+1} * u.
 (C5)  Open-pair census and closure reach in explicit architectures.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import (blockindex, perm_from_arch, fibres, ap4_violations,
                  class_seq_violations, open_scales, antiopen_scales, closure)


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def vdc_key(v):
    """van der Corput key: reverse binary digits, least significant first."""
    s = bin(v)[2:][::-1]
    return (len(s), s)


def build(N, b, tfun, orderfun):
    """orderfun(fibre_list) -> ordered list."""
    c = lambda v: blockindex(v, b) + tfun(v)
    F = fibres(N, c)
    within = {m: orderfun(F[m]) for m in F}
    perm, pos = perm_from_arch(N, c, within)
    return c, within, perm, pos


ORDERS = {
    'increasing': lambda L: sorted(L),
    'decreasing': lambda L: sorted(L, reverse=True),
    'vdc':        lambda L: sorted(L, key=vdc_key),
    'vdc_rev':    lambda L: sorted(L, key=vdc_key, reverse=True),
}


def report(N, b, tname, tfun, oname):
    c, within, perm, pos = build(N, b, tfun, ORDERS[oname])
    j = lambda v: blockindex(v, b)
    t = tfun
    viol = ap4_violations(pos, N)
    inc = [x for x in viol if x[2] == 'inc']
    dec = [x for x in viol if x[2] == 'dec']
    ii = class_seq_violations(N, c)

    # (C1) forcing check, only meaningful when there is no increasing 4-AP
    c1_tested = c1_bad = 0
    opens = 0
    for u in range(1, N + 1):
        for d in open_scales(pos, u, N):
            opens += 1
            if u + d <= N:
                c1_tested += 1
                if not (c(u + d) <= c(u)):
                    c1_bad += 1
    # (C2) class-determined openness
    c2_tested = c2_bad = 0
    for u in range(3, N + 1):
        for d in range(1, (u - 1) // 2 + 1):
            if c(u - 2 * d) < c(u - d) < c(u):
                c2_tested += 1
                if not (pos[u - 2 * d] < pos[u - d] < pos[u]):
                    c2_bad += 1
    # (C4) closure / delay bound
    c4_tested = c4_bad = 0
    worst_reach = (0, 1, 1)
    for u in range(1, N + 1):
        cl = closure(pos, u, N)
        mx = max(cl)
        for v in cl:
            c4_tested += 1
            if not (c(v) <= c(u)):
                c4_bad += 1
        if j(mx) - j(u) > t(u):
            worst_reach = ('VIOLATION', u, mx)
        if mx / u > worst_reach[0] if isinstance(worst_reach[0], (int, float)) else False:
            worst_reach = (mx / u, u, mx)
    return dict(N=N, b=b, t=tname, order=oname, inc4=len(inc), dec4=len(dec),
                ii_viol=len(ii), open_pairs=opens, C1=(c1_tested, c1_bad),
                C2=(c2_tested, c2_bad), C4=(c4_tested, c4_bad),
                max_reach=round(worst_reach[0], 3) if isinstance(worst_reach[0], float) else worst_reach)


if __name__ == "__main__":
    print("=" * 100)
    print("EXPLICIT CLASS ARCHITECTURES  (t = delay, order = within-class order)")
    print("=" * 100)
    hdr = f"{'b':>2} {'t':>8} {'order':>10} {'N':>5} {'inc4AP':>8} {'dec4AP':>8} {'(ii)viol':>9} " \
          f"{'openPairs':>10} {'C1 bad':>7} {'C2 bad':>7} {'C4 bad':>7} {'maxreach':>9}"
    print(hdr)
    rows = []
    for b in (3, 4, 5):
        for tname, tfun in (('0', lambda v: 0), ('v2', v2), ('1_odd', lambda v: v % 2)):
            for oname in ORDERS:
                N = 300
                r = report(N, b, tname, tfun, oname)
                rows.append(r)
                print(f"{r['b']:>2} {r['t']:>8} {r['order']:>10} {r['N']:>5} {r['inc4']:>8} "
                      f"{r['dec4']:>8} {r['ii_viol']:>9} {r['open_pairs']:>10} "
                      f"{r['C1'][1]:>7} {r['C2'][1]:>7} {r['C4'][1]:>7} {str(r['max_reach']):>9}")
    print()
    print("C1 = 'u open at d but c(u+d) > c(u)'  (must be 0 whenever inc4AP = 0)")
    print("C2 = 'c(u-2d)<c(u-d)<c(u) but (u-2d,u-d,u) not positionally increasing' (must be 0 always)")
    print("C4 = 'v in Cl(u) but c(v) > c(u)'      (must be 0 whenever inc4AP = 0)")
