# ROUTES.md — route registry (Erdős 727)

Format: id | mathematical family | status | key lemma targets / outcome
Last updated 2026-07-28 ~10:50 UTC. See NOTES.md (newest first) and MIRROR.md for the
consolidated structural picture.

## Proved and audited-pending engines (the run's positive results)

- **R2 | Master Lemma SP — small-prime carry machinery** | PROVED, audit in progress |
  `attempts/route-R2/LEMMA_SP.md`. For fixed k, density `1 − 18exp(−√(log M)/120)` of
  m ∈ [M,2M], uniformly in every AP of modulus ≤ M^{1/10}, satisfies the exact 727 criterion
  at every p ≤ exp(c√(log M)), with spike bounds and per-prime surplus. Explicit constants;
  40/40 numerical checks. Barrier documented: cannot reach p > exp(c√log M).
- **R12 | Lemma R_k / Lemma R‴ — large-prime membership engine** | PROVED, audit in progress |
  `attempts/route-R12/LADDER.md`. R‴: small-prime demands + squarefree rough parts +
  cofactor congruence C_ℓ at every large prime ⟹ n ∈ S_k. Zero false positives on all even
  n ≤ 6·10⁴; certifies 10/41 of S_3 ∩ [1,6·10⁴]. Subsumes Lemma R_k (prime-box form).
- **R3 | Balakran dissection** | COMPLETE | `attempts/route-R3/FAMILY.md`: explicit infinite
  family F = {pq−1 : (3q+1)/2 ≤ p ≤ 2q−1} ⊆ S_1, elementary proof + Nagura; re-derives
  Balakran. `BREAKAGE.md`: exact k=2 failure taxonomy, Lemma Q, Lemma R. Independently
  reproduced by a second agent run.
- **MIRROR | structural theorem** | PROVED (M1–M5 verified) | `MIRROR.md`: digit trichotomy
  A/B/C explaining why the Jan-2026 carry-engineering closed 728/729/401 but not 727;
  √-smoothness derived as a corollary; residual content = cofactor congruences; measured
  first-moment obstruction (S/F → 0 for every u).

## Blocked routes (with diagnosis)

- **R1 | algebraic power families (z⁴−2, w⁸−2, s¹⁶−2)** | BLOCKED: Lemma Q + first-moment
  obstruction | squares double valuations past digit supply; budgets never close; the
  measured obstruction (MIRROR §6) shows the failure is structural, not slack.
- **R12-B | Statement B (four primes, pq+1 = 2rs in ratio boxes)** | BLOCKED: beyond current
  technology | R11 verdict: stacks balanced-E₂ (every published detector emits only unbalanced
  E₂ — which 727 membership forbids) with double specified parity (open even for Chen's 2p+1
  branch); the equation literature has no lower bounds ("parity-squared").
- **R5 | data mining** | COMPLETE (no proof path) | exact S_k on [1,10⁸) for k=2..6
  (|S_2| = 1,364,676 … |S_6| = 63); densities slowly increasing for every k; NO forbidden
  congruence classes; x²−2 family not enriched; no exploitable pattern found.
- **R8 | classical toolbox verification** | COMPLETE | `attempts/route-R8/TOOLBOX.md`: T1–T8
  with exact citations; corrections logged (Dickman form of T7 valid only on β ∈ [1/2,1];
  T5 uniform only at sieve-axiom level; T6 constant 3/(2π)).
- **R11 | Statement-B literature** | COMPLETE | `attempts/route-R11/LITERATURE.md`, 8 items.
  Key find: Hildebrand 1985 (Balog's conjecture) gives consecutive smooth pairs at positive
  density — so the k=2 supply is known and the residual is purely the congruence injection.

## Active / open routes

- **R13 | injectability anatomy (Hildebrand 1985, Balog–Ruzsa, Heath-Brown 1987)** | ACTIVE |
  can the positive-density consecutive-smooth machinery carry an AP restriction and the
  cofactor congruences C_ℓ? This is the gating question for the k=2 named variant.
- **R10 | general-k headline constructions (Balog–Wooley injection)** | ACTIVE |
  for k ≥ 3 even the SUPPLY is open: positive-density k-strings of n^α-smooth integers need
  α > e^{−1/(k−1)}, which exceeds 1/2 exactly when k ≥ 3; only thin BW-strings exist there.
- **R7 | NO-branch obstruction hunting** | ACTIVE (data-disfavored) | S_k nonempty and
  slowly densifying for all k ≤ 6 up to 10⁸; no congruence or prime-power obstruction found.
  Kept alive per protocol; no finiteness mechanism identified.
- **R9 | per-prime digit dynamics** | ACTIVE | largely absorbed into MIRROR + Lemma SP.

## Status of the problem

Neither branch is resolved. The run's rigorous localization: all digit/carry content is
discharged (SP + R‴ + trichotomy); what remains is a *joint* arithmetic statement —
smoothness of consecutive integers together with cofactor congruences at their large prime
factors — which sits behind the binary-correlation/parity barrier for k = 2, and behind an
additionally open smooth-supply problem for k ≥ 3.
