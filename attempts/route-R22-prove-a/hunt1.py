"""hunt1.py — machine hunt for counterexamples to Conjecture R21-C (and to its
repaired form R21-C').

R21-C  : (ii) + geometric fibres  =>  t constant on some infinite AP.
R21-C' : (ii) + geometric fibres  =>  some infinite AP is TAME (c|_P eventually
         non-decreasing).   [R21-C' is what Prop 29 actually needs.]

Family tested here: SCALE-INVARIANT delays.  Write v = b^{j(v)} * theta, theta in [1,b).
Put t(v) = 1 iff theta in [A,B).  Then t is 1 exactly on the union of the "annuli"
[A b^k, B b^k), k = 0,1,2,...
Both level sets have unbounded gaps, so neither contains an infinite AP; hence
t is constant on NO infinite AP.  The only question is whether (ii) holds.

Exact rational arithmetic throughout (A, B are Fractions).
"""
import sys
from fractions import Fraction
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from local import jtable, four_aps                                    # noqa: E402


def scale_t(b, A, B, N, J):
    """t[v] = 1 iff A <= v / b^{J[v]} < B."""
    An, Ad = A.numerator, A.denominator
    Bn, Bd = B.numerator, B.denominator
    pw = [1]
    while pw[-1] * b <= N:
        pw.append(pw[-1] * b)
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        P = pw[J[v]]
        if v * Ad >= An * P and v * Bd < Bn * P:
            t[v] = 1
    return t


def first_violation(t, b, N, J):
    for x, d in four_aps(N):
        v0, v1, v2, v3 = x, x + d, x + 2 * d, x + 3 * d
        c0 = J[v0] + t[v0]; c1 = J[v1] + t[v1]
        c2 = J[v2] + t[v2]; c3 = J[v3] + t[v3]
        if c0 < c1 < c2 < c3:
            return ('inc', x, d, (v0, v1, v2, v3), (c0, c1, c2, c3))
        if c0 > c1 > c2 > c3:
            return ('dec', x, d, (v0, v1, v2, v3), (c0, c1, c2, c3))
    return None


def scan(b, N, dens):
    J = jtable(N, b)
    good = []
    cands = []
    for da in dens:
        for na in range(da, b * da):
            A = Fraction(na, da)
            for db in dens:
                for nb in range(db, b * db + 1):
                    B = Fraction(nb, db)
                    if B <= A:
                        continue
                    cands.append((A, B))
    cands = sorted(set(cands))
    for (A, B) in cands:
        t = scale_t(b, A, B, N, J)
        if all(x == 0 for x in t[1:]) or all(x == 1 for x in t[1:]):
            continue
        r = first_violation(t, b, N, J)
        if r is None:
            good.append((A, B))
        else:
            pass
    return good, len(cands)


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    for b in (3, 4, 5):
        good, ncand = scan(b, N, [1, 2, 3, 4])
        print(f"b={b} N={N}: {len(good)}/{ncand} scale-invariant (A,B) satisfy (ii)")
        for g in good[:40]:
            print("    A,B =", g)
