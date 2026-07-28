"""selfsim_chain.py — an explicit SELF-SIMILAR infinite forcing chain inside tau.

Scale invariance (proved in REPORT.md, Lemma O2): for the constant-priority comparator
tau, u is open at scale d  <=>  3u is open at scale 3d.  Hence if there is a finite
forcing path  u = w_0 -> w_1 -> ... -> w_r = 3^j * u,  then applying the scaling
n |-> 3^j n repeatedly concatenates it into an INFINITE forcing chain
  u -> ... -> 3^j u -> ... -> 3^{2j} u -> ...
Every step u_k -> u_{k+1} of a forcing chain gives u_{k+1} < u_k in the order
(Theorem 16(a)), so tau contains an infinite strictly descending sequence — the exact
obstruction Theorem 16 forbids in a 4-AP-free permutation of N.

This script SEARCHES for such a u (a "scaling cycle") and verifies the found path
directly against the raw definition of openness (tau.before), not via Lemma O.
"""

import sys
from collections import deque

sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, v3, dig3
from chains_tau import open_scales_natural


def reach_path(u0, target, M):
    """BFS in the forcing DAG from u0 to target (values increase, all <= M)."""
    prev = {u0: None}
    q = deque([u0])
    while q:
        u = q.popleft()
        if u == target:
            break
        for d in open_scales_natural(u, M):
            w = u + d
            if w not in prev:
                prev[w] = u
                q.append(w)
    if target not in prev:
        return None
    p, x = [], target
    while x is not None:
        p.append(x)
        x = prev[x]
    return p[::-1]


def verify_path(t, p):
    """Verify each step u -> u+d is a genuine forcing step from the RAW definition."""
    for u, w in zip(p, p[1:]):
        d = w - u
        assert d >= 1 and u - 2 * d >= 1, (u, w)
        a, b = u - 2 * d, u - d
        assert t.before(a, b) and t.before(b, u), ("not open", u, d)
        assert t.before(w, u), ("forcing conclusion fails", u, d)
    return True


if __name__ == "__main__":
    t = Tau(prio_const((0, 1, 2)))
    print("searching for a scaling cycle u ->* 3^j u  (natural priorities)")
    found = []
    for u0 in range(2, 400):
        for j in (1, 2):
            tgt = u0 * 3 ** j
            M = tgt
            p = reach_path(u0, tgt, M)
            if p:
                found.append((u0, j, p))
                break
        if len(found) >= 6:
            break
    for u0, j, p in found:
        verify_path(t, p)
        print(f"  u0={u0:4d}  ->* 3^{j}*u0={u0*3**j:5d}  in {len(p)-1} steps: {p}  VERIFIED")
    if not found:
        print("  none found up to 400")
    else:
        u0, j, p = found[0]
        print()
        print(f"CANONICAL WITNESS: u0={u0}, j={j}, cycle {p}")
        # exhibit the first three scaled copies concatenated, verified end to end
        chain = list(p)
        for s in (1, 2):
            chain += [x * 3 ** (j * s) for x in p[1:]]
        verify_path(t, chain)
        print(f"  concatenated 3 copies -> chain of {len(chain)} values, "
              f"first 20: {chain[:20]}")
        print(f"  VERIFIED end to end against tau.before (raw definition).")
        print(f"  => tau contains an infinite forcing chain, hence an infinite "
              f"strictly descending sequence.")
