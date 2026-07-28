#!/usr/bin/env python3
"""
glue.py -- combine gadget pools from PAIRWISE DISJOINT windows into an exact
representation of a target rational.

If W_1,...,W_m are legal sets living in pairwise disjoint (and hence
non-interfering) windows, their union is legal too -- every element keeps the
neighbour it had inside its own gadget -- and the reciprocal sums simply add.
With every gadget value written as a_j/D the gluing condition is the INTEGER
equation  a_1 + ... + a_m = target*D,  which is an ordinary subset-sum over
small integers and is solved here by meet-in-the-middle.

The resulting set is re-verified from scratch with fractions.Fraction before
being printed.

usage: glue.py target poolfile1 poolfile2 [poolfile3 ...]
       (target as "1" or "1/2"; pools must all share the same D)
"""
import sys
from fractions import Fraction


def load(fn):
    out = {}
    D = None
    for line in open(fn):
        t = line.split()
        if len(t) < 3:
            continue
        a, d = int(t[0]), int(t[1])
        D = d if D is None else D
        assert d == D, "pools must share D"
        U = [int(x) for x in t[2:]]
        if a not in out or len(U) < len(out[a]):
            out[a] = U
    return D, out


def main():
    target = Fraction(sys.argv[1])
    files = sys.argv[2:]
    pools = []
    D = None
    for fn in files:
        d, p = load(fn)
        if not p:
            print(f"# pool {fn} is EMPTY", file=sys.stderr)
            return 1
        D = d if D is None else D
        assert d == D
        pools.append((fn, p))
        lo, hi = min(p), max(p)
        print(f"# {fn}: {len(p)} values in [{lo}/{D}, {hi}/{D}] "
              f"= [{lo/D:.5f}, {hi/D:.5f}], elements {min(min(U) for U in p.values())}"
              f"..{max(max(U) for U in p.values())}")
    tgt = target * D
    assert tgt.denominator == 1, "target*D must be an integer"
    tgt = int(tgt)

    half = (len(pools) + 1) // 2
    left, right = pools[:half], pools[half:]

    def enumerate_sums(ps, cap=4000000):
        cur = {0: []}
        for _, p in ps:
            nxt = {}
            for s, ch in cur.items():
                for a in p:
                    v = s + a
                    if v > tgt:
                        continue
                    if v not in nxt:
                        nxt[v] = ch + [a]
                        if len(nxt) >= cap:
                            break
                if len(nxt) >= cap:
                    break
            cur = nxt
            if not cur:
                return {}
        return cur

    LS = enumerate_sums(left)
    RS = enumerate_sums(right)
    print(f"# left sums {len(LS)}, right sums {len(RS)}")
    hit = None
    for s, ch in RS.items():
        if tgt - s in LS:
            hit = LS[tgt - s] + ch
            break
    if hit is None:
        print("no combination found")
        return 1
    U = []
    for (fn, p), a in zip(pools, hit):
        U += p[a]
    U = sorted(U)
    s = sum(Fraction(1, n) for n in U)
    S = set(U)
    assert len(S) == len(U), "elements repeat across windows"
    iso = [n for n in U if (n - 1) not in S and (n + 1) not in S]
    assert not iso, f"isolated points {iso}"
    assert s == target, f"sum {s} != {target}"
    print("SOL " + " ".join(map(str, U)))
    runs, cur = [], [U[0]]
    for a, b in zip(U, U[1:]):
        if b == a + 1:
            cur.append(b)
        else:
            runs.append(cur); cur = [b]
    runs.append(cur)
    print(f"# |U|={len(U)} min={min(U)} max={max(U)} r={len(runs)} "
          f"cap={sum(len(r)//2 for r in runs)} sum={s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
