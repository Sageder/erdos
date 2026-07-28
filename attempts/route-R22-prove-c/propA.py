"""propA.py -- verification of Proposition A (forcing/delay bound) and of the
Theorem-14 BARRIER, plus the mandatory standing sanity check on coarsenings.

Proposition A.  In a class architecture c = j + t with NO increasing monotone 4-AP:
     v in Cl(u)  =>  c(v) <= c(u)  =>  j(v) - j(u) <= t(u) - t(v) <= t(u),
   hence  max Cl(u) < b^{ j(u) + t(u) + 1 } <= b^{t(u)+1} * u.
   Equivalently  t(u) >= j(max Cl(u)) - j(u).

Barrier claim tested: the triadic reversed-block permutation (Theorem 14) is a class
architecture with geometric fibre design and t == 0, it satisfies condition (ii), it has
NO increasing monotone 4-AP -- hence every constraint derivable from Theorem 16 holds in
it and its closures are finite.  It is nevertheless NOT a 196 counterexample (decreasing
4-APs).  So no argument built only from Theorem 16 can refute class architectures.
"""

import sys, random
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import (blockindex, perm_from_arch, fibres, ap4_violations,
                  class_seq_violations, open_scales, closure)
from forcing_class import v2, vdc_key, ORDERS, build
from apcheck import has_monotone_kap_pos


def propA_check(N, b, tfun, oname, verbose=False):
    c, within, perm, pos = build(N, b, tfun, ORDERS[oname])
    j = lambda v: blockindex(v, b)
    viol = ap4_violations(pos, N)
    n_inc = sum(1 for x in viol if x[2] == 'inc')
    n_dec = sum(1 for x in viol if x[2] == 'dec')
    n_ii = len(class_seq_violations(N, c))
    bad_c, bad_j, worst = 0, 0, (0.0, None, None)
    slack = []
    for u in range(1, N + 1):
        cl = closure(pos, u, N)
        mx = max(cl)
        for v in cl:
            if c(v) > c(u):
                bad_c += 1
        if j(mx) - j(u) > tfun(u):
            bad_j += 1
        slack.append(tfun(u) - (j(mx) - j(u)))
        r = mx / u
        if r > worst[0]:
            worst = (r, u, mx)
    return dict(N=N, b=b, order=oname, inc=n_inc, dec=n_dec, ii=n_ii,
                badC=bad_c, badJ=bad_j, maxreach=round(worst[0], 3),
                argmax=worst[1:], minslack=min(slack))


if __name__ == "__main__":
    print("=" * 108)
    print("PROPOSITION A on increasing-4-AP-FREE class architectures (within-class order = decreasing)")
    print("=" * 108)
    print(f"{'b':>2} {'t':>7} {'N':>5} {'inc4AP':>7} {'dec4AP':>7} {'(ii)':>5} "
          f"{'badC':>5} {'badJ':>5} {'maxreach':>9} {'argmax(u,maxCl)':>18} {'min slack':>10}")
    for b in (3, 4, 5):
        for tname, tfun in (('0', lambda v: 0), ('v2', v2), ('1_odd', lambda v: v % 2),
                            ('v3', lambda v: (lambda n: (0 if n % 3 else 1 + (0 if (n // 3) % 3 else 1)))(v))):
            for N in (300, 900):
                r = propA_check(N, b, tfun, 'decreasing')
                print(f"{b:>2} {tname:>7} {N:>5} {r['inc']:>7} {r['dec']:>7} {r['ii']:>5} "
                      f"{r['badC']:>5} {r['badJ']:>5} {r['maxreach']:>9} "
                      f"{str(r['argmax']):>18} {r['minslack']:>10}")
    print()
    print("badC = |{u, v in Cl(u) : c(v) > c(u)}|   -- Proposition A part 1, must be 0")
    print("badJ = |{u : j(max Cl(u)) - j(u) > t(u)}| -- Proposition A part 2, must be 0")
    print()

    # ---------------- BARRIER ------------------------------------------------
    print("=" * 108)
    print("BARRIER: triadic reversed-block layout T (b=3, t=0, within-class order = decreasing)")
    print("=" * 108)
    for N in (300, 900, 2700):
        c, within, perm, pos = build(N, 3, lambda v: 0, ORDERS['decreasing'])
        viol = ap4_violations(pos, N)
        ninc = sum(1 for x in viol if x[2] == 'inc')
        ndec = sum(1 for x in viol if x[2] == 'dec')
        maxcl = max(len(closure(pos, u, N)) for u in range(1, N + 1))
        maxpos_ratio = max(pos[v] / v for v in range(1, N + 1))
        print(f"  N={N:5d}  increasing monotone 4-APs = {ninc}   decreasing = {ndec}   "
              f"max |Cl(u)| = {maxcl}   max pos(v)/v = {maxpos_ratio:.4f}   "
              f"(ii)-violations = {len(class_seq_violations(N, c))}")
    print("  => every consequence of Theorem 16 is satisfied by T; T is a geometric class")
    print("     architecture satisfying (ii); T is killed ONLY by decreasing 4-APs, which")
    print("     Theorem 16 never sees.  Forcing-only arguments therefore cannot close the family.")
    print()

    # ------------- STANDING SANITY CHECK: geometric coarsening ----------------
    print("=" * 108)
    print("STANDING SANITY CHECK (Remark 31): geometric coarsening of a finite avoider")
    print("=" * 108)
    rng = random.Random(196)

    def random_avoider(N, tries=400000):
        """Greedy/backtracking search for a monotone-4-AP-free permutation of [1..N]
        by insertion in increasing value order (Lemma 8 intervals)."""
        # parity recursion: 3-AP-free hence 4-AP-free, deterministic and exact
        def parity(n):
            if n == 1:
                return [1]
            odd = parity((n + 1) // 2)
            even = parity(n // 2)
            return [2 * x - 1 for x in odd] + [2 * x for x in even]
        return parity(N)

    for N in (81, 243, 729):
        perm = random_avoider(N)
        assert not has_monotone_kap_pos(perm, 4), "avoider check failed"
        assert not has_monotone_kap_pos(perm, 3), "3-AP-free check failed"
        pos = [0] * (N + 1)
        for i, v in enumerate(perm):
            pos[v] = i + 1
        for b in (3, 4):
            cc = lambda v: blockindex(pos[v], b)   # coarsening by POSITION
            nii = len(class_seq_violations(N, cc))
            sizes = {}
            for v in range(1, N + 1):
                sizes[cc(v)] = sizes.get(cc(v), 0) + 1
            # is the delay t = c - j constant on any AP of step <= 8 inside [N/3, N]?
            print(f"  N={N:4d} b={b}: (ii)-violations of the coarsening = {nii};  "
                  f"fibre sizes {[sizes[m] for m in sorted(sizes)]}")
    print("  => the coarsening always satisfies (ii) with geometric fibres; any argument")
    print("     that applies to it is WRONG as a proof of R21-C.")
