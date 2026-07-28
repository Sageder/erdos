"""witness.py — THE COUNTEREXAMPLE to Conjecture R21-C (and to its repaired
'tameness' form).

    b >= 4 integer,  3 <= A < B < b  reals (rational here).
    t(v) = 1 if  A <= v / b^{floor(log_b v)} < B,  else 0
    c(v) = floor(log_b v) + t(v)

Claims (Theorem R22-1 in the report; verified numerically here):
  (C1) c satisfies condition (ii) on ALL of N  -- proved, and machine-checked to N.
  (C2) t is constant on NO infinite arithmetic progression.
  (C3) NO infinite arithmetic progression is tame (c|_P is never eventually
       non-decreasing) -- so Proposition 29 does not apply to any AP.
  (C4) fibres are finite with |F_m| = (b + B - A + (B-A)/b) * b^{m-1}-ish  ~ b^m.

Two independent checks of (ii) are run:
  * the O(N^2/3) (x,d) scan (int_scan)
  * a literal quadruple scan over (x, second term) (brute_scan) on a smaller prefix
Both use exact integer arithmetic.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from local import jtable                                              # noqa: E402


def build(b, A, B, N):
    J = jtable(N, b)
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
    c = [0] + [J[v] + t[v] for v in range(1, N + 1)]
    return J, t, c


def int_scan(c, N):
    """(x,d) scan."""
    for d in range(1, (N - 1) // 3 + 1):
        lim = N - 3 * d
        for x in range(1, lim + 1):
            c0 = c[x]; c1 = c[x + d]
            if c0 < c1:
                c2 = c[x + 2 * d]
                if c1 < c2 and c2 < c[x + 3 * d]:
                    return ('inc', x, d)
            elif c0 > c1:
                c2 = c[x + 2 * d]
                if c1 > c2 and c2 > c[x + 3 * d]:
                    return ('dec', x, d)
    return None


def brute_scan(c, N):
    """independent implementation: loop over (first term, second term)."""
    for x in range(1, N + 1):
        for y in range(x + 1, N + 1):
            d = y - x
            z = y + d
            w = z + d
            if w > N:
                break
            q = (c[x], c[y], c[z], c[w])
            if (q[0] < q[1] < q[2] < q[3]) or (q[0] > q[1] > q[2] > q[3]):
                return ('inc' if q[0] < q[1] else 'dec', x, d, q)
    return None


def ap_diagnostics(t, c, N, qmax=20):
    """(C2)/(C3): for every AP with q<=qmax, does t take both values in the top
    half, and does c have a descent in the top half?"""
    lo = N // 2
    bad_const, bad_tame = [], []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = [v for v in range(max(r, 1), N + 1, q) if v >= 1]
            el = [v for v in el if v >= lo]
            if len(el) < 4:
                continue
            vals = {t[v] for v in el}
            if len(vals) < 2:
                bad_const.append((q, r))
            if not any(c[el[i + 1]] < c[el[i]] for i in range(len(el) - 1)):
                bad_tame.append((q, r))
    return bad_const, bad_tame


def fibres(c, N):
    from collections import Counter
    return sorted(Counter(c[1:]).items())


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    for (b, A, B) in [(5, F(3), F(4)), (4, F(3), F(7, 2)), (6, F(3), F(5)),
                      (5, F(7, 2), F(9, 2)), (8, F(3), F(7))]:
        J, t, c = build(b, A, B, N)
        r1 = int_scan(c, N)
        print(f"b={b} A={A} B={B}  N={N}: (ii) scan -> {r1}")
        r2 = brute_scan(c, min(N, 4000))
        print(f"      independent brute scan on [1..{min(N,4000)}] -> {r2}")
        bc, bt = ap_diagnostics(t, c, N)
        print(f"      APs q<=20 with t constant on the top half: {len(bc)} {bc[:5]}")
        print(f"      APs q<=20 with NO c-descent in the top half (tame): "
              f"{len(bt)} {bt[:5]}")
        print(f"      fibre sizes: {fibres(c, N)[:9]}")
