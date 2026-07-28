"""cond2.py -- exact checkers for condition (ii) of the class architecture.

Setting (CORE Props 29-31, Conjecture R21-C):  c(v) = j(v) + t(v) with j(v) = floor(log_b v)
and t : N -> Z>=0.  Condition (ii): for every 4-AP (x, x+d, x+2d, x+3d) with all four terms
in [1..N], the class sequence (c(x), c(x+d), c(x+2d), c(x+3d)) is neither strictly
increasing nor strictly decreasing.

THREE independent implementations, cross-validated against each other:
  * violations_literal   -- literal definition, pure-python double loop over (d, x).
  * violations_numpy     -- vectorised over x for each d (different code path, numpy ints).
  * violations_caseanal  -- case analysis on the block deltas (D1,D2,D3) as in CORE
                            Lemma 34 / Prop 37; independent of the direct c-comparison.
Additionally `coarsening_sanity` cross-validates against the TRUSTED checker
experiments/apcheck.py through Remark 31: the geometric coarsening of any monotone-4-AP-free
permutation satisfies (ii).

Exact integer arithmetic throughout (no floats anywhere).
"""

import sys
import numpy as np

sys.path.insert(0, '/home/user/erdos/experiments')


def blk(v, b):
    """floor(log_b v) by exact integer arithmetic."""
    j, p = 0, 1
    while p * b <= v:
        p *= b
        j += 1
    return j


def blocks(N, b):
    """array J with J[v] = floor(log_b v) for v in 1..N (J[0] unused)."""
    J = np.zeros(N + 1, dtype=np.int64)
    for v in range(1, N + 1):
        J[v] = blk(v, b)
    return J


# ---------------------------------------------------------------- implementation 1
def violations_literal(t, N, b, limit=None):
    """t: list/array with t[v] for v in 1..N. Returns list of (x, d, orientation, cs)."""
    c = [0] * (N + 1)
    for v in range(1, N + 1):
        c[v] = blk(v, b) + int(t[v])
    out = []
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            a, bb, cc, dd = c[x], c[x + d], c[x + 2 * d], c[x + 3 * d]
            if a < bb < cc < dd:
                out.append((x, d, 'inc', (a, bb, cc, dd)))
                if limit and len(out) >= limit:
                    return out
            elif a > bb > cc > dd:
                out.append((x, d, 'dec', (a, bb, cc, dd)))
                if limit and len(out) >= limit:
                    return out
    return out


# ---------------------------------------------------------------- implementation 2
def violations_numpy(t, N, b, limit=None):
    J = blocks(N, b)
    tt = np.zeros(N + 1, dtype=np.int64)
    tt[1:N + 1] = np.asarray(t[1:N + 1], dtype=np.int64)
    c = J + tt
    out = []
    for d in range(1, N // 3 + 1):
        top = N - 3 * d
        if top < 1:
            break
        xs = np.arange(1, top + 1)
        c0, c1, c2, c3 = c[xs], c[xs + d], c[xs + 2 * d], c[xs + 3 * d]
        inc = (c0 < c1) & (c1 < c2) & (c2 < c3)
        dec = (c0 > c1) & (c1 > c2) & (c2 > c3)
        for x in xs[inc]:
            out.append((int(x), d, 'inc', tuple(int(c[x + i * d]) for i in range(4))))
        for x in xs[dec]:
            out.append((int(x), d, 'dec', tuple(int(c[x + i * d]) for i in range(4))))
        if limit and len(out) >= limit:
            return out[:limit]
    return out


# ---------------------------------------------------------------- implementation 3
def violations_caseanal(t, N, b, limit=None):
    """Case analysis on block deltas: strictly increasing  <=>  for every i,
    t_i - t_{i-1} > -D_i ;  strictly decreasing <=> t_i - t_{i-1} < -D_i.
    Never forms c explicitly."""
    J = [0] * (N + 1)
    for v in range(1, N + 1):
        J[v] = blk(v, b)
    out = []
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u = (x, x + d, x + 2 * d, x + 3 * d)
            D = [J[u[i + 1]] - J[u[i]] for i in range(3)]
            T = [int(t[v]) for v in u]
            if all(T[i + 1] - T[i] > -D[i] for i in range(3)):
                out.append((x, d, 'inc', tuple(J[v] + int(t[v]) for v in u)))
            elif all(T[i + 1] - T[i] < -D[i] for i in range(3)):
                out.append((x, d, 'dec', tuple(J[v] + int(t[v]) for v in u)))
            if limit and len(out) >= limit:
                return out
    return out


def satisfies_ii(t, N, b):
    return len(violations_numpy(t, N, b, limit=1)) == 0


def first_violation(t, N, b):
    v = violations_numpy(t, N, b, limit=1)
    return v[0] if v else None


# ---------------------------------------------------------------- tameness measurement
def tame_report(t, N, b, Q=12, tail_frac=0.5):
    """For each AP P = {r, r+q, ...} with q <= Q inside [1..N], report
       * ndesc = number of steps n with c(p_{n+1}) < c(p_n)  (a 'c-descent')
       * maxrun = longest run of consecutive non-descending steps
       * ndesc_tail / maxrun_tail over the tail (last tail_frac of P)
       * tconst  = whether t is constant on the tail of P
    A progression with no c-descent in its tail is TAME on the tested window.
    """
    J = [blk(v, b) for v in range(N + 1)]
    c = [0] + [J[v] + int(t[v]) for v in range(1, N + 1)]
    rows = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 6:
                continue
            s0 = int(len(P) * (1 - tail_frac))
            desc = [n for n in range(len(P) - 1) if c[P[n + 1]] < c[P[n]]]
            desc_tail = [n for n in desc if n >= s0]
            # longest run without a descent, in the tail
            marks = [s0 - 1] + desc_tail + [len(P) - 1]
            maxrun = max(marks[i + 1] - marks[i] for i in range(len(marks) - 1))
            tset = set(int(t[v]) for v in P[s0:])
            rows.append(dict(q=q, r=r, n=len(P), ndesc=len(desc), ndesc_tail=len(desc_tail),
                             maxrun_tail=maxrun, tconst_tail=(len(tset) == 1)))
    return rows


def worst_tame(rows):
    """The most 'tame-looking' progression: max maxrun_tail, tie-broken by fewest descents."""
    return max(rows, key=lambda r: (r['maxrun_tail'], -r['ndesc_tail']))


# ---------------------------------------------------------------- cross-validation
def _cross_validate():
    import random
    rng = random.Random(196)
    for trial in range(200):
        N = rng.randint(20, 90)
        b = rng.choice([3, 4, 5])
        T = rng.choice([1, 1, 2, 3])
        t = [0] * (N + 1)
        for v in range(1, N + 1):
            t[v] = rng.randint(0, T)
        a = sorted(violations_literal(t, N, b))
        c = sorted(violations_numpy(t, N, b))
        e = sorted(violations_caseanal(t, N, b))
        assert a == c == e, (N, b, T, len(a), len(c), len(e))
    print("cond2: 3 implementations agree on 200 random instances  OK")


def coarsening_sanity(Ns=(20, 40, 60), b=3, seed=7):
    """Remark 31 cross-check against the TRUSTED checker experiments/apcheck.py.

    For a monotone-4-AP-free permutation sigma of [1..N], the geometric coarsening
    g(v) := j  where pos(v) in [b^j, b^{j+1})   satisfies condition (ii)
    (a strictly monotone class sequence along a 4-AP would make pos monotone along it).
    We build sigma with the parity recursion (3-AP-free, hence 4-AP-free), confirm
    4-AP-freeness with apcheck's *trusted* checker, then confirm that our own
    condition-(ii) machinery reports zero violations for the class function g.
    Note g is NOT of the form floor(log_b v)+t with t>=0, so we test the raw
    class-sequence predicate (the same predicate cond2 implements).
    """
    from apcheck import has_monotone_kap_pos, has_monotone_kap_brute

    def parity_perm(n):
        if n <= 1:
            return [1] * n
        odds = parity_perm((n + 1) // 2)
        evens = parity_perm(n // 2)
        return [2 * x - 1 for x in odds] + [2 * x for x in evens]

    ok = True
    for N in Ns:
        perm = parity_perm(N)
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "parity perm should be 4-AP-free"
        if N <= 9:
            assert has_monotone_kap_brute(perm, 4) == has_monotone_kap_pos(perm, 4)
        pos = [0] * (N + 1)
        for i, v in enumerate(perm):
            pos[v] = i + 1
        g = [0] * (N + 1)
        for v in range(1, N + 1):
            g[v] = blk(pos[v], b)
        bad = []
        for d in range(1, N // 3 + 1):
            for x in range(1, N - 3 * d + 1):
                s = [g[x + i * d] for i in range(4)]
                if s[0] < s[1] < s[2] < s[3] or s[0] > s[1] > s[2] > s[3]:
                    bad.append((x, d, s))
        print(f"  coarsening sanity N={N} b={b}: 4-AP-free={not has_monotone_kap_pos(perm,4)}, "
              f"(ii)-violations of the coarsening = {len(bad)}")
        ok = ok and not bad
    print("cond2: Remark-31 coarsening sanity", "OK" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    _cross_validate()
    coarsening_sanity()
