"""r16lib.py — Route R16: tau-repair via graded override schedules.

Object of study: linear orders on N of the form  u < w  iff  (g(u), taukey(u)) <_lex
(g(w), taukey(w)), where
  * g : N -> Z is a "generation" / promotion-time function with finite fibers
    (=> order type omega, CORE.md Lemma 1: predecessors of v are a subset of the
    finite set {w : g(w) <= g(v)}),
  * taukey is the generalized base-3 priority comparator tau* (R3 Lemma T, extended
    here to context-dependent priorities pr_{l,c}: compare u,w at the lowest base-3
    digit level l where they differ, using a priority permutation that may depend on
    l AND on the common digits below l (= u mod 3^l = w mod 3^l)).

Facts used (proofs in REPORT.md):
  * tau* kills all monotone 4-APs on every subset (Lemma T*, same cycle proof:
    all four terms of a 4-AP share digits < v3(d), so all three adjacent pairs are
    compared at level v3(d) with the SAME priority; digits cycle a, a+delta, a+2delta, a).
  * For graded orders the fate of a 4-AP is decided by the rule table:
    with mu_k = cmp(g_{k-1}, g_k) in {<,=,>} and s_k = tau*-sign of adjacent pair k,
    final sign sigma_k = + if mu_k is '<', - if '>', s_k if '='.
    DEAD-inc iff all sigma_k = +;  DEAD-dec iff all sigma_k = -.
    Since (s_1,s_2,s_3) always has >=1 plus and >=1 minus (cycle argument), all-'='
    words are safe; words containing both '<' and '>' are safe; danger is exactly
    monotone-compatible mu with cooperating tau-signs at the '=' slots.

All arithmetic exact (python ints; numpy int64 only for position scans, M <= 10^6).
"""

import sys
import numpy as np

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute  # validated checkers

# ---------------------------------------------------------------- digit utilities


def v3(n):
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def digit3(n, l):
    return (n // 3 ** l) % 3


def digits3(n):
    d = []
    while n:
        d.append(n % 3)
        n //= 3
    return d  # low to high


def len3(n):
    return len(digits3(n))


# ---------------------------------------------------------------- the graded order


class GradedTauOrder:
    """Order = lex on (g(n), taukey(n)).  Subclasses / instances supply:
       gfun(n) -> int (generation), prio(l, c) -> permutation p of (0,1,2) meaning
       priority rank p[digit] at level l with context c = n mod 3^l (shared digits).
    """

    def __init__(self, gfun, prio=None, depth=16, name="graded"):
        self.gfun = gfun
        # prio(l, c): default natural priorities (0,1,2) at every level
        self.prio = prio if prio is not None else (lambda l, c: (0, 1, 2))
        self.depth = depth
        self.name = name

    # -- tau* key of n: tuple of priority ranks of digits, low level first.
    def taukey(self, n):
        w = []
        m = n
        c = 0  # context = digits below current level, as an integer
        p3 = 1
        for l in range(self.depth):
            pr = self.prio(l, c)
            dig = m % 3
            w.append(pr[dig])
            c += dig * p3
            p3 *= 3
            m //= 3
        return tuple(w)

    def key(self, n):
        return (self.gfun(n),) + self.taukey(n) + (n,)

    def restriction(self, M):
        """Values 1..M in position order (= the induced permutation of [1..M])."""
        return sorted(range(1, M + 1), key=self.key)

    # -- tau*-sign of the ordered pair (u,w), u != w: +1 if u before w under tau* alone.
    def tausign(self, u, w):
        l = v3(abs(w - u)) if u != w else None
        assert u != w
        # first differing digit level = v3(w-u)
        c = u % 3 ** l
        pr = self.prio(l, c)
        du, dw = digit3(u, l), digit3(w, l)
        assert du != dw
        return 1 if pr[du] < pr[dw] else -1


# ---------------------------------------------------------------- witness scanning


def find_mono4_all(perm, cap=100000):
    """All (x, d, orient) monotone 4-APs of a permutation of [1..M]; exact."""
    M = len(perm)
    pos = np.empty(M + 1, dtype=np.int64)
    pos[np.asarray(perm, dtype=np.int64)] = np.arange(M, dtype=np.int64)
    wits = []
    for d in range(1, (M - 1) // 3 + 1):
        top = M - 3 * d
        if top < 1:
            break
        p0 = pos[1 : top + 1]
        p1 = pos[1 + d : top + d + 1]
        p2 = pos[1 + 2 * d : top + 2 * d + 1]
        p3_ = pos[1 + 3 * d : top + 3 * d + 1]
        inc = (p0 < p1) & (p1 < p2) & (p2 < p3_)
        dec = (p0 > p1) & (p1 > p2) & (p2 > p3_)
        for orient, mask in ((1, inc), (-1, dec)):
            if mask.any():
                for xi in np.nonzero(mask)[0]:
                    wits.append((int(xi) + 1, d, orient))
                    if len(wits) >= cap:
                        return wits
    return wits


def min_kill(perm):
    """Minimal max-term x+3d over all witnesses; None if clean."""
    wits = find_mono4_all(perm, cap=1)
    if not wits:
        return None
    # find_mono4_all scans d ascending then x ascending; not minimal max-term.
    # do a dedicated scan by max-term:
    M = len(perm)
    pos = {v: i for i, v in enumerate(perm)}
    for top in range(4, M + 1):
        for d in range(1, (top - 1) // 3 + 1):
            x = top - 3 * d
            if x < 1:
                break
            ps = [pos[x + k * d] for k in range(4)]
            if ps[0] < ps[1] < ps[2] < ps[3] or ps[0] > ps[1] > ps[2] > ps[3]:
                return top
    return None


# ---------------------------------------------------------------- classification


def classify_witness(order, x, d, orient):
    """Return a dict describing why (x,d,orient) died, for a GradedTauOrder."""
    terms = [x + k * d for k in range(4)]
    v = v3(d)
    a = digit3(x, v)
    delta = digit3(d, v)
    e = d // 3 ** v
    g = [order.gfun(t) for t in terms]
    mu = []
    for k in range(3):
        mu.append("<" if g[k] < g[k + 1] else (">" if g[k] > g[k + 1] else "="))
    s = [order.tausign(terms[k], terms[k + 1]) for k in range(3)]
    # rule-table prediction
    sig = []
    for k in range(3):
        sig.append(1 if mu[k] == "<" else (-1 if mu[k] == ">" else s[k]))
    pred = 1 if all(t == 1 for t in sig) else (-1 if all(t == -1 for t in sig) else 0)
    # mode label
    if all(m == "<" for m in mu) or all(m == ">" for m in mu):
        mode = "G-MONO"  # generations strictly monotone along AP
    elif "=" in mu and (("<" in mu) or (">" in mu)):
        mode = "G-TIE"  # monotone-compatible with tau cooperation at ties
    elif all(m == "=" for m in mu):
        mode = "G-FLAT"  # should be impossible for tau* internals
    else:
        mode = "G-MIX"  # should be impossible (mixed <,> is safe)
    single = e in (1, 2)
    return dict(
        x=x, d=d, orient=orient, terms=terms, v=v, a=a, delta=delta, e=e,
        g=g, mu="".join(mu), s=tuple(s), pred=pred, mode=mode, single_trit=single,
        lens=[len3(t) for t in terms],
    )


def diagnose(order, perm, wits, kmax=8):
    """Classify the first witnesses (sorted by max-term); verify rule table."""
    out = []
    by_top = sorted(wits, key=lambda w: (w[0] + 3 * w[1], w[1]))
    for (x, d, o) in by_top[:kmax]:
        c = classify_witness(order, x, d, o)
        ok = "OK" if c["pred"] == o else "!!RULE-TABLE-MISMATCH"
        out.append(
            f"  ({x},{d},{'inc' if o == 1 else 'dec'}) terms={c['terms']} v={c['v']} "
            f"(a,delta,e)=({c['a']},{c['delta']},{c['e']}) g={c['g']} mu={c['mu']} "
            f"s={c['s']} mode={c['mode']} single={c['single_trit']} {ok}"
        )
    return "\n".join(out)


def mode_histogram(order, wits, sample=4000):
    import collections
    h = collections.Counter()
    step = max(1, len(wits) // sample)
    for (x, d, o) in wits[::step]:
        c = classify_witness(order, x, d, o)
        h[(c["mode"], "inc" if o == 1 else "dec", "1trit" if c["single_trit"] else "multi")] += 1
        if c["pred"] != o:
            h[("RULE-TABLE-MISMATCH",)] += 1
    return h


# ---------------------------------------------------------------- verdict runner


def verdict(order, M=10000, kmax=8, quickM=1200):
    """Run a candidate: check restriction [1..quickM] first, then [1..M]."""
    perm = order.restriction(quickM)
    assert sorted(perm) == list(range(1, quickM + 1)), "not a permutation of [1..M]"
    wits = find_mono4_all(perm)
    if not wits:
        perm = order.restriction(M)
        assert sorted(perm) == list(range(1, M + 1))
        wits = find_mono4_all(perm)
    mk = min_kill(perm) if wits else None
    n = len(perm)
    # displacement ratio on the checked range (lower bound on the true profile)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    ratio = max(pos[v] / v for v in range(1, n + 1))
    res = dict(name=order.name, checked=n, nwits=len(wits), min_kill=mk,
               ratio=round(ratio, 2), wits=wits, perm=perm)
    return res


def report_line(res):
    if res["nwits"] == 0:
        return (f"{res['name']:<48} CLEAN to M={res['checked']}  "
                f"maxdisp={res['ratio']}")
    return (f"{res['name']:<48} DIES  min_kill={res['min_kill']}  "
            f"#wits(M={res['checked']})={res['nwits']}  maxdisp={res['ratio']}")


# ---------------------------------------------------------------- F1 family


def make_F1(alphas, betas, prio=None, name=None, depth=None):
    """g(n) = sum_l q_l(digit_l n), q_l = (0, alphas[l], betas[l]).
    Default tie priorities: natural (0,1,2) per level unless prio given."""
    depth = depth or len(alphas)
    A = list(alphas)
    B = list(betas)

    def gfun(n):
        tot = 0
        l = 0
        while n:
            t = n % 3
            if t == 1:
                tot += A[l]
            elif t == 2:
                tot += B[l]
            n //= 3
            l += 1
        return tot

    nm = name or f"F1 a={A[:6]}.. b={B[:6]}.."
    return GradedTauOrder(gfun, prio=prio, depth=depth, name=nm)


def prio_const(perm3):
    p = tuple(perm3)
    return lambda l, c: p


def prio_per_level(perms):
    ps = [tuple(p) for p in perms]
    return lambda l, c: ps[l % len(ps)]


def prio_magnitude(alphas, betas):
    """Priorities consistent with q-magnitude: rank digits by (0, alpha_l, beta_l)."""
    prs = []
    for a, b in zip(alphas, betas):
        vals = [(0, 0), (a, 1), (b, 2)]
        vals.sort()
        pr = [0, 0, 0]
        for rank, (_, dig) in enumerate(vals):
            pr[dig] = rank
        prs.append(tuple(pr))
    return lambda l, c: prs[l] if l < len(prs) else prs[-1]


# ---------------------------------------------------------------- self-check

def selfcheck():
    import random
    rng = random.Random(196)
    # 1. tau* (constant priorities) kills 4-APs on [1..M] — Lemma T reproduction
    for prios in [(0, 1, 2), (2, 0, 1), (1, 2, 0), (0, 2, 1), (2, 1, 0), (1, 0, 2)]:
        o = GradedTauOrder(lambda n: 0, prio=prio_const(prios), depth=9,
                           name=f"pure tau {prios}")
        perm = o.restriction(1500)
        assert not has_monotone_kap_pos(perm, 4), prios
    # 2. context-dependent tau* also kills (Lemma T*): random context priorities
    import itertools
    PERMS = list(itertools.permutations((0, 1, 2)))
    tbl = {}
    def prio_rand(l, c):
        k = (l, c)
        if k not in tbl:
            tbl[k] = PERMS[rng.randrange(6)]
        return tbl[k]
    o = GradedTauOrder(lambda n: 0, prio=prio_rand, depth=9, name="tau* random ctx")
    perm = o.restriction(1500)
    assert not has_monotone_kap_pos(perm, 4)
    # also on random subsets, via general checker
    from apcheck import has_monotone_kap_general
    for _ in range(60):
        S = rng.sample(range(1, 4000), 60)
        seq = sorted(S, key=o.key)
        assert not has_monotone_kap_general(seq, 4)
    # 3. rule table: random small graded orders — predicted deaths == actual deaths
    for trial in range(40):
        levels = 6
        A = [rng.randrange(1, 40) for _ in range(levels)]
        B = [rng.randrange(1, 40) for _ in range(levels)]
        o = make_F1(A, B, depth=8)
        M = 200
        perm = o.restriction(M)
        wits = find_mono4_all(perm)
        # predicted set
        predset = set()
        for d in range(1, (M - 1) // 3 + 1):
            for x in range(1, M - 3 * d + 1):
                c = classify_witness(o, x, d, +1)
                if c["pred"] != 0:
                    predset.add((x, d, c["pred"]))
        assert predset == set(wits), (A, B, len(predset), len(wits))
    # 4. find_mono4_all vs trusted checker on random perms
    for _ in range(300):
        n = rng.randint(4, 40)
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert (len(find_mono4_all(p)) > 0) == has_monotone_kap_pos(p, 4)
    print("r16lib selfcheck OK: Lemma T + T* reproduction, rule table exact on 40 "
          "random graded orders, scanner cross-validated (300 perms)")


if __name__ == "__main__":
    selfcheck()
