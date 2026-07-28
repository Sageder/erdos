"""sat_normalforms.py — SAT tests of the TWO-POINT NORMAL FORMS derived in route R13.

Uses the validated order encoding of experiments/sat_order.py (transitivity + the two
3-literal AP clauses).  Every SAT model is decoded and re-checked with the trusted
apcheck.has_monotone_kap_pos; every UNSAT is re-run with a second solver.

Normal forms tested (see REPORT for the derivations):

  NF-RR  pos(1)=1, pos(2)=2
         PROVED necessary at EVERY N: take two records w<w' of a hypothetical
         counterexample, D=w'-w, restrict to P={w+jD} (Corollary 26); the transported
         permutation b has b(1)=1, b(2)=2, and every restriction of b to [1..N] is a
         4-AP-free permutation of [1..N] with pos(1)=1, pos(2)=2.

  NF-RG  pos(1)=1, pos(M)=M
         PROVED necessary for infinitely many M: record w, grounded g>w, sandwich.

  NF-RRG pos(1)=1, pos(2)=2, pos(M)=M
         PROVED necessary for infinitely many M: apply the sandwich inside b.

  NF-RRGG pos(1)=1, pos(2)=2, pos(M-1)=M-1, pos(M)=M
         NOT proved necessary (needs two b-grounded values at consecutive integers) —
         measured only, as a probe of how much more the normal form can take.
"""

import sys
import time

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos            # noqa: E402
from sat_order import build, decode                 # noqa: E402
from pysat.solvers import Cadical195, Glucose42     # noqa: E402


def pins_clauses(N, var, first_pins=(), last_pins=()):
    """first_pins: values that must occupy positions 1,2,... in that order.
       last_pins:  values that must occupy positions N, N-1, ... in that order
                   (given as [M, M-1, ...] meaning M last, M-1 second-to-last)."""
    cl = []
    fp = list(first_pins)
    for k, v in enumerate(fp):
        # v precedes every value not among fp[:k]
        for w in range(1, N + 1):
            if w == v or w in fp[:k]:
                continue
            cl.append([var(v, w)] if v < w else [-var(w, v)])
    lp = list(last_pins)
    for k, v in enumerate(lp):
        # v follows every value not among lp[:k]
        for w in range(1, N + 1):
            if w == v or w in lp[:k]:
                continue
            cl.append([-var(v, w)] if v < w else [var(w, v)])
    return cl


def test(N, first_pins=(), last_pins=(), solvers=("cadical",)):
    cl, pool, var = build(N, inc4=True, dec4=True)
    cl = cl + pins_clauses(N, var, first_pins, last_pins)
    out = []
    perm = None
    for s in solvers:
        S = Cadical195(bootstrap_with=cl) if s == "cadical" else Glucose42(bootstrap_with=cl)
        t0 = time.time()
        sat = S.solve()
        dt = time.time() - t0
        if sat and perm is None:
            perm = decode(S.get_model(), N, var)
        S.delete()
        out.append((s, sat, dt))
    return out, perm


def verify(perm, first_pins, last_pins):
    n = len(perm)
    assert not has_monotone_kap_pos(perm, 4), "decoded model has a monotone 4-AP"
    for k, v in enumerate(first_pins):
        assert perm[k] == v, (k, v, perm[:6])
    for k, v in enumerate(last_pins):
        assert perm[n - 1 - k] == v, (k, v, perm[-6:])
    return True


NFS = {
    "NF-RR":    (lambda M: (1, 2), lambda M: ()),
    "NF-RG":    (lambda M: (1,),   lambda M: (M,)),
    "NF-RRG":   (lambda M: (1, 2), lambda M: (M,)),
    "NF-RRGG":  (lambda M: (1, 2), lambda M: (M, M - 1)),
}

if __name__ == "__main__":
    which = sys.argv[1]
    Ns = [int(x) for x in sys.argv[2:]] or [20, 40, 60, 80, 100, 130, 160]
    fpf, lpf = NFS[which]
    for M in Ns:
        fp, lp = fpf(M), lpf(M)
        res, perm = test(M, fp, lp, solvers=("cadical",))
        s, sat, dt = res[0]
        if sat:
            verify(perm, fp, lp)
            print(f"{which} M={M:4d}: SAT   ({dt:6.1f}s)  head={perm[:8]} tail={perm[-4:]}",
                  flush=True)
        else:
            res2, _ = test(M, fp, lp, solvers=("glucose",))
            print(f"{which} M={M:4d}: UNSAT ({dt:6.1f}s) [cadical]; glucose={res2[0][1]} "
                  f"({res2[0][2]:.1f}s)  <== EXTINCTION", flush=True)
            break
