"""
ADVERSARIAL AUDIT 5b: a SECOND, structurally different exact decision procedure for
   "is there an assignment with min_r F_q(r) >= T ?"
so that the KILL verdicts of M_audit_phi.py's branch-and-bound can be confirmed or refuted
by an algorithm that shares no logic with it.

METHOD (forward Pareto dynamic programming, integer arithmetic):
  * scale everything by K = lcm of the moduli so all weights are integers;
  * an item at level j is placed at one of q^j nodes; it adds w to the q^{J-j} leaves below;
  * CAP each leaf's accumulated value at d = T*K - base*K (excess above d is never useful),
    so a state is a vector in {0..d}^{q^J};
  * keep only Pareto-maximal states (componentwise dominance) -- valid because the set of
    reachable future increments does not depend on the current state;
  * canonicalise each state under the automorphism group of the q-ary tree (which permutes
    leaves while preserving every block), again valid since the future options are invariant.
  * feasible  <=>  the all-d state is reachable.

A third, hand-checkable necessary condition is also implemented:
  CAPPED AGGREGATE TEST.  For every leaf r, sum over items covering r of min(w_i, d) >= d.
  Summing over any set R of leaves:  sum_i min(w_i,d) * c_i(R) >= d*|R|, where c_i(R) is the
  largest number of leaves of R inside one level-j_i block.  Violation => infeasible.
"""
import sys, os, itertools
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


def build(S, q, T):
    J = max(nu(m, q) for m in S)
    K = lcm(S) * q ** J
    base = sum(K // m for m in S if m % q != 0)          # scaled
    items = []
    for m in S:
        j = nu(m, q)
        if j >= 1:
            items.append((q ** j * K // m, j))
    d = T * K - base
    return J, K, base, items, d


def capped_aggregate(S, q, T, Rs=None):
    """returns True if the capped-aggregate necessary condition is VIOLATED (=> infeasible)."""
    J, K, base, items, d = build(S, q, T)
    if d <= 0:
        return False
    F = q ** J
    tests = []
    tests.append(tuple(range(F)))                       # all leaves
    if Rs:
        tests.extend(Rs)
    # also: one leaf from each level-j block, for each j
    for j in range(1, J + 1):
        R = tuple(b * q ** (J - j) for b in range(q ** j))
        tests.append(R)
    for R in tests:
        Rs_ = set(R)
        tot = 0
        for w, j in items:
            blk = q ** (J - j)
            c = max(len(Rs_ & set(range(b * blk, (b + 1) * blk))) for b in range(q ** j))
            tot += min(w, d) * c
        if tot < d * len(R):
            return True
    return False


def automorphisms(q, J):
    """all leaf permutations induced by Aut of the complete q-ary tree of depth J."""
    if J == 0:
        return [(0,)]
    sub = automorphisms(q, J - 1)
    n = q ** (J - 1)
    out = []
    for perm_root in itertools.permutations(range(q)):
        for choice in itertools.product(sub, repeat=q):
            p = [0] * (q ** J)
            for c in range(q):
                tgt = perm_root[c]
                for x in range(n):
                    p[c * n + x] = tgt * n + choice[c][x]
            out.append(tuple(p))
    return out


def feasible_dp(S, q, T, state_cap=4_000_000, verbose=False):
    J, K, base, items, d = build(S, q, T)
    F = q ** J
    if d <= 0:
        return True
    items.sort(key=lambda t: -t[0])
    auts = automorphisms(q, J)
    if verbose:
        print(f"      DP: J={J} fibers={F} items={len(items)} |Aut|={len(auts)} d={d}")

    def canon(v):
        return min(tuple(v[p[i]] for i in range(F)) for p in auts)

    def dominated_prune(states):
        st = sorted(states, key=lambda v: -sum(v))
        keep = []
        for v in st:
            ok = True
            for u in keep:
                if all(u[i] >= v[i] for i in range(F)):
                    ok = False
                    break
            if ok:
                keep.append(v)
        return keep

    cur = {canon(tuple([0] * F))}
    remaining = list(items)
    for idx, (w, j) in enumerate(items):
        blk = q ** (J - j)
        nxt = set()
        for v in cur:
            for b in range(q ** j):
                nv = list(v)
                for t in range(b * blk, (b + 1) * blk):
                    nv[t] = min(d, nv[t] + w)
                nxt.add(canon(tuple(nv)))
        # feasibility short-circuit
        full = tuple([d] * F)
        if full in nxt:
            return True
        # upper bound prune: drop states that cannot reach all-d with the remaining items
        rem_w = sum(x for x, _ in items[idx + 1:])
        rem_cov = sum(x * q ** (J - jj) for x, jj in items[idx + 1:])
        pruned = []
        for v in nxt:
            need = sum(d - x for x in v)
            if need > rem_cov:
                continue
            if max(d - x for x in v) > rem_w:
                continue
            pruned.append(v)
        cur = set(dominated_prune(pruned))
        if verbose:
            print(f"        after item {idx+1}/{len(items)} (w={w},lvl={j}): {len(cur)} states")
        if len(cur) > state_cap:
            raise MemoryError("state explosion")
        if not cur:
            return False
    return tuple([d] * F) in cur


def audit(LH_list, T=Fraction(2), qs=None, verbose=False):
    for LH in LH_list:
        S = pool(LH)
        B = sum(Fraction(1, m) for m in S)
        print(f"L_H = {LH} (L_E = {2*LH})  |S| = {len(S)}  H-budget = {float(B):.6f}")
        for q in sorted({p for p in range(2, 100) if isprime(p) and LH % p == 0}):
            if qs and q not in qs:
                continue
            bb, best = phi_q_at_least(S, q, T)
            cap = capped_aggregate(S, q, T)
            try:
                dp = feasible_dp(S, q, T, verbose=verbose)
                dps = str(dp)
            except (MemoryError, RecursionError) as e:
                dp, dps = None, f"n/a ({e})"
            agree = "AGREE" if (dp is not None and bb is not None and dp == bb) else "?"
            print(f"   q={q:<3} B&B feasible={bb}   independent DP feasible={dps}   "
                  f"capped-aggregate refutes={cap}   {agree}")
            if dp is not None and bb is not None and dp != bb:
                print("   *** DISAGREEMENT -- one of the two solvers is WRONG ***")


if __name__ == "__main__":
    args = [int(x) for x in sys.argv[1:]] or [27720]
    audit(args, verbose=True)
