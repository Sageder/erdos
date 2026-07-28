"""forcing2.py — route R17. The FULL forced-descent digraph G* and closure machinery.

Conventions: PROBLEM.md. perm[i] = value at position i+1; pos[v] = position of value v.
`v < w` in VALUE, `v prec w` iff pos[v] < pos[w].

THE SIX FORCED DESCENTS.  They are exactly the unit propagations of the two 3-literal
clauses attached to the 4-AP (x, x+d, x+2d, x+3d):  with l_i = [x+(i-1)d prec x+id],
   no increasing 4-AP  =  (~l1 | ~l2 | ~l3),      no decreasing 4-AP  =  (l1 | l2 | l3).
Each clause yields three unit propagations, i.e. three forced prec-facts; written with
the SOURCE of the resulting descending edge called s (all conditions on out-of-range
values are vacuous, and each rule needs its mentioned values >= 1):

  (U1)  s-2d prec s-d prec s                    =>  s+d prec s      [edge s -> s+d]
  (U2)  s+d prec s+2d prec s+3d                 =>  s+d prec s      [edge s -> s+d]
  (U3)  s-d prec s   and   s+d prec s+2d        =>  s+d prec s      [edge s -> s+d]
  (D1)  s+2d prec s+d prec s                    =>  s-d prec s      [edge s -> s-d]
  (D2)  s-d prec s-2d prec s-3d                 =>  s-d prec s      [edge s -> s-d]
  (D3)  s-d prec s-2d  and  s+d prec s          =>  s-d prec s      [edge s -> s-d]

 (U1) is Theorem 16(a) of CORE.md -- the only rule used there.
 (U2): else (s, s+d, s+2d, s+3d) is an increasing monotone 4-AP.
 (U3): with x = s-d, l1 and l3 hold, so l2 must fail: else an increasing 4-AP.
 (D1): else (s+2d, s+d, s, s-d) read in increasing position order is a decreasing 4-AP.
 (D2): else (s, s-d, s-2d, s-3d) read in increasing position order is a decreasing 4-AP.
 (D3): with x = s-2d, ~l1 and ~l3 hold, so l2 must hold: else a decreasing 4-AP.

Digraph G* on the values: edge s -> t whenever one of the six rules forces t prec s.
Every edge is prec-descending, out-degree is finite => Cl_{G*}(u) subset {u} u pred(u)
is finite, |Cl_{G*}(u)| <= pos(u), and 196-YES <=> some vertex has an infinite
G*-closure.  G (Theorem 16) is the sub-digraph using rule (U1) only.

FINITE BOARDS: every rule instance mentions only finitely many values; on [1..N] we
apply an instance only when ALL mentioned values lie in [1..N].  Hence the digraph
computed on the restriction sigma_N of an infinite avoider is a SUBGRAPH of the true
one (edges are never spurious, only missing) -- so closure sizes measured on finite
boards are LOWER BOUNDS for the infinite object.  (For rule (U1) alone, openness of a
value v only involves values <= v, so G-openness is computed exactly.)
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute


def make_pos(perm):
    N = len(perm)
    pos = [0] * (N + 2)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    return pos


# ---------------------------------------------------------------- openness (rule U1)

def open_scales(pos, u, N):
    """d >= 1 with u-2d >= 1 and pos[u-2d] < pos[u-d] < pos[u]  (u OPEN at scale d)."""
    return [d for d in range(1, (u - 1) // 2 + 1)
            if pos[u - 2 * d] < pos[u - d] < pos[u]]


def is_open(pos, u, N):
    return bool(open_scales(pos, u, N))


# ---------------------------------------------------------------- the four rules

def edges_U1(pos, s, N):
    """s -> s+d because (s-2d, s-d, s) is positionally increasing."""
    out = []
    for d in range(1, (s - 1) // 2 + 1):
        if s + d <= N and pos[s - 2 * d] < pos[s - d] < pos[s]:
            out.append(s + d)
    return out


def edges_U2(pos, s, N):
    """s -> s+d because (s+d, s+2d, s+3d) is positionally increasing."""
    out = []
    d = 1
    while s + 3 * d <= N:
        if pos[s + d] < pos[s + 2 * d] < pos[s + 3 * d]:
            out.append(s + d)
        d += 1
    return out


def edges_D1(pos, s, N):
    """s -> s-d because (s+2d, s+d, s) is positionally increasing (dec 3-AP)."""
    out = []
    d = 1
    while s + 2 * d <= N:
        if s - d >= 1 and pos[s + 2 * d] < pos[s + d] < pos[s]:
            out.append(s - d)
        d += 1
    return out


def edges_D2(pos, s, N):
    """s -> s-d because (s-d, s-2d, s-3d) is positionally increasing (dec 3-AP)."""
    out = []
    for d in range(1, (s - 1) // 3 + 1):
        if pos[s - d] < pos[s - 2 * d] < pos[s - 3 * d]:
            out.append(s - d)
    return out


def edges_U3(pos, s, N):
    """s -> s+d because (s-d prec s) and (s+d prec s+2d)."""
    out = []
    for d in range(1, s):
        if s + 2 * d <= N and pos[s - d] < pos[s] and pos[s + d] < pos[s + 2 * d]:
            out.append(s + d)
    return out


def edges_D3(pos, s, N):
    """s -> s-d because (s-d prec s-2d) and (s+d prec s)."""
    out = []
    for d in range(1, (s - 1) // 2 + 1):
        if s + d <= N and pos[s - d] < pos[s - 2 * d] and pos[s + d] < pos[s]:
            out.append(s - d)
    return out


RULES = {'U1': edges_U1, 'U2': edges_U2, 'U3': edges_U3,
         'D1': edges_D1, 'D2': edges_D2, 'D3': edges_D3}
ALLRULES = ('U1', 'U2', 'U3', 'D1', 'D2', 'D3')


def out_edges(pos, s, N, rules=ALLRULES):
    out = set()
    for r in rules:
        out.update(RULES[r](pos, s, N))
    return out


def closure(pos, u0, N, rules=ALLRULES):
    seen = {u0}
    stack = [u0]
    while stack:
        s = stack.pop()
        for t in out_edges(pos, s, N, rules):
            if 1 <= t <= N and t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def longest_chain(pos, u0, N, rules=ALLRULES):
    """Length (#edges) of the longest G-path from u0; the digraph is acyclic (all
    edges strictly decrease pos), so a memoised DFS terminates."""
    memo = {}

    def go(s):
        if s in memo:
            return memo[s]
        memo[s] = 0  # guard (acyclic, so never revisited on a live path)
        best = 0
        for t in out_edges(pos, s, N, rules):
            if 1 <= t <= N:
                best = max(best, 1 + go(t))
        memo[s] = best
        return best

    return go(u0)


# ---------------------------------------------------------------- spines

def records(pos, N):
    """value-records: w s.t. every value placed before w is smaller (Lemma 11)."""
    out = []
    best = 0
    perm = [0] * (N + 1)
    for v in range(1, N + 1):
        perm[pos[v]] = v
    for i in range(1, N + 1):
        v = perm[i]
        if v > best:
            out.append(v)
            best = v
    return out


def grounded(pos, N):
    """g s.t. pos[g] > pos[v] for all v < g."""
    out = []
    best = 0
    for g in range(1, N + 1):
        if pos[g] > best:
            out.append(g)
        best = max(best, pos[g])
    return out


# ---------------------------------------------------------------- validation

def verify_rules(perm, brute=False):
    """Check every instance of the six rules on a 4-AP-free board: each derived
    edge s -> t must really satisfy pos[t] < pos[s].  Returns #instances checked."""
    N = len(perm)
    pos = make_pos(perm)
    n = 0
    for s in range(1, N + 1):
        for r in ALLRULES:
            for t in RULES[r](pos, s, N):
                assert 1 <= t <= N
                assert pos[t] < pos[s], ("RULE VIOLATION", r, perm, s, t)
                n += 1
    return n


if __name__ == "__main__":
    from itertools import permutations
    # (0) cross-validate the trusted checker against brute force on random boards
    import random
    rng = random.Random(17)
    for _ in range(400):
        n = rng.randint(4, 8)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert has_monotone_kap_pos(p, 4) == has_monotone_kap_brute(p, 4)
    print("checker cross-validation OK")

    # (1) exhaustive rule verification on all 4-AP-free boards, N <= 9
    for N in range(4, 10):
        cnt = inst = 0
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_pos(p, 4):
                continue
            cnt += 1
            inst += verify_rules(list(p))
        print(f"N={N}: {cnt} avoiders, {inst} rule instances, ALL edges prec-descending")
