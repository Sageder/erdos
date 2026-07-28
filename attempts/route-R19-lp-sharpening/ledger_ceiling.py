"""ledger_ceiling.py -- CERTIFIED upper bounds on the ledger ceiling C_ledger(N).

For each N we exhibit an explicit increasing-4-AP-free permutation sigma of [1..N]
(CP-SAT feasible solution, re-verified by an independent checker) with a small value of
sum_j tau_j.  Every such witness certifies

    S_inc(N) <= sum_j tau_j(sigma)   =>   C_ledger(N) <= N(N+1)/(2(N^2+N-sum tau)),

i.e. NO argument of the CORE-Thm-12 ledger type can prove LP-inc(C) at board size N for
that C or larger.  (Only an upper bound is claimed; the CP-SAT optimum may be smaller,
which would only lower the ceiling further.)

Witnesses are written to witnesses.txt so the bounds are reproducible without a solver.
"""

import sys, os, json
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from r19lib import has_inc_4ap, taus, triadic
from min_tau import cpsat_min_tau, C_ledger

if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or list(range(24, 121, 4))
    budget = float(os.environ.get("BUDGET", "60"))
    out = open("/home/user/erdos/attempts/route-R19-lp-sharpening/witnesses.txt", "a")
    worst = Fraction(0)
    for N in Ns:
        st, val, perm = cpsat_min_tau(N, budget=budget)
        if st == "UB":
            val = val[0]
        if perm is None:
            print(f"{N}: {st}"); continue
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_inc_4ap(perm), "witness has an increasing 4-AP"
        s = sum(taus(perm)[1:])
        assert s == val
        tri = sum(taus(triadic(N))[1:])
        s = min(s, tri)
        cb = C_ledger(N, s)
        worst = max(worst, cb)
        print(f"N={N:4d}: sum tau <= {s:7d}  (gamma <= {s/N**2:.5f})   "
              f"C_ledger(N) <= {float(cb):.5f} = {cb}   [{st}, best of CP-SAT/triadic]",
              flush=True)
        out.write(json.dumps({"N": N, "sum_tau": s, "perm": perm}) + "\n")
        out.flush()
    print(f"\nMAX over the scanned N:  C_ledger(N) <= {float(worst):.5f} = {worst}")
    out.close()
