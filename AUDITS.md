# AUDITS.md — adversarial audit reports (Erdős 727)

No candidate arguments yet. Every candidate proof gets a written audit here by a fresh
adversarial pass (subagent given only PROBLEM.md + the draft) BEFORE being believed, using the
12-item checklist of PROMPT §7. Verdict first.

---

## Audit 1 — Master Lemma SP (`attempts/route-R2/LEMMA_SP.md`), 2026-07-28

**VERDICT: PASS with cosmetic repairs.** Fresh adversarial auditor, given only PROBLEM.md +
the target; wrote 8 independent verification scripts (`audit_sp_1..8.py`). Every mathematical
statement — SP.0, SP.K, SP.1–SP.9, Master Lemma parts (1)(2)(3), Corollaries SP-A/B/C — is
**correct as stated**; every identity re-derived from scratch, every constant re-derived by
hand, counterexample hunts exhaustive and by exact sampling. **No fatal error, no false
theorem.** Repairs are confined to prose/illustrative text (Section 6 hypothesis bookkeeping,
Remark 7.2, Section 8 commentary, description of the numerical certificate); none touches a
proof. Full report: `attempts/route-R2/AUDIT_SP.md`. Four repairs listed and applied
2026-07-28 (appended to `LEMMA_SP.md`):
- **R1.** "`t ≥ 3` ⟺ `√L ≥ 80`" in the SP-A hypothesis check is wrong; the correct threshold
  is 60. Both are over-satisfied downstream, so nothing changes.
- **R2.** "the forced demand at `p = 2` is `≥ 11 + ν₂((2k)!)`" is FALSE as written: for
  `k = 3`, `q₀ = 2¹⁰`, `M = 10⁶` the true minimum is `W₂ = 14`, not `≥ 15`, and `W₂ < 15` for
  489 of 977 elements. Correct sufficient form: `W₂(m) ≥ ν₂(2m) = 1 + ν₂(m) ≥ 11`. The
  conclusion drawn was reproduced exactly.
- **R3.** "`κ₂(m) = s₂(m) ≈ 10`" overstates the supply (mean 5.885, max 10 in that AP);
  restated as `≤ 10, mean ≈ 5.9`, which strengthens the point.
- **R4.** The T13 verification row was mislabelled: `M = 2⁶⁴, 2²⁰⁰, 10⁶⁰` do **not** meet the
  lemma's own (H4) (which needs `M ≳ 10⁶⁶⁸` there); T13 tests the deterministic chain gated on
  SP.9's conclusion. The auditor closed the gap by re-running end-to-end at genuinely compliant
  scales (`2⁶⁰⁰ … 251¹⁰⁴⁰`, 181–2496 decimal digits) with zero violations.
Auditor's M5, recorded because it bears on the route: AP-uniformity does **not** by itself
deliver the intended intersection, since "window all `√(2n)`-smooth" is not a union of APs.

**Scope warning recorded by the auditor (binding on all downstream use):** Lemma SP proves
NOTHING about problem 727. It is a density-1 statement for the criterion at primes
`p ≤ exp(√(log M)/6)` only; the regime `p ∈ (exp(c√log M), n+k]` — including the smooth-window
constraint — is entirely untouched. The header "proved in full" is true of the *lemma* and must
never be quoted as a status for the route or for the problem.

## Audit 2 — Ladder lemmas (`attempts/route-R12/LADDER.md` §§1, 2, 3, 4.5), 2026-07-28

**VERDICT: PASS with repairs (R1–R3, all applied 2026-07-28).** Fresh adversarial auditor,
13 independent scripts, no route-R12 code imported. Sections 1, 2, 3, 4.5 are mathematically
correct as *sufficient-condition* statements about the literal object `((n+k)!)² | (2n)!`;
quantifier order correct; every prime range covered; the 2k-deficit correctly absorbed; no
circularity. **Zero false positives** in every brute-force test (Lemma R_k to n = 2·10⁶;
Lemma R‴ to n = 10⁶, k = 2..6). All PROBLEM.md calibration data reproduced exactly.

Repairs required and applied:
- **R1.** The threshold `n > (2k)⁴` in Lemma R_k was justified falsely (`c_j`, the pinned
  P₀-smooth part, is unbounded in k; counterexample class k=2, P₀=4, ν₂=10, ν₃=5 gives
  c₂ = 248832 needing n ≳ 7.7·10²¹). Restated as `n > 2·(max_j c_j)⁴`. Not fatal — the
  needed inequality was separately a hypothesis.
- **R2.** `B_k` was under-specified: as printed, `B_k ⟹ S_k infinite` did not follow, because
  the residue condition `(c_j r_j mod s_j) ≥ (s_j+1)/2` — the entire content of the position-1
  carry at `s_j` — lived only in the proof. Conditions (α) r_j ≠ s_j, (β) r_j, s_j > max(P₀,c_j),
  (γ) ratio box + residue condition are now inlined; the ambiguous "the (any) admissible class"
  is fixed to an explicit ∃-class.
- **R3.** §6 applied R‴ with k=3, P₀=5, violating the stated `P₀ ≥ 2k`. Substantively harmless
  (no prime in (5,6]) but the hypothesis is load-bearing: with a genuinely too-small P₀
  (k=3, P₀=4) the predicate **does** produce false positives. Hypothesis restated in the form
  the proof uses: every prime ℓ > P₀ satisfies ℓ > 2k (equivalently P₀ ≥ 2k−1).

**Standing caveat recorded by the auditor:** LADDER.md does not resolve 727 or the named k=2
variant; it is a reduction to `B_k`, an unproved prime-equation statement of comparable
strength, which under PROBLEM.md's insufficiency list does not count as progress toward a
resolution. The document states this itself. The value claimed — full elementary discharge of
the digit/carry side — is real and verified.


## Audit 3 — injectability anatomy (route R13), 2026-07-28

Not an audit of a proof but of a *strategy*, and it overturned two claims this run had been
repeating. Recorded here because both corrections are load-bearing.

1. **The residual target as this run had stated it was FALSE.** "Positive density with the
   cofactor congruence `C_ℓ` at every large prime" has density `≍ (log x)^{−1/2}`, since `C_ℓ`
   pins the carry to digit position 1 (a ~1/2 event) across `~log log x` primes. Independently
   re-verified here (`experiments/verify_L0_rescope.py`): among `n^{1/2}`-smooth pairs the
   all-`C_ℓ` fraction decays 0.0119 → 0.0110 → 0.0107 while the **exact** criterion holds at a
   stable 0.1029 → 0.1089 → 0.1058; at `b = 0.35` the exact criterion rises to 0.18–0.24 while
   all-`C_ℓ` falls to 0.004. The target is restated with the exact criterion and `b` free.
2. **The supply threshold was mis-instantiated.** Hildebrand's `k`-string hypothesis is on the
   *density* (`d(A) > (k−2)/(k−1)`), which for `k = 2` is simply `d(A) > 0`; hence for every
   `b > 0` there is positive lower density of consecutive `n^b`-smooth pairs. The earlier
   "`α > e^{−1/(k−1)} = 0.368` for `k = 2`" line was wrong and has been corrected in `LADDER.md`.
3. **Definitive negative on the injection question posed to this route:** `p`-stability, the
   sole hypothesis of the whole Hildebrand/Balog–Ruzsa/Heath-Brown family, is *maximally*
   violated by the carry conditions — dilation permutes a cofactor residue condition; measured
   agreement between the condition at `n` and at `2n` is 0.5037 where stability requires 1. No
   lemma in that family can be strengthened to carry them.
4. **New lead route identified** (papers absent from the earlier sweep): Tao–Teräväinen
   arXiv:2512.01739 and Teräväinen 2018 give the congruence restriction *free* in the published
   statements, making L1 (congruence-restricted consecutive smooth pairs) hard-but-classical.
   The residual wall L4 is joint cofactor equidistribution, with all moduli `≪ x^{1/2}`, i.e.
   inside BV range — **not** a parity or bilinear-prime problem, because no prime is detected
   and the smooth supply is unconditional. L4a (single largest prime factor) is the concrete
   first target.
## Audit 4 — route R14 `L4A.md` (L4a, Prop O1, Theorems A/B, Hypothesis U), 2026-07-28

**VERDICT: MIXED.** The unconditional core survives; one conditional theorem is broken; the
framing overstated the reduction; and the reduction does not count as progress.

**Survives (verified by the auditor from scratch, zero counterexamples):** Lemmas 1, 2, 2′, 3,
3′, 4, 5 — 720,406 exhaustive Lemma-2 instances, 756,666 for Lemma 2′, 120,000 random large
instances, exact Lemma-3 residue counts (including the `e ≥ 2` bound by brute force), a grid
check of Lemma 3′, and 46,297 members of the class `157 mod 648`. All tables reproduced to the
exact integer from an independent sieve; the eight claimed `S₂` members re-certified by Legendre
valuations at every prime `≤ 2n`.

**Broken / not proved:**
- **Proposition O1 is NOT proved** and was falsely listed as unconditional: §7 supplies only a
  Dickman-model asymptotic plus measurements, and the model step `S(x,b) ≍ x·ρ(1/b)²` is itself
  an unproved independence heuristic. The measurements are correct (auditor reproduced
  `A/S = 1.40, 2.55, 5.98, 9.17` and the raw counts exactly); the Proposition is not.
- **Theorem A is fatally broken:** Hypothesis U is applied to an `ℓ`-dependent family
  (right-hand side normalised by `#{n : ℓ ∥ n+1, P(n+1) = ℓ}`), which U does not cover — and the
  `P(n+1) = ℓ` constraint is load-bearing, since only it makes the sum over `ℓ` telescope. With
  what U legitimately gives, the bound costs `E[#{ℓ > 4 : ℓ ∥ n+1}]` ≈ 2.65/2.77/2.49/1.94 at
  `b = .5/.4/.3/.25`, yielding `≈ 1.3·#S(x)` — worse than trivial. Not repairable by raising `J₀`
  (that forces `J₀ ≍ log log x`, hence `b → 0` with `x`).
- **Hypothesis U at `θ = 1` is FALSE** for every `C` and `b` (explicit construction: take `ℓ` the
  largest prime `≤ x^{1/m}`, `m = ⌈1/b⌉`, `J = m−1`, so `ℓ^J ≈ x/ℓ` exhausts the cofactor range).
  `θ < 1` strictly is forced.
- **Theorem B's derivation is sound** — quantifier order, `R` never depending on `n`, coverage of
  `p = 2, 3` and all `ℓ ≥ 5` including prime powers and the boundary `ℓ ≈ x^b`, and the
  summation interchange all check out — but it inherits the false `θ = 1` column.

**Framing overstatement:** "any `θ > 0` and any `C` suffice because `b` is free" hides that the
binding constraint is the *ratio* `θ/b ≥ 62.8`, i.e. moduli `q ≥ y^{62.8}` (`y = x^b`) versus
`y^{6.59}` known for a single smooth number; and Soundararajan's range condition at `u = 1/b ≈ 63`
caps `y ≲ 2·10⁷`, so that theorem cannot be invoked as `x → ∞`. Highest-value repair identified:
sharpening Lemma 3′ at prime powers `a ≥ 2` would drop the requirement from `y^{63}` to `y^{7.3}`,
right at the edge of the known range — the crude prime-power step is the single reason the route
asks for `y^{63}`.

**Judgement on Hypothesis U (the question this audit was asked to settle).** Logically weaker
than 727(k=2) in form — an upper bound only, with an arbitrary constant, no asymptotic, no
converse, and with all digit/carry combinatorics stripped out. But: no case is known for pairs
above `(log x)^c`; no standard conjecture (GRH, EH, ABC) implies it; the operative parameters are
far more extreme than advertised; and it is precisely the conjunction of two items PROBLEM.md
excludes **by name** — "smooth-neighbor conjectures" and "digit equidistribution along sparse
families". **DECISION: Hypothesis U counts as a reduction to an unproved statement of comparable
strength, and is NOT progress on 727 under the stated rules.**
