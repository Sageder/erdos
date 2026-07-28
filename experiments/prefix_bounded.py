"""prefix_bounded.py — the sharpest cheap test of the negative branch.

By CORE.md Lemma 6, 196-NO needs SOME profile phi with phi-bounded avoiders at every N.
On a board of size N the bound pos(v) <= phi(v) is vacuous whenever phi(v) >= N, so for
a fast-growing phi the ONLY real content is: can an initial segment of values be held at
bounded positions while N -> infinity?

Concretely: for fixed K and bound c, is there a monotone-4-AP-free permutation of [1..N]
with pos(v) <= c*v for all v <= K (no constraint on v > K)?  If this stays satisfiable as
N grows for every K, then profiles like phi(v) = 2^v are viable and the negative branch
is in good shape.  If it FAILS at some N for some K, that is exactly criterion FIN(K)
(CORE.md Lemma 7) being realized -- which PROVES 196-YES.

So each row below is decisive in one direction or the other, at the parameters tested.
Engine: lazy-transitivity CEGAR (validated against exhaustive enumeration and against an
eager two-solver encoding).
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from vlogv_probe import solve_phi

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    c = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    Ns = [int(x) for x in (sys.argv[3].split(",") if len(sys.argv) > 3 else
                           ["400", "600", "800", "1200"])]
    phi = lambda v: (c * v if v <= K else 10**9)
    for N in Ns:
        t0 = time.time()
        r, p, rd, bites = solve_phi(N, phi)
        dt = time.time() - t0
        if p:
            assert sorted(p) == list(range(1, N + 1))
            assert not has_monotone_kap_pos(p, 4)
            pos = {v: i + 1 for i, v in enumerate(p)}
            assert all(pos[v] <= c * v for v in range(1, K + 1)), "prefix bound violated"
        print(f"K={K} c={c} N={N}: {r} ({dt:.0f}s, {rd} rounds, {bites} constrained)", flush=True)
        if r == "UNSAT":
            print(f"  ==> FIN({K}) REALIZED at c={c}, N={N}: every avoider of [1..{N}] has "
                  f"some v <= {K} with pos(v) > {c}v. This PROVES 196-YES if it holds for "
                  f"every c (Lemma 7).", flush=True)
            break
        if r == "UNKNOWN":
            break
