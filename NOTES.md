# NOTES.md — lab notebook, newest entries at top

## 2026-07-28 (Opus-5) — WAVE-2 WORKFLOW COMPLETE: three of MY OWN programmes closed
- R17: CO-SUPPLY IS **REFUTED**, in two lines. Every value-record is CLOSED (u open at d
  => u+d precedes u => a larger value precedes u => u not a record). Lambda is infinite,
  so infinitely many closed values exist. => Theorem 16's chain programme is DEAD, not
  merely stuck. Also: EVERY propagation-style weakening is refuted as a family (in any
  digraph with position-descending edges, closures finite => every maximal chain ends at a
  sink); measured 40-67% of forcing edges land on a closed value (84% at N=9). And my
  quantitative reading of Thm 16(b) was WRONG: |Cl(u)| >= f(u) only gives pos(u) >= f(u),
  a contradiction iff #{u : f(u) <= P} < P; for Thm 16's own digraph no admissible f
  exists since |Cl(w)|=1 at records.
  NET POSITIVE: G*, a six-rule forced-descent digraph removing the record obstruction
  (sinks 40-65% -> 1-3%, longest chain 14 -> 132 at N=320); and an omega-free chain
  construction quantifying R5's barrier (one anchor buys <= log2 m steps; adversary holds
  it to 2-3 regardless of N).
- R18: Theorem 16 imposes **ZERO** constraint on block architectures — in any layered
  permutation every forcing edge stays INSIDE one block, so bounded closures are free.
  The bounded-closure mission I commissioned was vacuous (sigma_N has no open value at
  all). Its UNSAT direction would not have been a YES theorem either.
  NET POSITIVE: exact block decomposition of 4-AP-freeness (2-3 orders faster, localizes
  each death to one block); geometric cuts r=3, r=4 dead; parity-inside-blocks collapses
  to 2-SAT and is dead for every ratio.
- R19: the unweighted LEDGER CEILING IS EXACTLY 2 — for triadic, Sum_j tau_j = (3/4)N^2 +
  N/2 exactly (K=2..9), so C_ledger(N) < 2 for every N. No unweighted-ledger argument can
  reach C >= 2. And Thm 16's forcing step IS Thm 12's demand mechanism, so closures and
  the ledger are the SAME tool, not independent ones.
- CORE.md now carries Theorems 44, 45, 46 recording all three closures, and VERDICT.md has
  an UPDATE section with the revised bottom line.
- Running tally of self-corrections is now SIX: Remark 17 (meaning of linear extinction),
  correction to Remark 22 (block layouts not dead), Thm 16(c) vacuity, Remarks 31/36
  (degenerate objective, dropped clauses), Prop 38 Case 2 (densification unsupported), and
  now the Thm 16(b) quantitative mis-reading. Same root cause every time.
- STILL RUNNING: wave-3 workflow (12 agents) on Conjecture R21-C from both sides, plus
  t01_realize2.py (T=1 joint realizability; SAT at N=60,100 with full end-to-end checks).

## 2026-07-28 (Opus-5) — R21: the experiment I commissioned was VACUOUS (proved), but it
## closed the entire arithmetic delay world by proof
- MY MIS-SPECIFICATION, recorded (CORE Remark 31): I endorsed R20's recommendation and
  commissioned a direct AP-uniformity search. R21 proved it cannot decide anything:
  (a) the objective is DEGENERATE — max_sigma min_AP max_n pos_P(n)/n equals the trivial
      bound min|P cap [1..N]| ~ N/8, attained by dumping values 1..15 at the end
      (certified N=60 -> 6, N=100 -> 11); the optimum is realized at index n=1.
  (b) feasibility is AUTOMATIC and infeasibility IMPOSSIBLE — the geometric coarsening
      c(v) := j where pos(v) in [b^j, b^{j+1}) of ANY finite avoider has geometric fibres
      and satisfies condition (ii); avoiders exist at every N, so (i)+(ii) never goes
      extinct. And every avoider already meets Remark 17's gamma-floor on every AP, so
      D1-infeasibility cannot be certified at any level <= gamma.
  => D1 has NO independent finite content; it is exactly Corollary 26 + universal linear
  extinction. Lesson for the portfolio: before commissioning a search, check whether a
  trivial construction already satisfies the constraint system.
- WHAT SURVIVED, and it is the strongest NO-side theorem of the run (CORE Props 29-30,
  both re-derived and checked by me):
  * Prop 29 (tameness bound): for ANY class function with finite fibres emitted in
    increasing index order, and ARBITRARY within-class orders, a tame AP P (class weakly
    increasing on a tail) has sup pos_P(n)/n <= 1 + R_P. Geometric fibres => R_P = O(b)
    => LINEAR displacement on P => D1 fails there. Uniform over all gadgets.
  * Cor 30 (arithmetic world closed): if the delay's level set U_{k*} is a union of
    residue classes mod m, then t is constant on a full class P, P is tame, D1 fails.
    This retires rho(v_p(v)) for EVERY prime p, rho(v_p(v+s)), every function of v mod m,
    and every Boolean combination of congruences — for ALL geometric-fibre architectures.
    In particular R20's surviving CLS(5,a) is now dead BY PROOF (its odds are tame),
    not by a search inside Remark 27's blind spot.
- ALSO MEASURED by R21: AP-alternation is NOT 2-adically rigid — explicit mod-4 rule
  t(v)=0 (even), 2 (v=1 mod 4), 1 (v=3 mod 4) is AP-alternating, verified to M=3000; but
  it is congruence-determined so Cor 30 kills it. All period-m AP-alternating functions
  classified for m=2,3,4,6,8: only constants (m=3) or parity-alternating (2-adic-shaped).
  The MID family (level sets meeting every AP) has 0 tame APs and growing displacement
  but FAILS condition (ii).
- OPEN successor: Conjecture R21-C — (ii) + geometric fibres => t constant on some
  infinite AP. Would close block-index-plus-delay architectures entirely. NOT implied by
  Cor 30, and NOT finitely decidable (any proof that would also apply to the geometric
  coarsening of a finite avoider is wrong — the standing sanity check).

## 2026-07-28 (Opus-5) — R20 RETURNS: v log v FALSIFIED; AP-uniformity is the real filter
- MY v log v HYPOTHESIS IS FALSIFIED for the natural family. R20's alpha-wall: with
  phi_alpha(v)=ceil(alpha*v*log2(2v)), the minimal admissible alpha*(N) = 0.45, 0.50,
  0.50, 0.50, 0.50, >0.50 at N = 20, 30, 45, 60, 90, 130. So phi_{0.5} DIES at N=130
  (CEGAR UNSAT) — v log v profiles hit a wall exactly like linear ones, just ~9x slower
  per unit parameter. (Audit item R20 flagged: that UNSAT was single-solver; I have an
  eager two-solver re-verification running: experiments/verify_r20_alpha.out.)
- Also falsified: the STRUCTURAL picture. The optimal finite witnesses are NOT log-lag
  interleavings — the phi_{0.5} witness at N=90 has cut points {1,2,4,11,90} and emission
  order [1..11][12..31][61..90][44..60][32..43]: geometric ratio~2.8 blocks in order then
  a REVERSED tail. Delay is not concentrated on high 2-adic valuation values.
- NEW PROVED THEORY (folded into CORE.md as Corollary 26 + Remark 27):
  * Prop R20-2 = Corollary 26 (AP-restriction for displacement): every infinite AP
    restriction of a 4-AP-free permutation is itself one, of order type omega. Hence
    Theorem 12 and every certified extinction apply to EVERY AP separately, giving
    limsup pos_P(n)/n >= 9/8 for all P. DESIGN PRINCIPLE D1: a NO-witness needs unbounded
    relative displacement along EVERY AP, not just globally.
  * Lemma R20-1: the first NON-INTERVAL block architecture (class c(v)=floor(log_b v)+t(v)
    with t AP-alternating) — proved, with sharpness witnesses.
  * Prop R20-3 (dichotomy): every member of that family either has an AP on which it is
    linear (dies by D1) or has O(log v)-thin classes (no reduction). Kills the natural
    'delay by 2-adic valuation' designs: the odds carry constant delay, so the odd
    restriction is an in-order geometric block ordering.
- REMARK 27 — SEARCH BLIND SPOT (qualifies several earlier readings, including mine):
  from N*(C) ~ 4 e^{4.15(C-1.25)}, a design with AP-restriction displacement constant C
  cannot die before N ~ 6e3 (C=3), 1e7 (C=5), 1e9 (C=6). So verification to M=1e4-1e5
  CANNOT certify or refute any design with C >~ 3. R1's ratio-5/6 corridor (incl. the
  depth-5 feasible cuts [1,2,4,10,90..92]) and R20's CLS(5,a) (alive at N=250) BOTH sit
  in this blind spot — their survival at reachable N is NOT evidence. Conversely CLS(3,a)
  dying at N=250, and the ratio-3 shoulder chain 1,2,5,14,41,122 dying at 160 values, ARE
  informative (low C should die early) — and the latter is evidence against R1's
  Conjecture W for ratio-3 chains.
- R20's own next-step recommendation, which I endorse: switch from profile-SHAPE search to
  AP-UNIFORMITY search — look directly for a class function c with finite fibres, no
  strictly monotone 4-AP class sequence, and unbounded displacement on every AP r+qN
  (q <= 8). Either it produces the first D1-compatible architecture, or it converts D1
  into a genuine YES-side obstruction. First experiment that could bear on both branches.

## 2026-07-28 (Opus-5) — CORRECTION: depth-5 block layouts are ALIVE (island moves)
- R1-final scanning other prefixes found DEPTH-5 FEASIBLE cut sequences
  [1,2,4,10,90], [1,2,4,10,91], [1,2,4,10,92] — ratios 2, 2, 2.5, 9, ACCELERATING and
  non-geometric. The earlier depth-5 UNSATs applied only to continuations of the specific
  prefix {2,8,26,140}. So the in-order block program is NOT closed; the feasible window
  MOVES with the prefix rather than vanishing.
- CORE.md now carries an explicit correction to Remark 22. Narrowed status: geometric
  ratios 3/4 and bounded-lag interleavings are DEAD by certificate; tuned accelerating
  cut sequences are ALIVE at depth 5, unknown beyond. Remarks 23 (pair counting) and 25
  (sign must live on a convex partition) are unaffected but do not by themselves close
  the block family.
- Second time this run a negative reading of finite certificates had to be narrowed
  (first: Remark 17). Standing discipline: finite UNSATs bound only the family they
  quantify over.
- NEW Remark 25 (proved + exhaustively classified): the escape 'replace block parity by
  an arithmetic sign' fails because such rules are NOT TRANSITIVE. Over the family
  eps(u,l)=f_l(bit_{l+1}(u)), f_l in {0,1,id,not}: only 16/256 transitive on [1..64] and
  [1..96], and NONE genuinely u-dependent. Transitivity forces the sign constant on
  pieces of a convex partition -> block layouts are forced, not incidental.

## 2026-07-28 (Opus-5) — THE 4-vs-5 GAP, PINNED (Theorem 21, Remarks 22-23)
- R2's Construction A INDEPENDENTLY VERIFIED by me to N=65535: blocks B_m=[4^m,4^{m+1})
  concatenated in increasing order, each sorted by van der Corput (binary LSB-first),
  REVERSED for odd m. Order type omega is trivial (finite blocks listed in order).
  NO monotone 5-AP. Contains monotone 4-APs (first: 2,7,12,17). This is an explicit,
  machine-confirmed instance of DEGS77(b) with an explicit kill mechanism.
- REMARK 22 (the gap, exactly): the length-5 solution is a CONTIGUOUS GEOMETRIC BLOCK
  LAYOUT — MSD-like at top level (finite blocks => order type omega), LSD-like inside
  each block (vdC => AP killing). It threads Remark 20's dichotomy by putting the two
  priorities at DIFFERENT SCALES. Route R1 proved by SAT+Koenig certificates (quantified
  over ALL gadgets) that this architecture fails for 4-APs at ratios 3 and 4. So the
  exact mechanism that settles length 5 is PROVABLY UNAVAILABLE at length 4.
- REMARK 23 (why, structurally): Theorem 21's contradiction is a TWO-PAIR parity
  argument. For a k-AP in a ratio-r layout, t2..tk occupy <= ceil(log_r(k-1))+1 blocks:
  k=5, r=4 gives FOUR terms in two blocks = PAIR+PAIR (two pair-criteria, contradiction
  since the pairs' first elements differ by 2d so their bit_l agree while adjacent blocks
  demand opposite parity); k=4, r=3 gives THREE terms in two blocks = PAIR+SINGLETON —
  only one pair criterion, no contradiction. Four terms simply do not supply two pairs.
- MACHINE CONFIRMATION of Remark 23: all four naive length-4 analogues die instantly —
  ratio-3 + base-2 vdC + alt: (2,5,8,11); no reversal: (5,7,9,11); base-3 vdC + alt:
  (8,9,10,11); no reversal: (1,2,3,4). And (2,5,8,11) is exactly a 1+2+1 pattern
  (2 in B_0, 5,8 in B_1, 11 in B_2) — the pair+singleton case.
- FRESH-EYES agent (isolated from all route history) INDEPENDENTLY re-derived Lemma 13(a)
  (records infinite + no (k-1)-AP; 3-line reproof of DEGS77(a); length 4 <=> records
  3-AP-free, Roth-critical) and independently proved the one-base-point argument cannot
  close at length 4 (its (R) is false, via a 2-adic/3-adic antidiagonal order) — matching
  R5's Generic Escape. Two independent derivations of both facts.
  It also measured nu_L(N) := min over avoiders of max_{v<=L} pos(v) = L (FLAT) for all
  L <= 20, N <= 128 — so FIN(K)-type criteria are dead at reachable scales, and cut
  points exist at every tested L (consistent with R1's E(V) result).
- CPU: box was at load 38 on 4 cores; killed my prefix/vlogv probes to give the agent
  fleet the cores. Certified data already banked: N*(C)=4,15,31,90 (C=1.25..2, C=2 also
  eager-verified at N=85 with cadical+glucose agreeing); v log v SAT through N=100.

## 2026-07-28 (Opus-5) — CEGAR validated 3 ways; C=2 extinction independently confirmed
- CEGAR engine now validated against an INDEPENDENT METHOD: it reproduces route R9's
  exhaustive extension-tree thresholds exactly (C=1.5: SAT at N=14, UNSAT at N=15;
  C=1.75: SAT at N=30, UNSAT at N=31), plus unconstrained controls SAT at N=50, 120.
- C=2 extinction CONFIRMED by the eager O(N^3)-transitivity encoding: N=85 UNSAT
  (cadical, 298593 clauses, 297s); glucose cross-check running. So the plain-target
  extinction threshold for pos(v) <= 2v is <= 85 (CEGAR found UNSAT at 90; eager pins
  it at <= 85).
- v log v PROBE (the decisive NO-side feasibility question, CORE.md Remark 18):
  phi(v) = v*log2(v) is SAT at N=60 (15 values constrained). Larger N running.
  Rationale: phi(v) >= N once v >~ N/log N, so on a board of size N this profile
  constrains only the SMALL values — precisely the regime where shallow probes found
  avoiders alive (pos(v)<=2v for all v<=8 at N=355). Linear profiles die because they
  bind the LARGE values; v log v does not bind them at all.
- Ledger check (by hand): Theorem 12's drop-ledger CANNOT kill phi = v log v — the
  demand Sum e* >= N^2/18 costs only a constant factor in Sum f(w-e*) with f(x)=x log x,
  whereas a contradiction would need a log N factor. So the LP machinery is provably
  silent on the candidate profile; killing it needs a different mechanism.

## 2026-07-28 (Opus-5) — STRATEGIC PIVOT: linear-profile extinction cannot decide 196
- NEW CERTIFIED EXTINCTIONS (plain target, pos(v) <= floor(Cv)): N*(C) = 4, 15, 31, 90
  for C = 1.25, 1.5, 1.75, 2.0. C=1.5/1.75 agree with route R9's EXHAUSTIVE enumeration
  (independent method); C=2.0 (N=90) from CEGAR, eager two-solver re-verification running.
- k=5 CALIBRATION (experiments/k5_calibration.py, eager encoding, cadical+glucose agree):
  for k=5 — where an infinite avoider is KNOWN to exist (DEGS77(b)) — finite avoiders
  under pos(v) <= 1.25v ALSO go extinct (N=13). At C=1.5, 1.75 k=5 survives past N=70
  while k=4 dies at 15, 31.
- THEREFORE (CORE.md Remark 17): linear-profile extinction is NOT evidence for YES.
  Two independent reasons: (a) Lemma 6 quantifies over ALL profiles phi — killing every
  LINEAR phi leaves v log v, v^{1+eps} untouched; (b) the same extinction signature
  appears in the known-NO case k=5. R19's LP program is re-scoped: it yields a structure
  theorem (any NO-witness has superlinear displacement) but is NOT a path to YES.
- NEW NO-SIDE TARGET (data-driven): displacement pos(v) = Theta(v log v) is consistent
  with every certificate so far (N*(C) ~ 4 e^{4.15(C-1.25)}; R9 independently fits
  a e^{bC}, b ~ 2.2-2.8, i.e. avoiders of [1..N] exist with max pos(v)/v ~ O(log N)).
  R9's own read: weak lean NO. Its other key numbers: avoider tree strongly supercritical
  (mean branching 9.4 at N=12 -> 14.6 at N=32); dead ends only from N=12, still ~5.7% at
  N=32; on every measured axis k=4 sits between k=3 (YES) and k=5 (NO), closer to k=5.
- R8 report landed: Z-side map (195's answer lies in {2,3,4}; length 4 open on BOTH
  sides and neither transfers), theorem T3 (no annulus-macro arrangement of Z avoids
  monotone 3-APs), theorem T2 (any split extension of an N-permutation to Z contains a
  monotone 4-AP, so 196-NO does not yield a Z-avoider by concatenation).
- YES side must therefore attack ∀phi-extinction directly, or bypass Lemma 6 via
  Theorem 16's forcing chains.

## 2026-07-28 (Opus-5) — CEGAR engine + CORRECTION to the linear-profile picture
- Built experiments/profile_cegar.py: order encoding + AP clauses + per-value
  predecessor-count cardinality, with LAZY transitivity (CEGAR). Two bugs found and
  fixed during validation: (i) the cycle finder walked FORWARD and could dead-end,
  falsely reporting acyclicity (fix: after Kahn every residual vertex has an alive
  IN-neighbour, so walk BACKWARD); (ii) one cycle per round is far too slow — now
  extracts up to 400 vertex-disjoint cycles per round. Validated against the eager
  O(N^3)-transitivity encoding with TWO solvers (cadical + glucose) agreeing at
  (N,C) = (20,1.5), (21,1.5), (34,2), (40,2).
- CONVENTION NOTE: profile bound is now floor(C*v) — the exact meaning of pos(v) <= Cv.
  Earlier scans used ceil(C*v) and are therefore slightly more permissive; the C=1.5
  threshold moves from N=22 (ceil) to N<=20 (floor).
- CORRECTION to the earlier reading: PLAIN (both-orientation) linear-profile avoiders are
  ALIVE much further than the asym variant suggested: C=2 SAT at N=60, C=3 SAT at N=60,
  C=5 SAT at N=90. So plain extinction is CERTIFIED only for C <= 1.5. The claim
  'linear profiles die up to C=3' was ASYM-only and must not be quoted for the plain
  problem. This materially improves the NO side's room and means route R1's ratio-5
  island is NOT excluded by any profile theorem we have.
- Scan running to N = 130..350 for C = 2, 3, 5.

## 2026-07-28 (Opus-5) — extension-tree thinness measured
- tower_extend.py (E1): SAT-found plain avoiders EXTEND for M=20->30, 30->45, 40->60 but
  are DEAD ENDS at M=60->90 and 80->120 (no extension exists at all, with the prefix's
  relative order held fixed). So typical solver-found avoiders die; the extension tree is
  thin at scale. NOTE the sigma tower is a genuine INFINITE branch (verified early on:
  sigma_8 restricts to sigma_4, and the parity recursion is restriction-compatible for
  all N) whose limit fails order type omega — so infinite branches exist and the whole
  question is whether one has bounded displacement (Lemma 6). Greedy tower-building is
  therefore NOT decisive (Koenig builds the tower from level-wise existence); the
  decisive computation is the profile-bounded existence question.
- Running: plain_profile_cpsat.py (transitivity-free CP-SAT, plain both-orientation
  target, C = 2, 3, 5 up to N = 500). C=2 N=40 SAT so far.
- FINlin: plain SHALLOW K=8 dies neither at c=2 (SAT to N=355) nor c=3 (SAT to N=305).
  Lemma 7b's FIN-type extinction is not happening at accessible parameters — the YES
  side should not lean on it.

## 2026-07-28 (Opus-5 session) — THEOREM 16 (forcing closure) + wave-2 workflow
- MODEL SWITCH: Fable-5 credits exhausted; session moved to claude-opus-5. All six
  Fable-pinned agents die on resume (credit error) — they are DEAD; new work must be
  spawned fresh. Their directories/logs survive and are being consolidated.
- NEW THEOREM 16 (proved, exhaustively verified, in CORE.md): call u OPEN at scale d if
  (u-2d, u-d, u) is positionally increasing. Then u+d must be positioned BEFORE u
  (else increasing 4-AP). Hence the forward closure Cl(u) under u -> u+d lies inside
  pred(u): |Cl(u)| <= pos(u), always finite. Since the closure tree is finitely
  branching (d <= (u-1)/2), Koenig gives the EXACT REFORMULATION:
     196-YES  <=>  every 4-AP-free permutation admits an infinite forcing chain
                   (= an infinite pos-descending chain, impossible at order type omega).
  Verified F1/F2 on ALL 195154 avoiders with N <= 9, zero violations.
- LEMMA 16.1 (supply, re-derived cleanly): for every value w and every modulus m there
  is e in mN with (w, w+e, w+2e) increasing. Proof: predecessors of w are finite so
  w < w+e in position for large e; failure for all large e in mN forces the infinite
  descending chain w+e > w+2e > w+4e > ... Contradiction with omega.
- THE GAP, now sharply located: supply yields increasing 3-APs STARTING at a prescribed
  value; chains need one ENDING at a prescribed value ("co-supply"). Co-supply is FALSE
  on finite boards (sigma_N has no monotone 3-AP at all), so only an omega-essential
  proof can work. ALSO: chains have strictly decreasing positions, and a value at
  position p can be open only if it has 2 predecessors in AP with it — so low-position
  values are automatically closed and chains die naturally. A YES proof must therefore
  beat pos(u_0) with chain length from u_0.
- MEASURED (forcing_closure.py) on SAT witnesses: open-value fraction rises 35% (N=40)
  -> 64% (N=160); max closure size grows ~N/2 (9,19,20,32,65,78 at N=40..160).
- GREEDY ONLINE (greedy_latest.py): the canonical insertion process (Lemma 8 intervals)
  under memoryless strategies latest/earliest/mid gets STUCK at v=27/27/38 (X-config,
  Lemma 10). Online greedy is not a route; backtracking/SAT is required.
- FINlin probe: plain SHALLOW K=8, c=2 still SAT at N=355 -> FIN-type extinction at
  those parameters looks unlikely; Lemma 7b remains unrealized.
- WAVE-2 WORKFLOW launched (6 missions + 6 adversarial audits): R17 co-supply/infinite
  chain (YES crux), R18 bounded-closure NO-design (new constructive angle from Thm 16),
  R19 LP sharpening in the window (43/24, 3) plus two-orientation beyond 3, R1-final
  (in-order block death: depth-5 island points 700/740/760/780/800 all UNSAT — verify
  + decide), R16 tau-repair, and consolidation of R2/R4/R8/R9.
- RUNNING inline: plain_profile_cpsat.py (transitivity-free CP-SAT; plain profile
  C=2,3,5 to N=500) — the decisive gate for block architectures.

## 2026-07-28 ~limit-hit checkpoint (agents terminated by session limit, resets 05:40 UTC)
- ALL five in-flight agents killed by usage limit mid-work: R2 (was: mod4 complete,
  checking 2 background computations), R4 (headline certification instances running,
  completion-watcher armed), R8 (core work done, writing REPORT.md with proofs),
  R1-island (depth-5 probes running; comparing (26..80] system with R3 Sigma_3 for the
  joint lemma), R16 (starting: reusing R3 tau machinery). R9 also pending finalization
  (certification batch was computing).
- RESUME PLAN (wake scheduled ~05:45 UTC via send_later): SendMessage-resume each of
  R2, R4, R8, R9, R1, R16 with 'limits reset; container jobs may have died; re-run
  interrupted computations and finish deliverables'. Agent ids are pinned in this
  session's context; if lost, their work dirs identify them (attempts/route-R*/).
- Everything proved/verified so far is committed and pushed. CORE.md: 15 audited items
  (2 repaired). Live candidate regions: ratio-5 island (R1), tau-repair (R16),
  asym multi-scale words (R11). YES-side: two-orientation LP frontier, FINlin
  segments, record/grounded nets (Lemma 15).

## 2026-07-28 ~harvest wave-1 continued (R6, R3, R1-corridors in; corrections)
- R6 COMPLETE: ceiling theorem (CORE Thm 14, independently re-proved): triadic
  reversed-block has pos<=3v-1, NO increasing 4-AP => increasing-only methods cap at
  C*_inc in [43/24, 3]; dyadic calibration example CORRECTED (contains (1,6,11,16)).
  Density-alone provably insufficient (Behrend slack); two-orientation invariant needed.
- R3 COMPLETE: Lemma T (base-3 priority comparator kills ALL 4-APs on EVERY subset,
  both orientations — proof re-verified by me); DRUP-certified death of contiguous
  base-3/4 block orderings; {8,26,80}={3^j-1} coherence with R1. => R16 launched
  (tau-repair). FRAMING: k-adic comparators kill k-APs on every subset; DEGS77 = repair
  impossible at 3, possible at 5; 196 = the repair threshold at 4.
- R1 CORRIDOR REVISION (major): ratio-3/4 in-order dead BUT robust SAT ISLAND at ratio
  ~5: UNSAT notch [3.2,4.35]V2 then SAT island [4.8,~5.8]V2; {5,25,125} SAT,
  {2,8,26,140} SAT; {2,8,26,140,700} UNSAT (edge); banded gadget template. E(V)
  settled for ALL V. R1 resumed: decide depth-5 island, hand-build banded rule to 1e5.
- CORRECTION (plain thresholds): plain C=2 SAT at N=60 (36s; N=90 timed out) — plain
  extinction only CERTIFIED at C<=1.5 (N=22); 'kill C<=3' was ASYM-only. Plain
  C in [2,5] open; ratio-5 island consistent with all data. NO side healthier.
- AUDIT: 13/15 SOUND, 2 gaps repaired. asym pos(2)<=5 pin SAT at N=305.
- Load: box oversubscribed; killed my leftover solver; in flight: R2, R4, R8,
  R9-final, R1-island, R16.

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
- DEPTH 4/5 UPDATE: {2,8,26,150} SAT too (depth-4 island is an interval >= {140,150});
  {2,8,26,160} UNSAT. Depth-5: {2,8,26,140,700} UNSAT (sound via relaxation);
  760 (island center) + triple controls {26,140,700/756} did not resolve in-session.
  Depth-5 island survival = THE open frontier for the ratio-5-6 in-order corridor.
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
