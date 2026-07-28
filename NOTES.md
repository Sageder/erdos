# NOTES.md — lab notebook (newest entries at top)

## 2026-07-28 ~11:25 UTC — R13 verdict: TWO of my claims overturned; target re-scoped; new lead

- R13 obtained Hildebrand 1985 IN FULL (AMS open archive) and reconstructed it, plus
  Tao–Teräväinen arXiv:2512.01739 and Teräväinen 2018 (NEITHER was in the R11 sweep).
- **L0 — MY RESIDUAL TARGET WAS FALSE.** "Positive density with C_ℓ at every large prime" has
  density ≍ (log x)^{−1/2}: C_ℓ pins the carry to digit position 1 (~1/2 per prime) across
  ~log log x primes. I VERIFIED THIS MYSELF (experiments/verify_L0_rescope.py):
  among n^{1/2}-smooth pairs, all-C_ℓ = 0.0119 → 0.0110 → 0.0107 (decaying) while the EXACT
  criterion = 0.1029 → 0.1089 → 0.1058 (stable); at b = 0.35, exact = 0.18–0.24, all-C_ℓ = 0.004.
  ⟹ target restated with the EXACT criterion κ_ℓ(n) ≥ 2ν_ℓ(n+j) and b a FREE KNOB
  (failure prob per prime ≲ 2^{−1/b}). My own LADDER §4.5 remark (iii) already said C_ℓ is
  sufficient-not-necessary (45/263 coverage) — I then mis-stated the target anyway. Lesson:
  restate targets from the exact criterion, never from a sufficient proxy.
- **Supply threshold mis-instantiated.** Hildebrand's k-string hypothesis is on the DENSITY
  (d(A) > (k−2)/(k−1)) — for k=2 that is just d(A) > 0, so ANY b > 0 gives positive density of
  consecutive n^b-smooth pairs. My "e^{−1/(k−1)} = 0.368 for k=2" line was wrong (that formula
  uses ρ(u) = 1 − log u, valid only u ≤ 2). Corrected in LADDER §6.
- **Stable-set injection: definitively NO.** p-stability (the sole hypothesis of the whole
  Hildebrand 85/89 / Balog–Ruzsa / Heath-Brown family) is MAXIMALLY violated by carry
  conditions: dilation permutes a cofactor residue condition. Measured agreement of the
  condition at n vs at 2n = 0.5037, where stability requires 1. Not fixable by strengthening
  any lemma — the hypothesis IS the obstruction; closing under dilations ≤ N costs e^{−N}
  against a tower-sized N(ε).
- **NEW LEAD ROUTE (character change).** Tao–Teräväinen 2512.01739 Thm 3.1 carries the AP
  restriction 1_{n≡b (W)} FREE in the published statement ⟹ L1 (congruence-restricted
  consecutive smooth pairs) is hard-but-classical, essentially available. Decomposition:
  L1 (available) + L2, L3 (routine) + L4 (THE WALL: joint cofactor/carry equidistribution).
  Crucially L4 is NOT a parity problem and NOT a bilinear-prime problem — no prime is detected,
  the smooth supply is unconditional; all moduli ℓ² ≤ x^{2b} ≪ x^{1/2} are inside BV range.
  Open parts: modulus is a function of n; ~log log x simultaneous conditions; the weight is not
  multiplicative (so not an admissible g₂ in Thm 3.1). L4a (single largest prime factor) is the
  concrete first target — R14 LAUNCHED on it.
- **k ≥ 3**: gap is now EXPLICIT AND SMALL: need α = 1/2; known α > e^{−1/2} = 0.6065
  (Hildebrand 89), α > e^{−2/3} = 0.5134 (Tao–Teräväinen short-interval-uniform). McNamara
  arXiv:2312.08544 gives a stable set of density exactly 1/2 with no 3-string ⟹ the soft /
  stable-set route CANNOT reach 1/2 at all. Frontier = the interval 0.5134 → 0.5, non-softly.
- Lemma SP audit repairs R1–R4 applied (R2 was a genuinely false illustrative claim: W₂ ≥ 15
  asserted, true min 14, violated by 489/977; R4: T13 row mislabelled — auditor re-ran at
  hypothesis-compliant scales of 181–2496 digits, zero violations).
- Statement B route superseded as lead: it needs prime detection, L1–L4 does not.

## 2026-07-28 ~10:50 UTC — MIRROR THEOREM (proved+verified) + crux experiment verdict

- CRUX EXPERIMENT (experiments/crux_equidistribution.py, n ≤ 3e5, exhaustive):
  * 98.96% of ALL n fail some per-prime condition ⟹ any first-moment/union bound taken over
    all n is WORTHLESS against the ρ(2)²≈9.4% smooth set. (Rigorous kill of the "subtract
    failures unconditionally" strategy — this is why every power-family budget collapsed.)
  * smooth-window density measured 9.373% ≈ ρ(2)² (the two smoothness events are independent).
  * membership | smooth window = 11.05%; | n^{1/3}-smooth window = 11.64% (NOT better — more
    digits per prime is exactly cancelled by more primes: raising smoothness does not help).
  * per-prime pass rates match the corrected digit model (top digit ~n/ℓ^{D-1} is too small to
    carry ⟹ usable positions = 1/β − 1, not 1/β).
  * NON-INDEPENDENCE MEASURED: P(all pass | smooth) = 0.1105 vs product model 0.3297
    (ratio 0.335) ⟹ conditions are positively correlated in failure; independence heuristics
    overstate the target 3×. Any injection proof must handle this.
  * No AP obstruction (n ≡ 7 mod 24 gives 10.18%, same ballpark).
- MIRROR THEOREM (MIRROR.md; proved elementarily, verified M1–M5 all PASS):
  In the m = n+k variable BOTH 727 and the solved siblings ask "does a product of consecutive
  integers divide C(2m,m)?" with the SAME supply κ_p(m). The difference is only WHERE the
  divisor block sits, and a digit trichotomy for p > 2k decides everything:
    TYPE A  m ≡ −i (mod p^J): digits p−i, p−1, …  ALL LARGE ⟹ J carries FREE   [728/729/401]
    TYPE B  2m ≡ odd i:       digits (p+i)/2, (p−1)/2, … ⟹ J carries FREE      [727 odd slots]
    TYPE C  m ≡ +i (mod p^J): digits i, 0, 0, …  ALL SMALL ⟹ ZERO low carries  [727 even slots]
  727's block {2m,…,2m−2k+1} splits: odd slots = type B (free), even slots 2(m−i) = type C.
  The siblings' block {m+1,…,m+k} is entirely type A (free). Same shape, mirrored location,
  inverted digit pattern. THIS is why Jan-2026 carry-engineering closed 728/729/401 and not 727.
  Corollaries (proved): (a) the √(2n)-smoothness of the window is not an extra hypothesis but
  the type-C carry-room inequality p^{2J} ≲ 2m (M5: zero violations); (b) the residual content
  is exactly the cofactor congruence C_p of Lemma R‴.
- CONSOLIDATED LOCALIZATION: small primes DONE (Lemma SP, proved, AP-uniform, density 1);
  large primes DONE given C_p (Lemma R‴, proved); remaining = one statement: infinitely many n
  with √(2n)-smooth window AND all cofactor congruences. For k=2 the smooth supply is KNOWN
  (Hildebrand 1985 = Balog's conjecture, positive density); for k ≥ 3 the supply itself is open
  (positive-density k-strings need α > e^{−1/(k−1)} > 1/2). Injection blocked by the measured
  correlation obstruction above + R11's parity/balancedness barrier.
- Resources: Fable-5 credits exhausted mid-run; session switched to Opus. Audits + R13 anatomy
  relaunched under Opus (wf_0d0ea0f6-516).

## 2026-07-28 ~06:30 UTC — Wave-1 complete: MASTER LEMMA SP proved; S_2..S_6 to 1e8; R3 reproduced

- R2 delivered MASTER LEMMA SP (attempts/route-R2/LEMMA_SP.md), FULLY PROVED, explicit
  constants, verified 40/40 (incl. 2e4-sample checks at M = 2^64, 2^200, 10^60 in APs):
  for fixed k, all but 18·exp(−√(log M)/120) of m in [M,2M] — uniformly in EVERY AP of
  modulus q0 ≤ M^{1/10} — satisfy the exact 727 criterion at every p ≤ exp(√(log M)/6),
  plus spike bounds and a per-prime surplus (log M/log p)/120. AP-specific discoveries:
  naive spike bound FALSE in APs (needs ν_p(2q0) correction); carries counted on masked
  positions [ν_p(q0), L_p). HARD BARRIER (documented): this counting cannot reach
  p > exp(c√log M); AP moduli beyond M^{1/8} need new ideas.
  ⟹ For any future family argument: small primes are DONE via SP; the fight is entirely
  at p ∈ (exp(c√log M), √(2n)] — consistent with the triangle analysis.
- R3 rerun independently reproduced FAMILY.md/BREAKAGE.md conclusions (same family, same
  Lemma R, same Statement B; falsified hexagonal folklore; Pell square-parametrization
  carry-deficit confirmed). Good reproducibility.
- R5: complete exact S_k on [1, 1e8), k = 2..6, in 250 s (segmented rough-remainder sieve
  + vectorized digit checks; validated vs PROBLEM.md tables):
  |S_2| = 1,364,676; |S_3| = 139,975; |S_4| = 13,188; |S_5| = 1,012; |S_6| = 63;
  min S_5 = 252,965; min S_6 = 3,648,835. Per-decade densities slowly INCREASING for all
  k ≤ 6 (log-log slopes 1.04–1.45); NO forbidden congruence classes (mod 2..27, 5..);
  x²−2 family NOT enriched (120 hits vs 136.5 expected — slight deficit, consistent with
  the auto-fail structure); slot-of-max-LPF uniform. NO branch: data-disfavored ≤ 1e8.
- R7/R9 (wave-1) + R10 (wave-2) + R13 (anatomy) all died at session limit (reset 5:40 UTC,
  now past); relaunching all four now. R7 left verify_members.py (committed).

## 2026-07-28 ~02:00 UTC — R11 literature verdict; Lemma R‴; new flagship = Hildebrand injection

- LEMMA R‴ proved+verified (0 false positives, all even n ≤ 6e4): small-prime demands +
  squarefree rough parts + per-large-prime residue condition C_ℓ:
  ((n+j)/ℓ − 1) mod ℓ ≥ (ℓ−1)/2 ⟹ n ∈ S_k. Subsumes Lemma R_k (boxes just force C_ℓ).
  LADDER.md §4.5–4.6 has it + the "difficulty triangle".
- R11 (attempts/route-R11/LITERATURE.md, 8 items, citations verified):
  * NO published result implies Statement B (four-prime pq+1=2rs): it stacks archimedean
    windows (fine) + BALANCED E₂ (every published detector needs UNBALANCED E₂ per GGPY
    (1.24)) + double specified parity (open even for Chen's 2p+1 branch). The equation
    literature (item 5) is empty of lower bounds — "parity-squared".
  * KEY STRUCTURAL IRONY: published tuple detectors (GGPY Thm 3 on {m, 2m−1}: consecutive
    N ∈ P₂, N+1 = 2P₂, factors > N^{1/10}) produce only UNBALANCED E₂'s — and unbalanced
    means a factor > √(2n), which 727-membership FORBIDS. Parity meets balancedness exactly
    at the membership boundary.
  * GAME-CHANGER: Hildebrand 1985 (Proc AMS 95, "On a conjecture of Balog") — POSITIVE
    LOWER DENSITY of {n: P(n) ∈ (n^a, n^b) ∧ P(n+1) ∈ (·)} for ANY 0 ≤ a < b ≤ 1; also
    Balog–Ruzsa 1995/97 (stable sets): positive density with n, an+c both n^β-smooth.
    ⟹ consecutive-√-smooth supply at POSITIVE DENSITY is KNOWN — corner (i) of the
    triangle is not smoothness-blocked; the entire k=2 residual = C_ℓ conditions along
    Hildebrand-type sets.
  * My budget analysis: unconditional subtraction of C_ℓ-failures fails (top-band moduli
    cap the digit-truncation: subtraction ~0.3–0.4 vs base density ρ(2)²·c ~ 0.05): the
    C_ℓ conditions MUST be counted/injected INSIDE the Hildebrand/Balog–Ruzsa/Heath-Brown
    machinery. R11 reached the same conclusion independently ("residual difficulty...
    equidistribution of digit conditions in Heath-Brown-type constructions").
- LAUNCHED R13: obtain + dissect Hildebrand 1985, Balog–Ruzsa, Heath-Brown 1987,
  Hildebrand 1989; verdict on injectability of AP-restriction + C_ℓ conditions.
- Statement B (pure four-prime) reclassified: blocked at current technology (keep as the
  clean formal target it is; the R‴/Hildebrand path is now the flagship for k=2).

## 2026-07-28 ~01:20 UTC — STRATEGIC MERGE: Lemma R supersedes power families for k=2

- Wave-1 died at session limit but R3 delivered before dying: FAMILY.md (complete re-proof of
  Balakran: F = {pq−1: (3q+1)/2 ≤ p ≤ 2q−1} ⊆ S_1 via 2 forced carries at p and q;
  infinitude via Nagura) and BREAKAGE.md (k=2 failure taxonomy + LEMMA R + LEMMA Q).
- LEMMA R (elementary, complete proof, verified on 123/123 solutions): primes q,p,s,r with
  pq+1 = 2rs, (3q+1)/2 ≤ p ≤ 2q−1, 2s+1 ≤ r ≤ 4s−1, 2r mod s ≥ (s+1)/2, n = pq−1 not a
  2-power ⟹ n ∈ S_2. NO probabilistic mid-range — every prime of (n+1)(n+2) is a parameter
  with hand-forced carries. Missing ingredient = STATEMENT B: infinitude of such quadruples.
- I verified: condition 4 is ARCHIMEDEAN: r/s ∈ [9/4,5/2)∪[11/4,3)∪[13/4,7/2)∪[15/4,4).
  So Statement B = solutions of pq − 2rs = −1, four primes, ratio boxes. Frontier analytic
  number theory (dispersion/BFI/Harman; adjacent: Chen 2p+1=P_2, Heath-Brown consecutive
  almost-primes, GGPY E_2 machinery, Motohashi BV-for-E_2, Titchmarsh for pq+1).
- LEMMA Q (R3): consecutive-splitting polynomial identities force a square on one side;
  squares double valuations past digit supply. EXPLAINS why quartic/octic/hexadecic budgets
  kept failing (my independent hexadecic-budget analysis reached the same wall from the
  analytic side: no (2^r, theta) closes unconditionally). Power-family route R1 → SUPERSEDED.
- First-moment over the RAW {pq−1} family genuinely fails (true E ≈ 2 > 1, measured 11.7%
  survival) — structure on n+2 is NECESSARY, not an artifact of lossy bounds.
- General k: Lemma R generalizes to k−1 simultaneous equations (much harder); the t-factor
  relaxation (n+2 = 2r_1..r_t) trades equation-hardness against digit-freedom.
- NEXT: R11 literature route (consecutive almost-primes / E_2 levels / pq+1 technology);
  then Statement-B attack plan; independent re-verification of Lemma R (audit-grade).

## 2026-07-27 ~23:40 UTC — Prop N verified; quartic→octic calibration; K2 program viable

- Prop N (master reduction) + Lemma O VERIFIED (attempts/route-R1/verify_propN.py: PASS,
  brute force k=2,3 to 3e4; 2e4 random Lemma-O cases).
- Quartic scan (n = z^4−2, z in [1e3, 9e3]): density 1.2% overall, 19.9% among sqrt-smooth z
  with p<=13 ignored. E[#fail] = 1.19. CORRECTION to Discovery 2: the +1-shift danger is NOT
  fixed by z = x^2 — binomial digits of (ap+1)^4 = (a^4, 4a^3, 6a^2, 4a, 1) are all < p/2
  when a^4 < p: primes p | z−1 with p > z^{2/3}-ish are near-certain failures (measured 94%
  at D=4). ASYMMETRY CONFIRMED: (ap−1)^{even} patterns are safe (z+1 source: ~0 failures).
- OCTIC FIX: m = w^8, n = w^8−2: window {w^8−1, w^8}, w^8−1 = (w−1)(w+1)(w^2+1)(w^4+1):
  the z−1 danger inherits only from w−1's factors > w^{8/9} (Dickman weight log(9/8)=0.118).
  Octic scan (w in [300, 4200], theta=0.42, P0=13): conditional density 48.15%,
  TOTAL E = 0.63 < 1 (w: 0.33 [cut to ~0.07 with theta=1/3], w−1: 0.25 [asymp ~0.12,
  small-sample inflated], w4+1: 0.05, w+1/w2+1: ZERO across all exposures).
  ASYMPTOTIC BUDGET ≈ 0.25 << 1 ⟹ first-moment + Markov strategy is empirically SOLID.
- Small-prime engineering at p ≤ 13 reduces to FINITE existence checks: at p=7,11,13 choose
  w mod p avoiding the ≤8 roots of w^8=1 (no condition at all); p=5 forced (w^8≡1 mod 5
  always) — engineer J=1 via w mod 25 + one carry via digits of w^8 mod 5^L; p=2,3 similar
  explicit classes. All machine-checkable.
- DECISION: proof target = "S_2 infinite via octic family + first moment". Tools: Dickman-in-
  fixed-AP (base count), exact AP counting (w−1 zone), quartic/octic Weyl mod p^t (w-source
  digit cylinders), divisor-switch + Selberg upper (w^4+1 source), finite checks (p ≤ P0).
  Wave-2 agent R8 is verifying the exact citable forms in parallel.
- Waves running: wave1 = R2 (Lemma SP), R3 (Balakran), R5 (big sieve), R7 (NO-side),
  R9 (digit dynamics); wave2 = R8 (toolbox), R10 (headline/general-k BW injection).

## 2026-07-27 ~22:20 UTC — Aristotle-728 paper digested; structural discoveries (TO VERIFY NUMERICALLY)

Paper (arXiv 2601.07421 v5, Sothanaphan): proves log-gap 728 via reduction to
C(m+k,k) | C(2m,m), i.e. per prime W_p(m,k) ≤ κ_p(m) + ν_p(k!), where κ_p(m) = ν_p(C(2m,m)) =
carries doubling m base p, W_p = ν_p((m+1)···(m+k)), V_p = max_i ν_p(m+i). Their machinery:
 - Lemma 4: W_p ≤ ν_p(k!) + V_p (so only spikes V_p matter — the k! slack is why 728 is easier).
 - Lemma 5: p > 2k FREE: p^J | m+i, i≤k<p/2 ⟹ lowest J digits of m are top-heavy (p−i, p−1,...)
   ⟹ J forced carries. [KEY ASYMMETRY vs 727: our window ends AT 2m, no slack, see below.]
 - Lemmas 6–14: for p ≤ 2k force X_p(m) = #{first L_p digits ≥ ⌈p/2⌉} ≥ µ_p/2 via
   Chernoff + residue-class counting in [M,2M]; spikes excluded via V_p < J_p + t(M),
   t(M) ~ 10 log log M. Union bound |Bad| < M.
 - Lemma 15/Theorem 3 (appendix): carry Markov chain, P(S_L ≤ (1−δ)L/2) ≤ C e^{−I(δ)L};
   density-1 of m with κ_p(m) ≥ (1−δ)/2 · log m/log p for ALL p ≤ exp(c√log m), spike-free.
   This is the strongest reusable block. NOTE Prop 1 (optimality): uses s₂(m) ≤ (1/2+ε)log₂m a.e.

727 in the same normal form (verified equivalent in verify_identities.py, pending):
  n ∈ S_k ⟺ ∀p: κ_p(m) ≥ W'_p(m) := ν_p((2m)(2m−1)···(2m−2k+1)), m = n+k.
Differences from 728: window at the TOP (ends at 2m), no ν_p(k!) rescue. Consequences:
 (a) For p > 2k, at most one window multiple; ODD-position multiples (2m−odd) force their own
     carries (top-heavy residues — Lemma-5-style, rederived for subtraction side): FREE.
     EVEN positions 2(n+j): p^ν ∥ n+j puts digits of (k−j) at bottom of m: NO low carries;
     need ν carries from digits ≥ position ν. For p > √(2m)-ish: impossible ⟹ smoothness
     of window n+1..n+k at threshold √(2n) is NECESSARY (matches PROBLEM.md).
 (b) Small primes p ≤ 2k: need κ_p ≥ ~2k/(p−1) + spikes: EXACTLY the 728 carry-rich counting,
     with demands O_k(1) — for FIXED k the digit depth needed is O_k(1): positive-density
     conditions. Port of Lemmas 6–14 gives: all p ≤ P₀ conditions hold for positive proportion
     of m ∈ [M,2M] (any fixed P₀, or even P(m) growing with density 1 per Theorem 3 analog).

DISCOVERY 1 (k=2 ansatz sharpening; MUST TEST): for n = X²−2 (m = X², window {X²−1, X²}):
 - q ∥ X−1 with 2(X−1)² < q³ ⟹ digits of X² base q are (a², 2a, 1), a=(X−1)/q < √(q/2)
   ⟹ ZERO carries ⟹ AUTO-FAIL. So P(X−1) ≲ 1.26·X^{2/3} is NECESSARY along the ansatz.
 - q ∥ X+1, q³ > ~2X²: digits (a²−1, q−2a, 1), q−2a > q/2 ⟹ carry AUTO-PASS. (Asymmetry!)
 - q ∥ X, q > X^{2/3}: m = (v², 0, 0) base q, need 2 carries, at most 1 available ⟹ AUTO-FAIL:
   P(X) ≤ X^{2/3} NECESSARY.
DISCOVERY 2 (quartic fix): X = z² kills both auto-fail thresholds STRUCTURALLY:
   X−1 = (z−1)(z+1) has P ≤ z+1 ~ X^{1/2}; P(X) = P(z) ≤ X^{1/2}. So along n = z⁴−2 every
   auto-fail source vanishes; all remaining per-prime conditions are probabilistic with ≥3–4
   digit room. First-moment heuristic: E[#failing primes per z] plausibly < 1 ⟹ Markov gives
   positive proportion of z with z⁴−2 ∈ S₂ ⟹ S₂ infinite. Counting needs only equidistribution
   of z (FULL integer parameter — no sparse-family averaging problem!) in residue classes +
   Weyl-type bounds for z⁴ mod q^j. TOP PRIORITY: test empirical density of {z : z⁴−2 ∈ S₂}.
DISCOVERY 3 (k=3 supply EXISTS unconditionally): Pell equation y² − 2u² = −1 (inf. many sols),
   x = 2u: x²−2 = 2y². Window for n = x²−3: {x²−2, x²−1, x²} = {2y², (x−1)(x+1), x²}:
   all √(2n)-smooth! So the k=3 smooth-window supply is NOT blocked by open conjectures.
   (k=4 via same trick needs two simultaneous Pell conditions — finitely many expected;
   general-k supply still hinges on Balog–Wooley-type theorems — literature check pending.)
NO-side note: none of this excludes NO for large k; keep R7 alive.

NEXT: (1) numerics: verify Discoveries 1–3 + family densities + failure histograms by
β = log q/log X; (2) literature: exact Balog–Wooley statement; smooth numbers in APs ranges;
(3) launch route subagents; (4) big sieve S₂..S₆ to 10⁸.

## 2026-07-27 ~21:50 UTC — Session 1 start: pre-flight PASSED, setup

- Pre-flight per PROMPT §1: erdosproblems.com forum threads 403 bot-blocked (expected; operator
  manual browser check was the mandatory launch gate and this run was launched after it).
  My own checks: AI-contributions wiki (data through 2026-06-30) — NO mention of 727;
  teorth/erdosproblems problems.yaml fetched fresh from main — 727 status "open"
  (728 "proved", consistent with known Aristotle result; no news). No claim encountered
  anywhere. RUN PROCEEDS.
- Repo was empty (no commits). Wrote PROBLEM.md, ROUTES.md, this file, AUDITS.md stub.
- Observation recorded during setup (to verify computationally): the full per-prime condition
  compresses to the clean equivalent
      n ∈ S_k  ⟺  (2m)(2m-1)···(2m-2k+1) | C(2m, m),  m = n+k,
  because 2k - s_p(2k) = (p-1)·ν_p((2k)!) turns the deficit inequality into
  ν_p(C(2m,m)) ≥ ν_p(C(2m,2k)) + ν_p((2k)!) for every p. Balakran = k=1 case
  ((2m)(2m-1) | C(2m,m) i.o.). MUST be verified numerically before use.
- Balakran m-values (m = n+1): 6, 15, 28, 45, 66, 91, 153 are hexagonal j(2j-1), but 42, 77,
  110, 120-missing, 126, 140, 156, 170 break the pattern — dissect in R3.
- Next: calibration gate (reproduce §4 table), verify all §2 identities, then launch routes.
