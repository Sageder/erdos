"""degenerate.py — the exact optimum of the LITERAL AP-uniformity objective.

Objective (mission item (iii), literal form):
    U(N, qmax) := max over monotone-4-AP-free permutations sigma of [1..N]
                  of   min over APs P = {r+q, r+2q, ...}, q <= qmax, of
                       max_n pos_P(n)/n .

Trivial upper bound: pos_P(n) <= |P|, so max_n pos_P(n)/n <= |P| with equality iff the
smallest element of P is positioned after every other element of P; hence
    U(N, qmax) <= L_min(N, qmax) := min_{q<=qmax, 0<=r<q} |P_{q,r} cap [1..N]|.
The smallest elements of all these APs lie in [1..2*qmax-1] (the element r+q).  So the
bound is ATTAINED as soon as some avoider of [1..N] positions the values 1..2qmax-1 after
all larger values -- and this experiment exhibits such avoiders.

Conclusion drawn in the report: the literal optimum is the trivial combinatorial bound
L_min ~ N/qmax, attained by a device that has nothing to do with AP-uniformity; the
objective is degenerate at index n = 1 and carries no information about design
principle D1.
"""

import sys, time
from fractions import Fraction

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_uniformity, all_aps, pos_of, displacement       # noqa: E402
from engine import OrderEncoding, solve, verify_avoider               # noqa: E402


def Lmin(N, qmax):
    return min(len(el) for q, r, el in all_aps(N, qmax) if el)


if __name__ == "__main__":
    qmax = 8
    small = list(range(1, 2 * qmax))          # 1..15
    for N in (60, 100, 140):
        enc = OrderEncoding(N)
        enc.no_monotone_4ap()
        enc.before_all(small, [w for w in range(2 * qmax, N + 1)])
        t0 = time.time()
        res, perm, rounds = solve(enc, time_budget=900)
        dt = time.time() - t0
        if res != "SAT":
            print(f"N={N}: {res} ({dt:.0f}s, {rounds} rounds)", flush=True)
            continue
        verify_avoider(perm, N)
        assert set(perm[-(2 * qmax - 1):]) == set(small)
        u, who, n = ap_uniformity(perm, qmax=qmax)
        print(f"N={N}: SAT ({dt:.0f}s, {rounds} rounds).  min-AP displacement = {u} "
              f"(={float(u):.2f}) at AP (q={who[0]},r={who[1]}), index n={n};   "
              f"trivial upper bound L_min = {Lmin(N, qmax)}", flush=True)
        assert u == Lmin(N, qmax), (u, Lmin(N, qmax))
        print("   => the literal optimum U(N,8) equals its trivial upper bound.")
        open(f"/home/user/erdos/attempts/route-R21-apuniform/wit_last15_N{N}.txt",
             "w").write(repr(perm))
