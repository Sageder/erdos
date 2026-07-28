"""
AUDIT 5b: independent EXACT decision procedure for  Phi_q(S) >= T,
by forward Pareto dynamic programming with recursive (wreath-product) canonicalisation.
Shares no code path with M_audit_phi.py's branch-and-bound beyond the pool construction.

Soundness of the two reductions used:
 * CAPPING at d = T*K - base*K: value above d on a leaf is never useful, and the reachable
   future increments do not depend on the current state, so capping preserves feasibility.
 * CANONICALISATION: the set of future placements is invariant under Aut(q-ary tree of depth J);
   the canonical form is obtained by recursively canonicalising the q subtrees and sorting them.
 * DOMINANCE: if canon(u) >= canon(v) componentwise then anything reachable from v is reachable
   from u, so v may be discarded.
"""
import sys, os, time
from fractions import Fraction
from math import gcd
from sympy import isprime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M_audit_phi import pool, phi_q_at_least, nu, divisors


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def make_canon(q, J):
    def canon(v):
        if len(v) == 1:
            return v
        n = len(v) // q
        parts = sorted(canon(v[c * n:(c + 1) * n]) for c in range(q))
        out = ()
        for p in parts:
            out += p
        return out
    return canon


def feasible(S, q, T, cap_states=3_000_000, verbose=False):
    J = max(nu(m, q) for m in S)
    F = q ** J
    K = lcm(S) * q ** J
    base = sum(K // m for m in S if m % q != 0)
    items = sorted([(q ** nu(m, q) * K // m, nu(m, q)) for m in S if m % q == 0], reverse=True)
    d = T * K - base
    if d <= 0:
        return True
    if not items:
        return False
    d = int(d)
    canon = make_canon(q, J)
    cur = {canon(tuple([0] * F))}
    full = tuple([d] * F)
    n = len(items)
    sufw = [0] * (n + 1)
    sufc = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        sufw[i] = sufw[i + 1] + items[i][0]
        sufc[i] = sufc[i + 1] + items[i][0] * q ** (J - items[i][1])
    for i, (w, j) in enumerate(items):
        blk = q ** (J - j)
        nxt = set()
        for v in cur:
            for b in range(q ** j):
                nv = list(v)
                for t in range(b * blk, (b + 1) * blk):
                    x = nv[t] + w
                    nv[t] = d if x > d else x
                if sum(d - x for x in nv) > sufc[i + 1]:
                    continue
                if max(d - x for x in nv) > sufw[i + 1]:
                    continue
                nxt.add(canon(tuple(nv)))
        if full in nxt:
            return True
        st = sorted(nxt, key=lambda v: -sum(v))
        keep = []
        for v in st:
            if not any(all(u[k] >= v[k] for k in range(F)) for u in keep):
                keep.append(v)
        cur = set(keep)
        if verbose:
            print(f"      item {i+1}/{n} w={w} lvl={j}: {len(nxt)} raw -> {len(cur)} pareto",
                  flush=True)
        if not cur:
            return False
        if len(cur) > cap_states:
            raise MemoryError(f"state explosion {len(cur)}")
    return full in cur


if __name__ == "__main__":
    LHs = [int(x) for x in sys.argv[1:]] or [27720]
    T = Fraction(2)
    for LH in LHs:
        S = pool(LH)
        B = sum(Fraction(1, m) for m in S)
        print(f"L_H = {LH} (L_E = {2*LH})  |S|={len(S)}  H-budget={float(B):.6f}", flush=True)
        for q in sorted({p for p in range(2, 100) if isprime(p) and LH % p == 0}):
            t = time.time()
            bb, best = phi_q_at_least(S, q, T)
            tb = time.time() - t
            t = time.time()
            try:
                dp = feasible(S, q, T)
            except MemoryError as e:
                dp = None
            td = time.time() - t
            flag = "AGREE" if dp == bb else ("n/a" if dp is None else "*** DISAGREE ***")
            print(f"   q={q:<3} B&B={str(bb):<5} ({tb:.2f}s)   independentDP={str(dp):<5} "
                  f"({td:.2f}s)   {flag}", flush=True)
