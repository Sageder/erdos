"""core.py -- independent tooling for Erdos 196 (route-FRESH).

Conventions match PROBLEM.md / experiments/apcheck.py:
  perm[i] = value at position i+1 (0-indexed list), values distinct positive ints.
  monotone k-AP: positions i_1<...<i_k with values x, x+d, ..., x+(k-1)d (d>=1)
  read in increasing OR decreasing value order along those increasing positions.

Everything here is exact integer arithmetic.

Independent implementation #1: sign-sequence formulation.
  For a permutation of [1..N] with position map p, define eps_e(y) = sign(p(y+e)-p(y)).
  Claim (proved in REPORT.md, Prop 1): a monotone k-AP exists  iff  for some e>=1 and
  some y, the (k-1) signs eps_e(y), eps_e(y+e), ..., eps_e(y+(k-2)e) are all equal.
  This is used as a genuinely different code path from apcheck.py's (x,d) scan.
"""

from itertools import combinations


# ---------------------------------------------------------------- checkers

def has_kap_signs(perm, k):
    """Sign-sequence checker (independent code path). perm = perm of [1..N]."""
    n = len(perm)
    pos = [0] * (n + 2)
    for i, v in enumerate(perm):
        pos[v] = i
    need = k - 1                      # number of equal consecutive signs needed
    for e in range(1, (n - 1) // (k - 1) + 1):
        for start in range(1, e + 1):  # residue class start
            run = 0
            prev = 0
            y = start
            while y + e <= n:
                s = 1 if pos[y + e] > pos[y] else -1
                run = run + 1 if s == prev else 1
                prev = s
                if run >= need:
                    return True
                y += e
    return False


def has_kap_brute(perm, k):
    """Literal definition scan (ground truth, tiny n only)."""
    for idxs in combinations(range(len(perm)), k):
        vals = [perm[i] for i in idxs]
        d = vals[1] - vals[0]
        if d == 0:
            continue
        if all(vals[j + 1] - vals[j] == d for j in range(k - 1)):
            return True
    return False


# ------------------------------------------------- incremental "blocked" engine
#
# Building a permutation left to right (appending values).  Appending v is ILLEGAL
# iff it completes a monotone 4-AP, i.e. iff some monotone 3-AP (t1,t2,t3) already
# placed in increasing position order has continuation t3+(t2-t1) == v.
# So maintain blocked[] : once blocked, a value can never be placed again (the
# blocking triple never disappears).  This is the engine for the Reach searches.

class Builder:
    """Left-to-right builder over the value universe [1..N]."""

    __slots__ = ("N", "pos", "seq", "blocked", "nblocked_unplaced", "_undo")

    def __init__(self, N):
        self.N = N
        self.pos = [-1] * (N + 2)     # pos[v] = position (0-based) or -1
        self.seq = []
        self.blocked = [False] * (N + 2)
        self.nblocked_unplaced = 0
        self._undo = []

    def can_append(self, v):
        return self.pos[v] == -1 and not self.blocked[v]

    def append(self, v):
        """Append v; returns list of newly blocked values (for undo)."""
        assert self.can_append(v)
        n = len(self.seq)
        self.pos[v] = n
        self.seq.append(v)
        newly = []
        N = self.N
        pos = self.pos
        # new monotone 3-APs whose LAST (position-wise) element is v:
        #   (v-2e, v-e, v) with p(v-2e) < p(v-e) < n, for e in Z\{0}
        # each blocks the continuation v+e.
        for e in range(1, N):
            ok_any = False
            for ee in (e, -e):
                a, b, c = v - 2 * ee, v - ee, v + ee
                if 1 <= a <= N and 1 <= b <= N:
                    ok_any = True
                    if pos[a] != -1 and pos[b] != -1 and pos[a] < pos[b]:
                        if 1 <= c <= N and not self.blocked[c]:
                            self.blocked[c] = True
                            newly.append(c)
                            if pos[c] == -1:
                                self.nblocked_unplaced += 1
            if not ok_any:
                break
        self._undo.append(newly)
        return newly

    def pop(self):
        v = self.seq.pop()
        newly = self._undo.pop()
        for c in newly:
            self.blocked[c] = False
            if self.pos[c] == -1:
                self.nblocked_unplaced -= 1
        self.pos[v] = -1
        return v

    def dead(self):
        """Some value of [1..N] is unplaced and permanently blocked."""
        return self.nblocked_unplaced > 0

    def free_values(self):
        return [v for v in range(1, self.N + 1)
                if self.pos[v] == -1 and not self.blocked[v]]


def build_check(seq, N):
    """Rebuild `seq` with the Builder and confirm legality (paranoia check)."""
    b = Builder(N)
    for v in seq:
        if not b.can_append(v):
            return False
        b.append(v)
    return True
