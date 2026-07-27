# NOTES.md — lab notebook, newest entries at top

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
