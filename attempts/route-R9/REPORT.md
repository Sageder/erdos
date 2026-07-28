# Route R9 REPORT — Structural census of finite monotone-4-AP-free permutations

Erdős problem 196 (statement of record: /home/user/erdos/PROBLEM.md). All code and raw
outputs in this directory. Everything labeled EXACT is a complete enumeration; everything
labeled SIS carries batch-based error bars (deterministic seed 196); everything labeled
BEAM is heuristic lower-bound evidence and is explicitly NOT an extinction certificate
(see §6.3 for a proven instance of beam failure).

"Avoider" = permutation of [1..N] with no monotone 4-term AP (both orientations).

---

## 0. Verdict first

**The finite data does not decide 196, but it localizes the battle sharply. My read: a
weak lean NO (a counterexample permutation of ℕ plausibly exists), with the decisive
open question isolated as the ∀φ-extinction law (CORE.md Lemma 6 / LP program).**

The four load-bearing observations:

1. **The avoider tree is enormously supercritical.** Absolute counts grow
   superexponentially — mean branching (extensions per avoider) is 9.4 at N=12, 14.6 at
   N=32 and still rising. Dead ends (unextendable avoiders) do not exist at all until
   N=12 and their fraction is still only ~5.7% at N=32. Bulk choking of plain avoiders
   never begins in the observable range.
2. **Every linear displacement bound dies, with certified extinctions.** EXACT complete
   enumeration kills pos(v) ≤ Cv for C = 1.5 (at N=15), 1.6 (N=18), 1.75 (N=31), and
   pos(v) ≤ v+3 (N=19); this extends Theorem 12 (LP(9/8), proved) and agrees with the
   SAT route. The extinction profile is universal: exponential growth, a peak, then a
   cliff to zero within 1–2 levels.
3. **Displacement-death does NOT discriminate YES from NO.** Calibration on k=5
   (5-AP-free, where an infinite avoider is KNOWN to exist, DEGS77) shows the same
   finite walls at small C. On every measured axis (wall scale, branching, growth), k=4
   sits strictly between k=3 (known YES) and k=5 (known NO) — and closer to k=5 in log
   scale. So the observed extinctions are compatible with NO.
4. **The empirical φ (minimum displacement of surviving branches) grows only
   logarithmically.** The first N at which max_v pos(v)/v > C is forced fits
   N*(C) ≈ a·e^{bC} with b ≈ 2.2–2.8 over the certified range; inverting, avoiders of
   [1..N] exist with max pos(v)/v ≈ O(log N). A NO-witness must have pos(v)/v
   unbounded (conditional on extinction at every fixed C — supported at C ≤ 3, open
   beyond), but profiles as tame as pos(v) ≲ v·log v are consistent with all data.
   This is the direct answer to the added coordinator request (§6).

---

## 1. Formulation, engine, and validation

### 1.1 The insertion/extension tree (used for everything)

Avoiders are built by inserting values in increasing order: an avoider of [1..n+1]
restricts (delete value n+1) to an avoider of [1..n], so the set of all avoiders of all
sizes forms a tree rooted at (1), where children of a level-n node are the valid
insertions of n+1. Since n+1 is the maximum value, any monotone 4-AP created by its
insertion has n+1 as largest term, i.e. is (m−3d, m−2d, m−d, m), m = n+1, with m at the
last (increasing orientation) or first (decreasing) position among the four. Hence each
d forbids a suffix (if pos(m−3d) < pos(m−2d) < pos(m−d)) or a prefix (if
pos(m−3d) > pos(m−2d) > pos(m−d)) of the n+1 insertion slots, and:

> **Interval theorem.** The valid insertion slots for n+1 into an avoider of [1..n]
> always form a contiguous (possibly empty) interval [lo, hi].

This is the same fact as CORE.md Lemma 8 (independent derivations agree). It was
verified BRUTE-FORCE over all 22,266 avoiders of [1..8]: for each, all 9 insertions of
value 9 were checked by the full O(C(n,4)) definition scan; the allowed sets matched the
[lo,hi] formula in all cases and were always intervals (validate.py, V3: 0 mismatches).

### 1.2 Engine and validation ladder

census.c (this directory), modes: `exact` (complete DFS with statistics), `dump`,
`sis` (sequential importance sampling), `tame` (complete DFS restricted to
displacement-bounded subtree, k ∈ {3,4,5}), `tsis` (unbiased tame-count estimator),
`beam` (wide beam search), `dive` (random descents). Validation:

- apcheck.py cross-validates its two checkers against the literal definition (3000
  perms + 1500 sequences) — pre-existing, re-run.
- V1/V2: enumerated avoider SETS equal brute-force sets for N = 6, 7, 8 (set equality,
  not just counts).
- Counts match the known table 6, 22, 102, 564, 3336, 22266, 168864 (N = 3..9), and
  3-AP-free counts match 1, 2, 4, 10, 20, 48, 104, 282, 496 (N ≤ 9).
- V3: interval theorem brute-forced (above).
- V4: tame counts (C=2 and K=+3, k ∈ {3,4}) match brute-force filtered counts at
  N = 6, 7, 8 (12/12 checkpoints).
- Incremental 3-AP flag cross-checked against direct 3-AP counting at every node with
  full stats (≈14.3M nodes): 0 failures.
- SIS estimates agree with exact counts at N ≤ 14 within quoted error (≤ 0.02%).
- D=13 full rerun after the container restart reproduced all counts bit-identically.
- The two independent count paths (children-sum at level D vs direct visiting at D+1)
  agree at every level.

---

## 2. Deliverable 1 — exhaustive census (EXACT to N = 14, counts to N = 15)

| N | avoiders (EXACT) | 3-AP-free | dead ends | dead % | max branch |
|---|-----------------:|----------:|----------:|-------:|-----------:|
| 1 | 1 | 1 | 0 | 0 | 2 |
| 2 | 2 | 2 | 0 | 0 | 3 |
| 3 | 6 | 4 | 0 | 0 | 4 |
| 4 | 22 | 10 | 0 | 0 | 5 |
| 5 | 102 | 20 | 0 | 0 | 6 |
| 6 | 564 | 48 | 0 | 0 | 7 |
| 7 | 3,336 | 104 | 0 | 0 | 8 |
| 8 | 22,266 | 282 | 0 | 0 | 9 |
| 9 | 168,864 | 496 | 0 | 0 | 10 |
| 10 | 1,307,470 | 1,066 | 0 | 0 | 11 |
| 11 | 11,066,766 | 2,460 | 0 | 0 | 12 |
| 12 | 101,361,722 | 6,128 | 515,296 | 0.508% | 13 |
| 13 | 949,812,334 | 12,840 | 5,477,338 | 0.577% | 14 |
| 14 | 9,471,574,188 | 29,380 | 61,824,566 | 0.653% | 15 |
| 15 | 100,130,083,830 | — | — | — | — |

(N=15 from children-sum at level 14; census at 15 not computed. Raw: exact_D14.txt.)

### 2.1 Statistics (EXACT, all avoiders of each N ≤ 11; full histograms in exact_D12_stats.txt)

Highlights at N = 11 (11,066,766 avoiders):

- **LIS/LDS**: identically distributed (forced by the reverse and complement symmetries
  of the class — an internal consistency check that holds exactly). Concentrated:
  LIS ∈ {4,5} for 86.7% of avoiders; extremes LIS=2 (1,148 avoiders) up to LIS=8 (14).
- **Displacement is typical, not exceptional**: max|pos(v)−v| ≥ 7 for 71% of avoiders;
  mean max_v pos(v)/v = 6.45 at N=11 and grows ≈ 0.55·N (SIS, §3): a typical avoider is
  about as displaced as a uniformly random permutation. Value 1 sits at position
  ~N/2 on average, with a smooth symmetric distribution over ALL positions
  (759,963 avoiders have pos(1)=1; 1,172,712 have pos(1)=6). pos(1) and pos(N) are
  identically distributed (symmetry).
- **Fixed points**: ≈ Poisson(1)-like (39.1% have none; max observed 7).
- **Monotone 3-APs**: mean 6.99 per avoider at N=11 (max 13); a uniform random
  permutation of [1..11] would average 8.33. So 4-AP-freeness only mildly suppresses
  3-APs; avoiders are NOT approximately 3-AP-free.

### 2.2 3-AP-free avoiders vs the rest

The 3-AP-free subpopulation (counts 1,066 / 2,460 / 6,128 / 12,840 / 29,380 at
N = 10..14; growth ratio ≈ 2.2–2.3 per step vs ≈ 9–10.6 for all avoiders — an
exponentially vanishing fraction) is structurally extreme:

- LIS support narrows to {4,5} at N=11 (vs {2..8} overall).
- MORE displaced, not less: min max|pos−v| is 6 (vs 2 overall) at N=11; mean
  maxratio 6.59 vs 6.45; pos(1) distribution is flatter with a characteristic dip at
  the exact middle and peaks at positions 5 and 7 (parity-construction signature),
  vs a smooth middle-peaked curve overall.
- Fewer fixed points (max 3 at N=11 vs 7).

Interpretation: the "cleanest" candidates (3-AP-free) are forced into large, rigid,
parity-like displacement; 4-AP-free-only avoiders are vastly more numerous and much
closer to generic permutations carrying a bounded density of 3-APs.

---

## 3. Deliverable 2 — growth of the absolute count

Exact to N=15; SIS beyond (32 batches × 1M samples, seed 196; estimator: uniform
random child along the insertion tree, weight = product of branching factors —
unbiased by construction; empirical relative stderr ≤ 0.15% throughout, validated
against exact values at N ≤ 14). Raw: sis_main.txt.

| N | count | r_N = c(N+1)/c(N) | q_N = r_N/(N+1) | count/N! | ln(count)/N |
|---|------:|---------:|--------:|---------:|------:|
| 8 | 22,266 (EXACT) | 7.584 | 0.843 | 0.552 | 1.251 |
| 12 | 1.01362e8 (EXACT) | 9.371 | 0.721 | 0.212 | 1.536 |
| 16 | 1.0563e12 ± 0.017% | 11.28 | 0.664 | 5.05e-2 | 1.730 |
| 20 | 1.9381e16 ± 0.027% | 12.59 | 0.599 | 7.97e-3 | 1.875 |
| 24 | 5.1605e20 ± 0.056% | 13.40 | 0.536 | 8.32e-4 | 1.987 |
| 28 | 1.8134e25 ± 0.091% | 14.19 | 0.489 | 5.95e-5 | 2.077 |
| 32 | 7.7882e29 ± 0.150% | — | — | 2.96e-6 | 2.151 |

(Full table N = 3..32 in sis_main.txt. The prior "fraction ≈ 5e-4 at N=24" is
confirmed in order of magnitude: 8.3e-4 ± 0.06%.)

**Findings.**
- The absolute count grows SUPERexponentially in the entire observed range: r_N is
  increasing (≈ +0.27/step at N≈30, decelerating slowly), so no c^N law fits;
  ln(count)/N is still climbing at N=32.
- Relative to N!, the count dies: the per-step fraction ratio q_N declines steadily
  0.92 → 0.46 with no visible floor. If q_N → q* > 0 the fraction decays exactly
  exponentially; the data cannot distinguish q* > 0 from q_N → 0 slowly (e.g.
  r_N ~ αN would give q → α). Either way: **absolute counts explode, the fraction
  vanishes** — the question is never about counting but about corridor survival.

---

## 4. Deliverable 3a — extension tree and dead ends

- **Children form an interval** (§1.1), so "branching" = interval length; max possible
  branching n+1 is REALIZED at every level ≤ 14, by a fat positive fraction of
  avoiders: 23.3% of all avoiders of [1..12] accept ALL 13 insertions of value 13
  (22.8% at 13, 21.7% at 14). The extension tree is not merely supercritical, it has a
  persistent bulk of maximally-free nodes.
- **Dead ends first exist at N = 12** (515,296 of 101,361,722 — every avoider of
  [1..11] extends). Brute-force-verified example: (8 12 6 3 11 1 5 9 10 7 2 4) is
  4-AP-free and each of the 13 insertions of value 13 creates a monotone 4-AP.
  Dead-end fraction (EXACT to 14, SIS beyond): 0.51%, 0.58%, 0.65%
  at 12, 13, 14; then 1.4%, 1.4%, 1.5%, 1.9%, 2.0%, 2.0%, 2.8% ... 5.7% at N = 32.
  Slow, roughly linear-in-N creep; no cliff.
- **Branching histograms** (exact_D14.txt): unimodal with a spike at b = n+1; minimum
  nonzero branching 1; mean branching r_N as in §3.
- The full-freedom spike and interval structure say: a positive fraction of avoiders
  put every triple (m−3d, m−2d, m−d) in non-monotone position order simultaneously —
  local obstructions are avoidable in bulk, and obstruction pressure builds only very
  slowly with N.

---

## 5. Deliverable 3b — infinite branches, compactness, and the tame census

**Lemma (König/limit; agrees with CORE.md Lemma 6).** If for some function
φ : ℕ → ℕ the tree of φ-bounded avoiders (pos(v) ≤ φ(v) for all v) has nodes at every
level, then 196-NO holds: the subtree is downward closed (restriction only decreases
positions), finitely branching, hence by König has an infinite branch; along it
pos_n(v) is nondecreasing in n and ≤ φ(v), so converges; the limit is injective, and
surjective onto positions (minimal-missing-position argument: once positions 1..j−1
are final, only slot-j insertions can touch position j, and infinitely many of those
would push some fixed value's position beyond its bound); 4-AP-freeness passes to the
limit because insertion preserves relative order. Conversely a NO-witness a yields
φ-bounded avoiders at every N with φ(v) = pos_a(v). **So 196 is EXACTLY the question
of whether some displacement profile φ survives at every N** — and the census below
measures which φ die and how.

### 5.1 Certified extinctions (EXACT complete enumerations, this route, k = 4)

pos(v) ≤ ⌊Cv⌋ (equivalently max_v pos(v)/v ≤ C):

| constraint | extinct at N | peak level count | total tree size | profile file |
|---|---|---|---|---|
| C = 3/2 | **15** | 78 (at n=13) | 276 nodes | cert_C1.5.txt |
| C = 8/5 | **18** | 670 (14) | 2,168 | cert_C1.6.txt |
| C = 7/4 | **31** | 146,238 (29) | 1,036,992 | cert_C1.75.txt |
| pos ≤ v+1 | **11** | — | 63 | (rerunnable in ms) |
| pos ≤ v+2 | **14** | — | 2,764 | — |
| pos ≤ v+3 | **19** | 43,373 (12) | 168,686 | cert_Kplus3.txt |
| pos ≤ v+4 | **25** | — | 21,051,114 | — |

Additive crossing points are LINEAR in the slack (N*(K) ≈ 4 + ~5.3K for K = 0..4),
versus exponential in C for the multiplicative family (§6.2) — consistent with a
displacement-ratio floor that decays toward 1 as ~O(K/N) additive slack is spread
over [1..N], and further support for the log-growth picture of §6.2.

All show the universal shape: exponential-ish growth → peak → cliff to 0 within 1–2
levels (C=7/4: 146,238 → 6,472 → 0). These are unconditional, computer-verified
statements: e.g. **no 4-AP-free permutation of [1..31] has pos(v) ≤ ⌊7v/4⌋ for all v;
hence (Lemma above) no 4-AP-free permutation of ℕ has pos(v) ≤ 7v/4 for all v.** This
extends Theorem 12's proven C < 9/8 to C ≤ 1.75 (solver-grade, not DRAT-logged;
cross-checked against the SAT route where ranges touch: SAT's ceil-variant
pos ≤ ⌈1.5v⌉, a strictly looser constraint, dies at 22 vs my floor-variant at 15 —
consistent ordering).

### 5.2 The C = 2 tame tree: growth then death, at scale

EXACT level counts (beam widths below cap are exact): 1, 2, 4, 11, 30, 102, 276, 915,
3641, 12443, 41660, 165563, 504289 (n = 1..13). Unbiased tsis estimates (32 batches,
tsis_k4_C2.txt): ≈ 1.24e4 (n=10), ≈ 1.86e6 (14), ≈ 2.3e7 (16), ≈ 1.3e9 (20),
≈ 5.8e10 ± 15% (24) — per-level growth ratio ≈ 2.5–3.4. The tree exceeds 10^13 nodes,
so complete enumeration is out of reach. Yet it dies: beams of width 10^6–4×10^6
(4 seeds/caps) all collapse at levels 50–55 with the signature cliff (10^6 nodes at
level 49 → 29,281 children → 0). Uniform random dives die by 38 (2M dives); weighted
samples die by 42. Explicit VERIFIED witness at N=50 (§8): 4-AP-free, max
pos(v)/v = 2.000. Status: ρ(50) ≤ 2 CERTIFIED by witness; extinction "≈ 55" is beam
evidence only (§6.3 caveat).

### 5.3 Calibrations: k = 3 (known YES) and k = 5 (known NO)

Extinction levels of pos(v) ≤ ⌊Cv⌋ trees (k=3 rows C ≤ 6 are EXACT complete
enumerations; k=4 C ≥ 2 and all k=5 rows are beam horizons — §6.3 caveat):

| C | k=3 (YES known) | k=4 (this problem) | k=5 (NO known) |
|---|---|---|---|
| 1.5 | 5 | 15 (EXACT) | 68 |
| 2 | 10 | ~50–55 | 113 |
| 2.5 | 12 | ~63 | 99* |
| 3 | 13 | ≥ 74 (SAT witness; beams die 59–63: false floor) | 113* |
| 4 | 20 | ~75 | — |
| 6 | 29 | ~79 | — |
| 8 | 36* | ~92 | — |
| 10 | 48* | — | — |
| 16 | 68* | — | — |

(* = beam cap 200K; other beams cap 1M–4M.)

Readings:
- k=3 dies fast at every C — the method correctly detects the known YES.
- **k=5 ALSO dies at small C, although an infinite 5-AP-free permutation exists.** So
  finite tame extinction is NOT a YES-signal; it only says the witness (for k=5, the
  DEGS construction) does not live at linear displacement with small constant.
- k=4 sits strictly between, and closer to k=5 than to k=3 on a log scale
  (at C=2: 10 / ~53 / 113).

---

## 6. Displacement of surviving branches — the empirical φ (added coordinator request)

### 6.1 Exact staircase of ρ(N) := min over avoiders of [1..N] of max_v pos(v)/v

EXACT by census (D=13 run with per-level min tracking; argmin examples in
exact_D13_phi.txt; min over all avoiders = min over extendable avoiders at every
level ≤ 13):

- ρ(N) = 1 for N ≤ 3 (identity survives); ρ > 1 forced at N = 4;
- ρ(N) = 4/3 for 4 ≤ N ≤ 9 (argmin e.g. 1 2 4 3 7 5 8 6 9);
- ρ(N) = 3/2 for 10 ≤ N ≤ 14 (argmin at 13: 1 2 4 3 7 5 8 6 9 12 10 13 11);
- ρ(N) ∈ (1.5, 1.6] for N = 15..17; ∈ (1.6, 1.75] for 18..30; > 1.75 for N ≥ 31
  (from §5.1 certificates + monotonicity of ρ, which holds because restriction only
  lowers positions);
- ρ(50) ∈ (1.75, 2] (witness, §8); ρ(74) ≤ 3 (SAT-route asym witness at N=74);
  beams suggest ρ crosses 2 near N ≈ 55 and 3 near N ≈ 75–100 (heuristic only).

### 6.2 Growth law of the crossing points N*(C) (first N with ρ(N) > C)

Certified points: N*(1)=4, N*(4/3)=10, N*(3/2)=15, N*(8/5)=18, N*(7/4)=31, and
N*(2) ≥ 51. Successive slopes Δln N*/ΔC ≈ 2.7, 2.5, 1.8, 3.6, ≥ 2.0: consistent with
**N*(C) ≈ a·e^{bC}, b ≈ 2.2–2.8**; a quadratic law ~8C² (also floated by the SAT
route) underestimates N*(7/4) = 31 and is disfavored by N*(2) ≥ 51 but not yet dead —
certifying C = 1.8–1.875 exactly and a plain-SAT C=2 kill would discriminate.
Inverting the exponential: **avoiders of [1..N] exist with max pos(v)/v ≈ (1/b)·ln N ≈
0.36–0.45·ln N** — the minimum displacement of surviving branches grows only
LOGARITHMICALLY in N. Meanwhile the TYPICAL avoider has max pos(v)/v ≈ 0.55·N (SIS):
survival at small displacement happens in exponentially thin corridors whose floor
rises like log N.

Consequence for NO-witness design (the "where must a witness live" parametrization):
conditional on extinction at every fixed C — certified ≤ 1.75 for plain avoiders
(this route, complete enumeration; plain-SAT independently ≤ 1.5), certified ≤ 3 for
the asym subclass (SAT route), heuristically supported up to ~8 (beams), open beyond —
any counterexample has limsup pos(v)/v = ∞; but the log-growth of ρ means
profiles as small as pos(v) ≤ v·(log v)^{1+ε} — or even pos(v) ≤ v·max(1, c·log v) —
are consistent with every certificate we have. (The SAT route's superlinear probe —
pos ≤ 2v^{1.5} alive at N = 130+ — fits this picture with room to spare.)

### 6.3 Methodological caution: beams produce false floors (proved instance)

My C=3 beams (caps 1M–4M, several seeds) died at levels 59–63, but the SAT route
exhibits (asym, hence in particular plain 4-AP-free) witnesses with pos ≤ 3v at
N = 74. So beam extinction levels can be ≥ 15 levels below truth: survival corridors
are thinner than 10^-6 of the population but nonempty. All beam numbers above must be
read as "horizon of a 10^6-wide uniform search" — a search-difficulty measure, useful
comparatively across k at fixed cap, never as extinction proof. (My EXACT extinctions
in §5.1 are complete enumerations and unaffected.) By the same token the k=5 "walls"
at 68/99/113 are horizons only.

The probe ladder is strictly ordered everywhere it was measured (uniform dives <
weighted samples < beams < truth): e.g. k=4 C=2: 38 / 42 / 50–55 / ≥ 51;
k=4 C=2.5: 47 / — / 63 / ?; k=4 C=3: — / — / 59–63 / ≥ 74 (SAT); k=5 C=2: 89 / — /
113 / ≥ 113. Each strengthening of the search pushes the apparent wall out; only
complete enumeration (or DRAT-certified UNSAT) pins it.

---

## 7. Which answer does the data lean toward, and why

**Lean: NO, weakly.** Reasons:

1. On every quantitative axis measured here — tame-wall scale, wall growth with C,
   branching, count growth — k=4 clusters with k=5 (the known-NO case) rather than
   with k=3 (the known-YES case), sitting between them but nearer k=5 in log scale.
2. The plain avoider tree is violently supercritical with tiny and slowly-growing
   dead-end pressure; nothing in the finite data hints at global choking. (Weak
   evidence by itself: for k=3 — YES — plain counts also never choke; the YES lives
   entirely in the displacement quantifier.)
3. The corridor phenomenon (§6.3): even at displacement ratio 3, avoiders persist to
   N ≥ 74 through corridors invisible to million-wide searches. Survival keeps being
   real where search says dead, and the empirical φ floor grows only like log N.
4. YES-side assets from this census: the extinction law is real, sharp-cliffed, and
   certified through C = 1.75; the parametrized target "∀φ-extinction" (equivalently:
   prove ρ(N) → ∞, then arbitrary profiles via Lemma 6) is a concrete program, and
   Theorem 12 shows it is provable in nontrivial ranges. If YES is true, THIS is the
   proof shape, and the census supplies its quantitative profile (cliff shapes,
   corridor widths, log-growth floor).

### Next steps (ranked)

1. **Certify the φ frontier upward**: exact floor-DFS for C = 1.8, 1.833, 1.875
   (launched; ~10^10-node trees), plain-SAT (DRAT-logged) kills for C = 2, 2.5, 3 to
   replace beam horizons with certificates and discriminate e^{bC} vs 8C² for N*(C).
2. **Prove a log lower bound for ρ(N)**: multi-scale version of Theorem 12's ledger
   (each dyadic value-scale pays its own drop-sum) targeting ρ(N) ≥ c·log N — the
   first ∀φ step beyond fixed C; kills all pos ≤ Cv NO-architectures at once (gates
   BLOCKS.md linear profiles).
3. **k=5 displacement of the DEGS witness**: derive its pos(v)/v growth. If DEGS
   lives at pos ≤ Cv for concrete C, the k=5 tame-wall divergence point becomes a
   sharp YES/NO discriminator template for k=4; if DEGS is superlinear, the k=4/k=5
   analogy strengthens the NO lean.
4. **Corridor anatomy at C=2–3**: take SAT witnesses at N=60–74, measure pinned
   values (slack 0) and the two-spine pattern (CORE Lemma 11); feed as seeds to
   construction routes (superlinear profiles pos ~ v·log v, blocks with
   logarithmically swelling blocks).
5. Extend exact census to N=15–16 (OpenMP over level-8 subtree roots) if dead-end/
   branching trends near the count peak are needed with certainty.

---

## 8. Artifacts and reproducibility

- census.c — engine (compile: gcc -O3 -march=native -o census census.c -lm).
- validate.py — validation ladder V1–V5 (all pass).
- exact_D12_stats.txt — full statistics histograms N ≤ 11 (+ counts to 13).
- exact_D13.txt / exact_D13_phi.txt / exact_D14.txt — exact counts to 15, censuses,
  empirical-φ argmins.
- sis_main.txt — SIS to N=32 (32×1M, seed 196).
- tsis_k4_C2.txt — unbiased C=2 tame-count estimates.
- tame_k3_mult.txt, cert_C1.5.txt, cert_C1.6.txt, cert_C1.75.txt, cert_Kplus3.txt —
  EXACT extinction profiles.
- beam_*.txt — beam horizons (heuristic; §6.3 caveat).
- tame_certifications.txt / tame_certifications2.txt — exact certification runs
  (second batch: C=1.8, C=1.875, K=+5, C=3 beam seed study).
- Verified N=50, C≤2 witness (permutation of [1..50], no monotone 4-AP, checked
  independently with apcheck; max pos(v)/v = 2.0 exactly):
  1 10 17 2 4 3 8 9 7 5 23 6 25 28 21 22 15 18 20 16 19 11 13 12 37 40 14 46 38 42
  50 49 47 43 48 34 35 39 45 41 44 31 29 33 36 32 26 24 30 27

Key numbers at a glance: counts 101,361,722 (N=12, EXACT) ... 100,130,083,830 (N=15,
EXACT); ≈ 7.79e29 ± 0.15% (N=32, SIS); dead ends start at N=12 (0.51%), reach only
5.7% by N=32; mean branching 14.6 and rising at N=32; certified displacement
extinctions C = 1.5/1.6/1.75 at N = 15/18/31; ρ(N) staircase 1, 4/3, 3/2, ... with
exponential-fit crossing law N*(C) ≈ a·e^{(2.2–2.8)C}.
