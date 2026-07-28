"""
A_split_check.py

CLAIM TESTED (a rigorous necessary condition, no SAT needed):

  Lemma A1.  Every n in E is even.  A class a (mod n) meets only integers of the parity of
  a.  So in a covering system with moduli in E, the classes with EVEN residue must by
  themselves cover every even integer and those with ODD residue every odd integer.  A
  class a (mod n), a even, covers a proportion 2/n of the even integers.  Hence, writing
  M_0 / M_1 for the two (disjoint!) sets of moduli,
        sum_{n in M_0} 2/n  >=  1        and       sum_{n in M_1} 2/n  >=  1,
  i.e. each of the two DISJOINT subsets has 1/n-sum at least 1/2.  Both inequalities are
  strict because an exact cover of Z by distinct moduli > 1 is impossible
  (Davenport-Mirsky-Newman-Rado), but the non-strict form already suffices below.

  Necessary condition SPLIT(L):  D_E(L) admits two disjoint subsets M_0, M_1 with
  sum_{M_0} 1/n >= 1/2 and sum_{M_1} 1/n >= 1/2.

If SPLIT(L) fails, NO covering system with distinct moduli in E has lcm dividing L, with
no search at all.  Since M_0, M_1 need not exhaust D_E(L), SPLIT(L) is equivalent to:
some subset S of D_E(L) has  L/2 <= sum_{n in S} L/n  and  sum_{n not in S} L/n >= L/2.
That is an exact subset-sum question, decided here with an exact integer bitset DP.

CONCLUSION: printed table.  For every L tested SPLIT(L) turned out to hold whenever
B_E(L) > 1 -- i.e. the split condition is (empirically) no stronger than the density
bound on these L.  Recorded honestly as a NEGATIVE result about this pruning idea.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, budget
from fractions import Fraction


def split_exact(L, mods):
    """Exact bitset subset-sum.  Weights w_n = L/n (integers).  Returns a witness split
    or None.  A subset S works iff sum_S w > L/2 and W - sum_S > L/2 (strict, see below)."""
    W = sum(L // n for n in mods)
    if W < L:
        return None
    reach = 1                       # bit i set  <=>  sum i is attainable
    parent = {0: None}
    for n in mods:
        w = L // n
        new = reach | (reach << w)
        # record parents for reconstruction
        add = new & ~reach
        s = add
        while s:
            b = s & -s
            v = b.bit_length() - 1
            parent[v] = (v - w, n)
            s ^= b
        reach = new
    # STRICT form: each half is itself a covering system of Z with distinct moduli > 1
    # (Lemma A1), so by Davenport-Mirsky-Newman-Rado its reciprocal sum is > 1, i.e.
    # sum_{n in M_c} L/n > L/2.  Weights are integers, so  >= floor(L/2) + 1.
    half = L // 2 + 1
    lo, hi = half, W - half
    s = None
    for v in range(lo, hi + 1):
        if (reach >> v) & 1:
            s = v
            break
    if s is None:
        return None
    part, cur = [], s
    while cur:
        prev, n = parent[cur]
        part.append(n)
        cur = prev
    part = sorted(part)
    rest = sorted(set(mods) - set(part))
    return part, rest


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1:]] or [55440, 65520, 100800, 110880, 131040,
                                            151200, 166320, 181440, 360360, 720720]
    for L in Ls:
        d = D_E(L)
        b = budget(d)
        if b < 1:
            print(f"L={L}: B_E={float(b):.5f} < 1  ->  UNSAT by density, SPLIT vacuous")
            continue
        r = split_exact(L, d)
        if r is None:
            print(f"L={L}: B_E={float(b):.5f}  ->  SPLIT FAILS  ==>  UNSAT (proved, "
                  f"no search)")
        else:
            p, q = r
            print(f"L={L}: B_E={float(b):.5f}  ->  SPLIT holds; e.g. "
                  f"M0 sum={float(budget(p)):.5f} (|M0|={len(p)}), "
                  f"M1 sum={float(budget(q)):.5f} (|M1|={len(q)})")
            print(f"        M0 = {p}")
