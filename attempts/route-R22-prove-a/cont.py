"""cont.py — EXACT continuous test of condition (ii) for scale-invariant delays.

Setup.  b >= 3 integer.  tau : [1,b) -> Z>=0.  Extend to all reals z > 0 by
    C(z) := floor(log_b z) + tau( z / b^{floor(log_b z)} ),
so C(b z) = C(z) + 1  (scale invariance with ratio b).
For integers v, C(v) = j_b(v) + t(v) with t(v) = tau(v/b^{j(v)}) >= 0:  exactly the
architecture of Conjecture R21-C.

Condition (ii) for the integer architecture is the restriction to integer (x,d) of

    (CONT)  for all real y > 0 and e > 0:
            (C(y), C(y+e), C(y+2e), C(y+3e)) is neither strictly increasing nor
            strictly decreasing.

So (CONT)  =>  (ii) holds on ALL of N.  This is the key: (CONT) is a finite, exactly
decidable condition, and it settles the INFINITE statement.

Reductions proved in REPORT (re-derived by the code's structure):
 * strictly decreasing is impossible whenever tau <= 1 (C(z) in {J(z), J(z)+1}, and
   C(y) > C(y+3e) forces all four into one b-block, where C takes <= 2 values).
 * strictly increasing forces y+3e > b*y, i.e. y/e < 3/(b-1)  (bounded region).
 * scale invariance lets us fix e = 1.

Exact arithmetic: A, B, and all test points are Fractions.
"""
import sys
from fractions import Fraction as F


def C_of(z, b, cuts):
    """z a positive Fraction; cuts = sorted list of tau's breakpoints in [1,b) with
    values, given as list of (start, value) with start[0] == 1.
    Returns floor(log_b z) + tau(mantissa)."""
    k = 0
    while z >= b:
        z /= b
        k += 1
    while z < 1:
        z *= b
        k -= 1
    val = cuts[0][1]
    for (s, v) in cuts:
        if z >= s:
            val = v
        else:
            break
    return k + val


def critical_ys(b, cuts, ymax, kmin=-6, kmax=3):
    """all y in (0, ymax] of the form beta*b^k - i, i in 0..3, beta a breakpoint."""
    S = set()
    for (s, _) in cuts:
        for k in range(kmin, kmax + 1):
            base = F(s) * F(b) ** k
            for i in range(4):
                y = base - i
                if 0 < y <= ymax:
                    S.add(y)
    return sorted(S)


def violations(b, cuts, verbose=False):
    """exhaustive exact search for a (CONT) violation with e = 1.
    Tests every critical y and a midpoint of every gap between consecutive
    critical ys, plus one point below the smallest critical y."""
    ymax = F(3, b - 1)
    crit = critical_ys(b, cuts, ymax)
    pts = []
    prev = F(0)
    for y in crit:
        pts.append((prev + y) / 2)
        pts.append(y)
        prev = y
    pts.append((prev + ymax) / 2)
    pts.append(ymax)
    bad = []
    for y in pts:
        if y <= 0:
            continue
        c = [C_of(y + i, b, cuts) for i in range(4)]
        if c[0] < c[1] < c[2] < c[3]:
            bad.append(('inc', y, tuple(c)))
        if c[0] > c[1] > c[2] > c[3]:
            bad.append(('dec', y, tuple(c)))
    # tiny-y regime: C(y) -> -inf, so only the 3-term tail matters
    tiny = crit[0] / 2 if crit else F(1, 100)
    for y in [tiny, tiny / 7, tiny / 101]:
        c = [C_of(y + i, b, cuts) for i in range(1, 4)]
        if c[0] < c[1] < c[2]:
            bad.append(('inc-tail', y, tuple(c)))
    return bad


def annulus_cuts(A, B, b):
    """tau = 1 on [A,B), 0 elsewhere in [1,b);  requires 1 <= A < B <= b."""
    cuts = [(F(1), 0)]
    if A > 1:
        cuts.append((F(A), 1))
    else:
        cuts = [(F(1), 1)]
    if B < b:
        cuts.append((F(B), 0))
    return cuts


def scan_annuli(b, dens):
    out = []
    seen = set()
    for da in dens:
        for na in range(da + 1, b * da):
            A = F(na, da)
            if not (1 < A < b):
                continue
            for db in dens:
                for nb in range(db + 1, b * db):
                    B = F(nb, db)
                    if not (A < B < b):
                        continue
                    if (A, B) in seen:
                        continue
                    seen.add((A, B))
                    cuts = annulus_cuts(A, B, b)
                    bad = violations(b, cuts)
                    if not bad:
                        out.append((A, B))
    return out, len(seen)


if __name__ == "__main__":
    dens = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1
                             else ['1', '2', '3', '4', '5', '6'])]
    for b in (3, 4, 5, 6):
        good, n = scan_annuli(b, dens)
        print(f"b={b}: {len(good)}/{n} annuli 1<A<B<b satisfy (CONT)")
        for g in good[:60]:
            print("     A =", g[0], " B =", g[1])
