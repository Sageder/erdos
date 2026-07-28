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
proof. Full report: `attempts/route-R2/AUDIT_SP.md`.

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
