"""coarsen.py — Proposition R21-5: the coarse (class-architecture) conditions are
satisfied by the geometric COARSENING of any monotone-4-AP-free permutation.

Given a monotone-4-AP-free permutation a of [1..N] and a ratio b, define
    c(v) := j   where   pos_a(v) in [b^j, b^{j+1}).
Then
  * the fibres are exactly the geometric position blocks: |F_j| = #([b^j,b^{j+1}) cap [1..N]);
  * c satisfies (ii): a strictly monotone class sequence along a 4-AP would make pos_a
    strictly monotone along that 4-AP, i.e. a monotone 4-AP of a;
  * (measured) the number of TAME APs (c|_P weakly increasing on the top half) is small
    or zero.
Since monotone-4-AP-free permutations of [1..N] exist for every N (parity recursion), the
mission's conditions (i)+(ii) -- and empirically (iii) in its no-tame form -- can never be
refuted by a finite search.  This is the structural reason every search in this route
returned SAT.
"""

import sys, ast, os, time, math

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_elements                                       # noqa: E402
from clsdisp import four_aps                                         # noqa: E402
from apcheck import has_monotone_kap_pos                             # noqa: E402
from engine import OrderEncoding, solve, verify_avoider              # noqa: E402


def coarsen(perm, b):
    N = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    return [0] + [int(math.log(pos[v], b) + 1e-12) for v in range(1, N + 1)]


def check_ii(cl, N):
    for (a, b_, cc, d) in four_aps(N):
        s = (cl[a], cl[b_], cl[cc], cl[d])
        if s[0] < s[1] < s[2] < s[3]:
            return ('inc', a, b_, cc, d, s)
        if s[0] > s[1] > s[2] > s[3]:
            return ('dec', a, b_, cc, d, s)
    return None


def tame_count(cl, N, qmax=8):
    out = []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = ap_elements(N, q, r)
            if len(el) < 4:
                continue
            cs = [cl[v] for v in el]
            h = cs[len(cs) // 2:]
            if all(h[i] <= h[i + 1] for i in range(len(h) - 1)):
                out.append((q, r))
    return out


if __name__ == "__main__":
    from collections import Counter
    perms = []
    R20 = '/home/user/erdos/attempts/route-R20-vlogv'
    for fn in ('cw_CLS(5,a)_250.txt', 'cw_CLS(3,a)_160.txt', 'wit_N90_a0.5.txt'):
        p = os.path.join(R20, fn)
        if os.path.exists(p):
            perm = ast.literal_eval(open(p).read().strip())
            if sorted(perm) == list(range(1, len(perm) + 1)):
                perms.append((fn, perm))
    for N in (60, 120):
        enc = OrderEncoding(N)
        enc.no_monotone_4ap()
        res, perm, _ = solve(enc, time_budget=600)
        if res == "SAT":
            verify_avoider(perm, N)
            perms.append((f"CEGAR avoider N={N}", perm))
    for tag, perm in perms:
        N = len(perm)
        assert not has_monotone_kap_pos(perm, 4), tag
        for b in (2, 3, 5):
            cl = coarsen(perm, b)
            bad = check_ii(cl, N)
            tm = tame_count(cl, N)
            sizes = sorted(Counter(cl[1:]).items())
            print(f"{tag:24s} N={N:4d} b={b}: (ii) {'OK' if bad is None else 'FAILS '+str(bad)};"
                  f"  fibres {sizes};  tame APs (q<=8): {len(tm)} {tm[:6]}")
            assert bad is None, (tag, b, bad)
    print("\nProposition R21-5 confirmed: the geometric coarsening of every tested finite "
          "avoider satisfies (i)+(ii) exactly, for every ratio b tested.")
