# ROUTES.md — route registry for Erdős 196

Status values: active / blocked: <reason> / merged / retired.
Group by mathematical idea, not wording. Keep YES and NO routes alive until one side is excluded.

| id | family | sign | status | key lemma targets |
|----|--------|------|--------|-------------------|
| R1 | Recursive/self-similar block constructions, scale growth + reflections | NO | active | finite 4-AP-free gadgets composable across scales; kill within-block / adjacent-scale / ≥3-scale APs |
| R2 | Re-engineer DEGS77 5-AP gadget down to length 4 | NO | active | reconstruct DEGS77 construction; isolate why it fails at 4; engineer around obstruction |
| R3 | Base-b digit / parity constructions | NO | complete → spawns R16 | Theorems A/B (DRUP-certified): contiguous digit-block orderings dead; 26 orderings die ≤ value 12; Lemma T comparator; cut-set {8,26,80}={3^j−1} coherence with R1 |
| R4 | SAT/CP search over finite avoiders with surjectivity pressure (displacement bounds π(v) ≤ Cv) | both | active | for fixed C do avoiders die at finite N(C)? survivors → gadgets; extinction → YES-side lemma |
| R5 | Pigeonhole/Ramsey bootstrap: forced 3-APs → 4th term | YES | blocked: Generic Escape Prop (attempts/route-R5/REPORT.md §4) — one-point-anchored supply can never close a finite forcing tree | staircase L10 + anchored supply Thm 2/2' proved; hand-offs: two-point supply (R13), staircase-vs-displacement (R6/R10) |
| R6 | Density/Szemerédi on increasing subsequences + exhaustion of ℕ | YES | REPORT filed; density-alone CLOSED (Behrend slack r₄²/x→∞; both one-sided systems realizable: triadic ↑, identity ↓); merged into R15 | attempts/route-R6/: L1-L3+Dilworth proved; T1-T6 tested N≤9 exhaustive; dyadic calibration REFUTED, triadic proved (ratio-3 forced, Prop 7.5); LP-inc ceiling C*_inc≤3 human-proved, ≥43/24 machine-assisted |
| R7 | Compactness/limit over extension tree with explicit order-type-ω control | both | merged into R10 | CORE.md Lemma 6 resolves the trap: pointwise φ-bound survives the limit |
| R8 | Transfer analysis ℕ vs ℤ at length 4 | expl. | active | which mechanism separates one-sided from two-sided; folding obstructions |
| R9 | Structural census of finite avoiders (DP/transfer statistics, LIS, displacement, blocks) | both | active | conjecture the true sign early; steer portfolio |
| R10 | Displacement-compactness frame: NO ⟺ ∃φ-uniform finite avoiders; YES via FIN(K) or ∀φ-extinction | both | active | CORE.md Lemmas 6-7; feeds R4 |
| R11 | Asymmetric strategy: no dec-3AP + no inc-4AP (⟹ NO-witness); descent-word + leader-spine structure | NO | active | ASYM.md A1-A2; finite existence N>27?; multi-scale descent-word realization |
| R12 | Contiguous-block CSP architectures (BLOCKS.md) | NO | blocked: R1's SAT+König theorems kill in-order geometric layouts for every gadget (cut-set {8,26,80}); bounded-lag interleaves die at stage 7; linear-profile extinction (Thm 12 + empirics) squeezes the rest | superseded by R1 corridors: tuned cut windows, non-decomposing layouts |
| R13 | Two-point supply hunt (R5 hand-off) | YES | pending wave 2 | SAT-map candidate two-point supply statements; only route past Generic Escape barrier |
| R14 | FINlin / SHALLOW extinction program: initial-segment shallow placement dies on large boards | YES | active (inline) | Lemma 7b; mus_profile.py shows asym C=2 extinction driven by segment [1..15]@2v; shallow_scan.py probing plain FINlin(8/15) |
| R15 | LP sharpening: true mechanism of C ≥ 2 linear-profile extinction | YES | active (R6-merge + inline) | Thm 12 gives C < 9/8; R6: LP-inc(C) proved ∀C ≤ 43/24 (CP-SAT UNSAT, N=32/40/48) and FALSE ∀C ≥ 3 (triadic, pos ≤ 3v−1, human-proved) — sharpening must couple (H↓) beyond 3; conjecture C*_inc = 3; Γ-dense escape documented |
| R16 | τ-repair: base-3 priority comparator kills all 4-APs on every subset (R3 Lemma T); repair to order type ω via override schedules with superlinear displacement | NO | pending wave 2 | R3 Prop B/B': τ's own mechanism forces infinite predecessors, overrides must occur infinitely often; find schedule preserving avoidance, or kill the family |
| R17 | Co-supply / infinite forcing chain (Thm 16 crux) | YES | active (wave 2) | co-supply or weaker chain-continuation; quantitative |Cl(u)| lower bound |
| R18 | NO-design with bounded forcing closures (Thm 16 as design principle) | NO | active (wave 2) | SAT with closure-size caps; structured candidate to 10^4 |
| R19 | LP sharpening: (43/24, 3) inc-only, and two-orientation past 3 | YES | active (wave 2) | Thm 14 caps inc-only at 3; certify plain C=2,2.5,3 |
| R16 | tau-repair (base-3 comparator to order type omega) | NO | active (wave 2) | override schedules; truncated-depth tau; closure behaviour of tau |
| R20 | Displacement Θ(v·log v) constructions (data-driven NO target) | NO | active (wave 2) | v·log₂v profile SAT through N=100; needs logarithmically growing debt — outside R1's dead bounded-lag regions |
| FRESH | Isolated independent attack (no route history) | both | filed | independently re-derived Lemma 13(a) and the two-base-point necessity; measured ν_L(N)=L flat for L≤20, N≤128 |

## Status synthesis (2026-07-28, after Theorem 21 / Remarks 20, 22, 23)

NEGATIVE branch — the two natural mechanisms are now closed:
- digit-comparator family: Remark 20 dichotomy (LSD kills 4-APs but forces infinite
  predecessor classes; MSD gives order type ω but is a block layout);
- block-layout family: R1's gadget-quantified SAT+König certificates, plus Remark 23's
  pair-counting reason (the length-5 argument needs TWO pairs; four terms give
  pair+singleton). Machine-confirmed: all four naive length-4 analogues of Theorem 21
  die immediately, the first at (2,5,8,11), a 1+2+1 pattern.
What remains: R20 (Θ(v log v) displacement), R18 (bounded closures), R16 (τ-repair
beating the dichotomy), R11 (asymmetric), and R1's ratio-5 island if it survives.

AFFIRMATIVE branch — barriers are explicit:
- one-point-anchored forcing provably cannot close (R5's Generic Escape, re-derived
  independently by FRESH);
- displacement/LP arguments cannot decide the problem (Remark 17: Lemma 6 quantifies over
  ALL profiles, and the known-NO case k=5 exhibits the same linear-profile extinction);
- FIN/FINlin shallow criteria are dead at reachable scales (ν_L(N)=L flat).
What remains: R17 (co-supply / infinite forcing chain — the Theorem 16 crux), R13
(two-point supply), and exploiting the coupled 3-AP-free record family of Lemma 24,
whose obstacle is the absence of any density lower bound (Roth-critical).
