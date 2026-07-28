# Route D — local obstruction hunt (NO branch). Final report.
(Transcribed by the session: the subagent's harness blocked it from writing report .md files.
All its scripts are `experiments/D_01…D_11`.)

## Bottom line
Route D did NOT prove NO, and **proved that the entire class of obstructions it was chartered to
find cannot prove NO**. That negative meta-result is the main deliverable, together with an
unconditional lcm lower bound and an independent re-derivation of the parity split.

## PROVED
- **D1 = our Lemma M3 (independent re-derivation).** E-covering ⟺ two DISJOINT S_0,S_1 ⊆ H each
  carrying a covering of ℤ; and lcm_E = 2·lcm_H exactly. Verified on 20000 random all-even
  families (5268 covering / 14732 not — non-vacuous both ways).
  *Reframing:* the solved p ≥ 3 variant (Selfridge) is exactly "H supports ONE covering"; 273 asks
  for a **second, disjoint** one built from the moduli the first did not use.
- **D2 arithmetic of E.** For every odd prime r, H omits the class (r−1)/2 mod r except m itself.
  Hence every n ∈ E is ≡ 0 or 4 (mod 6) — **E has no element ≡ 2 (mod 6)** — and every n ∈ E with
  3∤n satisfies n ≡ 10 (mod 12). Multiples of d have density 1/φ(d) in H, measured on
  H ∩ [2,2·10⁶] (283144 elements): d=3 → 0.4996, d=5 → 0.2500, d=9 → 0.1664, d=15 → 0.1250.
  **This REFUTES the prompt's suggestion that the arithmetic of E might obstruct**: the enrichment
  makes E *better* than a random set of its density at supplying moduli divisible by any d, and
  the residue restrictions are conditions on the *residue* of a modulus, invisible to covering
  arguments which depend only on the divisibility lattice.
- **D3 fiber lemma** (matches our derivation): for a covering, prime q, J ≥ max ν_q(n_i), every
  r ∈ ℤ/q^J has F_q(r) := Σ_{i : a_i ≡ r mod q^{ν_q(n_i)}} q^{ν_q(n_i)}/n_i ≥ 1, and the average of
  F_q over r is exactly Σ 1/n_i. Via D1 the requirement for 273 is **≥ 2**.
- **D4 multi-prime hierarchy Φ_Q**, with Φ_Q ≤ min_{q∈Q} Φ_q: prime PAIRS are strictly stronger
  than single primes. Implemented exactly in `D_08_phiQ.c`, cross-validated against `D_05_phi.c`
  and against the classical covering {2,3,4,6,12} (Φ₂ = Φ_{2,3} = 1 exactly).
- **D5 minimality.** In an irredundant covering, for every prime q the active q-adic nodes at each
  level form complete sibling groups; so q | lcm ⟹ at least q moduli are divisible by q.
- **D6 ★ THE DECISIVE NEGATIVE RESULT.** Any m ∈ S coprime to ∏Q contributes 1/m to EVERY cell for
  EVERY residue assignment, so Φ_Q(S) ≥ Σ_{m ∈ S, gcd(m,∏Q)=1} 1/m, and that sum diverges over H
  for every fixed finite Q (Mertens–Dirichlet). Explicit thresholds: A_Q(H ∩ [2,Y]) ≥ 2 first at
  **Y = 9944** for Q={3}, **Y = 82899** for Q={2}, and ≈ 3·10⁴⁷ for Q={2,3} (extrapolated).
  ⟹ **S = H ∩ [2,82899] satisfies every single-prime fiber condition with threshold 2, at every
  level, for every residue assignment.** No obstruction local at a FIXED finite set of primes can
  ever prove NO. PROMPT §5 idea 5 (q-adic fiber trees) is dead, with a finite certificate.

## MEASURED
- Complete sieve of budget(L_H) for every L_H ≤ 2·10⁶: only **408** pass budget ≥ 2; smallest
  27720; max 2.2682 at L_H = 1801800. Over smooth L_H ≤ 10⁷ the max is 2.3259 at 7207200.
  So everywhere in reach the budget exceeds the hard floor of 2 by only ~10–15%.
- **Unconditional theorem claimed:** walking the 408 survivors and killing via Φ_q < 2 gives
  kills at L_H = 27720, 32760, 50400, 55440, 65520, 75600, 83160, hence **lcm_E ≥ 2·90720 =
  181440**. (Compute expired while grinding L_H = 90720; the bound is a floor, not a ceiling.)
  **AUDITED INDEPENDENTLY by the session** — see AUDITS.md audit 4.
- By L_H ≈ 7·10⁵ the single-prime conditions are satisfied with explicit witnesses (Φ_q ≥ 2.11 at
  L_H = 720720, 1441440, 1801800), so the single-prime route cannot push the bound past ~10⁶.
- Pair condition at L_H = 720720: best assignments found give Φ_{2,3} ≥ 1.849, Φ_{2,5} ≥ 1.906,
  Φ_{3,5} ≥ 1.952 — all < 2 while every single-prime Φ_q ≥ 2.11. **NOT a proof** (the exact
  branch-and-bound did not terminate). If confirmed this would push the lcm bound past 2·10⁶.
  **This is Route D's single most promising unfinished computation.**

## FAILED, and exactly which quantifier step breaks
Every obstruction of the form "∃ finite Q and functional Ψ_Q with Ψ_Q(S) < 2 for all finite
S ⊆ H" fails at the universal quantifier over S, because for every fixed finite Q,
Σ_{m ∈ H, gcd(m,∏Q)=1} 1/m = ∞: one can always retreat to moduli coprime to Q, which pass every
Q-local test for free. A NO proof therefore needs a functional coupling ALL primes with a bound
uniform in the number of primes — i.e. Hough/BBMST distortion technology, which provably requires
least modulus ≥ 616000 while min E = 4.

## Route D's own honest prior
"The answer is probably YES, and the obstruction is purely constructive tightness (budget only
~13% above the hard floor at every reachable lcm), not a genuine local obstruction."
