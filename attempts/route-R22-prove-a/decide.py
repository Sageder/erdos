"""decide.py — EXACT and COMPLETE decision of condition (ii) for scale-invariant delays.

Scale-invariant delay:  tau : [1,b) -> {0..T} piecewise constant with rational
breakpoints;  t(v) := tau(v / b^{j_b(v)});  c := j_b + t.
Extend to positive reals:  C(z) := floor(log_b z) + tau(mantissa_b(z)),  so C(bz)=C(z)+1.

(CONT):  no 4-AP of positive REALS (Y0,Y1,Y2,Y3) has C strictly monotone.
(CONT) => condition (ii) on N  (integers are a subset of the reals).
Conversely a violation of (CONT) on an OPEN region yields integer violations for all
large scales, so for open violations the two are equivalent.

DECISION PROCEDURE (exact, complete).
Normalise by a power of b so that Y1 in [1,b)  (allowed: C(bz)=C(z)+1 preserves the
monotonicity pattern).  Then, writing the AP as Y_i = Y1 + (i-1)E:
    Y3 = 2*Y2 - Y1,   Y0 = 2*Y1 - Y2,
so the configuration is the point (Y1,Y2) in the plane, and every constraint
"Y_i lies in piece p" is a pair of linear inequalities in (Y1,Y2).
Enumerate all assignments of pieces to Y0..Y3 whose C-values are strictly monotone,
and test each resulting 2-variable linear system for feasibility by exact
Fourier-Motzkin elimination over the rationals (strictness tracked).
Ranges used (proved in REPORT):
   J(Y3) <= J(Y1) + 1  since Y3/Y1 < 3 <= b        -> Y2, Y3 in [1, b^2)
   Y0 in (0, Y1) subset (0, b);  levels below -(T+2) make C(Y0) < C(Y1) automatic.
"""
import sys
from fractions import Fraction as F


# ------------------------------------------------------- exact 2-var feasibility ----
# constraint: (a, b, c, strict)  meaning  a*Y1 + b*Y2 <= c   (or < c if strict)

def _feasible_1d(cons):
    """cons: list of (a, c, strict) meaning a*x <= c (or <). Return True if some x."""
    lo, lo_strict = None, False
    hi, hi_strict = None, False
    for (a, c, st) in cons:
        if a == 0:
            if c < 0 or (c == 0 and st):
                return False
            continue
        if a > 0:
            v = F(c, 1) / a
            if hi is None or v < hi or (v == hi and st):
                if hi is None or v < hi:
                    hi, hi_strict = v, st
                else:
                    hi_strict = hi_strict or st
        else:
            v = F(c, 1) / a
            if lo is None or v > lo or (v == lo and st):
                if lo is None or v > lo:
                    lo, lo_strict = v, st
                else:
                    lo_strict = lo_strict or st
    if lo is None or hi is None:
        return True
    if lo < hi:
        return True
    if lo == hi:
        return not (lo_strict or hi_strict)
    return False


def feasible_2d(cons):
    """cons: list of (a,b,c,strict) meaning a*Y1+b*Y2 <= c (or <).  Exact."""
    ups, los, rest = [], [], []
    for (a, b, c, st) in cons:
        if b == 0:
            rest.append((a, c, st))
        elif b > 0:                       # Y2 <= (c - a*Y1)/b
            ups.append((F(-a, 1) / b, F(c, 1) / b, st))     # Y2 <= p*Y1 + q
        else:                             # Y2 >= (c - a*Y1)/b
            los.append((F(-a, 1) / b, F(c, 1) / b, st))     # Y2 >= p*Y1 + q
    newc = list(rest)
    for (pl, ql, sl) in los:
        for (pu, qu, su) in ups:
            # pl*Y1+ql <= pu*Y1+qu  ->  (pl-pu)*Y1 <= qu-ql
            newc.append((pl - pu, qu - ql, sl or su))
    if not los or not ups:
        return _feasible_1d(rest) if rest else True
    return _feasible_1d(newc)


# ------------------------------------------------------------------ pieces ----------
def pieces_at_level(tau, b, m):
    """tau = [(s_0=1, v_0), (s_1, v_1), ...] on [1,b).  Returns list of
    (lo, hi, cval) for the level-m copy: [b^m*s_i, b^m*s_{i+1}) with C = m + v_i."""
    P = F(b) ** m
    out = []
    for i, (s, v) in enumerate(tau):
        hi = tau[i + 1][0] if i + 1 < len(tau) else F(b)
        out.append((F(s) * P, F(hi) * P, m + v))
    return out


def decide(tau, b, verbose=False):
    """Return None if (CONT) holds, else a witness (Y1,Y2) description."""
    T = max(v for _, v in tau)
    lvl0 = pieces_at_level(tau, b, 0)
    lvl01 = lvl0 + pieces_at_level(tau, b, 1)
    mlow = -(T + 2)
    p0 = []
    for m in range(mlow, 1):
        p0 += pieces_at_level(tau, b, m)
    CATCH = ('catch', F(0), F(b) ** mlow, None)      # C(Y0) automatically small

    # linear forms:  Y0 = 2Y1 - Y2, Y1, Y2, Y3 = -Y1 + 2Y2
    forms = {0: (F(2), F(-1)), 1: (F(1), F(0)), 2: (F(0), F(1)), 3: (F(-1), F(2))}

    def box(i, lo, hi):
        """lo <= form_i < hi  as two constraints."""
        a, bb = forms[i]
        return [(-a, -bb, -lo, False), (a, bb, hi, True)]

    base = []
    # AP ordering Y0 < Y1 < Y2 < Y3 is automatic from E>0; impose E > 0: Y2 - Y1 > 0
    base.append((F(1), F(-1), F(0), True))          # Y1 - Y2 < 0
    base.append((F(-2), F(1), F(0), True))          # -Y0 < 0  i.e. Y0 > 0

    cnt = 0
    for (l1, h1, c1) in lvl0:
        for (l2, h2, c2) in lvl01:
            if c2 == c1:
                continue
            for (l3, h3, c3) in lvl01:
                if not ((c1 < c2 < c3) or (c1 > c2 > c3)):
                    continue
                pre = list(base) + box(1, l1, h1) + box(2, l2, h2) + box(3, l3, h3)
                if not feasible_2d(pre):
                    continue
                for pz in p0 + [CATCH]:
                    if pz[0] == 'catch':
                        l0, h0, c0 = pz[1], pz[2], None
                        okinc = (c1 < c2 < c3)
                        okdec = False           # C(Y0) very small: cannot exceed C(Y1)
                    else:
                        l0, h0, c0 = pz
                        okinc = (c0 < c1 < c2 < c3)
                        okdec = (c0 > c1 > c2 > c3)
                    if not (okinc or okdec):
                        continue
                    cons = pre + box(0, l0, h0)
                    cnt += 1
                    if feasible_2d(cons):
                        return dict(kind='inc' if okinc else 'dec',
                                    cvals=(c0, c1, c2, c3),
                                    boxes=((l0, h0), (l1, h1), (l2, h2), (l3, h3)))
    if verbose:
        print("   systems tested:", cnt)
    return None


def annulus(A, B, b):
    A, B = F(A), F(B)
    assert 1 <= A < B <= b
    tau = []
    tau.append((F(1), 1 if A == 1 else 0))
    if A > 1:
        tau.append((A, 1))
    if B < b:
        tau.append((B, 0))
    return tau


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print("control: tau == 0 (c = j_b):", decide([(F(1), 0)], b))
    print("control: annulus A=3/2 B=2 (known integer violation 547,1531,2515,3499):")
    print("   ", decide(annulus(F(3, 2), F(2), b), b))
