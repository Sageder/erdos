# AUDIT_LADDER.md — adversarial audit of `attempts/route-R12/LADDER.md` §§1, 2, 3, 4.5

Auditor: fresh adversarial pass, 2026-07-28. Sources read: `PROBLEM.md` and `LADDER.md` only.
All identities re-derived from scratch; all numerical claims re-tested with independent scripts
written for this audit (`audit_core.py`, `audit_calib.py`, `audit_S2big.py`, `audit_Rppp.py`,
`audit_Rppp_big.py`, `audit_Rk.py`, `audit_gen_R2.py`, `audit_diag.py`, `audit_probe1.py`,
`audit_probe2.py`, `audit_probe3.py`, `audit_probe4.py`, `audit_final_scan.py`).
No route-R12 code was imported.

---

## VERDICT

**PASS with repairs.** No fatal error. Sections 1, 2, 3, 4.5 are mathematically correct as
*sufficient-condition* statements about the literal object `((n+k)!)^2 | (2n)!`; the quantifier
order is right; every prime range is covered; the `2k`-deficit is correctly absorbed by the
valuation form of the criterion; there is no circularity. **Zero false positives** in every
brute-force test I ran (up to `n = 2·10^6` for Lemma R_k, up to `n = 10^6` for Lemma R‴,
`k = 2..6`). Every numerical claim in §§2, 4.5, 6 that I could reproduce reproduced **exactly**.

Three defects require repair (R1–R3 below); none breaks the chain, but R1 and R2 mean the
implication `B_k ⟹ S_k infinite` is not literally proved by the text as printed.

**Standing caveat (not a defect, stated by the document itself):** LADDER.md does *not* resolve
727 or the named k = 2 variant. It is a reduction to `B_k`, an unproved prime-equation statement.
`B_k ⟹ S_k` infinite, but not conversely, and `B_k` is not known to be weaker than 727-YES — it
demands infinitely many `n` with `n+1` and `n+2` both balanced semiprimes in fixed classes,
which is strictly beyond current technology. Under `PROBLEM.md → "What does NOT count"` this is
a "reduction to an unproved statement of comparable strength"; §4 and §4.6 say so honestly. The
value claimed — full elementary discharge of the digit/carry side — is real and verified.

---

## 1. Independent re-derivation

### §1 criterion — CORRECT
`(n+k)! = n! · ∏_{j=1}^k (n+j)`, so `ν_ℓ((n+k)!) = ν_ℓ(n!) + Σ_j ν_ℓ(n+j)`. Kummer/Legendre give
`ν_ℓ((2n)!) − 2ν_ℓ(n!) = ν_ℓ(C(2n,n)) = c_ℓ(n)`. Hence
`ν_ℓ((2n)!) ≥ 2ν_ℓ((n+k)!) ⟺ c_ℓ(n) ≥ 2 Σ_j ν_ℓ(n+j)`. Primes not dividing the window have
demand 0, so restricting to `ℓ | (n+1)···(n+k)` is legitimate. Direction of the inequality is
correct; the `2k`-deficit that `PROBLEM.md` warns about is exactly what the term
`2 Σ_j ν_ℓ(n+j)` encodes, so §1 is *not* the naive central-binomial condition.

**Numerics.** For all `n < 3000` and `k = 1,2,3` I compared four independently coded predicates:
(a) direct `((n+k)!)^2 | (2n)!` via Legendre over every prime `≤ n+k`; (b) `PROBLEM.md`'s
`∀p: 2 s_p(n+k) − s_p(2n) ≥ 2k`; (c) §1's criterion; (d) the product form
`∏_{j=n−k+1}^{n+k} j | C(2n, n+k)` with exact `math.comb`. **0 mismatches.**
Calibration against `PROBLEM.md` sanity data — all exact:
`S_1` first 15 and `|S_1 ∩ [1,441]| = 40`; `S_2` first 20 (starting 208) and
`|S_2 ∩ [1,2·10^5]| = 1981`; `S_3` first 8 (starting 3475) and `|S_3 ∩ [1,6·10^4]| = 41`;
`S_4 ∩ [1,6·10^4] = {8174, 51984}`.

### §2 Lemma R_k — CORRECT (given its stated hypotheses)

*Digit expansion at `r = r_j`.* `n = c r s − j = (cs − 1)·r + (r − j)`. Verified. Validity of the
"exactly two digits" claim: low digit `r − j ∈ [0, r)` needs `1 ≤ j < r` ✓; high digit `cs − 1 < r`
is **exactly the box lower bound** `c_j s_j − 1 < r_j` ✓, and `cs − 1 ≥ 0` since `s` is prime.
Doubling: position 0 carries iff `2(r−j) ≥ r ⟺ r ≥ 2j`, true because `r > P₀ = 2k ≥ 2j` ✓.
Position 1 with carry-in 1: `2(cs−1) + 1 = 2cs − 1 ≥ r` is **exactly the box upper bound** ✓.

*Digit expansion at `s = s_j`.* `cr = As + b`, `n = A s² + (b−1)s + (s−j)`. Verified. Low digit
`s − j ∈ [0, s)` ✓; digit-1 `b − 1 ∈ [0, s−1)` needs `b ≠ 0`, which follows *immediately* from the
residue hypothesis `b ≥ (s+1)/2 > 0` (the document's argument via `s ∤ cr` is redundant but sound).
Position 0: `2(s−j) ≥ s ⟺ s ≥ 2j` ✓. Position 1: `2(b−1)+1 ≥ s ⟺ b ≥ (s+1)/2` ✓.
**Carry-in chain is sound**: carries propagate strictly upward, so digits at positions ≥ 2 (i.e.
the unknown expansion of `A`) cannot affect the carries out of positions 0 and 1. Correct.

*Class condition (ii).* A digit `d ≥ ⌈ℓ/2⌉` gives `2d + c_in ≥ 2d ≥ ℓ`, hence a carry out of that
position **irrespective of the carry-in** — the claim is right. The window `[D_ℓ, D_ℓ + 2V_ℓ]` has
`2V_ℓ + 1` positions, so `c_ℓ(n) ≥ 2V_ℓ + 1 > 2V_ℓ` ✓ (one carry more than needed).
*Consistency of (i) with (ii):* `ν_ℓ(n+j) = v` is determined by `n mod ℓ^{v+1}`, i.e. by digits
`0..max_j v_{ℓ,j} = D_ℓ − 1`; (ii) constrains only positions `≥ D_ℓ`. **Disjoint**, so the class
exists (choose `L_ℓ ≥ D_ℓ + 2V_ℓ + 1`, CRT across `ℓ ≤ P₀`). The existence argument (i)/(ii) is
valid. Note carefully that `j` may exceed `ℓ` (e.g. `ℓ=2, k=5, j=4`) — this does **not** break
disjointness, since the criterion for `ν_ℓ(n+j)` still only reads `n mod ℓ^{v+1}`.
**Numerics:** (ii) ⟹ `c_ℓ(n) ≥ 2V_ℓ` checked for `k = 2, 3, 5`, all `n ≤ 1.5·10^5`, all `ℓ ≤ 2k`:
**0 violations**.

*Prime coverage is complete.* `ℓ ≤ P₀`: (ii). `ℓ > P₀`: `ℓ` divides at most one window element
(else `ℓ | ` a difference `< k < ℓ`), and by hypothesis `(n+j)/c_j = r_j s_j` with `c_j` the *full*
`P₀`-smooth part, so the only primes `> P₀` dividing the window are the `r_j, s_j`, each exactly
to the first power (`r ∤ c` since `r > P₀`, `r ≠ s`), giving demand exactly 2. Cross-`j`
collisions (`r_j = r_{j'}`, `r_j = s_{j'}`) are impossible for `ℓ > 2k > k`. No gap.

*Cross-check against `PROBLEM.md`'s large-prime criterion (a trap I set and the lemma survives).*
The box forces `n+j ≤ r_j² < 2(n+j)` (verified on 3·10^5 random `(c,r,s)` triples), so `r_j` is
right at the `√`-boundary. `PROBLEM.md` says every prime `p > max(√(2n), 2k)` with a multiple in
`(n, n+k]` **fails** — and `r_j | n+j ∈ (n, n+k]`. No contradiction arises, because the box
*also* forces `r_j² ≤ 2n`: from `r ≤ 2cs − 1` we get `r² ≤ 2crs − r ≤ 2crs − 2j = 2n` (using
`r ≥ 2j`). So `r_j ≤ √(2n)` always and the large-prime regime is never entered. Confirmed on the
actual hits. This is the sharpest available consistency test and the lemma passes it.

### §3 ladder theorem — CORRECT modulo repairs R1/R2
`B_k` gives infinitely many `n ≡ c₀ (mod Q₀)` with the factorisation; all but finitely many exceed
the Lemma-R_k threshold; each such `n ∈ S_k`; hence `S_k` infinite. Quantifiers: `k` fixed first,
`(c₀, Q₀)` and the boxes depend on `k` alone and never on `n`, `n → ∞` inside, and the per-prime
condition is verified for **every** prime for each individual `n` (not prime-range-by-prime-range).
`(∀k ≥ 2: B_k) ⟹ 727-YES` follows. `B_2 ⟹` the named `k = 2` variant only — correctly stated.
**No circularity**: nothing downstream of `B_k` is used to establish any part of §§1–2, 4.5;
`B_k` is the sole unproved input and is labelled as such.
*Non-vacuity of the congruence side (checked):* `(n+j)/c_j ≡ (c₀+j)/c_j` is a **unit** mod
`Q₀/c_j`, precisely because (i) pins `ν_ℓ(n+j)` exactly. So `B_k`'s congruence constraints on
`r_j s_j` are not self-contradictory.

### §4.5 Lemma R‴ — CORRECT
`W = (n+j)/ℓ`, `n = (W−1)ℓ + (ℓ−j)`. Verified. Digit 0 `= ℓ − j ∈ [0, ℓ)` needs `ℓ > j`, supplied
by `ℓ > P₀ ≥ 2k ≥ 2j`; higher digits are those of `W − 1`, so digit 1 `= (W−1) mod ℓ` **regardless
of how large `W` is**. Position 0: `2(ℓ−j) ≥ ℓ ⟺ ℓ ≥ 2j` ✓. Position 1 with carry-in:
`2·((W−1) mod ℓ) + 1 ≥ ℓ ⟸ C_ℓ`, and `(ℓ−1)/2 ∈ ℤ` since `ℓ > 4` is odd ✓. `ℓ ∥ n+j` plus
"at most one window element" gives demand exactly 2 ✓. Coverage is complete: `ℓ ≤ P₀` → (a);
`ℓ > P₀` dividing the window → (b); `ℓ > P₀` not dividing the window → demand 0. **The carry chain
holds for every `j ≤ k` and every `ℓ > 2k`.** Correct.
*Remark (i) "subsumes Lemma R_k" — verified symbolically:* at `ℓ = r`, `(n+j)/r − 1 = cs − 1 < r`,
so `C_r ⟺ cs − 1 ≥ (r−1)/2 ⟺ r ≤ 2cs − 1` = the box upper bound; at `ℓ = s`,
`(cr − 1) mod s = b − 1`, so `C_s ⟺ b ≥ (s+1)/2` = the residue hypothesis. True.
`p = 2` is never in scope of (b) (`ℓ ≥ 5`) and is handled by (a); prime powers are excluded by
`ℓ ∥ n+j`; `n+j` prime is correctly rejected (`W = 1 ⟹ (W−1) mod ℓ = 0 < (ℓ−1)/2`), matching
`PROBLEM.md`'s fact that a prime in `(n, n+k]` always kills membership.

---

## 2. Numerical verification (all independently regenerated)

| claim in LADDER.md | my result | status |
|---|---|---|
| §4.5 R‴, 0 false positives on even `n ≤ 6·10^4` | 0 FP on **all** `n ≤ 6·10^4` (k=2,P₀=4) | ✅ stronger |
| §4.5 coverage `45/263` of even `S_2` members `≤ 6·10^4` | exactly `45/263` (and `107/534` overall) | ✅ exact |
| §6 R‴ k=3, P₀=5 certifies `10/41` of `S_3 ≤ 6·10^4`, incl. 3475, 0 FP | exactly `10/41`, incl. 3475, 0 FP | ✅ exact |
| §2 "18/18 regenerated solutions q ≤ 1500 in S₂" | exactly **18** candidates, **18** in `S_2` | ✅ exact (see M5) |
| §3 k=3: 0 structural hits below `4·10^5` | 0 full-Lemma-R_3 hits `≤ 2·10^6` | ✅ consistent |
| §6 B_3 box-form, 0 hits `≤ 3·10^7` | not reachable at my budget | ⚠ unchecked |

Extended false-positive hunt for **Lemma R‴**, all `n ≤ 10^6`, my own SPF sieve + exact integers:

```
k=2 P0=4 : certified=1751  FALSE POSITIVES=0
k=3 P0=6 : certified= 113  FALSE POSITIVES=0
k=4 P0=8 : certified=   6  FALSE POSITIVES=0
k=5 P0=10: certified=   0  FALSE POSITIVES=0
k=6 P0=12: certified=   0  FALSE POSITIVES=0
k=3 P0=4 : certified=  73  FALSE POSITIVES=3   [110287, 266912, 972037]   <-- P0 < 2k
```
The last line is a deliberate hypothesis-violation test and **it breaks**, confirming `P₀ ≥ 2k`
is load-bearing rather than decorative: at `n = 110287, k = 3`, `ℓ = 5 | n+3` and
`2(ℓ − j) = 4 < 5`, so there is no position-0 carry; `c_5(n) = 0 < 2 =` demand.

Extended false-positive hunt for the **full Lemma R_k** (hypotheses expressed pointwise,
*including* condition (ii)), all `n ≤ 2·10^6`:
`k=2, P₀=4`: 2 hits (`n = 239837, 1512186`), **0 false positives**; `k=3, P₀=6`: 0 hits.
Generative regeneration from prime pairs (`s ≤ 1500`, `n ≲ 4.5·10^6`): 2 hits
(`1512186, 2880636`), 0 false positives. Canonical `k=2` class (`c₁=1, c₂=2`, `n ≡ 0 mod 12`,
`4 | n`), `s ≤ 6000`, `n ≲ 7.2·10^7`: **242 candidates, all 242 in `S_2`, 0 failures.**

**Deliberate hypothesis-stripping test.** Dropping condition (ii) from Lemma R_k (keeping boxes +
residue conditions) over arbitrary classes produces genuine counterexamples:
`n = 26791` (`ℓ=3`: `c_3 = 3 < 4 =` demand) and `n = 124930`, `557770` (`ℓ=3`: `c_3 = 1 < 2`).
So the class conditions are not ornamental. **Lemma R_k, as stated, includes them.**

---

## 3. Defects requiring repair

**R1 (repair). The threshold `n > (2k)^4` in Lemma R_k is false as justified.**
The parenthetical claims this is "large enough that `s_j > c_j` is automatic". From the box,
`√((n+j)/2)/c_j < s_j ≤ √(n+j)/c_j`, so `s_j > c_j` needs roughly `n > 2 c_j^4`. But `c_j` is the
pinned `P₀`-smooth part of `n+j` — a free parameter of the class, **unbounded in `k`**. Explicit
counterexample class: `k = 2`, `P₀ = 4`, pin `ν_2(n+2) = 10`, `ν_3(n+2) = 5`; then
`c_2 = 2^10·3^5 = 248832` and `s_2 > c_2` requires `n ≳ 7.7·10^21`, versus `(2k)^4 = 256`.
*Why it is not fatal:* `s_j > max(P₀, c_j)` is separately listed as a **hypothesis** of the
`r_j, s_j` bullet, so the lemma itself remains true. *Repair:* delete the parenthetical and write
`n > 2·(max_j c_j)^4` (a constant of the class, hence of `k`) — or drop the threshold entirely and
rely on the stated hypothesis.

**R2 (repair). `B_k` is under-specified; as literally written, `B_k ⟹ S_k` infinite does not follow.**
`B_k` says only "`(n+j)/c_j = r_j s_j` with primes in the Lemma-R_k **boxes**". The word "boxes"
naturally reads as the archimedean ratio conditions `c_j s_j − 1 < r_j ≤ 2 c_j s_j − 1` alone. The
proof of Lemma R_k additionally needs, for every `j`:
(α) `r_j ≠ s_j`; (β) `r_j, s_j > max(P₀, c_j)`; (γ) `(c_j r_j mod s_j) ≥ (s_j + 1)/2`.
(γ) is the *entire* content of the position-1 carry at `s_j` — without it the lemma is simply
false. §3's later parenthetical does mention "+ the residue conditions", but the statement of
`B_k` must carry them. *Repair:* restate `B_k` with (α), (β), (γ) inline.
Secondary: "**For the (any) admissible class `(c₀, Q₀)`**" is ambiguous between `∀`-class and
`∃`-class. Only `∃` is needed (and only `∃` is plausible); as an `∀` statement `B_k` is
gratuitously stronger. Fix the quantifier explicitly.

**R3 (repair). §6 applies R‴ with `k = 3, P₀ = 5`, violating the stated hypothesis `P₀ ≥ 2k = 6`.**
Substantively harmless — there is no prime in `(5, 6]`, so every `ℓ > P₀` still satisfies
`ℓ ≥ 7 > 2k` — but the hypothesis is genuinely load-bearing (see the `k=3, P₀=4` false positives
above), so the mismatch must not be left standing. *Repair:* state the hypothesis in the form the
proof actually uses — "every prime `ℓ > P₀` satisfies `ℓ > 2k`", equivalently `P₀ ≥ 2k − 1`.

---

## 4. Minor issues (no logical impact)

- **M1.** Lemma R_k's proof contains an unedited editorial aside: `"[and n < r² iff cs ≤ r — wait:
  ...]"`. Delete; the correct statement is that `cs − 1 < r` forces `n < r²`, i.e. exactly two
  base-`r` digits.
- **M2.** The audit note "`r_j = s_j` must be excluded explicitly — the `c_j = 1` box does not
  exclude it" is over-cautious: the residue condition already excludes it, since `r = s` gives
  `c_j r_j mod s_j = c r mod r = 0 < (s+1)/2`. Harmless (the hypothesis is stated anyway).
  Likewise the proof's justification of `b ≠ 0` via `s ∤ cr` is redundant given `b ≥ (s+1)/2`.
- **M3.** R‴ remark (ii): "For `ℓ > √(2(n+k))`: `C_ℓ ⟺ W ≥ (ℓ+1)/2`" is *vacuously* true — above
  that threshold `W < ℓ/2`, so both sides are always false. The informative threshold is
  `ℓ > √(n+k)` (which is what makes `W < ℓ` and the reduction mod `ℓ` trivial); the useful
  conclusion, that `C_ℓ` forces `ℓ ≲ √(2(n+j))`, then follows. Restate.
- **M4 (substantive but non-fatal — recommend strengthening).** Condition (ii) is far more
  restrictive than the demand it buys: it forces `2V_ℓ + 1` carries where `2V_ℓ` suffice, and it
  ignores carries coming from anywhere else. Measured cost: in the canonical `k=2` class
  (`c₁=1, c₂=2, n ≡ 0 mod 12, 4 | n`) only **13 of 242** genuine box-solutions with `n ≲ 7.2·10^7`
  satisfy (ii) — yet **all 242** lie in `S_2`. Reason: in that class `c_2(n) = s_2(n) ≥ 2`
  automatically (`3 | n` keeps `n` off the powers of 2) and `V_3 = 0`, so demand (a) is free. So
  `B_2` as printed is ≈20× stronger than what the ladder actually needs. Replace (ii) by
  R‴'s (a) plus a cheap class-forceable substitute (e.g. `n ≡ 0 mod 12` for `k = 2`); this costs
  nothing and materially weakens the analytic target.
- **M5.** §2's "Verified: 18/18 regenerated solutions q ≤ 1500 in S₂" reproduces exactly — but I
  can only reproduce it by testing the boxes **without** condition (ii); only **1** of those 18
  satisfies (ii). The document should say which predicate was verified, otherwise the line reads
  as a verification of Lemma R_k as stated. (With (ii): 2 hits `≤ 2·10^6`, both in `S_2`.) Also
  "`q`" is never defined in LADDER.md — name the parameter.
- **M6.** §2 says `P₀ = 2k` "(any `P₀ ≥ 2k` works)"; worth recording which bound does which job:
  "`ℓ` divides at most one window element" only needs `ℓ > k − 1`, whereas the position-0 carry
  needs `ℓ ≥ 2j` for `j ≤ k`, i.e. `ℓ ≥ 2k`. Constants are otherwise explicit and uniform in `n`
  (they depend on `k` alone), which is what the quantifier order requires.
- **M7.** §6's smoothness thresholds arithmetically check out (`e^{−1} = 0.3679`,
  `e^{−1/2} = 0.6065`), but the attributions (Hildebrand 1985 pairs; BW98 strings) are asserted,
  not proved here. §§4, 4.6, 6 are context only and were not audited for literature accuracy.

---

## 5. Checklist verdicts

1. Statement is literally about `((n+k)!)^2 | (2n)!` — **YES**; §1 is a correctly derived
   equivalent (independently re-derived and machine-checked against 3 other forms).
2. Quantifier order (`k` first; one `n` beats every prime) — **CORRECT**; the class, `Q₀`, `P₀`
   and boxes depend on `k` alone, and every lemma verifies all primes for each fixed `n`.
3. Per-prime inequality direction and the `2k`-deficit — **CORRECT**; the deficit is absorbed
   exactly by the valuation form `2 Σ_j ν_ℓ(n+j)`.
4. All prime ranges covered incl. `p ~ √(2n)`, `p ≤ 2k`, `p = 2` — **YES**; and the box provably
   keeps `r_j ≤ √(2n)`, so the `p > √(2n)` failure regime of `PROBLEM.md` is never entered.
5. Constants explicit, uniformities tracked — **MOSTLY**; one wrong explicit constant (R1).
6. Every numerical claim re-checked with independent exact-integer scripts — **DONE**; all
   reproducible claims reproduced exactly; 0 false positives anywhere.
7. Circularity / unproved auxiliary infinitude — **NONE inside §§1–3, 4.5**; the entire analytic
   burden is isolated in `B_k`, openly unproved. The ladder therefore does not resolve 727.
8. Edge cases — small `n` (thresholds), prime powers (`ℓ ∥ n+j`), `r = s` (excluded twice over),
   AP-modulus interaction (CRT class is non-empty; `(n+j)/c_j` is a unit mod `Q₀/c_j`),
   digit-expansion validity (`cs − 1 < r`, `0 ≤ b−1 < s`, `0 ≤ ℓ−j < ℓ`) — **all checked, all OK**.
