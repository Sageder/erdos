"""sat_measure.py — R17. Forcing-digraph statistics on large SAT-found 4-AP-free boards.

Compares Theorem 16's digraph G (rule U1 only) with the full forced-descent digraph
G* (rules U1,U2,D1,D2).  Everything is a LOWER bound for the infinite object
(finite board loses rule instances that reach above N).
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from apcheck import has_monotone_kap_pos
from sat_order import solve
from forcing2 import (make_pos, open_scales, out_edges, closure, longest_chain,
                      records, grounded)

from forcing2 import ALLRULES as ALL
G = ('U1',)


def report(perm, tag):
    N = len(perm)
    assert not has_monotone_kap_pos(perm, 4), "board is not 4-AP-free!"
    pos = make_pos(perm)
    rec = set(records(pos, N))
    nopen = sum(1 for u in range(1, N + 1) if open_scales(pos, u, N))
    gsinks = [u for u in range(1, N + 1) if not out_edges(pos, u, N, G)]
    gssinks = [u for u in range(1, N + 1) if not out_edges(pos, u, N, ALL)]
    clG = [len(closure(pos, u, N, G)) for u in range(1, N + 1)]
    clGs = [len(closure(pos, u, N, ALL)) for u in range(1, N + 1)]
    chG = [longest_chain(pos, u, N, G) for u in range(1, N + 1)]
    chGs = [longest_chain(pos, u, N, ALL) for u in range(1, N + 1)]
    argG = max(range(1, N + 1), key=lambda u: chG[u - 1])
    argGs = max(range(1, N + 1), key=lambda u: chGs[u - 1])
    K = 10
    print(f"{tag} N={N}: |records|={len(rec)}  open={nopen}({100*nopen//N}%)  "
          f"G-sinks={len(gsinks)}({100*len(gsinks)//N}%)  G*-sinks={len(gssinks)}({100*len(gssinks)//N}%)")
    print(f"    max|Cl_G|={max(clG)}  max|Cl_G*|={max(clGs)}   "
          f"longest chain: G={max(chG)} (from u={argG}, pos={pos[argG]})  "
          f"G*={max(chGs)} (from u={argGs}, pos={pos[argGs]})")
    print(f"    max_{{u<={K}}}|Cl_G|={max(clG[:K])}  max_{{u<={K}}}|Cl_G*|={max(clGs[:K])}  "
          f"| G*-sinks that are records: {len([u for u in gssinks if u in rec])}/{len(gssinks)}"
          f" | records that are NOT G*-sinks: {len([w for w in rec if w not in gssinks])}/{len(rec)}",
          flush=True)
    return dict(N=N, maxclG=max(clG), maxclGs=max(clGs), chG=max(chG), chGs=max(chGs),
                sinksG=len(gsinks), sinksGs=len(gssinks), nopen=nopen)


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [40, 60, 80, 100, 130, 160]
    for N in Ns:
        t0 = time.time()
        sat, perm = solve(N, inc4=True, dec4=True)
        assert sat
        report(perm, f"[sat {time.time()-t0:.0f}s]")
