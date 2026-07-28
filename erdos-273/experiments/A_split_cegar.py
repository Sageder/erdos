"""
A_split_cegar.py

CLAIM TESTED: is there a covering system of Z with DISTINCT moduli, all in
E = {p-1 : p >= 5 prime}, all dividing a given L?  Decided exactly, by CEGAR on the
parity split instead of one monolithic SAT instance.

By Lemma A1 such a covering is exactly a pair of DISJOINT subsets M_0, M_1 of
D_H(Lh), Lh = L/2, each of which supports a covering of Z/Lh with distinct moduli.
(M_c = {n/2 : n used with residue of parity c}.)

MASTER (tiny SAT over 2|D_H| Booleans P[m][c] = "m in half c"):
   - P[m][0], P[m][1] mutually exclusive  (a modulus is used in at most one half)
   - Lemma A2 overlap clauses
   - refinement clauses discovered below
SUB-ORACLE (one SAT over Z/Lh per half):  "can Z/Lh be covered with distinct moduli
   taken from M_c?"

Refinement is sound because coverability is MONOTONE in the modulus set: if M_c cannot
cover, no subset of M_c can, so any solution must put some modulus OUTSIDE M_c into half c.
   UNSAT(M_c)  =>  add clause   OR_{m not in M_c} P[m][c].
If both halves come back SAT we have a genuine certificate for Erdos 273 and it is written
out and independently re-verified.  If the master becomes UNSAT, no covering with moduli in
E has lcm dividing L -- a proof.

CONCLUSION: printed; certificates written to ../attempts/route-A-satsearch/certs/.
"""
import sys, os, time, json
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, budget, verify_cover
from A_sat_cover import overlap_sets, minimal_hitting_sets, solve_cover

CERTS = "/home/user/erdos/erdos-273/attempts/route-A-satsearch/certs"


def run(L, sub_timeout=300, total_budget=1500, verbose=True):
    assert L % 2 == 0
    Lh = L // 2
    D = D_H(Lh)
    assert [2 * m for m in D] == D_E(L), "Lemma A1 bookkeeping mismatch"
    B = budget(D)                     # = B_H(Lh) = 2 * B_E(L)
    k = len(D)
    t_start = time.time()
    print(f"=== L={L}  Lh={Lh}  |D_H|={k}  B_H={float(B):.6f} "
          f"(each half needs > 1, so both halves' excess < {float(B-2):.6f})")
    if B <= 2:
        print("    >>> UNSAT by the density bound alone (B_H <= 2).")
        return "UNSAT(density)", None

    from pysat.solvers import Solver
    s = Solver(name="cadical153")

    def P(i, c):
        return 2 * i + c + 1

    for i in range(k):
        s.add_clause([-P(i, 0), -P(i, 1)])
    T_sets = overlap_sets(D, B - 2, pool=min(k, 20), smax=4, maxsets=2000)
    idx = {m: i for i, m in enumerate(D)}
    for T in T_sets:
        for c in (0, 1):
            s.add_clause([-P(idx[m], c) for m in T])
    for S in minimal_hitting_sets(D, B - 1, smax=4, pool=min(k, 16), maxsets=250):
        for c in (0, 1):
            s.add_clause([P(idx[m], c) for m in S])
    print(f"    master: {len(T_sets)} overlap clauses seeded", flush=True)

    memo_unsat, memo_sat = [], []
    rounds = 0
    while True:
        if time.time() - t_start > total_budget:
            print(f"    >>> OUT OF TIME after {rounds} rounds")
            return "TIMEOUT", rounds
        rounds += 1
        if not s.solve():
            print(f"    >>> MASTER UNSAT after {rounds} rounds "
                  f"({time.time()-t_start:.0f}s)  ==>  NO covering with moduli in E has "
                  f"lcm dividing {L}")
            return "UNSAT", rounds
        model = set(l for l in s.get_model() if l > 0)
        M = [[], []]
        for i, m in enumerate(D):
            for c in (0, 1):
                if P(i, c) in model:
                    M[c].append(m)
        ok = [None, None]
        for c in (0, 1):
            Mc = set(M[c])
            if budget(M[c]) <= 1:
                ok[c] = ("UNSAT", None)
                continue
            if any(Mc <= u for u in memo_unsat):
                ok[c] = ("UNSAT", None)
                continue
            hit = next((cl for U, cl in memo_sat if U <= Mc), None)
            if hit is not None:
                ok[c] = ("SAT", hit)
                continue
            t_sub = time.time()
            ok[c] = solve_cover(Lh, M[c], "full", sub_timeout, world="H")
            if verbose:
                print(f"      sub[{c}] |M|={len(M[c])} sum={float(budget(M[c])):.4f}"
                      f" -> {ok[c][0]} in {time.time()-t_sub:.1f}s", flush=True)
            if ok[c][0] == "UNSAT":
                memo_unsat.append(Mc)
            elif ok[c][0] == "SAT":
                memo_sat.append((set(n for n, _ in ok[c][1]), ok[c][1]))
        if ok[0][0] == "SAT" and ok[1][0] == "SAT":
            classes = ([(2 * n, 2 * a) for n, a in ok[0][1]] +
                       [(2 * n, 2 * a + 1) for n, a in ok[1][1]])
            good, msg = verify_cover(L, classes, world="E", relaxed=False)
            print(f"    >>> *** CERTIFICATE FOUND *** {len(classes)} classes, check: {msg}")
            os.makedirs(CERTS, exist_ok=True)
            fn = os.path.join(CERTS, f"cert_E_full_L{L}_cegar.json")
            json.dump(dict(L=L, world="E", mode="full", verdict="SAT",
                           classes=classes, nmods=len(classes)),
                      open(fn, "w"), indent=1)
            print(f"    written to {fn}")
            return "SAT", classes
        if "TIMEOUT" in (ok[0][0], ok[1][0]):
            print(f"    >>> sub-oracle TIMEOUT at round {rounds}; aborting (incomplete)")
            return "TIMEOUT", rounds
        for c in (0, 1):
            if ok[c][0] == "UNSAT":
                s.add_clause([P(i, c) for i, m in enumerate(D) if m not in set(M[c])])
        if verbose:
            print(f"    round {rounds}: |M0|={len(M[0])} |M1|={len(M[1])} "
                  f"memo_unsat={len(memo_unsat)} t={time.time()-t_start:.0f}s", flush=True)


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:2]] or [55440]
    sub = float(sys.argv[2]) if len(sys.argv) > 2 else 300
    tot = float(sys.argv[3]) if len(sys.argv) > 3 else 1500
    for L in Ls:
        v, info = run(L, sub, tot)
        print(f"### L={L}: {v}")
