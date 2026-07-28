"""rules.py — explicit class-function rules: does (ii) hold, and is the rule
D1-compatible (AP-uniform)?  Route R21.

For an explicit c : N -> Z>=0 we test, on [1..M], exactly the three mission conditions:

  (ii)   no 4-AP (x,x+d,x+2d,x+3d) with strictly monotone class sequence;
  (i)    fibre sizes |c^{-1}(j) cap [1..M]| (reported; growth is the design);
  (iii)  for each AP P = {r+q, ...} with q <= qmax, the maximal coarse displacement
         max_n (1 + #{m : c(p_m) < c(p_n)})/n and, more diagnostically, whether c|_P is
         weakly increasing on the top half of P (= R20-3(a)'s tame alternative, which by
         Proposition R21-2 caps the AP displacement).

The design idea being tested (route R21's lead): D1 requires the *overtaking mass* to be
equidistributed over EVERY modulus.  In CLS(b,rho) the delayed set {t >= k} is 2^k N,
which misses the odd AP entirely -- exactly R20-3(a).  The MID family replaces the 2-adic
valuation of v by the 2-adic valuation of a MIDDLE digit window of v, whose level sets
meet every AP.
"""

import sys, math
from fractions import Fraction

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                # noqa: E402


def v2(n):
    k = 0
    while n and n % 2 == 0:
        n //= 2
        k += 1
    return k


# ---------------------------------------------------------------- rule family ------
def CLS(b, rho=lambda a: a):
    """route R20's architecture: c(v) = floor(log_b v) + rho(v_2(v))."""
    def c(v):
        return int(math.log(v, b) + 1e-12) + rho(v2(v))
    return c


def SHIFT(b, s, rho=lambda a: a):
    def c(v):
        return int(math.log(v, b) + 1e-12) + rho(v2(v + s))
    return c


def MID(b, frac=Fraction(1, 2), rho=lambda a: a):
    """c(v) = floor(log_b v) + rho(v_2( floor(v / 2^h) )), h = floor(frac*bitlen(v)).
    The delayed sets {t>=k} are 'middle-digit' sets and meet EVERY arithmetic
    progression (for q < 2^h any residue is compatible with prescribed high bits)."""
    def c(v):
        L = v.bit_length()
        h = int(frac * L)
        top = v >> h
        return int(math.log(v, b) + 1e-12) + (rho(v2(top)) if top else 0)
    return c


def MIDFIX(b, h, rho=lambda a: a):
    """fixed digit window: t = rho(v_2(floor(v/2^h)))."""
    def c(v):
        top = v >> h
        return int(math.log(v, b) + 1e-12) + (rho(v2(top)) if top else 0)
    return c


# ---------------------------------------------------------------- tests ------------
def check_ii(c, M):
    """first 4-AP with strictly monotone class sequence, or None."""
    for e in range(1, (M - 1) // 3 + 1):
        for x in range(1, M - 3 * e + 1):
            s = (c(x), c(x + e), c(x + 2 * e), c(x + 3 * e))
            if s[0] < s[1] < s[2] < s[3]:
                return ('inc', x, e, s)
            if s[0] > s[1] > s[2] > s[3]:
                return ('dec', x, e, s)
    return None


def ap_diagnostics(c, M, qmax=8):
    """for each AP: max coarse displacement, and whether c is weakly increasing on the
    top half of the AP (tame alternative)."""
    rows = []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(M, q, r)
            if len(el) < 4:
                continue
            cls = [c(v) for v in el]
            L = len(cls)
            best, arg = Fraction(0), None
            for n in range(1, L + 1):
                S = sum(1 for x in cls if x < cls[n - 1])
                val = Fraction(1 + S, n)
                if val > best:
                    best, arg = val, n
            half = cls[L // 2:]
            weakinc = all(half[i] <= half[i + 1] for i in range(len(half) - 1))
            rows.append((q, r, L, best, arg, weakinc))
    return rows


def fibres(c, M):
    from collections import Counter
    return Counter(c(v) for v in range(1, M + 1))


def report(name, c, M, qmax=8):
    bad = check_ii(c, M)
    fb = fibres(c, M)
    rows = ap_diagnostics(c, M, qmax)
    tame = [(q, r) for (q, r, L, d, a, wi) in rows if wi]
    worst = min(rows, key=lambda t: t[3])
    print(f"{name:26s} M={M:5d}  (ii): {'OK' if bad is None else 'FAILS ' + str(bad)}")
    print(f"    fibre sizes (class: size) = "
          f"{sorted(fb.items())[:12]}{' ...' if len(fb) > 12 else ''}")
    print(f"    min over APs (q<={qmax}) of max coarse displacement = "
          f"{float(worst[3]):.3f} at AP (q={worst[0]},r={worst[1]}), index {worst[4]}")
    print(f"    APs whose top half is weakly increasing in class (TAME): "
          f"{len(tame)}/{len(rows)}  {tame[:10]}")
    return bad, rows


if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    print("=== control: route R20's CLS(b, a) ===")
    for b in (3, 5):
        report(f"CLS({b}, a)", CLS(b), M)
    print("\n=== shifted 2-adic (Lemma R20-1a) ===")
    report("SHIFT(3, s=1, a)", SHIFT(3, 1), M)
    print("\n=== MID: middle-digit valuation (delay meets every AP) ===")
    for frac in (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)):
        report(f"MID(3, frac={frac})", MID(3, frac), M)
    for h in (2, 3, 4):
        report(f"MIDFIX(3, h={h})", MIDFIX(3, h), M)
