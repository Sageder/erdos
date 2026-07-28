"""census.py — R17. Exhaustive census over ALL monotone-4-AP-free permutations of [1..N].

Measured (exactly, all boards):
  A. records are G-closed (Thm R17.1): count violations of "w record => w has no U1 edge".
  B. #G-sinks (= closed values) and #G*-sinks per board; are the sinks exactly the records?
  C. (B1)-propagation: is there always an open u and a scale d with u+d closed?
     (proof: chains terminate; here we measure how often propagation fails.)
  D. closure sizes: max |Cl_G(u)|, max |Cl_{G*}(u)|; the gain from the 3 extra rules.
  E. FCH-style: min over boards of max_{u<=K} |Cl_{G*}(u)|  (0 = finite boards give
     no leverage, which is what the 3-AP-free parity board forces).
Caveat: finite boards are the exact shadow of the infinite object only for rule U1;
rules U2/D1/D2 lose instances that use values > N, so G*-numbers are lower bounds.
"""

import sys
from itertools import permutations
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R17-cosupply')
from apcheck import has_monotone_kap_pos
from forcing2 import (make_pos, open_scales, out_edges, closure, records, grounded,
                      RULES)

from forcing2 import ALLRULES as ALL


def board_stats(perm, K=3):
    N = len(perm)
    pos = make_pos(perm)
    rec = set(records(pos, N))
    gr = set(grounded(pos, N))
    openv = set()
    Gsink = set()
    Gssink = set()
    for u in range(1, N + 1):
        if open_scales(pos, u, N):
            openv.add(u)
        else:
            Gsink.add(u)
        if not out_edges(pos, u, N, ALL):
            Gssink.add(u)
    # A: records must be G-sinks
    viol_rec = [w for w in rec if w in openv]
    # C: some open u with a scale d s.t. u+d is G-closed
    prop_fail = 0
    prop_tot = 0
    for u in openv:
        for d in open_scales(pos, u, N):
            if u + d <= N:
                prop_tot += 1
                if u + d in Gsink:
                    prop_fail += 1
    maxG = max(len(closure(pos, u, N, ('U1',))) for u in range(1, N + 1))
    maxGs = max(len(closure(pos, u, N, ALL)) for u in range(1, N + 1))
    smallGs = max(len(closure(pos, u, N, ALL)) for u in range(1, min(K, N) + 1))
    return dict(rec=rec, gr=gr, openv=openv, Gsink=Gsink, Gssink=Gssink,
                viol_rec=viol_rec, prop_fail=prop_fail, prop_tot=prop_tot,
                maxG=maxG, maxGs=maxGs, smallGs=smallGs)


if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    for N in range(4, Nmax + 1):
        cnt = 0
        viol = 0
        sinks_eq_rec = 0
        gstar_rec_escape = 0     # boards where some record is NOT a G*-sink
        propfail_boards = 0
        pf_tot = pf_num = 0
        maxG = maxGs = 0
        min_small = 10 ** 9
        sumGsink = sumGssink = 0
        gsink_notrec = 0
        example_escape = None
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            cnt += 1
            st = board_stats(list(p))
            viol += len(st['viol_rec'])
            if st['Gsink'] == st['rec']:
                sinks_eq_rec += 1
            if not (st['rec'] <= st['Gssink']):
                gstar_rec_escape += 1
                if example_escape is None:
                    example_escape = (p, sorted(st['rec'] - st['Gssink']))
            if st['prop_fail']:
                propfail_boards += 1
            pf_num += st['prop_fail']
            pf_tot += st['prop_tot']
            maxG = max(maxG, st['maxG'])
            maxGs = max(maxGs, st['maxGs'])
            min_small = min(min_small, st['smallGs'])
            sumGsink += len(st['Gsink'])
            sumGssink += len(st['Gssink'])
            gsink_notrec += len(st['Gsink'] - st['rec'])
        print(f"N={N}: avoiders={cnt}")
        print(f"   A record-is-G-closed violations: {viol}")
        print(f"   B mean #G-sinks={sumGsink/cnt:.2f}  mean #G*-sinks={sumGssink/cnt:.2f}"
              f"   (of {N} values); boards with G-sinks == records: {sinks_eq_rec}/{cnt};"
              f" mean #(G-sinks that are not records)={gsink_notrec/cnt:.2f}")
        print(f"   B' boards where some record ESCAPES being a G*-sink: {gstar_rec_escape}/{cnt}"
              + (f"  e.g. {example_escape}" if example_escape else ""))
        print(f"   C forcing edges u->u+d with u+d G-closed: {pf_num}/{pf_tot};"
              f" boards where propagation fails somewhere: {propfail_boards}/{cnt}")
        print(f"   D max|Cl_G|={maxG}  max|Cl_G*|={maxGs}")
        print(f"   E min over boards of max_{{u<=3}}|Cl_G*(u)| = {min_small}", flush=True)
