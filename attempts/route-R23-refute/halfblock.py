"""halfblock.py -- the HALF-BLOCK witness W3: the main refutation of Conjecture R21-C.

DEFINITION.  b >= 3, j(v) = floor(log_b v), (h_M)_{M>=0} any sequence of integers >= 2.

        t(v) = 0        if v <= 2*b^{j(v)}        ("low half" L_M = [b^M, 2 b^M])
        t(v) = h_{j(v)} if v >  2*b^{j(v)}        ("high part" H_M = (2 b^M, b^{M+1}) )

THEOREM (proof in REPORT; six-case enumeration reproduced in `explain`).
c = j + t satisfies condition (ii) for EVERY b >= 3 and EVERY (h_M).
With h_M >= 2 it has a geometric fibre design, is constant on no infinite AP, has NO tame
AP, and (if h_M -> oo) has unbounded displacement along EVERY infinite AP.

The three geometric facts the proof uses, for a 4-AP (x, u_1, u_2, u_3), u_i = x+i*d:
  (G1) d <= u_1 - 1, hence u_3 = u_1 + 2d <= 3 u_1 - 2 < 3 u_1.
  (G2) block-gap: j_3 <= j_1 + 1 (needs b >= 3), so (D_2,D_3) in {(0,0),(0,1),(1,0)}.
  (G3) u_2 = (u_1 + u_3)/2.
"""
import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from cond2 import blk, violations_numpy, violations_literal, violations_caseanal


def W3(N, b, h):
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        M = blk(v, b)
        t[v] = 0 if v <= 2 * b ** M else h(M)
    return t


def explain():
    return """
Write P = b^M where M = j(u_1), Q = b P = b^{M+1}.  t is 2-valued on each block, with
t = 0 exactly on [b^K, 2 b^K] for every K.
(D_2,D_3) = (0,0): u_1,u_2,u_3 all in block M, where t takes only the two values 0 and h_M;
   a strictly monotone triple needs three distinct values.  IMPOSSIBLE.
(D_2,D_3) = (0,1): u_1,u_2 in block M, u_3 in block M+1.
   u_3 = 2u_2 - u_1 <= 2(bP - 1) - P = (2b-1)P - 2 < 2bP = 2 b^{M+1},  so t(u_3) = 0.
   increasing needs 0 <= t_1 < t_2 <= t_3 = 0.  IMPOSSIBLE.
   decreasing needs t_2 > t_3 + D_3 = 1 and t_1 > t_2 + D_2 = t_2; t_1 > t_2 with
   t_1,t_2 in {0,h_M} forces t_2 = 0, contradicting t_2 > 1.  IMPOSSIBLE.
(D_2,D_3) = (1,0): u_1 in block M, u_2,u_3 in block M+1.
   u_2 = (u_1+u_3)/2 < (bP + 3u_1)/2 < (bP + 3bP)/2 = 2bP,  so t(u_2) = 0.
   increasing needs t_1 <= t_2 = 0, i.e. t_1 = 0, i.e. u_1 <= 2P; and t_3 > t_2 = 0, i.e.
   u_3 > 2bP.  But u_3 < 3u_1 <= 6P <= 2bP for b >= 3.  IMPOSSIBLE.
   decreasing needs t_2 > t_3 + D_3 = t_3 >= 0, i.e. 0 > 0.  IMPOSSIBLE.
Step 1 of the AP is never used: the last three terms already make every case impossible.
"""


def fibres(t, N, b):
    from collections import Counter
    C = Counter()
    for v in range(1, N + 1):
        C[blk(v, b) + t[v]] += 1
    return [(m, C[m], C[m] / b ** m) for m in sorted(C) if b ** (m + 1) <= N]


def descents_per_ap(t, N, b, Q=16):
    """For each AP of step q<=Q: number of c-descents, and the block index of the last one."""
    c = [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]
    out = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 8:
                continue
            ds = [P[i] for i in range(len(P) - 1) if c[P[i + 1]] < c[P[i]]]
            out.append((q, r, len(ds), blk(ds[-1], b) if ds else -1))
    return out


def tconst_windows(t, N, b, Q=16):
    """t must be non-constant on every AP; test on the window [N/b^2, N] (spans >=2 blocks)."""
    lo = max(2, N // b ** 2)
    bad = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = [v for v in range(r, N + 1, q) if v >= lo]
            if len(P) < 6:
                continue
            if len(set(t[v] for v in P)) == 1:
                bad.append((q, r))
    return bad


def displacement(t, N, b, Q=16):
    import bisect
    c = [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]
    out = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 8:
                continue
            cs = sorted((c[p], p) for p in P)
            keys = [k for k, _ in cs]
            best = {p: bisect.bisect_left(keys, k) + 1 for k, p in cs}
            out.append((q, r, max(best[P[n]] / (n + 1) for n in range(len(P)))))
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    print(explain())
    # cross-validate the three (ii) implementations on this witness
    for b in (3, 4, 7):
        t = W3(1500, b, lambda M: M + 2)
        a = sorted(violations_numpy(t, 1500, b))
        c1 = sorted(violations_literal(t, 1500, b))
        e = sorted(violations_caseanal(t, 1500, b))
        assert a == c1 == e
    print("cross-check: three (ii) implementations agree on W3 at N=1500, b=3,4,7\n")
    for b in (3, 4, 5, 7, 10):
        for hn, h in [("h=2", lambda M: 2), ("h=M+2", lambda M: M + 2),
                      ("h=2^M+2", lambda M: 2 ** M + 2)]:
            t = W3(N, b, h)
            V = violations_numpy(t, N, b, limit=2)
            fb = fibres(t, N, b)
            dd = descents_per_ap(t, N, b)
            tc = tconst_windows(t, N, b)
            dp = displacement(t, N, b)
            notame = sum(1 for q, r, n, _ in dd if n == 0)
            print(f"b={b:2d} {hn:8s} N={N}: (ii)viol={len(V)}  "
                  f"APs(q<=16) with NO c-descent: {notame}/{len(dd)}  "
                  f"t-const APs: {len(tc)}  |F_m|/b^m in "
                  f"[{min(r[2] for r in fb):.2f},{max(r[2] for r in fb):.2f}]  "
                  f"min-max AP displacement: {min(d[2] for d in dp):.1f}-{max(d[2] for d in dp):.1f}"
                  + ("" if not V else f"   VIOLATION {V[0]}"))
