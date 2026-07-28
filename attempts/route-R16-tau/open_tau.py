"""open_tau.py — Theorem-16 openness / forcing structure inside the comparator tau.

Claim tested (Lemma O, proved in REPORT.md sec. 4):
  In tau, u is OPEN at scale d (i.e. (u-2d, u-d, u) positionally increasing) iff,
  with v = v3(d) and context c = u mod 3^v,
      dig3(d, v) == delta*(v,c)   and   dig3(u, v) == x3(v,c)
  where x1<x2<x3 is the prio(v,c)-sorted digit list and delta* = x2-x1 mod 3.
  (plus the domain condition u - 2d >= 1.)

Claim tested (Cor O2): u is tau-open at SOME scale iff there is a level v with
  dig3(u,v) == x3(v, u mod 3^v)  and  2 * delta*(v, u mod 3^v) * 3^v < u.

Then: forcing chains.  Theorem 16(a) (valid for ANY 4-AP-free linear order, tau included)
gives u open at d  =>  u+d precedes u.  We look for long / infinite forcing chains in tau.
"""

import sys
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/attempts/route-R16-tau")
from taulib import Tau, prio_const, prio_levels, v3, dig3, top3


def open_scales_bruteforce(t, u, M=None):
    """All d>=1 with u-2d>=1 and (u-2d,u-d,u) tau-positionally increasing."""
    out = []
    for d in range(1, (u - 1) // 2 + 1):
        a, b = u - 2 * d, u - d
        if t.before(a, b) and t.before(b, u):
            out.append(d)
    return out


def open_scales_formula(t, u):
    out = []
    for d in range(1, (u - 1) // 2 + 1):
        v = v3(d)
        c = u % 3 ** v
        x1, x2, x3 = t.x123(v, c)
        ds = (x2 - x1) % 3
        if dig3(d, v) == ds and dig3(u, v) == x3:
            out.append(d)
    return out


def is_open_formula(t, u):
    """Cor O2 test."""
    v = 0
    while 3 ** v <= u:
        c = u % 3 ** v
        x1, x2, x3 = t.x123(v, c)
        ds = (x2 - x1) % 3
        if dig3(u, v) == x3 and 2 * ds * 3 ** v < u:
            return True
        v += 1
    return False


def verify(t, U=3000, name=""):
    bad = 0
    for u in range(1, U + 1):
        a = open_scales_bruteforce(t, u)
        b = open_scales_formula(t, u)
        if a != b:
            bad += 1
            if bad < 4:
                print("  MISMATCH", u, a[:8], b[:8])
        if (len(a) > 0) != is_open_formula(t, u):
            bad += 1
            print("  COR-O2 MISMATCH", u)
    print(f"  [{name}] Lemma O + Cor O2 verified on u<={U}: "
          f"{'OK' if bad == 0 else str(bad)+' MISMATCHES'}")
    return bad == 0


def forcing_step_check(t, U=2000):
    """Theorem 16(a) sanity inside tau: u open at d => u+d precedes u."""
    bad = 0
    for u in range(1, U + 1):
        for d in open_scales_formula(t, u):
            if not t.before(u + d, u):
                bad += 1
    print(f"  Theorem 16(a) inside tau verified for all u<={U}: "
          f"{'OK' if bad == 0 else str(bad)+' violations'}")
    return bad == 0


def longest_chain(t, u0, maxlen=200):
    """Greedy/BFS longest forcing chain from u0 (chain values strictly increase,
    u_{k+1} = u_k + d with d an open scale of u_k)."""
    best = [u0]
    seen = {}

    def dfs(u, path):
        nonlocal best
        if len(path) > len(best):
            best = list(path)
        if len(path) >= maxlen:
            return
        ds = open_scales_formula(t, u)
        # try large d first (fast growth) then small
        for d in sorted(ds, reverse=True):
            w = u + d
            if w in seen and seen[w] >= len(path):
                continue
            seen[w] = len(path)
            path.append(w)
            dfs(w, path)
            path.pop()
    dfs(u0, [u0])
    return best


def unbounded_chain(t, u0, steps=40, prefer="small"):
    """Follow a chain greedily for `steps` steps, choosing an open scale that keeps
    the successor open.  Returns the chain (stops if stuck)."""
    ch = [u0]
    u = u0
    for _ in range(steps):
        ds = open_scales_formula(t, u)
        if not ds:
            break
        cand = [d for d in ds if open_scales_formula(t, u + d)]
        if not cand:
            # take any step; chain will die next
            u = u + (min(ds) if prefer == "small" else max(ds))
            ch.append(u)
            break
        d = min(cand) if prefer == "small" else max(cand)
        u = u + d
        ch.append(u)
    return ch


if __name__ == "__main__":
    print("=== Lemma O (openness characterisation in tau) ===")
    tests = [
        (Tau(prio_const((0, 1, 2))), "natural (0,1,2)"),
        (Tau(prio_const((2, 1, 0))), "reversed (2,1,0)"),
        (Tau(prio_const((1, 2, 0))), "(1,2,0)"),
        (Tau(prio_levels([(0, 1, 2), (2, 0, 1), (1, 2, 0), (0, 2, 1)])), "per-level cycle"),
    ]
    import random
    rng = random.Random(7)
    PERMS = list(permutations((0, 1, 2)))
    tbl = {}

    def prio_rand(l, c):
        if (l, c) not in tbl:
            tbl[(l, c)] = PERMS[rng.randrange(6)]
        return tbl[(l, c)]
    tests.append((Tau(prio_rand), "context-dependent random"))

    for t, nm in tests:
        verify(t, U=2000, name=nm)
    print()
    print("=== Theorem 16(a) inside tau ===")
    for t, nm in tests[:3]:
        forcing_step_check(t, U=1500)
    print()
    print("=== forcing chains in tau (natural priorities) ===")
    t = Tau(prio_const((0, 1, 2)))
    for u0 in (5, 8, 17, 26, 50, 100, 242, 243, 244, 500, 728, 729, 730):
        ch = unbounded_chain(t, u0, steps=25, prefer="small")
        print(f"  u0={u0:4d}  chain len {len(ch):3d}  {ch[:9]}{' ...' if len(ch)>9 else ''}"
              f"  last={ch[-1]}")
    print()
    print("  which u are NOT tau-open at any scale (natural priorities), u<=300:")
    t = Tau(prio_const((0, 1, 2)))
    closed = [u for u in range(1, 301) if not is_open_formula(t, u)]
    print("   ", closed)
