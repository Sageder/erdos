#!/usr/bin/env python3
r"""
polyrule.py -- decide the class of POLYNOMIAL substitution rules.

CLASS.  A *polynomial substitution rule* is a finite list of pairs (g_t, L_t),
g_t in Z[n] with positive leading coefficient, L_t >= 2, such that

        sum_{t} sum_{j=0}^{L_t-1}  1/(g_t(n)+j)  =  1/n     identically.     (**)

The image of n is the union of the blocks [g_t(n), g_t(n)+L_t-1]; blocks of
length >= 2 are exactly what legality demands, so a rule of this kind is a
UNIFORM sum-preserving map raising the minimum whenever min_t g_t(n) > n.
(Theorem A of nogo.py says NO such rule exists with all g_t LINEAR.  The
classical 1/n = 1/(n+1) + 1/(n(n+1)) is a nonlinear rule with L_t = 1, so the
question is genuinely open once nonlinear forms are allowed.)

SEARCH (complete inside its stated scope).  By Theorem B2 at least one g_t is
linear.  We enumerate the LINEAR part exactly:
    blocks [a_i n + b_i , a_i n + b_i + L_i - 1],  1 <= a_i <= AMAX,
    |b_i| <= BMAX,  2 <= L_i <= LMAX,  at most KMAX blocks,
subject to the necessary leading-order condition  sum_i L_i / a_i = 1  (n -> oo).
For each we form the exact deficit  R = 1/n - (linear part)  in Q(n), and then
try to complete it with NONLINEAR blocks.  Completion is not enumerated blindly:
if R = sum_{j<L} 1/(g+j) + (rest) with deg g minimal, then g = L/R + O(1), so g
is forced to be the polynomial part of L/R up to a bounded additive constant;
we test those candidates exactly (depth DEPTH times, allowing several nonlinear
blocks of increasing degree).

Everything is exact (sympy Poly / Rational).  A negative answer is a theorem
about the enumerated class only, and the scope is printed.

usage: polyrule.py [AMAX BMAX LMAX KMAX DEPTH CONST]
"""
import sys, itertools
import sympy as sp

n = sp.symbols('n')
AMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
LMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 4
KMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 3
DEPTH = int(sys.argv[5]) if len(sys.argv) > 5 else 3
CONST = int(sys.argv[6]) if len(sys.argv) > 6 else 3


def blocksum(g, L):
    return sum(1 / (g + j) for j in range(L))


def try_complete(R, depth, used):
    """Try to write the rational function R as a sum of <= depth blocks
    [g, g+L-1] with L >= 2 and deg g >= 2.  Returns a list of (g,L) or None."""
    R = sp.cancel(sp.together(R))
    if R == 0:
        return used
    if depth == 0:
        return None
    num, den = sp.fraction(R)
    num, den = sp.Poly(num, n), sp.Poly(den, n)
    if num.degree() >= den.degree():          # R does not tend to 0: hopeless
        return None
    for L in range(2, LMAX + 1):
        # g must be close to L/R = L*den/num
        q, r = sp.div(L * den, num, n)
        qp = sp.Poly(q, n)
        if qp.degree() < 2:
            continue
        # g must be an integer polynomial within O(1) of the quotient L*den/num;
        # round every coefficient to the nearest integer and vary the constant.
        co = [sp.Integer(sp.floor(c + sp.Rational(1, 2))) for c in qp.all_coeffs()]
        base = sum(c * n ** (len(co) - 1 - i) for i, c in enumerate(co))
        cands = [sp.expand(base + d) for d in range(-CONST, CONST + 1)]
        for g in cands:
            gp = sp.Poly(g, n)
            if gp.degree() < 2 or gp.LC() <= 0:
                continue
            R2 = sp.cancel(sp.together(R - blocksum(g, L)))
            if R2 == 0:
                return used + [(g, L)]
            res = try_complete(R2, depth - 1, used + [(g, L)])
            if res is not None:
                return res
    return None


def linear_parts():
    forms = []
    for a in range(1, AMAX + 1):
        for L in range(2, LMAX + 1):
            forms.append((a, L))
    out = []
    for k in range(1, KMAX + 1):
        for combo in itertools.combinations_with_replacement(forms, k):
            if sum(sp.Rational(L, a) for a, L in combo) != 1:
                continue
            for bs in itertools.product(range(-BMAX, BMAX + 1), repeat=k):
                out.append(tuple((a, b, L) for (a, L), b in zip(combo, bs)))
    return out


if __name__ == "__main__":
    LP = linear_parts()
    print("scope: a<=%d |b|<=%d 2<=L<=%d blocks<=%d nonlinear-depth=%d const-window=%d"
          % (AMAX, BMAX, LMAX, KMAX, DEPTH, CONST))
    print("linear parts with sum L/a = 1 :", len(LP), flush=True)
    hits = []
    for idx, lp in enumerate(LP):
        # disjointness of the linear blocks for large n (else not a legal image)
        ok = True
        for (a, b, L), (a2, b2, L2) in itertools.combinations(lp, 2):
            if a == a2 and not (b + L - 1 < b2 or b2 + L2 - 1 < b):
                ok = False
        if not ok:
            continue
        R = 1 / n - sum(blocksum(a * n + b, L) for a, b, L in lp)
        R = sp.cancel(sp.together(R))
        if R == 0:
            hits.append((lp, []))
            print("EXACT LINEAR RULE", lp, flush=True)
            continue
        res = try_complete(R, DEPTH, [])
        if res is not None:
            hits.append((lp, res))
            print("HIT", lp, res, flush=True)
        if idx % 200 == 0:
            print("  ...%d/%d" % (idx, len(LP)), flush=True)
    print("total hits:", len(hits))
    for h in hits:
        print("   ", h)
