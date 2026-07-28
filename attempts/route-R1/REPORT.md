# Route R1 report — self-similar / recursive block constructions (Erdős 196, NO side)

Session 2026-07-27. All machine claims are exact-arithmetic, produced by code in this
directory; checkers cross-validated against trusted `/home/user/erdos/experiments/apcheck.py`
(800 random permutations + 400 random general value-sets at k=4, plus brute force on small n).
Finite checks are evidence, not proof.

## VERDICT (route status: largely CLOSED by machine impossibility proofs; two narrow corridors remain)

1. **Every concrete instantiation tried (10 gadget/partition/layout combos + 64 interleaved
   gadget schedules) DIES.** Exact minimal killing 4-APs listed in §2.
2. **Far stronger: the "blocks in increasing position order" ansatz is dead at geometric
   scaling for EVERY gadget choice.** SAT-encoded necessary constraints, with a König
   argument making finite stages exactly decisive (§1):
   - ratio 3, blocks [1,3),[3,9),[9,27),[27,81): **UNSAT** at 4 blocks (values 1..80);
   - ratio 4, blocks [1,4),...,[64,256): **UNSAT** at 4 blocks (values 1..255);
   - minimal infeasible cut-set **{8, 26, 80}** — all of its sub-cut-sets are feasible.
3. The obstruction is inherently **three-scale**: single cuts never obstruct
   (E(V) SAT for all V tested up to 120), cut PAIRS never obstruct (all tested SAT),
   geometric triples die. Feasible third cuts form a bounded WINDOW:
   after cuts (8,26): V3 <= 79 geometry-dead, V3 in {90,110} UNSAT, V3 = 140 SAT,
   V3 = 180 UNSAT again. Non-monotone in V3 — a corridor of tuned accelerating cut
   sequences remains open but untestable beyond 3 cuts at current SAT sizes (§3 T-CUTS).
4. **Decomposing interleavings** (adjacent block swaps etc.) die by reduction to the same
   cut obstruction (a lookahead-1 swap of ratio-2 blocks IS the dead cut-set {3,15,63,255}).
5. **Non-decomposing interleavings** (perpetual debt; no cut points), the only structural
   escape: layout 2,4,1,6,3,8,5,... with ratio-2 geometric blocks is SAT through stage 6
   (175 values placed, values up to 255), **UNSAT at stage 7** — the held-back block
   [16,32) cannot be inserted, for ANY gadgets. UNSAT-core mechanism in §3 T-ILV:
   the debt (owed block [64,128)) forces inversions in the block above it, which combine
   with inversions forced in the late-placed small block to complete decreasing 4-APs.
   Variant patterns/partitions: see `staged2.log` (geom3-lag2, evens-lead-4, odd-leading
   lag-2, factorial-lag2) — status recorded there as runs complete.

No candidate survived to M = 10^4, so deliverable 4's construction branch is vacuous;
the honest statement of what remains alive, with proof obligations, is §4.

## 1. Framework (deliverable 1) and the exact stage principle

`framework.py`: block partitions (equal / geometric-r / factorial), gadget zoo
(parity recursion σ, value-reflected, position-reversed, both, evens-first, identity,
reverse, top-half-first), assembly under arbitrary block layout, restriction to [1..M],
and two vectorized exact checkers (`monotone_4ap_violations` for permutations of [1..M];
`monotone_4ap_violations_general` for arbitrary distinct-value sequences — needed because
interleaved coverage is not a value-prefix). Checks at M = 10^4 take seconds; all
checkers cross-validated against the trusted apcheck implementations (`python3 framework.py`).

`satsearch.py` / `satsearch2.py`: a *stage* of a block construction = covered slots 1..T
(block set S, all other values placed later). Boolean vars o_{uv} for in-block order,
cross-block order fixed by layout; eager transitivity (lazy CEGAR optional). Constraints:
- **C1**: no monotone 4-AP among covered values (both orientations);
- **C2**: no monotone 3-AP among covered values (position order) whose missing 4th AP term
  (above-top for increasing, below-bottom for decreasing) is uncovered — it arrives later
  and completes a monotone 4-AP.
Proved and used: (restriction) stage-T' solutions restrict to stage-T solutions;
(completeness) an infinite (partition, layout, gadgets) object is monotone-4-AP-free iff
every stage satisfies C1∧C2 — the last-arriving term of any monotone 4-AP is last in
position, so the other three are a C2 violation one stage earlier (same-block ties: C1);
(König) finite branching + restriction ⇒ **an infinite construction exists iff every
finite stage is SAT**. Hence each UNSAT below is an impossibility THEOREM for its
(partition, layout) pair, quantified over all gadget choices, modulo only code correctness
(mitigated by: independent re-verification of every SAT witness through the trusted
checker path, and the eager/CEGAR paths agreeing where both were run).

## 2. Instantiations and exact kills (deliverable 2)

Logs: `sweep_I1_I5.log`, `sweep_I6_I10.log`, `interleave_sweep.log`. Case labels for
in-order layouts (machine-verified complete for ratio >= 3 in `patterns.py`):
A=(b,b,b,b); B1=(b,b,b,b+1); B1'=(a,b,b,b) a<b; B2=(b,b,b+1,b+1); B3=(a,b,b,b+1) a<b;
B4=(a,b,b+1,b+1) a<b.

| id | partition | gadgets | layout | verdict | first exact kills | mechanism |
|----|-----------|---------|--------|---------|-------------------|-----------|
| I1 | equal 16 | σ | in order | DIES (16,593,638 APs at M=10^4) | +15,16,17,18; +13,15,17,19 | B2 plus unbounded 'other' patterns: equal blocks admit APs meeting 4 distinct blocks, forced monotone |
| I2 | geom ×2 | σ | in order | DIES (4,948,140) | +1,2,3,4; +2,3,4,5; +1,3,5,7 | ratio 2 < 3 admits forced multi-block patterns (1,6,11,16 meets 4 blocks) |
| I3 | geom ×4 | σ | in order | DIES (2,355,872) | +1,3,5,7 B2; +1,6,11,16 B3 | σ parity invariance: odd-before-even at every scale ⇒ B2 with odd d always monotone |
| I3b | geom ×3 | σ | in order | DIES | analogous | same |
| I4 | geom ×4 | σ/reflect alternating | in order | DIES (1,087,156) | +2,7,12,17 B3; +2,9,16,23 B4 | reflection fixes odd-d B2, flips B3/B4 demand families into violation |
| I5 | geom ×4 | σ/pos-reversed alt. | in order | DIES (1,088,248) | +2,7,12,17 B3; +8,12,16,20 B2 | position reversal preserves the violated co-orientations |
| I6 | geom ×4 | all reflected | in order | DIES (2,330,394) | +2,7,12,17 B3; +11,14,17,20 B2 | as I4 |
| I7 | factorial | σ | in order | DIES (70,093 at M=5039) | +4,5,6,7 B2; +1,3,5,7 B3 | growing ratio does not remove boundary families B2/B3/B4 |
| I8 | geom ×4 | σ | adjacent swaps | DIES (1,514,391) | +14,15,16,17 B2; B2− appears | decomposing interleave ⇒ same cut obstruction + new decreasing B2 |
| I9 | geom ×4 | top-half-first (σ halves) | in order | DIES (1,276,888) | +2,3,4,5 B2; −5,8,11,14 A | coarse inversion creates in-block decreasing 4-APs |
| I10 | geom ×4 | full top-half recursion | in order | DIES (7,484,226) | −4,5,6,7 etc. A | decreasing APs everywhere in-block |
| ILV | geom ×2 | all 64 σ-variant schedules | 2,4,1,6,3,8,5,... | ALL DIE | e.g. +2,3,4,5; +3,8,13,18 | classical gadgets miss the interleaved inversion demands |

## 3. Failure taxonomy (deliverable 3) — precise design constraints

Block = [s, rs), next = [rs, r²s), in-order layout unless stated. Machine-verified
(`patterns.py`): for r >= 3 every 4-AP has pattern A/B1/B1'/B2/B3/B4; for r = 2 and for
equal blocks, patterns meeting >= 3 distinct blocks exist and are automatically monotone
in-order (r=2 example: 1,6,11,16). **DC0: in-order needs ratio >= 3.**

- **T-B1**: increasing in-block 3-AP (w,w+e,w+2e) with w+3e >= rs is fatal (upper extension
  lands later); dually B1' with w−e in [1,s). Decreasing 3-APs are harmless in-order.
  ⇒ gadgets must avoid all increasing 3-APs with exit room. σ qualifies (3-AP-free).
- **T-B2 (two-scale coupling)**: for every pair (a,b) ⊂ [s,rs) with 2b−a >= rs — a dense,
  scale-invariant family, nonempty for every a <= rs−2 — the AP (a, b, 2b−a, 3b−2a) has its
  upper pair in the next block; at least one of the two pairs must be position-inverted.
  σ-type gadgets fail by parity: for odd d, odd term precedes even term at every scale of σ,
  so 1,3,5,7 and all scaled copies are monotone. Per-block reflections trade B2 for B3/B4
  (I4–I6 data). **DC1: adjacent gadgets must jointly invert the K-family {(a,b): 2b−a >= rs}.**
- **T-B3/T-B4 (three-scale imports, unavoidable)**: pairs (u,u+d) ⊂ [s,rs) with u−d in an
  earlier block and u+2d >= rs (B3), and pairs (v,v+d) with v−d in the previous block and
  v−2d below it (B4) MUST be inverted — the other two AP terms sit in distinct other blocks
  with forced relative order. Demands concentrate in the lower-middle of the block, gap d ≍ s.
- **T-LOCAL**: the decoupled sufficient system (invert all K ∪ D3 ∪ D4; no in-block monotone
  4-AP; no increasing 3-AP with exit room) is **UNSAT** at block 3 for r=3,4 and already at
  block 2 for r=5,6 (`localsat.py`). No "same local rule each block" construction exists;
  cross-block cooperation is mandatory.
- **T-GLOBAL (in-order death)**: with full cooperation the ansatz still dies:
  cuts {2,8,26,80} and {3,15,63,255} UNSAT; minimal infeasible sub-configuration {8,26,80}.
  Family-level core (`core_8_26_80.log`): B4-imports (0,1,2,2)+ into the top segment,
  boundary-crossing extension bans (ext+ (1,2,2) and (2,2,2)), and 4-AP-freeness of
  segment (26,80] ALONE — a 54-integer impossibility. A 120-clause MUS
  (`mus_top_segment.log`): ~60 forced inversions (u+d before u; u in [27,53], d ≈ 10–27)
  build a dense descent web; transitivity then manufactures decreasing 4-APs (55 F4− bans),
  and the ascending escapes are blocked by F3/F4+ increasing bans. 
- **T-CUTS (feasibility windows, forced acceleration)**: {V1,26,80} SAT iff V1 <= 6.
  {8,26,V3}: geometry-dead V3 <= ~79; UNSAT at 90, 110; SAT at 140; UNSAT at 180.
  So the 3rd-cut window after (8,26) is roughly [~112..~170] — bounded on BOTH sides:
  cut sequences must accelerate, but not too fast, and geometric spacing at any fixed
  ratio hits a dead triple. Whether some tuned super-geometric sequence survives all
  depths is open (4th cuts ~700 exceed current exact-SAT reach).
- **T-ILV (non-decomposing escape and its own death)**: layouts with perpetual debt
  (never covering a prefix of blocks; minimal form: evens lead by one, odds owed —
  2,4,1,6,3,8,5,...) have NO cut points, so T-GLOBAL does not apply. New hazard class
  **C2−**: decreasing 3-APs among covered values whose 4th (lower) term is owed.
  Equal blocks: GEOM_DEAD at stage 4 (forced chains). Ratio-2 geometric: SAT at stages
  2,4,6 (up to 175 values placed) but **UNSAT at stage 7** (`staged_T7.log`).
  Family core (`core_T7.log`, blocks numbered j = [2^{j-1},2^j), slot order 2,4,1,6,3,8,5):
  ('+',2,4,5,5), ('+',4,5,5,5), ('+',5,5,5,5), ('−',5,5,6,6), ('−',5,6,6,6),
  ('ext+',4,6,6,7): the owed block 7 = [64,128) forces pair-inversions in block 6 = [32,64)
  (increasing 3-APs anchored in block 4 would complete into block 7); the late-placed
  block 5 = [16,32) must invert pairs demanded by (2,4,5,5)-APs; the two inversion webs
  assemble decreasing 4-APs across blocks 5–6. **Debt propagates backwards as
  decreasing-AP pressure — the mirror image of the in-order B2 squeeze.**

## 4. Deliverable 4 status: no survivor at M = 10^4; alive corridors + proof skeleton

No instantiation or SAT-derived object reaches M = 10^4 alive. Alive-unknown corridors:

- (a) **Tuned accelerating in-order cut sequences** (T-CUTS windows). Needs: window law
  W(V1,V2) = set of feasible V3; then an infinite sequence with V_{k+2} ∈ W(V_k,V_{k+1})
  at every k, PLUS feasibility of all longer prefixes (windows are only the 3-cut
  projection — 4-cut constraints will narrow them further; {2,8,26} SAT but {2,8,26,140}
  untested beyond memory-feasible sizes today).
- (b) **Non-decomposing layouts other than lag-2/ratio-2** (staged2.log: geom3-lag2,
  evens-lead-4, odd-leading, factorial-lag2). Any surviving pattern would next need a
  closed-form gadget rule mined from SAT witnesses (`witness_mine.log`; the stage-6
  witness blocks are structurally irregular — no classical rule matches).

Proof skeleton IF a rule is found for a corridor-(b) family — obligations:
1. Lemma A (in-block): the rule's gadget has no monotone 4-AP.
2. Lemma B (C1 cross-block): all covered-pattern families non-monotone in BOTH
   orientations (interleaving makes decreasing cross-block patterns possible, unlike in-order).
3. Lemma C (C2): no increasing 3-AP with uncovered upper term at any stage; no decreasing
   3-AP with owed lower term at any stage (the new obligation class).
4. Lemma D: bijectivity + order type ω (automatic: finite blocks, bijective slot pattern).
Honest gaps: no candidate rule exists; stage-8+ feasibility of any pattern unknown;
no structural theory of which debt patterns relieve rather than concentrate the
decreasing-AP pressure.

## 5. Next steps

- Complete `staged2.log` variants; if ALL die at small stages, declare bounded-debt
  block ansätze dead and hand R1's remains to unbounded-displacement designs
  (DEGS77-style sparse hold-back streams — closer to R2/R3 than to block constructions).
- Distill the {8,26,80} MUS into a human lemma; extract the exact 3-cut window law
  W(V1,V2) on small sizes; attempt an inductive impossibility ("every infinite cut
  sequence eventually contains a dead triple/quadruple") — if it succeeds, EVERY
  monotone-4-AP-free permutation of N is eventually indecomposable (no cut points
  past V*), a structure theorem valuable on the YES side as well.
- Probe E(V) beyond 120 with CEGAR; if E(V*) ever fails, unconditional indecomposability
  past V* follows for any counterexample — a major YES-side lemma.

## File map

`framework.py` (library + self-check) · `run_instantiations.py`, `sweep_I1_I5.log`,
`sweep_I6_I10.log` (deliverable 2) · `patterns.py` (pattern completeness) ·
`localsat.py`, `localsat.log` (decoupled UNSAT) · `satsearch.py`, `sat_r3.log`,
`sat_r4.log` (in-order death), `extendable.log` (E(V)), `cuts1.log`, `cuts2.log`
(cut landscape) · `core_8_26_80.log`, `mus_top_segment.log` (obstruction anatomy) ·
`satsearch2.py` (staged arbitrary-layout SAT; C1/C2 system), `staged1.log`,
`staged_T7.log`, `staged2.log`, `witness_mine.log`, `core_T7.log` (interleaved anatomy).
