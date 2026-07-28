"""
A_minimal_L.py

CLAIM TESTED: what is the SMALLEST modulus L for which the (world, mode) problem
    world H, mode full      : cover Z/L with distinct divisors of L in H = {m>=2 : 2m+1 prime}
    world H, mode relaxed   : cover Z/L minus {0} likewise, no class hitting 0
    world E, mode full      : cover Z/L with distinct divisors of L in E = {n>=4 : n+1 prime}
    world E, mode relaxed   : cover Z/L minus {0} likewise
is SATISFIABLE?

Why it matters: world H is a single "parity half" of Erdos 273 (Lemma A1).  Establishing
that H-coverings exist at all -- and at which L -- is the prerequisite for the real
question, which needs TWO DISJOINT H-coverings sharing the same L.
The minimal L for world E is a lower bound on the lcm of any E-covering system.

Every candidate L is a y-smooth number below the bound; the density test
sum_{n | L, n in world} 1/n > 1 rules most of them out with no SAT call.

CONCLUSION: printed table; smallest SAT L per (world,mode).
"""
import sys, os, time, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, budget
from A_sat_cover import run

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def smooth_numbers(bound):
    out = {1}
    for p in PRIMES:
        new = set()
        for x in out:
            v = x
            while v <= bound:
                new.add(v)
                v *= p
        out = new
    return sorted(out)


if __name__ == "__main__":
    BOUND = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
    WORLD = sys.argv[2] if len(sys.argv) > 2 else "H"
    MODE = sys.argv[3] if len(sys.argv) > 3 else "full"
    TMO = float(sys.argv[4]) if len(sys.argv) > 4 else 120
    FORBID = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else []
    STOP = (sys.argv[6] != "all") if len(sys.argv) > 6 else True
    cands = [L for L in smooth_numbers(BOUND) if L > 1]
    D = D_H if WORLD == "H" else D_E
    live = [(L, [x for x in D(L) if x not in FORBID]) for L in cands]
    live = [(L, d) for L, d in live if budget(d) > 1]
    print(f"{len(live)} candidates L <= {BOUND} with budget > 1 (world {WORLD})")
    print(f"smallest such L: {live[0][0] if live else None}")
    results = []
    for L, d in live:
        t = time.time()
        out = run(L, WORLD, MODE, None, None, "weak", 6, 0, "cadical153", TMO,
                  "/home/user/erdos/erdos-273/attempts/route-A-satsearch/certs",
                  forbid=FORBID, tag="_min" + ("_no" + "_".join(map(str, FORBID)) if FORBID else ""))
        results.append((L, len(d), float(budget(d)), out["verdict"],
                        round(out["solve_time"], 2)))
        print(f"### L={L} #mods={len(d)} budget={float(budget(d)):.4f} "
              f"-> {out['verdict']} in {out['solve_time']:.2f}s", flush=True)
        if out["verdict"] == "SAT":
            print("### FIRST SAT FOUND at L =", L)
            if STOP:
                break
    print("\nL, #mods, budget, verdict, solve_time")
    for r in results:
        print(r)
