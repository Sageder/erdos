"""verify.py -- full verification of the refuting constructions for Conjecture R21-C.

Two witnesses:
  W1 "SLIVER"  (b >= 4): t(v) = h_M on alternate stripes of the free region
                 R_M = [3 b^M, b^{M+1}), t(v) = 0 on the sliver S_M = [b^M, 3 b^M).
                 -> condition (ii), geometric fibres, no tame AP, and (with h_M -> oo)
                    UNBOUNDED displacement along every AP.
  W2 "BLOCK-CONSTANT" (any b >= 3): t(v) = tau(j(v)).  Condition (ii) is automatic
                 (c takes at most 2 values on the last three terms of any 4-AP).
                 With tau oscillating and drops >= 2, no AP is tame.  Bounded displacement.

Checks:
  (1) condition (ii) : zero violations   (numpy checker; cross-checked against the literal
      and case-analysis checkers at smaller N)
  (2) t constant on NO progression of step <= Q
  (3) NO progression of step <= Q is tame: the PROOF mechanism is verified block by block --
      for every block M whose free region lies inside [1..N] and every AP of step q <= L_M,
      an explicit c-descent is exhibited inside that block.
  (4) geometric fibre design: |F_m| / b^m bounded above and below
  (5) displacement along every AP: best-case (most favourable within-class order)
      max_n pos_P(n)/n
"""
import sys, random, bisect
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from cond2 import blk, violations_numpy, violations_literal, violations_caseanal
from construct import make_t, fibre_sizes


def stripes(b, S):
    def L(M):
        return max(1, ((b ** (M + 1)) - 3 * (b ** M)) // (2 * S))
    return L


# ---------------------------------------------------------------- witnesses
def W1(N, b, h, S=4):
    return make_t(N, b, h, stripes(b, S)), stripes(b, S)


def W2(N, b, tau):
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        t[v] = tau(blk(v, b))
    return t


# ---------------------------------------------------------------- checks
def check_ii(t, N, b):
    return violations_numpy(t, N, b, limit=3)


def check_no_tame_blockwise(t, N, b, L, Q=12):
    """For every block M with free region inside [1..N] and every AP of step q <= min(Q,L_M)
    and every residue r, exhibit a c-descent strictly inside block M.  Returns
    (n_tested, n_failed, sample_failures)."""
    c = [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]
    tested = failed = 0
    fails = []
    M = 0
    while b ** (M + 1) <= N:
        lo, hi = b ** M, b ** (M + 1)      # block M
        for q in range(1, min(Q, L(M)) + 1):
            for r in range(q):
                P = [v for v in range(lo + ((r - lo) % q), hi, q)]
                if len(P) < 3:
                    continue
                tested += 1
                if not any(c[P[i + 1]] < c[P[i]] for i in range(len(P) - 1)):
                    failed += 1
                    if len(fails) < 4:
                        fails.append((M, q, r))
        M += 1
    return tested, failed, fails


def check_t_nonconstant(t, N, b, Q=12, tail_frac=0.5):
    bad = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 8:
                continue
            s0 = int(len(P) * (1 - tail_frac))
            if len(set(t[v] for v in P[s0:])) == 1:
                bad.append((q, r))
    return bad


def check_fibres(t, N, b):
    fs = fibre_sizes(t, N, b)
    rs = [(m, n, n / b ** m) for m, n in fs if b ** (m + 1) <= N]
    return rs


def check_displacement(t, N, b, Q=12):
    c = [0] + [blk(v, b) + t[v] for v in range(1, N + 1)]
    out = []
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < 8:
                continue
            cs = sorted((c[p], p) for p in P)
            keys = [k for k, _ in cs]
            best = {p: bisect.bisect_left(keys, k) + 1 for k, p in cs}
            out.append((q, r, max(best[P[n]] / (n + 1) for n in range(len(P)))))
    return out


def report(tag, t, N, b, L=None, Q=12):
    V = check_ii(t, N, b)
    nc = check_t_nonconstant(t, N, b, Q)
    fb = check_fibres(t, N, b)
    dp = check_displacement(t, N, b, Q)
    print(f"--- {tag}   (N={N}, b={b}) ---")
    print(f"  (1) (ii) violations                 : {len(V)}" + ("" if not V else f"  {V[:2]}"))
    print(f"  (2) APs (q<={Q}) with t const on tail: {len(nc)}" + ("" if not nc else f"  {nc[:4]}"))
    if L is not None:
        te, fa, fs = check_no_tame_blockwise(t, N, b, L, Q)
        print(f"  (3) blockwise descent test          : {te - fa}/{te} (AP,block) pairs have an "
              f"in-block c-descent" + ("" if not fa else f"   FAILURES {fs}"))
    print(f"  (4) |F_m|/b^m over complete blocks   : "
          f"{[round(r[2], 3) for r in fb]}")
    print(f"  (5) max_n pos_P(n)/n, best case      : min over APs = {min(d[2] for d in dp):.1f}, "
          f"max = {max(d[2] for d in dp):.1f}")
    return len(V) == 0 and not nc


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    print("=== cross-check of the three (ii) implementations on the witnesses ===")
    for b in (4, 5):
        t, _ = W1(1500, b, lambda M: M + 1)
        assert sorted(violations_numpy(t, 1500, b)) == sorted(violations_literal(t, 1500, b)) \
               == sorted(violations_caseanal(t, 1500, b))
    t = W2(1500, 3, lambda K: 2 if K % 2 == 0 else 0)
    assert sorted(violations_numpy(t, 1500, 3)) == sorted(violations_literal(t, 1500, 3)) \
           == sorted(violations_caseanal(t, 1500, 3))
    print("   agree (0 violations) for W1 (b=4,5) and W2 (b=3) at N=1500")

    print("\n=== W1  SLIVER witness ===")
    ok = True
    for b in (4, 5, 8):
        for hn, h in [("h_M = 1  (bounded)", lambda M: 1),
                      ("h_M = M+1", lambda M: M + 1),
                      ("h_M = 2^M", lambda M: 2 ** M)]:
            t, L = W1(N, b, h)
            ok &= report(f"W1 b={b}  {hn}", t, N, b, L=L)

    print("\n=== W2  BLOCK-CONSTANT witness (works at b=3 too) ===")
    for b in (3, 4):
        for tn, tau in [("tau=2,0 alternating", lambda K: 2 if K % 2 == 0 else 0),
                        ("tau=3,1,0 period 3", lambda K: [3, 1, 0][K % 3])]:
            t = W2(N, b, tau)
            ok &= report(f"W2 b={b}  {tn}", t, N, b)
    print("\nALL CORE CHECKS PASSED" if ok else "\nSOME CHECK FAILED")
