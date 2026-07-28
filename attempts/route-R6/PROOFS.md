# Route R6 — Density/Szemerédi structure of a hypothetical counterexample: PROOFS

Status: all lemmas below are **proved in full** unless explicitly tagged *(remark, not used)*
or *(heuristic)*. Machine tests: `finite_tests.py` (exhaustive over all monotone-4-AP-free
permutations of `[1..N]`, `N ≤ 10`), `calibration_tests.py` (reversed-block examples).
Conventions are those of `/home/user/erdos/PROBLEM.md` (binding).

## 0. Setup, notation, cited theorems

Throughout, `a : ℕ → ℕ` is a bijection (`ℕ = {1,2,3,…}`), written as the sequence
`a(1), a(2), …`; `π = a⁻¹`, so `π(v)` is the (finite) position of value `v`.

**Standing hypothesis (H)** (assumed only where stated): `a` has **no monotone 4-AP**:
there are no positions `i₁<i₂<i₃<i₄` and `x,d ≥ 1` with
`(a(i₁),…,a(i₄)) = (x, x+d, x+2d, x+3d)` [**(H↑)**, increasing orientation] or
`= (x+3d, x+2d, x+d, x)` [**(H↓)**, decreasing orientation].
Every lemma below is annotated with which half it uses; this matters because the
calibration example satisfies (H↑) but not (H↓).

- An **increasing subsequence** of `a` is a (finite or infinite) set of positions
  `i₁ < i₂ < …` with `a(i₁) < a(i₂) < …`; **decreasing subsequence** likewise with
  `a(i₁) > a(i₂) > …`. Its **value set** is `{a(i₁), a(i₂), …}`.
- For `x ≥ 1`, the **induced permutation** `a|ₓ` is the sequence of the values
  `1,…,x` listed in the order of their positions; it is a permutation of `[1..x]`
  (restriction principle, PROBLEM.md). `LIS(x)`, `LDS(x)` denote the longest
  increasing / decreasing subsequence lengths of `a|ₓ`. Monotone subsequences of `a|ₓ`
  are exactly monotone subsequences of `a` with all values `≤ x` (same positions,
  relabeled), so monotone 4-APs of `a|ₓ` are monotone 4-APs of `a`.
- `r₄(N)` (resp. `r₃(N)`) = maximum size of a subset of `[1..N]` containing no 4-term
  (resp. 3-term) arithmetic progression. Since a 4-AP contains a 3-AP, every 3-AP-free
  set is 4-AP-free, so `r₄(N) ≥ r₃(N)`.
- **Upper density** of `A ⊆ ℕ`: `d̄(A) = limsup_{N→∞} |A ∩ [1..N]|/N`. It is finitely
  subadditive: `d̄(A ∪ B) ≤ d̄(A) + d̄(B)` (limsup of a sum ≤ sum of limsups).

**Cited theorems** (exact statements; hypotheses verified at each use):

- **[Sz4] Szemerédi 1969** (*On sets of integers containing no four elements in
  arithmetic progression*, Acta Math. Acad. Sci. Hungar. 20 (1969) 89–104): for every
  `δ > 0` there is `N₀(δ)` such that for all `N ≥ N₀(δ)`, every `A ⊆ [1..N]` with
  `|A| ≥ δN` contains a 4-term AP `x, x+d, x+2d, x+3d` (`d ≥ 1`).
  Equivalent forms used: (i) `r₄(N)/N → 0`; (ii) every `A ⊆ ℕ` with `d̄(A) > 0`
  contains a 4-term AP. [(ii) from the finite form: if `d̄(A) = 2δ > 0` there are
  arbitrarily large `N` with `|A ∩ [1..N]| ≥ δN`; take such an `N ≥ N₀(δ)`.]
- **[vdW] van der Waerden 1927**: for all `k, r ≥ 1` there is `W(k,r)` such that every
  `r`-coloring of `[1..W(k,r)]` contains a monochromatic `k`-term AP.
  Strengthening **[vdW∞]** proved in Lemma 3.4 below: in any `r`-coloring of ℕ, some
  single color class contains arbitrarily long APs.
- **[Beh] Behrend 1946** (*On sets of integers which contain no three terms in
  arithmetical progression*, PNAS 32 (1946) 331–332): there is an absolute `c > 0`
  with `r₃(N) ≥ N·exp(−c√(log N))` for all `N ≥ 2`. Hence also
  `r₄(N) ≥ N·exp(−c√(log N))`. Used only in the assessment (§6), never in a proof
  of a necessary condition.
- **[GT] Green–Tao 2017** (*New bounds for Szemerédi's theorem, III: a polylogarithmic
  bound for r₄(N)*, Mathematika 63): `r₄(N) ≪ N (log N)^{−c}` for some absolute
  `c > 0`. *(remark-level only; no proof below depends on it.)*
- **[DEGS77(a)]** (certified background, PROBLEM.md): every permutation of ℕ contains
  a monotone 3-term AP.

## 1. L0 and L1: increasing subsequences

**Lemma L0** (any permutation of ℕ; no (H)). *(i) Every strictly decreasing sequence
of positive integers is finite; hence every decreasing subsequence of `a` is finite.
(ii) The left-to-right maxima (records: positions `n` with `a(n) > a(m)` for all
`m < n`) form an infinite increasing subsequence.*

*Proof.* (i) A strictly decreasing sequence in `ℕ` is injective into `[1..first term]`.
(ii) Records form an increasing subsequence by definition. If `n` is a record with value
`a(n)`, let `p = π(v)` for some value `v > max{a(1),…,a(n)}` (exists: `a` surjective onto
the infinite set ℕ, so values are unbounded); the least position `p' ≤ p` with
`a(p') > a(n)` is a record `> n`. So records are unbounded. ∎

**Lemma L1** (uses (H↑) only). *Under (H↑), the value set `V` of every increasing
subsequence of `a` contains no 4-term AP.*

*Proof.* Along an increasing subsequence, value order coincides with position order.
If `x, x+d, x+2d, x+3d ∈ V` (`d ≥ 1`), their four positions (as elements of the
subsequence) are ordered as their values: `π(x) < π(x+d) < π(x+2d) < π(x+3d)`.
That is an increasing monotone 4-AP of `a`, contradicting (H↑). ∎

**Corollary L1.1** (L1 + [Sz4](ii)). *Under (H↑), the value set of every increasing
subsequence of `a` has upper density 0.*

**Corollary L1.2** (finite shadow; L1). *Under (H↑): every increasing subsequence with
all values `≤ x` has length `≤ r₄(x)`; in particular `LIS(x) ≤ r₄(x)` for all `x`.*

**Lemma L1′** (dual; uses (H↓) only). *Under (H↓), the value set of every decreasing
subsequence contains no 4-term AP; every decreasing subsequence with values `≤ x` has
length `≤ r₄(x)`; in particular `LDS(x) ≤ r₄(x)`.*

*Proof.* Along a decreasing subsequence, value order is the reverse of position order:
if `x, …, x+3d ∈ V` then `π(x+3d) < π(x+2d) < π(x+d) < π(x)`, a decreasing monotone
4-AP, contradicting (H↓). Size bound as in L1.2 (density is vacuous: the set is finite
by L0(i)). ∎

## 2. Patience machinery (proved from scratch, valid for infinite sequences)

For `n ∈ ℕ` let `ℓ(n)` = length of the longest decreasing subsequence of `a` **ending
at position `n`**. This is well defined: such a subsequence lives in `[1..n]`. Let the
**pile** `U_j = {n : ℓ(n) = j}` (positions) and `V_j = a(U_j)` (values), `j ≥ 1`.

**Lemma P** (any permutation of ℕ; no (H)). *(a) Each nonempty `U_j` is an increasing
subsequence. (b) Interlock: for every `n ∈ U_j` with `j ≥ 2` there is `m < n` with
`a(m) > a(n)` and `ℓ(m) = j−1`; iterating, every `n ∈ U_j` is the last element of a
decreasing subsequence `m₁ < m₂ < … < m_j = n` with `ℓ(m_t) = t` for all `t`.
(c) The piles partition the positions; `sup_j {j : U_j ≠ ∅} = sup` of lengths of
decreasing subsequences (both may be `∞`). (d) `U_1` = set of records, which is
infinite. (e) For each `x`, the same construction applied to `a|ₓ` partitions `[1..x]`
into exactly `LDS(x)` increasing subsequences of `a|ₓ`; dually (exchanging the roles of
increasing/decreasing via labels `ℓ↑(n)` = longest increasing subsequence ending at
`n`), `[1..x]` partitions into exactly `LIS(x)` decreasing subsequences. Consequently
`x ≤ LIS(x) · LDS(x)`. (f) Any cover of the positions of `a` (or of `a|ₓ`) by
increasing subsequences has at least `sup`-decreasing-length (resp. `LDS(x)`) members.*

*Proof.* (a) Let `m < n`, `ℓ(m) = ℓ(n) = j`. If `a(m) > a(n)`, appending `n` to a
longest decreasing subsequence ending at `m` gives `ℓ(n) ≥ j+1`, a contradiction; since
`a` is injective, `a(m) < a(n)`. (b) Take a longest decreasing subsequence
`m₁ < … < m_j = n`; then `ℓ(m_t) ≥ t` (its prefix ends at `m_t`), and `ℓ(m_t) > t` is
impossible for `t < j` since extending a longer one ending at `m_t` by
`m_{t+1}, …, m_j` (values keep decreasing) would give `ℓ(n) > j`. In particular
`m = m_{j−1}` works. (c) Partition is clear; `ℓ(n) = j` exhibits a decreasing
subsequence of length `j`, and conversely a decreasing subsequence of length `j` ends
at some `n` with `ℓ(n) ≥ j`, and by (b) all labels `1..ℓ(n)` occur. (d) `ℓ(n) = 1`
iff there is no `m < n` with `a(m) > a(n)`, i.e. `n` is a record; infinite by L0(ii).
(e) The construction only uses relative order, so it applies verbatim to the finite
sequence `a|ₓ`; the number of nonempty piles is `max ℓ = LDS(x)` by (c). The dual
statement is the same argument on the sequence with values negated. For the product
bound: `[1..x]` is partitioned by (e) into `LDS(x)` increasing subsequences, each of
length `≤ LIS(x)`, so `x ≤ LDS(x)·LIS(x)`. (f) An increasing and a decreasing
subsequence share at most one position (two shared positions would be ordered both ways
in values). A decreasing subsequence of length `s` (which exists for every
`s < 1 + sup`, by (c)) therefore needs `s` distinct covering members. ∎

**Theorem D (infinite Dilworth/patience for sequences — the version this route
settles on).** *Let `a` be any permutation of ℕ, `s* ∈ ℕ ∪ {∞}` the sup of lengths of
its decreasing subsequences.*
1. *If `s* < ∞`: the minimum number of increasing subsequences covering all positions
   is exactly `s*`, and the piles `U_1, …, U_{s*}` realize it (constructively; no
   compactness needed).*
2. *If `s* = ∞`: no finite family of increasing subsequences covers the positions, but
   the countable pile partition `{U_j}_{j≥1}` always exists, all piles nonempty, with
   the interlock property P(b).*

*Proof.* 1: upper bound P(a),(c); lower bound P(f). 2: P(f) gives the negative half
(for every `s` there is a decreasing subsequence of length `s+1`); P(a)–(c) the rest. ∎

**False variants and traps** (deliverable 1):

- *"All decreasing subsequences finite ⇒ some finite cover by increasing
  subsequences" is FALSE.* By L0(i), **every** permutation of ℕ has all decreasing
  subsequences finite; but e.g. the reversed-block permutation `T` of §5 has
  `LDS(3^K−1) = 2·3^{K−1}` unbounded (machine-verified, `calibration_tests.py` (C)),
  so by P(f) no finite cover exists. Finiteness of each antichain is far weaker than
  boundedness of antichains — this is the standard infinite-combinatorics trap.
- *Sup attained?* `s* = ∞` does **not** mean an infinite decreasing subsequence exists
  (none does, L0(i)). "Unbounded lengths" and "an infinite one" must not be conflated.
- *(remark, not used)* For general infinite posets, width `≤ s` (all antichains of
  size `≤ s`) still implies a partition into `s` chains (compactness from finite
  Dilworth, e.g. via Rado's selection lemma); we never need this — for sequences the
  patience labels give it constructively, which is why Theorem D is stated for
  sequences only.

## 3. L2 and L3: the two axes are exhausted

**Lemma L2** (uses (H↑) via L1, plus [vdW]). *Under (H↑), decreasing subsequences of
`a` have unbounded (finite) lengths: `s* = ∞`. Moreover every pile value set `V_j` is
4-AP-free and `d̄(V_j) = 0`, and any FINITE union of pile value sets (indeed of value
sets of arbitrary increasing subsequences) has upper density 0.*

*Proof.* Suppose `s* = s < ∞`. By Theorem D.1, `ℕ = V_1 ∪ … ∪ V_s` with each `V_j` the
value set of an increasing subsequence. Color each `v ∈ [1..W(4,s)]` by its pile index.
By [vdW] (hypotheses: `r = s` colors, interval `[1..W(4,s)]` fully colored — it is,
since the `V_j` cover ℕ) some `V_j` contains a 4-term AP; by L1 that contradicts (H↑).
So `s* = ∞`. Each `V_j` is the value set of an increasing subsequence (P(a)), so L1 and
L1.1 give 4-AP-freeness and `d̄(V_j) = 0`; finite subadditivity of `d̄` gives the last
claim. ∎

Note: L2 needs only [vdW], not [Sz4]; the density claims need [Sz4].

**Lemma L2.5 (quantitative sandwich).** *For every `x ≥ 1`:*
- *(i) (no (H)) `x ≤ LIS(x) · LDS(x)`;*
- *(ii) (uses (H↑)) `LIS(x) ≤ r₄(x)` and `LDS(x) ≥ x / r₄(x)`;*
- *(iii) (uses (H↓)) `LDS(x) ≤ r₄(x)` and `LIS(x) ≥ x / r₄(x)`.*

*Under full (H), by [Sz4](i): `LIS(x), LDS(x)` are both `o(x)` and both `→ ∞`, at rate
at least `x/r₄(x)`.*

*Proof.* (i) is P(e). (ii): first half is L1.2. Second half: by P(e), `[1..x]` is
partitioned into `LDS(x)` sets, each the value set of an increasing subsequence of
`a|ₓ`, hence of `a` (restriction principle), hence of size `≤ r₄(x)` by L1.2; so
`x ≤ LDS(x)·r₄(x)`. (iii) is the mirror image using L1′ and the dual partition in
P(e). The orientation split is exactly as marked — (ii) never invokes (H↓), (iii)
never invokes (H↑); the calibration example satisfies (ii) and violates the first half
of (iii) (machine: `calibration_tests.py` (D)/(E)). ∎

**Lemma 3.4 [vdW∞].** *For every `r`-coloring `χ : ℕ → [r]`, some color class contains
arbitrarily long APs.*

*Proof.* For each `k`, `[1..W(k,r)]` contains a monochromatic `k`-AP; let `c_k` be its
color. Some color `c` occurs infinitely often among `(c_k)`, and a `k`-AP contains a
`k'`-AP for every `k' ≤ k`, so color `c` has `k`-APs for every `k`. ∎

**Lemma L3** (surjectivity used everywhere above; here the pile refinement).
*Under (H↑): the piles satisfy — `V_j` is infinite for EVERY `j ≥ 1`.*

*Proof.* `U_1` is the record set, infinite by P(d). Suppose some pile is finite; let
`j` be minimal with `U_j` finite (so `j ≥ 2`), and `M = max{a(m) : m ∈ U_j}` (finite,
`U_j ≠ ∅` by L2 + P(c)). By interlock P(b), every `n ∈ U_{j+1}` has a witness
`m ∈ U_j` with `a(n) < a(m) ≤ M`; injectivity gives `|U_{j+1}| < M`, and inductively
every `U_{j'}`, `j' > j`, has all values `< M`, so `⋃_{j' ≥ j} V_{j'} ⊆ [1..M]` is
finite. Hence the complement of `V_1 ∪ … ∪ V_{j−1}` in ℕ is finite. Color ℕ with `j`
colors: pile index for `V_1,…,V_{j−1}`, one junk color for the finite rest. By
[vdW∞], some class has arbitrarily long APs; the junk class is finite, so some `V_i`
(`i ≤ j−1`) contains (in particular) a 4-term AP, contradicting L1. ∎

**Lemma L3.5 (order-type control for induced permutations).** *Let `S ⊆ ℕ` be
infinite and `φ : S → ℕ` its order isomorphism (`φ(v)` = rank of `v` in `S`). List the
elements of `S` in position order (of `a`) as `b(1), b(2), …` and set
`a_S(i) = φ(b(i))`. Then `a_S : ℕ → ℕ` is a bijection with all predecessor sets
finite — i.e. a legitimate permutation of ℕ in the sense of PROBLEM.md.*

*Proof.* The positions `{π(v) : v ∈ S}` form an infinite subset of ℕ, so listing `S`
by position is a well-defined enumeration `b`; each `v ∈ S` occurs at the finite index
`|{w ∈ S : π(w) ≤ π(v)}|`. `a_S` is a bijection as a composition of the bijections
`i ↦ b(i)` (ℕ→S) and `φ` (S→ℕ). Every value `φ(v)` sits at a finite index, and every
index is filled — order type `ω` on both axes. ∎
