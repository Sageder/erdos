# AUDITS.md — adversarial audits (Erdős 273)

Every candidate proof gets a written audit here BEFORE it is believed, run against the PROMPT §7
checklist. Verdict first, then item-by-item.

## Audit 1 — Lemma M2 (infimum of Σ1/n over distinct-moduli covering systems = 1)
**Verdict: PASSES, but it is NOT a result about problem 273.**
Claim audited: `attempts/route-M-main/COST_INFIMUM.md`.
1. Admissibility (moduli of the form p−1, p ≥ 5): **N/A and explicitly disclaimed.** The systems
   C_k use moduli 2, 3, 4, 6, 12 and their doublings — 2 and 3 are NOT in E, 12 is not, etc. The
   lemma is about the UNRESTRICTED problem. The write-up says so; it must never be cited as
   progress on 273.
2. Distinctness: checked in code for every C_k (assert on len(set(mods))).
3. Coverage over a full period: verified by explicit mod-lcm sweeps for C_0..C_8.
4. Finiteness/explicitness: each C_k is finite and printed; no "continue similarly".
5. Quantifiers: the statement is ∀ε ∃C, correctly proved by an explicit sequence.
6. No use of modulus 2 in the E-world: N/A (not an E-statement).
7. Density inequality direction: the lower bound Σ1/n ≥ 1 is used correctly (subadditivity), and
   strictness comes from DMNR, applied with its hypotheses (exact cover, k ≥ 2, distinct moduli).
8. Circularity: none — the doubling map is explicit and does not presuppose anything about E.
9. Independent corroboration: Filaseta–Kalogirou (arXiv:2407.15280) reportedly prove the stronger
   statement that least modulus ≤ 4 permits Σ1/n < 1+ε and that > 4 forces a positive excess.
   Recorded as UNVERIFIED-at-primary-source (sandbox egress blocked).
**Net effect on the project:** removes reciprocal-budget counting from BOTH branches' toolkits.

## Audit 2 — Lemma M1 (lcm of any qualifying system is ≥ 55440)
**Verdict: PASSES.**
Claim: every covering system with all moduli in E has L = lcm(moduli) with
f(L) := Σ_{n | L, n ∈ E} 1/n > 1; the least L with f(L) > 1 is 55440 = 2⁴·3²·5·7·11.
1. Every modulus divides the lcm — trivially true, and every modulus is in E, so the used moduli
   form a subset of {n | L : n ∈ E}; hence Σ_used 1/n ≤ f(L). ✓
2. Σ_used 1/n > 1 for a distinct-moduli covering (density + DMNR). ✓
3. The minimum was computed by an EXHAUSTIVE sieve over ALL L ≤ 3·10⁶ (not just smooth L), and
   independently re-derived in the 10⁷ scan; the value at 55440 was re-checked in exact rational
   arithmetic (6429/6160). ✓
4. Hidden truncation check: the statement is a lower bound on L, so scanning an initial range is
   legitimate — the first L found with f(L) > 1 is genuinely the minimum. ✓
5. Overclaim check: this does NOT say lcm = 55440 is achievable, nor bound L above. The
   "divisibility-minimal lattices" list is valid only within the scanned range; a larger lcm may
   have minimal ancestors above 10⁷. Recorded.

## Audit 3 — parity-split equivalence (E-covering ⟺ two disjoint H-coverings)
**Status: NOT YET AUDITED.** Route C was asked to re-prove both directions from scratch. Must not
be used load-bearing until that audit is written here. Specific things to check when it arrives:
negative integers (classes are two-sided); M_0 ∩ M_1 = ∅ enforced; distinctness within each M_j;
the E-unit vs H-unit budget bookkeeping (Σ_{m∈M_j} 1/m > 1 corresponds to Σ_{n∈S_j} 1/n > 1/2, so
the two together give the ordinary Σ 1/n > 1 and there is NO doubling of the E-budget
requirement — an error I made once during setup and corrected).

## Audit 4 — Route D's fiber condition Φ_q ≥ 2 and the lcm lower bound
**Verdict: PASSES (condition re-derived and kills independently reproduced).**
1. Re-derivation. For a covering of ℤ, a prime q, and J ≥ max ν_q(n_i): the integers y ≡ r
   (mod q^J) that a class b_m (mod m) can meet are exactly those with b_m ≡ r (mod q^{ν_q(m)}),
   and inside that fiber the class has relative density q^{ν_q(m)}/m. Density is subadditive and
   the fiber must be covered, so F_q(r) ≥ 1 for every r. Checked: the Haar average of F_q over r
   is exactly Σ 1/n_i, so "Σ 1/n_i > 1" is only the AVERAGE and the covering condition is the
   MINIMUM — the direction is used correctly (§7 item 7).
2. Factor 2. By Lemma M3 the two halves are DISJOINT subsets of the same pool with their own
   residues, so F_q = F_q^{(0)} + F_q^{(1)} ≥ 2 pointwise. Enlarging the used set only increases
   F_q, so it is legitimate to test the full pool S. ✓
3. Independent reimplementation. `experiments/M_audit_phi.py` was written from scratch (it imports
   no D_ code) with exact `Fraction` arithmetic and a complete branch-and-bound; its two prunes
   were checked for soundness (an item at level j can be placed above any chosen fiber, so the
   per-fiber bound is valid; each item adds w to exactly q^{J−j} fibers, so the aggregate bound is
   valid); the symmetry break fixes only the FIRST item, valid because the q-ary tree automorphism
   group acts transitively on level-j nodes.
4. Reproduced Route D's kills exactly: L_H = 27720 (q=2), 32760 (q=2), 50400 (q=2), 55440 (q=5),
   65520 (q=2), 75600 (q=2). Node cap never reached on these.
5. Overclaim check: a FAILURE to kill proves nothing; the walk only yields a lower bound. Route D
   stated this correctly. The bound is "lcm ≥ 2·(first survivor)", not an upper bound.
**Consequence:** L = 55440 — the minimal budget-feasible lattice — is rigorously ELIMINATED. The
SAT and DFS runs at 55440 were therefore chasing an already-decided instance; both were stopped.

## Audit 5 — Route A's Lemma A2 (forced overlap) and Theorem A3
**Verdict: PASSES.**
1. Lemma A2 re-derived from scratch: g(S) = Σ_{m∈S} 1/m − dens(∪ S) is non-decreasing (adding a
   class of modulus m′ raises the sum by 1/m′ and the density by at most 1/m′); g(M) = X because
   the union is ℤ; for pairwise coprime T the classes are independent by CRT so dens(∪_T) is
   exactly 1 − Π(1−1/m) for ANY residues. Hence X ≥ f(T). The "any residues" step is the crux and
   it is correct — coprimality makes the bound residue-free, which is what lets it quantify over
   all assignments.
2. Brute-force counterexample hunt: 463 (covering system, coprime subset) pairs from random
   covering systems on lattices 12…180; no violation; tightest slack exactly 1/6 at T = {2,3}.
3. f-values re-computed exactly: f({2,3}) = 1/6, f({2,5}) = 1/10, f({3,5}) = 1/15. ✓
4. A3's forcing step re-checked at the threshold: 31/30 − 1/4 = 47/60, − 1/6 = 13/15,
   − 1/10 = 14/15, all < 1, so 4, 6, 10 are forced. ✓
5. Strictness: the pigeonhole needs X_c < 1/15 STRICTLY, which needs X_{1−c} > 0 strictly — that
   is DMNR applied to the other half (a distinct-moduli covering cannot be exact). Hypotheses of
   DMNR (k ≥ 2, distinct moduli, exactness) are correctly checked. ✓
6. Enumeration reproduced independently: 90 values L ≤ 10⁶ with B_E(L) > 1, ALL divisible by 60,
   smallest 55440; A3 kills 63, leaving the stated 27. ✓
7. Scope check (§7 item 5): A3 is a statement about a FIXED L, not about all finite S ⊆ E. It
   contributes a lower bound on the lcm, never a NO proof. Route A stated this correctly.
8. Note: A3 does NOT kill 55440 (B_E = 6429/6160 > 31/30); the fiber condition does. The two
   tools are genuinely complementary and are combined in `experiments/M_eliminate.py`.
