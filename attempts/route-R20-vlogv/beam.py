"""beam.py — profile-bounded beam / stochastic search for long monotone-4-AP-free
permutations of [1..N] with pos(v) <= phi(v), phi(v) = ceil(alpha * v * log2(2v)).

Insertion tree (CORE.md Lemma 8, R9's interval theorem): values arrive in increasing
order; when v is inserted the admissible slots form the interval (Lo(v), Hi(v)).
Inserting at 0-based index s puts v at position s+1 and shifts every later value one
position right, so the profile constraint is maintained incrementally:
   * s + 1 <= phi(v),
   * every w currently at index i >= s must still satisfy i + 2 <= phi(w).
Both are exact (no relaxation): a full run of length N produces a certified
phi-bounded avoider, re-verified with the trusted checker.

This is a SEARCH, so failures prove nothing; successes are witnesses.
"""

import sys, math, random
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0, '/home/user/erdos/experiments')
from framework import is_free
from apcheck import has_monotone_kap_pos


def phi_vlogv(alpha):
    return lambda v: max(1, math.ceil(alpha * v * math.log2(2 * v)))


class State:
    __slots__ = ('order', 'pos', 'n')

    def __init__(self, N):
        self.order = np.zeros(N + 1, dtype=np.int64)   # order[0..n-1] = values
        self.pos = np.zeros(N + 2, dtype=np.int64)     # pos[v] = 0-based index
        self.n = 0

    def copy(self):
        s = State.__new__(State)
        s.order = self.order.copy()
        s.pos = self.pos.copy()
        s.n = self.n
        return s

    def insert(self, v, s):
        n = self.n
        self.order[s + 1:n + 1] = self.order[s:n]
        self.order[s] = v
        if n > s:
            self.pos[self.order[s + 1:n + 1]] += 1
        self.pos[v] = s
        self.n = n + 1


def admissible(st, v, phicap):
    """Return (lo, hi) 0-based insertion index bounds [lo, hi] (inclusive) or None."""
    n = st.n
    lo, hi = 0, n
    dmax = (v - 1) // 3
    if dmax >= 1:
        ds = np.arange(1, dmax + 1, dtype=np.int64)
        a = st.pos[v - 3 * ds]
        b = st.pos[v - 2 * ds]
        c = st.pos[v - ds]
        inc = (a < b) & (b < c)
        dec = (a > b) & (b > c)
        if inc.any():
            hi = min(hi, int(c[inc].min()))       # v strictly before v-d
        if dec.any():
            lo = max(lo, int(c[dec].max()) + 1)   # v strictly after v-d
    # profile of v
    hi = min(hi, phicap[v] - 1)
    # profile of the shifted tail: need index i+2 <= phi(order[i]) for all i >= s
    if n > 0:
        vals = st.order[:n]
        slack = phicap[vals] - (np.arange(n) + 2)   # >=0 required if shifted
        # suffix-min
        sufmin = np.minimum.accumulate(slack[::-1])[::-1]
        bad = np.nonzero(sufmin < 0)[0]
        if bad.size:
            lo = max(lo, int(bad.max()) + 1)
    if lo > hi:
        return None
    return lo, hi


def run(N, alpha, width=1, seed=0, bias='latest', verbose=False):
    rng = random.Random(seed)
    phi = phi_vlogv(alpha)
    phicap = np.array([0] + [phi(v) for v in range(1, N + 1)], dtype=np.int64)
    beam = [State(N)]
    for v in range(1, N + 1):
        nxt = []
        for st in beam:
            r = admissible(st, v, phicap)
            if r is None:
                continue
            lo, hi = r
            cands = list(range(lo, hi + 1))
            if bias == 'latest':
                cands.sort(reverse=True)
            elif bias == 'earliest':
                pass
            elif bias == 'mid':
                mid = (lo + hi) / 2
                cands.sort(key=lambda s: abs(s - mid))
            elif bias == 'random':
                rng.shuffle(cands)
            for s in cands[:max(1, width)]:
                s2 = st.copy()
                s2.insert(v, s)
                nxt.append(s2)
        if not nxt:
            return v, beam[0] if beam else None      # stuck at value v
        rng.shuffle(nxt)
        # keep the widest-freedom states: score = total remaining slack
        def score(st):
            vals = st.order[:st.n]
            return int((phicap[vals] - (np.arange(st.n) + 1)).min())
        nxt.sort(key=score, reverse=True)
        beam = nxt[:width]
        if verbose and v % 100 == 0:
            print(f"   v={v} beam={len(beam)}", flush=True)
    return None, beam[0]


def certify(st, alpha):
    perm = [int(x) for x in st.order[:st.n]]
    N = st.n
    assert sorted(perm) == list(range(1, N + 1))
    assert is_free(perm, 4)
    assert not has_monotone_kap_pos(perm, 4)
    phi = phi_vlogv(alpha)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    assert all(pos[v] <= phi(v) for v in perm), "profile violated"
    return perm


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    alphas = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['0.5'])]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    for alpha in alphas:
        best = 0; bestperm = None
        for bias in ('latest', 'mid', 'random'):
            for sd in range(seeds):
                stuck, st = run(N, alpha, width=width, seed=sd, bias=bias)
                got = st.n if st is not None else 0
                if stuck is None:
                    got = N
                if got > best:
                    best, bestperm = got, st
                print(f"  alpha={alpha} bias={bias} seed={sd} width={width}: "
                      f"{'COMPLETE N='+str(N) if stuck is None else 'stuck at v='+str(stuck)}",
                      flush=True)
                if stuck is None:
                    break
            if best == N:
                break
        if bestperm is not None and best == N:
            perm = certify(bestperm, alpha)
            with open(f"/home/user/erdos/attempts/route-R20-vlogv/beam_a{alpha}_N{N}.txt", "w") as f:
                f.write(repr(perm))
            print(f"alpha={alpha}: CERTIFIED phi-bounded avoider of [1..{N}]", flush=True)
        else:
            print(f"alpha={alpha}: best reached {best}/{N}", flush=True)
