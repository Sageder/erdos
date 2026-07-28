# NOTES.md — lab notebook, newest entries at top

## 2026-07-28 later (route R1): MAJOR REVISION — in-order corridor at ratio 5-6 is ALIVE
- Window law refined (attempts/route-R1/windows*.log): after cuts (V1,V2):
  geometry-dead (V2, 3V2-3] (exact lemma, machine-checked); 1-2 point SAT shoulder at
  3V2-2; UNSAT notch ~ [3.2, 4.35]*V2 (activates by V2=16, present even for V1=2 at
  V2=26); robust SAT ISLAND ~ [4.8, 5.8+]*V2 ((8,26): 125,135,140,145,150 all SAT).
- Depth-4 memory: {2,8,26,140} SAT (!), {2,8,26,100/120/160} UNSAT — island survives
  under full prefix but seems narrowed at edges (150-comparison running).
- Pure geometric ratio 5: {5,25,125} SAT. So earlier "in-order dead" verdict is scoped:
  DEAD for ratios <= 4.3 (notch) and r=3,4 staged (Koenig-exact); ALIVE-UNKNOWN in the
  ratio-5-6 island corridor. r=5 witness has clean banded structure (witness_r5_stats.log):
  top-2/5 of block first (banded), bottom-3/5 after; 88.6% of K-family inverted.
- E(V) settled for ALL V via sigma_V witness (e_of_v_sigma.log): single cuts never
  obstruct; obstruction irreducibly >= 3 scales.
- V1-memory thresholds: {V1,16,70} feasible iff V1<=6; {V1,20,100} iff V1<=7; {V1,26,80} iff V1<=6.
- Next: depth-5 island test (V5 ~ 700, fivecut.log, CEGAR); r=5 banded gadget rule + framework
  check to 1e5. Consistency with CORE.md Thm 12 (C<9/8) and linear-extinction C=3: corridor
  sits at displacement constant ~5-6, not yet excluded by those results.


## 2026-07-28 R4 displacement-class thresholds (attempts/route-R4/)
- CERTIFIED extinction thresholds (min N with NO 4-AP-free permutation of [1..N]), each
  by >=2 independent engines (fast/fast2 DFS + CaDiCaL order-encoding + CP-SAT spot checks;
  witnesses re-verified by apcheck): pi(v)<=floor(Cv): C=1 -> N=4, 3/2 -> 15, 7/4 -> 31,
  15/8 -> 37. Ceil profile (sat_order "plain"): 5/4 -> 14, 3/2 -> 22 (reproduces the SAT
  campaign exactly, cross-toolchain). a(i)<=floor(Ci): 3/2 -> 17. BOTH bounds (C=2!):
  max SAT N=49, UNSAT N=50..56 (CaDiCaL; N=50 also CP-SAT). Sequences a(i)<=Ci (no
  surjectivity): 5/4 -> 6 (5-node tree, hand-checkable), 4/3 -> 18 => THEOREM: every
  permutation of N with a(i) <= 4i/3 for all i contains a monotone 4-AP.
- Corollary chain: any 4-AP-free permutation of N has some v<=37 with pos(v) > 15v/8;
  cannot satisfy pos(v)<=2v AND a(i)<=2i jointly beyond N=49-prefixes.
- Frontier still ALIVE (witnesses): one-sided pi(v)<=2v at N>=49 (pending @50), C=5/2
  ceil at N>=60, C=3 at N>=60; sequences 3/2 at N>=34.
- Survivor structure (complete populations + SAT enumeration, results/mining.txt):
  rigid forced heads (all 6472 last A-7/4 survivors share positions 1-8 =
  1,7,2,4,3,9,8,5), both walls saturated, dyadic upper-half-first blocks with defect
  values parked exactly at pi(v)=2v; clean UL rule fails at N=15 (verified) — defects
  are essential. LIS ~ 2 sqrt(N).
- Data: route-R4/results/{frontier.jsonl,counts.jsonl,thresholds.tsv,mining.txt},
  avoiders/ (377 verified witnesses), survivors/ (complete last populations).

## 2026-07-28 ~audit+scan update
- AUDIT COMPLETE (fresh-context agent, appended to AUDITS.md): 13/15 items SOUND, no
  circularity, compactness step genuinely preserves order type ω. Two REPAIRABLE gaps,
  both repaired in CORE.md and re-pushed: (1) Thm 12's limsup clause was a sup/limsup
  slip — fixed via additive-slack ledger (auditor machine-verified: C=11/10 with slack
  Q=50 still fails at N=4522); (2) Lemma 13(b) strict g2>2g1 overclaimed the e=g1
  boundary (counterexample: (1,2,4,3), Γ={1,2,3}) — weakened to e≥g1; dyadic-window
  consequence survives. Auditor also independently recounted asym witness counts (match)
  and verified the finite form of Thm 12 NEVER fails at C=9/8 (N<3000) while failing at
  N=22/40/43 for C=1.1/1.111/1.1125 — the 9/8 constant is exactly where the ledger dies.
- CORRECTION (asym_pos2.py): pinning ONLY pos(2)<=5 in the asym target is still SAT at
  N=305 — the huge pos(2) delays seen in solver witnesses were NOT forced. Single-value
  pinning does not kill asym; extinction needs JOINT initial-segment constraints
  ([1..15]@2v at C=2). R11 stays alive. FIN-type criteria must quantify over segments.
- R9 partially returned (numbers audited, certification batch still computing; will
  finalize itself). Remaining: R2, R3, R4, R6, R8, R1-corridors + shallow_scan +
  plain C>=2 thresholds.

## 2026-07-28 — route R6 FILED (attempts/route-R6/REPORT.md): density route + LP merge
- Deliverables complete: L0-L3 + infinite Dilworth (constructive patience version;
  false variants refuted), T1-T6 necessary conditions, ALL machine-verified
  exhaustively on avoiders N<=9 (N=10 pass still running post-restart).
- CORRECTION: brief's calibration example (reversed DYADIC blocks) is WRONG — it has
  increasing 4-APs ((1,6,11,16) at pos (1,5,12,31)). Ratio-3 blocks (triadic) are the
  right object; ratio->3 is FORCED in the reversed-block family (Prop 7.5: any pair of
  block starts beta<gamma in a bad window obeys gamma<=3beta-5).
- LP MERGE HEADLINES: (i) CEILING (human-proved): triadic has pos(v)<=3v-1 and NO
  increasing 4-AP => LP-inc(C) FALSE for all C>=3; no (H-up)-only argument (Thm-12
  ledger, R5 staircases, records/piles) can reach C>=3; observed full extinction at
  C<=3 is a genuinely two-orientation phenomenon. (ii) R5 hand-off ANSWERED (negative
  for C>=3): explicit L10 staircases live inside triadic (staircase_demo.py).
  (iii) SHARPENING (machine-assisted): CP-SAT UNSAT certificates => LP-inc(C) for all
  C <= 43/24 ~ 1.792 (N=32,40,48 independent), vs 9/8 human. min-SAT C climbing:
  3/2@12, 13/8@16, 5/3@24, 7/4@28, 11/6@32. CONJECTURE C*_inc = 3 exactly.
- Honest gap (deliverable 3): cardinality coupling x <= LIS*LDS with both <= r4(x)
  has Behrend slack r4(x)^2/x -> infinity; triadic realizes ALL increasing-side
  lemmas, identity realizes all decreasing-side ones => YES needs a two-orientation,
  non-cardinality invariant. Open LP window: C in (43/24, 3) inc-side, then couple (H-down).

## 2026-07-28 — session (route R1 agent): corridor closure
- E(V) settled for ALL V: sigma_V witnesses it (3-AP-free => no incr 3-AP w/ extension).
  Single cuts NEVER obstruct; in-order obstruction is irreducibly multi-cut (>=3 scales).
  See attempts/route-R1/e_of_v_sigma.log.
- Window law W(V1,V2) (feasible 3rd cuts): wide open at tiny scale ((2,8),(4,12) all SAT);
  UNSAT notches appear from V2=16 on ((4,16): notch at ~60; (6,20): ~66-86; (8,26): 90-110
  and 180 dead, 140 alive island). Notches widen/multiply with scale. windows.log.
- Interleaved (non-decomposing) layouts: lag-2 ratio-2 pattern died at stage 7 (UNSAT,
  any gadgets); debt propagates backwards as decreasing-AP pressure (core_T7.log).
  Other patterns (geom3-lag2, lead-4, odd-leading, factorial-lag2) being verdicts-run.
- REPORT.md at attempts/route-R1/ carries the full taxonomy + impossibility statements.


## 2026-07-28 (post-restart) — session 1 continued: LP verified, MUS mechanism, FINlin program
- Container restart killed all background jobs; 6 wave-1 agents resumed via SendMessage
  (R2,R3,R4,R6,R8,R9) + R1 resumed on corridor closure + fresh-context AUDITOR launched
  on CORE.md/ASYM.md.
- Theorem 12 LP(9/8) fully machine-verified (lp_check.py): V1/V2 exhaustive on all
  168864 avoiders of [1..9]; ceiling-corrected prediction N0=91 at C=1.1 confirmed
  UNSAT by SAT; actual frontier ~12 => theorem has ~7.6x slack. Committed.
- Lemma 13 NEW: in any 4-AP-free permutation, record set Λ is FULLY 3-AP-free
  (upward extension forced by recordness); grounded set Γ is 3-AP-free per dyadic
  window (downward extension forced). Verified on 168864 avoiders + SAT witnesses.
- Lemma 7b (FINlin): if for some fixed K, for every c, boards eventually kill
  'pos(v)<=cv for all v<=K', then 196-YES. Motivated by MUS finding:
  asym C=2 N=34 extinction is driven EXACTLY by initial segment [1..15]@2v
  (mus_profile.py — minimal sufficient profile-constraint set = [1..15]).
- Asym witness mining: SAT witnesses delay SMALL values enormously (pos(2)=111 at
  N=140, pos/v up to 55x at v=2; leaders 3-AP-free confirming Lemma 13). If minimal
  pos(2) over asym witnesses is unbounded in N, the ENTIRE asym route R11 dies
  (single-value restriction argument, no pigeonhole needed). asym_pos2.py scanning
  (asym + plain analogues, B=5..40).
- RUNNING: shallow_scan.py (plain FINlin(8/15) probe), plain_thresholds2 (plain C>=2),
  asym_pos2.py, auditor agent, 7 route agents. Monitor armed on scan outputs.
- Wave-2 routes registered: R12 blocked (R1's theorems), R13 two-point supply
  (pending), R14 FINlin/SHALLOW program (active inline), R15 LP sharpening (active).

## 2026-07-28 ~01:25 UTC — route R3 (digit orderings -> omega) report filed
- Full report: attempts/route-R3/REPORT.md (verdict-first). Highlights:
  - THEOREM A (human proof): 2^M*(1,6,11,16) meets 4 pairwise-distinct dyadic blocks
    (M, M+2, M+3, M+4); any ordering with eventually contiguous dyadic blocks has a
    monotone increasing 4-AP regardless of internal block orders. Sharp at
    separation 2: adjacent-block interleaving kills all single-AP forcing (Lemma L2).
  - THEOREM B (machine-exact, CP-SAT + Glucose independent cross-check): the
    decoupled single-block system Sigma_3 (internal 4-AP-freeness + edge-3-AP bans +
    forced pair inversions; purely arithmetic, neighbor-free) is UNSAT for
    D_3=[27,81) base 3 and D_3=[64,256) base 4; a scaling lemma propagates UNSAT to
    all higher blocks => contiguous base-3/base-4 block orderings of N are dead with
    ANY internals. Coupled base-3 death at exactly N=87 (SAT at 86); 245-AP
    irreducible core saved + third-checked. Dissection: every proper sub-family
    conjunction SAT; 140-constraint irreducible core — death is 5-family-global.
  - Lemma T: base-3 priority comparator tau kills ALL monotone 4-APs on EVERY subset
    of N (any per-level priorities) — exact 4-AP analog of the parity recursion;
    order type >> omega. Prop B: breaking all L1-case-(ii)/(iii) APs by the sigma
    valuation mechanism forces 2^t to have infinitely many predecessors (non-omega).
  - 26 digit-defined omega-orderings ALL FAIL by value <= 24; failure taxonomy in
    report Sec. 5. Cross-route: R1 cut-set {8,26,80} = {3^j-1} = base-3 block tops.
  - Pending at cutoff (running): decoupled Sigma_2 for b=5,6,8; 2-separated dyadic
    N=127/255 (probe encoding bug found+fixed mid-session: separation chain covered
    even offsets only; fixed version re-verifies separation on returned models).

## 2026-07-28 ~00:20 UTC — session 1, SAT probe campaign: displacement laws
- ORDER-ENCODED SAT (experiments/sat_order.py: order vars + transitivity + one 3-clause
  per AP) massively outperforms search: plain avoiders found at N=120 in 2s; asym
  (no dec-3AP + no inc-4AP) witnesses at N=100 in 1s; asym alive N=160 with pos<=5v.
- EXTINCTION THRESHOLDS (minimal UNSAT N; cadical; C=2 row independently confirmed by
  CP-SAT direct-positional model):
    asym + pos<=ceil(Cv): C=1: 4 (hand-proved: pos<=v forces identity; script row '8'
    was a bracketing artifact, only affects C=1); C=1.25: 14; C=1.5: 20; C=2: 34;
    C=2.5: 56; C=3: 75; (C=3.5, 4 running).
    plain + pos<=ceil(Cv): C=1: 4 (same argument); C=1.25: 14; C=1.5: 22 — plain
    tracks asym closely at small C (dec-3AP constraints nearly free there).
  Fits: both quadratic ~8C^2 and exponential ~e^{~C} fit mid-range; C=4 will
  discriminate. plain C=8 SAT through N=200 (304s) — no large-C extinction reachable.
- Superlinear probe: asym + pos<=ceil(D v^1.5): D=1 dies by N=60 (small-value pinch:
  v^1.5 tighter than 3v for v<=8 — thresholds are dominated by small-value slack);
  D=2 alive at N=130+.
- MORAL: (i) profile-bounded avoider extinction is a real finite phenomenon at every
  tested tightness — a provable-looking 'LP theorem' family (any 4-AP-free permutation
  of N has pos(v)/v unbounded? and quantitatively more) — YES-side flagship target,
  connects to R5's staircase (L10) planted inversions; (ii) NO-side constructions need
  built-in superlinear displacement; contiguous-block architectures (BLOCKS.md) have
  LINEAR profiles => likely dead if LP holds — gate stays: prove-or-refute LP before
  investing in R12 blocks CSP. (iii) SOLVER-GRADE vs THEOREM-GRADE: any extinction
  used in a final argument needs DRAT-logged UNSAT + drat-trim verification + second
  engine — protocol TODO.
- R5 DONE (first wave-1 return): Generic Escape Proposition PROVES no finite forcing
  tree from one-point-anchored supply can close => R5 blocked with two hand-offs:
  two-point supply hunt (R13, wave 2), staircase-vs-displacement global counting
  (feeds LP hunt). 19 verified structural lemmas + staircase L10 are keepers.

## 2026-07-27 ~23:10 UTC — session 1, inline core theory + portfolio launched
- 8 background route agents launched (R1 blocks, R2 DEGS, R3 digits, R4 displacement
  search, R5 Ramsey-YES, R6 density-YES, R8 Z-transfer, R9 census), each with
  PROBLEM.md + route brief only. Awaiting reports; will merge into ROUTES.md.
- CORE.md (attempts/core/) written with 10 proved lemmas: order-type lemma; short
  independent proof of DEGS77(a) 3-AP forcing (z=a(1) anchored cascade + descending
  chain vs ω); WLOG a(1)=1 for NO-witness; anchored disjunction A_j∨B_j and (★★);
  tame-kill (|pos(v)-cv|<=B dies); DISPLACEMENT COMPACTNESS: 196-NO <=> exists φ with
  φ-bounded finite avoiders for all N (fixes the §3 König trap — the pointwise φ bound
  is what survives the limit); FIN(K) criterion (finite-shallowness extinction => YES),
  FIN(1) false via parity; interval characterization Lo(v)<pos(v)<Hi(v); slot
  relaxation (surjectivity onto positions is free — only finite-predecessors matters);
  stuckness = X-configuration (inc-3AP-top below dec-3AP-top aimed at same target).
  All machine checks pass (experiments/core_checks.py).
- Adversary analysis: anchored constraints alone admit a type-ω model ("B always":
  k→2k, 3j→2j DAG acyclic, finite ancestors) — Lemma 4 alone cannot give YES.
- Cross-block analysis (inline, to merge with R1): contiguous-block designs with blocks
  in increasing positional order ALWAYS die: AP x tiny, x+d,x+2d,x+3d in 3 consecutive
  dyadic blocks (e.g. 1,15,29,43) is increasing-monotone. Any 4-AP has b4<=b2+2 in
  dyadic block indices, x>0 forces last-two-terms in same-or-adjacent blocks. Block
  ORDER must have all consecutive triples (m,m+1,m+2) non-monotone (else the m1<m2
  family kills it); two-in-one-block patterns couple gadgets of block PAIRS both ways
  (increasing pairs vs π(m)<π(m'), decreasing pairs vs reversed) — matches prompt's
  warning that two-scale case is where these die.
- ASYM route opened (attempts/core/ASYM.md): target no-dec-3AP + no-inc-4AP (implies
  full NO-witness). Proved: descent words along EVERY progression avoid 11 and 000
  (density in [1/3,1/2]); leaders (values before all larger values) form an infinite,
  unbounded, 4-AP-free (density-0) increasing spine; every non-leader drop-chains down
  to a leader above it in value. Single-scale (rotation/Sturmian) realization
  impossible: would need {eθ} ∈ [1/3,1/2] for all e. Finite boards: witnesses exist
  exhaustively N ≤ 27+ (asym_exhaust.py running; nodes ~2x per N — hardening).
- Shallow-pinning probe: (K,C)=(2,2) counts EXPLODE (824k at N=12, >2M cap onward) —
  no early FIN(2) extinction; counting is the wrong probe, existence-at-large-N is the
  question (R4's SAT machinery needed).
- NEXT: harvest agent reports as they land; decide wave 2; keep asym_exhaust running;
  consider SAT for asym existence at N=35..60.

## 2026-07-27 ~21:55 UTC — session 1 start
- Repo empty; on branch claude/erdos-196-monotone-4ap-gk9blp. Wrote PROBLEM.md, ROUTES.md, this file.
- PRE-FLIGHT: forum thread https://www.erdosproblems.com/forum/thread/196 returns HTTP 403 (bot-blocked),
  as does the problem page. Matches the documented launch-day state; the launch operator checked both
  manually on 2026-07-27 and found no claim. Proceeding per PROMPT §1.
- Python 3.11.15; installed sympy, python-sat, ortools. 4 cores.
- Calibration experiments PASSED: 4-AP-free counts N=3..9 = 6,22,102,564,3336,22266,168864;
  3-AP-free = 4,10,20,48,104,282,496; parity construction verified (N<=256 + spot checks).
