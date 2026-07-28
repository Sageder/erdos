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

## Where the problem actually sits

After the above, all digit/carry content of 727 is discharged. What remains is a single
**joint** arithmetic statement:

> infinitely many `n` whose window `n+1,…,n+k` is `√(2n)`-smooth **and** whose large prime
> factors all satisfy the cofactor congruence of Lemma R‴.

- For **k = 2** the smooth supply alone is a *known theorem*. Verified directly from the paper
  (`attempts/route-R13/papers/hildebrand1985_balog.txt`): Hildebrand's Theorem states that
  `d(A) > 0` implies `d(A_N ∩ (A_N + 1)) > 0` for all large `N`, where `A_N` is the
  dilation-closure of `A`; for a set that is `k`-stable for every `k` (Balog's hypothesis)
  `A_N ⊆ A` up to density zero, giving `d(A ∩ (A+1)) > 0`. The smooth set
  `A = {n : P(n) ≤ n^{1/u}}` is `k`-stable for every `k` — `kA ⊆ A` is immediate, and
  `k^{-1}(A ∩ kℕ) ⊆ A` fails only on `{n : P(n) ∈ (n^{1/u}, k^{1/u} n^{1/u}]}`, a set of density
  zero since the exponent window shrinks to a point — and has density `ρ(u) > 0`. Hence there is
  **positive density** of `n` with `n` and `n+1` both `n^{1/u}`-smooth, which is exactly the
  k = 2 window supply.
  *Correction to an earlier second-hand characterisation in this run:* the stronger "both largest
  prime factors in a prescribed band `(n^a, n^b)` for any `0 ≤ a < b ≤ 1`" form was attributed to
  this paper by the literature sweep; the paper's own stated consequence is the large-prime-factor
  case (`P(n), P(n+1) > n^{1-ε}`). Only the smooth-set instance is used above, and it is verified.
  By result 6 the congruences cannot be stripped off by an unconditional first moment, so they
  must be counted *inside* the smooth set — and there they are positively correlated
  (measured joint pass rate 0.1105 against 0.3297 for an independence model). This injection
  is the whole of the k = 2 variant.
- For **k ≥ 3** the supply itself is open: positive-density `k`-strings of `n^α`-smooth
  integers are known only for `α > e^{−1/(k−1)}`, which exceeds `1/2` exactly when `k ≥ 3`;
  only Balog–Wooley's thin strings exist below that.
- The clean prime-parametrized target (`Statement B`: infinitely many prime quadruples with
  `pq + 1 = 2rs` in explicit ratio boxes) was shown by literature sweep to be **beyond current
  technology**: it stacks balanced-`E₂` structure — which every published detector fails to
  produce, per GGPY (1.24), and which 727 membership *forces* — against double specified
  parity, open even in Chen's single-form `2p+1` branch. Under the run's own insufficiency
  list this reduction does not count as progress toward a resolution, and it is not claimed as
  such.

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
