# route-FRESH — an independent attack on Erdős 196

Worked from `PROBLEM.md` only (deliberately no other project notes read). All code in this
directory; every asserted claim is machine-checked by `verify_all.py` (all checks pass) and every
checker is cross-validated against `experiments/apcheck.py`. Exact integer arithmetic throughout.

**Headline.** The best new thing here is a three-line structural theorem:

> **Theorem 4.** If a permutation of ℕ has no monotone 4-AP, then its set of **left-to-right maxima
> (records)** contains no 3-term arithmetic progression. More generally, no monotone *k*-AP implies
> the record set contains no (*k*−1)-term AP; the case *k*=3 says the record set has ≤1 element,
> which is impossible, so this *reproves the Davis–Entringer–Graham–Simmons 3-AP theorem in three
> lines*. Moreover the same holds for the record set of the restriction of the permutation to **every**
> infinite AP.

This converts "order type ω" into a statement about a *single, canonically defined, infinite,
3-AP-free set*, and connects the problem to Roth/Behrend-type structure rather than to digit or
block constructions. It is not by itself a proof — I show below exactly why, and what it would take.

The second contribution is negative and, I think, useful: I identify the natural "one base point"
reduction of the problem and **prove it cannot work**, with an explicit counterexample.

---

## 0. Notation

`a : ℕ → ℕ` is the permutation, `p = a⁻¹` the **position function** (`p(v)` = position of value `v`).
`A_n := a({1,…,n})` = the set of values in the first `n` positions. For `e ≥ 1` define the **sign
sequence**  `ε_e(y) := sign( p(y+e) − p(y) ) ∈ {+,−}`,  `y ≥ 1`.
A **record** is a value `u` larger than every value before it; equivalently `p(u) < p(w)` for every
`w > u`. `U` denotes the set of records.

---

## PROVED

### Prop 1 (run-length reformulation). *[machine-checked; probably standard]*
`a` contains a monotone *k*-AP **iff** for some `e ≥ 1` and some `y ≥ 1` the `k−1` signs
`ε_e(y), ε_e(y+e), …, ε_e(y+(k−2)e)` are all equal.

*Proof.* The quadruple `x, x+d, x+2d, x+3d` is monotone in position iff the three consecutive
comparisons agree in sign; transitivity of `<` does the rest. ∎

So the ladder of Erdős's problem is a ladder of **run lengths**: "no monotone *k*-AP" = "for every
`e`, the sign sequence `ε_e` restricted to each residue class mod `e` has no run of `k−1` equal
signs." *k*=3 is run-length ≤1 (perfect alternation) — impossible [DEGS77]; *k*=5 is run-length ≤3 —
possible [DEGS77]; **the open case is run-length ≤2**. This makes the problem look like a
*bounded-run-length* condition holding simultaneously in every arithmetic scale.

### Lemma 2 (backward closure). *[machine-checked]*
`a` has no monotone 4-AP **iff** (i) every increasing monotone 3-AP `p(y)<p(y+e)<p(y+2e)` has
`p(y+3e) < p(y+2e)`, and (ii) every decreasing monotone 3-AP `p(y+2e)<p(y+e)<p(y)` with `y−e ≥ 1`
has `p(y−e) < p(y)`.
**Corollary.** Every prefix set `A_n` is closed under continuation of increasing 3-APs.
**Asymmetry worth noting:** the increasing continuation `y+3e` always exists, the decreasing one
`y−e` may fall below 1. One-sidedness of ℕ lives exactly here, and it is why "decreasing 3-APs near
the bottom are free".

### Lemma 3 (permanent blocking). *[machine-checked]*
When building `a` left to right, a value `v` may be appended iff no already-placed monotone 3-AP has
continuation `v`. Blocking is monotone in time, hence permanent. So a monotone-4-AP-free permutation
of ℕ is exactly an infinite play of a solitaire game with self-generated deadlines
(`core.py::Builder` implements this and agrees with `apcheck.py` on all tested inputs).

### Theorem 4 (RECORDS — the main new idea). *[proof below; exhaustively machine-checked on all 70 378 monotone-K-AP-free permutations of [1..N], N ≤ 8, K = 3,4,5]*
Let `a` be a permutation of ℕ with no monotone *k*-AP (`k ≥ 3`). Then:
1. `U` (the record set) is **infinite**;
2. `U` contains **no (k−1)-term arithmetic progression**.

*Proof.* (1) For any `x`, the set `{p(w) : w > x}` is a nonempty set of positive integers, so it has
a least element, attained at some `u > x`. Every `w > u` satisfies `w > x`, `w ≠ u`, hence
`p(w) > p(u)`: so `u ∈ U` and `u > x`. Thus `U` is unbounded. (This is the *only* place where order
type ω is used — well-ordering of positions.)
(2) Suppose `u_1 < u_2 < … < u_{k−1}` lie in `U` and form an AP with difference `δ`. For `i<j`,
`u_j > u_i` and `u_i ∈ U` give `p(u_i) < p(u_j)`; so positions increase along the AP. Also
`u_{k−1}+δ > u_{k−1} ∈ U` gives `p(u_{k−1}+δ) > p(u_{k−1})`. Hence
`u_1 < u_2 < … < u_{k−1} < u_{k−1}+δ` is a monotone increasing *k*-AP. Contradiction. ∎

**Corollary 4a (new 3-line proof of the DEGS 3-AP theorem).** For `k=3`, (2) says `U` has no 2-term
AP, i.e. `|U| ≤ 1`, contradicting (1). Hence every permutation of ℕ contains a monotone 3-AP.

**Corollary 4b.** In a monotone-4-AP-free permutation, `U` is an infinite 3-AP-free set, so by Roth
it has density 0: **records must be sparse** (Behrend-like or lacunary); e.g. `U = {2^j}` is allowed.

**Theorem 4' (self-similar version).** *[machine-checked exhaustively, same range]* For every infinite
AP `S`, the restriction `a|_S` is again a monotone-4-AP-free permutation of order type ω, so *its*
record set `U_S := {u ∈ S : p(u) < p(w) ∀ w ∈ S, w > u}` is an infinite 3-AP-free subset of `S`.
(`U ∩ S ⊆ U_S`, so this is strictly more information than Theorem 4.)

### Lemma 5 (restriction / normalisation).
(i) The restriction of a monotone-4-AP-free permutation of ℕ to any infinite AP or to any tail
`[u,∞)`, read in position order and renormalised affinely, is again one. (APs are affine-invariant,
and any subset of an ω-order is an ω-order.)
(ii) **Normalisation:** if a monotone-4-AP-free permutation of ℕ exists, then one exists with
`a(1) = 1` (restrict to `[a(1),∞)` and translate).

### Theorem 6 (every base point has an increasing monotone 3-AP).
For every permutation `a` of ℕ, every `x ≥ 1` and every modulus `m ≥ 1`, there are **infinitely many**
`d ∈ mℕ` with `p(x) < p(x+d) < p(x+2d)`.

*Proof.* Take `m=1` (general `m`: apply this to `a|_{x+mℕ}` via Lemma 5(i)). Let
`M := max a({1,…,p(x)})`; for `d > M` both `x+d, x+2d` exceed `M`, so their positions exceed `p(x)`.
If only finitely many `d` worked, enlarge `M` past all of them; then for every `d > M`,
`p(x) < p(x+d)` forces `p(x+2d) < p(x+d)`. Putting `d_j := 2^j d_0` (`d_0 > M`) gives
`p(x+d_0) > p(x+d_1) > p(x+d_2) > …`, an infinite strictly decreasing sequence in ℕ. ∎

Only the *increasing* orientation is used: the increasing direction is the forced resource, the
decreasing one is not (the identity permutation has no decreasing 3-AP at all).

### Theorem 7 (profile reformulation: order type ω made finitary).
A monotone-*K*-AP-free permutation of ℕ exists **iff** there is a single non-decreasing
`n : ℕ → ℕ` with `n_L ≥ L` such that **for every** `N` there is a monotone-*K*-AP-free permutation `σ`
of `[1..N]` with `rank_σ(v) ≤ n_v` for all `v ≤ N`.

*Proof.* (⇒) `n_L := max_{v≤L} p(v)`; restrict. (⇐) The profile-respecting permutations of `[1..N]`,
with "restrict to `[1..N−1]`" as the parent map, form an infinite finitely-branching tree (deleting
the value `N` preserves *K*-AP-freeness and can only lower ranks). König gives an infinite branch,
i.e. a linear order on ℕ with no monotone *K*-AP in which `v` has `< n_v` predecessors; a countable
linear order all of whose predecessor sets are finite has order type ω. ∎

**Corollary 7a (a rigorous one-sided finite criterion).** Put
`ν_L(N) := min over monotone-4-AP-free σ of [1..N] of max_{v ≤ L} rank_σ(v)`. Then `ν_L(N)` is
non-decreasing in `N`, and **if `ν_L(N) → ∞` for a single `L`, the answer to Erdős 196 is YES.**

### Prop 8 (the natural "one base point" reduction provably fails). *[explicit counterexample, machine-checked]*
Normalise `a(1)=1` (Lemma 5). Then `p(1) < p(1+e)` for every `e`, so the 4-AP `(1, 1+e, 1+2e, 1+3e)`
forces, with `g(e) := p(1+e)`:  **for all `e ≥ 1`, NOT `g(e) < g(2e) < g(3e)`.** Hence Erdős 196 = YES
would follow from:

> **(R)** every bijection `g` of ℕ (order type ω) has some `e` with `g(e) < g(2e) < g(3e)`.

**(R) is false.** Write `e = 2^a 3^b m`, `gcd(m,6)=1`; the triple `(e,2e,3e)` is
`(a,b) → (a+1,b) → (a,b+1)` in the exponent lattice. Order ℕ by: antidiagonal `a+b` ascending;
within an antidiagonal by `b` **descending**; dovetailed over `m` so that every stage is finite (order
type ω). Then `g(e) < g(2e)` (later antidiagonal) and `g(3e) < g(2e)` (same antidiagonal, larger `b`
comes first), so the pattern never occurs. Verified: 0 violations for all `e ≤ 6666`.

**Consequence:** any proof of YES must use **at least two base points** (equivalently, must use more
than "the value at position 1 precedes everything"). This kills a whole natural family of attacks,
including the obvious strengthening of the descent proof of the 3-AP theorem: the 3-AP theorem *does*
follow from one base point, and 4 provably does not.

---

## CONJECTURED (not proved)

* **C1.** For every `L` and every `N` there is a monotone-4-AP-free permutation of `[1..N]` whose
  first `L` values are exactly `{1,…,L}` (i.e. `ν_L(N) = L` always). Measured true for all `L ≤ 20`,
  `N ≤ 128`. If true, Corollary 7a can never prove YES, and the ω-obstruction is invisible to every
  "single-`L`" invariant — it lives entirely in the *joint* profile of Theorem 7.
* **C2.** The answer is NO, and a counterexample has a lacunary-like record set (Theorem 4 forces
  3-AP-freeness of the records; `{2^j}` is the natural candidate) together with a self-similar
  filling of the gaps. I am about 55/45 on NO vs YES; see "assessment".
* **C3.** The number of monotone-4-AP-free permutations of `[1..N]` is `N!·c^{N(1+o(1))}` with
  `c ≈ 0.85` (fitted from the exact counts below).

## MEASURED (finite evidence, never proof)

Exact counts of monotone-4-AP-free permutations of `[1..N]` (independent DFS engine; agrees with the
exhaustive `apcheck` enumeration for `N ≤ 9`):

| N | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|----|
| count | 22 | 102 | 564 | 3336 | 22266 | 168864 | 1307470 |
| /N! | .917 | .850 | .783 | .662 | .552 | .465 | .360 |

(3-AP-free, for contrast: 10, 20, 48, 104, 282, 496 — a vanishing fraction.)

**The invariant that detects DEGS but not the open case.** With `ν_L(N)` as in Cor. 7a:

* `K = 3`: `ν_2(N)` = 3, 4, 5, 8, 12, 17, 20 for `N` = 8, 12, 16, 24, 32, 40, 48 — grows linearly,
  as it must (DEGS forces `ν_L(N) → ∞`). Lex-min profiles likewise grow: `n_2 = 4,6,7,10,13,17`.
* `K = 4`: `ν_L(N) = L` for **all** `L ≤ 20` and all `N ≤ 128` (SAT/cadical, `nu.py`, `profile.py`).
  So this invariant is **flat** in the open case, throughout the computable range.
* Lex-min profile for `K = 4` froze at `(n_1..n_8) = (1,2,4,4,7,11,11,11)` for all `16 ≤ N ≤ 96`,
  witnessed by the head `1,2,4,3,10,7,5,15,11,8,6`. (Later coordinates grow, but that proves nothing:
  lexicographic minimisation deliberately sacrifices them — see "did not work".)
* `Reach(s)` (largest `N` admitting a 4-AP-free permutation of `[1..N]` starting with `s`): of the
  120 length-3 prefixes from `[1..6]`, 111 survive to `N = 96`; the 9 that die are exactly those that
  already contain a monotone 3-AP whose continuation is then unplaceable.

**Theorem 4 in the finite range:** 0 violations among all 70 378 monotone-*K*-AP-free permutations of
`[1..N]`, `N ≤ 8`, `K = 3,4,5`, for both the plain and the every-AP version.

## WHAT DID NOT WORK (honest list)

1. **Head-size invariants.** `m_k(N)` := min over 4-AP-free perms of `[1..N]` of `max` of the first
   `k` values. Provably bounded if a counterexample exists, and provably ≥ `k`. Measured `m_k(N) = k`
   for all `k ≤ 8`, `N ≤ 64`: dead flat. Same for `ν_L`. **The reason is structural, not
   computational:** for each single `L` the constant profile `(L,…,L)` is achievable, and only the
   *joint* profile of Theorem 7 is restrictive (the joint profile `n_v = v` would force the identity).
2. **Lex-min profiles as a proof route.** I initially thought a blowing-up coordinate of the lex-min
   profile proves YES. It does not: lex-min is only *lexicographically* non-decreasing in `N`, so a
   later coordinate may explode while the intersection over all `N` is still non-empty. Recorded
   because the mistake is easy to make and the data (coordinate `n_14` growing like `0.75N`) looks
   deceptively like a proof.
3. **One-base-point / multiplicative reduction.** Prop 8: provably impossible. The clean sub-question
   "must every ω-order have `g(e) < g(2e) < g(3e)`?" has answer NO (antidiagonal lattice order).
4. **Local-extremum counting.** Runs of length ≤2 in every `ε_e` force ≥ `VE/4 − O(E²)` local maxima
   among `v ≤ V`, `e ≤ E`; a value at position `n` can be a local max for at most `(n−1)/2` values of
   `e`. Combining gives only `Σ_{v≤V} p(v) ≳ V²/32`, weaker than the trivial `V²/2`. No contradiction;
   the counting is off by a constant factor and I see no way to fix the constant.
5. **Safety/closure searches.** "Prefixes with no permanently blocked value" is a necessary condition
   that is *trivially* satisfiable at every finite size (the parity recursion has no monotone 3-AP at
   all, hence blocks nothing), so it carries no information. Same for the compactness/König tree of
   restrictions: it always has infinite branches, and the entire content is rank stabilisation.
6. **Getting a contradiction out of Theorem 4 alone.** Absent other constraints, *any* infinite set can
   be the record set of an ω-permutation (place `u_1`, then all values `< u_1`, then `u_2`, then all
   values in `(u_1,u_2)`, …), and infinite 3-AP-free sets exist. So Theorem 4 must be combined with a
   second constraint; I did not find one that closes.

---

## Assessment: the best idea and its prospects

**The idea.** Theorem 4 + 4′: in a counterexample, the record set — and the record set of *every*
affine sub-copy — is an infinite 3-AP-free set, and the record set is exactly where "order type ω"
enters (it is the only place my proof uses well-ordering). The `k`-graded version explains the whole
DEGS ladder in one line: `k=3` forces `|U| ≤ 1` (contradiction), `k=5` only forces `U` to be 4-AP-free
(easy), and `k=4` sits exactly at "`U` must be 3-AP-free" — satisfiable in isolation, but
*Roth-critical*.

**Why it might go further.** (a) It reduces an ω-statement to a statement about a canonical set, and
Theorem 4′ supplies one such set for every AP `S`: an infinite, highly overlapping family of
3-AP-free sets `{U_S}` inside a single permutation, all coupled through one order. A contradiction
would follow from any lemma "some `U_S` contains a 3-AP", and `U_S` is far from arbitrary — it is the
sequence of first-placed elements of the successive tails of `S`, generated by one order across all
`S` simultaneously. (b) It is orthogonal to digit/block constructions, so it also sharply constrains
any attempted counterexample (C2): records must be Behrend-like, and by Lemma 5(ii) plus
self-similarity the same must hold after restricting to every tail and every AP.

**Why it might not.** The coupling is the whole difficulty and I could not quantify it: for a fixed
`S`, `U_S` can be extremely sparse (the running maximum can jump arbitrarily far), so there is no
density lower bound to play against Roth's upper bound. A completion needs a genuinely new ingredient
forcing records to be *dense* somewhere — and Prop 8 shows the naive "use the first element" route to
such an ingredient is provably closed.

**Next thing I would do:** try to prove or refute "for every monotone-4-AP-free permutation there are
`S` and three elements of `U_S` in AP", for `S = {c + kd}` with `d` lacunary, using Theorem 6 (every
base point admits increasing 3-APs with difference in any prescribed `mℕ`). Theorems 4′ and 6
constrain the same object from opposite directions and have not yet been combined.

---

### Files
`core.py` (independent sign-sequence checker + incremental blocking engine), `sat.py` (SAT encoding of
monotone-*K*-AP-freeness as a linear order), `nu.py`, `profile.py` (the invariants of Cor. 7a /
Thm 7), `reach.py` (`Reach(s)`), `xval.py` (cross-validation vs `experiments/apcheck.py`),
`verify_all.py` (**all report claims, all pass**), `t1.py`–`t12.py` (the experiments quoted above).
