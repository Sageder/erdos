"""banded.py — parametric "banded" within-class orders (route R20).

Motivated by route R1's mined ratio-5 witness ("the block is BANDED: bands permuted, sigma-like
fine structure inside").  Within-class key for v in base-b block [b^j, b^{j+1}):

    f(v) = (v - b^j) / (b^j (b-1))  in [0,1)   -- the offset fraction inside the block
    expand f in base B:  f = 0.d_1 d_2 d_3 ...
    key(v) = ( pi(d_1), pi(d_2), ..., pi(d_L), tail )

i.e. split the block into B bands, order the bands by the permutation pi, and recurse
inside each band.  pi = identity gives the value order, pi = reversal gives the
descending order; genuinely non-monotone pi are the interesting ones.

Combined with the class functions of Lemma R20-1 this is a fully explicit RULE.
"""
import sys, itertools
sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
from framework import restrict, violations
from constructions import cls_delay, cls_block, v2, logb, w_sigma


def make_banded(b, B, pi, L=14, inner=None):
    """pi: tuple of length B, a permutation of range(B)."""
    def key(v):
        j = logb(v, b)
        lo = b ** j
        width = lo * (b - 1)
        off = v - lo                      # in [0, width)
        digs = []
        num, den = off, width
        for _ in range(L):
            num *= B
            d = num // den
            if d >= B:
                d = B - 1
            digs.append(pi[d])
            num -= d * den
            if num == 0:
                break
        t = tuple(digs)
        return (t, inner(v)) if inner else (t, v)
    return key


def scan(M, bs, Bs, classfams, inner=None, top=25, quiet=False):
    out = []
    for cn, c in classfams.items():
        bb = int(cn.split('(')[1].split(',')[0].rstrip(')'))
        for B in Bs:
            for pi in itertools.permutations(range(B)):
                w = make_banded(bb, B, pi, inner=inner)
                key = (lambda c=c, w=w: (lambda v: (c(v), w(v))))()
                perm = restrict(key, M)
                vio = violations(perm, 4)
                if not vio:
                    out.append((10 ** 9, cn, B, pi, "SURVIVES"))
                else:
                    x, d, s = vio[0]
                    out.append((x + 3 * d, cn, B, pi,
                                f"({x},{d},{s}) terms {x},{x+d},{x+2*d},{x+3*d}"))
    out.sort(reverse=True)
    if not quiet:
        for mt, cn, B, pi, info in out[:top]:
            tag = f"SURVIVES to {M}" if mt == 10 ** 9 else f"dies@{mt}"
            print(f"{cn:11s} B={B} pi={pi}  {tag:16s} {info}")
    return out


if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    Bs = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['2', '3', '4'])]
    fams = {}
    for b in (3, 4, 5, 6, 7):
        fams[f'CLS({b},a)'] = cls_delay(b, lambda a: a)
        fams[f'BLK({b})'] = cls_block(b)
    print(f"=== banded scan, inner=value, M={M} ===")
    scan(M, None, Bs, fams)
    print(f"\n=== banded scan, inner=sigma, M={M} ===")
    scan(M, None, Bs, fams, inner=w_sigma)
