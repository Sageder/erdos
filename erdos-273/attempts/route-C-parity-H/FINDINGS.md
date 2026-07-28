# Route C — parity split and the halved world H. Final report.
(Transcribed by the session; scripts: `experiments/C_*`, raw output in `experiments/C_out/`.)

## PROVED
- **Theorem C1 = Lemma M3, re-derived from scratch in both directions** (sixth independent
  derivation this run) and verified computationally: an E-covering exists iff two DISJOINT finite
  M_0, M_1 ⊆ H each carry a distinct-moduli covering of ℤ. Verified for all x ∈ [−4000, 4000] on
  600 random systems **including negative residues**; full-period coverage equivalence on explicit
  and 200 shifted cases; and **distinctness of the E-moduli ⟺ M_0 ∩ M_1 = ∅** on 400 random pairs,
  confirming that disjointness is exactly the extra content. Negative controls behave.
- **★ NEW STRUCTURE OF H (elementary, verified by me independently).** For an odd prime q,
  2m+1 ≡ 0 (mod q) ⟺ m ≡ (q−1)/2 (mod q). Since 2m+1 must be prime, H meets the class
  (q−1)/2 mod q only in the single point m = (q−1)/2. Consequences:
  * **H contains no m ≡ 1 (mod 3)** (residues of H mod 3 are exactly {0, 2});
    equivalently **E contains no n ≡ 2 (mod 6)** (residues of E mod 6 are exactly {0, 4}).
  * H ∩ {m ≡ 2 mod 5} = {2}, H ∩ {m ≡ 3 mod 7} = {3}, H ∩ {m ≡ 5 mod 11} = {5}, etc.
  * The powers of 2 in H are exactly 2, 8, 128, 32768 (Fermat primes).
  This is the precise reason the moduli every cheap least-modulus-3 covering wants are missing:
  **4 ≡ 1 (mod 3), 10 ≡ 1 (mod 3), 12 ≡ 2 (mod 5)** — so 4, 10, 12 ∉ H.
  CAVEAT (route D's point, which stands): these are conditions on the *residue* of a modulus,
  whereas covering feasibility depends on the *divisibility lattice* of the chosen moduli, so the
  restriction is transverse to every covering-theoretic argument found so far.
- **Unconditional lcm bound, independently re-derived:** any E-covering with lcm N has
  B_H(N/2) > 2; the set {B_H > 2} is upward closed under divisibility; exhaustive sieve for
  L ≤ 3·10⁶ gives smallest L = 27720, hence **lcm ≥ 55440**, with lcm/2 a multiple of one of the
  55 minimal elements ≤ 3·10⁶ (27720, 32760, 50400, 75600, 90720, 102960, …).

## VERIFIED
- **Question (i): H-coverings exist, easily.** Four certificates independently re-verified
  (primality of 2m+1, distinctness, full mod-L sweep, negative window, E-image check). Route C's
  cheapest: cost 1.488889, moduli {2,3,6,8,9,15,18,20,30,36,90,120} at L = 360.
  **NOTE:** route F found a cheaper one — cost **65/48 ≈ 1.3542** at L = 288, moduli
  {2,3,6,8,9,18,36,48,96,288} — which the session re-verified. Route C did not test L = 288.
- **Question (ii), exhaustive UNSAT** for "covering with distinct moduli in H ∖ {2} dividing L"
  (complete DFS with no-good recording): L = 360 (165 743 nodes), 660 (88 103), 720 (46 021 340),
  810 (128 879 911), 960 (111 609). L = 720 independently confirms route G. These agree with the
  session's fiber-test kills at the same lattices.
- Tightness: the H-coverings found consume nearly the whole lattice budget (1.898 of 1.904 at
  L = 2520; 2.063 of 2.087 at L = 27720), so a disjoint pair inside one lattice plausibly needs
  B_H(L) ≈ 3.
- Budget growth: best achievable B_H(L) is 2.38 at log₁₀L ≈ 7, 2.68 at 12.4, **3.02 at
  log₁₀L ≈ 25**. A lattice roomy enough for a disjoint pair is astronomically beyond any mod-L sweep.

## FAILED, and why
- **No H-covering avoiding the modulus 2 was found in ANY lattice tried**: L = 360, 630, 660, 720,
  810, 840, 900, 960, 990, 1260, 2520, 5040, 27720, 151200, 360360, 720720, 2162160, 10810800
  (deterministic ascending, randomized 1/m-weighted restarts, and CaDiCaL). Undecided lattices with
  node counts: 630 (4.4·10⁷), 840 (1.6·10⁸), 900 (4.2·10⁸), 990 (7.7·10⁸).
  **This is search failure, not evidence for nonexistence.**
- **The q-adic fiber test does NOT bite question (ii) at L = 27720**: with S = H-divisors minus 2,
  for q = 2 the odd part alone gives 0.9605 per leaf against a deficit of 0.0395 with supply 2.81;
  for q = 3 the base is 0.6192, deficit 0.3808, supply 6.5. So Φ₂, Φ₃ ≥ 1 comfortably. **The
  forbid-2 pool is too rich for local fiber tests at that size** — consistent with the session's
  frontier analysis (the test can only bite while the q-coprime sub-budget is ≤ 1).
- A sharper per-divisor necessary condition was derived and **collapsed**: the worst divisor is
  always d = 1, so it adds nothing beyond B_H > 2.
- **SAT was weaker than the DFS here.** CaDiCaL failed to decide even L = 2520 forbid-2
  (6 452 vars, 12 196 clauses) in 900 s.
- **No positive control for the `--pair` solver mode** — it never returned SAT on any instance, so
  its uncompleted UNSAT verdicts are NOT to be trusted. Flagged by the agent itself.

## Bottom line
Step 1 is settled: the problem is exactly "two disjoint H-coverings". Question (i) is YES and
cheap. Question (ii) — an H-covering avoiding the modulus 2 — is the decisive open point; route C
added five exhaustive UNSAT lattices and the lcm ≥ 55440 bound, but neither a certificate nor a
general impossibility argument.
