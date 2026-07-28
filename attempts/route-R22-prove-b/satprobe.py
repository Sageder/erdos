"""satprobe.py -- route R22: does the HEAD-DELAY architecture admit 4-AP-free
within-class orders on [1..N]?

Reuses route R20's validated CEGAR class-order solver (`classsat.solve_classes`), which
returns UNSAT only as an impossibility statement over ALL within-class orders, and
re-verifies every SAT model with the trusted experiments/apcheck.py checker.

CAUTION (CORE.md Remark 27): this architecture has SUPERLINEAR displacement, so by the
certified extinction law it cannot be expected to die at reachable N.  A SAT verdict is
therefore NOT evidence of viability; only an UNSAT would be informative.
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from classsat import solve_classes                                  # noqa: E402
from apcheck import has_monotone_kap_pos                            # noqa: E402
from arch import blk                                                # noqa: E402


def head_class(b, s_of_m, K_of_m):
    def c(v):
        m = blk(v, b)
        s = s_of_m(m)
        return m + (K_of_m(m) if v < b ** m + s else 0)
    return c


FAMILIES = {
    'HEAD(3, s=m+1, K=m)':  head_class(3, lambda m: m + 1, lambda m: m),
    'HEAD(3, s=m+1, K=1)':  head_class(3, lambda m: m + 1, lambda m: 1),
    'HEAD(5, s=m+1, K=m)':  head_class(5, lambda m: m + 1, lambda m: m),
    'HEAD(3, s=2m+2, K=m)': head_class(3, lambda m: 2 * m + 2, lambda m: m),
}

if __name__ == "__main__":
    names = sys.argv[1].split(',') if len(sys.argv) > 1 else list(FAMILIES)
    Ns = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else
                           ['60', '100', '160', '250'])]
    for nm in names:
        c = FAMILIES[nm]
        for N in Ns:
            t0 = time.time()
            res, w, rounds = solve_classes(N, c)
            dt = time.time() - t0
            extra = ""
            if res == "SAT":
                assert sorted(w) == list(range(1, N + 1))
                assert not has_monotone_kap_pos(w, 4), "model is not an avoider!"
                pos = {v: i + 1 for i, v in enumerate(w)}
                extra = f" maxpos/v={max(pos[v] / v for v in range(1, N + 1)):.2f}"
                open(f"/home/user/erdos/attempts/route-R22-prove-b/cw_{nm.replace(' ','')}_{N}.txt",
                     "w").write(repr(w))
            elif res.startswith("FORCED"):
                extra = f" at (x,e)={w}"
            print(f"{nm} N={N}: {res} ({dt:.0f}s, {rounds} rounds){extra}", flush=True)
            if res != "SAT":
                break
