# Route F — how cheap can a distinct-moduli covering system be? Final report.
(Transcribed by the session: the subagent's harness blocked it from writing report .md files.
All its scripts are `experiments/F_*`.)

## PROVED
- **Waste identity.** For distinct moduli n_i | L: Σ 1/n_i = (L+W)/L with
  W = Σ_r (mult(r) − 1) ∈ ℤ_{≥0}. So the minimum cost is exactly μ(L) = 1 + X(L)/L, X = min W.
- **Residue identity / lower bounds.** With P(z) = Σ_r (mult(r)−1) z^r and ζ a primitive N-th root
  (N | L, N > 1): P(ζ) = L Σ_{i : N | n_i} ζ^{a_i}/n_i. Taking N = n_k (largest modulus) gives
  |P(ζ)| = L/n_k, hence **X ≥ L/n_k**; and **X ≥ 2** (X = 1 would force an exact cover with
  distinct moduli after deleting one class, contradicting DMNR).
- **Infimum = 1 (independent re-derivation of our Lemma M2), with a stronger staircase.**
  D(C,m) = {2^{j−1}−1 mod 2^j}_{j≤m} ∪ {(2^m−1)+2^m b_i mod 2^m m_i} is a distinct-moduli covering
  of cost 1 + 2^{−m}(c−1). Seeded from 4/3 this gives cost 1 + 1/(3·2^m) for every m; verified
  exhaustively mod L for m = 0..14 (L up to 196608, 19 classes, cost 49153/49152). Waste is the
  constant integer W = 4 throughout.
- **★ RIGIDITY THEOREM (new, and the most useful structural fact found this session).**
  If residue classes with pairwise DISTINCT moduli > 1 partition ℤ ∖ (c mod D) *exactly*
  (disjointly), then D = 2^m and the moduli are exactly {2,4,8,…,2^m} — the dyadic staircase,
  unique up to translation. (Generating functions: at a primitive n_k-th root only i = k has a
  pole, forcing n_k = D, D even, a_k ≡ c + D/2; delete and induct.) Verified exhaustively for all
  L ≤ 40: 184 configurations, 0 violations.
  **Corollary.** E ∩ {2^k} = {4,16,256,65536} and H ∩ {2^k} = {2,8,128,32768} — the Fermat primes
  (minus 1, resp. halved). Neither set contains two consecutive powers of 2, and 2 ∉ E. Hence
  **in E there is no waste-0 partial cover missing exactly one class at all**, and in H only the
  trivial one (D = 2). The only known mechanism driving cost → 1 is structurally unavailable in E.
  (This does NOT prove costs in E/H are bounded away from 1 — other mechanisms are not excluded.)
- **Parity reduction** (third independent derivation, agrees with Lemma M3), and
  B_E(2L) = ½ B_H(L), so B_E(2L) > 1 ⟺ B_H(L) > 2.

## VERIFIED (finite per-L theorems)
- Exact minima X(L) with explicit optima re-verified mod L: X(12)=4 (μ=4/3), X(24)=4 (7/6),
  X(36)=7, X(48)=4 (13/12), X(60)=16, X(72)=7, X(96)=4 (25/24), X(144)=7. X is NOT monotone.
- **H-coverings exist; the smallest lcm is 180**, and every budget-feasible L < 180 is UNSAT.
- Exact H-minima μ_H(L) for 12 values of L. **Cheapest H-covering found anywhere: 65/48 at
  L = 288**: 0/2, 1/3, 3/6, 5/8, 2/9, 17/18, 23/36, 41/48, 17/96, 257/288.
  Its E-image {4,6,12,16,18,36,72,96,192,576} ⊆ E **covers every even integer** at cost 65/96.
  **Re-verified independently by the session** (moduli distinct, all n+1 prime, covers exactly the
  evens mod 576).
- μ_H sits at 65/48 for ALL of L = 288, 576, 864, 1152, 1728 — **no downward trend**, the opposite
  of the unrestricted world where μ → 1.
- **No H-covering avoiding the modulus 2** for L ∈ {180, 270, 360, 540, 720, 900} (SAT-UNSAT).
  This is the M4 pivot; the finite evidence so far points the wrong way for the YES branch.
- Smallest L_H with B_H > 2 is 27720 (= our Lemma M1); smallest with B_H > 1 + 65/48 is 21621600.

## MEASURED, NOT PROVED (and must not be used in any proof)
- X(L) ≥ 4 always (no counterexample L ≤ 530, 20 values capped). Only X ≥ 2 is proved.
- **μ_H ≥ 65/48 is pure measurement.** No lower bound on μ_H was proved. The rigidity theorem
  removes the only known cheapening mechanism but does not exclude others (waste-0 partial covers
  missing several classes, then recursing, are not ruled out).
- Threshold estimate: if 65/48 is near the floor for H-coverings then an E-covering needs
  B_H > 130/48 = 2.708, i.e. **lcm ≈ 10^15–10^16** — far beyond any flat search.

## FAILED / incomplete
- X(120) and the unrestricted X(L) for L = 180,240,360,720,840,1260,2520,5040: branch-and-bound
  node counts exceed 3.6·10⁸; RC2 MaxSAT stalls past L ≈ 100. Only X(120) ≥ 15 established.
- X ≥ 3 / X ≥ 4 not proved: the generating-function argument that kills X = 1 becomes a
  multi-branch case analysis at X = 2 which was not closed.
- Two disjoint H-coverings were neither found nor refuted at any L.
