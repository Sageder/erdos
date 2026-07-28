"""hunt2.py — annulus delays, done properly.

t(v) = 1 iff  A <= v/b^{j(v)} < B,  with 1 < A < B < b  (STRICT: so every block
contains values with t=0 both below and above the annulus, hence neither level set
contains an infinite AP, hence t is constant on NO infinite AP).

Reports for each surviving (A,B):
  * first (ii)-violation up to N (None = survives)
  * tameness diagnostics: for each AP P (q<=qmax, residue r), does c|_P have a strict
    DESCENT in the last third of [1..N]?  (a descent of c along P is necessary for
    P to be non-tame; if some AP has no descent at all in the tail, that AP is the
    tame one Prop 29 needs.)
"""
import sys
from fractions import Fraction
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from local import jtable, four_aps                                    # noqa: E402
from hunt1 import scale_t, first_violation                            # noqa: E402


def tame_report(c, N, qmax=12, tailfrac=Fraction(2, 3)):
    """returns list of (q,r) whose AP has NO strict descent of c beyond N*tailfrac."""
    lo = int(N * tailfrac)
    tame = []
    for q in range(1, qmax + 1):
        for r in range(q):
            el = list(range(r if r >= 1 else q, N + 1, q))
            if len(el) < 6:
                continue
            desc = any(c[el[i + 1]] < c[el[i]] for i in range(len(el) - 1)
                       if el[i] >= lo)
            if not desc:
                tame.append((q, r))
    return tame


def main(b, N, qmax=12):
    J = jtable(N, b)
    dens = [1, 2, 3, 4, 5, 6]
    cands = set()
    for da in dens:
        for na in range(da + 1, b * da):
            A = Fraction(na, da)
            if A <= 1 or A >= b:
                continue
            for db in dens:
                for nb in range(db + 1, b * db):
                    B = Fraction(nb, db)
                    if B <= A or B >= b:
                        continue
                    cands.add((A, B))
    survivors = []
    for (A, B) in sorted(cands):
        t = scale_t(b, A, B, N, J)
        if sum(t[1:]) == 0 or sum(t[1:]) == N:
            continue
        r = first_violation(t, b, N, J)
        if r is None:
            c = [0] + [J[v] + t[v] for v in range(1, N + 1)]
            tm = tame_report(c, N, qmax)
            survivors.append((A, B, len(tm), tm[:6]))
    print(f"b={b} N={N}: {len(survivors)} annulus delays with 1<A<B<b survive (ii)")
    for s in survivors:
        print(f"   A={s[0]} B={s[1]}  #tame-APs(q<={qmax}) = {s[2]}  {s[3]}")
    return survivors


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    for b in (3, 4, 5, 6):
        main(b, N)
