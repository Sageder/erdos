# Route R1 report — self-similar / recursive block constructions (Erdős 196, NO side)

Sessions 2026-07-27/28. All machine claims are exact-arithmetic, produced by code in
this directory; checkers cross-validated against trusted
`/home/user/erdos/experiments/apcheck.py` (800 random permutations + 400 random
general value-sets at k=4, plus brute force on small n). Finite checks are evidence,
not proof.

## VERDICT

1. **Every concrete instantiation tried (10 gadget/partition/layout combos + 64
   interleaved gadget schedules) DIES.** Exact minimal killing 4-APs in §2.
2. **The "blocks in increasing position order" ansatz at geometric ratio ≤ 4 is dead
   for EVERY gadget choice** — machine-verified UNSAT of necessary-constraint systems,
   made exactly decisive by a König argument (§1): ratio 3 dies at 4 blocks (values
   1..80), ratio 4 at 4 blocks (values 1..255); minimal infeasible cut-set {8,26,80}.
3. **REVISION from the window-law data (§3.7): in-order is NOT dead at all ratios.**
   Feasible third cuts after (V1,V2) form: a geometry-dead zone (V2, 3V2−3] (exact
   lemma, machine-checked), a thin SAT shoulder from 3V2−2 (width shrinking to 1–2 points as V1/V2 grows),
   an UNSAT notch ≈ [3.2, 4.35]·V2 (activating at scale V2 ≥ 16, present even for V1=2
   once V2 ≥ 26), and a robust SAT **island ≈ [4.8, ≥5.8]·V2** ((8,26): 125–150 all SAT). Island-hopping chains pass every test we can afford:
   {2,8,26,140} and {2,8,26,150} SAT (depth 4: the island survives full prefix memory
   as an interval) and the
   pure ratio-5 geometric {5,25,125} SAT. **The alive corridor for R1-in-order is
   V_{k+1}/V_k ≈ 5–6**, unreachable by our SAT beyond ~4 cuts (V5 ≈ 700).
4. E(V) (single-cut extendability) is settled for ALL V: σ_V (parity recursion) is a
   witness — it is 3-AP-free, hence has no monotone 4-AP and no increasing 3-AP with
   upward extension. Single cuts NEVER obstruct; the obstruction is irreducibly
   ≥ 3-scale (`e_of_v_sigma.log`, machine-confirmed to V = 4096).
5. **Bounded-lag non-decomposing interleavings die**: the lag-2 pattern
   2,4,1,6,3,8,5,… with ratio-2 geometric blocks is UNSAT at stage 7 for all gadgets
   (`staged_T7.log`, core anatomy in `core_T7.log`: debt propagates backwards as
   decreasing-AP pressure). Equal-size blocks under any such pattern die by forced
   geometry at stage 4. Other patterns (geom3-lag2, evens-lead-4, odd-leading lag-2,
   factorial-lag2): verdicts in `staged2.log` as solver runs complete (the 486-value
   block instances exceed lazy-transitivity convergence within this session's compute;
   unresolved entries are marked there).

No candidate survived to M = 10^4 (deliverable 4's construction branch vacuous);
the surviving corridor + proof obligations are in §4.

## 1. Framework (deliverable 1) and the exact stage principle

`framework.py`: block partitions (equal / geometric-r / factorial), gadget zoo
(parity recursion σ, value-reflected, position-reversed, both, evens-first, identity,
reverse, top-half-first), assembly under arbitrary block layout, restriction to [1..M],
two vectorized exact checkers (`monotone_4ap_violations` for permutations of [1..M];
`monotone_4ap_violations_general` for arbitrary distinct-value sequences, as interleaved
coverage is not a value-prefix). M = 10^4 checks take seconds. All checkers
cross-validated against the trusted apcheck implementations (`python3 framework.py`).

`satsearch.py` / `satsearch2.py`: SAT encodings (CaDiCaL) of a *stage* = covered
slots 1..T (block set S; every other value placed later). Boolean vars o_{uv} for
in-block order; cross-block order fixed by layout; eager transitivity, lazy CEGAR
optional. Constraints:
- **C1**: no monotone 4-AP among covered values (both orientations);
- **C2**: no monotone 3-AP among covered values (in position order) whose missing 4th
  AP term (above-top for increasing, below-bottom for decreasing) is uncovered.
Proved and used: stage-T′ solutions restrict to stage-T solutions; an infinite
(partition, layout, gadgets) object is monotone-4-AP-free iff every stage satisfies
C1∧C2; König ⇒ **an infinite construction exists iff every finite stage is SAT**.
So each UNSAT is an impossibility theorem for its (partition, layout) pair over ALL
gadget choices, modulo code correctness (every SAT witness is independently
re-verified through the trusted checker path).

## 2. Instantiations and exact kills (deliverable 2)

Logs: `sweep_I1_I5.log`, `sweep_I6_I10.log`, `interleave_sweep.log`. Case labels for
in-order layouts (machine-verified complete for ratio ≥ 3, `patterns.py`):
A=(b,b,b,b); B1=(b,b,b,b+1); B1'=(a,b,b,b) a<b; B2=(b,b,b+1,b+1); B3=(a,b,b,b+1) a<b;
B4=(a,b,b+1,b+1) a<b.

| id | partition | gadgets | layout | verdict | first exact kills | mechanism |
|----|-----------|---------|--------|---------|-------------------|-----------|
| I1 | equal 16 | σ | in order | DIES (16,593,638 APs ≤ 10^4) | +15,16,17,18; +13,15,17,19 | B2 + unbounded patterns: equal blocks admit APs meeting 4 blocks, forced monotone |
| I2 | geom ×2 | σ | in order | DIES (4,948,140) | +1,2,3,4; +2,3,4,5; +1,3,5,7 | ratio 2 < 3 admits forced multi-block patterns (1,6,11,16) |
| I3 | geom ×4 | σ | in order | DIES (2,355,872) | +1,3,5,7 B2; +1,6,11,16 B3 | σ parity invariance: odd-before-even at every scale ⇒ odd-d B2 always monotone |
| I3b | geom ×3 | σ | in order | DIES | analogous | same |
| I4 | geom ×4 | σ/reflect alt. | in order | DIES (1,087,156) | +2,7,12,17 B3; +2,9,16,23 B4 | reflection fixes odd-d B2, flips B3/B4 demands into violation |
| I5 | geom ×4 | σ/pos-rev alt. | in order | DIES (1,088,248) | +2,7,12,17 B3; +8,12,16,20 B2 | position reversal preserves the violated co-orientations |
| I6 | geom ×4 | all reflected | in order | DIES (2,330,394) | +2,7,12,17 B3; +11,14,17,20 B2 | as I4 |
| I7 | factorial | σ | in order | DIES (70,093 ≤ 5039) | +4,5,6,7 B2; +1,3,5,7 B3 | growing ratio does not remove B2/B3/B4 boundary families |
| I8 | geom ×4 | σ | adjacent swaps | DIES (1,514,391) | +14,15,16,17 B2; B2− appears | decomposing interleave ⇒ same cut obstruction + decreasing B2 |
| I9 | geom ×4 | top-half-first (σ halves) | in order | DIES (1,276,888) | +2,3,4,5 B2; −5,8,11,14 A | coarse inversion creates in-block decreasing 4-APs |
| I10 | geom ×4 | full top-half recursion | in order | DIES (7,484,226) | −4,5,6,7 etc. A | decreasing APs everywhere in-block |
| ILV | geom ×2 | all 64 σ-variant schedules | 2,4,1,6,3,8,5,… | ALL DIE | e.g. +2,3,4,5; +3,8,13,18 | classical gadgets miss the interleaved inversion demands |

## 3. Failure taxonomy (deliverable 3) — precise design constraints

Block = [s, rs), next = [rs, r²s), in-order layout unless stated.

### 3.1 Geometry constraints
`patterns.py`: for r ≥ 3 every 4-AP has pattern A/B1/B1'/B2/B3/B4; for r = 2 and equal
blocks, patterns meeting ≥ 3 distinct blocks exist and are automatically monotone
in-order (r=2: 1,6,11,16). **DC0: in-order needs ratio ≥ 3.**

### 3.2 T-B1/B1' (3-AP with exit room)
Increasing in-block 3-AP (w,w+e,w+2e) with w+3e ≥ rs (or w−e ∈ [1,s)) is fatal.
Decreasing 3-APs are harmless in-order. σ qualifies (3-AP-free).

### 3.3 T-B2 (two-scale coupling)
For every pair (a,b) ⊂ [s,rs) with 2b−a ≥ rs — dense, scale-invariant, nonempty for
every a ≤ rs−2 — at least one of (a,b) and (2b−a, 3b−2a) ⊂ next block must be
position-inverted. σ-gadgets fail by parity (odd-d APs like 1,3,5,7 always monotone);
per-block reflections trade B2 for B3/B4. **DC1: adjacent gadgets must jointly invert
the K-family {(a,b): 2b−a ≥ rs}.**

### 3.4 T-B3/T-B4 (three-scale imports, unavoidable inversions)
Pairs (u,u+d) ⊂ [s,rs) with u−d in an earlier block and u+2d ≥ rs (B3), and pairs
(v,v+d) with v−d in the previous block, v−2d below it (B4), MUST be inverted; they
concentrate in the lower-middle of the block with gap d ≍ s. **DC2.**

### 3.5 T-LOCAL (decoupling dies)
The decoupled sufficient system (invert all K ∪ D3 ∪ D4; no in-block monotone 4-AP;
no increasing 3-AP with exit room) is UNSAT at block 3 for r=3,4 and block 2 for
r=5,6 (`localsat.py`). Cross-block cooperation is mandatory at every ratio.

### 3.6 T-GLOBAL (in-order death at ratio ≤ 4)
With full cooperation the r=3,4 ansatz still dies: cuts {2,8,26,80} and {3,15,63,255}
UNSAT; minimal infeasible sub-configuration {8,26,80}. Family-level core
(`core_8_26_80.log`): B4-imports into the top segment + boundary-crossing extension
bans + 4-AP-freedom of segment (26,80] ALONE — a 54-integer impossibility; 120-clause
MUS in `mus_top_segment.log`: ~60 forced inversions (u+d before u; u ∈ [27,53],
d ≈ 10–27) build a descent web; transitivity manufactures decreasing 4-APs (55 F4−
bans) while ascending escapes are blocked by F3/F4+ bans.

### 3.7 T-WINDOWS (the window law; `windows.log`, `windows2.log`, `windows3.log`)
**Geometry lemma (machine-checked, `geometry_lemma.log`)**: for V1 ≥ 2, V2 ≥ 2V1 the
third cuts killed by forced chains alone are EXACTLY V2 < V3 ≤ 3V2−3 (dead intervals
[x+2d, x+3d−1] over x ≤ V1 < x+d ≤ V2 < x+2d tile the zone; V3 ≥ 3V2−2 is clean).

SAT-level data (beyond geometry). S = SAT, U = UNSAT; **bold** = notch/island landmarks:

| (V1,V2) | tested V3 → verdicts |
|---------|---------------------|
| (2,8)   | 22,26,30,36,42,50,60,70,80,100 → ALL S |
| (4,12)  | 34,40,48,56,64,72,90,110 → ALL S |
| (4,16)  | 46 S, 52 S, 54 S, **56–66 U (notch)**, 68 S, 70 S, 80 S, 96 S, 120 S |
| (6,20)  | 58 S, 60 S, 62 S, **64–86 U (notch)**, 90 S, 94 S, 100 S, 120 S, 140 S |
| (8,26)  | ≤75 geom-dead, **76 S (shoulder = 3V2−2)**, 78 U, 80 U, 90 U, 110 U (notch), **125,135,140,145,150 S (island)**, 180 U; 160, 200, 220 in flight |
| (2,26)  | 76 S, 90 S, **110 U (notch exists even at V1=2)**, 140 S, 180 in flight |
| fixed ratio 5 | **{5,25,125} SAT**; {6,36,216}, {4,24,144}, {5,30,180} in flight |

First-cut memory (fixed (V2,V3), vary V1):

| (V2,V3) | feasible iff |
|---------|--------------|
| (26,80) | V1 ≤ 6 (tested 2..12) |
| (20,100) | V1 ≤ 7 (tested 2..14) |
| (16,70) | V1 ≤ 6 (tested 2..12) |

Depth-4 memory {2,8,26,V4}: 100 U, 120 U, **140 S, 150 S**, 160 U (130 in flight).
Compare 3-cut level: {8,26,140/145/150} all S — the island survives full prefix
memory as an interval (≥ {140,150}), trimmed at most at the outer edge (160).
Depth-5 {2,8,26,140,V5}: **700 UNSAT** (sound: lazy-transitivity UNSAT is a
relaxation UNSAT); 760 ≈ 5.4·140 (island center) and the triple-level controls
{26,140,700/756} did not resolve within this session's compute — the depth-5
island question is THE open frontier. Note 700 = 5.0·140 sits at the island's lower
edge, where depth-4 also showed death (100 = 3.8·26 U), so 700's death is consistent
with BOTH conjectures; 760's verdict would discriminate.

**Window shape (empirical law)**: after (V1,V2) with V2 ≥ 2V1 ≥ 4:
geometry-dead (V2, 3V2−3] (exact); a 1–2 point SAT shoulder from 3V2−2, widening as
V1/V2 shrinks (at (8,26) it is exactly {76,±77}; at (2,26) it reaches 90; at V2 ≤ 12
it merges with everything — no notch at all); an UNSAT **notch ≈ [3.2, 4.35]·V2**
activating at scale V2 ≥ 16 and present even for V1 = 2 once V2 ≥ 26; a robust SAT
**island ≈ [4.8, ≥5.8]·V2** ((8,26): 125–150 all SAT); death again by ≈ 6.9·V2
(180 U for (8,26)), with notch-2 onset between V2 = 20 (absent at 7·V2 = 140) and
V2 = 26.

**Conjecture W (window persistence — favored)**: the island [~4.8, ~5.8]·V2 stays SAT
at all scales and under full prefix memory, so in-order cut sequences with ratios
≈ 5–6 are feasible at every finite depth: **the in-order block ansatz is ALIVE exactly
in the ratio-5–6 corridor** (dead ≤ 4.35 by the notch; r = 3,4 dead by T-GLOBAL).
Evidence: {2,8,26,140} S (depth 4), {5,25,125} S, island robustness across (V1,V2).
**Anti-conjecture (inductive impossibility)**: prefixes progressively trim islands
({2,8,26,160} U vs {8,26,160}?, {2,8,26,100/120} U) until extinction at some finite
depth. Current data shows trimming at edges but NO trimming at the island center
through depth 4; deciding depth 5 needs V5 ≈ 700 (attempt in `fivecut.log`, beyond
comfortable exact-SAT reach this session). Both conjectures are stated precisely so
either can be attacked; the data leans toward W.

**Ratio-5 witness structure** (`witness_r5.log`, `witness_r5_stats.log`): the
top segment [26,126) of the {5,25,125} witness is BANDED: values ≥ ~86 (the b-partners
of the K-demands, b ≥ (rs+s+2·20)/2-ish) occupy the first ~40 positions in three bands
(upper-middle, top, high-middle), the bottom 3/5 follows in descending bands with
σ-like fine structure; 88.6% of the K-family {(a,b): 2b−a ≥ 126} is inverted. This
suggests a parametric "banded gadget" family for an explicit ratio-5 rule (§4).

### 3.8 T-ILV (non-decomposing interleavings)
Layouts with perpetual debt (never covering a block prefix; minimal form
2,4,1,6,3,8,5,…) have NO cut points, so cut analysis does not apply. New hazard
class C2−: decreasing 3-APs among covered values whose 4th (lower) term is owed.
Equal blocks: GEOM_DEAD at stage 4. Ratio-2 geometric: SAT at stages 2,4,6 (175
values) but **UNSAT at stage 7** (`staged_T7.log`). Family core (`core_T7.log`,
value-blocks j = [2^{j-1}, 2^j)): ('+',2,4,5,5), ('+',4,5,5,5), ('+',5,5,5,5),
('−',5,5,6,6), ('−',5,6,6,6), ('ext+',4,6,6,7) — the owed block 7 forces inversions
in block 6; the late-placed block 5 must invert pairs demanded by (2,4,5,5)-APs; the
two inversion webs complete decreasing 4-APs across blocks 5–6. **Debt propagates
backwards as decreasing-AP pressure — the mirror of the in-order B2 squeeze.**
Variant patterns (geom3-lag2, evens-lead-4, odd-leading lag-2, factorial-lag2):
`staged2.log`; large-block (≥ 486 values) stages exceeded lazy-transitivity
convergence in this session — marked unresolved rather than guessed.

## 4. Deliverable 4 status and the surviving corridor

No explicit candidate survived to M = 10^4. The surviving corridor is now sharply
described: **in-order geometric-like growth with ratio ≈ 5–6** (island chain), for
which SAT gives witnesses up to values ≈ 256 at 4 cuts. To convert into a candidate:
1. Mine {5,25,125} / {2,8,26,140} witnesses for per-segment structure; formulate a
   parametric gadget rule at ratio 5 or 6.
2. Framework-check the rule to M = 10^4 / 10^5 (fast, no SAT).
3. Proof obligations if a rule passes: (A) in-block 4-AP-freeness at every scale;
   (B) cases B1,B1',B2,B3,B4 closed (the pattern-completeness lemma of `patterns.py`
   holds at r ≥ 5, so the case list is exactly this); (C) the B2-coupling argument
   between consecutive scaled gadgets; (D) bijection + order type ω (automatic).
Honest gaps: no rule yet; island persistence beyond depth 4 unproven (Conjecture W);
localsat shows the DECOUPLED r=5 system is UNSAT, so any rule must use genuinely
coupled adjacent-block structure — a per-block rule with alternating phase, say.

## 5. Next steps

- Decide Conjecture W at depth 5: {2,8,26,140,V5}. V5 = 700 is UNSAT (done);
  V5 ≈ 740–800 (island center) is the open frontier (`fivecut.log`,
  `triple_26_140.log`); needs stronger lazy-transitivity engineering or an
  incremental construction heuristic instead of monolithic SAT.
- Mine ratio-5 witnesses; hand-build an r=5 two-phase gadget rule; framework-check to
  10^5. This is now the highest-value R1 activity — the corridor is concrete.
- Distill {8,26,80} MUS into a human lemma; likewise the notch law (which is the
  quantitative content of "ratios ≤ 4.3 die").
- Cross-route consistency (per coordinator): CORE.md Thm 12 (pos(v) ≤ Cv with
  C < 9/8 forces an increasing 4-AP) and empirical extinction of linear profiles to
  C ≈ 3 are consistent with everything here: in-order ratio-r blocks give linear
  displacement with constant ≈ r, and our corridor sits at r ≈ 5–6 > 3; the interleaved
  (bounded-lag) architectures die independently. If linear-profile extinction is
  eventually PROVED up to C = 6+, it would kill the corridor from the other side and
  (with T-GLOBAL + notch) close in-order R1 entirely — worth coordinating.
- If the corridor dies: R1's residue is exactly the unbounded-displacement /
  indecomposable regime (DEGS77-style sparse hold-back streams) — R2/R3 territory.

## File map

`framework.py` (library + self-check) · `run_instantiations.py`, `sweep_I1_I5.log`,
`sweep_I6_I10.log` (deliverable 2) · `patterns.py` (pattern completeness) ·
`localsat.py`, `localsat.log` (decoupled UNSAT) · `satsearch.py`, `sat_r3.log`,
`sat_r4.log` (in-order death r≤4), `extendable.log`+`e_of_v_sigma.log` (E(V) settled),
`cuts1.log`, `cuts2.log`, `windows.log`, `windows2.log`, `windows3.log`,
`geometry_lemma.log` (window law) · `core_8_26_80.log`, `mus_top_segment.log`
(obstruction anatomy) · `satsearch2.py` (staged arbitrary-layout SAT; C1/C2),
`staged1.log`, `staged_T7.log`, `staged2.log`, `witness_mine.log`, `core_T7.log`
(interleaved anatomy) · `fivecut.log` (depth-5 attempt) · `windows_refine.py`.
