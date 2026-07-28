# Route R6 REPORT — Density/Szemerédi structure of a hypothetical counterexample

## Verdict

**Erdős 196 is NOT resolved by this route.** The density/Dilworth tension
(increasing subsequences have 4-AP-free, density-0 value sets, yet must jointly
exhaust ℕ) is real and now fully proved, but it **provably cannot yield a
contradiction on its own**: the cardinality coupling has slack factor
`r₄(x)²/x → ∞` (Behrend), and each one-sided constraint system is individually
realizable. The route's positive outputs are:

1. **Full proofs** of L0–L3, the infinite patience/Dilworth theorem (with the
   false variants separated and refuted by counterexample), and six machine-tested
   necessary conditions T1–T6 on any counterexample (PROOFS.md §§1–4).
2. **A correction:** the brief's calibration example (reversed dyadic blocks) is
   wrong — it CONTAINS increasing monotone 4-APs, e.g. `(1,6,11,16)` at positions
   `(1,5,12,31)`. Ratio-3 blocks (triadic) are the correct calibration object,
   and ratio → 3 is *forced* in the reversed-block family (PROOFS.md §5, §7.5).
3. **LP merge (cross-route, prioritized per coordinator):**
   - **Ratio-3 ceiling (human-proved):** there is a permutation of ℕ with
     `pos(v) ≤ 3v − 1` for all `v` (a chain variant even `≤ 3v − 5` for `v ≥ 3`)
     and NO increasing monotone 4-AP. Hence LP-inc(C) is FALSE for all `C ≥ 3`,
     and **no increasing-orientation-only argument (CORE Thm 12's ledger,
     R5-staircase counting, records/grounded/pile counting) can prove any
     displacement bound at or beyond C = 3.** The empirical full-4-AP extinction
     at C = 3 is necessarily a two-orientation phenomenon.
   - **R5 hand-off answered (negatively for C ≥ 3):** R5's L10 staircases use
     only the increasing orientation, and explicit full staircases (verified
     `g ≥ 3` steps and planted inversions) coexist with `pos(v) ≤ 3v−1` inside
     the triadic example (`staircase_demo.py`). Staircase counting can only prove
     LP below 3, if at all.
   - **Sharpening of LP(9/8) (machine-assisted):** CP-SAT UNSAT certificates give
     **LP-inc(C) for all C ≤ 43/24 ≈ 1.792** (vs human-proved 9/8 = 1.125),
     via the finite bridge Prop 7.2. Finite thresholds are strictly climbing
     (min-SAT C: 3/2 at N=12 → 11/6 at N=32). **Conjecture: C*_inc = 3 exactly.**

## 1. Proved core (deliverable 1) — PROOFS.md §§1–3

- **L1**: value sets of increasing subsequences are 4-AP-free; upper density 0 by
  Szemerédi (k=4, Szemerédi 1969, exact statement quoted). Dual L1′ for
  decreasing subsequences (4-AP-free; finite automatically).
- **L2**: decreasing subsequences are each finite (well-ordering) but of
  unbounded length — proof needs only van der Waerden, not Szemerédi.
  Quantitatively (L2.5): `x ≤ LIS(x)·LDS(x)`, `LIS(x), LDS(x) ≤ r₄(x)`, hence
  both lie in `[x/r₄(x), r₄(x)]`; orientation-dependence of each half tracked
  exactly (this matters: the calibration example obeys the (H↑) halves and
  violates an (H↓) half at `x = 26`: `LDS = 18 > 15 = r₄(26)`, exact).
- **L3**: piles (dec-patience level sets) partition ℕ into increasing
  subsequences with the interlock property; under (H↑) there are infinitely many
  piles and EVERY pile is infinite (uses the vdW∞ strengthening, proved).
- **Theorem D** (infinite Dilworth/patience, sequence version, constructive):
  bounded decreasing length `s*` ⟺ minimal increasing cover has exactly `s*`
  parts; `s* = ∞` ⟹ no finite cover but a canonical countable pile partition.
  **False variant refuted**: "all decreasing subsequences finite ⟹ finite
  cover" fails — every permutation of ℕ has all decreasing subsequences finite,
  while triadic has unbounded LDS, so no finite cover (each increasing part meets
  a decreasing chain at most once). "Unbounded lengths" vs "an infinite one"
  carefully separated (no infinite decreasing subsequence exists at all).
- **L3.5**: induced permutations on infinite value sets are again permutations of
  ℕ (order type ω) — the lemma that makes tail/AP-restriction closure legitimate.

## 2. Necessary conditions, machine-tested (deliverable 2) — PROOFS.md §4

T1 (sandwich), T2 (pile structure: countably many infinite interlocked
density-0 piles; finite unions still density 0), T3 (closure under tails and
affine sub-progressions; with DEGS77(a): monotone 3-APs at every scale in every
residue class), T4 (local displacement: every value-window of length L contains
`v` with `|pos(v) − v| > (L−4)/6`; corollary `limsup |pos(v)−v|/v ≥ 1/6`),
T5 (record values: infinite, 4-AP-free, density 0), T6 (forced-extension
constraints = R5's L1/L2/L3a/L3b interface).

Machine verification: **exhaustive over all 194,160 monotone-4-AP-free
permutations of [1..N], N = 3..9** (counts match calibration exactly), with exact
`r₄(N)` values from brute force; zero failures across all six condition families
(`finite_tests.py`, logs `finite_89.log`). The N = 10 pass (≈1.4M avoiders) was
relaunched after the container restart and is still running at time of writing
(same code path; N ≤ 9 is the certified claim). Triadic calibration: all
(H↑)-side conditions verified on prefixes up to 19,682 values; (H↓)-side
violations demonstrated exactly where predicted (`calibration_tests.py`,
`calibration.log` — COMPLETE, all assertions pass).

## 3. The honest assessment (deliverable 3)

**Can increasing/decreasing tension alone give a contradiction? NO — with a
precise reason.** The only coupling that pure density/cardinality arguments see is
`x ≤ LIS(x)·LDS(x)` with both factors in `[x/r₄(x), r₄(x)]`. A contradiction
would need `r₄(x) < √x`; Behrend 1946 (via `r₄ ≥ r₃`) gives
`r₄(x) ≥ x·e^{−c√(log x)}`, so the inequality `x ≤ r₄(x)²` holds with slack
factor `≥ x·e^{−2c√(log x)} → ∞`. Szemerédi/Green–Tao upper bounds
(`r₄(x) ≪ x(log x)^{−c}`) cannot repair this: the sandwich stays consistent for
any `r₄` between `(log)^c`-savings and Behrend density.

**Worse, each orientation is separately satisfiable:** triadic realizes ALL
(H↑)-consequences with a linear profile (`pos ≤ 3v−1`, complete prefixes
`A_n = [1..n]` infinitely often); the identity realizes all (H↓)-consequences.
So every necessary condition provable from one orientation — including
everything in §§1–6 of PROOFS.md tagged one-sided, CORE Lemma 11, R5's whole
cascade including L10 — is jointly realizable and can never close the problem.

**The exact gap.** Countably many density-0 sets can cover ℕ (even with the
interlock structure — triadic's piles do it), so L1+L3 need a genuinely
two-orientation quantitative input. The sharpest available frame is the LP
program: the missing input X must be a position-structure invariant that (a) uses
both orientations, and (b) is not a function of value-set cardinalities of
monotone subsequences. Concretely, X must beat the profile barrier in the window
`C ∈ (43/24, 3)` on the increasing side and then couple in (H↓) to pass 3 —
e.g. the descent-word constraint "no 000 AND no 111 at every step size" (both
orientations simultaneously), whose one-sided halves are each realizable but
whose conjunction is exactly 196. The R4/SAT extinction data (full 4-AP-freedom
dies by C = 3 empirically) plus Theorem 7.3 (increasing-only survives at 3)
localizes the whole difficulty of 196's YES side in this coupling.

**Quantified state of LP (after this route):**
| statement | status |
|---|---|
| LP-inc(C), C < 9/8 | proved (CORE Thm 12; audited) |
| LP-inc(C), C ≤ 43/24 ≈ 1.792 | proved machine-assisted (CP-SAT UNSAT at N=32, N=40, N=48 — three independent runs; witnesses re-verified independently at all SAT points) |
| LP-inc(C), 43/24 < C < 3 | open; finite thresholds strictly climbing (min-SAT C = 11/6 at N=32) |
| LP-inc(C), C ≥ 3 | FALSE (triadic; chain variant with pos(v) ≤ 3v−5, v ≥ 3) — human-proved |
| LP-full(C), C ≥ 3 | open (= would need (H↓)); empirically true up to C = 3 (R4 data) |
| reversed-block family | ratio → 3 forced: limsup b_{k+1}/b_k ≥ 3 (Prop 7.5, human-proved with machine-exact feasibility lemma) |

## 4. Files

- `PROOFS.md` — all statements and proofs (§§0–8), orientation-usage annotated.
- `r6lib.py` — shared exact tools (self-checking; cross-validated against
  `experiments/apcheck.py`).
- `finite_tests.py` (+ `finite_89.log`, `finite_10.log`) — exhaustive T1–T6.
- `calibration_tests.py` (+ `calibration.log`) — dyadic refutation, triadic
  verification, exact (H↓)-violation demo.
- `family_opt_check.py` — exact bad-window feasibility (F1) + family probes (F2, F3).
- `staircase_demo.py` — R5-L10 staircases inside the triadic example.
- `lp_threshold.py` (+ `lp_scan.log`) — CP-SAT scan and UNSAT certificates.

## 5. Hand-offs

- To R5: staircase counting must target C < 3 only, and needs an (H↓) hook; the
  `g ≥ 3` in L9 and the ratio-3 ceiling are the same constant — a sharpened L9
  (`g ≥ 3` with positive frequency of `g > 3`?) is the natural attack on 7.7.
- To R4: the extinction experiments at fixed C should now separately track
  increasing-only vs full avoidance; increasing-only survives forever at C = 3
  (triadic gives live finite witnesses at every N), so any observed full
  extinction at C ≤ 3 measures precisely the (H↓) contribution.
- To R1/R3: Prop 7.5 is a hard design constraint: interval-block constructions
  are pinned to ratio ≥ 3 − o(1) blocks, where in-block structure must then
  avoid decreasing 4-APs inside intervals — impossible for full intervals
  (4 consecutive integers); so blocks must be non-intervals or overlapping
  scales. This kills the naive "repair the dyadic example" program.

