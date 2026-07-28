"""
A_theorem_A3.py

STATES AND MACHINE-CHECKS the following theorem, which is what the SAT/bookkeeping
experiments of Route A distilled into.  Everything below is elementary and needs NO search
over residues.

Notation.  E = {p-1 : p prime, p >= 5} (equivalently n >= 4 with n+1 prime); all n in E are
even.  D_E(L) = {n in E : n | L},  B_E(L) = sum_{n in D_E(L)} 1/n.

LEMMA A1 (parity split).  Suppose a_1 (mod n_1), ..., a_k (mod n_k) is a covering system
with n_i in E distinct.  Write n_i = 2 m_i.  A class a (mod 2m) contains only integers of
the parity of a, so putting M_c = {m_i : a_i = c (mod 2)} we get two DISJOINT families of
distinct moduli in H = {m >= 2 : 2m+1 prime}, and in the variable t (x = 2t resp. 2t+1)
each M_c is itself a covering system of Z.  Consequently
        sum_{m in M_c} 1/m > 1  for c = 0,1     [strict: Davenport-Mirsky-Newman-Rado],
        sum_{m in M_0} 1/m + sum_{m in M_1} 1/m <= 2 B_E(L)   [disjointness],
hence each half's EXCESS  X_c := sum_{m in M_c} 1/m - 1  satisfies  X_c < 2 B_E(L) - 2.

LEMMA A2 (forced overlap).  For a covering family with moduli M and any T subset M with
PAIRWISE COPRIME elements,
        X := sum_{m in M} 1/m - 1  >=  f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1-1/m).
Proof.  g(S) := sum_{m in S} 1/m - dens(union_{m in S} A_m) is non-decreasing in S (adding a
class raises the sum by 1/m and the union density by at most 1/m); g(M) = X since the union
is Z; and for pairwise coprime T the CRT makes the classes independent, so
dens(union_T) = 1 - prod_T (1 - 1/m) EXACTLY, whatever the residues are.  Hence X = g(M)
>= g(T) = f(T).                                                                        []

THEOREM A3.  Let 60 | L and  1 < B_E(L) <= 31/30.  Then NO covering system of Z with
distinct moduli, all in E, has lcm dividing L.

Proof.  4, 6, 10 are in E and divide L.  Every covering satisfies sum over used moduli of
1/n >= 1; if n_0 were unused this gives 1 <= B_E(L) - 1/n_0, i.e. 1/n_0 <= B_E(L) - 1 <=
1/30.  Since 1/4, 1/6, 1/10 all exceed 1/30, all three of 4, 6, 10 must be used.  By Lemma
A1 each of them lies in exactly one of the two halves; their halved moduli are 2, 3, 5.
Any two of 2, 3, 5 are coprime and
        f({2,3}) = 1/6,   f({2,5}) = 1/10,   f({3,5}) = 1/15,
all >= 1/15 >= 2 B_E(L) - 2.  So by Lemma A2 no two of 2, 3, 5 can lie in the same half:
that half would have excess >= 1/15 while Lemma A1 forces excess < 2B_E(L) - 2 <= 1/15.
Three objects in three pairwise distinct classes, but there are only two halves --
contradiction.                                                                          []

This script (i) re-verifies f({2,3}), f({2,5}), f({3,5}) in exact rational arithmetic,
(ii) sieves every L <= X, and reports how many of the L that survive the density bound
B_E(L) > 1 are killed outright by Theorem A3, and lists the survivors -- the only lcm
values <= X that a covering system for Erdos 273 could possibly have.

CONCLUSION: printed.
"""
import sys, os
from fractions import Fraction
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import is_prime, D_E, budget


def f_of(T):
    s = sum(Fraction(1, m) for m in T)
    pr = Fraction(1)
    for m in T:
        pr *= Fraction(m - 1, m)
    return s - 1 + pr


if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
    assert f_of((2, 3)) == Fraction(1, 6)
    assert f_of((2, 5)) == Fraction(1, 10)
    assert f_of((3, 5)) == Fraction(1, 15)
    print("f({2,3}) = 1/6, f({2,5}) = 1/10, f({3,5}) = 1/15   (exact)   OK")
    thr = Fraction(31, 30)
    print(f"Theorem A3 threshold: B_E(L) <= {thr} = {float(thr):.6f}")

    B = np.zeros(X + 1, dtype=np.float64)
    for n in range(4, X + 1):
        if is_prime(n + 1):
            B[n::n] += 1.0 / n
    idx = np.nonzero(B > 1.0 - 1e-9)[0]
    live, killed, survivors, not60 = 0, 0, [], []
    for L in idx:
        L = int(L)
        if L < 4:
            continue
        b = budget(D_E(L))
        if b <= 1:
            continue
        live += 1
        if L % 60:
            not60.append(L)
            continue
        if b <= thr:
            killed += 1
        else:
            survivors.append((L, float(b)))
    print(f"\nL <= {X}:")
    print(f"  {live} values of L survive the density bound B_E(L) > 1")
    print(f"  {len(not60)} of them are not divisible by 60 (Theorem A3 not applicable): "
          f"{not60}")
    print(f"  {killed} are killed outright by Theorem A3")
    print(f"  {len(survivors)} survive and would need an actual search:")
    for L, b in survivors:
        print(f"      L = {L:>9}   B_E = {b:.6f}   D_E size = {len(D_E(L))}")
