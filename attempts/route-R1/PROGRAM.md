# Route R1 — Program K2: S_2 is infinite via the quartic ansatz (lead route, k=2 variant)

Status: program stage — every step listed with its tool; numerics must calibrate the
first-moment budget BEFORE proof investment. Nothing here is proved yet unless marked.

## Master reduction (Proposition N + Lemma O) — elementary, to be written up first

With m = n + k, n > 2k^2: n ∈ S_k iff
 (a) ∀ p ≤ 2k: κ_p(m) ≥ W'_p(m) = ν_p((2m)(2m−1)···(2m−2k+1));
 (b) ∀ p > 2k, ∀ j ∈ [1,k] with p | n+j: κ_p(⌊m/p^J⌋) ≥ J, where J = ν_p(n+j).
Proof ingredients:
 - For p > 2k at most one window element is divisible by p; odd-position elements
   (2m − odd i) force J carries automatically:
   LEMMA O: p odd prime, p > 2k ≥ i, i odd, p^J ∥ 2m − i ⟹ m mod p^J = (p^J + i)/2 has
   digits d_0 = (p+i)/2 ≥ ⌈p/2⌉, d_1..d_{J−1} = (p−1)/2; doubling chains J carries. □(drafted)
 - Even positions 2m − 2(k−j) = 2(n+j): m ≡ k−j mod p^J: digits of (k−j) then zeros:
   zero carries from bottom J digits, no carry into position J; κ_p(m) = κ_p(⌊m/p^J⌋). □(drafted)
STATUS: verify numerically (verify_propN.py), then write up.

## The family

Parameters: z ∈ [Z, 2Z], z ≡ c₀ (mod Q₀) (Q₀ = ∏_{p ≤ P₀} p^{L_p}, fixed), z is
z^{θ_s}-smooth with θ_s = 1/2 (possibly 0.45); n = z⁴ − 2, m = z⁴, k = 2.
Window: {n+1, n+2} = {z⁴−1, z⁴}; top window {2m−3, 2m−2, 2m−1, 2m}.
Conditions after Prop N (p ≥ 5; p = 2, 3 engineered via c₀ mod Q₀):
 - p^ν ∥ z  ⟹ need κ_p((z/p^ν)⁴) ≥ 4ν       [source 'z']
 - p^J ∥ z−1 ⟹ need κ_p(⌊z⁴/p^J⌋) ≥ J        [source 'z−1']
 - p^J ∥ z+1 ⟹ need κ_p(⌊z⁴/p^J⌋) ≥ J        [source 'z+1']
 - p^J ∥ z²+1 ⟹ need κ_p(⌊z⁴/p^J⌋) ≥ J       [source 'z²+1']
 - odd top-window elements 2z⁴−1, 2z⁴−3: automatic by Lemma O (p ≥ 5). p=3 | 2z⁴−3 ⟺ 3|z:
   handled inside p=3 engineering.
Auto-pass (proved by digit pattern, to be written): p ∥ z²+1 with p = z^γ, γ > 4/3:
digits of z⁴ are (a²−1, p−2a, 1), a = (z²+1)/p, forcing a carry. Similarly J=2 analog.

## First-moment budget (heuristic; to be CALIBRATED numerically, then proved with
explicit error terms)

E[#failures per z in the family] ≈
  E_z (β ≤ 1/2 since z smooth; P(fail at β) ≈ P(Bin(⌈4/β⌉−4, ~1/2) ≤ 3)) ≈ 0.35
+ E_{z±1} (J=1: P ≈ 2^{−(#digits)}, #digits ≥ 3 — tiny; J≥2: Σ 1/p² — tiny) ≈ 0.05
+ E_{z²+1} (γ ∈ (1, 4/3): crude bound P=1 gives ≈ 0.29·C_sieve; with digit conditions
  ≈ 0.29·0.2·C_sieve; γ ≤ 1: ≈ 2^{−(#digits)} sums — small) ≈ 0.1–0.6 (calibrate!)
+ spikes (p^J with J ≥ 2 beyond the above: Σ small) ≈ 0.05
TARGET: total < 1 − δ. Then Markov: ≥ δ·|family ∩ [Z,2Z]| members have zero failures,
and |family| ≥ c(Q₀)·ρ-positive·Z ⟹ S₂ ∩ [scale Z⁴] ≠ ∅ for every large Z ⟹ S₂ infinite.

## Tools per counting step (all classical; no smooth-AP equidistribution needed)

 T1. Base count: smooth numbers in the fixed class c₀ mod Q₀: Dickman-in-AP for fixed
     modulus (Tenenbaum III.5-type / elementary). Lower bound c·ρ(1/θ_s)·Z.
 T2. Source 'z' failures: z = p^ν v: count over v-interval; digit conditions on v⁴ are
     unions of residue classes mod p^t; incomplete quartic Weyl sums over v ∈ [V, 2V] mod
     p^t ≤ V^{4−δ} give equidistribution; smoothness of z DROPPED for the upper bound.
 T3. Source 'z±1' failures: divisor switch z∓... = ap^J; for fixed cofactor a, digit
     conditions become sawtooth conditions in p; equidistribution of {N/p} over primes
     (Vinogradov) or crude bounds suffice given the 2^{−D} room.
 T4. Source 'z²+1' failures: z²+1 = a·q, a ≤ z^{1−...} small: Σ_a ρ₂(a)/a · (Selberg/BT
     upper bound for q prime) · (digit conditions via sawtooth in the a-parametrization).
     Constant C_sieve ≤ 2+ε enters — budget must absorb it (or narrow the γ-window and
     use digit conditions to cut the 0.29 before the sieve constant multiplies).
 T5. Small primes p ≤ P₀: existence of a good class c₀ mod p^{L_p}: counting via complete
     quartic character/exponential sums mod p^L (Hua), or explicit construction; verify
     candidate classes numerically first.
 T6. Assembly: |Bad| ≤ Σ (T2..T5 counts) < (1−δ)·(T1 count) for large Z.

## Risks / open ends

 - The C_sieve constant in T4 (budget tightness) — mitigate with digit conditions.
 - Overlaps of conditions (p in two sources — impossible for p ≥ 5 (gcd's) ✓).
 - The Bin(D, 1/2) model for carries is Markov-chain-correct up to O(1/p) — use the
   728-paper Lemma 15 chain analysis for rigor.
 - z⁴−2 ≡ 0 possibilities mod engineered primes: make c₀ avoid p | z⁴−2 for p ≤ P₀?
   NO — p | n = z⁴−2 is allowed and irrelevant: conditions are about the WINDOW products
   (n+1, n+2 and odd elements), not n. ✓
 - k=2 ONLY. The headline (all k) needs a different supply; see R-BW injection route.

## Immediate numerics (calibrate.py-style gate for this route)

 N1. verify_propN.py: Prop N + Lemma O against brute force for k=2,3, n ≤ 3·10^4.
 N2. quartic_scan.py: density of z⁴−2 ∈ S₂ for z ∈ [10^3, 10^4]: overall, restricted to
     √z-smooth z, and with best-found class mod 16·9·25·49; failure-source breakdown
     (z / z−1 / z+1 / z²+1 / p≤P₀ / spikes) with β-histograms; compare against the
     budget table above. Also empirical P(fail | source, β) curves vs Bin model.
 N3. The γ ∈ (1, 4/3) z²+1 auto-pass boundary: verify the (a²−1, p−2a, 1) pattern claim.
