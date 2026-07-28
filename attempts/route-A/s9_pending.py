#!/usr/bin/env python3
"""
s9_pending.py -- TASK ITEM 2: the "pending unit fraction" calculus.

STATE = (S, P) where
    S  = a set of integers already placed, every maximal run of S has length >= 2
         (a partial legal set), and
    P  = a multiset of PENDING unit fractions 1/N (denominators not in S),
    with   sum_{n in S} 1/n  +  sum_{1/N in P} 1/N  =  1   at all times.

MOVES
  (M1) block-extraction  1/m -> [a,b] + 1/N   whenever  1/m - H(a,b) = 1/N exactly
       (table precomputed; the canonical member is 1/m = 1/(2m)+1/(2m+1)+1/(2m(2m+1)))
  (M2) split             1/n -> 1/(n+d) + 1/(n + n^2/d)   for every d | n^2, d <= n
  (M3) absorb            a pending 1/N with N adjacent to a run of S (N = b+1 or a-1)
       is moved into S -- the run just gets longer, S stays legal
  (M4) merge             two pendings 1/A, 1/(A+1) become the run [A,A+1]
                         (more generally a maximal consecutive set of >= 2 pendings)
  Every move must keep all denominators distinct and blocks disjoint.

FINISHED when P is empty.

usage: python3 s9_pending.py [DMAX] [DEPTH]
"""
import sys, heapq
from fractions import Fraction


def H(a, b):
    return sum((Fraction(1, n) for n in range(a, b + 1)), Fraction(0))


def build_M1_table(mmax, elt_max):
    """all (m, a, b, N) with 1/m - H(a,b) = 1/N,  b <= elt_max."""
    tab = {}
    for m in range(1, mmax + 1):
        t = Fraction(1, m)
        lst = []
        for a in range(2, elt_max):
            if Fraction(1, a) + Fraction(1, a + 1) >= t:
                continue
            s = Fraction(1, a)
            for b in range(a + 1, elt_max + 1):
                s += Fraction(1, b)
                if s >= t:
                    break
                r = t - s
                if r.numerator == 1:
                    lst.append((a, b, r.denominator))
        if lst:
            tab[m] = lst
    return tab


def splits(n):
    out = []
    nn = n * n
    for d in range(1, n):
        if nn % d == 0:
            out.append((n + d, n + nn // d))
    return out


def runs_ok(S):
    A = sorted(S)
    if not A:
        return True
    cur = [A[0]]
    for x in A[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            if len(cur) < 2:
                return False
            cur = [x]
    return len(cur) >= 2


def normalise(S, P):
    """apply M3 and M4 to exhaustion.  Returns (S,P) or None if a pending
       collides with S."""
    S = set(S)
    P = list(P)
    if any(x in S for x in P):
        return None
    if len(set(P)) != len(P):
        return None
    changed = True
    while changed:
        changed = False
        # M4: consecutive pendings
        Ps = sorted(P)
        i = 0
        while i < len(Ps):
            j = i
            while j + 1 < len(Ps) and Ps[j + 1] == Ps[j] + 1:
                j += 1
            if j > i:
                blk = Ps[i:j + 1]
                if all(x not in S for x in blk) and \
                   all(x - 1 not in S and x + 1 not in S for x in (blk[0], blk[-1])) or True:
                    for x in blk:
                        S.add(x)
                        P.remove(x)
                    changed = True
                    break
            i = j + 1
        if changed:
            continue
        # M3: pending adjacent to an existing run
        for x in list(P):
            if (x - 1) in S or (x + 1) in S:
                S.add(x)
                P.remove(x)
                changed = True
                break
    if not runs_ok(S):
        return ("partial", frozenset(S), tuple(sorted(P)))
    return ("legal", frozenset(S), tuple(sorted(P)))


def search(dmax=10 ** 7, maxdepth=9, elt_max=400, mmax=400, report=20):
    tab = build_M1_table(mmax, elt_max)
    n_m1 = sum(len(v) for v in tab.values())
    print("M1 table: %d (m,[a,b],N) triples with m<=%d, elements<=%d"
          % (n_m1, mmax, elt_max))
    ex = sorted(tab.items())[:6]
    for m, lst in ex:
        print("   1/%d = H(%d,%d) + 1/%d   (%d entries for this m)"
              % (m, lst[0][0], lst[0][1], lst[0][2], len(lst)))

    start = (frozenset(), (1,))
    seen = {start}
    stack = [(0, frozenset(), (1,))]
    found = []
    nodes = 0
    while stack:
        depth, S, P = stack.pop()
        nodes += 1
        if not P:
            if runs_ok(S) and sum((Fraction(1, n) for n in S), Fraction(0)) == 1:
                found.append(sorted(S))
                print("   *** FINISHED:", sorted(S))
                if len(found) >= report:
                    break
            continue
        if depth >= maxdepth:
            continue
        used = set(S) | set(P)
        for m in P:
            rest = list(P)
            rest.remove(m)
            # M1
            for (a, b, N) in tab.get(m, ()):
                if N > dmax or N in used:
                    continue
                blk = set(range(a, b + 1))
                if blk & used:
                    continue
                res = normalise(set(S) | blk, rest + [N])
                if res is None:
                    continue
                key = (res[1], res[2])
                if key not in seen:
                    seen.add(key)
                    stack.append((depth + 1, res[1], res[2]))
            # M2
            for (x, y) in splits(m):
                if x > dmax or y > dmax or x in used or y in used:
                    continue
                res = normalise(set(S), rest + [x, y])
                if res is None:
                    continue
                key = (res[1], res[2])
                if key not in seen:
                    seen.add(key)
                    stack.append((depth + 1, res[1], res[2]))
    print("nodes=%d states=%d finished=%d" % (nodes, len(seen), len(found)))
    return found


if __name__ == "__main__":
    D = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    search(dmax=D, maxdepth=K)
