# Route R6 — Density/Szemerédi structure of a hypothetical counterexample: PROOFS

Status: all lemmas below are **proved in full** unless explicitly tagged *(remark, not used)*,
*(heuristic)*, or *(machine-assisted)*. Machine tests: `finite_tests.py` (exhaustive over all
monotone-4-AP-free permutations of `[1..N]`: `N ≤ 9` complete, `N = 10` in progress at
filing), `calibration_tests.py` (reversed-block examples).
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
  `r₄(N) ≥ N·exp(−c√(log N))`. Used only in the assessments (§8, REPORT.md), never in a proof
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

## 4. Necessary conditions on any counterexample (T1–T6), each machine-tested

Standing hypothesis (H) (both orientations) unless a weaker one is flagged.
Machine tests: `finite_tests.py` — **exhaustive** over all monotone-4-AP-free
permutations of `[1..N]`, `N = 3..9` (194,160 avoiders; counts match the calibration
sequence 6, 22, 102, 564, 3336, 22266, 168864), with exact `r₄(N)` from brute force
(`r₄(1..10) = 1,2,3,3,4,5,5,6,7,8`); `N = 10` run separately (same code path).
All tests **pass** on every avoider. Calibration on the triadic example: §5.

**T1 (sandwich).** For every `x`: `x ≤ LIS(x)·LDS(x)`; `LIS(x) ≤ r₄(x)` and (H↓)
`LDS(x) ≤ r₄(x)`; hence `x/r₄(x) ≤ LIS(x), LDS(x) ≤ r₄(x)`, both `o(x)`, both `→ ∞`.
*Proof:* Lemma L2.5. *(Test: T1 block of `finite_tests.py`.)*

**T2 (pile structure).** The dec-patience piles partition ℕ into infinitely many
increasing subsequences (Theorem D.2 + L2), **every pile infinite** (L3), every pile
value set 4-AP-free of upper density 0 (L1, L1.1), any finite union of pile value
sets has upper density 0 (L2), interlock chains as in P(b): every `v` in pile `j`
bottoms a decreasing chain of length `j` through piles `j, j−1, …, 1` whose value set
is 4-AP-free (L1′, uses (H↓)), so `j ≤ r₄(max prefix value at time π(v))`.
*(Test: T2 block — pile partition, count = LDS, monotone piles, 4-AP-free pile value
sets, interlock witnesses; dual Mirsky piles likewise.)*

**T3 (closure under affine sub-progressions).** For every infinite AP
`P = {c + (t−1)m : t ≥ 1}` (`c ≥ 1, m ≥ 1`), the renormalized induced permutation
`a_P` (Lemma L3.5 applied to `S = P`, composed with the affine order isomorphism
`P → ℕ`) is again a permutation of ℕ with no monotone 4-AP.
*Proof.* `a_P` is a legitimate permutation of ℕ by L3.5. A 4-term AP inside `P`
has common difference divisible by `m`, and the affine map `c+(t−1)m ↦ t` is a
bijection between 4-APs of ℕ contained in `P` and 4-APs of ℕ; positions are
inherited, so a monotone 4-AP of `a_P` pulls back to one of `a`. ∎
**Corollary T3.1** (with [DEGS77(a)] applied to `a_P`, and to its tails via
`P' ⊆ P`): `a` contains monotone 3-APs with all terms `≡ c (mod m)` and min term
`> M`, for every `c, m, M` — infinitely many monotone 3-APs at every scale in every
residue class. (This is also R5's Corollary 2.1, proved there via anchored supply;
the two proofs are independent.)
*(Test: T3 block — every residue-class restriction of every finite avoider is a
4-AP-free permutation after renormalization.)*

**T4 (local displacement; uses (H↑) only).** For every interval
`I = [u, u+L−1] ⊆ ℕ`: `max_{v∈I} |π(v) − v| > (L−4)/6`.
*Proof.* Suppose `C := max_{v∈I}|π(v)−v|` satisfies `6C ≤ L−4`. Put `d = 2C+1`,
`x = u`. All four terms `x, x+d, x+2d, x+3d` lie in `I` (`x+3d = u+6C+3 ≤ u+L−1`).
For `t = 0,1,2`: `π(x+(t+1)d) ≥ x+(t+1)d − C = x+td + (C+1) > x+td + C ≥ π(x+td)`.
So the four positions increase strictly: an increasing monotone 4-AP, contradicting
(H↑). ∎
**Corollary T4.1.** `limsup_{v→∞} |π(v)−v|/v ≥ 1/6`.
*Proof.* Apply T4 to `I = [1..L]`: some `v_L ≤ L` has `|π(v_L)−v_L| > (L−4)/6`.
For any `B`, `C_B := max_{v≤B}|π(v)−v|` is finite, so for `L > 6C_B+4` the witness
has `v_L > B`; thus `v_L → ∞`, and `|π(v_L)−v_L|/v_L > (L−4)/(6L) → 1/6`. ∎
(Comparison: CORE.md Theorem 12 gives `limsup π(v)/v ≥ 9/8`, i.e. signed excess
`≥ 1/8` along a subsequence; T4.1 gives unsigned excess `≥ 1/6` — neither implies
the other; T4 itself is a *local, every-window* statement with no analogue there.)
*(Test: T4 block — all windows of all avoiders; tightness data: minimal window-max
displacement over avoiders at `N=9` is `2` for `L=9`, vs bound `⌈(9−4)/6⌉ = 1`:
the constant 1/6 is not optimized.)*

**T5 (records; uses (H↑) only).** The record (left-to-right maxima) value set is
infinite (L0(ii)), 4-AP-free, of upper density 0; the left-to-right minima value
set is finite. (= CORE.md Lemma 11(b) spine `Λ`; independent proof here via L0+L1.
LR minima form a decreasing subsequence, finite by L0(i).)
*(Test: T5 block.)*

**T6 (forced extension; interface to R5).** For every increasing 3-AP
`(x, x+d, x+2d)` (positions increasing): `π(x+3d) < π(x+2d)`, and `π(x−d) > π(x)`
if `x−d ≥ 1`; mirror statements for decreasing 3-APs. Combined with T3.1: these
constraints fire at every scale and in every residue class.
*Proof:* immediate from (H) (= R5 lemmas L1, L2, L3a, L3b, proved there; re-proved
in one line each by reading off the excluded 4-AP).
*(Test: T6 block, both orientations.)*

## 5. Calibration: the reversed-block examples (and a correction to the brief)

Let `2 ≤ b₁ < b₂ < ⋯` be "block starts", `b₀ := 1`, and let `RB(b)` be the
permutation of ℕ listing the blocks `[b_k, b_{k+1})`, `k = 0, 1, …`, in order,
each block in DECREASING value order. Then block `k` occupies positions
`[b_k, b_{k+1})`, and `π(v) = b_k + b_{k+1} − 1 − v` for `v ∈ [b_k, b_{k+1})`.

**Lemma C0 (pattern dichotomy).** In `RB(b)`: two values in the same block appear
in inverted order (larger first); two values in different blocks appear in value
order. Hence: an increasing monotone 4-AP of `RB(b)` is exactly a 4-term AP whose
terms lie in four DISTINCT blocks; a decreasing monotone 4-AP is exactly a 4-term
AP whose terms lie in ONE block. Decreasing 4-APs always exist (any block of length
`≥ 4` contains 4 consecutive integers), so no `RB(b)` is a full counterexample —
`RB(b)` calibrates the (H↑)-side lemmas only. This is stated explicitly per the
route brief.

**Lemma C1 (bad-window inequality).** If a 4-term AP `x, x+d, x+2d, x+3d` has its
terms in four distinct blocks, and `β < γ` are block starts with
`x+d < β ≤ x+2d < γ ≤ x+3d`, then `γ ≤ 3β − 5`.
*Proof.* `d ≤ β−1−x` (from `x+d ≤ β−1`), so
`γ ≤ x+3d = (x+d)+2d ≤ (β−1) + 2(β−1−x) = 3β − 3 − 2x ≤ 3β − 5` since `x ≥ 1`. ∎

**Theorem C2 (ratio-3 calibration examples; fully proved).**
If `b_{k+1} ≥ 3b_k − 4` for all `k ≥ 1`, then `RB(b)` has NO increasing monotone
4-AP. In particular:
- *(triadic)* `b_k = 3^k`: no increasing 4-AP, and `π(v) ≤ 3v − 1` with equality
  exactly at `v = 3^k`;
- *(chain)* `b₁ = 3`, `b_{k+1} = 3b_k − 4` (starts 3, 5, 11, 29, 83, …): no
  increasing 4-AP, and `π(v) ≤ 3v − 5` for all `v ≥ 3` (head: `π(1)=2, π(2)=1`);
  every ratio `π(v)/v < 3` strictly, `limsup_v π(v)/v = 3` unattained.
*Proof.* If an increasing 4-AP existed, C0 puts its terms in 4 distinct blocks, so
some starts `β < γ` sit as in C1, giving `γ ≤ 3β−5`. But all pairs of starts
satisfy `γ ≥ b_{next}(β) ≥ 3β−4` (the map `β ↦ 3β−4` is increasing, so all later
starts are `≥ 3β−4`). Contradiction. Profiles: `π(v) ≤ b_{k+1} − 1` on block `k`
and `b_{k+1} − 1 ≤ 3b_k − 1 ≤ 3v − 1` (triadic), `= 3b_k − 5 ≤ 3v − 5` (chain). ∎

**Correction C3 (the brief's dyadic example is WRONG).** The reversed-dyadic
permutation (`b_k = 2^k`) HAS increasing monotone 4-APs: `(1, 6, 11, 16)` at
positions `(1, 5, 12, 31)` and `(2, 7, 12, 17)` at positions `(3, 4, 11, 30)`
(machine: the minimal failing prefix has 28 positions, where `(x,d) = (1,6)`,
i.e. the AP `(1,7,13,19)` at positions `(1,4,10,28)`, completes; see
`calibration_tests.py` (A)). The brief's claim "dyadic blocks reversed is 4-AP-free except for
decreasing in-block APs" is false; ratio ≥ 3 restores it (Theorem C2), and §7.5
shows ratio → 3 is *forced* in this family. All §4 calibrations therefore use the
triadic example.

**Machine verification** (`calibration_tests.py`, `family_opt_check.py`):
triadic has no increasing 4-AP on prefixes up to `3⁹−1 = 19682` (and the chain up
to 40000); all decreasing 4-APs lie inside single blocks (`K ≤ 7` exhaustive);
`π`-formula, records `{3^{k+1}−1}` (3-AP-free), patience label `ℓ(v) = 3^{k+1}−v`,
pile `j = {3^{m+1}−j : 3^{m+1}−j ≥ 3^m}` (infinite, 3-AP-free — matches T2),
`LDS(3^K−1) = 2·3^{K−1}`, `LIS(3^K−1) = K` all verified exactly; T1's
increasing-side half holds (`LDS(x)·r₄(x) ≥ x`, `LIS(x) ≤ r₄(x)`) while its
decreasing-side half is VIOLATED at `x = 26` (`LDS(26) = 18 > 15 = r₄(26)`,
exact) — as it must be, since triadic satisfies only (H↑); this shows the
decreasing-side tests have teeth. T3 (residue restrictions, increasing side), T4
(all windows in `[1..728]`), T5 (records) verified on triadic.

## 6. What is forced about the profile π(v)/v and the prefix sets A_n

Let `A_n = {a(1), …, a(n)}` (so `|A_n| = n`) and `F(n,x) = |A_n ∩ [1..x]|`.

1. **Forced:** `limsup |π(v)−v|/v ≥ 1/6` (T4.1); `limsup π(v)/v ≥ 9/8`
   (CORE Thm 12, (H↑) only); local displacement `> (L−4)/6` in every value window
   of length `L` (T4); and — new, §7 — every improvement of the `9/8` toward `3`
   is machine-certified at `43/24`, while `≥ 3` is impossible for (H↑)-only
   methods (Theorem C2 gives an (H↑)-witness with `π(v) ≤ 3v−1`).
2. **Not forced by the increasing side:** `A_n = [1..n]` for infinitely many `n`
   ("complete prefixes") is CONSISTENT with all (H↑)-side constraints: triadic has
   `A_n = [1..n]` exactly at `n = 3^K − 1`. So no lemma provable from (H↑) alone
   can rule out block-structured profiles, bounded `π(v)/v`, or
   `liminf F(n,n)/n = 1`.
3. **Not forced by the decreasing side alone:** the identity permutation satisfies
   every (H↓)-side constraint vacuously (no decreasing pair at all), with
   `π(v) = v`. Hence ANY profile constraint beyond §6.1 must genuinely couple the
   two orientations — no "one-orientation" argument can improve them.
4. `sup_n (max A_n − n)` and `L(x)/x` (`L(x) = max_{v≤x} π(v)`): unconstrained by
   everything proved here — triadic has `L(x) ≤ 3x` and complete prefixes; whether
   a FULL counterexample can have `L(x) = O(x)` is exactly the LP question of §7
   at full strength (LP-full for all C ⟺ no counterexample with `π(v) = O(v)`).

## 7. The LP merge: displacement thresholds, staircases, and the ratio-3 ceiling

Definitions. For `C ≥ 1`:
**LP-inc(C)**: every permutation of ℕ with `π(v) ≤ Cv` for all `v` contains an
*increasing* monotone 4-AP. **LP-full(C)**: same conclusion weakened to "contains
a monotone 4-AP (either orientation)". Clearly LP-inc(C) ⇒ LP-full(C).
CORE.md Theorem 12 (audited line-by-line here: the ledger `Σ_w e*(w)` supply/demand
argument is correct): **LP-inc(C) holds for all C < 9/8.**

**Proposition 7.2 (finite bridge; adapted from CORE Lemma 6).** LP-inc(C) is FALSE
iff for every `N` there exists a permutation of `[1..N]` with `pos(v) ≤ ⌊Cv⌋` for
all `v ≤ N` and no increasing monotone 4-AP.
*Proof.* (⇒ direction of failure) An infinite witness restricts to `[1..N]`
(restriction principle) with positions only shrinking, preserving `pos(v) ≤ ⌊Cv⌋`
(positions are integers) and no-increasing-4-AP. (⇐) König: nodes at level `N` =
increasing-4-AP-free `⌊Cv⌋`-bounded permutations of `[1..N]`, parent = restriction;
levels finite and nonempty; an infinite branch defines a limit linear order on ℕ
with predecessor sets of size `≤ ⌊Cv⌋ − 1`, hence (CORE Lemma 1) a permutation of
ℕ; it is `Cv`-bounded and increasing-4-AP-free because every alleged violation
lives in some finite restriction. (Identical to CORE Lemma 6's proof with
`φ(v) = ⌊Cv⌋` and "4-AP-free" replaced by "increasing-4-AP-free" throughout —
restriction preserves this weaker property equally.) ∎
**Consequence.** A single UNSAT at `(C, N)` proves LP-inc(C′) for all `C′ ≤ C`.

**Theorem 7.3 (ratio-3 ceiling; fully human-proved).** LP-inc(C) is FALSE for
every `C ≥ 3`: the triadic permutation satisfies `π(v) ≤ 3v − 1` and has no
increasing monotone 4-AP (Theorem C2); the chain variant even has `π(v) ≤ 3v − 5`
for `v ≥ 3` with all ratios strictly below 3. Hence, writing
`C*_inc := sup{C : LP-inc(C) holds}`:  `9/8 ≤ C*_inc ≤ 3`, and:
**no argument that uses only the increasing orientation — in particular the
Theorem-12 ledger, and any counting of R5-staircases, records, grounded values, or
piles — can prove LP-full(C) for any C ≥ 3.** Whatever kills linear-profile
candidates at `C ≥ 3` (as the R4/SAT extinction data suggests happens) must
invoke decreasing-orientation constraints.

**7.4 The R5 hand-off, answered.** R5's L10 (staircase theorem — verified here:
its proof chain Thm 2 → L9 → L10 uses (H↑) only, never (H↓)) holds in the triadic
permutation. `staircase_demo.py` exhibits explicit full staircases inside triadic
(e.g. from `u=1`: steps `4, 36, 324, 2916, 26244`, tops `9, 81, 729, 6561, 59049`,
top positions strictly increasing, every rung's planted inversion
`π(T_i+f_i) < π(T_i)` verified), coexisting with `π(v) ≤ 3v−1`. **So "staircases
from every value, counted globally, contradict linear displacement profiles" is
false for profiles at `C ≥ 3`, and can only be true for `C < 3` if the counting
somehow exploits `C < 3` sharply.** The reason staircases are cheap under a linear
profile: each rung's inversion pair `(T_i, T_i+f_i)` may be co-blocked, costing
`O(1)` displacement ratio; rung steps growing geometrically (factor ≥ 3) fit
exactly inside ratio-3 blocks. The `g ≥ 3` of L9 and the ratio 3 of Theorem C2
are the same 3: `(x+3d)/(x+d) < 3`. Staircase counting BELOW `C = 3` remains open
and is the right target (see §8).

**7.5 Block-family rigidity (why 3 is the family optimum).** In the family
`RB(b)`: if `RB(b)` has no increasing 4-AP then, for every `k` with
`b_k ≥ max(7, 2b₁+1)`, the interval `(b_k+1, 3b_k−5]` contains no block start,
and `b_{k+1} ∈ {b_k+1} ∪ (3b_k−5, ∞)`; consequently `limsup_k b_{k+1}/b_k ≥ 3`
and `limsup_v π(v)/v ≥ 3`. So triadic/chain are optimal in this family, and the
family cannot approach any `C < 3`.
*Proof.* Machine-exact feasibility (F1 of `family_opt_check.py`, exhaustive for
`β ≤ 60`, plus the human proof): for starts `α < β < γ` with
`2 ≤ α ≤ (β−1)/2`, a "bad window" `x < α ≤ x+d < β ≤ x+2d < γ ≤ x+3d` exists
iff `γ ≤ 3β−5` and not (`α = 2`, `β` even, `γ = β+1`). [Human proof of both
directions. Necessity is Lemma C1 (no side conditions needed). Sufficiency: with
`x = 1` the constraints read `α−1 ≤ d`, `⌈(β−1)/2⌉ ≤ d`, `⌈(γ−1)/3⌉ ≤ d`,
`d ≤ β−2`, `d ≤ ⌊(γ−2)/2⌋`; an integer `d` exists iff each lower bound is at
most each upper bound: `α−1 < ⌈(β−1)/2⌉` (from `α ≤ (β−1)/2`);
`⌈(β−1)/2⌉ ≤ β−2` (β ≥ 3); `⌈(β−1)/2⌉ ≤ ⌊(γ−2)/2⌋` holds for β odd (⟺ γ ≥ β+1)
and for β even ⟺ γ ≥ β+2 — the parity obstruction; `⌈(γ−1)/3⌉ ≤ β−2 ⟺ γ ≤ 3β−5`;
`⌈(γ−1)/3⌉ ≤ ⌊(γ−2)/2⌋` for all γ ≥ 6 (direct check for γ ≤ 10, algebra for
γ ≥ 11). If `β` is even and `γ = β+1`: `x = 2` forces `d = (β−2)/2` and works
whenever `α ≥ 3` (`α ≤ 2+d`, `2+3d ≥ β+1 ⟺ β ≥ 4`); only `α = 2` leaves
`x = 1` as the sole choice, where `d = (β−1)/2 ∉ ℤ` — the exact exception.]
Now take `k` with `β := b_k ≥ max(7, 2b₁+1)`, `α := b₁ ≤ (β−1)/2`. Any start
`γ ∈ (b_k+1, 3b_k−5]` yields a bad window (the exception only exempts
`γ = β+1`), i.e. an increasing 4-AP by C0 — contradiction. If `b_{k+1} = b_k+1`,
apply the statement at `k` to exclude starts in `(b_k+1, 3b_k−5]`, so
`b_{k+2} > 3b_k − 5 ≥ 3b_{k+1} − 8`; either way some ratio `b_{j+1}/b_j ≥ 3 − 8/b_j`
occurs at `j ∈ {k, k+1}`. As `b_k → ∞`, `limsup b_{j+1}/b_j ≥ 3`, and
`π(b_j)/b_j = (b_{j+1}−1)/b_j` realizes it. ∎
*(Machine: F2 — dyadic bad with witness `(1,5)`; triadic good; triadic + one extra
start at `2·3⁴` bad; chain `b→3b−5` bad; chain `b→3b−4` good to 40000. F3 — no
three consecutive starts.)*

**7.6 Machine-assisted sharpening of Theorem 12 (CP-SAT UNSAT certificates).**
`lp_threshold.py` (encoding: `AllDifferent` positions, `pos(v) ≤ ⌊Cv⌋`, one
reified drop-disjunction per window `(u,e)`; every SAT witness re-verified by an
independent checker):

| N  | largest grid C proved UNSAT | min grid C with verified SAT witness |
|----|------------------------------|--------------------------------------|
| 12 | 35/24 ≈ 1.458 | 3/2 |
| 16 | 19/12 ≈ 1.583 | 13/8 |
| 20 | 19/12 | 13/8 |
| 24 | 13/8 ≈ 1.625 | 5/3 |
| 28 | 41/24 ≈ 1.708 | 7/4 |
| 32 | 43/24 ≈ 1.792 | 11/6 |
| 40 | 43/24 | (budget-limited; none found below 2) |
| 48 | 43/24 | (budget-limited; none found below 2) |

By Prop 7.2: **LP-inc(C) holds for all C ≤ 43/24 ≈ 1.792** — machine-assisted
(CP-SAT INFEASIBLE at `(43/24, N)` for `N = 32, 40, 48`, three independent runs),
versus the human-proved 9/8 = 1.125. The finite thresholds `min_C(N)` are
non-decreasing in `N` (restriction is monotone) and have passed 11/6;
by Theorem 7.3 they converge to a limit `≤ 3`, and by Prop 7.2 that limit is `C*_inc`.
**Conjecture 7.7** *(heuristic, supported by 7.5 + the trend above)*:
`C*_inc = 3`, i.e. LP-inc(C) holds for every `C < 3`, sharply witnessed at 3 by
the triadic family. What is rigorous today: `43/24 ≤ C*_inc ≤ 3` (machine-assisted
lower), `9/8 ≤ C*_inc` (human-only lower).

## 8. Where this leaves the density route (summary; full assessment in REPORT.md)

Proved tension: a counterexample must partition ℕ into infinitely many infinite,
interlocked, 4-AP-free (density-0) increasing piles (T2), with
`x/r₄(x) ≤ LIS(x), LDS(x) ≤ r₄(x)` (T1). Cardinality alone cannot close: the
sandwich is consistent iff `r₄(x) ≥ √x`, and Behrend gives
`r₄(x) ≥ x·e^{−c√(log x)} ≫ √x` — the slack factor `r₄(x)²/x` is
`≥ x e^{−2c√(log x)} → ∞`. Both one-sided constraint systems are individually
realizable (triadic for (H↑), identity for (H↓)), so ANY YES proof must couple
orientations; the LP program of §7 is the sharpest currently available coupling
frame, with the open window exactly `C ∈ (43/24, 3)` on the increasing side and
"beyond 3 requires (H↓)" as a proved structural boundary.
