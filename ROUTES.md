# ROUTES.md — route registry (Erdős 727)

Format: id | mathematical family | status (active / blocked: reason / merged) | key lemma targets

## YES routes

 - **R1 [SUPERSEDED by R12 — Lemma Q: polynomial parametrizations force squares; power-family budgets do not close unconditionally] | CRT digit engineering on algebraic smooth-window families** | active |
  For k=2: family n = x^2 - 2 (window {x^2-1, x^2} is (x+1)-smooth). Targets: (L1a) mid-range
  lemma — along a sub-family of x's, digit condition holds at every p ≤ √(2n); (L1b) generalize
  window ansatz to k ≥ 3 with PROVED infinitude.
- **R2 | Carry-engineering transfer from 728/729/401 (arXiv 2601.07421)** | active |
  Port the method that manufactures prescribed carry patterns for all p simultaneously to the
  deficit inequality (p-1)(c_p - b_p) ≥ 2k - s_p(2k). Targets: (L2a) understand the machinery;
  (L2b) re-target it at c_p - b_p surplus.
- **R3 | Balakran dissection and upgrade k=1 → fixed k** | active |
  Reconstruct Balakran's construction for ((n+1)!)^2 | (2n)!; identify exactly what breaks at
  k=2; upgrade. Targets: (L3a) explicit Balakran family; (L3b) the k=2 failure mechanism.
- **R4 | Analytic counting along constructed sequences** | active |
  |S_k ∩ [1,X]| → ∞ via smooth-number counts + digit control, uniformity explicit. Targets:
  (L4a) a family dense enough to beat union-bound losses at mid primes.
- **R5 | Parametric-family mining from large-scale data** | active |
  Sieve S_2..S_6 to 10^8+; hunt congruence/algebraic/digit-motif subfamilies; prove one family
  infinite and inside S_k. Targets: (L5a) the sieve; (L5b) a family with a valuation-lemma proof.
- **R6 | Uniformization: single-k success → every fixed k** | pending (needs a single-k win) |

## NO routes

- **R7 | Obstruction hunting** | active |
  Weight/counting arguments playing Σ_p (p-1)(c_p - b_p) against global digit identities;
  attempt to prove some S_{k_0} finite. At minimum delimit rigorously why obstructions fail.
- **R8 | Reduction interface analysis** | active |
  Which consecutive-smooth-number statements are equivalent to / weaker / stronger than the
  large-prime half of 727; prove the provable ones unconditionally. Also: literature check on
  Balog–Wooley-type theorems (strings of consecutive n^ε-smooth integers) — if such a theorem
  covers threshold n^{1/2} for all k, the large-prime regime is DONE by citation and the fight
  is purely mid-range/small primes.
- **R9 | Per-prime digit dynamics** | active |
  Study {m : (p-1)(c_p(m) - b_p(m)) ≥ 2k - s_p(2k)} as a carry/borrow counting problem;
  characterize intersections across primes at growing depth. Both signs.

## Post-wave-1 additions (2026-07-28)

- **R11 | Statement-B literature (consecutive almost-primes, E_2 levels, dispersion)** | active |
- **R12 | FLAGSHIP k=2: Lemma R + Statement B** | active |
  Lemma R proved+verified (attempts/route-R3/BREAKAGE.md §4). Targets: (L12a) Statement B or
  a relaxation (more prime factors per side: pq+1 = 2r_1..r_t, or pqr+1 = 2stu) provable with
  published dispersion/Harman technology; (L12b) full audit of Lemma R; (L12c) generalization
  ladder toward fixed k ≥ 3 (k−1 simultaneous equations — hard; document exactly).
- **R1 status detail** | blocked: superseded | Lemma Q (route-R3) explains the square-burden;
  independent budget analysis (PROOF_SKELETON.md) reached the same wall analytically.
