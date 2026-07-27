"""engine.py — Route R4 reference backtracking engine (Python, exact arithmetic).

Claim tested per run: existence / count of monotone-4-AP-free permutations of [1..N]
under displacement constraints. Conventions per PROBLEM.md: positions and values 1-based;
perm[i-1] = a(i) = value at position i; pi(v) = position of value v.

Constraint classes (C = num/den, exact rational):
  A : pi(v) <= C*v            for all v          (upper bound on position of each value)
  B : a(i)  <= C*i            for all i          (equivalently pi(v) >= ceil(v/C))
  C : both A and B
  D : pi(v) <= 2*v            for all v <= N//2  (prefix coverage, factor 2 fixed)
  Bp: injective SEQUENCE a(1..N) of distinct positive integers (not nec. a permutation
      of [1..N]) with a(i) <= C*i and no monotone 4-AP among its values.  This is the
      exact object inherited by every position-prefix of an infinite permutation
      satisfying a(i) <= C*i, so Bp-extinction at N certifies an infinite theorem.

Search: values placed in increasing order v = 1..N (classes A,B,C,D).  When v is placed,
values present are exactly 1..v-1, so every monotone 4-AP is detected exactly once, when
its LARGEST element is placed.  For each d >= 1 with v-3d >= 1, writing
p1=pi(v-3d), p2=pi(v-2d), p3=pi(v-d):
  p1<p2<p3  => placing v at any p > p3 completes an increasing 4-AP  => require p <= p3-1
  p1>p2>p3  => placing v at any p < p3 completes a decreasing 4-AP   => require p >= p3+1
so the AP-safety region for v is an INTERVAL [L, U] intersected with free positions and
with the class interval [lo(v), hi(v)].  This makes the search exact and complete.

Class Bp is searched by positions i = 1..N, appending w = a(i): the new element sits at
the last position, so it can only be the largest value of an increasing 4-AP
(need pi(w-3d)<pi(w-2d)<pi(w-d), all present) or the smallest value of a decreasing one
(need pi(w+3d)<pi(w+2d)<pi(w+d), all present).  Complete for the same reason.

Modes: 'exists' (stop at first avoider), 'count' (count all), both exhaustive unless the
node cap is hit (result then flagged inexhaustive).
"""

from fractions import Fraction
import sys

sys.setrecursionlimit(100000)


def bounds_for_class(N, cls, C):
    """Return (lo, hi) arrays (1-indexed, entries for v=1..N) of position bounds."""
    num, den = C.numerator, C.denominator
    lo = [1] * (N + 1)
    hi = [N] * (N + 1)
    for v in range(1, N + 1):
        if cls in ("A", "C"):
            hi[v] = min(N, (num * v) // den)          # pi(v) <= floor(Cv)
        if cls in ("B", "C"):
            lo[v] = -((-v * den) // num)              # pi(v) >= ceil(v/C)
        if cls == "D":
            if v <= N // 2:
                hi[v] = min(N, 2 * v)
    return lo, hi


class SearchResult:
    def __init__(self):
        self.count = 0
        self.example = None
        self.nodes = 0
        self.exhaustive = True


def search_perm(N, cls, C, mode="exists", node_cap=None, collect=None):
    """Backtracking over permutations of [1..N] for classes A,B,C,D.

    Returns SearchResult.  collect: optional list to receive up to `collect_max`
    avoiders (as tuples perm with perm[i-1]=a(i))."""
    assert cls in ("A", "B", "C", "D")
    lo, hi = bounds_for_class(N, cls, C)
    num, den = C.numerator, C.denominator
    pos = [0] * (N + 1)          # pos[v] = position of value v (1..N)
    used = [False] * (N + 2)
    res = SearchResult()
    need_fill_check = cls in ("B", "C")

    def min_free():
        for p in range(1, N + 1):
            if not used[p]:
                return p
        return None

    def rec(v):
        if node_cap is not None and res.nodes > node_cap:
            res.exhaustive = False
            return True  # abort
        if v > N:
            res.count += 1
            if res.example is None or collect is not None:
                perm = [0] * N
                for w in range(1, N + 1):
                    perm[pos[w] - 1] = w
                if res.example is None:
                    res.example = tuple(perm)
                if collect is not None and len(collect) < 1000:
                    collect.append(tuple(perm))
            return mode == "exists"
        L, U = lo[v], hi[v]
        for d in range(1, (v - 1) // 3 + 1):
            p1, p2, p3 = pos[v - 3 * d], pos[v - 2 * d], pos[v - d]
            if p1 < p2 < p3:
                if p3 - 1 < U:
                    U = p3 - 1
            elif p1 > p2 > p3:
                if p3 + 1 > L:
                    L = p3 + 1
            if L > U:
                return False
        for p in range(L, U + 1):
            if used[p]:
                continue
            used[p] = True
            pos[v] = p
            ok = True
            if need_fill_check:
                m = min_free()
                if m is not None and (num * m) // den <= v:
                    ok = False   # position m can never be filled by any value > v
            if ok:
                res.nodes += 1
                if rec(v + 1):
                    used[p] = False
                    return True
            used[p] = False
        return False

    rec(1)
    return res


def search_seq_Bp(N, C, mode="exists", node_cap=None):
    """Class Bp: injective sequences a(1..N), a(i) <= C*i, distinct positive integers,
    no monotone 4-AP among placed values.  Returns SearchResult (example is the sequence)."""
    num, den = C.numerator, C.denominator
    maxval = (num * N) // den
    pos = [0] * (maxval + 1)     # pos[w] = position of value w, 0 = absent
    seq = []
    res = SearchResult()

    def safe(w, i):
        # would appending value w at position i create a monotone 4-AP?
        d = 1
        while w - 3 * d >= 1:
            p1, p2, p3 = pos[w - 3 * d], pos[w - 2 * d], pos[w - d]
            if p1 and p2 and p3 and p1 < p2 < p3:
                return False
            d += 1
        d = 1
        while w + 3 * d <= maxval:
            p1, p2, p3 = pos[w + 3 * d], pos[w + 2 * d], pos[w + d]
            if p1 and p2 and p3 and p1 < p2 < p3:
                return False
            d += 1
        return True

    def rec(i):
        if node_cap is not None and res.nodes > node_cap:
            res.exhaustive = False
            return True
        if i > N:
            res.count += 1
            if res.example is None:
                res.example = tuple(seq)
            return mode == "exists"
        top = (num * i) // den
        for w in range(1, top + 1):
            if pos[w]:
                continue
            if not safe(w, i):
                continue
            pos[w] = i
            seq.append(w)
            res.nodes += 1
            if rec(i + 1):
                pos[w] = 0
                seq.pop()
                return True
            pos[w] = 0
            seq.pop()
        return False

    rec(1)
    return res


# ----------------------------------------------------------------------------- brute
def brute_counts(N, cls, C):
    """Ground truth for tiny N: filter all N! permutations by constraints + 4-AP-freeness
    using the validated checker from experiments/apcheck.py."""
    from itertools import permutations
    sys.path.insert(0, "/home/user/erdos/experiments")
    from apcheck import has_monotone_kap_brute

    lo, hi = bounds_for_class(N, cls, C)
    cnt = 0
    for p in permutations(range(1, N + 1)):
        okc = True
        for i, v in enumerate(p):
            if not (lo[v] <= i + 1 <= hi[v]):
                okc = False
                break
        if okc and not has_monotone_kap_brute(p, 4):
            cnt += 1
    return cnt


def brute_counts_Bp(N, C):
    """Ground truth for tiny N for class Bp: enumerate all injective sequences."""
    sys.path.insert(0, "/home/user/erdos/experiments")
    from apcheck import has_monotone_kap_brute

    num, den = C.numerator, C.denominator
    cnt = 0

    def rec(i, seq, usedvals):
        nonlocal cnt
        if i > N:
            if not has_monotone_kap_brute(seq, 4):
                cnt += 1
            return
        top = (num * i) // den
        for w in range(1, top + 1):
            if w in usedvals:
                continue
            usedvals.add(w)
            seq.append(w)
            rec(i + 1, seq, usedvals)
            seq.pop()
            usedvals.remove(w)

    rec(1, [], set())
    return cnt


if __name__ == "__main__":
    # Self cross-validation: engine counts vs brute-force ground truth, N <= 7.
    Cs = [Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(5)]
    print("cross-validating engine vs brute force (all permutations + validated checker)")
    for N in range(4, 8):
        for cls in ("A", "B", "C", "D"):
            for C in Cs:
                if cls == "D" and C != Fraction(2):
                    continue
                got = search_perm(N, cls, C, mode="count").count
                want = brute_counts(N, cls, C)
                assert got == want, (N, cls, str(C), got, want)
        print(f"  N={N}: classes A,B,C,D OK for all C")
    for N in range(1, 7):
        for C in Cs[1:]:
            got = search_seq_Bp(N, C, mode="count").count
            want = brute_counts_Bp(N, C)
            assert got == want, (N, "Bp", str(C), got, want)
        print(f"  N={N}: class Bp OK for all C")
    # unconstrained sanity: class A with huge C should reproduce known 4-AP-free counts
    known = {4: 22, 5: 102, 6: 564, 7: 3336}
    for N, want in known.items():
        got = search_perm(N, "A", Fraction(10**6), mode="count").count
        assert got == want, (N, got, want)
    print("  unconstrained counts N=4..7 match known 22,102,564,3336")
    print("ALL ENGINE CROSS-VALIDATIONS PASSED")
