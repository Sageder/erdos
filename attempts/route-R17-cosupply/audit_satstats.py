"""Reproduce the report's un-scripted SAT-board numbers:
   'immediate-death edges 40-67 % (G) -> 2-9 % (G*)' and 'longest chain 14 -> 132 at N=320'."""
import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from apcheck import has_monotone_kap_pos
from sat_order import solve
from forcing2 import make_pos, out_edges, longest_chain, ALLRULES, records

G = ('U1',)
for N in [int(x) for x in (sys.argv[1:] or [40, 60, 80, 100, 130, 160, 200, 260, 320])]:
    sat, perm = solve(N, inc4=True, dec4=True)
    assert sat and not has_monotone_kap_pos(perm, 4)
    pos = make_pos(perm)
    gsink = {u for u in range(1, N + 1) if not out_edges(pos, u, N, G)}
    gssink = {u for u in range(1, N + 1) if not out_edges(pos, u, N, ALLRULES)}
    eG = [(u, t) for u in range(1, N + 1) for t in out_edges(pos, u, N, G)]
    eGs = [(u, t) for u in range(1, N + 1) for t in out_edges(pos, u, N, ALLRULES)]
    dG = sum(1 for (u, t) in eG if t in gsink)
    dGs = sum(1 for (u, t) in eGs if t in gssink)
    cG = max(longest_chain(pos, u, N, G) for u in range(1, N + 1))
    cGs = max(longest_chain(pos, u, N, ALLRULES) for u in range(1, N + 1))
    print(f"N={N}: G edges={len(eG)} dead={dG} ({100*dG/max(1,len(eG)):.0f}%) | "
          f"G* edges={len(eGs)} dead={dGs} ({100*dGs/max(1,len(eGs)):.0f}%) | "
          f"sinks G={len(gsink)}({100*len(gsink)//N}%) G*={len(gssink)}({100*len(gssink)//N}%) | "
          f"longest chain G={cG} G*={cGs}", flush=True)
