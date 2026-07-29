"""reconstruct.py -- Proposition W4-B, constructive direction, machine-verified.

From a monotone-4-AP-free permutation sigma of [1..N] with pos(v) >= v/b, build the
class architecture

    c(v) := floor(log_b pos_sigma(v)) + 1 ,     F_m := c^{-1}(m)

and check, literally:
  (1) fibres are the position blocks, |F_m| = (b-1) b^{m-1}  (GEOMETRIC, ratio b);
  (2) t(v) := c(v) - floor(log_b v)  satisfies t >= 0   (the "delay >= 0" hypothesis);
  (3) classes emitted in increasing index order reproduce sigma  (REALIZABLE, with the
      within-class orders read off from sigma);
  (4) condition (ii) holds: no strictly monotone class sequence along any 4-AP;
  (5) report max t (delay size) and max pos(v)/v (upper displacement) so one can see
      whether the delay is bounded (dead by Remark 42 / R1) or growing.

This is the converse half of Prop W4-B: every witness of the finite lower-profile problem
P(b,N) IS a finite geometric-fibre class architecture with delay t >= 0 satisfying
condition (ii) AND clearing the realizability layer.  So the realizability obstruction of
Proposition 41 is a property of the particular delays produced there, not of the family.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-W4-unbounded')
from apcheck import has_monotone_kap_pos
from dualprofile import cpsat_P, verify_P


def ilog(n, b):
    assert n >= 1
    k, p = 0, 1
    while p * b <= n:
        p *= b; k += 1
    return k


def reconstruct(perm, b):
    N = len(perm)
    pos = {v: i + 1 for i, v in enumerate(perm)}
    c = {v: ilog(pos[v], b) + 1 for v in range(1, N + 1)}
    # (1) fibres = position blocks
    from collections import Counter
    fib = Counter(c.values())
    for m, sz in sorted(fib.items()):
        exp = min(b ** m, N + 1) - b ** (m - 1)
        assert sz == exp, f"fibre {m} size {sz} != {exp}"
    # (2) t >= 0
    t = {v: c[v] - ilog(v, b) for v in range(1, N + 1)}
    assert all(t[v] >= 0 for v in range(1, N + 1)), "delay negative"
    # (3) emission order reproduces sigma
    order = sorted(range(1, N + 1), key=lambda v: (c[v], pos[v]))
    assert order == list(perm), "emission order != sigma"
    # (4) condition (ii)
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            cs = [c[x + i * d] for i in range(4)]
            assert not (cs[0] < cs[1] < cs[2] < cs[3]), (x, d, cs)
            assert not (cs[0] > cs[1] > cs[2] > cs[3]), (x, d, cs)
    maxt = max(t.values())
    maxC = max(pos[v] / v for v in range(1, N + 1))
    minC = min(pos[v] / v for v in range(1, N + 1))
    nclass = len(fib)
    return maxt, maxC, minC, nclass


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    Ns = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2
                           else "20,30,40,60,80,100".split(','))]
    for N in Ns:
        t0 = time.time()
        r, w = cpsat_P(b, 1, N, workers=2, time_limit=1800)
        if r != "SAT":
            print(f"b={b} N={N}: {r}", flush=True); break
        verify_P(w, b, 1, N)
        maxt, maxC, minC, nc = reconstruct(w, b)
        print(f"b={b} N={N}: architecture OK -- classes={nc}, max delay t={maxt}, "
              f"max pos/v={maxC:.3f}, min pos/v={minC:.3f}  ({time.time()-t0:.1f}s)",
              flush=True)
