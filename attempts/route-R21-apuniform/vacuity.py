"""vacuity.py — is the literal AP-uniformity optimisation on a finite board vacuous?

Claim tested (Proposition R21-1 in REPORT): on a finite board, EVERY monotone-4-AP-free
permutation already achieves AP-uniformity at the level forced by the restriction
principle, and the *maximum* of the min-over-APs displacement is ~N/q, reached by the
trivial device of positioning the values 1..qmax last.  Hence neither outcome the R21
mission anticipated (a nontrivial optimum, or certified infeasibility) can arise from the
literal encoding.

Three measurements:
  A. AP-uniformity of avoiders produced for other purposes (R20 witnesses) and of fresh
     unconstrained CEGAR avoiders.
  B. the "delay the first qmax values" device: SAT search for an avoider of [1..N] whose
     values 1..8 occupy the last 8 positions; measure the resulting AP-uniformity.
  C. the automatic lower bound gamma(M) from the certified extinction thresholds.
"""

import sys, time, ast
from fractions import Fraction

sys.path.insert(0, '/home/user/erdos/attempts/route-R21-apuniform')
from apdisp import ap_uniformity, ap_report, pos_of, all_aps, displacement  # noqa: E402
from engine import OrderEncoding, solve, verify_avoider                     # noqa: E402
from apcheck import has_monotone_kap_pos                                    # noqa: E402

# certified extinction thresholds N*(C) (CORE.md Remark 17): no C-bounded monotone-4-AP-
# free permutation of [1..N*] exists.  gamma(M) := min over avoiders of [1..M] of
# max_v pos(v)/v  satisfies gamma(M) > C whenever M >= N*(C).
CERTS = [(Fraction(5, 4), 4), (Fraction(3, 2), 15), (Fraction(7, 4), 31), (Fraction(2), 90)]


def gamma_lower_bound(M):
    """largest certified C with N*(C) <= M, i.e. gamma(M) > C."""
    best = None
    for C, Nstar in CERTS:
        if M >= Nstar:
            best = C
    return best


def measure(perm, tag, qmax=8):
    N = len(perm)
    u_all, who_all, n_all = ap_uniformity(perm, qmax=qmax, theta=Fraction(0))
    u_tail, who_tail, n_tail = ap_uniformity(perm, qmax=qmax, theta=Fraction(1, 2))
    pos = pos_of(perm)
    glob = max(Fraction(pos[v], v) for v in range(1, N + 1))
    print(f"{tag:34s} N={N:4d}  minAPdisp={float(u_all):7.3f} (AP q={who_all[0]},r={who_all[1]}, n={n_all})"
          f"  tail(min,n>=L/2)={float(u_tail):7.3f}  global max pos/v={float(glob):6.3f}")
    return u_all, u_tail, glob


if __name__ == "__main__":
    print("=== C. automatic lower bound from certified extinctions ===")
    for M in (4, 15, 31, 90, 200, 1000):
        g = gamma_lower_bound(M)
        print(f"  every monotone-4-AP-free permutation of [1..{M}] has max_n pos(n)/n > "
              f"{g if g is not None else '(no certificate)'}")
    print("  => by the restriction principle the same bound holds for EVERY AP")
    print("     restriction of length >= M, for every finite avoider.\n")

    print("=== A. AP-uniformity of avoiders built for other purposes ===")
    import os
    R20 = '/home/user/erdos/attempts/route-R20-vlogv'
    for fn in ('wit_N90_a0.5.txt', 'cw_CLS(5,a)_250.txt', 'cw_CLS(3,a)_160.txt'):
        p = os.path.join(R20, fn)
        if not os.path.exists(p):
            continue
        perm = ast.literal_eval(open(p).read().strip())
        if sorted(perm) != list(range(1, len(perm) + 1)):
            print(f"  (skip {fn}: not a permutation of an initial segment)")
            continue
        assert not has_monotone_kap_pos(perm, 4), fn
        measure(perm, f"R20 {fn}")

    print("\n  fresh unconstrained CEGAR avoiders:")
    for N in (60, 120, 200):
        enc = OrderEncoding(N)
        enc.no_monotone_4ap()
        t0 = time.time()
        res, perm, rounds = solve(enc, time_budget=500)
        assert res == "SAT", (N, res)
        verify_avoider(perm, N)
        measure(perm, f"unconstrained CEGAR ({time.time()-t0:.0f}s)")

    print("\n=== B. the 'delay the first qmax values' device ===")
    for N in (60, 120, 200):
        enc = OrderEncoding(N)
        enc.no_monotone_4ap()
        small = list(range(1, 9))
        enc.before_all(small, [w for w in range(9, N + 1)])
        t0 = time.time()
        res, perm, rounds = solve(enc, time_budget=800)
        dt = time.time() - t0
        if res != "SAT":
            print(f"  N={N}: {res} ({dt:.0f}s)")
            continue
        verify_avoider(perm, N)
        assert set(perm[-8:]) == set(small), perm[-8:]
        u, tail, glob = measure(perm, f"1..8 last ({dt:.0f}s)")
        open(f"/home/user/erdos/attempts/route-R21-apuniform/wit_last8_N{N}.txt",
             "w").write(repr(perm))
