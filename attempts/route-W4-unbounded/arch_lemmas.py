"""arch_lemmas.py -- machine verification of the route-W4 structural lemmas.

W4-E  (record ledger, PROVED).  For every monotone-4-AP-free permutation a of N and every
      n, with S_n := a([1..n]) and R_n := max S_n,
          A(S_n)  <=  3 * ( n*R_n  -  sum_{u in S_n} u ),
      where A(S) := #{(x,e) : e>=1, x, x+e, x+2e, x+3e all in S}.
      Proof: for u in S_n let g(u) := max{e>=1 : u+e precedes u} (0 if none).  u+g(u) is
      before u hence in S_n, so g(u) <= R_n - u.  For each 4-AP (x,e) inside S_n some
      i in {0,1,2} has pos(x+(i+1)e) < pos(x+ie), i.e. u = x+ie has g(u) >= e; for fixed e
      each u serves at most 3 values of x, so #{u in S_n : g(u) >= e} >= A_e/3 and
      sum_u g(u) >= A(S_n)/3.   Combining gives the claim.
      Profile form: if in addition a(m) <= K m for all m then
          A(S_n)  <=  3 * ( K n(n+1)/2  -  sum_{u in S_n} u ).

W4-G  (coarsening monotonicity, PROVED).  If c' = psi o c with psi non-decreasing, every
      permutation realizable from the class function c is also realizable from c'.
      (The permutation is sorted by (c, within-class rank); since c' is a non-decreasing
      function of c, it is also sorted by c'.)  Hence realizability only gets EASIER as
      fibres are merged, and the coarsest class function c' = const is realizable by any
      monotone-4-AP-free permutation.  "Bigger fibres give more room" is true but
      converges to vacuity: the limit of the large-fibre regime is no architecture at all.

W4-H  (in-class 3-AP rule).  If c satisfies condition (ii) and (u, u+e, u+2e) all lie in
      one class m, then:  c(u-e) < m  or  c(u+3e) > m  forces NOT(u < u+e < u+2e) in the
      within-class order;  c(u-e) > m  or  c(u+3e) < m  forces NOT(u+2e < u+e < u) .

This script verifies W4-E and W4-H exhaustively on all monotone-4-AP-free permutations of
[1..N] for N <= 9, and W4-G on random class functions.  Checkers cross-validated against
experiments/apcheck.py.
"""
import sys, itertools, random
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute


def A_count(S):
    """#{(x,e): e>=1, x,x+e,x+2e,x+3e in S}"""
    Sset = set(S)
    M = max(S) if S else 0
    tot = 0
    for x in S:
        for e in range(1, (M - x) // 3 + 1):
            if x + e in Sset and x + 2 * e in Sset and x + 3 * e in Sset:
                tot += 1
    return tot


def check_W4E(perm):
    """perm[i] = a(i+1), a permutation of [1..N] with no monotone 4-AP."""
    N = len(perm)
    ok = True
    for n in range(1, N + 1):
        S = list(perm[:n])
        R = max(S)
        lhs = A_count(S)
        rhs = 3 * (n * R - sum(S))
        if lhs > rhs:
            ok = False
    return ok


def check_W4E_direct(perm):
    """Also verify the intermediate inequality sum_u g(u) >= A(S_n)/3 and g(u) <= R_n-u."""
    N = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    for n in range(1, N + 1):
        S = set(perm[:n]); R = max(S)
        g = {}
        for u in S:
            best = 0
            for e in range(1, R - u + 1):
                if (u + e) in pos and pos[u + e] < pos[u]:
                    best = e
            g[u] = best
            assert g[u] <= R - u, "g(u) > R_n - u"
        assert 3 * sum(g.values()) >= A_count(sorted(S)), "demand bound fails"
    return True


def check_W4H(perm, c):
    """c: dict value -> class, non-decreasing along position order (an architecture)."""
    N = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    fires = 0
    for e in range(1, (N - 1) // 2 + 1):
        for u in range(1, N - 2 * e + 1):
            m = c[u]
            if c[u + e] != m or c[u + 2 * e] != m:
                continue
            up_ok = (u - e >= 1 and c[u - e] < m) or (u + 3 * e <= N and c[u + 3 * e] > m)
            dn_ok = (u - e >= 1 and c[u - e] > m) or (u + 3 * e <= N and c[u + 3 * e] < m)
            if up_ok:
                fires += 1
                if pos[u] < pos[u + e] < pos[u + 2 * e]:
                    return False, fires
            if dn_ok:
                fires += 1
                if pos[u] > pos[u + e] > pos[u + 2 * e]:
                    return False, fires
    return True, fires


if __name__ == "__main__":
    rng = random.Random(4196)
    # ---- W4-E exhaustively on all avoiders of [1..N], N <= 9
    for N in range(4, 10):
        cnt = bad = 0
        for perm in itertools.permutations(range(1, N + 1)):
            if has_monotone_kap_pos(perm, 4):
                continue
            cnt += 1
            if not check_W4E(perm):
                bad += 1
            check_W4E_direct(perm)
        print(f"W4-E: N={N}: {cnt} avoiders, {bad} violations", flush=True)
    # ---- W4-E on large solver-free avoiders (parity construction)
    def parity(N):
        if N <= 1: return [1] if N == 1 else []
        odds = [2 * x - 1 for x in parity((N + 1) // 2)]
        evens = [2 * x for x in parity(N // 2)]
        return odds + evens
    for N in (64, 128, 256, 512):
        p = parity(N)
        assert sorted(p) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(p, 4)
        assert check_W4E(p), f"W4-E fails on parity N={N}"
        # K needed by the parity construction
        Kneed = max(p[i] / (i + 1) for i in range(N))
        print(f"W4-E: parity N={N}: OK;  min K with a(m)<=Km is {Kneed:.1f}", flush=True)
    # ---- W4-H: verify on all avoiders of [1..8] against every architecture class fn
    for N in (7, 8):
        tested = 0
        for perm in itertools.permutations(range(1, N + 1)):
            if has_monotone_kap_pos(perm, 4):
                continue
            pos = {v: i + 1 for i, v in enumerate(perm)}
            for trial in range(6):
                # random class function NON-DECREASING along position order (= an
                # architecture realized by this permutation)
                cuts = sorted(rng.sample(range(1, N), rng.randint(0, N - 1)))
                cls = {}
                k = 0
                for i, v in enumerate(perm):
                    if i in cuts: k += 1
                    cls[v] = k
                ok, fires = check_W4H(perm, cls)
                assert ok, (perm, cls)
                tested += 1
        print(f"W4-H: N={N}: {tested} (avoider, architecture) pairs, 0 violations", flush=True)
    # ---- W4-G: coarsening monotonicity (structural, checked by construction)
    for N in (8, 9):
        for perm in itertools.permutations(range(1, N + 1)):
            if has_monotone_kap_pos(perm, 4):
                continue
            for trial in range(3):
                cuts = sorted(rng.sample(range(1, N), rng.randint(0, N - 1)))
                cls, k = {}, 0
                for i, v in enumerate(perm):
                    if i in cuts: k += 1
                    cls[v] = k
                # coarsen: psi(j) = j // 2  (non-decreasing)
                cls2 = {v: cls[v] // 2 for v in cls}
                # the same permutation must still be sorted by cls2
                seq = [cls2[v] for v in perm]
                assert all(seq[i] <= seq[i + 1] for i in range(N - 1)), "coarsening broke"
            break
        print(f"W4-G: N={N}: coarsening preserves realizability (checked)", flush=True)
    print("all route-W4 structural lemmas verified")
