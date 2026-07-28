"""slack.py — R17.  THE quantity: slack(u) = pos(u) - |Cl_{G*}(u)| >= 0 (Thm 16(b)).

196-YES would follow from deriving slack(u) < 0 for some u.  Here we measure how
close to 0 the slack gets on actual 4-AP-free boards, who the sinks are, and how the
minimum slack behaves as N grows.  (All finite-board numbers are LOWER bounds on
|Cl| for the infinite object, hence UPPER bounds on the true slack -- except that
pos(u) itself is also truncated: pos_{sigma_N}(u) <= pos_a(u).  Both effects push the
same way for U1 but not in general, so treat as measurement only.)
"""
import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from apcheck import has_monotone_kap_pos
from sat_order import solve
from forcing2 import make_pos, closure, out_edges, records, open_scales

from forcing2 import ALLRULES as ALL
G = ('U1',)


def run(perm, tag=""):
    N = len(perm)
    assert not has_monotone_kap_pos(perm, 4)
    pos = make_pos(perm)
    rec = set(records(pos, N))
    rows = []
    for u in range(1, N + 1):
        c = len(closure(pos, u, N, ALL))
        rows.append((pos[u] - c, u, pos[u], c))
    rows.sort()
    sinks = [u for u in range(1, N + 1) if not out_edges(pos, u, N, ALL)]
    print(f"{tag}N={N}: min slack={rows[0][0]} at u={rows[0][1]} (pos={rows[0][2]}, |Cl*|={rows[0][3]});"
          f"  5 smallest slacks: {[(r[0], r[1], r[2]) for r in rows[:5]]}")
    print(f"   G*-sinks (u,pos,isrecord): {[(u, pos[u], u in rec) for u in sinks]}")
    # slack restricted to u with pos(u) large
    big = [r for r in rows if r[2] >= N // 2]
    print(f"   min slack among pos>=N/2: {big[0][0] if big else None}  "
          f"| mean slack = {sum(r[0] for r in rows)/N:.1f}", flush=True)
    return rows[0][0]


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [40, 60, 80, 100, 130, 160, 200]
    for N in Ns:
        sat, perm = solve(N, inc4=True, dec4=True)
        assert sat
        run(perm)
