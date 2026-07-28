"""construct.py -- the SLIVER construction: an explicit refutation of Conjecture R21-C.

KEY LEMMA (proved in REPORT; verified here).  Let b >= 3 and let (x, x+d, x+2d, x+3d) be a
4-AP with x >= 1, d >= 1, and put u_i = x + i*d.  If j(u_3) = j(u_1) + 1 =: M then

        b^M  <=  u_3  <  3 * b^M ,

i.e. u_3 lies in the bottom "sliver" S_M := [b^M, 3*b^M) of its block.
(Proof: d = u_1 - x <= u_1 - 1 so u_3 = u_1 + 2d <= 3u_1 - 2 < 3 b^M, since u_1 < b^M.)

CONSTRUCTION.  b >= 4 (so S_M is a proper subset of block M), an arbitrary sequence
(h_M) of positive integers, an arbitrary subset D_M of the free region
R_M := [3 b^M, b^{M+1}) of each block.  Define

        t(v) = h_M  if v in D_M  (M = j(v)),        t(v) = 0 otherwise.

THEOREM.  c = floor(log_b .) + t satisfies condition (ii), for EVERY choice of (h_M) and
(D_M).  (Proof in REPORT; the six cases are enumerated in `explain_cases`.)

Choosing D_M = alternate stripes of width L_M -> infinity and h_M -> infinity gives a t
that is constant on NO infinite AP, has NO tame AP, has a geometric fibre design, and has
unbounded displacement along every AP.
"""
import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from cond2 import blk, violations_numpy, violations_literal, violations_caseanal, tame_report


def sliver_lemma_check(N, b):
    """Independent exhaustive verification of the KEY LEMMA."""
    J = [0] * (N + 1)
    for v in range(1, N + 1):
        J[v] = blk(v, b)
    bad = []
    pw = [b ** m for m in range(0, 40)]
    cnt = 0
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u1, u3 = x + d, x + 3 * d
            if J[u3] == J[u1] + 1:
                cnt += 1
                M = J[u3]
                if not (pw[M] <= u3 < 3 * pw[M]):
                    bad.append((x, d, u3, M))
            elif J[u3] > J[u1] + 1:
                bad.append(('block-gap violated', x, d, J[u1], J[u3]))
    return cnt, bad


def make_t(N, b, h, L, delayed_stripes=True):
    """t(v)=h(M) on alternate stripes of width L(M) inside R_M=[3b^M, b^{M+1}); 0 elsewhere."""
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        M = blk(v, b)
        lo = 3 * b ** M
        if v < lo:
            t[v] = 0
        else:
            s = (v - lo) // L(M)
            t[v] = h(M) if (s % 2 == 1) == delayed_stripes else 0
    return t


def fibre_sizes(t, N, b, mmax=None):
    from collections import Counter
    C = Counter()
    for v in range(1, N + 1):
        C[blk(v, b) + t[v]] += 1
    ms = sorted(C)
    return [(m, C[m]) for m in ms if mmax is None or m <= mmax]


def ap_displacement(t, N, b, Q=12):
    """Emission order: classes in increasing index, arbitrary inside.  The WORST-CASE
    (largest) position of v is |{w<=N : c(w) <= c(v)}|; the best case is
    |{w : c(w) < c(v)}|+1.  For an AP P we report max_n pos_P(n)/n using the *best case*
    (i.e. the most favourable within-class order) so the bound is honest: even in the best
    within-class order the displacement blows up."""
    c = [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]
    rows = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 8:
                continue
            cs = sorted((c[p], p) for p in P)
            # best-case rank of p_n: number of P-elements with strictly smaller class, +1
            import bisect
            keys = [k for k, _ in cs]
            best = {}
            for k, p in cs:
                best[p] = bisect.bisect_left(keys, k) + 1
            ratio = max(best[P[n]] / (n + 1) for n in range(len(P)))
            rows.append((q, r, round(ratio, 2)))
    return rows


def explain_cases():
    return """
Case analysis (t >= 0, t(v)=0 unless v is in the free region R_{j(v)}, where t(v)=h_{j(v)}):
Write j_i = j(u_i), D_i = j_i - j_{i-1}; block-gap lemma gives D_2 + D_3 <= 1.
  c strictly increasing  <=>  t_i - t_{i-1} > -D_i  for i = 1,2,3.
  c strictly decreasing  <=>  t_i - t_{i-1} < -D_i  for i = 1,2,3.
(D_2,D_3) = (0,0): u_1,u_2,u_3 all in block M, so t takes at most the TWO values 0, h_M on
   them; a strictly monotone triple needs three distinct values.  Impossible.
(D_2,D_3) = (0,1): j_1 = j_2 = M, j_3 = M+1.  By the KEY LEMMA u_3 lies in the sliver
   S_{M+1}, so t_3 = 0.
   increasing needs t_2 > t_1 >= 0 and t_3 >= t_2, i.e. 0 = t_3 >= t_2 > t_1 >= 0.  Impossible.
   decreasing needs t_2 > t_3 + D_3 = 1 and t_1 > t_2 + D_2 = t_2; but t_1, t_2 are both in
   {0, h_M}, so t_1 > t_2 forces t_1 = h_M, t_2 = 0, contradicting t_2 > 1.  Impossible.
(D_2,D_3) = (1,0): j_1 = M, j_2 = j_3 = M+1.  u_2 < u_3 < 3 b^{M+1} and u_2 >= b^{M+1}, so
   BOTH u_2 and u_3 lie in the sliver S_{M+1}: t_2 = t_3 = 0.
   increasing needs t_3 > t_2, i.e. 0 > 0.  Impossible.
   decreasing needs t_2 > t_3 + D_3 = 0, i.e. 0 > 0.  Impossible.
No case survives, so condition (ii) holds -- for EVERY choice of h_M and of the free-region
subsets D_M.  (Step 1 of the AP was never needed: the construction kills the last three
terms outright.)
"""


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    for b in (4, 5, 8):
        cnt, bad = sliver_lemma_check(min(N, 6000), b)
        print(f"b={b}: KEY LEMMA on {cnt} straddling 4-APs up to {min(N,6000)}: "
              f"{'OK' if not bad else 'FAILED ' + str(bad[:3])}")
    print(explain_cases())
    for b in (4, 5, 8):
        for hname, h in [("h=1 (bounded)", lambda M: 1), ("h=M+1 (unbounded)", lambda M: M + 1)]:
            t = make_t(N, b, h, lambda M: M + 1)
            V = violations_numpy(t, N, b, limit=3)
            print(f"b={b} {hname:20s} N={N}: (ii) violations = {len(V)}"
                  + (f"  {V[:2]}" if V else "   <-- SATISFIES (ii)"))
