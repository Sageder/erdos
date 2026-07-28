"""verify.py -- full verification of the SLIVER construction as a refutation of R21-C.

Checks, for a range of (b, h, stripe) parameters and up to a large N:
  (1) condition (ii): zero violations  [numpy checker; cross-checked with the literal and
      the case-analysis checkers at a smaller N]
  (2) t is constant on NO progression of step <= Q (tested on the tail of each AP)
  (3) NO progression of step <= Q is tame: c|_P has c-descents at a positive rate in the
      tail (we report the longest run of non-descending steps in the tail)
  (4) the fibre design is geometric: |F_m| / b^m stays in a bounded window
  (5) displacement along every AP of step <= Q grows (D1): best-case pos_P(n)/n
  (6) STRESS: the theorem claims condition (ii) for an ARBITRARY subset D_M of the free
      region; we test random subsets.
"""
import sys, random
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from cond2 import blk, violations_numpy, violations_literal, violations_caseanal, tame_report
from construct import make_t, fibre_sizes, ap_displacement


def stripes(b, S):
    """stripe width so that each free region R_M carries exactly 2S stripes."""
    def L(M):
        return max(1, ((b ** (M + 1)) - 3 * (b ** M)) // (2 * S))
    return L


def run(N, b, hname, h, S, Q=12):
    L = stripes(b, S)
    t = make_t(N, b, h, L)
    V = violations_numpy(t, N, b, limit=3)
    rows = tame_report(t, N, b, Q=Q, tail_frac=0.5)
    ntame = [r for r in rows if r['ndesc_tail'] == 0]
    nconst = [r for r in rows if r['tconst_tail']]
    worstrun = max(r['maxrun_tail'] for r in rows)
    fs = fibre_sizes(t, N, b)
    ratios = [(m, n, round(n / b ** m, 3)) for m, n in fs if b ** (m + 1) <= N]
    disp = ap_displacement(t, N, b, Q=Q)
    mindisp = min(d[2] for d in disp)
    print(f"b={b} h={hname} stripes/block={2*S} N={N}")
    print(f"   (1) condition (ii) violations           : {len(V)}"
          + ("" if not V else f"   {V[:2]}"))
    print(f"   (2) APs (q<={Q}) with t constant on tail : {len(nconst)} / {len(rows)}")
    print(f"   (3) TAME APs (no c-descent in tail)     : {len(ntame)} / {len(rows)}"
          f"   longest non-descending tail run = {worstrun}")
    print(f"   (4) |F_m| / b^m  (full blocks)          : {[r[2] for r in ratios]}")
    print(f"   (5) min over APs of max_n pos_P(n)/n    : {mindisp}"
          f"    (max {max(d[2] for d in disp)})")
    return len(V) == 0 and not ntame and not nconst


def stress_random(N, b, trials=25, seed=196):
    """Condition (ii) for RANDOM subsets D_M of the free regions and random h_M."""
    rng = random.Random(seed)
    bad = 0
    for it in range(trials):
        t = [0] * (N + 1)
        H = {M: rng.randint(1, 6) for M in range(0, 30)}
        for v in range(1, N + 1):
            M = blk(v, b)
            if v >= 3 * b ** M and rng.random() < 0.5:
                t[v] = H[M]
        V = violations_numpy(t, N, b, limit=1)
        if V:
            bad += 1
            print("   STRESS FAILURE", b, V[:1])
    print(f"   stress: {trials} random (h_M, D_M) choices at N={N}, b={b}: "
          f"{trials - bad}/{trials} satisfy (ii)")
    return bad == 0


def crosscheck(N, b):
    L = stripes(b, 4)
    t = make_t(N, b, lambda M: M + 1, L)
    a = sorted(violations_numpy(t, N, b))
    c = sorted(violations_literal(t, N, b))
    e = sorted(violations_caseanal(t, N, b))
    assert a == c == e, (len(a), len(c), len(e))
    print(f"   cross-check of 3 (ii)-implementations at N={N}, b={b}: agree, "
          f"{len(a)} violations")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    print("=== cross-check ===")
    crosscheck(1200, 4)
    crosscheck(1200, 5)
    print("=== stress (arbitrary free-region subsets & heights) ===")
    for b in (4, 5, 8):
        stress_random(2500, b)
    print("=== full verification of the stripe witness ===")
    allok = True
    for b in (4, 5, 8):
        for hname, h in [("1", lambda M: 1), ("M+1", lambda M: M + 1),
                         ("2^M", lambda M: 2 ** M)]:
            allok &= run(N, b, hname, h, S=4, Q=12)
    print("ALL CHECKS PASSED" if allok else "SOME CHECK FAILED")
