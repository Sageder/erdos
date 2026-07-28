"""profile_sat.py — SAT feasibility of monotone-4-AP-free permutations of [1..N] under a
GENERAL displacement profile phi (route R20).

Motivation (CORE.md Lemma 6 + Remark 17): 196-NO needs only SOME profile phi admitting
phi-bounded avoiders at every N.  Linear profiles pos(v) <= C v go extinct with
N*(C) ~ 4 exp(4.15(C-1.25)).  Here we measure the analogous wall for the family

    phi_alpha(v) = ceil( alpha * v * log2(2v) )      (a "v log v" profile)

If alpha*(N) := min alpha admitting an avoider stays BOUNDED as N grows (while
C*(N) ~ log N grows), that is direct evidence for the R20 target.

Engine: identical to experiments/profile_cegar.py (order encoding, lazy transitivity
CEGAR), generalized to an arbitrary phi.  Soundness notes carried over verbatim:
adding transitivity clauses only removes models, so UNSAT at any CEGAR round is UNSAT
for the full transitive system; SAT is only returned when the tournament is acyclic and
the decoded permutation is re-verified with the trusted checker apcheck.py.
"""

import sys, time, math
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

sys.path.insert(0, '/home/user/erdos/experiments')
from profile_cegar import find_cycles


def solve_profile(N, phi, max_rounds=200000, verbose=False):
    """phi: callable v -> int upper bound on pos(v).  Returns (verdict, perm, rounds)."""
    pool = IDPool()

    def var(u, w):
        return pool.id(('x', u, w))          # u < w ; true means u before w

    def lit(u, w):
        return var(u, w) if u < w else -var(w, u)

    cl = []
    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [lit(x + k * e, x + (k + 1) * e) for k in range(3)]
            cl.append([-a[0], -a[1], -a[2]])   # no increasing 4-AP
            cl.append([a[0], a[1], a[2]])      # no decreasing 4-AP
    nconstrained = 0
    for v in range(1, N + 1):
        bound = int(phi(v))
        if bound >= N:
            continue
        if bound < 1:
            return "INFEASIBLE-PROFILE", None, 0
        nconstrained += 1
        lits = [lit(w, v) for w in range(1, N + 1) if w != v]
        enc = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=pool,
                             encoding=EncType.seqcounter)
        cl.extend(enc.clauses)

    S = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        if not S.solve():
            S.delete()
            return "UNSAT", None, rounds
        model = set(S.get_model())

        def order_of(u, w):
            return var(u, w) in model

        cycs = find_cycles(order_of, N)
        if not cycs:
            import functools
            vals = list(range(1, N + 1))

            def cmp(u, w):
                if u == w:
                    return 0
                before = order_of(u, w) if u < w else (not order_of(w, u))
                return -1 if before else 1
            vals.sort(key=functools.cmp_to_key(cmp))
            S.delete()
            return "SAT", vals, rounds
        for cyc in cycs:
            L = len(cyc)
            for i in range(L):
                u, w, z = cyc[i], cyc[(i + 1) % L], cyc[(i + 2) % L]
                if len({u, w, z}) == 3:
                    S.add_clause([-lit(u, w), -lit(w, z), lit(u, z)])
            S.add_clause([-lit(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
        rounds += 1
        if verbose and rounds % 500 == 0:
            print(f"    [round {rounds}: {len(cycs)} cycles]", flush=True)
        if rounds > max_rounds:
            S.delete()
            return "UNKNOWN", None, rounds


def vlogv(alpha):
    return lambda v: max(1, math.ceil(alpha * v * math.log2(2 * v)))


def linear(C):
    return lambda v: max(1, int(C * v))


def verify(perm, phi, N):
    assert sorted(perm) == list(range(1, N + 1)), "not a permutation"
    assert not has_monotone_kap_pos(perm, 4), "solver model has a monotone 4-AP!"
    pos = {v: i + 1 for i, v in enumerate(perm)}
    assert all(pos[v] <= phi(v) for v in range(1, N + 1)), "profile violated!"
    return True


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "alpha"
    if mode == "alpha":
        alphas = [float(x) for x in sys.argv[2].split(",")]
        Ns = [int(x) for x in sys.argv[3].split(",")]
        for a in alphas:
            phi = vlogv(a)
            for N in Ns:
                t0 = time.time()
                res, perm, rounds = solve_profile(N, phi, verbose=True)
                dt = time.time() - t0
                if res == "SAT":
                    verify(perm, phi, N)
                print(f"vlogv alpha={a} N={N}: {res} ({dt:.0f}s, {rounds} rounds)",
                      flush=True)
                if res == "SAT":
                    with open(f"/home/user/erdos/attempts/route-R20-vlogv/witness_a{a}_N{N}.txt", "w") as f:
                        f.write(repr(perm))
                if res in ("UNSAT", "UNKNOWN"):
                    break
    elif mode == "lin":
        Cs = [float(x) for x in sys.argv[2].split(",")]
        Ns = [int(x) for x in sys.argv[3].split(",")]
        for C in Cs:
            phi = linear(C)
            for N in Ns:
                t0 = time.time()
                res, perm, rounds = solve_profile(N, phi, verbose=True)
                dt = time.time() - t0
                if res == "SAT":
                    verify(perm, phi, N)
                print(f"linear C={C} N={N}: {res} ({dt:.0f}s, {rounds} rounds)", flush=True)
                if res in ("UNSAT", "UNKNOWN"):
                    break
