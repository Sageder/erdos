"""classscreen.py — extinction thresholds for CONVEX vs NON-CONVEX class architectures
under the exact sign-vector decision procedure of signsat.py (Proposition W4-3).

Each row: the largest N at which sign vectors exist making the architecture
monotone-4-AP-free, bracketed by the first N at which none does (two solvers agreeing,
SAT models re-verified against the literal 4-AP definition).

REQUIREMENTS B7 caveat: a SURVIVAL to N only means something if the architecture's
displacement constant C is small (N*(C) ~ 4exp(3.89(C-1.25)): C=2 -> 74, C=3 -> 3.6e3).
The measured C at the SAT point is printed for exactly that reason.
"""
import sys
from fractions import Fraction
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from signsat import decide, threshold
from numeration import base_digits, zeck_digits, fibs_upto


def blk(b):
    def f(N):
        c = [0] * (N + 1)
        for v in range(1, N + 1):
            j, p = 0, 1
            while p * b <= v:
                p *= b
                j += 1
            c[v] = j
        return c
    return f


def cuts_cls(cuts):
    def f(N):
        c = [0] * (N + 1)
        cs = list(cuts)
        while cs[-1] <= N:
            cs.append(cs[-1] * (cs[-1] // cs[-2]))
        for v in range(1, N + 1):
            j = 0
            while j + 1 < len(cs) and cs[j + 1] <= v:
                j += 1
            c[v] = j
        return c
    return f


def residue_blocks(m, L):
    """NON-CONVEX: class = (which L-window) * m + (v mod m).  Fibres are arithmetic
    progressions of step m inside a window; classes interleave residues."""
    def f(N):
        c = [0] * (N + 1)
        for v in range(1, N + 1):
            c[v] = (v // L) * m + (v % m)
        return c
    return f


def geo_residue(b, m):
    """NON-CONVEX: class = b-block index * m + (v mod m)."""
    def f(N):
        c = [0] * (N + 1)
        for v in range(1, N + 1):
            j, p = 0, 1
            while p * b <= v:
                p *= b
                j += 1
            c[v] = j * m + (v % m)
        return c
    return f


def vdcfrac(v):
    d = base_digits(v, 2)
    num, den = 0, 1
    for cc in d:
        den *= 2
        num = num * 2 + cc
    return Fraction(num, den)


def soft_blocks(b, K):
    """NON-CONVEX 'soft blocks': class = floor(log_b(v*(1+K*vdC(v)))) -- a multiplicative
    scale hierarchy whose level sets are not intervals."""
    def f(N):
        c = [0] * (N + 1)
        for v in range(1, N + 1):
            x = v * (1 + K * vdcfrac(v))
            j, p = 0, Fraction(1)
            while p * b <= x:
                p *= b
                j += 1
            c[v] = j
        return c
    return f


def zeck_len_plus_wt(a):
    """NON-CONVEX: class = (index of top Zeckendorf term) * a + (#Zeckendorf terms)."""
    def f(N):
        F = fibs_upto(N)
        c = [0] * (N + 1)
        for v in range(1, N + 1):
            d = zeck_digits(v, F)
            top = max(i for i, x in enumerate(d) if x)
            c[v] = top * a + sum(d)
        return c
    return f


CANDIDATES = [
    ("CONVEX  blocks ratio 2", blk(2)),
    ("CONVEX  blocks ratio 3", blk(3)),
    ("CONVEX  blocks ratio 4", blk(4)),
    ("CONVEX  blocks ratio 5", blk(5)),
    ("CONVEX  blocks ratio 6", blk(6)),
    ("CONVEX  blocks ratio 8", blk(8)),
    ("CONVEX  accel cuts 1,2,4,10,90", cuts_cls([1, 2, 4, 10, 90])),
    ("NONCVX  residue-blocks m=2 L=8", residue_blocks(2, 8)),
    ("NONCVX  residue-blocks m=3 L=12", residue_blocks(3, 12)),
    ("NONCVX  residue-blocks m=4 L=16", residue_blocks(4, 16)),
    ("NONCVX  geo3 x residue mod 2", geo_residue(3, 2)),
    ("NONCVX  geo3 x residue mod 3", geo_residue(3, 3)),
    ("NONCVX  geo5 x residue mod 2", geo_residue(5, 2)),
    ("NONCVX  soft blocks b=3 K=2", soft_blocks(3, 2)),
    ("NONCVX  soft blocks b=4 K=3", soft_blocks(4, 3)),
    ("NONCVX  soft blocks b=5 K=4", soft_blocks(5, 4)),
    ("NONCVX  Zeck top*4 + weight", zeck_len_plus_wt(4)),
    ("NONCVX  Zeck top*8 + weight", zeck_len_plus_wt(8)),
]

if __name__ == "__main__":
    HI = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    print("architecture                      last SAT N   first UNSAT N   C at SAT   notes")
    for name, fn in CANDIDATES:
        try:
            a, b = threshold(fn, hi=HI)
        except Exception as ex:
            print(f"{name:33s} ERROR {ex}")
            continue
        v, info = decide(fn(a), a)
        c = info.get("disp", float("nan"))
        rc = info.get("recheck", "-")
        ag = info.get("agree", "?")
        if b is None:
            print(f"{name:33s} {a:8d}   (none <= {HI})   C={c:7.2f}   {rc} agree={ag}")
        else:
            v2_, i2 = decide(fn(b), b)
            print(f"{name:33s} {a:8d}   {b:11d}     C={c:7.2f}   {rc} agree={ag}/"
                  f"{i2.get('agree','?')}")
