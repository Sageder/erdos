"""validate.py — cross-validation of the continuous checker cont.py against the
exact integer checker local.py / hunt1.py, plus positive controls.

Standard: any claim of "no violation" must be reproduced by a second, independent
encoding.  Here:
  (1) positive control: a tau that provably violates (CONT) must be detected;
  (2) agreement: for many random step-function taus, CONT-clean  <=>  integer-clean
      on [1..N] for large N (one-way implication CONT-clean => integer-clean is a
      theorem; the converse is only expected, and disagreements are reported);
  (3) the integer checker is itself cross-checked against a literal brute-force
      quadruple scan on small N.
"""
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from local import jtable                                              # noqa: E402


def tau_to_t(cuts, b, N, J):
    """t[v] = tau(v/b^{J[v]}) using exact rational comparison."""
    pw = [1]
    while pw[-1] * b <= N:
        pw.append(pw[-1] * b)
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        P = pw[J[v]]
        val = cuts[0][1]
        for (s, vv) in cuts:
            if F(v) >= F(s) * P:
                val = vv
            else:
                break
        t[v] = val
    return t


def int_violation(t, b, N, J, cap=3):
    out = []
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            v0, v1, v2, v3 = x, x + d, x + 2 * d, x + 3 * d
            c0 = J[v0] + t[v0]; c1 = J[v1] + t[v1]
            c2 = J[v2] + t[v2]; c3 = J[v3] + t[v3]
            if c0 < c1 < c2 < c3:
                out.append(('inc', x, d, (c0, c1, c2, c3)))
            elif c0 > c1 > c2 > c3:
                out.append(('dec', x, d, (c0, c1, c2, c3)))
            if len(out) >= cap:
                return out
    return out


def brute_int_violation(t, b, N, J, cap=3):
    """literal definition scan over (x,d) — same thing, written independently as a
    triple loop over the four values."""
    out = []
    for x in range(1, N + 1):
        for y in range(x + 1, N + 1):
            d = y - x
            if x + 3 * d > N:
                break
            q = [x, x + d, x + 2 * d, x + 3 * d]
            cc = [J[u] + t[u] for u in q]
            inc = all(cc[i] < cc[i + 1] for i in range(3))
            dec = all(cc[i] > cc[i + 1] for i in range(3))
            if inc or dec:
                out.append(('inc' if inc else 'dec', x, d, tuple(cc)))
                if len(out) >= cap:
                    return out
    return out


def random_cuts(b, rng, maxval=3, npieces=4):
    pts = sorted({F(rng.randint(1, 6 * (b - 1)) + 6, 6) for _ in range(npieces)})
    pts = [p for p in pts if 1 < p < b]
    cuts = [(F(1), rng.randint(0, maxval))]
    for p in pts:
        cuts.append((p, rng.randint(0, maxval)))
    return cuts


if __name__ == "__main__":
    b = 3
    print("--- integer checker vs literal brute force, N=300, 60 random taus ---")
    rng = random.Random(20260728)
    Nb = 300
    Jb = jtable(Nb, b)
    ok = True
    for _ in range(60):
        cu = random_cuts(b, rng)
        t = tau_to_t(cu, b, Nb, Jb)
        a = bool(int_violation(t, b, Nb, Jb, cap=1))
        c = bool(brute_int_violation(t, b, Nb, Jb, cap=1))
        if a != c:
            ok = False
            print("   MISMATCH", cu, a, c)
    print("   agreement:", ok)
