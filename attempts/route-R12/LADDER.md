# LADDER.md — the reduction ladder for Erdős 727 (route R12 consolidation)

Everything in Sections 1–3 is elementary and either proved here or numerically verified
with proofs drafted; Section 4 isolates the analytic frontier. m = n + k throughout;
c_ℓ(n) = #carries of n + n base ℓ = ν_ℓ(C(2n,n)).

## 1. Criterion (proved; verified)

n ∈ S_k ⟺ for every prime ℓ | (n+1)···(n+k): c_ℓ(n) ≥ 2 Σ_{j=1}^k ν_ℓ(n+j).
[(n+k)! = n!·∏(n+j); Legendre/Kummer. Verified: experiments/verify_identities.py,
route-R3/reductions.py.]

## 2. Lemma R_k (general fixed k; elementary)

Fix k ≥ 2 and set P₀ = 2k (any P₀ ≥ 2k works). Choose:
 - a modulus Q₀ = ∏_{ℓ ≤ P₀} ℓ^{L_ℓ} and a class c₀ mod Q₀ such that for n ≡ c₀:
   (i) the valuations v_{ℓ,j} := ν_ℓ(n+j) are pinned (finite exact values) for all ℓ ≤ P₀,
       j ≤ k; write c_j := ∏_{ℓ ≤ P₀} ℓ^{v_{ℓ,j}} (the "small part" of n+j);
   (ii) for each ℓ ≤ P₀, the base-ℓ digits of n at positions [D_ℓ, D_ℓ + 2V_ℓ] are ≥ ⌈ℓ/2⌉,
       where D_ℓ = 1 + max_j v_{ℓ,j} and V_ℓ = Σ_j v_{ℓ,j}. (Such digits force
       c_ℓ(n) ≥ 2V_ℓ = the full ℓ-demand, for EVERY n in the class.)
   EXISTENCE of the class: trivial — n is a free variable; prescribe n mod ℓ^{L_ℓ} digit
   by digit (choose the low digits to realize any consistent valuation pattern
   v_{ℓ,j} of k consecutive integers, then the forcing digits above). CRT across ℓ. □
 - for each j ∈ {1, ..., k}: DISTINCT primes s_j ≠ r_j, both > max(P₀, c_j), with
   (n+j)/c_j = r_j s_j,   c_j s_j − 1 < r_j ≤ 2 c_j s_j − 1,   (c_j r_j mod s_j) ≥ (s_j+1)/2.

**Lemma R_k.** Any n ≡ c₀ (mod Q₀), n > (2k)^4 (large enough that s_j > c_j is
automatic), satisfying all of the above lies in S_k. [Audit note: r_j = s_j must be
excluded explicitly — the c_j = 1 box does not exclude it; distinctness across j is
automatic (gcd of window elements divides differences < k < s).]

Proof. Primes ℓ ≤ P₀: demand 2V_ℓ met by (ii) (digits ≥ ⌈ℓ/2⌉ each force a carry
regardless of neighbours). Primes ℓ > P₀ = 2k divide at most one window element (else
ℓ | difference < k), so the demand at r_j (resp. s_j) is exactly 2.
At r := r_j, c := c_j, s := s_j: n = c r s − j = (cs − 1) r + (r − j); both digits valid
(0 ≤ r − j < r; cs − 1 < r by the box), so the two lowest base-r digits of n are
(cs − 1, r − j) [and n < r² iff cs ≤ r — wait: n = (cs−1)r + (r−j) with cs − 1 < r means
exactly 2 digits]. Doubling: position 0: 2(r − j) ≥ r ⟺ r ≥ 2j — true (r > 2k ≥ 2j):
carry. Position 1 (carry-in 1): 2(cs − 1) + 1 ≥ r by the box upper bound: carry. c_r ≥ 2. ✓
At s := s_j: write c r = A s + b, b = c r mod s; b ≠ 0 (s prime > P₀ ≥ c, s ≠ r).
n = (As + b)s − j = A s² + (b − 1) s + (s − j): the two lowest base-s digits are
(b − 1, s − j) regardless of the expansion of A. Doubling: position 0: 2(s − j) ≥ s ⟺
s ≥ 2j: true: carry. Position 1: 2(b − 1) + 1 ≥ s ⟺ b ≥ (s + 1)/2: hypothesis: carry.
c_s ≥ 2. ✓ All demands met. ∎

[k = 2 instance = route-R3's Lemma R (c₁ = 1, c₂ = 2, plus n ∦ 2-power absorbed into the
class). Verified: 18/18 regenerated solutions q ≤ 1500 in S₂ (full criterion); R3: 123/123.]

## 3. The analytic targets B_k

**Statement B_k.** For the (any) admissible class (c₀, Q₀) of Lemma R_k: there are
infinitely many n ≡ c₀ (mod Q₀) such that for every j ≤ k, (n+j)/c_j = r_j s_j with primes
in the Lemma-R_k boxes.

**Theorem (ladder).** B_k ⟹ S_k infinite. (∀k ≥ 2: B_k) ⟹ 727-YES. B_2 ⟹ the named
k=2 variant. [Immediate from Lemma R_k. Quantifiers: k fixed first; the class and boxes
depend only on k; n → ∞ inside. No unproved smoothness/digit statement is consumed —
ALL digit content of 727 has been discharged into elementary forced carries; B_k is a
pure prime-equation statement: k−1 bilinear equations (c_{j+1}r_{j+1}s_{j+1} −
c_j r_j s_j = 1) in 2k prime variables + archimedean ratio boxes + congruence classes +
the residue conditions (c_j r_j mod s_j large).]

Heuristic counts: B_k solutions up to x ≈ x/(log x)^{2k} · (positive box/residue
constants): divergent for every k. Verified numerically for k = 2 (123 sols q ≤ 4000,
growth ≍ Q²/log⁴Q). For k = 3: 0 structural hits below 4·10⁵ — consistent with onset
~1/log⁶ (expected ≈ 0.1 there); larger search pending.

## 4. Difficulty assessment (honest)

- B_2: one bilinear equation pq + 1 = 2rs, four primes, boxes ≡ SL₂-matrix with (almost-)
  prime entries / "shifted E₂ is 2·E₂". At the dispersion/Harman frontier; not implied by
  any single published theorem we know yet (R11 literature sweep running). Relaxations
  compatible with Lemma-R''-style forcing: allow each window part to be q·p or q·p₁p₂
  (P₂-completions with residue conditions instead of pure forcing — the pos-1 carry
  condition at q becomes "p₁p₂ mod q ≥ (q+1)/2", a countable equidistribution event, so
  Chen-type switching outputs are ACCEPTABLE). Narrowest target (Theorem B*): parametrize
  n + 2 = 2rs by free prime pairs (r, s) in boxes; sieve the single sequence
  {2rs − 1} for values q·p or q·p₁p₂ with all factors > x^δ, ratio boxes, and residue
  conditions. Needs: level-of-distribution for bilinear (r,s)-sums to moduli x^{1/2+δ}
  (BFI/E₂-type inputs) + a Harman/Chen weighted decomposition. Research-paper scale.
- B_k, k ≥ 3: k−1 SIMULTANEOUS bilinear prime equations: no current technology (even two
  simultaneous Chen-type conditions are open). The headline through this ladder awaits
  fundamentally new analytic input — OR a different mechanism entirely (route R10).
- The ladder itself is (we believe) a genuinely new structural localization of 727:
  every digit/carry aspect is discharged elementarily; what remains is prime equations.

## 4.5 Lemma R‴ — the definitive membership engine (proved; verified, 0 false positives
on all even n ≤ 6·10⁴: attempts/route-R12/, run 2026-07-28)

**Lemma R‴.** Fix k ≥ 2 and P₀ ≥ 2k. Suppose:
 (a) for every prime ℓ ≤ P₀: c_ℓ(n) ≥ 2 Σ_{j=1}^k ν_ℓ(n+j)  [class-forceable when the
     small parts are bounded; else checked/counted];
 (b) for every j ≤ k and every prime ℓ > P₀ dividing n+j: ℓ ∥ n+j, and
     C_ℓ:  ((n+j)/ℓ − 1) mod ℓ ≥ (ℓ−1)/2.
Then n ∈ S_k.
Proof. ℓ ≤ P₀: (a). ℓ > P₀ ≥ 2k divides exactly one window element, demand 2. With
W = (n+j)/ℓ: n = (W−1)ℓ + (ℓ−j), digits (…, (W−1) mod ℓ, ℓ−j). Doubling: position 0:
2(ℓ−j) ≥ ℓ (ℓ > 2k ≥ 2j): carry; position 1 with carry-in: 2((W−1) mod ℓ) + 1 ≥ ℓ ⟸ C_ℓ:
carry. ∎
Remarks. (i) Subsumes Lemma R_k: the boxes force C_ℓ when the window part is a balanced
pair. (ii) For ℓ > √(2(n+k)): C_ℓ ⟺ W ≥ (ℓ+1)/2: balancedness = the necessary smoothness.
(iii) C_ℓ is one sufficient route to the second carry (higher-digit carries also count);
hence R‴ is sufficient, not necessary (coverage 45/263 of even S₂ members ≤ 6·10⁴).

## 4.6 The difficulty triangle (why k=2 is open; structural summary)

Any YES proof needs a supply of n with (necessarily) √-smooth windows AND the per-prime
second-carry conditions. Three corners, each blocked differently:
 (i) DENSE unstructured supply (all n, first moment): contains "n+1, n+2 both
     √(2n)-smooth in positive density" = open correlation problem; measured E > 1.
 (ii) RIGID algebraic supply (powers, Pell): infinitude known, but zero averaging freedom;
     squares double valuations past digit supply (Lemma Q); structural primes fail.
 (iii) PRIME-PARAMETRIZED supply (Lemma R_k/R‴ with each window part built from chosen
     primes): all digit content discharged elementarily; remaining task = prime-equation
     statements (B_k / B″ / shift-1 correlations of smooth∗prime sequences) at the
     dispersion/Chen frontier for k=2, beyond current technology for k ≥ 3.
Corner (iii) is the closest to current technology for the k=2 named variant.

## 5. Sharpest analytic form for k=2 (B†; lead analysis 2026-07-28)

Generalize Lemma R_2 to accept smooth-times-prime window parts (the balanced partner of a
large prime need not be prime — any P₀-smooth C in the right size-box works, with the
small primes of C paid by class-forced/counted carries at ℓ ≤ P₀ and the residue condition
(C·? mod ·) versions countable):
  n + 1 = M'·q (M' smooth-in-box, q prime, q ≤ 2M'−1-balance, residue cond),
  n + 2 = 2·C·r (C smooth-in-box, r prime, balance, residue cond).
Then S₂-infinitude ⟸ B†: the shift-1 correlation statement
  #{(C, r, M', q): 2Cr − M'q = 1, boxes/classes/residues} → ∞.
Assessment: binary (shift-1) correlation of two smooth∗prime sequences — NOT circle-method
amenable (binary obstruction); the right technology is dispersion/BFI-Titchmarsh-style
(one side needs level of distribution > 1/2 — plausible for smooth∗prime with the dense
smooth average — the other side Vaughan-decomposed), or a Chen-style weighted sieve if a
"consecutive P₂-with-structure" theorem (Heath-Brown line) can be adapted. Morally:
"n, n+1 both P₂ with smooth-parts and localized prime factors" — STRICTLY above Titchmarsh
(primality on both sides), below twins (dense smooth averaging available on both sides).
Waiting on R11 literature verdict to calibrate feasibility.
