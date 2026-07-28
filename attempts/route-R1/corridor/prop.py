"""prop.py -- polynomial-time SOUND refuter for the in-order cut system.

It performs unit propagation closed under transitivity on the order relation:

  R  :  a set of asserted facts  "u before v"  (a relation on [1..V])
  init:  u before v  whenever seg(u) < seg(v)          (the in-order layout)
  rules:
    (T)   u<v and v<w   =>  u<w                         (transitivity)
    (C1)  for a 4-AP (t1,t2,t3,t4): if three of the four links of the increasing
          chain t1<t2<t3<t4 are asserted, the fourth is asserted REVERSED;
          same for the decreasing chain t4<t3<t2<t1.
          (More generally: any chain whose links are all asserted is a violation.)
    (C2)  for x, x+d, x+2d <= V < x+3d: if two of the two links of x<x+d<x+2d are
          asserted -> contradiction; if one is asserted the other is asserted
          reversed.
  contradiction:  u before v  AND  v before u.

Every derived fact is a logical consequence of C1 & C2 & transitivity, which are
NECESSARY for a monotone-4-AP-free permutation of N with those cuts.  Hence

    prop_refute(cuts) == 'DEAD'   =>   no such permutation exists.

'ALIVE' is inconclusive (propagation is incomplete).

Implementation: bitset rows (Python ints) for the relation; O(V^2) words per closure
sweep.  Exact, no floating point.
"""

import numpy as np


def build(cuts):
    V = cuts[-1]
    seg = [0] * (V + 1)
    prev = 0
    for j, c in enumerate(cuts):
        for v in range(prev + 1, c + 1):
            seg[v] = j
        prev = c
    return V, seg


def chain_list(V):
    """All forbidden chains: C1 (both orientations) and C2."""
    out = []
    for d in range(1, (V - 1) // 3 + 1):
        for x in range(1, V - 3 * d + 1):
            q = (x, x + d, x + 2 * d, x + 3 * d)
            out.append(q)
            out.append(q[::-1])
    for d in range(1, (V - 1) // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V:
                out.append((x, x + d, x + 2 * d))
    return out


def prop_refute(cuts, max_rounds=200, return_state=False):
    V, seg = build(cuts)
    # bef[u] : bitset of v with "u before v"
    bef = [0] * (V + 1)
    for u in range(1, V + 1):
        m = 0
        for v in range(1, V + 1):
            if seg[u] < seg[v]:
                m |= (1 << v)
        bef[u] = m

    chains = chain_list(V)

    def closure():
        """Transitive closure (Warshall over bitsets). Returns False on contradiction."""
        changed = True
        while changed:
            changed = False
            for u in range(1, V + 1):
                row = bef[u]
                new = row
                m = row
                while m:
                    b = m & -m
                    k = b.bit_length() - 1
                    new |= bef[k]
                    m ^= b
                if new != row:
                    bef[u] = new
                    changed = True
        for u in range(1, V + 1):
            m = bef[u]
            while m:
                b = m & -m
                k = b.bit_length() - 1
                if bef[k] >> u & 1:
                    return False
                m ^= b
        return True

    if not closure():
        return ('DEAD', 'init-cycle') if not return_state else ('DEAD', 'init-cycle', bef)

    for rnd in range(max_rounds):
        newfacts = []
        for ch in chains:
            links = list(zip(ch, ch[1:]))
            unknown = []
            ok = True
            for a, b in links:
                if bef[a] >> b & 1:
                    continue
                if bef[b] >> a & 1:
                    ok = False       # this link is already reversed: chain dead
                    break
                unknown.append((a, b))
            if not ok:
                continue
            if not unknown:
                return ('DEAD', ('chain-forced', ch)) if not return_state else ('DEAD', ('chain-forced', ch), bef)
            if len(unknown) == 1:
                a, b = unknown[0]
                newfacts.append((b, a))   # force b before a
        if not newfacts:
            break
        prog = False
        for (a, b) in newfacts:
            if not (bef[a] >> b & 1):
                bef[a] |= (1 << b)
                prog = True
        if not prog:
            break
        if not closure():
            return ('DEAD', 'cycle') if not return_state else ('DEAD', 'cycle', bef)
    return ('ALIVE', rnd) if not return_state else ('ALIVE', rnd, bef)
