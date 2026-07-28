# Route G — Selfridge template surgery and divisor-lattice transplants. Final report.
(Transcribed by the session; scripts: `experiments/G_*`.)

## PROVED
- Lemmas 1–2 re-derive the parity split (fourth independent derivation, agrees with Lemma M3).
- **Corollary 3 (= our Observation M4).** Since 2 ∈ H lies in only one of S_0, S_1, a YES answer
  REQUIRES a covering system with distinct moduli all of the form (p−1)/2, p ≥ 7 prime, i.e. an
  H-covering with least modulus ≥ 3. **This is the crux object.**
- **Corollary 4.** If the lcm is L = 2M then s(M) := Σ_{m | M, 2m+1 prime, m≥2} 1/m > 2.
- **Lemma 5.** Two classes with coprime moduli always intersect, so in a DISJOINT packing all
  moduli on one parity class are pairwise non-coprime. D_H(180) contains the pairwise-coprime
  triples {2,3,5} and {2,5,9}, so the naive packing bound at L = 360 is unattainable.

## VERIFIED
- **Selfridge system reconstructed and triple-verified** (moduli dividing 360, p ≥ 3 allowed):
  0(2), 1(4), 3(6), 7(10), 11(12), 1(18), 1(30), 7(36), 23(40), 19(60), 67(72), 175(180);
  every n+1 ∈ {3,5,7,11,13,19,31,37,41,61,73,181} prime; Σ1/n = 23/18. Exhaustive enumeration
  finds exactly **827 978** such systems in that pool.
- **Rigidity of the Selfridge cheat.** D_H(180) = {2,3,5,6,9,15,18,20,30,36,90} has EXACTLY ONE
  inclusion-minimal covering subset — the whole pool. So the modulus-2 class carries exactly 180
  residues mod 360 and there is ZERO slack to redistribute.
- **Exact maximum coverage without the modulus 2, divisors of 360:** 260 of 360 residues, i.e.
  min uncovered 100 (density 5/18) — the density bound 80 is unattainable (Lemma 5). Exhaustive,
  787 532 nodes, with an explicit optimal witness and its 100-residue uncovered set.
- **s(M) > 2 first at M = 27720** (exact sieve + Fraction re-check over every M ≤ 3·10⁵) —
  third independent confirmation of our Lemma M1: lcm ≥ 55440, with lcm/2 in an explicit
  52-element list beginning 27720, 32760, 50400, 55440, 65520, 75600, 83160, 90720, 98280, …
- **Budget cap (beam search over 47-smooth M):** max s(M) for M ≤ 10³/10⁴/10⁵/10⁶/10⁷/10⁸/10⁹ =
  1.7097 / 1.9471 / 2.1333 / 2.2470 / 2.3259 / 2.4125 / 2.4838. Best *balanced* split (exact
  subset-sum DP, smooth M ≤ 3·10⁶): the smaller half never exceeds **≈ 1.1096** (M = 831600).
- **Transplants.** In the H-world the minimum number of inadmissible moduli, mindef(M), is
  2,2,1,2,2,1,1 for M = 12,24,36,48,60,72,120 and **0 from M = 180 onwards** (180, 360, 720, 1260,
  2520 all admit fully admissible transplants). In the E-world mindef(L) = 2 for L ≤ 240 and = 1
  for L = 360, 720, 1440, 2520, 5040 — **the single bad modulus always being exactly 2**. The
  Selfridge cheat is the unique obstruction at every classical lattice.
- **M = 180 is the smallest lattice supporting an H-covering** (SAT over every M ≤ 400; next are
  270, 288, 360).
- **CRUX, VERIFIED UNSAT:** there is NO covering with distinct moduli from D_H(M)∖{2} for
  **M = 180, 240, 270, 360, 420, 450, 480, 540, 600, 720** (all M ≤ 600 with budget > 1, plus 720;
  SAT cross-checked by an independent C branch-and-bound). Exact near-misses: min uncovered 25/180
  (density 5/36), 34/360 (17/180), 60/720 (1/12), with explicit optimal witnesses and uncovered
  sets. The obstruction concentrates on **4, 10, 12 ∉ H** (9, 21, 25 composite) — precisely the
  moduli every cheap least-modulus-3 covering wants.

## Correction to the working data (VERIFIED)
The H-list used in the wave-1 agent briefs **omitted 54** (2·54+1 = 109 is prime); correspondingly
108 ∈ E. Correct: H = 2,3,5,6,8,9,11,14,15,18,20,21,23,26,29,30,33,35,36,39,41,44,48,50,51,53,
**54**,56,… This was an error in the session's hand-written brief, not in PROBLEM.md (whose list
stops at 44 and is correct) and not in any computation (every agent recomputed H itself).

## FAILED
1. **The decisive instance was not decided.** D_H(27720)∖{2} (budget 1.5873, the first lattice
   where the density condition can hold): SAT with 106 285 vars / 187 119 clauses ran > 20 min
   without a verdict; likewise M = 1260, 2520, 5040. **So L = 55440 remains open at the crux.**
2. **No rigorous lower bound on the reciprocal cost of an H-covering.** All σ-measurements are
   upper bounds, so the budget-gap argument cannot be upgraded to a proof.
3. Route G finds **no mechanism for a NO answer**: every obstruction located is
   finite-lattice-specific and none survives passage to larger M.
