# NOTES.md — lab notebook, newest entries at top

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
