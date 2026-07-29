"""lam_sat.py -- exact lambda(N) = min over monotone-4-AP-free permutations sigma of
[1..N] of max_v v/pos_sigma(v), by binary search over the (finite, exact) candidate set
{v/s : 1 <= s <= v <= N} using the CEGAR SAT engine of dualprofile.py.

lambda(N) <= K  iff  P(K,N) is SAT.  A monotone-4-AP-free BIJECTION a of N with
a(m) <= K m for all m forces lambda(N) <= K for EVERY N (dualprofile.py docstring).
So  limsup_N lambda(N) = infinity  would refute the whole family, at every K.

Every SAT model is re-verified literally (apcheck + profile inequality).
"""
import sys, time
from fractions import Fraction
sys.path.insert(0, '/home/user/erdos/attempts/route-W4-unbounded')
from dualprofile import cegar_P, cpsat_P, verify_P


def lam(N, engine="cegar", tl=None, verbose=False):
    cands = sorted({Fraction(v, s) for v in range(1, N + 1) for s in range(1, v + 1)})
    lo, hi = 0, len(cands) - 1
    best = None
    calls = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        K = cands[mid]
        calls += 1
        if engine == "cegar":
            r, w, _ = cegar_P(K.numerator, K.denominator, N)
        else:
            r, w = cpsat_P(K.numerator, K.denominator, N, time_limit=tl)
        if verbose:
            print(f"    N={N} K={K}={float(K):.4f}: {r}", flush=True)
        if r == "SAT":
            verify_P(w, K.numerator, K.denominator, N)
            best = (K, w); hi = mid - 1
        elif r == "UNSAT":
            lo = mid + 1
        else:
            return None, None, calls
    return best[0], best[1], calls


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1].split(',')]
    engine = sys.argv[2] if len(sys.argv) > 2 else "cegar"
    for N in Ns:
        t0 = time.time()
        K, w, calls = lam(N, engine=engine, verbose=(len(sys.argv) > 3))
        print(f"lambda({N}) = {K} = {float(K):.4f}   ({time.time()-t0:.1f}s, {calls} solves)"
              + (f"  witness={w}" if N <= 40 else ""), flush=True)
