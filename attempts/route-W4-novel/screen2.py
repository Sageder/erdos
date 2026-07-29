"""screen2.py — non-digit mechanisms: Beatty/Sturmian, CF cut sequences, substitution
classes, real-valued potentials ("soft blocks"), and class+van-der-Corput architectures.

Every candidate is an explicit order-type-omega order on N (each is either a partition of
N into finite groups emitted in index order, or a potential f with f(v) >= v/C so that
{w : f(w) < f(v)} is finite).  We report:
  * the minimal monotone 4-AP of the value restriction to [1..N] (None = survives),
  * max_v pos(v)/v on the board -- the displacement constant C, which by REQUIREMENTS B7
    says how far one would have to search for a survival to mean anything
    (N*(C) ~ 4 exp(3.89(C-1.25)):  C=2 -> 74, C=3 -> 3.6e3, C=5 -> 9e6).
"""
import sys
from fractions import Fraction
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_key, pos_from_order, find_4aps
from numeration import base_digits, fibs_upto, zeck_digits

N = 4000

# ---------- helpers -------------------------------------------------------
def vdc(v, b=2, sign=0):
    """van der Corput value in [0,1) as an exact Fraction; sign=1 reverses digits."""
    d = base_digits(v, b)
    num, den = 0, 1
    for c in d:
        den *= b
        num = num * b + ((b - 1 - c) if sign else c)
    return Fraction(num, den)


def vdc_key(v, b=2, sign=0):
    """sort key for the base-b LSD (van der Corput) order restricted to a class."""
    d = base_digits(v, b)
    return tuple(((b - 1 - c) if sign else c) for c in d) + (0,) * 40


def order_from_classes(cls, N, within=None, sign_of=None):
    """cls[v] = class index (int).  Emit classes in increasing index; inside a class use
    `within` (default: van der Corput base 2, sign per class)."""
    groups = {}
    for v in range(1, N + 1):
        groups.setdefault(cls[v], []).append(v)
    out = []
    for j in sorted(groups):
        g = groups[j]
        s = 0 if sign_of is None else sign_of(j)
        g.sort(key=(within(j) if within else (lambda v, s=s: vdc_key(v, 2, s))))
        out.extend(g)
    return out


def report(name, order):
    pos = pos_from_order(order)
    n = len(order)
    hits = find_4aps(pos, n)
    disp = max((int(pos[v]) + 1) / v for v in range(1, n + 1))
    if hits:
        top, d, x, orient = hits[0]
        s = f"KILLED ({x},{x+d},{x+2*d},{x+3*d}) d={d} {orient}"
    else:
        s = f"4-AP-FREE to N={n}"
    print(f"{name:52s} | {s:44s} | C={disp:7.2f}")
    return hits


# ---------- 1. cut sequences from continued-fraction data -----------------
def cut_blocks(cuts, N, mode="rev"):
    """cuts = increasing list of block starts (1 = first).  mode: rev|vdc|vdcalt|id"""
    order = []
    cs = [c for c in cuts if c <= N] + [N + 1]
    for i in range(len(cs) - 1):
        blk = list(range(cs[i], min(cs[i + 1], N + 1)))
        if mode == "rev":
            blk.reverse()
        elif mode == "vdc":
            blk.sort(key=lambda v: vdc_key(v, 2, 0))
        elif mode == "vdcalt":
            blk.sort(key=lambda v: vdc_key(v, 2, i % 2))
        order.extend(blk)
    return order


print("=== A. cut sequences from continued-fraction / Fibonacci data (non-geometric) ===")
F = [1, 2]
while F[-1] <= N:
    F.append(F[-1] + F[-2])
report("Fibonacci cuts [F_k], blocks reversed", cut_blocks(F, N, "rev"))
report("Fibonacci cuts [F_k], vdC inside", cut_blocks(F, N, "vdc"))
report("Fibonacci cuts [F_k], vdC alternating sign", cut_blocks(F, N, "vdcalt"))
pell = [1, 2]
while pell[-1] <= N:
    pell.append(2 * pell[-1] + pell[-2])
report("Pell cuts [q_k] (sqrt2), vdC alternating", cut_blocks(pell, N, "vdcalt"))
# Sturmian-lengths cut sequence: block k has length ceil(k*alpha) for alpha=golden
alpha = Fraction(196418, 121393)          # convergent of phi, exact
cuts, c, k = [1], 1, 1
while c <= N:
    c += int(alpha * k)
    cuts.append(c)
    k += 1
report("Sturmian-length cuts (lengths ~ k*phi), reversed", cut_blocks(cuts, N, "rev"))

print()
print("=== B. Beatty / rotation gadgets inside geometric blocks ===")
al = Fraction(196418, 121393) - 1          # {phi} exact rational convergent
for b in (3, 4, 5):
    cls = [0] * (N + 1)
    for v in range(1, N + 1):
        j = 0
        p = 1
        while p * b <= v:
            p *= b
            j += 1
        cls[v] = j
    report(f"blocks ratio {b}, inside ordered by frac(v*alpha)",
           order_from_classes(cls, N, within=lambda j: (lambda v: (al * v) % 1)))
    report(f"blocks ratio {b}, inside by frac(v*alpha), alternating",
           order_from_classes(cls, N,
                              within=lambda j: (lambda v: ((al * v) % 1) * (1 if j % 2 == 0 else -1))))

print()
print("=== C. real-valued potentials: multiplicative 'soft blocks' (NON-convex classes) ===")
for K in (2, 3, 4, 6):
    report(f"f(v) = v*(1 + {K}*vdC2(v))   [soft blocks, ratio {K+1}]",
           sorted(range(1, N + 1), key=lambda v: (v * (1 + K * vdc(v, 2)), v)))
for K in (2, 3):
    report(f"f(v) = v*(1 + {K}*vdC3(v))",
           sorted(range(1, N + 1), key=lambda v: (v * (1 + K * vdc(v, 3)), v)))
for K in (2, 4):
    report(f"f(v) = v*(1 + {K}*frac(v*alpha))  [Beatty potential]",
           sorted(range(1, N + 1), key=lambda v: (v * (1 + K * ((al * v) % 1)), v)))

print()
print("=== D. class = block index + aperiodic delay, van der Corput inside class ===")
def sturm(v):
    return 1 if ((al * v) % 1) < Fraction(1, 2) else 0
def tm(v):                                    # Thue-Morse
    return bin(v).count("1") % 2
def zeckpar(v, F=fibs_upto(N)):               # parity of #Zeckendorf terms
    return sum(zeck_digits(v, F)) % 2
for b in (3, 4, 5):
    for dn, dl in (("Sturmian", sturm), ("Thue-Morse", tm), ("Zeck-parity", zeckpar)):
        cls = [0] * (N + 1)
        for v in range(1, N + 1):
            j, p = 0, 1
            while p * b <= v:
                p *= b
                j += 1
            cls[v] = 2 * j + dl(v)
        report(f"c = 2*blk{b} + {dn}, vdC(sign=class parity) inside",
               order_from_classes(cls, N, sign_of=lambda j: j % 2))
