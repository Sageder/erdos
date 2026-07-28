# Route B — recursive / hierarchical divisor-tree construction. Final report.
(Transcribed by the session; the subagent's harness blocked it from writing report .md files.
Scripts: `experiments/B_*`.)

## PROVED
- **B-P1 the recursion is exactly right.** For a node "class r mod D, to be finished by multiples
  of D": substituting x = r + Dy gives {n ∈ E : D | n} = {D·f : f ∈ P(D)} with the local pool
  P(D) = {f ≥ 1 : Df+1 prime, Df ≥ 4}; the class a mod Df becomes b mod f in y-space. So the node
  problem is the ORIGINAL problem with E replaced by P(D); f = 1 is the terminal move (the single
  modulus D, legal iff D ∈ E and unused). Brute-force verified for all D ≤ 59, n ≤ 4000, plus
  2000 random rescaling checks.
- **B-P2** the hole may always be taken to be 0 mod M' (translation invariance).
- **B-P3 parity is a GLOBAL constraint, not a per-node one.** At any node with D even the pool
  P(D) contains both odd and even f, so no analogous split exists deeper down: the parity
  obstruction lives entirely at the root and the tree does not dissolve it.
- **B-P4 Selfridge block.** {(2,0),(3,1),(4,3),(6,5),(12,9)} is an exact cover of ℤ (verified mod
  12). So if 2D+1, 3D+1, 4D+1, 6D+1, 12D+1 are all prime, the five moduli 2D,3D,4D,6D,12D ∈ E
  close the class r mod D outright — the cheapest known terminal move (weight 4/3).
- **B-P5 congruence conditions for Selfridge-closable D:** 30 | D and D ≡ 0 or 6 (mod 7).
  (D odd ⟹ 3D+1 even; D ≡ 1 (3) ⟹ 3 | 2D+1; D ≡ 2 (3) ⟹ 3 | 4D+1; each nonzero D mod 5 kills one
  of 4D+1, 12D+1, 3D+1, 6D+1; mod 7 the coefficients {2,3,4,6,12} ≡ {2,3,4,5,6} miss only 1.)
  Confirmed exhaustively for D < 200000.
- **B-P6 a verified partial certificate:** the 15 distinct moduli
  **4, 6, 12, 16, 18, 36, 42, 72, 96, 112, 126, 336, 672, 1008, 2016 — all in E — cover every even
  integer** (reciprocal sum 0.71677, lcm 2016), independently re-verified by trial-division
  primality + full mod-2016 sweep + distinctness.

## MEASURED
- Pool budgets B(D,Y) ≈ (D/φ(D))·log(log(DY)/log D), agreeing to ±30% for D ≤ 9699690, Y ≤ 10⁵;
  the d/φ(d) enrichment is real (factor 4–6 for primorial D). **Raw budget is never the local
  obstruction.**
- Divisor-restricted node budgets β(D,M) decay with depth (M = 43243200, median β): 1.54 (D<10²),
  1.15 (10²–10³), 0.92 (10³–10⁴), 0.72 (10⁴–10⁵), 0.60 (10⁵–10⁶). Fraction of nodes with β > 1.9
  (the empirical closure threshold): 18%, 2%, 1%, 0%, 0%. Deep nodes starve, but β recovers at
  ≈ +0.16 per unit of ln(#div M) — a search barrier, not an obstruction.
- Flat budgets: bE(L) ≈ 0.75 + 0.048 ln(#div L); best for L ≤ 3·10⁸ is 1.20736 at L = 248648400.
  bH(L) ≈ 1.54 + 0.094 ln(#div L); bH ≤ 2.451 for L ≤ 3·10⁸.
- Node-with-hole costs at D = 2 (M = 55440): hole density 1/3 → weight exactly 1.000
  (H-moduli {2,3,6}); 1/6 → 1.000; 1/12 → 1.194; 1/144 → 1.340. Chain steps are cheap.
- Cheapest full H-covering found by B: 1.4335 (15 moduli, M = 5040); 1.410 (19 moduli).
- **THE SUPPLY/DEMAND CROSSING.** Two disjoint H-coverings at the cheapest cost B could construct
  (2 × 1.4335 = 2.867) first become budget-feasible only at **L ≈ 2·10²²** (#div ≈ 4.4·10⁵), where
  bH = 2.878.
- Selfridge-closable D are rare: 11 values below 3·10⁵; exactly one among the 960 divisors of
  183783600; none among the divisors of 248648400, 86486400, 10810800.

## FAILED, and exactly why
- No certificate; no complete tree.
- Flat covering of ℤ/L by E-divisors failed for L = 10080, 55440, 720720, 10810800, 43243200
  (best greedy residual 14.1% at 55440): bE(L) ≤ 1.19 at searchable L versus ≈ 1.41 needed.
- **THE FAILURE POINT is the odd parity after the even parity is served.** Once the even side
  takes the cheap structure {2,3,6} (E: 4,6,12), the residual pool H∖{2,3,6} has budget 1.120
  (div 55440), 1.247 (div 720720), 1.384 (div 43243200); greedy leaves 6.3–11% of ℤ/720720
  uncovered even when granted a 1/4-density hole.
- Exact decision procedures did not converge: neither SAT (Cadical) nor complete DFS could decide
  "does H∖{2} ∩ div(M) contain a covering?" for M = 1260, 2520, 5040, 55440 in 15–20 min each.
  **No UNSAT proof for any of these — only search failure, which is zero evidence for NO.**

## Bottom line
The hierarchical framework is correct and shallow-node budgets are healthy; chain construction can
drive each branch's cost arbitrarily close to the floor 1. **Route B found no obstruction.** It
breaks purely on scale: the crossing point where the H-supply covers twice the cheapest
constructible H-covering is L ≈ 2·10²², while every node's local test needs an exhaustive sweep of
ℤ/M, capping M ≲ 10⁸ — a gap of fourteen orders of magnitude.
