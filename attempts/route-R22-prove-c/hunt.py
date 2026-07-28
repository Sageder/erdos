"""hunt.py -- machine hunt for a REFUTATION of R21-C' ("condition (ii) forces the delay
to be bounded on some infinite AP").

Two probes.

PROBE 1 (explicit rules).  A battery of explicit delays t : N -> Z_{>=0} defined by a
formula (hence genuinely infinite objects).  For each we measure
   * # condition-(ii) violations on [1..N],
   * whether t is bounded on some AP of step q <= Q inside the top half of [1..N]
     (a NECESSARY condition for R21-C' to be witnessed at reachable sizes),
   * fibre sizes |F_m| / b^m (the geometric-design test).
A rule that has ZERO (ii)-violations and is unbounded on every AP would be a candidate
refutation of R21-C' and would then have to be PROVED, not measured.

PROBE 2 (delay-height scaling, the honest finite proxy).  R21-C' is vacuous for any
FIXED finite range of t, so the proxy must let the range grow with N.  For each N we ask
a SAT solver for the largest K such that there is t : [1..N] -> {0..K} with
   (a) condition (ii) on every 4-AP inside [1..N],
   (b) t(v) = 0 somewhere in every window of L0 consecutive integers
       (a sufficient condition for the geometric fibre lower bound |F_m| >~ b^m/L0),
   (c) max t >= K on every window of L consecutive elements of every AP of step q <= Q
       inside [N/2, N]  (a RATE proxy for "t is unbounded along every AP", per Remark 36).
K(N) growing => evidence AGAINST R21-C'; K(N) flat => evidence FOR it.
Neither direction is a proof (Remarks 27, 31).
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex, class_seq_violations


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


# ----------------------------------------------------------------- PROBE 1

def make_delays(b):
    D = {}
    D['t=0'] = lambda v: 0
    D['t=1_odd'] = lambda v: v % 2
    D['t=v2'] = lambda v: vp(v, 2)
    D['t=v3'] = lambda v: vp(v, 3)
    D['t=v5'] = lambda v: vp(v, 5)
    D['t=vb'] = lambda v: vp(v, b)
    D['t=min(v2,2)'] = lambda v: min(vp(v, 2), 2)
    D['t=v2(v)+v3(v)'] = lambda v: vp(v, 2) + vp(v, 3)
    # "moving valuation": the 2-adic origin is shifted by a block-dependent amount.
    # unbounded along EVERY AP of odd step (each block contains a full residue system)
    D['t=v2(v-1) blk-shift'] = lambda v: vp(v - blockindex(v, b), 2) if v - blockindex(v, b) > 0 else 0
    D['t=v2(v-b^j)'] = lambda v: vp(v - b ** blockindex(v, b), 2) if v > b ** blockindex(v, b) else 0
    D['t=v2 or v3 by blk'] = lambda v: vp(v, 2) if blockindex(v, b) % 2 == 0 else vp(v, 3)
    D['t=v_{p(j)}'] = lambda v: vp(v, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41][blockindex(v, b) % 13])
    D['t=bitcount(v)'] = lambda v: bin(v).count('1')
    D['t=v2(v)*1_{j even}'] = lambda v: vp(v, 2) if blockindex(v, b) % 2 == 0 else 0
    D['t=j(v) (c=2j)'] = lambda v: blockindex(v, b)
    D['t=j//2'] = lambda v: blockindex(v, b) // 2
    return D


def ap_boundedness(tf, N, Q=8, lo_frac=0.5):
    """For each AP of step q<=Q, max of t over the top (1-lo_frac) part of [1..N].
    Returns the MINIMUM over all APs (small => some AP has small delay => R21-C' witnessed
    at this size) and the argmin."""
    lo = int(N * lo_frac)
    best = None
    for q in range(1, Q + 1):
        for r in range(q):
            vals = [tf(v) for v in range(lo, N + 1) if v % q == r % q]
            if len(vals) < 10:
                continue
            m = max(vals)
            if best is None or m < best[0]:
                best = (m, q, r)
    return best


def fibre_profile(tf, b, N):
    F = {}
    for v in range(1, N + 1):
        m = blockindex(v, b) + tf(v)
        F[m] = F.get(m, 0) + 1
    mmax = blockindex(N, b)          # only fibres that are certainly complete
    prof = []
    for m in range(0, mmax):
        prof.append(round(F.get(m, 0) / b ** m, 3))
    return prof


if __name__ == "__main__":
    N = 4000
    print("=" * 112)
    print(f"PROBE 1: explicit delay rules, N = {N}, Q = 8 (AP steps), top half of the range")
    print("=" * 112)
    for b in (3, 4, 5):
        print(f"\n--- b = {b} ---")
        print(f"{'rule':>24} {'(ii) viol':>10} {'min-over-AP max t':>18} {'argmin (q,r)':>13} "
              f"{'|F_m|/b^m profile (m=0..)':>30}")
        for name, tf in make_delays(b).items():
            c = lambda v, tf=tf, b=b: blockindex(v, b) + tf(v)
            nviol = len(class_seq_violations(min(N, 1200), c))
            bb = ap_boundedness(tf, N, Q=8)
            prof = fibre_profile(tf, b, N)
            print(f"{name:>24} {nviol:>10} {bb[0]:>18} {str(bb[1:]):>13} "
                  f"{str(prof[:7]):>30}")
    print()
    print("Reading: a refutation of R21-C' needs (ii) viol = 0, an unbounded")
    print("'min-over-AP max t' as N grows, and a fibre profile bounded away from 0 and inf.")
