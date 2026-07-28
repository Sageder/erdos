# PROOF SKELETON — Theorem K2: S_2 is infinite (octic family, first moment)

Target: for every large W there is w ∈ [W, 2W] with n = w⁸ − 2 ∈ S₂. Hence S₂ is infinite.
(Resolves the named k=2 variant `erdos_727.variants.k_2` affirmatively; NOT the headline.)

Family F(W): w ∈ [W, 2W], w ≡ c₀ (mod Q₀), P(w) ≤ w^{1/3}.
 (Q₀ = ∏_{p ≤ P₀} p^{L_p}; c₀, L_p, P₀ fixed by Lemma 3.)

Notation: m = w⁸; κ_p(x) = # carries when doubling x in base p (= ν_p(C(2x,x)));
d_j(x) = j-th base-p digit; "big digit" = d_j ≥ ⌈p/2⌉.

## Lemma chain (status tags: [V] numerically verified, [P] proved, [ ] to do)

L1 [V][ ] Criterion. n ∈ S₂ ⟺ ∀p: κ_p(m) ≥ ν_p((2m)(2m−1)(2m−2)(2m−3)), m = n+2.
   (Legendre/Kummer computation; PROBLEM.md chain; verified in verify_identities.py.)

L2 [V][ ] Reduction (Prop N, k=2 + Lemma O). For n > 8: n ∈ S₂ ⟺
   (a) κ₂(m) ≥ 2 + ν₂(m−1) and κ₃(m) ≥ W'₃(m);
   (b) ∀p ≥ 5, p^J ∥ m−1: κ_p(⌊m/p^J⌋) ≥ J;
   (c) ∀p ≥ 5, p ∣ m, e = ν_p(w): κ_p((w/p^e)⁸) ≥ 8e.
   Odd-position elements 2m−1, 2m−3 are free (Lemma O: m ≡ (p^J+i)/2 mod p^J has all J low
   digits ≥ ⌈p/2⌉). Verified in verify_propN.py.

L3 [ ] Small primes (finite certificate). There exist P₀, L_p (p ≤ P₀), and a class c₀ mod
   Q₀ = ∏ p^{L_p}, with (c₀, Q₀) = 1, such that every w ≡ c₀ satisfies the L2-conditions at
   every p ≤ P₀. Construction per prime:
    - p ∈ {7, 11, 13, ..., P₀}: choose c₀ mod p with c₀⁸ ≢ 0, 1 (mod p) — no condition at p.
      (Possible: ≤ 9 excluded residues < p for p ≥ 11; p = 7: w⁸ ≡ w² — exclude w ≡ 0, ±1.)
    - p = 5: w⁸ ≡ 1 (mod 5) forced. Choose c₀ mod 5^{L₅}: ν₅(w⁸−1) = 1 exactly, and digits
      1..L₅−1 of w⁸ contain a big digit forcing ≥ 1 carry above position 1. Finite search.
    - p = 3: fix ν₃(w⁸−1) = 1 (w ≡ 2 mod 9 e.g.) and force W'₃ = ν₃(2m−2) = 1 ≤ κ₃ via a
      big digit. (Check W'₃ composition: 3 ∤ m, 3 | m−1; odd elements: 3 | 2m−1 ⟺ m ≡ 2:
      m ≡ 1 mod 3 always (w⁸ ≡ 1) so 3 ∤ 2m−1, 3 | 2m−3 ⟺ 3 | m: no. So W'₃ = ν₃(2(m−1)).)
    - p = 2: w odd, fix ν₂(w⁸−1) = 5 (w ≡ 3 mod 8 hmm — VERIFY exact: ν₂(w²−1) for
      w ≡ 3 mod 8 is ν₂(w−1)+ν₂(w+1) = 1+2 = 3, ν₂(w²+1) = 1, ν₂(w⁴+1) = 1: total 5);
      demand s₂(m) ≥ 2 + 5 = 7: force 7 ones among low bits of w⁸ via c₀ mod 2^{L₂}.
   All existence claims are finite computations — produce certificates in smallprime_cert.py
   and verify each class on random w. MUST also prove: the class forces the conditions for
   ALL w ≡ c₀ (digit-forced carries are unconditional on higher digits; ν-values pinned).

L4 [ ] Base count. |F(W)| ≥ c₁ W for large W, c₁ = c₁(Q₀) > 0.
   Tool: smooth numbers in a fixed AP (R8-T1: Hildebrand + Granville; ρ(3) > 0).

L5 [ ] Carry-measure lemma (the cylinder-counting engine). Let p ≥ 5, t ≥ 1, r ≥ 1,
   Q = p^{J+t}. Let G ⊆ Z/QZ be the set of residues x with fewer than r carries among digit
   positions [J, J+t) when doubling any m ≡ x (mod Q) — precisely: carries computed from
   digits d_J..d_{J+t−1} with carry-in 0 at position J (undercounts true κ ⟹ G contains all
   failures). Then:
   (i) G is a union of "digit boxes"; via inclusion–exclusion over which positions have big
       digits, 1_G = Σ over ≤ 2^t signed terms, each an intersection of ≤ t single-digit
       interval conditions; each single-digit condition at position j is ONE interval mod
       p^{j+1} (up to ⌈⌉ boundary), so each term is an arithmetic box with Fourier ℓ¹-norm
       ≤ (C log p^{J+t})^{t}.
   (ii) μ(G) := |G|/Q ≤ P(N_t < r) + C t/p, where N_t = # successes in the stationary carry
       chain (R8-T8; re-prove: 2-state chain, Chernoff, P(Bin-type tail)). Explicit bound:
       μ(G) ≤ exp(−t·I(1 − 2r/t·(1+δ))) + Ct/p for r ≤ t(1/2 − δ)-range; also the trivial
       cap and exact small-t values (used numerically for the budget integrals).
   NOTE: define carefully "fewer than r carries among [J, J+t) with carry-in 0" as the
   failure superset: true κ_p(⌊m/p^J⌋) ≥ (carries in the window) always. [Direction check!]

L6 [ ] Weyl-equidistribution lemma (degree 8). For p ≥ 5, Q = p^s ≤ V^{8−δ}, any interval
   I of length V, any arithmetic box B ⊆ Z/QZ that is an intersection of ≤ t single-digit
   interval conditions (as in L5), any fixed class v ≡ a (mod Q₀·p^{fixed}) hmm — general
   form: for (Q, Q₀) coprime moduli:
     #{v ∈ I : v ≡ a (Q₀'), v⁸ mod Q ∈ B} = |I|·μ(B)·(1/Q₀') + O(E)
   with E ≤ (C log Q)^{t}·8·V^{1−2^{−7}+ε}·(number-of-terms bookkeeping) — assembled from:
   Weyl's inequality for degree-8 monomials (savings V^{−2^{−7}}), completion, and the
   Fourier ℓ¹ bound of boxes. The count of v with v⁸ ∈ (union via incl-excl) then carries
   ≤ 2^t·(t choose ·) terms — total error poly(t, log)·V^{1−2^{−7}+ε}. All constants explicit.
   ALSO the multiplicity subtlety: v ↦ v⁸ is ≤ 8·p^{c}-to-1 only on units — we do NOT need
   preimage counts: we count v directly through additive characters of v⁸. ✓

L7 [ ] w-source bound. Σ_{p > P₀, e ≥ 1, p^e ≤ (2W)^{1/3}} #{w ∈ [W,2W] free in class:
   p^e ∥ w, κ_p((w/p^e)⁸) < 8e} ≤ ε₇(P₀)·W + O(W^{1−c}), with explicit
   ε₇(P₀) = Σ_{β-integral} tail terms → 0 as P₀ → ∞... CAREFUL: ε₇ does NOT → 0 by raising
   P₀ alone (the boundary β ≈ 1/3 mass is fixed); ε₇ ≈ ∫_0^{1/3} taillike(β) dβ/β ≈ 0.12
   NUMERICALLY-EVALUATED rigorous bound: split (P₀, W^{1/3}] into dyadic/geometric β-bands,
   on each band apply L5+L6 with t(β) = ⌊(8−δ)(1−β)/β⌋ − J − 1 hmm bounded by Weyl range;
   sum explicit constants. Deliverable: a finite table of band-bounds whose sum is ≤ 0.13.
   (v-interval: v ∈ [W/p^e, 2W/p^e]; drop v-smoothness and the p^e ∥ (exact divisibility:
   v ≢ 0 mod p: harmless restriction enlarging count) for the upper bound.)

L8 [ ] (w−1)-source bounds.
   (a) Danger zone p > (2W²)^{...}: precisely: p ∥ w−1, p > c·W^{8/9}: certain-fail region:
       count ≤ Σ_{p ∈ (cW^{8/9}, 2W]} (W/p + O(1)) = (log(9/8) + o(1) + f(c))·W by Mertens.
       We do NOT even need failure to be certain here — we EXCLUDE the whole zone (any w
       with a w−1 factor there is counted as lost). Budget ≈ 0.118 + (c-adjustment).
   (b) Middle zone p ∈ (W^{2/3−η}, cW^{8/9}]: failure requires the (≤ 3) digits of
       ⌊w⁸/p^J⌋ visible above... use L5/L6 on the w-variable directly: w ≡ 1 + (class) mod
       p^{J}, digit conditions at positions [J, J+t): moduli p^{J+t} ≤ W^{8−δ} ⟹ t huge:
       but the digits available: only D = 8/β − J: t ≤ D: fail prob per exposure ≈ 2^{−D}:
       band-sums: Σ (W/p^J)·μ(G) over the zone ≈ ∫ 2^{−(8/β−1)}dβ/β·W ≈ 0.07·W. Rigorous
       band table again. Weyl here is over w itself (interval length W, modulus ≤ W^{8−δ} ✓).
   (c) Low zone p ≤ W^{2/3−η}: μ(G) ≤ 2^{−D(β)} with D ≥ 4: band-sums small (≤ 0.02).
   (d) Spikes J ≥ 2: Σ_p,J≥2 W/p^J ≤ W·Σ 1/p(p−1) over p > P₀: ≤ W/(P₀ log P₀): tiny.
   Same treatment verbatim for (w+1)-source (empirically 0 failures — but we do NOT rely on
   the alternating-pattern auto-pass for the proof unless it shortens: bound as in (b), (c):
   the (b)-zone for w+1 needs the SAME band bounds — fine, budget doubles (b) to 0.14?? NO:
   for w+1 the danger-zone certain-fail does not occur (pattern is safe) but we may still
   pay the same (a)-style Mertens loss OR prove the auto-pass lemma:
   L8+ [ ] Auto-pass lemma for minus-shifts: p ∥ w+1, p > c'W^{8/9} ⟹ the digit at
   position 1 of m = ((ap−1)⁸ form) is ≥ ⌈p/2⌉ ⟹ κ ≥ 1 = J. Elementary binomial-digit
   computation — verified empirically (0 fails in 1500 exposures). Then (a)-loss only for
   w−1. DECIDE during drafting: prove L8+ (saves 0.118) — worth it.

L9 [ ] (w²+1)- and (w⁴+1)-source bounds. For p | w^{2^j}+1 (j = 1, 2), J = ν_p:
   (a) auto-pass: p ∥ w^{2^j}+1 with a = (w^{2^j}+1)/p, 2a² ≤ p ⟹ digits of m base p are
       (a²−1, p−2a, 1)-type with p−2a ≥ ⌈p/2⌉ ⟹ κ ≥ 1. Prove the exact inequality range.
       [Verified: 0 violations in scans.] Handles p ≥ (2)^{1/3}w^{2^{j+1}/3}.
   (b) Below the auto-pass line: divisor-switch: w^{2^j}+1 = a·p: for each a in dyadic
       ranges, w runs over ≤ ρ_{2^{j+1}}(a) classes mod a (roots of x^{2^j} ≡ −1), and p =
       (w^{2^j}+1)/a must be PRIME (else p not this source... careful: p prime is given —
       the event is "p prime factor in the zone" — parametrized by the cofactor a: bound:
       Σ_{a} #{w ∈ [W,2W]: w ≡ r_a (a), (w^{2^j}+1)/a ∈ P, digit-fail}. Drop digit-fail
       (crude) or keep 2-digit conditions (sawtooth in w — the digits of m base p with p a
       FUNCTION of w: d₁(m) ≈ frac((w^{2^j}+1)²-ish/…): monotone sawtooth pieces: elementary
       interval decomposition, no Weyl needed — the pieces where d₁ is small form an explicit
       union of w-intervals per a). Primality via Richert Thm 11.4 upper bound (R8-T5):
       ≤ (2+o(1))·S(F_a)(W/a)/log(W/a) uniformly a ≤ W^{1−δ}... wait the polynomial here is
       degree 2^j in w restricted to an AP mod a — verify the sieve axioms for these forms
       (R8 did F_a(t) = at² + 2z₀t + (z₀²+1)/a for j=1; the j=2 analog: quartic — sieve
       dimension still 1, axioms analogous — VERIFY; if the quartic sieve verification
       drags, fall back to counting also over prime-POWER cofactors... no: simplest crude
       route: drop primality too and pay ρ-average: Σ_a ρ(a)/a over the zone ~ const·log —
       DIVERGES: primality is needed. Keep Richert.)
   Budget target: ≤ 0.25 total for both j.
   ALSO µ-subtlety: ρ_{2^{j+1}}(a) averages (R8-T6-analog: Dirichlet series with L-functions
   for x^{2^{j+1}} ≡ −1: mean value constants — needed explicitly for the budget: compute
   via Landau/Wirsing or cite; numerically verifiable.)

L10 [ ] Assembly. |{w ∈ F(W): some condition fails}| ≤ (E-budget)·W + o(W) with
   E-budget = L7 + L8(a,b,c,d) + L9 + spikes ≤ 0.75 (target; each term a rigorous numeric
   bound from its band table). Since |F(W)| ≥ c₁W... WAIT — CRITICAL STRUCTURE POINT:
   the failure counts L7–L9 are over w in the CLASS+INTERVAL but WITHOUT smoothness (upper
   bounds relax smoothness), while |F(W)| = c₁W counts smooth-w-in-class: the comparison
   needs failure-count ≤ (1−δ)|F(W)|: c₁ = ρ(3)/Q₀-ish is SMALL (ρ(3) ≈ 0.0486/Q₀-fraction)
   while E-budget·W is ≥ 0.1·W·(1/Q₀-fraction? NO — failure counts are also within the
   class mod Q₀: both scale with 1/Q₀ hmm — but NOT with ρ(3)!!). ***THE SMOOTHNESS
   RELAXATION BREAKS THE BUDGET: E·W/Q₀ vs c₁W = ρ(3)W/Q₀: need E < ρ(3) ≈ 0.05 — NOT 1!***
   FIX REQUIRED: do not relax smoothness in the failure counts, OR restructure:
   Option A: count failures WITHIN smooth w: needs smooth-in-AP equidistribution at large
     moduli — the tool we lack.
   Option B: drop the smoothness restriction from the family and handle large prime factors
     of w by counting them as failures... but p ∥ w with p > W^{1/3}: v-interval too short
     for Weyl at demand 8: certain-fail-ish for p > W^{4/5}-zone only: for p ∈ (W^{1/3},
     W^{4/5}) the failure is genuinely probabilistic (~Bin(D)≤7, D = 8/β−8 ∈ (2, 16)) and
     the Weyl range t ≤ (8−δ)(1−β)/β − ... at β = 0.5: t ≤ 8−: μ(G-cap) ≈ P(Bin(7) ≤ 7) = 1
     — NO USABLE BOUND in (≈0.47, 0.8): mass log(0.8/0.47) ≈ 0.53 lost AT FULL WEIGHT ⟹
     E ≥ 0.53 + 0.118 + ... ≈ 0.8 — PLUS w-zone (0.8,1]: log(1/0.8) = 0.22 certain-fail ⟹
     E ≈ 1.0+: FAILS. Unless: Bin(7)≤7... demand 8 carries with only ≤ 8 digits total:
     β ∈ (0.47, 1): D = 8/β−8 < 9: available < 9 digits and need 8: μ_true ≈ tiny anyway??
     P(Bin(8) ≥ 8) = 2^{−8}: at β slightly < 0.5 there are just-enough digits: true fail
     prob ≈ 1 − 2^{−8}-ish ≈ 1: so genuinely ~certain-fail for all β > 0.47-ish!! ⟹
     zone (0.47, 1] weight log(1/0.47) ≈ 0.755 + rest > 1: Option B DEAD.
   Option C: RESTRUCTURE the family: w = q·u with u SMOOTH-SMALL FIXED-RANGE... the real
     issue: need a POSITIVE-density-like base within which failures are countable. Use
     w = u·s where u ∈ [W^{2/3}, 2W^{2/3}] arbitrary integer (free variable for Weyl!) and
     s ∈ S* a FIXED set of W^{1/3}-sized products of primes in (P₀, W^{1/100}]... hmm w's
     factors = u's factors ∪ s's: u arbitrary has big prime factors ⟹ dead as B.
   Option D: verify smooth-AP counts ARE available at the needed moduli: needed moduli for
     L7: p^t ≤ V^{8−δ} with v-interval... the failing-v count within SMOOTH v: smooth
     numbers weighted in Weyl sums: "Weyl sums over smooth numbers" EXIST (Vaughan–Wooley
     smooth Weyl sums! — the core of modern Waring: exponential sums Σ_{v smooth} e(αv⁸)
     have power-saving bounds!) — this is the actual fix: redo L6 with smooth-Weyl sums
     (Vaughan–Wooley technology, classical, published, explicit exponents). Alternatively:
   Option E: change the smoothness cap to a LARGE-FACTOR-COUNT cap: family = {w: w has at
     most ONE prime factor > W^{1/100} hmm same counting need}.
   Option F: PRECISE analysis: the failure events for p ≤ W^{1/3} only involve v = w/p^e:
     define family WITHOUT smoothness but with the w-source conditions IMPOSED VIA the
     structure: F = {w = p₁···p_r·(W^{1/100}-smooth part): each p_i in prescribed dyadic
     windows with prescribed digit-good classes}: build w multiplicatively so that the
     w-source conditions hold BY CONSTRUCTION: count |F| from below by choosing each p_i
     from the ≥ (1−tail)·π(range) good primes GIVEN the rest... circular dependence (each
     p_i's condition depends on v_i = w/p_i^{e_i} i.e. on the others) — break circularity
     with a fixed-point/greedy?: conditions are "κ_{p_i}(v_i⁸) ≥ 8": choose the p_i
     SEQUENTIALLY LAST-TO-FIRST?? Each condition constrains p_i given v_i (product of
     others): pick s (smooth core) first, then p₁ | given the rest... but v₁ includes
     p₂...p_r: choose p_r last: its condition depends on v_r = w/p_r (fixed by earlier
     choices): #good p_r in its window: (1 − o(1))·π(window) — GOOD primes for the
     condition at p_r: {p: κ_p(v_r⁸) ≥ 8}: counting good PRIMES p for FIXED N = v_r⁸:
     the {N/p^j}-over-primes equidistribution problem (large c)!! — back to the hard tool.
     BUT: we don't need equidistribution for a 1−o(1) count — a POSITIVE PROPORTION of
     good p suffices (redefine budget): is there a CHEAP argument that ≥ 51% of primes p
     in a dyadic window give κ_p(N⁸...) ≥ 8?? Without equidistribution: hmm. κ_p(v⁸) ≥ 1
     is cheap-ish (only need one big digit)... ≥ 8 needs 8 digits: no cheap trick.
   DECISION NEEDED. Option D (smooth Weyl sums, Vaughan–Wooley) is the classical-tool
   path: STATUS: check exact citable forms (R8 follow-up); expected: Σ_{v ∈ S(V, y)}
   e(αv^k) ≪ V^{1−c(k)+ε} for α in minor-arc-type conditions q ≤ V^{...}: our α = a/p^t:
   "major/minor" bookkeeping needed. This is the ONE genuinely heavy analytic ingredient
   left. Alternative sub-option D': use u = 1/3-smooth numbers' FLEXIBLE-FACTOR structure:
     every W^{1/3}-smooth w ∈ [W, 2W] can be written w = v·d with d ∈ [W^{1/3}, W^{2/3}]
     (standard divisor-splitting of smooth numbers!) — then for counting failures at p:
     w = p^e·(v): v is W^{1/3}-smooth of size W/p^e: split v = v'·d with d ∈ [D, 2D-ish
     any target range ≤ v^{...}]: v⁸ = v'⁸·d⁸: for FIXED (p, v'): d ranges over the
     divisor-parts — NOT an interval nor equidistributed for free... the standard smooth-
     number bilinear decomposition (Vaughan's for smooth numbers: type-II sums): Σ_{v
     smooth ~ V} f(v) = Σ_{d ~ D} Σ_{v' ~ V/D} a_d b_{v'} f(dv') + ...: TYPE-II bilinear
     with COEFFICIENTS: then |Σ Σ a b e(α(dv')⁸)| ≤ (bilinear Weyl: double large sieve /
     Vinogradov-type): degree-8 monomial bilinear sums: |Σ_d Σ_v e(α d⁸ v⁸)|: this is
     EXACTLY a "Type II Weyl sum" bounded by classical methods (double large sieve gives
     savings for α = a/q, q ∈ [V^{δ}, (DV)^{8−δ}]) — YES this is standard Vinogradov-
     style and AVOIDS needing named smooth-Weyl theorems: prove a self-contained bilinear
     lemma L6' with the double large sieve (Bombieri–Iwaniec) or even simpler Weyl-van der
     Corput + Cauchy–Schwarz in d. FEASIBLE and self-contained. ⟹ ADOPT: L6' bilinear
     version; L7 counts failures within smooth v via the bilinear decomposition.
     COST: constants weaken (savings V^{−c'} smaller) — irrelevant (errors are o(1)-level).
     TO VERIFY: smooth numbers admit the needed factorization d ∈ [D, 2D] with D chosen
     ≈ V^{1/2}: standard (any smooth number has a divisor in any dyadic window below it
     — since prime factors ≤ V^{1/3}: greedy: YES classical lemma, prove inline).
     Bookkeeping: the b_{v'} coefficients absorb the smooth-structure: upper-bound
     failure-count = Σ over smooth v with digit-condition: 1_condition(v⁸) expanded in
     characters: Σ_a c_a Σ_{v smooth} e(a v⁸/p^t): smooth-sum bounded bilinearly. ✓

L11 [ ] Conclusion. |F_good(W)| ≥ (c₁ − Σbudget·c₁-relative...) — with Option D'/F budget
   RESTATED relative to the smooth base: all failure counts L7–L9 must be proved as
   ≤ ε·|F(W)| with Σε < 1. For L8/L9 (conditions on w±1, w^{2^j}+1: moduli ≤ W^{small}):
   smooth-w-in-progressions needed TOO?!? — w ≡ 1 mod p with w smooth: modulus p up to 2W:
   SAME smooth-AP problem!!! ⟹ those too must go through the bilinear route: w = d·v
   splitting inside the count of {w smooth: w ≡ 1 (p), digit-conds}: bilinear congruence
   sums Σ_d Σ_v 1_{dv ≡ 1 (p)}·(digit): Kloosterman-ish/large-sieve counts: for the (a)
   zone (pure w ≡ 1 mod p, p ~ W^{0.9}): #{smooth w ≡ 1 (p)} on average over p: Σ_p (this)
   = #{(w smooth, p): p | w−1, p ~ P}: = Σ_{w smooth} #{p ~ P: p | w−1} ≤ Σ_{w smooth} 1
   [at most one such p]: · (fraction of smooth w with SOME factor of w−1 in zone):
   BUT that's what we're bounding — circular; correct: Σ_p #{w ∈ [W,2W]: p | w−1} counts
   PAIRS without smoothness: pairs ≤ (log(9/8))·W: smooth-w pairs ≤ pairs: ⟹ #(smooth w
   lost in zone (a)) ≤ 0.118·W: compare to base c₁W with c₁ = ρ(3)·(class factor):
   0.118/ρ(3) ≈ 2.4 ≫ 1 — SAME RELATIVE-BUDGET BREAK. ***CONCLUSION: EVERY source count
   must be conditioned on smooth w — the anatomy of w−1 for SMOOTH w.*** The bilinear
   route covers digit-conditions but the plain divisibility p | w−1 within smooth w at
   p ~ W^{0.9}: #{w smooth ∈ [W,2W]: w ≡ 1 mod p}: bilinear: w = dv (d ~ D any window):
   dv ≡ 1 (p): for each d: v ≡ d^{−1} (p): v-count: |v-interval|/p + O(1): Σ_d: (W/p)·
   (d-multiplicity issues: overcounting via multiple splittings — use a NORMALIZED
   splitting (unique d = product of smallest primes till ∈ [D, 2D])): ⟹ #{w smooth:
   p | w−1} ≤ Σ_{d ∈ D-window, d smooth-part-admissible} (V/p + O(1)) ≈ (W/p)·(splitting
   overhead 1) + O(#d-values): #d-values ~ D = W^{1/2}: O-term Σ_p W^{1/2}·π(W^{0.9})
   → junk: need D-window small... p ~ W^{0.9} ≫ v-interval W/D = W^{1/2}: v ≡ d^{−1}
   (p): ≤ 1 + W^{1/2}/p solutions: Σ_d (1 + ...) ≈ #d-values = huge?? each (d, v) pair
   with dv ≡ 1 (p): total pairs over d ~ W^{1/2}: Σ_d #{v: ...} = #{(d, v): dv ≡ 1 (p)}
   ≈ W/p·(divisor-ish) — Kloosterman equidistribution of the hyperbola mod p: #{(d, v) ∈
   box: dv ≡ 1 (p)} = box-area/p + O(p^{1/2}log²p) (Kloosterman/Weil ✓ classical!):
   = W/p + O(W^{0.45+}): Σ over p ~ W^{0.9}: main Σ W/p ✓ 0.118·(smooth-relative?? NO —
   this counts smooth w × (multiplicity of splittings) ≥ #smooth-w-hit — as an UPPER
   bound with unique-splitting normalization: = #{smooth w ≡ 1 (p)} EXACTLY (each smooth
   w has exactly one normalized splitting) = W/p·(density of pairs...) hmm the pairs (d,v)
   from normalized splittings of smooth numbers are a SUBSET of the full box-hyperbola
   count: upper bound = full count W/p + O(W^{0.45}): but W/p is the NON-smooth-relative
   count: ratio to smooth base: W/p/(ρ(3)W·...) — SAME 1/ρ INFLATION. To win we need the
   SMOOTH count ≈ ρ·W/p i.e. equidistribution of smooth w in the single class mod p ~
   W^{0.9}: strictly beyond unconditional knowledge (even on average this is at the edge).
   ⟹⟹ STRATEGIC RESOLUTION: avoid needing smooth w at all: RETUNE THE FAMILY: replace
   "P(w) ≤ w^{1/3}" by "w has NO prime factor in (W^{α}, W^{1/2}]" with... the purpose of
   smoothness was ONLY to kill w-source certain-fails at β ∈ (1/3, 1]. What the w-source
   REALLY needs: no prime factor with β > β* ≈ 0.47 (where D(β) < 9 digits make failure
   near-certain), and countable failures below. Weakest usable family restriction:
   "P(w) ≤ W^{0.45}" (u = 2.22: ρ(2.22) ≈ 0.22): relative budget denominators improve
   (1/ρ = 4.5): still E/ρ ≥ ... zone-(a) 0.118/0.22 = 0.53 ✓ FITS!!! Let me recompute all
   relative budgets with ρ = ρ(1/0.45) = ρ(2.22) ≈ 0.2–0.25: (a) 0.118/0.22 ≈ 0.53;
   (b)+(c) ≈ 0.09/0.22 ≈ 0.41 hmm 0.53+0.41 > 0.94 + w-source + L9... OVER 1 AGAIN.
   *** Unless the failure counts are themselves ∝ smooth-base (true but unprovable) ***
   RESOLUTION OPTIONS: (α) prove smooth-AP on AVERAGE over p (Bombieri–Vinogradov for
   smooth numbers — Harper 2012s: EXISTS! moduli to x^{1/2−ε} on average — our zone-(a)
   p ~ W^{0.9} EXCEEDS x^{1/2}; Drappeau/Fouvry-type dispersion for smooth to x^{3/5+}? —
   still < 0.9); (β) restructure so all condition-moduli ≤ W^{1/2−ε} and use average-
   smooth-AP (Harper): the offending moduli are w∓1-factors p > W^{1/2}: their conditions
   (J = 1) ARE simple: can we AUTO-PASS them?: w−1's factors p ∈ (W^{1/2}, W^{8/9}):
   D(β) = 8/β − 1 ∈ [8, 15) digits available: failure prob ~ 2^{−D} ≤ 2^{−8}: TRUE failure
   mass over the whole zone ≈ ∫_{1/2}^{8/9} 2^{−(8/β−1)}dβ/β ≈ 0.004 — TINY: it's only
   the COUNTING that forced the Mertens-loss, not reality. For these p the digit conditions
   live at moduli p^{1+t}: p ≤ W^{8/9}, need t ~ 8: p^{9} ~ W^{8}: Weyl over w-interval
   fine (W-length vs modulus ≤ W^{8−δ} ✓!!): #{w ∈ CLASS ∩ [W, 2W]: w ≡ 1 (p), digit-fail}
   ≤ Weyl-count over FULL w-interval (drop smoothness: (W/p^{J})·μ(G) + error): relative
   inflation 1/ρ ≈ 4.5×: Σ ≈ 4.5·0.004 ≈ 0.02 ✓✓ NEGLIGIBLE!! ⟹ the expensive Mertens-loss
   is ONLY needed where failure is CERTAIN-ish (no digits to inspect): p > c·W^{8/9}
   (D(β) ≤ 8 = demand: μ(G) ≈ 1): there ONLY the (a)-Mertens loss applies: 0.118/ρ(2.22)
   ≈ 0.53. Hmm — 0.53 JUST for that zone. REDUCE: shrink the certain-zone: demand at
   p ∥ w−1 is J = 1... wait NO!!! RECHECK: what exactly is demanded at p ∥ w−1, p ~ W^{0.9}:
   J = 1: κ_p(⌊m/p⌋) ≥ 1: ⌊m/p⌋ = ⌊w⁸/p⌋ ~ W^{7.1}: D = 7.9/0.9 ≈ 8.8 digits: failure =
   NO carry among ~8 digits ≈ 2^{−8}: NOT certain at all!!! Where did "certain-fail at
   p > W^{8/9}" come from?? From the BINOMIAL structure: w = ap+1: w⁸ = Σ C(8,i)a^i p^i:
   for a⁸ < p (β > 8/9): digits ARE the C(8,i)a^i: all < p/2 unless C(8,i)a^i ≥ p/2 for
   some i: for a⁸ ≪ p: 70a⁴ ≪ p^{...}: hmm a⁸ < p ⟹ a⁴ < p^{1/2} ⟹ 70a⁴ < p/2 for p >
   19600: ALL digits small: κ = 0: CERTAIN FAIL ✓ (that's the structure — the ~8.8 "digits"
   are NOT random: they are binomial coefficients!). So certain-zone = {β: a⁸ < p·c} =
   β > 8/9 STRUCTURAL ✓ as scanned (D=8: 152/190 fail ✓). ⟹ zone (8/9, 1]: RELATIVE cost
   0.118/ρ: with ρ(2.22) ≈ 0.22: 0.53. With ρ(2) = 0.3069 (θ_s = 1/2): 0.118/0.3069 =
   0.385; θ_s = 1/2 in turn re-opens w-source certain-fails at β ∈ (0.47, 0.5]: NO WAIT
   w-source demand-8-certainfail: D(β) = 8/β − 8 < 8+1 ⟹ 8/β < 17 ⟹ β > 8/17 ≈ 0.47:
   zone (0.47, 0.5]: weight log(0.5/0.47) ≈ 0.062: relative 0.062/0.307 ≈ 0.20 — plus
   probabilistic β < 0.47 contributions relative-inflated 1/ρ×(true ≈ small)...
   RELATIVE BUDGET @ θ_s = 1/2: w−1-certain 0.385 + w-source-certain 0.20 + (all
   probabilistic zones ≈ (1/ρ)·0.02-ish ≈ 0.07) + L9-sources (BT-constants ×(1/ρ)):
   true w⁴+1 mass ≈ 0.05·2(BT)·(1/0.307) ≈ 0.33?? hmm w⁴+1-真 ≈ 0.05: ×2 sieve × 3.3
   relative ≈ 0.33 + w²+1 similar smaller ≈ 0.1: TOTAL ≈ 0.385+0.20+0.07+0.43 ≈ 1.09 —
   MARGINALLY OVER. Squeeze options: (1) prove L8+ minus-shift auto-pass (already only
   w−1 counted ✓ included); (2) shrink w−1-certain zone: at β ∈ (8/9, 1): digits are
   C(8,i)a^i: fail is certain ONLY if also position-8-and-up digits (the a⁸ ≥ p case
   boundary) ... at a⁸ ≥ p (β < 8/9) top digits randomize; the certain zone is genuinely
   log(9/8). BUT the class mod Q₀!!! w ≡ c₀ (Q₀), c₀ ≢ 1: does p | w−1 constrain?: no.
   (3) HYBRID demand: at p ∥ w−1 in the certain zone the demand is κ_p(⌊m/p⌋) ≥ 1:
   carries can ALSO come from digit positions BELOW 8 in ⌊m/p⌋-terms?? recompute: m = w⁸,
   digits (1, 8a, 28a², ..., a⁸): ⌊m/p⌋ digits: (8a, 28a², ..., a⁸): doubling: 16a, 56a²,
   ...: carry iff some 2·C(8,i)a^i ≥ p: for a⁸ < p/2: 2a⁸ < p and all lower: certain fail
   ✓ zone stands. (4) MOVE THE FAMILY: kill w−1's large primes STRUCTURALLY by w = s²
   (hexadecic m = s^{16}): w−1 = (s−1)(s+1): certain zone moves to s∓1 factors > s^{16/17}:
   Mertens log(17/16) ≈ 0.0606 (only s−1 if minus-shift-lemma proved: s+1 safe): relative
   0.0606/ρ(2) = 0.20: w-source→s-source demand 16: certain-fail β_s > 16/33 ≈ 0.485:
   zone (0.485, 0.5]: log(0.5/0.485) = 0.03: relative 0.10: s^{2^j}+1 sources j = 1..3:
   MORE sources but each tiny: total L9-ish ≈ 0.35·?? — recompute during drafting;
   ESTIMATED TOTAL ≈ 0.20 + 0.10 + 0.10 + 0.35 ≈ 0.75 < 1 ✓ WITH ROOM. ⟹ ADOPT HEXADECIC
   m = s^{16}, n = s^{16} − 2, θ_s = 1/2 (family: s ∈ [S, 2S], s ≡ c₀ (Q₀), P(s) ≤ s^{1/2}).
   Everything above re-instantiates with 16 in place of 8. RE-CALIBRATE NUMERICALLY FIRST.

## Verdict of this skeleton pass
The proof architecture is: family {s^{16} − 2}, smooth-restricted parameter, finite small-
prime certificate, Mertens-loss only in structural certain-fail zones, Weyl/bilinear digit
counting elsewhere, Richert sieve for the s^{2^j}+1 sources, first moment relative to the
smooth base, Markov. REMAINING RISKS: (i) the relative-budget arithmetic must be redone
carefully with hexadecic numbers and REAL constants; (ii) bilinear/smooth-Weyl needed
wherever a digit-count must be conditioned on smooth s — CHECK: with the Mertens-losses
taken UNconditionally (relative-inflated), the remaining probabilistic counts can ALSO be
taken unconditionally (drop smoothness in upper bounds — inflates by 1/ρ(2) ≈ 3.26 —
budget above already used that). So NO smooth-AP/bilinear tool needed at all?! VERIFY in
drafting: every failure-count upper bound drops smoothness; every budget line is
(unconditional count)/(ρ(2)-relative base). If the arithmetic closes < 1, the proof needs
ONLY: Kummer/Legendre, Mertens, Dickman-in-fixed-AP (base), degree-16 Weyl + digit-box
Fourier, Richert Thm 11.4, ρ_d(a)-averages, finite certificates. ALL CLASSICAL. Next:
hexadecic_scan.py; then budget tables; then lemma drafts.
