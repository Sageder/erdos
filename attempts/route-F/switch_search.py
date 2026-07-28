#!/usr/bin/env python3
"""route-F step 1: SWITCH search.

A SWITCH on a window W=[x,y] for a modulus D is a pair (A,B) of legal systems
with A,B subset of W and  Sigma(B)-Sigma(A) = c/D  with c a nonzero integer.

LEMMA F1 (proved, see NOTES.md).  If (A,B) is a switch on [x,y], w=y-x, then
every n in A xor B satisfies:  for every prime p>w, p^{nu_p(n)} | D.
Call such n FREE; write F = F(x,y,D) for the set of free elements.

So the search is: find disjoint A',B' subset of F with Sigma(B')-Sigma(A')=c/D,
then repair legality with a common core C (see legalise()).

All arithmetic exact (int / Fraction).
"""
import sys
from fractions import Fraction
from math import gcd
from lib import smallest_prime_factors, lcm_list


def free_elements(x, y, D, spf):
    """{n in [x,y] : for every prime p > y-x, nu_p(n) <= nu_p(D)}"""
    w = y - x
    F = []
    for n in range(x, y + 1):
        m = n
        ok = True
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            if p > w:
                # nu_p(D) needed >= e
                d = D
                f = 0
                while d % p == 0:
                    d //= p
                    f += 1
                if f < e:
                    ok = False
                    break
        if ok:
            F.append(n)
    return F


def mitm_switches(F, D, max_report=40, cmax=None):
    """Enumerate sign vectors eps in {-1,0,1}^F with denom(sum eps_n/n) | D.
    Returns list of (c, [n with eps=-1 -> A'], [n with eps=+1 -> B']) with
    Sigma(B')-Sigma(A') = c/D, c != 0.  Meet-in-the-middle over residues.
    """
    L = lcm_list(F)
    g = gcd(L, D)
    M = L // g              # need S := sum eps_n * (L/n)  ==  0 (mod M)
    wts = [L // n for n in F]
    k = len(F)
    h = k // 2
    left, right = list(range(h)), list(range(h, k))

    # build right table: residue -> list of sign vectors (packed)
    table = {}
    for code in range(3 ** len(right)):
        c = code
        S = 0
        vec = []
        for i in right:
            t = c % 3
            c //= 3
            vec.append(t)
            if t == 1:
                S -= wts[i]
            elif t == 2:
                S += wts[i]
        table.setdefault(S % M, []).append(code)

    out = []
    seen = set()
    for code in range(3 ** len(left)):
        c = code
        S = 0
        for i in left:
            t = c % 3
            c //= 3
            if t == 1:
                S -= wts[i]
            elif t == 2:
                S += wts[i]
        r = (-S) % M
        if r in table:
            for rcode in table[r]:
                # reconstruct
                eps = [0] * k
                cc = code
                for i in left:
                    eps[i] = cc % 3
                    cc //= 3
                cc = rcode
                for i in right:
                    eps[i] = cc % 3
                    cc //= 3
                if all(e == 0 for e in eps):
                    continue
                tot = Fraction(0)
                Ap, Bp = [], []
                for i in range(k):
                    if eps[i] == 1:
                        Ap.append(F[i]); tot -= Fraction(1, F[i])
                    elif eps[i] == 2:
                        Bp.append(F[i]); tot += Fraction(1, F[i])
                cval = tot * D
                assert cval.denominator == 1, (cval, eps)
                cval = int(cval)
                if cval == 0:
                    continue
                if cmax is not None and abs(cval) > cmax:
                    continue
                key = (cval, tuple(Ap), tuple(Bp))
                if key in seen:
                    continue
                seen.add(key)
                out.append((cval, Ap, Bp))
                if len(out) >= max_report:
                    return out
    return out


def min_abs_c(F, D):
    """smallest |c| over all nonzero switches supported on F (exhaustive)."""
    best = None
    for c, Ap, Bp in mitm_switches(F, D, max_report=10 ** 9):
        if best is None or abs(c) < abs(best[0]):
            best = (c, Ap, Bp)
    return best


if __name__ == "__main__":
    x = int(sys.argv[1]); y = int(sys.argv[2]); D = int(sys.argv[3])
    spf = smallest_prime_factors(y + 1)
    F = free_elements(x, y, D, spf)
    print("window [%d,%d]  w=%d  D=%d" % (x, y, D, y - x))
    print("free elements (%d): %s" % (len(F), F))
    if len(F) > 26:
        print("too many for MITM here"); sys.exit(0)
    res = mitm_switches(F, D, max_report=20, cmax=None)
    for c, Ap, Bp in res[:20]:
        print("c=%d  A'=%s  B'=%s" % (c, Ap, Bp))
