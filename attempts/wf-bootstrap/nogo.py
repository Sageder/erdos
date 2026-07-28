#!/usr/bin/env python3
r"""
nogo.py -- NEGATIVE THEOREMS about sum-preserving substitution rules, with
symbolic/exhaustive corroboration.  All statements below are PROVED; the code
only re-checks the algebra on examples (a check is never the proof).

--------------------------------------------------------------------------
SETTING.
A *legal system* is a finite S ⊆ Z_{≥2} with no isolated point; equivalently a
disjoint union of blocks (runs of consecutive integers) of length ≥ 2.
Σ(S) = Σ_{n∈S} 1/n.

LEMMA 0 (UNION).  S, S' legal ⟹ S ∪ S' legal.  If S ∩ S' = ∅ then
Σ(S ∪ S') = Σ(S) + Σ(S').
Proof: every n ∈ S keeps its S-neighbour inside S ∪ S'. ∎
Consequence: legality is FREE under unions; in any construction the only real
constraints are DISJOINTNESS and EXACTNESS.

DEFINITION (blockwise map).  Let B be the set of blocks.  A *substitution rule*
is a partial map ψ : B → {legal systems}.  It acts on a legal U with maximal
runs R_1,…,R_r by Φ(U) := ⋃_i ψ(R_i), and is *admissible on U* when the ψ(R_i)
are pairwise disjoint.

LEMMA 1 (REDUCTION).  Φ preserves Σ on every legal U on which it is admissible
⟺ Σ(ψ(B)) = Σ(B) for every block B ∈ dom ψ.
Proof: (⟸) Lemma 0.  (⟹) a single block is itself a legal system. ∎

So the class of blockwise sum-preserving maps is *exactly* the set of solutions
of the

        LIFT PROBLEM:  given a block [a,b] and a threshold M, is
        H(a,b) = Σ_{n=a}^b 1/n the reciprocal sum of a legal system S
        with min S ≥ M ?

--------------------------------------------------------------------------
THEOREM A (no uniform linear substitution rule).  PROVED, no bound.

Let k ≥ 1, and let a_1,…,a_k be positive integers and b_1,…,b_k integers.  If

        Σ_{i=1}^k 1/(a_i n + b_i) = 1/n                                  (*)

holds for infinitely many integers n, then b_i = 0 for every i and Σ_i 1/a_i = 1.

Proof.  Both sides are elements of Q(n); an identity of rational functions at
infinitely many points is an identity.  Each summand has a simple pole at
α_i := −b_i/a_i with residue 1/a_i > 0.  For a fixed α, the residue of the left
side at α is Σ_{i : α_i = α} 1/a_i, a sum of POSITIVE numbers, hence ≠ 0: no
pole of any summand can be cancelled.  Therefore the pole set of the left side
is exactly {α_i}.  The right side has the single pole 0, so α_i = 0, i.e.
b_i = 0, for all i; then (*) reads (Σ 1/a_i)/n = 1/n. ∎

COROLLARY A1 (the block form; this is the one that matters).  There is NO
substitution rule of the shape
        n  ⟼  ⋃_{i=1}^k [a_i n + b_i , a_i n + c_i],   c_i ≥ b_i + 1,
        a_i ≥ 1, with Σ of the image = 1/n for infinitely many n.
Proof.  The image elements are the linear forms a_i n + b_i + j, 0 ≤ j ≤ c_i−b_i.
Apply Theorem A to that list: every offset must vanish, i.e. b_i + j = 0 for
every 0 ≤ j ≤ c_i − b_i ≥ 1 — two different values of j give two different
offsets, both forced to be 0.  Contradiction. ∎

COROLLARY A2 (periodic rules).  The same holds if the rule is only required to
be uniform on an arithmetic progression n ≡ s (mod M): substitute n = Mm + s;
a_i n + b_i = (a_i M) m + (a_i s + b_i) is again linear in m with positive
leading coefficient, and 1/n = 1/(Mm+s) has the single pole m = −s/M.  The
residue argument gives (a_i s + b_i)/(a_i M) = s/M, i.e. b_i = 0 for all forms
occurring, and Corollary A1's contradiction reappears. ∎

SCOPE.  Corollary A1 kills, in one line and with NO computational bound, every
parametric family attempted in this project:
  * the doubling map n ↦ {2n, 2n+1} / {2n−1, 2n}      (a=2, b∈{0,−1});
  * the c-maps n ↦ {cn, cn+1} / {cn−1, cn}, c ≥ 3;
  * blow-ups n ↦ [qn−d+s, qn+d+s];
  * ANY rule "replace n by blocks sitting at fixed offsets from fixed multiples
    of n", with any number of blocks, any colouring, any period.
It does NOT cover rules whose forms are nonlinear in n (see Theorem B) or rules
that are not uniform in n at all (the LIFT tables; those are the live case).

--------------------------------------------------------------------------
THEOREM B (polynomial rules: what survives).
Let g_1,…,g_m ∈ R[n] have positive leading coefficients, let L_t ≥ 1 and suppose
        Σ_{t=1}^m Σ_{j=0}^{L_t−1} 1/(g_t(n)+j) = 1/n   in R(n).           (**)
Then:
 (B1) no g_t + j has a positive real root.
 (B2) min_t deg g_t = 1.
Proof.  (B1) Let β > 0 be the largest positive real root of Π_{t,j}(g_t+j) if
one exists.  For n > β every factor is > 0 (positive leading coefficients and no
larger real root).  Let n ↓ β: every term whose denominator vanishes at β tends
to +∞ and no term tends to −∞, while 1/n → 1/β is finite.  Contradiction.
 (B2) Multiply (**) by n and let n → +∞: n·Σ → Σ_{t : deg g_t = 1} L_t/lc(g_t),
which must equal 1, so at least one g_t is linear; and no g_t can be constant
because a constant term contributes a nonzero constant to the left side. ∎

REMARK (why Theorem B cannot be pushed to a full no-go).  Nonlinear rules DO
exist if blocks of length 1 are allowed — the classical splitting
        1/n = 1/(n+1) + 1/(n(n+1))
is exactly such a rule (g_1 = n+1, g_2 = n²+n, L_1 = L_2 = 1).  This is the
precise reason "no local map can work" is FALSE as stated in general: what fails
is the LINEAR case (Theorem A).  Whether a polynomial rule with all L_t ≥ 2
exists is decided, for small degrees and coefficients, by polyrule.py.
"""
import sys
from fractions import Fraction

try:
    import sympy as sp
except Exception:
    sp = None


def check_theoremA_instances(amax=8, bmax=4, kmax=4):
    """Corroborate Theorem A by brute force.  EXACT: the difference
    F(n) = sum_i 1/(a_i n + b_i) - 1/n is a rational function whose numerator
    has degree <= k (denominator degree k+1); vanishing at k+2 distinct points
    where no denominator vanishes therefore forces F == 0."""
    import itertools
    hits = []
    forms = [(a, b) for a in range(1, amax + 1) for b in range(-bmax, bmax + 1)]
    for k in range(1, kmax + 1):
        pts = [10 ** 4 + 7 * j for j in range(k + 6)]     # no denominator vanishes
        for combo in itertools.combinations_with_replacement(forms, k):
            ok = True
            for n0 in pts:
                s = -Fraction(1, n0)
                for a, b in combo:
                    d = a * n0 + b
                    if d == 0:
                        ok = False; break
                    s += Fraction(1, d)
                if not ok or s != 0:
                    ok = False; break
            if ok:
                hits.append(combo)
    return hits


def check_A1_legality(hits):
    """For each identity found, check it is never legal: no two image elements
    are consecutive for n >= 2 (checked as polynomial identities)."""
    bad = []
    for combo in hits:
        legalpossible = False
        for (a, b) in combo:
            for (c, d) in combo:
                if (a, b) != (c, d) and a == c and abs(b - d) == 1:
                    legalpossible = True
        if legalpossible:
            bad.append(combo)
    return bad


if __name__ == "__main__":
    if sp is None:
        print("sympy unavailable"); sys.exit(1)
    hits = check_theoremA_instances()
    print("linear identities sum 1/(a n + b) = 1/n with a<=6,|b|<=3,k<=3:")
    for h in hits:
        print("   ", h)
    print("all have every b = 0 :", all(b == 0 for h in hits for (a, b) in h))
    print("any with two forms differing by 1 (i.e. possibly legal):",
          check_A1_legality(hits))
