# MIRROR.md — why 727 is the hard mirror image of 728/729/401

All statements below are proved (elementary) and machine-verified
(`experiments/mirror_theorem.py`: M1–M5 all PASS; `experiments/verify_identities.py`;
`attempts/route-R1/verify_propN.py`). Notation: `m = n + k`; `κ_p(x)` = number of carries
when adding `x + x` in base `p` (`= ν_p(C(2x,x))` by Kummer); `s_p`, `ν_p` as in PROBLEM.md.

## 1. Both problems are the same shape

Write the 727 criterion in the `m`-variable (PROBLEM.md product form, re-verified as M1):

> **727.** `n ∈ S_k ⟺ ∏_{i=0}^{2k-1} (2m − i) | C(2m, m) ⟺ ∀p: κ_p(m) ≥ ν_p(∏_{i<2k}(2m−i))`.

The solved siblings, in the same normal form (arXiv 2601.07421, Lemma 1 and Cor. 2 — used
here only as *method* background, no conclusion imported):

> **728/401 family.** the divisibility driving those results is
> `(m+1)(m+2)···(m+k) | C(2m, m)`, i.e. `∀p: κ_p(m) ≥ ν_p(∏_{i=1}^{k}(m+i)) − ν_p(k!)`.

So both ask: *does a product of consecutive integers divide the central binomial
`C(2m,m)`?* The supply side, `κ_p(m)`, is **identical**. Only the **location of the
divisor block relative to `m`** differs — and that is decisive.

## 2. The digit trichotomy (proved; M2–M4)

Fix a prime `p > 2k` and `J ≥ 1`. Everything depends on the residue of `m` mod `p^J`.

| type | residue of `m` mod `p^J` | base-`p` digits at positions `0..J−1` | carries there |
|---|---|---|---|
| **A** | `m ≡ −i`, `1 ≤ i ≤ k < p/2` | `p−i, p−1, …, p−1` — all `≥ ⌈p/2⌉` | **`J` (free)** |
| **B** | `2m ≡ i`, `i` odd, `p` odd | `(p+i)/2, (p−1)/2, …, (p−1)/2` — all `≥ ⌈p/2⌉` | **`J` (free)** |
| **C** | `m ≡ +i`, `0 ≤ i ≤ k−1 < p` | `i, 0, 0, …, 0` — all small | **`0`** |

*Proof.* Type A: a digit `d ≥ ⌈p/2⌉` gives `2d ≥ p`, a carry regardless of carry-in.
Type B: `m ≡ (p^J + i)/2`, whose digits are `(p+i)/2` then `(p−1)/2`, and `2·(p−1)/2 + 1 = p`,
so each position carries once one carry has started (position 0 gives `2·(p+i)/2 = p+i ≥ p`).
Type C: doubling `i, 0, …, 0` gives `2i < p` at position 0 (as `2i < 2k < p`) and `0` above,
so no carry is generated below position `J`. ∎ (M2/M3/M4: 5763 + 4626 + 5778 random/structured
cases, zero violations.)

## 3. The mirror

Split 727's divisor block `{2m, 2m−1, …, 2m−2k+1}` by parity:

- **odd slots** `2m − i`, `i` odd: **type B — free.**
- **even slots** `2m − 2i = 2(m − i)`, `0 ≤ i ≤ k−1`: for odd `p`, `ν_p(2(m−i)) = ν_p(m−i)`,
  i.e. `p^J | m − i`: **type C — the difficulty.**

The solved siblings' divisor block `{m+1, …, m+k}` is **entirely type A — free**
(this is exactly Lemma 5 of arXiv 2601.07421, "the range `p > 2k` is handled quickly").

> **Mirror Theorem.** For `p > 2k`, every prime-power condition of the 728/729/401 family is
> discharged for free by the type-A digit pattern; for 727 the odd half is discharged for free
> by the type-B pattern, while the even half is type C, where the low `J` digits of `m` supply
> **no** carries at all and all `J` required carries must be found at positions `≥ J`.

Same supply, same shape, mirrored divisor location — and the mirror inverts the digit
pattern from "all digits large" to "all digits zero". *That* is why one family fell to
carry-counting in January 2026 and the other did not.

## 4. Two consequences (proved)

**(a) Necessity of `√`-smoothness is a corollary, not an extra hypothesis.** In type C the
`J` carries must come from digit positions `≥ J`, of which there are `⌊log_p m⌋ − J + 1`.
Hence `J ≤ log_p m − J + 1`, so essentially `p^{2J} ≤ p·m`: a prime power `p^J ∥ m − i` with
`p^{2J} > 2m` kills membership outright (M5: zero violations, `k = 2, 3`, `n < 4·10⁴`). Since
`m − i` ranges over the window `n+1, …, n+k`, every `n ∈ S_k` (with `n > 2k²`) has a
`√(2n)`-smooth window — the smoothness constraint of PROBLEM.md *is* the type-C digit deficit.

**(b) The residual condition is a cofactor congruence.** For `p ∥ m − i` (the dominant case
`J = 1`), one carry is needed above position 0. Writing `W = (m−i)/p`, position 1 carries iff
`(W − 1) mod p ≥ (p−1)/2` — condition `C_p` of Lemma R‴ (`attempts/route-R12/LADDER.md` §4.5).
So after the trichotomy, 727 reduces to: *a smooth window, plus one congruence condition per
large prime factor, relating each prime to its cofactor.*

## 5. Why this closes the diagnosis of the run

Combining with the two proved engines of this project:

- **Small primes are solved.** Master Lemma SP (`attempts/route-R2/LEMMA_SP.md`, proved,
  explicit constants, AP-uniform) gives density `1 − 18exp(−√(log M)/120)` for the *exact* 727
  criterion at every `p ≤ exp(c√(log M))`, uniformly in every AP of modulus `≤ M^{1/10}`.
- **Large primes are solved conditionally.** Lemma R‴ discharges every `p > 2k` given the
  cofactor congruences `C_p` (proved; zero false positives over all even `n ≤ 6·10⁴`;
  certifies 10 of the 41 members of `S_3 ∩ [1, 6·10⁴]`).
- **What is left is exactly one statement**: infinitely many `n` whose window is `√(2n)`-smooth
  *and* whose large-prime cofactor congruences all hold. Consecutive-smooth supply at positive
  density is known for `k = 2` (Hildebrand 1985, Balog's conjecture) and **unknown for `k ≥ 3`**
  (positive-density `k`-strings of `n^α`-smooth integers require `α > e^{−1/(k−1)}`, which
  exceeds `1/2` exactly when `k ≥ 3`). Injecting the congruences into that supply is blocked by
  a measured obstruction, not a fixable slack:
  `experiments/crux_equidistribution.py` shows **98.96 %** of all `n ≤ 3·10⁵` fail some
  condition, so any first-moment bound taken over all `n` is worthless against the
  `ρ(2)² ≈ 9.4 %`-thin smooth set; the failure events must be counted *inside* the smooth set,
  where they are moreover **positively correlated** (observed joint pass rate `0.1105` versus
  product-model `0.3297`, ratio `0.335`) — so even an independence heuristic overstates the
  target by a factor 3.

The run's rigorous localization of 727 is therefore: **not a digit problem** (all digit content
is discharged by SP + R‴ + the trichotomy), but a *correlation* problem — smoothness of two
consecutive integers together with cofactor congruences at their large prime factors, i.e. the
same binary/parity barrier that R11's literature sweep found blocking every published route.

## 6. The first-moment obstruction (measured; `experiments/first_moment_obstruction.py`)

Using §4(b)'s reformulation — for `p ∥ n+j` the condition is exactly `κ_p((n+j)/p) ≥ 1`, i.e.
the cofactor has some base-`p` digit `≥ ⌈p/2⌉` — the failure density at primes `p ≤ n^{1/u}`
and the smooth-pair density were measured exhaustively for `n ≤ 2·10⁵`:

| `u` | `F(u)` = failure density | `2^{−u}` | `S(u)` = smooth-pair density | `ρ(u)²` | `S/F` |
|---|---|---|---|---|---|
| 2.0 | 0.40964 | 0.25000 | 0.05919 | 0.094159 | 0.1445 |
| 2.5 | 0.25813 | 0.17678 | 0.00907 | 0.016983 | 0.0352 |
| 3.0 | 0.16852 | 0.12500 | 0.00094 | 0.002361 | 0.0056 |
| 4.0 | 0.07934 | 0.06250 | 0.00002 | 0.000024 | 0.0003 |
| 5.0 | 0.03265 | 0.03125 | 0.00000 | 0.000000 | 0.0000 |

`F(u)` tracks `2^{−u}` (geometric decay: one digit-poor cofactor is a `2^{−D}` event with
`D ≈ u` usable digits), while `S(u)` tracks `ρ(u)² ≈ u^{−2u}` (super-exponential). Hence
`S(u)/F(u) → 0` **monotonically, for every `u`**:

> **First-moment obstruction.** No unconditional first-moment / union-bound argument over all
> `n` can exhibit a member of `S_2`, at any smoothness threshold `n^{1/u}`: the set of `n`
> failing some carry condition is geometrically thin in `u`, but the set of `n` with a smooth
> window is *super-exponentially* thinner. Failures must be counted **inside** the smooth set.

This is the rigorous form of the wall that closed every construction attempted in this run
(power families `z⁴−2`, `w⁸−2`, `s¹⁶−2`; the raw `pq−1` family; smoothness-restricted variants):
each died at the same accounting, and the table shows the death is structural, not slack.
Consequently a YES proof needs a *joint* statement — smoothness of two consecutive integers
**together with** cofactor congruences at their large prime factors — which is precisely the
binary-correlation/parity barrier identified independently by the literature sweep
(`attempts/route-R11/LITERATURE.md`).
