# Wave-2 route P2 — pivot certificate hunt. Final report.
(Transcribed by the session; scripts `experiments/P2_*`, logs `experiments/P2_out/`.)

## HEADLINE
**No pivot certificate exists at any lattice L ≤ 14490, nor at 27720.** In particular all five
lattices that survived the session's fiber scan — 1080, 1260, 1680, 2160, 2520 — are INFEASIBLE.

## PROVED (exact finite certificates of infeasibility)
- The five survivors, decided by **three independent implementations with identical node counts**:

  | L | \|S\| | budget | fast search | reductions-off (C) | reduction-free Python |
  |---|---|---|---|---|---|
  | 1080 | 17 | 1.22407 | 14 nodes | 71 837 | **71 837** |
  | 1260 | 19 | 1.24444 | 14 | 13 469 771 | **13 469 771** |
  | 1680 | 19 | 1.20060 | 5 | 7 997 | **7 997** |
  | 2160 | 18 | 1.24491 | 20 | 629 162 | **629 162** |
  | 2520 | 24 | 1.40357 | 127 | 22 475 855 | (≈10¹⁰ nodes, not run) |

  `P2_naive.py` is a deliberately dumb 60-line exhaustive search — no symmetry, no dominance, one
  obviously-valid density prune — written so the verdict does not rest on the fast searcher's
  reductions. **The session re-read that code, confirmed it is a complete enumeration, and reran it
  on 1080, 1680, 2160 obtaining the same node counts**, plus the positive control (modulus 2
  permitted at L = 288 → FEASIBLE, certificate re-verified from scratch).
- **COMPLETE for every L ≤ 14490**: 259 candidates with budget > 1 → 203 infeasible by the exact
  fiber test, 56 by exhaustive search, **0 undecided, 0 SAT**.
- **[14491, 51240]**: 134 further lattices infeasible, 0 SAT, 14 time-capped (15120, 22680, 25200,
  27720*, 30240, 32760, 37800, 40320, 41580, 42840, 45360, 46200, 49140, 50400).
- **L = 27720** — the first lattice where the pivot could hold on budget grounds, and the one
  routes B, C and G all failed to decide — separately decided **INFEASIBLE**, 116 692 nodes.
- Φ_Q(S) ≥ B_Q(L) := Σ 1/m over m ∈ S(L) coprime to ∏Q, so B_Q ≥ 1 makes the Q-local test vacuous.
  Smallest L with B₂(L) ≥ 1 is **L = 45045 = 3²·5·7·11·13** (B₂ = 1.01370).

## MEASURED
- **Exact optimal gaps — these are NOT near misses.** Minimum uncovered residues over ALL choices:
  gap(1080) = 76/1080 = 7.04 %, gap(1260) = 94/1260 = 7.46 %, gap(1680) = 180/1680 = 10.71 %,
  gap(2160) = 129/2160 = 5.97 %; 2520 ≤ 186 (7.38 %). A fixed 6–11 % of ℤ/L is unreachable no
  matter what residues are chosen.
- Kill primes are only **2 (78×), 3 (49×), 5 (13×)** up to L ≈ 10⁴ — never a larger prime.
- For **every one of the 18 424 lattices L ≤ 10⁶** with pivot budget > 1, min over q | L of B_q(L)
  is still < 1: the single-prime test is nowhere a-priori vacuous in that range, and the same holds
  for all pairs and triples. Max B₂ over L ≤ 10⁷ is only 1.11399. Route D's divergence is real but
  extraordinarily slow (log log).
- Pivot budget grows agonisingly slowly: 1.587 (27720), 1.747 (720720), 1.904 (1.1·10⁸) — never
  reaching 2 in the reachable range.
- **Structural fact (elementary, proved; heuristic in its consequence).** In Φ_q a modulus
  contributes weight q^{ν_q(m)}/m ≤ 1, with equality iff m is a power of q. Since 2^j ∈ H iff
  2^{j+1}+1 is a Fermat prime, the only powers of 2 in H are 2, 8, 128, 32768. Banning 2, the best
  2-adic weight available at level j = 2 is **1/5 (m = 20)** where unrestricted it would be
  **1 (m = 4)**. That is the precise sense in which "4 ∉ H" bites: the level-2 slot, where a cheap
  least-modulus-3 covering buys its 2-adic mass, costs a factor 5. Full weight is available only at
  the Fermat levels j = 3, 7 (15).
- SAT is the wrong tool: CaDiCaL did not finish L = 1080 in ~10 CPU-minutes while the
  modulus-ordered DFS decides it in 14 nodes. The decisive ingredient is a translation-orbit
  normalisation (process moduli increasingly, force b_{m_i} ∈ [0, gcd(lcm(used), m_i))).

## SCOPE — stated by the agent and endorsed here
UNSAT at L says only that *no pivot covering has lcm dividing L*. **H ∖ {2} is infinite**, so this
is a growing list of lattice lemmas and **not** a proof that the pivot fails, hence **not** a proof
that Erdős 273 is false. Route D's divergence barrier is untouched: the measured mechanism is
exactly the kind of fixed-finite-prime-set obstruction that cannot generalise.

## FAILED
No certificate found, so no positive resolution. No general theorem. 14 lattices in [15120, 50400]
time-capped; 55440 and the large highly-composite lattices (720720, …) unresolved.
