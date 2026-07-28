# Lemma M2 — the infimum of Σ 1/n over distinct-moduli covering systems is exactly 1

**Statement.** Let 𝒞 be the set of covering systems of ℤ with finitely many classes and pairwise
distinct moduli, all > 1. Then
  inf_{C ∈ 𝒞} Σ_{i} 1/n_i = 1,
and the infimum is NOT attained. Explicitly, for every k ≥ 0 there is a system C_k ∈ 𝒞 with
  Σ 1/n = 1 + (1/3)·2^{−k}.

**Proof.** Lower bound: natural density is subadditive and a class mod n has density 1/n, so
Σ 1/n_i ≥ 1 for any covering. If Σ 1/n_i = 1 the classes are pairwise of density-0 intersection;
two residue classes are either disjoint or meet in a class mod lcm (positive density), so the
system would be an exact cover with distinct moduli, contradicting
Davenport–Mirsky–Newman–Rado. Hence Σ 1/n_i > 1 for every C ∈ 𝒞: the infimum is not attained.

Upper bound — the DOUBLING MAP. Let C = {a_i mod n_i}_{i≤k} ∈ 𝒞. Define
  D(C) := {0 mod 2} ∪ { (2a_i + 1) mod 2n_i : i ≤ k }.
*Covering:* every even x is in 0 mod 2. Every odd x = 2y+1 satisfies, for some i, y ≡ a_i (mod n_i),
hence 2y+1 ≡ 2a_i+1 (mod 2n_i). So D(C) covers ℤ.
*Distinctness:* the moduli are 2 and 2n_1,…,2n_k; the n_i are distinct so the 2n_i are distinct,
and 2n_i ≥ 4 > 2. All moduli exceed 1. Finiteness is clear. So D(C) ∈ 𝒞.
*Cost:* cost(D(C)) = 1/2 + (1/2)·cost(C).
Starting from C_0 = {0 mod 2, 0 mod 3, 1 mod 4, 5 mod 6, 7 mod 12} with cost 4/3 and iterating,
cost(C_k) = 1/2 + cost(C_{k−1})/2 gives cost(C_k) = 1 + (1/3)·2^{−k} → 1. ∎

**Why this matters for problem 273.** It refutes the natural but false heuristic that a covering
system "needs" reciprocal cost ≈ 4/3. Since the reciprocal budget available inside a divisor
lattice grows only like ln ln L, the difference between needing 4/3 and needing 1 + ε is the
difference between lcm ≳ 10^15 and lcm ≳ 10^5. So NO budget-counting argument of this type can
decide the problem: the reciprocal-sum obstruction is genuinely powerless here, exactly as
PROMPT §3 warns.

**What it does NOT give.** The doubling map needs the moduli 2 and 2n_i to be admissible. In the
E-world admissibility of n and of 2n are unrelated conditions (n+1 and 2n+1 both prime), so
D does NOT act on E-systems, and the lemma gives no construction inside E. It is a statement
about the unrestricted problem only.

**Verification.** `experiments/M_cost_infimum.py` builds C_0,…,C_8 explicitly, verifies each is a
covering with distinct moduli by a full mod-lcm sweep, and prints the exact costs.
