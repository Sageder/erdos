# ANATOMY.md — route R13: what the consecutive-smooth positive-density proofs actually do,
# and exactly where the R‴ side-conditions (class mod Q₀, per-large-prime C_ℓ) break them

Session 2026-07-28. All statements below were read off primary texts where obtainable, or off
zbMATH reviews / citing papers where not; every claim is tagged with its provenance. Nothing here
was obtained by searching for the target problem itself.

---

## 0. Acquisition log (what is on disk, what is not, and why)

| Paper | Status | File |
|---|---|---|
| **Hildebrand, "On a conjecture of Balog", Proc. AMS 95 (1985), 517–523** | **FULL TEXT OBTAINED** (AMS open archive; the previous attempt's file was a paywall HTML page and has been deleted) | `papers/hildebrand1985_balog.pdf`, `papers/hildebrand1985_balog.txt` |
| **Hildebrand, "On integer sets containing strings of consecutive integers", Mathematika 36 (1989), 60–70** | text NOT obtainable (Cambridge Core + Wiley both 403; UIUC homepage dead; no OA mirror). Exact theorem statement recovered verbatim from the zbMATH review + two independent secondary restatements | — |
| **Balog–Ruzsa, "On an additive property of stable sets", LMS Lect. Notes 237 (Cardiff 1995; publ. 1997), 55–63** | text NOT obtainable (CUP chapter paywalled; the vdoc.pub scan of the volume exposes only the front matter + ch. 1). Exact main theorem from zbMATH review; Corollary 2 verbatim from Balog–Wooley | — |
| **Heath-Brown, "Consecutive almost-primes", J. Indian Math. Soc. 52 (1987), 39–49** (+ the 1999 corrigendum, JIMS 66, 203–205) | text NOT obtainable (JIMS has no OA back file for vol. 52; archive.org holds only pre-1930 volumes; author's page has no preprints). Statement + mechanism from the zbMATH review, from Hildebrand 1985's footnote 1, and from Banks–Pollack–Pomerance | `papers/bpp_symmetric_primes_1908.06161.pdf` (secondary) |
| McNamara, "A counterexample to Hildebrand's conjecture on stable sets", arXiv:2312.08544v2 (2025) | FULL TEXT | `papers/counterexample_stable_2312.08544.pdf` |
| Teräväinen, "On binary correlations of multiplicative functions", Forum Math. Sigma 6 (2018) | FULL TEXT | `papers/teravainen2018_binary_1710.01195.pdf` |
| Tao–Teräväinen, "Quantitative correlations and some problems on prime factors of consecutive integers", arXiv:2512.01739v2 (2026) | FULL TEXT | `papers/quant_corr_2512.01739.pdf` |

The last three were **not** in the R11 sweep and they change the assessment materially (§5, §6).
Verification scripts: `verify/`.

---

## 1. Hildebrand 1985, *On a conjecture of Balog* — full anatomy

### 1.1 Exact statements (verbatim from the text)

**Definitions.** `A ⊂̃ B` means d(A \ B) = 0. `A` is *k-stable* if `kA ⊂̃ A` and `k⁻¹(A ∩ kℕ) ⊂̃ A`.
For N ∈ ℕ put

    A_N  :=  ⋃_{n,d = 1}^{N}  (n/d)(A ∩ dℕ).

These form an ascending chain with A₁ = A.

**Theorem.** If d̲(A) > 0 then d̲(A_N ∩ (A_N + 1)) > 0 for all sufficiently large N. More precisely:
for every ε > 0 there are N(ε) ∈ ℕ and δ(ε) > 0 such that d̲(A) ≥ ε implies
`d̲(A_N ∩ (A_N + 1)) ≥ δ(ε)` for all N ≥ N(ε).

**Corollary 1 (= Balog's conjecture).** If d̲(A) ≥ ε and A is p-stable for every prime p ≤ N(ε),
then d̲(A ∩ (A+1)) ≥ δ(ε).

**Corollary 2.** For 0 < α < β < 1 the set `{n : n^α < P(n) < n^β and (n+1)^α < P(n+1) < (n+1)^β}`
has positive lower density.

**Remark on the final line of the paper:** "By a minor modification of the proof, the theorem
remains valid when d̲ is replaced by the upper density d̄."

### 1.2 Proof architecture

The proof is a **pure counting/pigeonhole argument. It is completely non-constructive: it never
exhibits, localizes, or even names a single element of A_N ∩ (A_N + 1).** It produces a *lower
bound for a density* by showing that if the target set were small, k explicitly-constructed sets
would be pairwise almost disjoint inside a host set that is too small to hold them.

**Free parameters (the entire list):**

1. `k = k(ε)` — the number of "gadget" translates. Chosen ≍ C/ε at the very end.
2. A **gcd-difference set** `n₁ < … < n_k` with `n_j − n_i = (n_i, n_j)` for all i<j (Lemma 1).
   Hildebrand's own construction is recursive; Heath-Brown's is better (§4). Put `n = ∏_{i} n_i²`.
3. A divisor cut-off `D`, fixed at the end by `log log(D+2) = k · φ(n/n_k)`.
4. The **divisor set** `𝒟 = 𝒟(D, r)`, `r = n/n_i`: all `d ≤ D` of the form `d = d₁p` with `p` prime,
   `(p, r) = 1`, and every prime `q | d₁` dividing `r`. (Because `n = ∏ n_j²`, all the `n/n_i` have
   the *same* prime support, so 𝒟 does not depend on i.)
5. `N ≥ max(n, D)`.

**Step A — Lemma 1 (the shift-1 gadget).** For every k ≥ 2 there exist `n₁<…<n_k` with
`n_j − n_i = (n_i,n_j)` (i<j). Writing `g = n_j − n_i`, `ν_i = n_i/g`, `ν_j = n_j/g`, this is exactly
the statement that **ν_j = ν_i + 1**: the additive shift by 1 that the theorem must produce is
manufactured out of the *multiplicative* data of the set. Hildebrand's footnote 1 credits
Heath-Brown [Mathematika 31 (1984), 141–149] with a stronger version (an extra condition, and the
lcm of the differences controlled) and gives a short self-contained recursion instead.
*Verified numerically* (`verify/verify2.py`): minimal examples (1,2), (2,3,4), (6,8,9,12); and for
every pair of every such set, ν_j − ν_i = 1 exactly. (Hildebrand's printed recursion
`N₁=1, N_{k+1} = (∑_{h≤k} N_h)N_k` as OCR'd does **not** satisfy the divisibility it needs from
k = 4 on; the lcm-closed variant `N_j = lcm(N_{j−1}, lcm_i ∑_{h=i}^{j−1} N_h)` does. This is an OCR
artefact of the scan, not a gap in the paper — the required sets demonstrably exist.)

**Step B — the host sets.** For 1 ≤ i ≤ k, d ∈ ℕ:

    B_{i,d} := n_i(A + d) ∩ ndℕ.

All k of them sit inside `ndℕ`, a set of density `1/(nd)`. Unwinding: `m = n_i(a+d) ∈ ndℕ` iff
`d | a` and `a/d ≡ −1 (mod n/n_i)`, i.e. `a ∈ A ∩ dT_i` with `T_i := (n/n_i)ℕ − 1`. Hence
`d_x(B_{i,d}) = (1/n_i) d_{x/n_i}(A ∩ dT_i) + o(1)`.

**Step C — Lemma 2 (the variance / Turán–Kubilius step).** For fixed r and D → ∞:

    (3)  ∑_{d ∈ 𝒟(D,r)} 1/d = (r/φ(r))(log log(D+2) + O(1));
    (4)  d̄( ℕ \ ⋃_{d ∈ 𝒟} d(rℕ − 1) ) ≪ φ(r)/log log(D+2).

Proof of (4): put `f(n) = #{d | n : d ∈ 𝒟, n/d ≡ −1 (mod r)}`, compute the mean `M = (1/r)∑_{d∈𝒟}1/d`
and the second moment, using **Siegel–Walfisz** (only for the *fixed* modulus r — so really just
Mertens in progressions) to evaluate `∑_{p' ≤ D, p' ≡ p (r)} 1/p'`, and apply Chebyshev.
Consequence: `S_i := ⋃_{d∈𝒟} dT_i` misses only a set of upper density `≪ φ(n/n_k)/log log(D+2)`,
so `d̲(A ∩ S_i) ≥ d̲(A) − O(φ(n/n_k)/log log D)`.

**Step D — inclusion–exclusion + the gcd gadget (where the shift by 1 appears).** From
`d_x(⋃_i B_{i,d}) ≤ 1/(nd)`:

    1/(nd)  ≥  ∑_i d_x(B_{i,d})  −  ∑_{i<j} d_x(B_{i,d} ∩ B_{j,d}).

For the pairwise terms: if `m = n_i(a+d) = n_j(a'+d)` with `d | a, d | a'`, set `g = n_j − n_i = (n_i,n_j)`,
`ν_i = n_i/g`, `ν_j = ν_i + 1`, `b = a/d`, `b' = a'/d`, and `x = m/(gd)`. Then

    x = ν_i(b+1) = ν_j(b'+1),   so   x − ν_j = ν_j b'  and  x − ν_i = ν_i b,

hence with `y := x − ν_j`:

    y = ν_j·(a'/d) ∈ A_N,      y + 1 = x − ν_i = ν_i·(a/d) ∈ A_N        (needs ν_i, ν_j, d ≤ N).

So each pairwise intersection injects (with density scaling factor gd) into `A_N ∩ (A_N + 1)`, giving
`d_x(B_{i,d} ∩ B_{j,d}) ≤ d_x(A_N ∩ (A_N+1)) + o(1)`.
*Verified by hand on a concrete instance* (n_i,n_j) = (6,8), d = 5, a = 15, a' = 10: m = 120, x = 12,
y = 8 = 4·(10/5), y+1 = 9 = 3·(15/5). ✓

**Step E — pigeonhole.** Sum over d ∈ 𝒟, let x → ∞, insert (3) and (4), balance by choosing D with
`log log(D+2) = k φ(n/n_k)`:

    D k² · d̲(A_N ∩ (A_N + 1))  ≥  c₀ d̲(A) + O(1/k).

Choose k = k(ε) so the O(1/k) is ≤ ε/2. **The engine is: k ≈ 1/ε sets, each of relative density ≈ ε
inside a common host, must overlap.** That is the whole idea, and it is why `k ≍ 1/ε`.

### 1.3 Density/count delivered, and the constants (brief Q4)

`δ(ε) = c ε /(D(k) k²)` with `k ≍ 1/ε` and `log log(D+2) = k φ(n/n_k)`, `n = ∏ n_i²`.
Hildebrand's own Lemma-1 set has `log n_k ≍ 2^k`, so `log n ≍ k2^k`, `φ(n/n_k) ≤ exp(O(k2^k))`, and
`D = exp exp exp(O(k 2^k))`. Net: **δ(ε) is roughly the reciprocal of a tower of height four in 1/ε,
and N(ε) = max(n, D) is of the same size.** The constants are explicit but astronomically
ineffective. Note the dependence on (α, β) enters *only* through `ε = d̲(Q_α \ Q_β) = ρ(1/β) − ρ(1/α)`
— nothing else in the proof sees α or β. This is important: **the method is completely blind to the
arithmetic of the set beyond its density and its stability.**

### 1.4 What Corollary 2 actually gives us for the k = 2 window (and a correction to LADDER §6)

Apply the Theorem + Corollary 1 to `A = {n : P(n) ≤ n^β}` (rather than the band). This A is
p-stable for every p — multiplying/dividing by a fixed p only moves the threshold exponent by
`O(1/log n)`, a density-zero perturbation — and `d(A) = ρ(1/β) > 0` **for every β > 0**. Hence:

> For **every** β > 0 there is a positive lower density of n with n+1 and n+2 both n^β-smooth.

LADDER.md §6 records the threshold `α > e^{−1/(k−1)}` and instantiates it at k = 2 as 0.368. That
instantiation is wrong: `e^{−1/(k−1)}` comes from requiring `ρ(1/α) > (k−2)/(k−1)` together with the
formula `ρ(u) = 1 − log u` valid only for u ≤ 2, and at k = 2 the requirement is `ρ(1/α) > 0`, i.e.
**no constraint at all**. The k = 3 entry (0.6065) is correct. Consequence for R13: the smoothness
exponent b is *free* — we may take b as small as we like, and that turns out to matter a great deal
(§7).

### 1.5 Q2 — can it tolerate `n ≡ c₀ (mod Q₀)`?

**As a black box: no, and structurally so.** The hypothesis of Corollary 1 is p-stability, and a
residue class is the canonical *non*-stable set: if A ⊆ {a ≡ c₀ (Q₀)} then pA ⊆ {a ≡ pc₀} which is
disjoint from A unless p ≡ 1 (Q₀). Applying the bare Theorem to a class-restricted A gives a
conclusion about `A_N ∩ (A_N + 1)`, and A_N contains `(n'/d')(A ∩ d'ℕ)` for all n',d' ≤ N — the class
is destroyed by construction.

**Where it *would* enter, if one rebuilt the proof.** The bookkeeping is completely explicit, and it
is worth recording because it is close to working:

* Lemma 2 survives a congruence on the divisors. Restrict 𝒟 to `d ≡ 1 (mod Q₀)`: since `d = d₁p`,
  this is a condition on p in a class mod Q₀r, and `∑_{p ≤ D, p ≡ · (Q₀r)} 1/p = log log D/φ(Q₀r) + O(1)`
  still diverges; the Siegel–Walfisz input is already there. **Cost: a constant factor.** Routine.
* With `d ≡ 1 (Q₀)` and `A ⊆ {a ≡ c₀}` we get `b = a/d ≡ c₀`, `b' ≡ c₀`, so the output is
  `y ≡ ν_j c₀`, `y + 1 ≡ ν_i c₀ (mod Q₀)`. Demanding `y ≡ c₀` forces, using ν_j = ν_i + 1,

      c₀ ≡ −1 (mod Q₀)   and   Q₀ | ν_i = n_i/(n_j − n_i)   for every pair i < j.

* So a class-compatible version of the whole argument needs a gcd-difference set with the *extra*
  divisibility `Q₀ | n_i/(n_j − n_i)` for all i < j. **Such sets exist for small k**
  (`verify/gcdset.py`, exhaustive to 4000): Q₀=2 gives (2,3), (12,14,15), (168,180,182,189);
  Q₀=3 gives (3,4), (36,39,40), (432,441,444,448); Q₀=4 gives (4,5), (80,84,85); Q₀=6 gives (6,7),
  (252,258,259). No k = 5 example below 4000 for any Q₀ ≥ 2 — the search is exhaustive but the bound
  is small, so this is *not* evidence of non-existence.

**Verdict.** A congruence-compatible Hildebrand theorem is a plausible but genuinely new elementary
theorem, gated on an unproved combinatorial existence lemma (gcd-difference sets with `Q₀ | ν_i` for
all pairs, for every k). Since `k = k(ε) ≍ 1/ε` and `Q₀ = ∏_{ℓ ≤ P₀} ℓ^{L_ℓ}` is large, the demand is
substantial. **But this route is now superseded** — §5 shows the congruence comes free from the
modern analytic proofs of the same corollary.

### 1.6 Q3 — can it tolerate the per-large-prime C_ℓ conditions? **No — and this is the crux.**

The R‴ condition is `C_ℓ : ((n+j)/ℓ − 1) mod ℓ ≥ (ℓ−1)/2` for every large prime ℓ ∥ n+j. Put

    A* = { m : m^α < P(m) ≤ m^β, P(m)² ∤ m, ((m/P(m)) − 1) mod P(m) ≥ (P(m) − 1)/2 }.

* **d(A*) > 0 is easy** (routine): write m = ℓw with ℓ = P(m) ≤ m^{1/2}; then w > ℓ ranges over an
  interval of length ≫ ℓ, so the residue condition on w mod ℓ keeps a proportion 1/2 + o(1).
  Measured density at x = 4·10⁶ with (α,β) = (0.40,0.50): **0.0704**, versus **0.1550** for the band
  alone — exactly the predicted factor ≈ 1/2 (`verify/stab.py`).
* **A\* is maximally NOT stable.** Multiplication by p replaces the cofactor `w` by `pw`, i.e. it
  multiplies `w mod ℓ` by p — a bijection of ℤ/ℓ that scrambles the condition completely.
  Quantitatively (`verify/stab2.py`, x = 4·10⁶, restricted to the 308 575 integers n < 2·10⁶ in the
  band for which P(2n) = P(n), so that band-membership is not the issue):

      #{ C_p(n) ⟺ C_p(2n) } / #{all}  =  0.5037.

  Stability demands this ratio → 1 (disagreement of density 0). It is 1/2. **The C_ℓ condition is
  as far from stable as a condition can be.**

* **The exact lemma that would need strengthening is not a lemma but the hypothesis.** The single
  place the multiplicative dilations are used is the definition of A_N and the final implication
  "A p-stable for p ≤ N ⟹ A_N ⊂̃ A". Everything else (Lemma 1, Lemma 2, the inclusion–exclusion) is
  indifferent to what A is. So the question "can Hildebrand produce C_ℓ?" is exactly the question
  "is `A_N ⊂̃ A*`?", and the answer is a measured, decisive no.

* **The obvious repair fails, quantitatively.** One can try to make A stable by intersecting over all
  the bounded dilations the proof uses: `A** := ⋂_{ν,d ≤ N} {m : the C-condition holds for νm/d}`. For
  each large ℓ this asks `w mod ℓ` to lie in an intersection of ≈ N² half-intervals under the
  multipliers `νd⁻¹ mod ℓ`; a three-distance argument shows this has proportion `≳ 1/(N·lcm(1..N))
  ≈ e^{−N}`. So `ε ↦ ε e^{−N(ε)}`, while `N(·)` is (§1.3) a tower in the reciprocal of its argument.
  The iteration `N ≥ N(ε e^{−N})` has **no fixed point**. (And A** is anyway only "p-stable up to
  N/p", so the closure has to be re-enlarged, making it worse.)

---

## 2. Hildebrand 1989, *On integer sets containing strings of consecutive integers*

**Theorem** (zbMATH review, verbatim; independently restated by Balog–Wooley and by McNamara).
If A is stable and `d̲(A) > (k−2)/(k−1)` (k ≥ 2) then `d̲(A ∩ (A−1) ∩ … ∩ (A−k+1)) > 0`.

**Conjecture 1.3 (Hildebrand).** Stable + positive lower density should suffice for every k.

**Architecture.** Same machinery as 1985 — the k = 2 case *is* the 1985 theorem — with the
inclusion–exclusion replaced by a k-fold version; the density threshold `(k−2)/(k−1)` is precisely a
`k`-set pigeonhole ("k−1 sets of relative density > (k−2)/(k−1) inside a host must have a common
point"), which is why it is a *hard* threshold for this style of argument and not an artefact.

**Consequence for smooth strings** (as quoted by Balog–Wooley, §1): for each fixed k there are
infinitely many strings of k consecutive `n^{α_k}`-smooth numbers whenever `α_k > exp(−1/(k−1))`,
and these strings form a set of positive lower density. `ρ(1/α) > (k−2)/(k−1)` with `ρ(u) = 1 − log u`
gives exactly `α > e^{−1/(k−1)}`.

**Hard barrier for k ≥ 3 (new information relative to R11/R12).**

* `k = 3` needs `α > e^{−1/2} = 0.6065 > 1/2`. So Hildebrand 1989 cannot deliver 3 consecutive
  `√n`-smooth numbers.
* **McNamara (arXiv:2312.08544v2, 2025) disproves Conjecture 1.3, and even the weaker
  Conjecture 1.4** (`S ∩ (S+1) ∩ (S+2) ≠ ∅`), for k = 3 with a stable set of density 1/2; more
  generally for every prime k with a stable set of density `1 − 1/(k−1)`, **matching Hildebrand's
  threshold exactly**. The counterexample is archimedean: pick `T` with `p^{iT} ≈ ±1` according to
  `p ≡ ±1 (mod 3)` and define S by `3^ℓ n ∈ S` iff (`n ≡ 1 (3)` and `Re(n^{iT}) > 0`) or
  (`n ≡ −1 (3)` and `Re(n^{iT}) < 0`); since `n^{iT} ≈ (n+1)^{iT} ≈ (n+2)^{iT}`, one of any three
  consecutive integers is excluded.
* Tao–Teräväinen's positive result in this direction (cited in McNamara §1): the conjecture does hold
  for sets that are additionally *uniformly distributed in short intervals* provided
  `d(S) > 1 − (4/3)/(k−1) + o(1)`. For k = 3 that is `d(S) > 1/3`, i.e. `α > e^{−2/3} = 0.5134`.
  Smooth numbers *are* uniformly distributed in short intervals, so this applies — **and it still
  misses 1/2, by 0.0134.** That is the sharpest published position of the k ≥ 3 supply frontier.

**Verdict for 727 with k ≥ 3:** the positive-density supply of 3 consecutive √-smooth integers is not
merely unproved, it is **provably unobtainable from the stable-set machinery alone** (McNamara),
and the best structured strengthening (Tao–Teräväinen) lands just above 1/2. This is a firmer
"open" than LADDER §6 recorded.

---

## 3. Balog–Ruzsa 1997, *On an additive property of stable sets*

**Main theorem** (zbMATH review, verbatim, Y. O. Hamidoune): *Let a, b > 0 and c ≠ 0 be integers with
(a,b) | c. If 𝒜 is a stable set with non-zero **upper** asymptotic density, then the linear equation
`am − bn + c = 0` has infinitely many solutions with m, n ∈ 𝒜.*

**Corollary 2** (verbatim from Balog–Wooley 1998, §1, which cites it): *whenever a > 0 and c ≠ 0 are
fixed integers and β > 0, there is a set of integers n of positive density for which both n and
an + c are n^β-smooth.* Balog–Wooley add that this "generalises a similar earlier conclusion of
Hildebrand [1985, Corollary 2] for consecutive integers".

**Architecture.** Not read, but forced by the shape of the statement: the gcd-difference gadget of
Hildebrand's Lemma 1 produces the shift `ν_j − ν_i = 1`; to produce a general relation `am − bn = −c`
one needs a set with `b·n_j − a·n_i = c·(n_i,n_j)`-type structure, i.e. a weighted gcd-difference set.
The relaxation from lower to upper density and from "positive density of solutions" to "infinitely
many solutions" is what one expects when the pigeonhole is run along a subsequence of scales.

**Q2/Q3 for this paper.**

* The stability hypothesis is *identical*, so §1.5 and §1.6 apply verbatim: neither `n ≡ c₀ (Q₀)` nor
  `C_ℓ` is a stable condition, and neither can be inserted.
* **One genuinely new affordance, worth recording:** because the coefficients (a,b) are free, one may
  take `a = Q₀`, `c` arbitrary and obtain infinitely many `n ∈ 𝒜` with `n ≡ c (mod Q₀)` **and**
  `(n − c)/Q₀ ∈ 𝒜`. So the Balog–Ruzsa generalisation *can* force one member of the pair into a fixed
  residue class. It cannot do so for the *difference-1* configuration we need: setting a = b = 1
  (forced by "n+1, n+2") kills the coefficient freedom. So the affordance is real but orthogonal.
* The result is stated as "infinitely many solutions" (upper density hypothesis), i.e. **weaker than
  positive density** for the general linear form; Corollary 2 restores positive density in the
  smooth-number instance.

**Q4.** Same ineffective tower constants as Hildebrand (the same pigeonhole with the same k ≍ 1/ε).

---

## 4. Heath-Brown 1987, *Consecutive almost-primes* (+ the 1999 note)

**Statement** (zbMATH review, verbatim): a quantitative version of Hildebrand's consequence — there
are infinitely many n such that both n and n+1 have a prime factor `> n^{1−ε}` with
`ε = c (log log n / log n)^{1/4}`, c > 0 absolute. (The 1999 note, JIMS 66, 203–205, is a
correction/footnote; later authors cite [1987]+[1999] jointly. Its content could not be read.)

**Mechanism** (zbMATH review, verbatim): the improvement comes from constructing sets
`S = {d₁ < … < d_R} ⊂ ℕ` with `d_j − d_i | (d_i,d_j)` for i<j — *the same gcd-difference gadget* —
minimizing `τ(S) = lcm{d_j − d_i}`. Heath-Brown proves such sets exist with `log τ ≪ R³ log R`, and
that any such set has `log τ ≫ R log R`.

**Why this is the "quantitative machine".** In Hildebrand's proof the gadget size `n = ∏ n_i²`
enters the final density through `φ(n/n_k)` inside a *double* exponential (§1.3), so a gadget of
doubly-exponential size produces a tower. Heath-Brown's construction replaces the size of the gadget
data by `exp(O(R³ log R))` — polynomial in the exponent — which is exactly what converts an
inverse-tower into the power `(log log n / log n)^{1/4}`. The same gadget with the same
`log τ ≪ R³ log R` bound is what Banks–Pollack–Pomerance (arXiv:1908.06161, Lemma 3.1/3.2) reuse
for symmetric primes, and what Heath-Brown 1984 used for `d(n) = d(n+1)` (there obtaining
`≫ x(log x)^{−7}` solutions up to x — so this machinery *is* capable of power-of-log counts, not just
infinitude).

**Q2/Q3.** The output is a large *prime factor*, not a smoothness band, and the argument is again a
pigeonhole over the R translates: no member is exhibited, and no congruence or cofactor condition is
carried. However the *gadget* is exactly where a congruence would have to be inserted (the
`Q₀ | n_i/(n_j−n_i)` demand of §1.5), and Heath-Brown's is the construction one would try to make
class-compatible, since it is the only one in the literature with good quantitative control. That is
a concrete, well-posed research task.

**Relevance ranking for R13: low.** Heath-Brown's conclusion (`P(n), P(n+1) > n^{1−ε}`) is the
*opposite* end of the (α,β) band from what S₂ needs (`P(n+1), P(n+2) ≤ n^{1/2}`). What we want from
him is the *gadget technology*, not the theorem.

---

## 5. The modern analytic route (NOT in the R11 sweep) — this changes the Q2 answer

Hildebrand's Corollary 2 has since been reproved, and strengthened to an asymptotic, by methods that
have nothing to do with stable sets.

**Teräväinen, Forum Math. Sigma 6 (2018), Theorem 1.19.** For any `a<b`, `c<d` in (0,1), the set
`{n : n^a ≤ P⁺(n) ≤ n^b, n^c ≤ P⁺(n+1) ≤ n^d}` has **positive asymptotic lower density**. (This
strictly generalises Hildebrand's Corollary 2, which is the case (a,b) = (c,d).) **Theorem 1.14:**
the Erdős–Pomerance conjecture `δ({n : P⁺(n) ≤ n^a, P⁺(n+1) ≤ n^b}) = ρ(1/a)ρ(1/b)` holds for
*logarithmic* density. Engine: Theorem 1.4, a binary correlation theorem for multiplicative
`g₁, g₂ : ℕ → [−1,1]`, requiring only that `g₁ ∈ U(x, ε⁻¹, ε)` — **uniform distribution in
arithmetic progressions to bounded moduli** — built on Matomäki–Radziwiłł and Tao's logarithmic
Elliott theorem.

**Tao–Teräväinen, arXiv:2512.01739v2 (2026), Theorems 1.8 and 3.1.** There is a set 𝒳 ⊂ ℕ of
logarithmic density 1 such that for x ∈ 𝒳 and all u, v ≥ 1,

    (1/x) ∑_{n ≤ x} 1_{n is x^{1/u}-smooth} · 1_{n+1 is x^{1/v}-smooth} = ρ(u)ρ(v) + O(log^{−c} x).

**This is an honest asymptotic with a power-of-log error**, obtained from a quantitative correlation
estimate (Theorem 3.1) built on Pilatte's decoupling inequality.

**The decisive detail for R13 (Q2).** Theorem 3.1's conclusion is literally

    (W/N) ∑_{N<n≤2N} (g₁(n+h₁) − δ_N) g₂(n+h₂) **1_{n ≡ b (mod W)}** ≪ L^{−c},   W ∈ [L^c],

with L up to log X and the exceptional set of scales *independent of (W, b, h₁, h₂)*. And the
verification of the hypothesis in the proof of Theorem 1.8 is exactly a smooth-number count
**in arithmetic progressions** `n ≡ a (mod q)`, uniform in a, q. So:

> **An added congruence `n ≡ c₀ (mod Q₀)` for fixed Q₀ is already inside the published statement.**
> Restricting to a class costs only the factor 1/Q₀ in the main term, for any Q₀ ≤ (log x)^c.

Teräväinen's Remark 1.9 makes the same point for the 2018 machinery (the method handles
`g₁(a₁n+h₁)g₂(a₂n+h₂)`, which is what `n = Q₀m + c₀` produces).

**Consequence.** Everything §1.5 struggled with is free on this side. The stable-set papers should be
regarded, for R13's purposes, as **the historically first but now weakest** proofs of the
consecutive-smooth supply. The only thing they still have that the analytic route does not is
`k ≥ 3` (Hildebrand 1989) — and there McNamara has shown the soft route is dead anyway.

---

## 6. Re-framing the target: strict C_ℓ has density 0; the exact carry condition does not

This is the most consequential structural finding of R13, and it is independent of which paper one
uses.

**(a) The literal target of the brief has density zero.** R‴(b) demands C_ℓ at *every* prime
`ℓ > P₀` dividing n+j. A typical n+j has `ω_{>P₀}(n+j) ≈ log log n` such primes, each imposing an
independent-looking event of probability ≈ 1/2, so the density is
`≈ ∏_{P₀<ℓ≤x}(1 − 1/(2ℓ)) ≍ (log x)^{−1/2}` — **zero density, count `≍ x/√(log x)`**. Measured
(`verify/dens2.py`, b = 1/2, conditional on n+1, n+2 both n^{1/2}-smooth):

| n-range | smooth-pair density | frac. satisfying **all C_ℓ** | frac. satisfying **exact carry** |
|---|---|---|---|
| [10⁵, 2·10⁶) | 0.0649 | 0.0109 | 0.1084 |
| [2·10⁶, 4·10⁶) | 0.0673 | 0.0098 | 0.1153 |
| [4·10⁶, 8·10⁶) | 0.0684 | 0.0093 | 0.1138 |

The C_ℓ column decays; the carry column does not. **So "positive density with all C_ℓ" is false as
stated, and no theorem can be asked to prove it.** The right target is `≫ x (log x)^{−A}`, or simply
infinitude.

**(b) The exact criterion is much cheaper, and it is a positive-density event.** LADDER §4.5
remark (iii) already notes C_ℓ is sufficient, not necessary. The true demand at `ℓ ∥ n+j`, `ℓ > 2k`,
is `c_ℓ(n) ≥ 2`: the position-0 carry is automatic (digit `ℓ − j ≥ ℓ/2`), and the second carry may
come from *any* higher digit, not only position 1. With `≈ log n/log ℓ ≥ 1/b` base-ℓ digits, the
failure probability at a single ℓ is `≈ 2^{−(log n/log ℓ − 1)}`, and summing over the prime factors
of n+j below `n^b`:

    P(some large-ℓ carry condition fails)  ≲  ∑_{t ≥ 1/b} (t+1) 2^{−t}  ≈ (1/b + 1)·2^{−1/b}  →  0  as b → 0.

Measured: the "exact carry" fraction is ≈ 0.11 at b = 1/2, **rises to 0.227 at b = 0.35**
(`verify/dens.py`), and is stable across scales. Since §1.4 frees the exponent b (any b > 0 gives
positive density of smooth pairs), **b is a knob that buys down the carry cost**. This is the single
most useful degree of freedom R13 uncovers.

**(c) The resulting statement is a level-of-distribution statement with SMALL moduli.** Given
`ℓ ∥ n+j`, the condition `c_ℓ(n) ≥ 2` is (implied by, and comparable to) a condition on `n mod ℓ²`,
i.e. on the cofactor `W = (n+j)/ℓ` mod ℓ. With `ℓ ≤ n^b` and b small, `ℓ² ≤ n^{2b} ≪ n^{1/2}`:
**the moduli are far below the Bombieri–Vinogradov barrier.** The difficulty is not the level; it is
(i) that the moduli are *determined by n itself*, and (ii) that the condition must hold at
`≈ log log n` primes *simultaneously*, and jointly with the smoothness of the *other* member of the
pair. This is a "cofactor equidistribution along smooth numbers" problem, not a parity problem and
not a bilinear-prime problem — a materially different (and softer-looking) frontier than the
B₂/B† prime-equation frontier of LADDER §4–§5.

---

## 7. The five brief questions, answered per paper (compressed)

| | Hildebrand 1985 | Hildebrand 1989 | Balog–Ruzsa 1997 | Heath-Brown 1987 | Teräväinen 18 / Tao–Ter. 26 |
|---|---|---|---|---|---|
| **Architecture** | non-constructive pigeonhole: gcd-difference gadget (Lemma 1) + variance/Siegel–Walfisz divisor lemma (Lemma 2) + inclusion–exclusion inside host `ndℕ` | same, k-fold | same, weighted for `am−bn+c=0` | same gadget, optimised (`log τ ≪ R³ log R`) | analytic: Halász/Matomäki–Radziwiłł + log-Elliott (2018); + Pilatte decoupling (2026) |
| **Free parameters** | k≍1/ε; gcd-set {n_i}; n=∏n_i²; D via `loglog D = kφ(n/n_k)`; 𝒟(D,r); N ≥ max(n,D) | + the k-fold threshold | + (a,b,c) | R; the set S; τ(S) | ε, ω(x); L, W, b, h₁,h₂; the exceptional scale set |
| **Constructive?** | No — no element is ever named | No | No | No | No, but it is an **asymptotic count**, so it survives being intersected with positive-density events |
| **Tolerates `n ≡ c₀ (Q₀)`?** | **No** (class ⇒ not stable). Rebuild possible in principle; needs a new gcd-set lemma (§1.5) | No | Only in the skew form `n ≡ c (Q₀)` with `(n−c)/Q₀ ∈ 𝒜` — not for difference 1 | No | **Yes, free** — `1_{n≡b (mod W)}` is in Thm 3.1's statement; the smooth-count hypothesis is verified in APs |
| **Tolerates C_ℓ / carry conditions?** | **No.** Not a lemma to strengthen — the *hypothesis* (p-stability) is violated with disagreement density 0.5037 (measured) | No | No | No | **Not as stated**, but the obstruction is different in kind: one needs the correlation estimate for a *non-multiplicative* weight (see L4 below) |
| **Density / count** | δ(ε) ≈ 1/tower₄(1/ε); depends on (α,β) only via ε = ρ(1/β) − ρ(1/α) | same, threshold (k−2)/(k−1) | same | `ε(n) = c(loglog n/log n)^{1/4}`; sibling 1984 result gives `≫ x(log x)^{−7}` | **ρ(u)ρ(v) + O(log^{−c}x)** at log-density-1 scales; positive lower density unconditionally (2018 Thm 1.19) |

---

## 8. New lemmas needed for
## "positive-count `n ≡ c₀ (Q₀)`, `n+1, n+2` both n^b-smooth-banded, all large-prime carry conditions met"
## — with honest verdicts

**L0. Restate the target correctly.** Replace "positive density with all C_ℓ" by either
(i) `≫ x(log x)^{−A}` with C_ℓ, or preferably (ii) **positive density with the exact criterion
`c_ℓ(n) ≥ 2ν_ℓ(n+j)` for all ℓ > P₀**, together with b chosen small.
**Verdict: routine** (elementary; the criterion is already in PROBLEM.md; the density accounting is
§6, numerically confirmed). *This step is mandatory — without it the stated target is provably false.*

**L1. Congruence-restricted consecutive smooth pairs.** For fixed b > 0, Q₀, c₀:
`#{n ≤ x : n ≡ c₀ (Q₀), n+1 and n+2 both n^b-smooth} ≫_b x/Q₀`.
**Verdict: hard-but-classical, essentially available.** Two routes, both adaptations rather than
citations: (a) Tao–Teräväinen Thm 3.1 + the proof of Thm 1.8 — the AP restriction `1_{n≡b(W)}` and the
AP smooth-count input are both already in the paper; this yields the asymptotic
`ρ(1/b)²/Q₀ + O(log^{−c}x)` for x in a set of logarithmic density 1, which suffices for infinitude.
(b) Teräväinen 2018 Thm 1.19 + Remark 1.9 for genuine positive *lower* density in the class.
*Not* available from Hildebrand/Balog–Ruzsa (§1.5).

**L2. Squarefreeness of the large part.** `ℓ ∥ n+j` for every ℓ > P₀ dividing n+j.
**Verdict: routine.** Cost `∏_{ℓ>P₀}(1 − 1/ℓ²)` — a positive constant; a standard sieve inclusion,
compatible with all of the above.

**L3. Small-prime forcing.** Choice of (Q₀, c₀) pinning `ν_ℓ(n+j)` for ℓ ≤ P₀ and forcing the
base-ℓ digit conditions of R‴(a).
**Verdict: routine** (Lemma R_k step (i)–(ii) in LADDER §2 is already proved and audited; it is a
pure CRT/digit-prescription statement, and it is exactly the `n ≡ c₀ (mod Q₀)` of L1).

**L4. THE HARD ONE — joint cofactor/carry equidistribution along the smooth pair.**
For a positive proportion of the n counted by L1: `c_ℓ(n) ≥ 2` for every prime `ℓ > P₀` dividing
`(n+1)(n+2)`.
**Verdict: OPEN.** But now with a much better-specified shape than "route B₂ / B†":
 * It is **not** a parity problem and **not** a binary prime-equation problem. No prime is being
   detected; the smooth-pair supply is already unconditional.
 * It is a statement about the joint distribution of `((n+j)/ℓ mod ℓ)_{ℓ | n+j}` over the smooth
   pairs — i.e. **equidistribution of cofactors modulo the prime factors, uniformly over all prime
   factors simultaneously**. For b small the moduli `ℓ²` are `≤ x^{2b} ≪ x^{1/2}` (well inside BV
   range); the difficulty is that the modulus is a function of n, that `≈ log log x` conditions must
   hold at once, and that the weight `1_{c_ℓ(n) ≥ 2 ∀ℓ}` is **not multiplicative** (it couples each ℓ
   with the whole cofactor), so it is not an admissible `g₂` in Tao–Teräväinen Thm 3.1.
 * Plausible attack shape: for each n+1 = ℓ·W, the condition is `W mod ℓ ∈ S_ℓ` with `|S_ℓ| ≥ (ℓ−1)/2`.
   Sum over the factorisations `(ℓ, W)` with W smooth. Equidistribution of smooth W in APs to modulus
   ℓ (Fouvry–Tenenbaum, Harman, Drappeau; level > 1/2 on average is known for smooth numbers) is the
   natural input; the coupling to `n+2` smooth is what Theorem 3.1-type correlation estimates would
   have to absorb.
 * **Sub-lemma L4a (the one to try first, and the honest "hard-but-classical" candidate):** the
   *single-prime* version — a positive proportion of the L1-pairs satisfy `c_ℓ(n) ≥ 2` at the largest
   prime factor ℓ of n+1 only. This is one AP condition to a single modulus `ℓ ≤ x^b` and should be
   within reach of the existing machinery. **Verdict: hard-but-classical.** Going from one prime to
   all of them simultaneously is the open step.

**L5. (Only if one insists on the stable-set route) class-compatible gcd-difference sets.**
For every k and every Q₀ there is `n₁<…<n_k` with `n_j − n_i = (n_i,n_j)` **and** `Q₀ | n_i/(n_j−n_i)`
for all i<j.
**Verdict: routine-to-hard-but-classical, currently unverified.** Exhaustively confirmed for
(Q₀,k) ∈ {(2,≤4), (3,≤4), (4,≤3), (6,≤3)} below 4000 (`verify/gcdset.py`); no k = 5 example found
below 4000 for Q₀ ≥ 2 (search bound too small to be evidence either way). *Not on the critical path*
given §5.

**L6. (For k ≥ 3 of the headline, not for the named k = 2 variant) 3 consecutive n^{1/2}-smooth
integers in positive density.**
**Verdict: OPEN, with a known obstruction.** Hildebrand 1989 needs `α > e^{−1/2} = 0.6065`;
Tao–Teräväinen's short-interval-uniform strengthening needs `α > e^{−2/3} = 0.5134`; and McNamara
(2025) shows the soft conjecture that positive density alone suffices is **false** at k = 3, matching
Hildebrand's threshold exactly. So the gap to 1/2 cannot be closed by any purely soft/stable-set
argument; it needs the smooth-specific analytic input, and 0.5134 → 0.5 is the frontier.

---

## 9. Frank verdict

1. **The k = 2 smoothness supply is not the problem, and is better than LADDER recorded.** For every
   b > 0 there is positive density of n with n+1, n+2 both n^b-smooth (Hildebrand 1985 Cor. 2 applied
   to `{P(n) ≤ n^β}`; LADDER §6's "k=2: 0.368" is a mis-instantiation). Since 2018/2026 there is also
   an *asymptotic* `ρ(u)ρ(v)`, with a power-of-log error, at almost all scales.

2. **The fixed congruence `n ≡ c₀ (mod Q₀)` is free — but only on the analytic side.** It is
   structurally impossible on the stable-set side (a class is not stable), and it is already inside
   the statement of Tao–Teräväinen Theorem 3.1 (`1_{n≡b (mod W)}`, `W ≤ (log X)^c`).

3. **The C_ℓ conditions are the wall, and they are exactly orthogonal to the stable-set method.**
   Stability is invariance under multiplicative dilation; C_ℓ is a condition on a cofactor residue,
   which dilation permutes. Measured disagreement under `n ↦ 2n`: 0.5037 (stability requires 0). The
   natural repair (close under all dilations ≤ N) loses `e^{−N}` in density against a tower-sized
   `N(ε)` and has no fixed point. **There is no lemma in Hildebrand 1985/1989, Balog–Ruzsa, or
   Heath-Brown whose strengthening would deliver C_ℓ; the hypothesis itself is the obstruction.**

4. **The stated target is false as stated and must be re-scoped.** "All C_ℓ" has density
   `≍ (log x)^{−1/2}` (measured 0.0109 → 0.0098 → 0.0093 across three ranges). Replacing C_ℓ by the
   *exact* carry criterion and taking b small restores a positive-proportion event (measured 0.108 at
   b = 1/2, 0.227 at b = 0.35, heuristically → 1 as b → 0). **This re-scoping is the main actionable
   output of R13.**

5. **After re-scoping, the residual open problem changes character** — from "binary correlations of
   smooth×prime sequences at the dispersion/Chen frontier" (LADDER §4–§5) to "joint equidistribution
   of cofactors mod their own prime factors along consecutive smooth numbers", with all moduli below
   `x^{2b} ≪ x^{1/2}`. That is not a parity problem and not a bilinear-prime problem. It is still
   open, and the multi-prime simultaneity plus non-multiplicativity of the weight is the specific
   thing that is open; but it is a strictly softer-looking frontier than B₂/B†, and L4a gives a
   concrete first target.

6. **For k ≥ 3 the headline remains blocked at the supply stage**, now with a proof (McNamara) that
   the soft route cannot work and a sharp numerical gap (0.5134 vs 0.5) at the best structured route.
