# VERDICT.md — Erdős problem 727, autonomous run of 2026-07-27/28

## Answer

**The problem is NOT resolved by this run.** Neither branch was proved:

- YES branch (∀k ≥ 2, S_k infinite): not proved.
- NO branch (∃k₀ ≥ 2 with S_{k₀} finite): not proved (and strongly disfavoured by data —
  S_k is nonempty with slowly *increasing* density for every k ≤ 6 up to 10⁸).

The named `erdos_727.variants.k_2` (k = 2 alone) is likewise **not** resolved.

Per the run protocol this is stated plainly and nothing below is presented as a resolution.
The remainder records what *was* established rigorously, and exactly where the problem sits.

## Pre-flight (mandatory gate)

Performed before any mathematics: the erdosproblems.com forum threads are bot-blocked (403 —
the operator's manual browser check was the launch gate); the AI-contributions wiki (data
through 2026-06-30) contains **no** mention of 727; `teorth/erdosproblems/data/problems.yaml`,
fetched fresh, lists 727 as `open` (728 as `proved`, consistent with the known Aristotle
result). No proof claim was encountered anywhere. The run proceeded legitimately.

## Established, audited results

All four survived a fresh adversarial audit by an agent given only the problem statement and
the target document, each of which wrote its own independent verification scripts
(21 scripts total; see `AUDITS.md`).

1. **Criterion normal forms** (`experiments/verify_identities.py`, I1–I8 all PASS).
   `n ∈ S_k` ⟺ `∀p: 2s_p(n+k) − s_p(2n) ≥ 2k` ⟺ `∀p: κ_p(n) ≥ 2Σ_j ν_p(n+j)` ⟺
   `∏_{i<2k}(2m−i) | C(2m,m)` with `m = n+k`. Calibration gate reproduces the sanity table
   exactly (S₂ starts 208; |S₂ ∩ [1,2·10⁵]| = 1981; S₄ ∩ [1,6·10⁴] = {8174, 51984}).

2. **The Mirror Theorem** (`MIRROR.md`, `experiments/mirror_theorem.py`, M1–M5 all PASS).
   In the `m`-variable, 727 and the solved siblings 728/729/401 are the *same* question —
   "does a product of consecutive integers divide `C(2m,m)`?" — with the *same* supply
   `κ_p(m)`. A digit trichotomy for `p > 2k` decides both: type A (`m ≡ −i`) and type B
   (`2m ≡ odd`) give the required carries **free**; type C (`m ≡ +i`) gives **zero** low
   carries. The siblings' divisor block is entirely type A; 727's splits into type B (free)
   and type C (the difficulty). This is a precise structural explanation of why the
   January-2026 carry-engineering closed those problems and not this one.
   Corollary (proved, not assumed): the `√(2n)`-smoothness of the window `n+1,…,n+k` *is*
   the type-C carry-room inequality `p^{2J} ≲ 2m`.

3. **The cofactor engine** (Lemma R‴, `attempts/route-R12/LADDER.md` §4.5; audit PASS with
   repairs R1–R3 applied). Membership follows from: the small-prime demands at `ℓ ≤ P₀`, plus,
   at every larger prime `ℓ ∥ n+j`, the single congruence `((n+j)/ℓ − 1) mod ℓ ≥ (ℓ−1)/2`.
   Zero false positives over all even `n ≤ 6·10⁴` (audit: to `n = 10⁶`, `k = 2..6`); certifies
   45 of the 263 even members of `S₂ ∩ [1,6·10⁴]` and 10 of the 41 members of `S₃`, including
   the least member 3475. Hypothesis on `P₀` shown load-bearing by the audit.

4. **Master Lemma SP** (`attempts/route-R2/LEMMA_SP.md`; audit PASS, cosmetic repairs only).
   For fixed `k`, all but `18exp(−√(log M)/120)` of `m ∈ [M,2M]` — uniformly in *every*
   arithmetic progression of modulus `≤ M^{1/10}` — satisfy the exact 727 criterion at every
   prime `p ≤ exp(c√(log M))`, with spike bounds and a per-prime surplus. Explicit constants
   throughout. **Scope warning (auditor's, binding):** this proves nothing about 727 itself;
   the regime `p > exp(c√log M)` is untouched, and that barrier is intrinsic to the method.

5. **Balakran re-derived constructively** (`attempts/route-R3/FAMILY.md`): the explicit family
   `F = {pq−1 : p, q prime, (3q+1)/2 ≤ p ≤ 2q−1}` lies in `S₁`, with an elementary two-carry
   proof and infinitude by Nagura. Independently reproduced by a second agent.

6. **The first-moment obstruction** — PROVED (`DRAFT.tex` Prop. 5.1; `MIRROR.md` §6;
   `experiments/first_moment_obstruction.py`). Failure density `F(u) ≥ c·2^{−u}/u`
   (digit-poor-cofactor counting + Mertens + Bonferroni) against smooth density
   `S(u) ≤ ρ(u) = u^{−u(1+o(1))}` (Dickman–de Bruijn), so `S(u)/F(u) → 0`. **No unconditional
   first-moment or union-bound argument over all `n` can produce a member of `S₂`, at any
   smoothness threshold.** Measured with the *exact* failure condition
   `κ_p(n) < 2ν_p(n+j)`: `S/F` = 0.128, 0.028, 0.004, 0.0001, ≈0 at u = 2, 2.5, 3, 4, 5;
   already at u = 2 one has `F(u) = 0.464 > ρ(u) = 0.307 ≥ S(u)`, so the obstruction is
   decisive at every measured threshold and not merely asymptotically. (An earlier version of
   this experiment used the proxy `κ_p(W) = 0`; the exact condition makes the obstruction
   strictly stronger.) This is the rigorous form of the wall that killed every construction
   attempted here, and it explains those deaths structurally rather than as slack.

7. **Computational corpus** (`attempts/route-R5/`): exact `S_k` on `[1,10⁸)` for `k = 2..6`
   (|S₂| = 1,364,676; |S₃| = 139,975; |S₄| = 13,188; |S₅| = 1,012; |S₆| = 63; min S₆ = 3,648,835),
   with per-decade densities slowly increasing for every `k`, **no** forbidden congruence
   classes, and no exploitable algebraic pattern (the `x²−2` family is *not* enriched).

## Where the problem actually sits (re-scoped 2026-07-28 after route R13)

**Correction to an earlier statement in this file.** A previous version of this section named
the residual target as "infinitely many `n` with a smooth window **and** the cofactor congruence
`C_ℓ` at every large prime". *That statement is false*: `C_ℓ` demands the carry at digit
position 1 specifically, a ~1/2 event per prime, so over the ~`log log x` large prime factors
its density decays like `∏_{ℓ>P₀}(1−1/(2ℓ)) ≍ (log x)^{−1/2}`. Verified independently
(`experiments/verify_L0_rescope.py`): among `n^{1/2}`-smooth pairs the all-`C_ℓ` fraction falls
(0.0119 → 0.0110 across `[10⁵,4·10⁵)` → `[4·10⁵,8·10⁵)`), while the **exact** criterion holds
for a stable positive proportion (0.1029 → 0.1089). `C_ℓ` is sufficient, never necessary —
carries at higher digit positions count too (LADDER §4.5 remark (iii)).

**The correct residual statement** is therefore, for fixed `k` and any `b > 0`:

> infinitely many `n` whose window `n+1,…,n+k` is `n^b`-smooth and which satisfy the *exact*
> criterion `κ_ℓ(n) ≥ 2ν_ℓ(n+j)` at every prime `ℓ > P₀` dividing the window.

with the failure probability per prime `≲ 2^{−1/b}`, so that `b` is a genuine free knob.

**k = 2.** The supply is a theorem, and stronger than this run first recorded: Hildebrand's
`k`-string threshold is on the *density* (`d(A) > (k−2)/(k−1)`, which is `> 0` for `k = 2`), so
for **every** `b > 0` there is positive lower density of `n` with `n+1, n+2` both `n^b`-smooth
(apply Hildebrand's Cor. 2 to the stable set `{P(m) ≤ m^b}`; the earlier "`e^{−1/(k−1)} = 0.368`"
line was a mis-instantiation of that threshold and has been corrected in `LADDER.md`).
The decomposition of what remains:
- **L1** (congruence-restricted smooth pairs, `#{n ≤ x : n ≡ c₀ (Q₀), n+1, n+2 both n^b-smooth}
  ≫_b x/Q₀`): *hard-but-classical, essentially available* — the AP restriction `1_{n≡b (W)}`
  and the AP smooth-count input both appear already in Tao–Teräväinen, arXiv:2512.01739, Thm 3.1
  and the proof of Thm 1.8 (route R13 obtained both papers; neither was in the earlier sweep).
- **L2** (`ℓ ∥ n+j` for large `ℓ`) and **L3** (small-prime forcing, already proved and audited
  as Lemma R_k steps (i)–(ii)): *routine*.
- **L4** (**the wall**): joint cofactor/carry equidistribution — for a positive proportion of the
  `n` from L1, `κ_ℓ(n) ≥ 2` at *every* large prime factor simultaneously.
- **L4a** (the concrete first target): the single-prime version — a positive proportion of L1
  pairs satisfying the condition at the largest prime factor of `n+1` only. One AP condition to
  a single modulus `ℓ ≤ x^b`; assessed as within reach of existing machinery.

**This changes the character of the residual problem.** Route R13's decisive negative finding is
that the entire stable-set family (Hildebrand 85/89, Balog–Ruzsa, Heath-Brown) is a
non-constructive pigeonhole whose sole hypothesis — `p`-stability, i.e. invariance under
multiplicative dilation — is *maximally violated* by the carry conditions, which dilation
permutes: measured agreement between the condition at `n` and at `2n` is **0.5037**, where
stability requires 1. There is no lemma in that family whose strengthening would deliver the
conditions; the hypothesis itself is the obstruction, and closing under all dilations `≤ N`
loses `e^{−N}` in density against a tower-sized `N(ε)`. But because the smooth supply is
unconditional and no prime is being *detected*, L4 is **not** a parity problem and **not** a
bilinear-prime problem — the barrier identified earlier in this run (balanced-`E₂` versus parity,
the dispersion/Chen frontier) applies to the prime-parametrized `Statement B` route and **not**
to this one. L4 is equidistribution of cofactors `(n+j)/ℓ` modulo `ℓ`, with all moduli
`ℓ² ≤ x^{2b} ≪ x^{1/2}`, i.e. well inside Bombieri–Vinogradov range. What is open is that the
modulus is a function of `n`, that `~log log x` conditions must hold at once, and that the weight
is not multiplicative (so it is not an admissible `g₂` in Thm 3.1). This is a strictly softer
frontier than the one this run previously recorded.

**k ≥ 3.** Still blocked at the supply stage, but the gap is now explicit and small: three
consecutive `n^α`-smooth integers at positive density are known for `α > e^{−1/2} = 0.6065`
(Hildebrand 1989) and for `α > e^{−2/3} = 0.5134` (Tao–Teräväinen's short-interval-uniform
strengthening), while 727 needs `α = 1/2`. McNamara (arXiv:2312.08544) exhibits a stable set of
density exactly 1/2 with no 3-term string, matching Hildebrand's threshold and proving the
**soft/stable-set route cannot reach 1/2 at all**. The frontier is the interval 0.5134 → 0.5,
and it must be crossed by non-soft means.

**Statement B** (the prime-parametrized route: infinitely many prime quadruples with
`pq + 1 = 2rs` in explicit ratio boxes) remains beyond current technology for the reasons
recorded earlier — balanced-`E₂` structure, which every published detector fails to produce and
which 727 membership forces, stacked against double specified parity. It is superseded as the
lead route by the L1–L4 decomposition above, which needs no prime detection at all.

## Independent-verification plan

- **Reproduce:** `python3 experiments/calibrate.py` (gate), `verify_identities.py`,
  `mirror_theorem.py`, `crux_equidistribution.py`, `first_moment_obstruction.py`;
  audit scripts `attempts/route-R2/audit_sp_*.py`, `attempts/route-R12/audit_*.py`.
- **Lean sketch** (statements only; none of these is the headline):
  `theorem mirror_typeC (p k J : ℕ) (hp : 2*k < p) (i : ℕ) (hi : i ≤ k-1)
     (m : ℕ) (h : m % p^J = i) : lowCarries p J m = 0` and the engine
  `theorem engine (k P₀ n : ℕ) (h₀ : ∀ ℓ, ℓ.Prime → ℓ > P₀ → ℓ > 2*k) (hsmall …) (hlarge …) :
     (n+k)! ^ 2 ∣ (2*n)!`. The headline statement to target remains
  `∀ k ≥ 2, Set.Infinite {n | (n+k)! ^ 2 ∣ (2*n)!}` (google-deepmind/formal-conjectures,
  `ErdosProblems/727.lean`) — **unproved here**.
- **Before any external communication:** nothing in this run should be posted as a solution or
  partial solution of 727. The only externally interesting items are results 2 and 6, and they
  are statements *about the difficulty*, not about the truth, of the conjecture.

## Honest bottom line

The run produced a sharp structural localization of Erdős 727 — why it resisted the method
that felled its three siblings, why every first-moment construction must fail, and what single
joint statement remains — together with two proved, audited engines and a large verified
computational corpus. It did **not** resolve the problem, in either direction, for any `k ≥ 2`.
