"""thresholds.py — minimal N at which each (numeration system, priority) family goes
extinct, reported as a BRACKETING SAT/UNSAT pair (per REQUIREMENTS Part C).

Downward inheritance justifying the binary search: the clause set at board size N-1 is a
sub-multiset of the one at N (every 4-AP inside [1..N-1] is a 4-AP inside [1..N]) and the
digit alphabets only shrink, so SAT at N implies SAT at N-1.  Verified empirically below
by checking SAT at (threshold-1) and UNSAT at (threshold).
"""
import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from levelsat import run
from numeration import (base_digits, factorial_digits, zeck_digits, fibs_upto,
                        ostrowski_digits, ostrowski_denoms)

NMAX = 260


def mk(nm):
    F = fibs_upto(4 * NMAX)
    cf_p = [2] * 40
    qp = ostrowski_denoms(cf_p, 4 * NMAX)
    cf_t = [3] * 40
    qt = ostrowski_denoms(cf_t, 4 * NMAX)
    cf_e = [1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12, 1, 1, 14, 1, 1, 16]
    qe = ostrowski_denoms(cf_e, 4 * NMAX)
    tbl = {
        "base 2": lambda v: base_digits(v, 2),
        "base 3": lambda v: base_digits(v, 3),
        "base 4": lambda v: base_digits(v, 4),
        "base 5": lambda v: base_digits(v, 5),
        "base 6": lambda v: base_digits(v, 6),
        "factorial base": factorial_digits,
        "Zeckendorf (phi)": lambda v: zeck_digits(v, F),
        "Ostrowski sqrt2": lambda v: ostrowski_digits(v, cf_p, qp),
        "Ostrowski [3,3,..]": lambda v: ostrowski_digits(v, cf_t, qt),
        "Ostrowski e-like": lambda v: ostrowski_digits(v, cf_e, qe),
    }
    return tbl[nm]


def threshold(nm, pri, hi=NMAX):
    fn = mk(nm)
    v, _ = run(nm, fn, hi, pri, verbose=False)
    if v == "SAT":
        return None, hi
    lo = 4
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        v, _ = run(nm, fn, mid, pri, verbose=False)
        if v == "SAT":
            lo = mid
        else:
            hi = mid
    return lo, hi


if __name__ == "__main__":
    print("system                  priority   SAT at N   UNSAT at N   (2 solvers agree at both)")
    for nm in ["base 2", "base 3", "base 4", "base 5", "base 6", "factorial base",
               "Zeckendorf (phi)", "Ostrowski sqrt2", "Ostrowski [3,3,..]",
               "Ostrowski e-like"]:
        for pri in ("lsd", "msd"):
            lo, hi = threshold(nm, pri)
            if lo is None:
                print(f"{nm:22s} {pri:8s}   survives to N={hi} (no extinction found)")
            else:
                fn = mk(nm)
                _, r1 = run(nm, fn, lo, pri, verbose=False)
                _, r2 = run(nm, fn, hi, pri, verbose=False)
                ag = (r1['cadical'] == r1['glucose']) and (r2['cadical'] == r2['glucose'])
                rv = r1.get('reverify', '-')
                print(f"{nm:22s} {pri:8s}   {lo:6d}     {hi:6d}       agree={ag} "
                      f"witness-recheck@SAT={rv}")
