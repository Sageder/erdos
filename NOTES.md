# NOTES.md — lab notebook (newest entries at top)

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
