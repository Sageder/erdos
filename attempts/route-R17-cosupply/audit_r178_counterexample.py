"""Counterexample to the explicit bound claimed in Lemma R17.8:

   "Lemma 16.1's scale is <= m * pos(w) * 2^{pos(w + m*pos(w))}"

Lemma 16.1 is a statement about ANY permutation of N.  We build an explicit
permutation of N (order type omega, bijective) with m = 1, w = 1 for which
   pos(1) = 2,  pos(1 + 1*pos(1)) = pos(3) = 3   =>  claimed bound = 1*2*2^3 = 16
yet the least e with (1, 1+e, 1+2e) positionally increasing is far above 16.

Reason the proof fails: the bound m*pos(w) only produces ONE step e0 with w prec w+e0;
the doubling argument of R17.8 needs w prec w+2^k e0 for EVERY k, which is only
guaranteed for e0 > E(w) = max{v>w : v prec w} - w, and E(w) is NOT bounded by any
function of pos(w).
"""
import sys

BOUND_TARGET = 400          # make ALL e <= BOUND_TARGET fail


def build(EMAX):
    """positions 1..: value 5 at pos1, value 1 at pos2, value 3 at pos3, then a
    topological order making pos(1+2e) < pos(1+e) for every e in [1,EMAX]\\{2,4}."""
    order = [5, 1, 3]
    placed = set(order)
    # constraint graph: for each e, need pos(1+2e) < pos(1+e)   (e != 4: 1+e=5 at pos 1)
    edges = {}   # a -> list of b meaning a must come before b
    nodes = set()
    for e in range(1, EMAX + 1):
        a, b = 1 + 2 * e, 1 + e
        if b == 5:          # (1,5,9) already killed since pos(5)=1 < pos(1)=2
            continue
        if a == 5:          # pos(5)=1 is already before everything
            continue
        edges.setdefault(a, []).append(b)
        nodes.add(a); nodes.add(b)
    nodes -= placed
    # topological sort (a before b)
    indeg = {v: 0 for v in nodes}
    for a, bs in edges.items():
        for b in bs:
            if a in nodes and b in nodes:
                indeg[b] += 1
    from collections import deque
    q = deque(sorted(v for v in nodes if indeg[v] == 0))
    out = []
    while q:
        v = q.popleft()
        out.append(v)
        for b in edges.get(v, []):
            if b in indeg:
                indeg[b] -= 1
                if indeg[b] == 0:
                    q.append(b)
    assert len(out) == len(nodes), "cycle in constraints"
    order += out
    placed |= set(out)
    # fill in every remaining natural number in increasing order (order type omega)
    v = 1
    filler = []
    M = 4 * EMAX + 20
    for v in range(1, M):
        if v not in placed:
            filler.append(v)
    order += filler
    return order


def least_increasing_e(order, w=1, cap=None):
    pos = {v: i + 1 for i, v in enumerate(order)}
    cap = cap or (max(order) - w) // 2
    for e in range(1, cap + 1):
        if w + 2 * e not in pos:
            break
        if pos[w] < pos[w + e] < pos[w + 2 * e]:
            return e
    return None


if __name__ == "__main__":
    for EMAX in (16, 50, 400):
        order = build(EMAX)
        pos = {v: i + 1 for i, v in enumerate(order)}
        assert len(set(order)) == len(order), "not injective"
        w = 1
        P = pos[1]
        e0 = 1 * P                    # m * pos(w)
        claimed = 1 * P * 2 ** pos[w + e0]
        least = least_increasing_e(order, 1, cap=EMAX)
        print(f"EMAX={EMAX}: pos(1)={P}, pos(1+m*pos(w))=pos({w+e0})={pos[w+e0]}, "
              f"claimed bound = {claimed}; least e with (1,1+e,1+2e) increasing "
              f"among e<={EMAX}: {least}")
