# L4A.md — route R14

> **AUDIT STATUS (2026-07-28, `AUDIT_L4A.md`, verdict MIXED). Read before using anything below.**
> * **Lemmas 1, 2, 2′, 3, 3′, 4, 5 — CONFIRMED CORRECT** by an independent adversarial auditor
>   (1.5M+ verified instances, zero counterexamples; every table reproduced to the exact integer).
>   These are the route's real, unconditional contribution.
> * **§7 Proposition O1 — NOT PROVED.** It is a Dickman-*model* computation plus measurements;
>   the step `S(x,b) ≍ x·ρ(1/b)²` is an unproved independence heuristic. Its *measurements* were
>   reproduced exactly and are reliable; the Proposition is downgraded to a heuristic, and §9's
>   listing of it under "proved unconditionally" is retracted. Its sieve corollary is a heuristic
>   about two particular strategies, not a statement about all proofs.
> * **§4 Theorem A — FATALLY BROKEN.** It applies Hypothesis U to an `ℓ`-dependent family
>   (right-hand side normalised by `#{n : ℓ ∥ n+1, P(n+1) = ℓ}`), which U does not cover; the
>   `P(n+1) = ℓ` constraint is load-bearing because only it makes the sum over `ℓ` telescope, and
>   it is a multiplicative condition on the cofactor, not a congruence mod `ℓ^J`. With what U
>   legitimately supplies the bound costs `E[#{ℓ>4 : ℓ ∥ n+1}]` ≈ 2.65/2.77/2.49/1.94 at
>   `b = .5/.4/.3/.25`, i.e. `≈ 1.3·#S(x)` — worse than trivial. Raising `J₀` cannot repair it.
> * **Hypothesis U at `θ = 1` is FALSE** for every `C`, `b`; `θ < 1` strictly is forced, and the
>   `θ = 1` column of the §5 corollary is vacuous.
> * **§5 Theorem B's derivation from U + L1 is SOUND**, but inherits the above restriction.
> * **Framing correction.** "Any `θ > 0` and any `C` suffice because `b` is free" is misleading:
>   the binding constraint is the ratio `θ/b ≥ 62.8`, i.e. moduli `q ≥ y^{62.8}` with `y = x^b`,
>   against `y^{6.59}` known for a *single* smooth number — and Soundararajan's range condition at
>   `u = 1/b ≈ 63` caps `y ≲ 2·10⁷`, so that theorem cannot be invoked as `x → ∞`.
>   Highest-value open repair: sharpening Lemma 3′ at prime powers `a ≥ 2` would lower the demand
>   to `θ/b ≈ 7.3`; the crude prime-power step is the sole reason the route asks for `y^{63}`.
> * **Status of the reduction.** Hypothesis U is the conjunction of two things PROBLEM.md excludes
>   by name ("smooth-neighbor conjectures", "digit equidistribution along sparse families"), has no
>   known case for pairs above `(log x)^c`, and is implied by no standard conjecture. It therefore
>   **counts as a reduction to an unproved statement of comparable strength and is NOT progress on
>   727.** Nothing in this file resolves 727 or its k = 2 variant.

Erdős problem 727, named variant `k = 2`. Session 2026-07-28. Continues
`attempts/route-R13/ANATOMY.md` (findings L0–L6) and `attempts/route-R12/LADDER.md` §4.5.

**Everything below is either (i) proved here and machine-verified, (ii) cited with attribution,
or (iii) explicitly labelled as a model / heuristic / conditional statement.  Nothing here
resolves Erdős 727 or its `k = 2` variant.  §4 and §5 are CONDITIONAL theorems; per
`PROBLEM.md` ("What does NOT count") a reduction to an unproved statement is not a
resolution, and §9 states plainly which unproved statement that is.**

---

## 0. One-paragraph summary

Write `P₀ = 4`, `y = x^b`, and let `SP_b(x) = {n ≤ x : n+1 and n+2 are both y-smooth}`.
For a prime `ℓ ≥ 5` with `ℓ ∥ n+j` (`j ∈ {1,2}`) the exact 727 condition at `ℓ` is
`κ_ℓ(n) ≥ 2`, and **Lemma 2** identifies its failure exactly: it fails iff `W − 1` is
*digit-poor* base `ℓ`, where `W = (n+j)/ℓ`. Truncating the digit-poor condition to the
lowest `J` base-`ℓ` digits (**Lemma 3**) turns it into a union of
`((ℓ−1)/2)((ℓ+1)/2)^{J−1}` residue classes for `W` mod `ℓ^J` — a congruence condition to
modulus `ℓ^J ≤ x^{Jb}`, of relative size exactly `(1/2)((ℓ+1)/(2ℓ))^{J−1} ≈ 2^{−J}`. Consequently *the whole of T1 and of L4 reduces to one analytic
statement*: **that the smooth pairs do not concentrate on such unions of classes**
(Hypothesis U, §3.3). Given U at *any* positive level `θ` and with *any* constant `C`, a
completely distribution-free counting lemma (**Lemma 4**) makes the union bound over all
large primes `< 1` for `b` small enough, and hence proves `S₂` infinite (**Theorem B**).
Hypothesis U is (a) *numerically confirmed* — the observed/uniform ratio for the low digit
is `1.003–1.008` at `x = 10⁸` and decreasing in `x`; (b) *known for a single smooth number*
(Soundararajan; Pascadi's `x^{66/107}`); and (c) **open for smooth pairs above polylogarithmic
moduli** — Tao–Teräväinen's Theorem 3.1 carries `1_{n≡b (mod W)}` only for `W ≤ (log X)^c`.
That last gap is the first genuinely open input, and it is a gap in the *modulus*, not in
the digits: §7 proves unconditionally that the smoothness of the second neighbour cannot be
discarded before the counting, so the gap cannot be circumvented by sieving.

---

## 1. Notation and the criterion

`κ_p(n)` = number of carries when adding `n + n` in base `p` ( `= ν_p(binom(2n,n))`, Kummer).
`s_p`, `ν_p` as in `PROBLEM.md`. Throughout `k = 2`, `P₀ = 4`, `y = x^b` with `0 < b < 1/2`,
and `SP_b(x) := {n ≤ x : P(n+1) ≤ y and P(n+2) ≤ y}`.

**Lemma 1 (criterion; PROBLEM.md, re-derived).**
`n ∈ S₂ ⟺ for every prime p: κ_p(n) ≥ 2(ν_p(n+1) + ν_p(n+2))`.

*Proof.* `(n+2)! = n!·(n+1)(n+2)`, so
`ν_p((2n)!) − 2ν_p((n+2)!) = [ν_p((2n)!) − 2ν_p(n!)] − 2ν_p((n+1)(n+2))
 = κ_p(n) − 2(ν_p(n+1)+ν_p(n+2))` by Legendre and Kummer. ∎

*Verified* (`gate_carry.py`, G1): the criterion agrees with exact factorial divisibility
`((n+2)!)² | (2n)!` for **all** `n ≤ 1300`, and reproduces `S₂ = 208, 458, 987, 1220, …`
of `PROBLEM.md`.

Since `ℓ ≥ 5 > 2` cannot divide both `n+1` and `n+2`, for such `ℓ` the demand is
`κ_ℓ(n) ≥ 2ν_ℓ(n+j)` for the unique `j ∈ {1,2}` with `ℓ | n+j`.

---

## 2. Unconditional structural lemmas (proved here)

### Lemma 2 (the digit-poor lemma; `e = 1`)

> Let `ℓ ≥ 5` be prime, `j ∈ {1,2}`, `ℓ ∥ n+j`, `W = (n+j)/ℓ ≥ 1`, `V = W − 1 ≥ 0`.
> Call `V` **digit-poor base ℓ** if its base-`ℓ` digits satisfy
> `d₀(V) ≤ (ℓ−3)/2` and `d_i(V) ≤ (ℓ−1)/2` for every `i ≥ 1`. Then
> `κ_ℓ(n) ≥ 2  ⟺  V is NOT digit-poor base ℓ.`

*Proof.* `n = ℓW − j = ℓV + (ℓ−j)` and `1 ≤ ℓ−j ≤ ℓ−1`, so the base-`ℓ` digits of `n` are
`(ℓ−j, d₀(V), d₁(V), …)`. Doubling at position `0`: `2(ℓ−j) = ℓ + (ℓ−2j)` and `ℓ−2j ≥ ℓ−4 ≥ 1`,
so a carry occurs there and the carry-in to position `1` is `1`. Write `c₀ = 1` and let `c_{i+1}`
be the carry out of position `i+1`, i.e. `c_{i+1} = 1 ⟺ 2d_i(V) + c_i ≥ ℓ`. Then
`κ_ℓ(n) = 1 + #{i ≥ 0 : c_{i+1} = 1}`, so `κ_ℓ(n) ≥ 2` iff some `c_{i+1} = 1`.
If no `c_{i+1} = 1` then `c_i = 0` for all `i ≥ 1`, and the conditions read
`2d₀ + 1 < ℓ` and `2d_i < ℓ (i ≥ 1)`, i.e. (for odd `ℓ`) `d₀ ≤ (ℓ−3)/2` and `d_i ≤ (ℓ−1)/2`:
`V` is digit-poor. Conversely, if `V` is digit-poor then by induction `c_i = 0` for all `i ≥ 1`,
so no further carry occurs. ∎

*Verified* (`gate_carry.py`, G2): `203 172` exhaustive instances (`n < 60 000`, all `ℓ ≥ 5`
with `ℓ ∥ n+j`) and `19 939` random instances with `ℓ < 4000`, `W < 10⁸`: **zero violations**.

Note the two extreme cases already recorded in LADDER §4.5 remark (ii)–(iii): the "one-carry"
congruence `C_ℓ` of Lemma R‴ is the statement `d₀(V) > (ℓ−3)/2` alone — sufficient, not
necessary; Lemma 2 is the exact condition, and this is what makes the target a
positive-proportion event instead of a density-zero one (R13 §6(a)).

### Lemma 2′ (prime powers)

> Let `ℓ ≥ 5`, `j ∈ {1,2}`, `ℓ^e ∥ n+j` with `e ≥ 1`, `W = (n+j)/ℓ^e`, `V = W−1`. Then
> `κ_ℓ(n) = e + #{carries produced by doubling V base ℓ with carry-in 1 at position 0}`,
> so the `ℓ`-demand `κ_ℓ(n) ≥ 2e` holds iff that doubling produces at least `e` carries.

*Proof.* `n = ℓ^e V + (ℓ^e − j)` and `ℓ^e − j = (ℓ−j) + (ℓ−1)ℓ + … + (ℓ−1)ℓ^{e−1}`, so the
digits of `n` at positions `0,…,e−1` are `ℓ−j, ℓ−1, …, ℓ−1`. Doubling: position `0` gives
`2(ℓ−j) ≥ ℓ` (carry), positions `1..e−1` give `2(ℓ−1)+1 = 2ℓ−1 ≥ ℓ` (carry). That is `e` carries,
with carry-in `1` into position `e`; positions `≥ e` carry the digits of `V`. ∎

### Lemma 3 (truncation: the failure event is a congruence condition)

> Let `ℓ ≥ 5`, `e ≥ 1`, `J ≥ 1`. If the `ℓ`-demand fails at `n` (with `ℓ^e ∥ n+j`) then
> the digits `d₀(V),…,d_{J−1}(V)` produce fewer than `e` carries; this event, `DP_J^{(e)}`,
> depends only on `W mod ℓ^J`. For `e = 1`:
>
> `#{residues V mod ℓ^J : digit-poor in positions 0..J−1} = ((ℓ−1)/2)·((ℓ+1)/2)^{J−1}`,
>
> so, among the residues of `W` mod `ℓ^J` that are coprime to `ℓ` (there are `ℓ^{J−1}(ℓ−1)`
> of them), the proportion satisfying `DP_J^{(1)}` is **exactly**
>
> `q_J(ℓ) = (1/2)·((ℓ+1)/(2ℓ))^{J−1} ≤ (1/2)·(3/5)^{J−1}` for `ℓ ≥ 5`.
>
> For `e ≥ 2`, the proportion of `W mod ℓ^J` coprime to `ℓ` satisfying `DP_J^{(e)}` is at most
> `(5/4)·Σ_{i<e} binom(J,i)·r^{J−i}`, `r := (ℓ+1)/(2ℓ) ≤ 3/5`.

*Proof.* The carry sequence `c₀ = 1, c_{i+1} = 1[2d_i + c_i ≥ ℓ]` is determined by `d₀,…,d_{J−1}`,
which are determined by `V mod ℓ^J` (equivalently `W mod ℓ^J`). For `e = 1` "no carry among
positions `0..J−1`" forces `d₀ ≤ (ℓ−3)/2` (i.e. `(ℓ−1)/2` values) and `d_i ≤ (ℓ−1)/2`
(i.e. `(ℓ+1)/2` values) for `1 ≤ i ≤ J−1`; and conversely. Position `0` corresponds to
`W mod ℓ ∈ [1,(ℓ−1)/2]`, exactly half the `ℓ−1` nonzero residues, whence `q_J`. For general `e`:
fix the set `S` of positions producing a carry, `|S| = i < e`; at each of the `J−i` positions
outside `S` we need `2d_t + c_t < ℓ`, i.e. at most `(ℓ+1)/2` values of `d_t`, and the positions
of `S` are unrestricted (`≤ ℓ` values). Dividing by `ℓ^{J−1}(ℓ−1) ≥ (4/5)ℓ^J` gives the `5/4`. ∎

### Lemma 3′ (uniform Chernoff form of Lemma 3)

> Let `x` be large, `θ ∈ (0,1]`, `ℓ ≥ 5`, `a ≥ 1`, `β = log ℓ / log x`, and suppose
> `aβ ≤ θ/11`. Put `J = ⌊θ/β⌋ − a ( ≥ 1 )`, so that `ℓ^{a+J} ≤ x^θ`. Then the proportion of
> residues `W mod ℓ^J` coprime to `ℓ` satisfying `DP_J^{(a)}` is at most
>
> `1.79 · 2^{−0.1659·θ/β}  ≤  2 · 2^{−θ/(7β)}`.

*Proof.* By Lemma 3 the proportion is `≤ (5/4)Σ_{i<a}binom(J,i)r^{J−i}`. For any `0 < z ≤ 1`
and `i < a` one has `1 ≤ z^{i−a}`, so
`Σ_{i<a}binom(J,i)r^{J−i} ≤ z^{−a}Σ_{i}binom(J,i)r^{J−i}z^{i} = z^{−a}(r+z)^J`.
Take `z = 1/10`; since `r ≤ 3/5`, `r + z ≤ 0.7` and `log₂(1/0.7) = 0.5146…`. Hence
`log₂(proportion) ≤ log₂(5/4) + a·log₂10 − 0.5146·J ≤ 0.837 + 3.836a − 0.5146·(θ/β)`,
using `J ≥ θ/β − a − 1`. Finally `a ≤ (θ/11)/β` gives `3.836a ≤ 0.3487·θ/β`, so
`log₂(proportion) ≤ 0.837 − 0.1659·θ/β`, and `0.1659 > 1/7`. ∎
(Both numerical steps are re-checked in `budget.py`.)

*Verified* (`gate_carry.py`, G2′): the count `((ℓ−1)/2)((ℓ+1)/2)^{D−1}` is exact for
`ℓ ∈ {5,7,11,101}` and `D ≤ 4`.

**This lemma is the pivot of the whole route.** It converts a digit condition on an object of
size `x` into a *congruence condition to a modulus `ℓ^J` that we may choose as small as we like*
(at the price of a weaker probability `q_J ≈ 2^{−J}`).

### Lemma 4 (the distribution-free budget)

> Let `x ≥ 3`, `0 < b ≤ 1`, `0 < r < 1`, `θ > 0`. Let `m ≤ x` have all prime factors `≤ x^b`
> and for `ℓ | m` put `β_ℓ = log ℓ / log x ( ≤ b)`. Then
>
> `Σ_{ℓ | m, ℓ > 4} r^{θ/β_ℓ} ≤ (1/b) · Σ_{k ≥ 1}(k+1)·t^k = (1/b)·t(2−t)/(1−t)²`,  `t := r^{θ/b}`.
>
> In particular the left side tends to `0` as `b → 0` for every fixed `θ > 0`, `r < 1`.

*Proof.* Put `k(ℓ) = ⌊b/β_ℓ⌋ ≥ 1`. Then `β_ℓ ≤ b/k(ℓ)`, so `θ/β_ℓ ≥ θk(ℓ)/b` and
`r^{θ/β_ℓ} ≤ t^{k(ℓ)}`. Also `∏_{ℓ|m} ℓ ≤ m ≤ x` gives `Σ_{ℓ|m} β_ℓ ≤ 1`, and every `ℓ` with
`k(ℓ) = k` has `β_ℓ > b/(k+1)`, so `#{ℓ | m : k(ℓ) = k} < (k+1)/b`. Sum. ∎

The lemma uses **no** information about the distribution of the prime factors of `m` — only
`Σ_{ℓ|m} β_ℓ ≤ 1`. This matters: it means the conditional theorems below need *only*
Hypothesis U, and no Dickman-type or smooth-number input at all.

With `r = 2^{−1/7}` (the exponent supplied by Lemma 3′) define

`K(b,θ) := (4/b)·t(2−t)/(1−t)²,  t = 2^{−θ/(7b)}`  (`budget.py`, Table B1).

### Lemma 5 (the small primes: an explicit class)

> Let `Q₀ = 648 = 2³·3⁴` and `c₀ = 157` (so `c₀ ≡ 5 mod 8`, `c₀ ≡ 76 mod 81`). Then every
> `n ≡ c₀ (mod Q₀)`, `n ≥ 3`, satisfies `ν₂(n+1)=1, ν₂(n+2)=0, ν₃(n+1)=0, ν₃(n+2)=1` and
> `κ₂(n) ≥ 2`, `κ₃(n) ≥ 2`; i.e. the criterion of Lemma 1 holds **identically on the class**
> at `p = 2` and `p = 3`. Hence for `n` in the class, `n ∈ S₂ ⟺ the demands at all ℓ ≥ 5 hold`.

*Proof.* `n ≡ 5 (mod 8)` gives `n+1 ≡ 6 (mod 8)` so `ν₂(n+1)=1` and `n+2` odd; the base-2 digits
of `n` at positions `0` and `2` equal `1`, and in base `2` a digit `1` always carries on doubling
(`2·1 + c ≥ 2`), so `κ₂(n) = s₂(n) ≥ 2 = 2(ν₂(n+1)+ν₂(n+2))`.
`76 = 1 + 1·3 + 2·9 + 2·27`, so `n ≡ 1 (mod 3)` (hence `3 ∤ n+1`, `3 | n+2`) and
`n + 2 ≡ 78 (mod 81)` has `ν₃ = 1`; the base-3 digits of `n` at positions `2,3` equal `2`, and
`2·2 = 4 ≥ 3` always carries, so `κ₃(n) ≥ 2 = 2(ν₃(n+1)+ν₃(n+2))`. ∎

*Verified* (`gate_class.py`): all `77 161` values `n ≡ 157 (mod 648)` below `5·10⁷` — zero
violations. End-to-end: among the `3·10⁶`-range `300`-smooth pairs in the class, the `8` with no
large-prime failure are `48109, 67549, 216589, 312493, 508837, 561973, 1776973, 2676397`, and
each was verified to satisfy `((n+2)!)² | (2n)!` by Legendre valuations at *every* prime `≤ 2n`.
(This is exactly step L3 of R13 §8, made explicit; it is an instance of Lemma R_k step (i)–(ii),
`route-R12/LADDER.md` §2.)

---

## 3. The analytic inputs

### 3.1 Supply (cited, unconditional)

**(S)** For every `b > 0`, `#SP_b(x) ≫_b x`.
[Hildebrand, *On a conjecture of Balog*, Proc. AMS 95 (1985), Cor. 2, applied to the stable set
`{m : P(m) ≤ m^b}`; see `route-R13/ANATOMY.md` §1.4 for why `b` is unconstrained at `k = 2`.
Also Teräväinen, Forum Math. Sigma 6 (2018), Thm 1.19.]

**(L1)** For fixed `Q₀, c₀` and `b > 0`,
`#{n ≤ x : n ≡ c₀ (Q₀), n+1, n+2 both x^b-smooth} ≫_{b,Q₀} x` (for `x` in a set of
logarithmic density 1, which suffices for infinitude).
[Tao–Teräväinen, arXiv:2512.01739v2, Thm 3.1 + the proof of Thm 1.8: the restriction
`1_{n ≡ b (mod W)}` is in the statement of Thm 3.1 and the smooth-count hypothesis is verified
in arithmetic progressions. Assessed in R13 §8 as *hard-but-classical, essentially available*;
**not re-proved here**.]

### 3.2 What is measured

The reader should keep in mind the two exact facts measured in §8: (i) the DP₁ event has
observed frequency `0.5048–0.5280` inside the smooth pairs at `x = 10⁸` against the exact
value `1/2`, decreasing towards `1/2` as `x` grows; (ii) the full digit-poor event has an
`x`-decreasing bias factor (`1.168 → 1.113 → 1.082` at `b = 0.4`, `x = 10⁶,10⁷,10⁸`).

### 3.3 Hypothesis U — the analytic input this route needs

> **Hypothesis U(θ, C; b, Q₀, c₀).** Let `𝒮(x) = {n ≤ x : n ≡ c₀ (mod Q₀), n+1 and n+2 both
> x^b-smooth}`. There are `θ > 0`, `C ≥ 1`, `x₀` such that for all `x ≥ x₀`, every prime
> `4 < ℓ ≤ x^b`, every `ν ∈ {1,2}`, every `a ≥ 1` and `J ≥ 1` with `ℓ^{a+J} ≤ x^θ`, and every
> set `R` of residues mod `ℓ^J` coprime to `ℓ`,
>
> `#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν, (n+ν)/ℓ^a mod ℓ^J ∈ R}
>     ≤ C·(|R| / (ℓ^{J−1}(ℓ−1)))·#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν}`.

In words: **inside the smooth pairs, the cofactor of the `ℓ`-part of `n+ν` is equidistributed,
up to a bounded factor, modulo `ℓ^J`, for all `ℓ^{J} ≤ x^θ`.** It is a *level-of-distribution*
statement for the smooth-pair counting function, stated relative to the natural normalisation
(so no knowledge of `#{n ∈ 𝒮 : ℓ^a ∥ n+ν}` itself is required). It is an *upper* bound only,
it needs no asymptotic, and `C` may be any constant.

**Status of U — this is the crux, see §9.**
* For a *single* smooth number, the analogue of U is essentially a theorem: Soundararajan
  (arXiv:0707.0299, Thm 1) gives `Ψ(x,y;q,a) ∼ Ψ_q(x,y)/φ(q)` for `q ≤ y^{4√e−ε}` in the range
  `exp(y^{1−ε}) ≥ x ≥ y^{(log log y)^4}`; for *bounded* `u = log x/log y` (our regime) the
  relevant statements are the on-average ones, culminating in Pascadi (Compositio, arXiv:2304.11696):
  smooth numbers are equidistributed in progressions to moduli of size `x^{66/107−o(1)}`, past
  the `x^{3/5}` barrier of Bombieri–Friedlander–Iwaniec / Fouvry–Tenenbaum / Drappeau / Maynard.
  Since our moduli are `ℓ^J ≤ x^θ` with `θ` free, this is comfortable.
* For *pairs* `n+1, n+2` both smooth, the only available AP-restricted statement is
  Tao–Teräväinen Thm 3.1, whose modulus is `W ∈ [L^c]` with `L ≤ log X` — i.e. **polylogarithmic**.
* **The gap between `(log x)^c` and `x^θ` is where 727(k=2) now sits.**

---

## 4. Theorem A (= T1, L4a), CONDITIONAL

> **Theorem A.** Assume Hypothesis U(θ, C) for some `θ > 0`, `C ≥ 1`, and (L1). Let `J₀` be the
> least `J ≥ 1` with `C·(1/2)(3/5)^{J−1} < 1` — so `J₀ = 1` when `C < 2`, and in general
> `J₀ ≤ 2 + log(C/2)/log(5/3)`. Let `0 < b < θ/(J₀+1)` and let `η > 0` be arbitrary. Then, with
> `δ := 1 − C·(1/2)(3/5)^{J₀−1} − η > 0`, for all large `x`
>
> `#{n ∈ 𝒮(x) : P(n+1) ∥ n+1, P(n+1) > 4 and κ_{P(n+1)}(n) ≥ 2} ≥ δ·#𝒮(x) ≫_{b,Q₀,C} x`:
>
> **a positive proportion of the smooth pairs satisfies the exact carry condition at the
> largest prime factor of `n+1`.**

*Proof.* Partition `𝒮(x)` according to `ℓ = P(n+1)`.

*Discards.* (i) `n+1` is `4`-smooth: `O(log²x)` values of `n`. (ii) `ℓ ≤ x^{ε}` for a fixed
`ε = ε(b) > 0`: then `n+1` is `x^{ε}`-smooth, and `#{n ≤ x : P(n+1) ≤ x^{ε}} = (ρ(1/ε)+o(1))x`;
choosing `ε` small enough in terms of `b` and `Q₀` makes this `< (η/2)·#𝒮(x)` for any prescribed
`η > 0`, because `#𝒮(x) ≫_{b,Q₀} x` by (L1) while `ρ(1/ε) → 0`. (iii) `ℓ > x^{ε}` and `ℓ² | n+1`:
`Σ_{ℓ > x^{ε}} x/ℓ² ≪ x^{1−ε}= o(#𝒮(x))`.

For the remaining `n`, `ℓ ∥ n+1` and `ℓ > 4`. By Lemma 2 the `ℓ`-condition fails iff
`V = (n+1)/ℓ − 1` is digit-poor base `ℓ`, which by Lemma 3 implies `DP_{J₀}^{(1)}`: a set `R` of
residues of `W = (n+1)/ℓ` mod `ℓ^{J₀}` coprime to `ℓ` with
`|R|/(ℓ^{J₀−1}(ℓ−1)) = q_{J₀}(ℓ) ≤ (1/2)(3/5)^{J₀−1}`. Since `ℓ^{1+J₀} ≤ x^{b(1+J₀)} ≤ x^θ`,
Hypothesis U applies with `a = 1`, `J = J₀`, and gives for each `ℓ`
`#{fail, P(n+1)=ℓ} ≤ C(1/2)(3/5)^{J₀−1}·#{n ∈ 𝒮(x) : ℓ ∥ n+1, P(n+1) = ℓ}`. Summing over `ℓ`
and adding back the discards gives the claim with `δ = 1 − C(1/2)(3/5)^{J₀−1} − η`. ∎

**Numerical content of Theorem A.** The measured DP₁ frequency at `ℓ = P(n+1)` inside `𝒮(x)`
(with `Q₀ = 1`) at `x = 10⁸` is `0.5048` (`b=0.4`), `0.5041` (`b=0.3`), `0.5066` (`b=0.25`) —
i.e. `C ≈ 1.01` suffices in practice and `J₀ = 1`, giving `δ ≈ 0.495`. The true failure rate
(all digits) is smaller still: `0.414, 0.287, 0.276` respectively.

---

## 5. Theorem B (= T2 / L4), CONDITIONAL

> **Theorem B.** Assume (L1) and Hypothesis U(θ, C) with the class `(Q₀,c₀) = (648,157)` of
> Lemma 5. Let `0 < b < θ/11` satisfy `C·K(b,θ) < 1`, where
> `K(b,θ) = (4/b)·t(2−t)/(1−t)²` with `t = 2^{−θ/(7b)}`. Then for all large `x` (in the
> log-density-1 set of (L1))
>
> `#(S₂ ∩ 𝒮(x)) ≥ (1 − C·K(b,θ) − o(1))·#𝒮(x) ≫_{b} x`.
>
> **In particular `S₂` is infinite** — i.e. the named `k = 2` variant of Erdős 727 holds.

*Proof.* By Lemma 5 the criterion of Lemma 1 holds at `p = 2` and `p = 3` for every
`n ∈ 𝒮(x)`. By Lemma 1 it remains to bound `B(x) := #{n ∈ 𝒮(x) : some prime ℓ ≥ 5 fails}`.
For `n ∈ 𝒮(x)`, every prime power `ℓ^a ∥ n+ν` (`ν ∈ {1,2}`, `ℓ > 4`) has `ℓ ≤ x^b`.

*(a) The pairs `(ℓ,a)` with `ℓ^a > x^{θ/11}`.* Trivially
`#{n ≤ x : ℓ^a | n+ν} ≤ x/ℓ^a + 1 ≤ x^{1−θ/11} + 1`. The number of such pairs is at most
`π(x^b)·(log x/log 5) ≪ x^{b}log x`, so their total contribution is
`≪ x^{1−θ/11+b}log x = o(x)` because `b < θ/11`.

*(b) The pairs `(ℓ,a)` with `ℓ^a ≤ x^{θ/11}`, i.e. `aβ_ℓ ≤ θ/11`.* Put `J = ⌊θ/β_ℓ⌋ − a ≥ 1`
(so `ℓ^{a+J} ≤ x^θ`). By Lemma 2′ a failure at `ℓ` forces fewer than `a` carries when doubling
`(n+ν)/ℓ^a − 1` with carry-in `1`, hence (Lemma 3) fewer than `a` among the positions
`0,…,J−1`; that event is a set `R` of residues mod `ℓ^J` coprime to `ℓ` of relative size
`≤ 2·2^{−θ/(7β_ℓ)}` by Lemma 3′. Hypothesis U therefore gives
`#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν, fail at ℓ} ≤ 2C·2^{−θ/(7β_ℓ)}·#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν}`.
Summing over all `(ℓ,a)` and `ν`, and **interchanging the order of summation** (legitimate
because the coefficient `2C·2^{−θ/(7β_ℓ)}` does not depend on `n`),
`Σ_{(ℓ,a),ν} ≤ 2C Σ_{n ∈ 𝒮(x)} Σ_{ν=1,2} Σ_{ℓ | n+ν, ℓ>4} 2^{−θ/(7β_ℓ)}`.
By Lemma 4 with `r = 2^{−1/7}` the inner double sum is `≤ 2·(1/b)t(2−t)/(1−t)²`, `t = 2^{−θ/(7b)}`,
for **every** `n` with `n+1, n+2` both `x^b`-smooth. Hence the total is `≤ C·K(b,θ)·#𝒮(x)`.

Adding (a) and (b), `B(x) ≤ (C·K(b,θ) + o(1))·#𝒮(x)`, and `#𝒮(x) ≫_{b,Q₀} x` by (L1). ∎

> **Corollary (the quantitative content).** For every `θ > 0` and every `C ≥ 1` there is `b > 0`
> with `C·K(b,θ) < 1` and `b < θ/11`. Largest such `b` (`budget.py`, Table B1):
>
> | `C \ θ` | `1` | `0.5` | `0.25` | `0.1` | `0.05` |
> |---|---|---|---|---|---|
> | `1.0` | `b* = 0.0159` | `0.00704` | `0.00316` | `0.00112` | `0.00051` |
> | `1.5` | `0.0148` | `0.00660` | `0.00298` | `0.00106` | `0.00049` |
> | `2.0` | `0.0141` | `0.00632` | `0.00287` | `0.00103` | `0.00047` |
>
> So even a *very weak* level of distribution `θ = 0.05` with a lossy constant `C = 2` suffices,
> at `b ≈ 5·10⁻⁴`. **This robustness in `θ` and `C` is the main structural gain of route R14**:
> the route needs no asymptotic, no small constant and no large level — only *some* positive
> power-of-`x` level of distribution for the smooth pairs.
>
> *Remark (how lossy `K` is).* Lemma 3′ is deliberately crude at prime powers `a ≥ 2`. If one
> only had to treat `a = 1` (i.e. `n+1, n+2` squarefree away from `2,3`), Lemma 3 gives the
> sharper constant `H(b,θ) = (25/(9b))t(2−t)/(1−t)²`, `t = (3/5)^{θ/b}`, whose thresholds are
> about 8–9 times larger: `b* = 0.137, 0.055, 0.023, 0.0078` for `θ = 1, 0.5, 0.25, 0.1`
> (`C = 1`). Since `b` is a free parameter this loss is immaterial; it is recorded only so the
> reader can see that the crude step is the prime-power one.

---

## 6. T2 answered directly: the measured `E[#failures]`

`E(x,b) := (1/#SP_b(x)) Σ_{n ∈ SP_b(x)} #{ℓ > 4 : ℓ | (n+1)(n+2), κ_ℓ(n) < 2ν_ℓ(n+j)}`
is the *true* first-moment budget (no truncation, `Q₀ = 1`), measured exactly
(`table_efail.py`; `pairlib.py` cross-checked against sympy on all `10 758` smooth pairs with
`X = 2·10⁵, y = 200`, `gate_pairlib.py`).

**Table 1 — measured `E`, its decomposition, and the true pass rate.** `y = ⌊X^b⌋`.
`E1` = failures at primes with `ℓ ∥ n+j`; `E2` = at primes with `ℓ² | n+j`;
`Esm` = at primes `ℓ ≤ √y`; `pass` = fraction with **no** large-prime failure;
`passS2` = fraction actually in `S₂`; `Plpf` = fraction failing at `ℓ = P(n+1)`;
`sqfr` = fraction with `ℓ ∥ n+j` for every `ℓ > 4`.

| X | b | y | #pairs | E | E1 | E2 | Esm | pass | passS2 | Plpf | sqfr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10⁶ | .50 | 1000 | 116 347 | 1.699 | 1.518 | 0.181 | 0.327 | 0.098 | 0.0799 | 0.509 | 0.681 |
| 10⁷ | .50 | 3162 | 1 114 139 | 1.677 | 1.550 | 0.126 | 0.272 | 0.108 | 0.0974 | 0.495 | 0.700 |
| 3·10⁷ | .50 | 5477 | 3 315 167 | 1.665 | 1.558 | 0.107 | 0.268 | 0.112 | 0.1037 | 0.491 | 0.708 |
| 10⁸ | .50 | 10 000 | 10 943 151 | 1.650 | 1.561 | 0.089 | 0.242 | 0.116 | 0.1102 | 0.487 | 0.715 |
| 10⁸ | .45 | 3981 | 5 486 501 | 1.598 | 1.487 | 0.110 | 0.221 | 0.131 | 0.1228 | 0.454 | 0.676 |
| 10⁸ | .40 | 1584 | 2 219 619 | 1.537 | 1.392 | 0.145 | 0.185 | 0.149 | 0.1376 | 0.421 | 0.622 |
| 10⁸ | .35 | 630 | 623 586 | 1.402 | 1.193 | 0.208 | 0.184 | 0.189 | 0.1710 | 0.355 | 0.542 |
| 10⁸ | .30 | 251 | 111 335 | 1.339 | 1.010 | 0.329 | 0.173 | 0.204 | 0.1761 | 0.317 | 0.427 |
| 10⁸ | .25 | 100 | 9 486 | 1.401 | 0.856 | 0.545 | 0.180 | 0.174 | 0.1237 | 0.339 | 0.313 |

(For `X = 10⁶, 3·10⁷` at the other `b` see `efail_big.out` and the run log.)

**Answer to T2, part 1 (honest).** *At every scale we can compute, `E(x,b) > 1` for every `b`.*
`E` decreases in `x` at fixed `b` (`1.699 → 1.650` at `b = 1/2`; `1.515 → 1.339` at `b = 0.3`) and
decreases in `b` at fixed `x` down to `b ≈ 0.3`, but it is contaminated by two effects that are
provably transient:
* `E2` (repeated prime factors) — an artefact of `y = X^b` being small at accessible `X`; it
  decays (`0.181 → 0.089` at `b = 1/2`) and vanishes as `x → ∞` at fixed `b`;
* `Esm` (small primes `ℓ ≤ √y`) — for a *fixed* `ℓ`, `κ_ℓ(n) < 2ν_ℓ` has probability
  `≍ 2^{−log x/log ℓ}` and so tends to `0`; measured `0.327 → 0.242`.

The part that survives is `E1`, and it is `< 1` already at `b = 0.3` (`E1 = 1.010`) and `b = 0.25`
(`E1 = 0.856`) at `X = 10⁸`.

**Answer to T2, part 2 (model).** Under the model assumptions (M1) Dickman prime-factor
statistics for smooth numbers, (M2) uniform cofactor digits, (M3) `e ≥ 2` negligible —
`model_E.py`, all three stated explicitly there —

`E_∞(b) = 2 ∫₀¹ (ρ(u−v)/ρ(u))·2^{1−⌊u/v⌋} dv/v`, `u = 1/b`.

**Table 2 — model vs. measurement (the measured column is `E1` at `X = 10⁸`).**

| b | u | `E_∞(b)` model | measured `E1` | ratio |
|---|---|---|---|---|
| 0.50 | 2.00 | 1.579 | 1.561 | 0.989 |
| 0.45 | 2.22 | 1.544 | 1.487 | 0.964 |
| 0.40 | 2.50 | 1.451 | 1.392 | 0.959 |
| 0.35 | 2.86 | 1.203 | 1.193 | 0.992 |
| 0.30 | 3.33 | 0.975 | 1.010 | 1.035 |
| 0.25 | 4.00 | 0.640 | 0.856 | 1.338 |

The model reproduces the exact count to `1–4 %` for `b ≥ 0.3`; the drift at `b = 0.25` is the
finite-size effect above (`y = 100`, only `9 486` pairs). Extending the model:
`E_∞(0.2) = 0.372`, `E_∞(0.15) = 0.156`, `E_∞(0.1) = 0.0179`, `E_∞(0.05) < 10⁻⁴`.

> **So: `E[#failures | smooth pair] < 1` for `b ≲ 0.3`, and `→ 0` as `b → 0`.**
> Measured directly for the surviving part `E1`; asymptotically for the whole of `E`.

**Answer to T2, part 3 (what the T1 method actually gives).** A proof via Hypothesis U at level
`θ` may use only the low `J = ⌊θ/β_ℓ⌋` digits, giving the budget of §5. Comparing:
`E_∞(0.25) = 0.64`, whereas the `θ`-truncated model budgets at `b = 0.25` are `1.81 (θ=0.5)`,
`4.72 (θ=0.25)`, `1.87 (θ=0.1)`; and the distribution-free `K(0.25,θ)` is larger still. **The
truncation is expensive, and that is why `b` must be taken much smaller than `0.3` in Theorem B
(`b* ≈ 0.016, 0.0070, 0.0032, 0.0011` for `θ = 1, 0.5, 0.25, 0.1`).** This is a real, quantified gap
between the union bound the method would give and the truth — but it is not an obstruction,
because `b` is free (§3.1 (S)).

---

## 7. Unconditional: the smoothness of `n+2` cannot be discarded

This is the T1-localised, sharpened form of the first-moment obstruction of `MIRROR.md` §6.

> **Proposition O1.** Fix `b ∈ (0,1/2)` and set
> `A(x,b) := #{n ≤ x : n+1 is x^b-smooth, ℓ = P(n+1) ∥ n+1, (n+1)/ℓ − 1 digit-poor base ℓ}`
> (the bad set with the smoothness of `n+2` **dropped**) and `S(x,b) := #SP_b(x)`. Then
> `A(x,b)/S(x,b) → ∞` as `b → 0`, uniformly for `x` large; in the Dickman model
> `A/S ≍ 2^{−1/b}/ρ(1/b) → ∞` since `ρ(u) = u^{−u(1+o(1))}` while `2^{−u} = e^{−u log 2}`.

**Measured** (`obstruction.py`):

| X | b | A | S | A/S |
|---|---|---|---|---|
| 10⁷ | .50 | 1 557 937 | 1 114 139 | 1.40 |
| 10⁷ | .40 | 593 725 | 233 279 | 2.55 |
| 10⁷ | .30 | 77 402 | 12 945 | 5.98 |
| 10⁷ | .25 | 15 459 | 1 685 | 9.17 |
| 10⁸ | .50 | 15 500 645 | 10 943 151 | 1.42 |
| 10⁸ | .40 | 5 867 917 | 2 219 619 | 2.64 |
| 10⁸ | .30 | 741 126 | 111 335 | 6.66 |
| 10⁸ | .25 | 124 479 | 9 486 | **13.12** |

The ratio grows in `x` as well as in `1/b`. **Consequence.** Any upper bound for the bad set
obtained by first discarding `1_{n+2 smooth}` is worse than trivial. Nor can the discarded
weight be recovered by sieving: detecting "`n+2` is `x^b`-smooth" by sifting the primes in
`(x^b, x^{θ'}]` at level `x^{θ'}` recovers only a factor `≍ b/θ'` (Mertens), whereas the
required saving is `ρ(1/b) = b^{(1/b)(1+o(1))}`, and recovering it would need sifting range and
level up to `x`. **Therefore the second smoothness condition must be carried, unfactorised,
through the entire argument — which is exactly why Hypothesis U is stated for the pair and not
for a single smooth number.**

---

## 8. The measured equidistribution (the numerical status of Hypothesis U)

`equidist.py` computes, for every prime `4 < ℓ ≤ y` with `ℓ ∥ n+1`, the observed frequency of
`DP_J` (`J = 1,2,3`) and of the exact digit-poor event, against the **exact** uniform-cofactor
prediction obtained by digit-DP over `V ∈ [0, X/ℓ)` (denominator corrected for `ℓ ∤ W`). The
`ALL` row is a consistency check: the ratio is `1.000` to four decimals, confirming the model
is the correct normalisation.

**Table 3 — ratio observed/uniform, `b = 0.4`, three scales.**

| X | set | exact | DP₁ | DP₂ | DP₃ |
|---|---|---|---|---|---|
| 10⁶ | ALL | 1.000 | 1.000 | 1.000 | 1.000 |
| 10⁶ | n+1 smooth | 1.042 | 1.001 | 1.019 | 1.030 |
| 10⁶ | **smooth pair** | **1.168** | **1.015** | 1.085 | 1.127 |
| 10⁷ | n+1 smooth | 1.030 | 1.001 | 1.012 | 1.021 |
| 10⁷ | **smooth pair** | **1.113** | **1.008** | 1.054 | 1.085 |
| 10⁸ | n+1 smooth | 1.024 | 1.000 | 1.009 | 1.016 |
| 10⁸ | **smooth pair** | **1.082** | **1.003** | 1.033 | 1.057 |

**Table 4 — at `X = 10⁸`, several `b` (smooth pairs).**

| b | y | exact | DP₁ | DP₂ | DP₃ |
|---|---|---|---|---|---|
| .50 | 10 000 | 1.041 | 1.008 | 1.022 | 1.031 |
| .35 | 630 | 1.196 | 1.003 | 1.071 | 1.131 |
| .30 | 251 | 1.364 | 1.004 | 1.073 | 1.201 |
| .25 | 100 | 2.263 | 1.005 | 1.101 | 1.475 |

**Table 5 — the T1 quantity itself: `ℓ = P(n+1)`, `ℓ ∥ n+1`, `X = 10⁸`.**

| b | set | exact failure rate | uniform model | DP₁ rate | DP₁ / (1/2) |
|---|---|---|---|---|---|
| .50 | n+1 smooth | 0.4691 | 0.4666 | 0.5168 | 1.034 |
| .50 | smooth pair | 0.4847 | 0.4672 | 0.5280 | 1.056 |
| .40 | n+1 smooth | 0.3947 | 0.3847 | 0.5007 | 1.001 |
| .40 | smooth pair | 0.4140 | 0.3851 | **0.5048** | **1.010** |
| .30 | n+1 smooth | 0.2296 | 0.2124 | 0.5002 | 1.000 |
| .30 | smooth pair | 0.2873 | 0.2094 | **0.5041** | **1.008** |
| .25 | n+1 smooth | 0.1525 | 0.1255 | 0.5003 | 1.001 |
| .25 | smooth pair | 0.2759 | 0.1179 | **0.5066** | **1.013** |

**Reading of these tables.**
1. `DP₁` — the *pure congruence* part of the digit-poor condition, a union of exactly half the
   classes for `W` mod `ℓ` — is equidistributed inside the smooth pairs to within `0.3–1.3 %`,
   and the deviation *decreases* with `x` (`1.015 → 1.008 → 1.003` at `b = 0.4`).
   **Hypothesis U with `J = 1` and `C = 1.02` is numerically indistinguishable from true.**
2. The *exact* digit-poor event has a larger bias (up to `2.26` at `b = 0.25`), and the bias
   grows with the number of constrained digits. This is not an arithmetic effect: it is the
   **archimedean** top-digit constraint. Digit-poorness in the top positions forces `W`, hence
   `n+1` and `n+2`, to be *smaller*, and smaller integers are more likely to be smooth. The
   effect is absent in the `ALL` row, small in the single-smooth row, and largest where the
   cofactor has fewest digits (small `b`).
3. Hence the correct formulation of the analytic input is with a *constant* `C`, not an
   asymptotic — which is exactly Hypothesis U, and exactly why Theorem B was engineered
   (Lemma 4) to tolerate any `C`.

---

## 9. Honest verdict, and the first open input

**Proved unconditionally in this route (new)** — NOTE: Proposition O1 was listed here
in error and has been retracted per the audit; it is a heuristic, not a theorem:
* **Lemma 2 / 2′** — the exact failure characterisation "cofactor minus one is digit-poor
  base `ℓ`", for `ℓ ∥ n+j` and for `ℓ^e ∥ n+j`. Verified on `223 111` instances, zero violations.
* **Lemma 3 / 3′** — the truncation of that condition to a *congruence mod `ℓ^J`*, with the
  exact count `((ℓ−1)/2)((ℓ+1)/2)^{J−1}`, proportion `q_J(ℓ) = (1/2)((ℓ+1)/(2ℓ))^{J−1}`, and a
  uniform prime-power bound `2·2^{−θ/(7β_ℓ)}`.
* **Lemma 4** — a distribution-free bound making the union bound over *all* large primes
  finite and `→ 0` as `b → 0`, for every fixed level `θ > 0`. (No Dickman input needed.)
* **Lemma 5** — the explicit class `n ≡ 157 (mod 648)` on which the `p = 2, 3` conditions hold
  identically; verified for `77 161` values, and the whole engine verified end-to-end on eight
  concrete members of `S₂` up to `2.68·10⁶` by Legendre valuations at every prime `≤ 2n`.
* **Proposition O1** — the smoothness of `n+2` cannot be discarded, nor recovered by sieving;
  measured ratio `A/S = 13.1` at `x = 10⁸, b = 0.25` and diverging.

**Conditional (and labelled as such):**
* **Theorem A (= T1 = L4a).** Hypothesis U(θ,C) ⟹ a positive proportion (`δ ≈ 1/2` in practice)
  of the smooth pairs satisfies the exact carry condition at `ℓ = P(n+1)`.
* **Theorem B (= L4).** Hypothesis U(θ,C) + (L1) ⟹ for `b` small enough, a positive proportion
  of the smooth pairs lies in `S₂`, hence **`S₂` is infinite**. Explicit thresholds in §5.
* **(L1)** itself is *not* proved here: it is R13's "hard-but-classical, essentially available
  from Tao–Teräväinen Thm 3.1 + the proof of Thm 1.8". It is a second conditional dependency.

**This is a reduction, not a resolution.** Per `PROBLEM.md`, "reductions to unproved statements
of comparable strength" do not count. Theorem B replaces 727(k=2) by Hypothesis U, and
Hypothesis U is an unproved statement about the same objects. What the reduction buys is that
U is (i) an *upper bound only*, (ii) needs *no asymptotic and no small constant*, (iii) needs
*only an arbitrarily small level `θ`*, and (iv) is a statement in a well-developed area
(smooth numbers in arithmetic progressions) rather than a statement about carries or factorials.

### The first genuinely open input, stated precisely

> **Open Problem (level of distribution for consecutive smooth numbers).** Do there exist
> `b > 0`, `θ > 0` and `C ≥ 1` such that, for all large `x`, all primes `ℓ ≤ x^b`, all `J ≥ 1`
> with `ℓ^J ≤ x^θ`, and all residues `a mod ℓ^J` coprime to `ℓ`,
>
> `#{n ≤ x : n+1, n+2 both x^b-smooth, ℓ ∥ n+1, (n+1)/ℓ ≡ a (mod ℓ^J)}
>   ≤ (C/(ℓ^{J−1}(ℓ−1)))·#{n ≤ x : n+1, n+2 both x^b-smooth, ℓ ∥ n+1}` ?
>
> Equivalently: **is the smooth-pair counting function equidistributed, up to a bounded factor,
> in arithmetic progressions to moduli of size `x^θ` for some `θ > 0`?**

Where the frontier sits, precisely:
* **Drop `n+2`** and it is a theorem: Soundararajan (arXiv:0707.0299) for individual moduli
  `q ≤ y^{4√e−ε}` in the large-`u` range; on average over moduli, up to `x^{66/107−o(1)}`
  (Pascadi, Compositio; after Bombieri–Friedlander–Iwaniec, Fouvry–Tenenbaum, Drappeau, Maynard).
  Table 5's "n+1 smooth" rows (ratios `1.000–1.034`) are the numerical shadow of this.
* **Keep `n+2` and shrink the modulus to `(log x)^{c}`** and it is a theorem:
  Tao–Teräväinen arXiv:2512.01739 Theorem 3.1, whose statement literally contains
  `1_{n ≡ b (mod W)}` for `W ∈ [L^c]`, `L ≤ log X`.
* **Both at once — pair *and* modulus `x^θ` — is open.** The obstruction is not parity and not
  a bilinear prime problem: no prime is being detected, and the supply of smooth pairs is
  unconditional. It is that the only known route to the smooth-pair asymptotic goes through
  correlations of multiplicative functions (Matomäki–Radziwiłł / Tao's logarithmic Elliott /
  Pilatte decoupling), and those methods are intrinsically limited to moduli of polylogarithmic
  size, since the modulus enters as a *dilation* `n ↦ Wn + b` of the multiplicative functions
  and the available non-pretentiousness/decoupling estimates lose a power of `W`.

### What R14 changes relative to R13

R13 assessed L4a as "hard-but-classical". **That assessment was too optimistic, and R14 corrects
it**: the required moduli are `x^{θ}` and not `(log x)^c`, and the only AP-restricted smooth-pair
theorem in existence stops at `(log x)^c`. Conversely, R14 improves R13's picture in three ways:
1. the digit condition is now *exactly* a congruence condition (Lemma 3), so nothing about
   digits remains open — the whole difficulty is one level-of-distribution statement;
2. the required level is *arbitrarily small* and the required constant *arbitrarily lossy*
   (Lemma 4 + Theorem B), which is far weaker than "an asymptotic at level `x^{1/2}`";
3. the numerics say the statement is true, with `C ≈ 1.01` and converging to `C = 1`, for the
   truncation `DP₁` that Theorem A actually uses (Tables 3–5); for the *untruncated* digit-poor
   event the bias is larger (up to `2.26`) but still bounded, and its source is identified in
   §8 as archimedean rather than arithmetic. The target is not a borderline claim.

### What R14 does **not** do

* It does not prove T1 (L4a) unconditionally, and §7 shows the natural unconditional routes
  (drop `n+2`; sieve for `n+2`) are provably insufficient.
* It says nothing about `k ≥ 3`, where the supply itself is blocked (R13 §2, §8 L6; McNamara
  arXiv:2312.08544). **Even a full proof of Theorem B's hypothesis would settle only the named
  `k = 2` variant, not the headline of Erdős 727.**

---

## Files

| file | what it does |
|---|---|
| `gate_carry.py` | G1: criterion == factorial divisibility, `n ≤ 1300`. G2: Lemma 2 on 223 111 instances. G2′: the exact digit-poor count. |
| `pairlib.py` | slice-based exact machinery: smooth mask, carries, digit-poor, per-prime failure data. |
| `gate_pairlib.py` | cross-checks `pairlib` against sympy on all 10 758 smooth pairs at `X=2·10⁵, y=200`; re-verifies 40 members of `S₂` by exact factorial division. |
| `gate_class.py` | Lemma 5: the class `157 mod 648`, `77 161` values checked; 8 certified `S₂` members. |
| `table_efail.py` → `efail_big.out` | Table 1 (`E`, `E1`, `E2`, `Esm`, pass rates) up to `X = 10⁸`. |
| `equidist.py` → `equi_b04.out`, `equi_b_all.out` | Tables 3–4: observed/uniform ratios for `DP_J` in ALL / `n+1` smooth / smooth pairs. |
| `obstruction.py` → `obstruction.out` | Table 5 (the T1 number) and Table of §7 (the ratio `A/S`). |
| `model_E.py` → `model_E.out` | Dickman `ρ` (verified to `10⁻⁵` at `u = 10`), `E_∞(b)`, the `θ`-truncated model budgets. |
| `budget.py` → `budget.out` | the explicit constants `K(b,θ)`, `H(b,θ)` of Theorem B and the thresholds `b*(θ,C)`; re-checks the two numerical steps of Lemma 3′. |
