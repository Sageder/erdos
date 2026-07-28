# AUDIT — route R1 / final ("fate of in-order block constructions")

Adversarial audit, 2026-07-28. Target: the deliverable returned by the route-R1/final
author (reproduced verbatim in the task prompt) together with the code and logs in
`/home/user/erdos/attempts/route-R1/final/`, checked against
`/home/user/erdos/PROBLEM.md` and the predecessor report
`/home/user/erdos/attempts/route-R1/REPORT.md`.

**Process note up front.** There is no `REPORT.md` or `STATUS.md` in
`/home/user/erdos/attempts/route-R1/final/`. The only prose is the returned summary,
and that summary is **truncated mid-word** ("…they are no longer loa"). Everything from
the tail of §3 onward — including §4 and deliverable (d) ("the empirical upper ratio law
… is *refuted*") — is unavailable and therefore **unaudited**. Several logs also end
without their own DONE line (`exhaust5_M110.log`, `exhaust5_M200.log`,
`exception_branches.log`, `depth6_grid.log`, `toprelax.log`): those jobs were killed
mid-run.

Audit artifacts (independent code, no route-R1 code reused):
`/tmp/claude-0/-home-user-erdos/16d68b37-9cd8-5fc8-ae52-36a43a9b9dde/scratchpad/r1audit/`
— `a1.py` (from-scratch witness checker), `enc.py` (from-scratch encoder, **eager**
transitivity, no CEGAR), `enc2.py` (CP-SAT integer-rank encoder), `brute.py`
(raw-enumeration oracle), `geom.py`, `proof.py`, `scan6.py`.

---

## 0. Verdict list

| # | Claim (as marked in the deliverable) | Verdict |
|---|---|---|
| 1 | Definition of *cut* and its stated equivalent forms | **SOUND** |
| 2 | "in-order block construction" ≡ "Cut(a) infinite" | **SOUND** (definitional; but it narrows R1's scope — see §2) |
| 3 | Lemma S: (C1),(C2),(C3) necessary; no decreasing-C2 family needed | **SOUND** |
| 4 | Lemma S monotonicity (S ⊆ S′, S′ feasible ⇒ S feasible) | **SOUND** |
| 5 | "Necessity ⇒ every UNSAT is a theorem" | **SOUND** (scope caveat, §3.5) |
| 6 | **Theorem A** (dead zone: W<U<V cuts, V ≥ 2U−1 ⇒ V ≥ 3U−2) | **SOUND** |
| 7 | Machine supplement: 99 exceptions `(1,U,U+1)`, U odd; `V=3U−2` never forced | **REPAIRABLE GAP** — numerics correct, but a finite check (U ≤ 200) is used for an unbounded claim. **Repair supplied in §4 (complete search-free proof).** |
| 8 | **Corollary A1** (V_{k+1} ≥ 3V_k−2 for k ≥ 2, ≤ 1 exception; V_k−1 ≥ 3^{k−3}(V₃−1); #cuts ≤ log₃N+O(1)) | **REPAIRABLE GAP** — inherits #7. Sound once Lemma G (§4) replaces the machine check. |
| 9 | **Corollary A2** (displacement; β ≥ 3) | **SOUND with an over-statement** — see §3.4 |
| 10 | **Corollary A3** (cut ⇒ Cl(u) ⊆ [u,V]) | Math **SOUND**; the two attached conclusions are **NOT SUPPORTED** — see §3.5 |
| 11 | "Lazy UNSAT is sound"; "TOP/WINDOW relaxation UNSAT is sound" | **SOUND** |
| 12 | Calibration: 19/19 agreement with R1, four engines | **CONFIRMED** on re-run subset; wording caveat (§3.6) |
| 13 | Depth-5 FEASIBLE with explicit verified witness | **CONFIRMED** (independently re-verified, §3.7) |
| 14 | Depth-6 UNSAT verdicts | **CONFIRMED** — but the *interpretation* ("the frontier moves to depth 6") **mis-locates the obstruction**: it is a 3-cut phenomenon (§3.8) |
| 15 | `exhaust5.py`: "EXHAUSTIVE search for a feasible 5-element cut set with max ≤ M" | **BROKEN** — two feasible depth-5 cut sets it never tested are exhibited in §3.9 |
| 16 | "R1's conclusion is WRONG"; "the shoulder … is invisible to a coarse grid" | **PARTLY MISATTRIBUTED** — §3.10. (A genuine refutation of a *different* R1 claim does survive.) |
| 17 | Deliverable (d), §4, and everything after the truncation point | **NOT AUDITABLE** (text does not exist) |

Nothing in the deliverable is **BROKEN** at the level of mathematics. The one BROKEN
item is a *computational completeness* claim (#15), and one framing claim is
misattributed (#16).

---

## 1. What was independently re-derived

I re-derived the constraint system from `PROBLEM.md` alone (`enc.py`), without reading
`cutsys.py` first for the encoding logic:

* variables `x_{u<v}` = "u before v" for `u,v` in the same block; cross-block order is a
  constant from the layout;
* **C1**: for every `x ≥ 1, d ≥ 1` with `x+3d ≤ V`, forbid the positional chain
  `x ≺ x+d ≺ x+2d ≺ x+3d` **and** its reverse `x+3d ≺ x+2d ≺ x+d ≺ x`;
* **C2**: for every `x, d ≥ 1` with `x+2d ≤ V < x+3d`, forbid `x ≺ x+d ≺ x+2d`;
* **eager** transitivity on all same-block ordered triples (so UNSAT needs no CEGAR
  soundness argument at all).

This reproduces every published verdict I re-ran:

```
[8,26,80]  UNSAT   [8,26,76]  SAT   [4,16,56] UNSAT   [4,16,68] SAT
[2,4,10]   SAT     [4,10,28]  SAT   [1,2,4,10,28] SAT (identical witness)
[1,2,4,10,28,82] UNSAT   [1,2,4,10,28,83] UNSAT
[1,3,4,10,28,82] UNSAT   [1,2,4,10,30,88] UNSAT
```

CP-SAT (integer ranks + AllDifferent, a different paradigm) agrees on the spot checks
I ran.

**End-to-end validation against the raw definition.** `brute.py` decides feasibility for
every cut set with `max ≤ 10` and small enough block factorials (**633 cut sets**) by
literally enumerating all in-order block orderings and testing the definition of a
monotone 4-AP directly, then compares with the SAT verdict: **0 mismatches**. (This test
first exposed a bug in *my own* encoder — forced chains were being dropped rather than
reported as unsatisfiable — which I fixed before re-running everything below. It did not
affect any UNSAT verdict, since dropping clauses only weakens the system, and every SAT
verdict quoted here is backed by a witness re-checked with `apcheck.py`.)

**The encoding is faithful and the certificates are real.**

---

## 2. Framing

`V` is a cut iff `{a(1..V)} = {1..V}` iff `pos(v) ≤ V` for all `v ≤ V` iff every value
`≤ V` precedes every value `> V`. All three are equivalent — re-derived, **SOUND**
(the third ⇐ direction: if `w > V` sits at position `p ≤ V`, some `v ≤ V` sits at a
position `> V ≥ p`, so `w ≺ v`).

"`a` is an in-order block construction" ≡ "`Cut(a)` is infinite" is a **stipulation**,
and a good one, but note it **narrows R1's original scope**: R1's §3.8 (T-ILV,
non-decomposing interleavings, pattern `2,4,1,6,3,8,5,…`) covers permutations with **no
cuts at all**, which this definition excludes by fiat. The headline "in-order block
constructions are NOT dead at depth 5" is therefore a statement about cut-bearing
permutations only. Not an error; a scope flag.

**Compactness (not stated in the surviving text, but load-bearing).** For a *fixed*
infinite cut sequence `V₁<V₂<⋯`, "every stage feasible" is genuinely equivalent to
existence: stage solutions are finite, restriction is well-defined by Lemma S
monotonicity, König gives an infinite branch, that branch is a linear order on ℕ of
order type **ω** (each block finite, blocks in order ⇒ every value has finitely many
predecessors), and it is 4-AP-free because every monotone 4-AP lies inside some stage
and stage-C1 forbids it. I verified this chain of reasoning; **it is correct**, and it
is what makes "feasible at every depth" equivalent to a NO answer to 196. It deserves to
be in the report explicitly, because without it "feasible" carries no weight.

---

## 3. Item-by-item

### 3.1 Lemma S — SOUND

(C3) is the definition of a cut. (C1) is `PROBLEM.md`'s restriction principle. (C2): if
`x ≺ x+d ≺ x+2d` inside `[1..V_k]` and `x+3d > V_k`, then `pos(x+3d) > V_k ≥ pos(x+2d)`
by the cut property, so `(x,x+d,x+2d,x+3d)` is an increasing monotone 4-AP. Requires
`x+3d` to *occur*, i.e. **surjectivity** — used legitimately and essentially (this is a
"no 4-AP-free permutation has these cuts" statement, not a YES-side existence argument).

The omission of a decreasing analogue of (C2) is **correct** and correctly justified:
every value `< V_k` is already covered, and a value `> V_k` sits after position `V_k`, so
it can never be the *first* term of a decreasing chain.

C1∧C2∧C3 is in fact the **complete** set of order constraints the cut prefix imposes: a
4-AP with two or more terms above `V_k` leaves their relative order free, so no clause
arises. I checked this exhaustively over the case split.

Monotonicity: restricting an `S′`-solution to `[1..max S]` is legal because `max S ∈ S′`
is a cut of that solution; a violated (C2) for `S` is a (C1) violation for `S′` when
`x+3d ≤ max S′`, and a (C2) violation otherwise. **SOUND.**

### 3.2 Theorem A — SOUND

Re-derived line by line. `W ≥ 1, W < U ⇒ U ≥ 2 ⇒ d = U−1 ≥ 1`. The three forced
comparisons are `pos(1) ≤ W < pos(U)`, `pos(U) ≤ U < pos(2U−1)` (needs `U < 2U−1`, i.e.
`U ≥ 2`), `pos(2U−1) ≤ V < pos(3U−2)` (needs `2U−1 ≤ V` and `V ≤ 3U−3`). Increasing
orientation only — correct, no decreasing case is needed. Boundary `U = 2`: gives the
4-AP `(1,2,3,4)`, valid. **No gap.**

### 3.3 The machine supplement and Corollary A1 — REPAIRABLE GAP

`geometry.py` is correct code (I re-implemented the same predicate independently in
`geom.py` and reproduced the 99 exceptions and the "V = 3U−2 never forced" line).

The **gap**: Theorem A only covers `V ≥ 2U−1`. Corollary A1 needs the *whole* dead zone
`U < V ≤ 3U−3`, and for `V < 2U−1` the deliverable leans entirely on a finite check to
`U ≤ 200`. As written, an unbounded arithmetic claim is being carried by a bounded
computation — the exact pattern the audit checklist item 9 is about. The rest of A1's
bookkeeping is fine: for `k ≥ 3` one may take `W = V_{k−1} ≥ V₂ ≥ 2`, so the `W = 1`
exception can occur only at the step `(V₁,V₂,V₃) = (1, odd, odd+1)` — hence "at most one
exception"; and `V_{k+1} ≥ 3V_k − 2 ⟺ V_{k+1} − 1 ≥ 3(V_k − 1)` gives the stated
`V_k − 1 ≥ 3^{k−3}(V₃−1)` and `#(Cut(a) ∩ [1,N]) ≤ log₃N + O(1)`.

**Repair: §4 gives a complete search-free proof.** With it, A1 is SOUND unconditionally.

### 3.4 Corollary A2 — SOUND, with one over-statement

`pos(v) ≤ V_k` for `v ∈ (V_{k−1},V_k]` is immediate. If `V_k ≤ βV_{k−1}` for all `k`
then for `v > V₁`, `pos(v) ≤ V_k ≤ βV_{k−1} < βv`. ✔

`β ≥ 3` is correct but only as a **supremum**: on the extremal chain `V_{k+1} = 3V_k−2`
every individual ratio is `< 3` (e.g. `1,2,4,10,28,82` has ratios `2, 2, 2.5, 2.8,
2.93`); the sup is 3 because `V_k/V_{k−1} ≥ 3 − 2/V_{k−1} → 3`. State it that way.

**Over-statement:** "The in-order family therefore sits at *linear* displacement with
constant ≥ 3". That holds only for the **bounded-ratio** sub-family. A cut sequence with
`V_{k+1}/V_k → ∞` has no linear displacement profile at all, and A1 does not forbid one.
The conclusion "pushing [LP] past `C = β` would kill every bounded-ratio in-order tower"
is fine as stated; the sentence before it is not.

### 3.5 Corollary A3 — math SOUND, conclusions NOT SUPPORTED

The mathematics: `u` open at scale `d` (CORE Thm 16: `u−2d ≥ 1` and `(u−2d,u−d,u)`
positionally increasing) forces `u+d ≺ u`. If `u ≤ V` with `V` a cut and `u+d > V`, then
`pos(u+d) > V ≥ pos(u)`, i.e. `u ≺ u+d` — contradiction. Hence `u+d ≤ V`, and by
induction `Cl(u) ⊆ [u,V]`. **SOUND**, re-derived.

Two attached conclusions do **not** follow:

1. *"R1's family **is** R18's bounded-closure family."* A3 gives
   `|Cl(u)| ≤ V − u + 1` where `V` is the least cut `≥ u`; by A1 `V` can be as large as
   `≈ 3u`, so this is a **linear-in-u**, block-trapped bound, not a uniform bound. Unless
   R18's "bounded" means precisely "block-trapped" (it is described in `ROUTES.md` as
   "bounded forcing closures"), the identification is unjustified.
2. *"any Thm-16 chain argument (R17) automatically defeats it."* **Vacuous.** CORE
   Theorem 16(b) already proves `|Cl(u)| ≤ pos(u) < ∞` for **every** 4-AP-free
   permutation of ℕ, so no such permutation admits an infinite forcing chain and there is
   no "Thm-16 chain argument" to apply to anything. This vacuity is already on record in
   `attempts/route-R17-cosupply/AUDIT.md` ("Theorem 16(c)'s biconditional is vacuous").
   A3 adds a genuinely new *localisation* (closures live inside one block); it does not
   hand R17 a weapon.

Also, the general claim in §1 that "every UNSAT is a theorem … quantified over all
gadgets/layouts/rules" is correct but should be read exactly: each UNSAT is a theorem
about **one finite cut set**, namely "no 4-AP-free permutation of ℕ has all of
`V₁,…,V_k` as cuts". It is not a theorem about all cut sets of a given cardinality —
that quantifier ranges over an infinite family and no finite computation reaches it.

### 3.6 Calibration — CONFIRMED, one wording caveat

`calib.py`'s `EXPECT` table has **20** entries; `calib.log` has **19** lines and no
`CALIB ALL AGREE` footer — the `[2,26,90]` run never finished. So "19/19" should read
"19 of 20 planned; the 20th did not complete". Of those 19 I independently re-decided 5
with `enc.py` (eager, from-scratch) and all agree.

Minor: the claim "*Every* SAT verdict re-verified … against the trusted `apcheck.py`
*and* a from-scratch `O(V²)` brute checker" is stronger than the code. In `calib.py`
`verify_witness_full` runs only for `engines[0]`; the from-scratch `brute_check` lives
only in `verify_depth5_sat.py` and runs only on that file's 8 cases.

### 3.7 Depth-5 feasibility — CONFIRMED

I re-verified the witnesses from scratch (`a1.py`), checking: permutation of `[1..V]`;
each claimed cut really is a cut (`set(seq[:c]) == set(1..c)`); no monotone 4-AP in
either orientation by direct `(x,d)` scan **and** by all three `apcheck.py` checkers
(`_brute`, `_pos`, `_general`); no C2 violation. Clean for

```
[1,2,4,10]    : 1 2 4 3 10 7 8 9 5 6
[1,2,4,10,28] : 1 2 4 3 10 7 8 9 5 6 28 19 22 26 27 18 20 23 25 24 16 21 13 15 11 17 12 14
[1,2,4,10,40] : (verified, 40 values)
```

My own encoder returns SAT for `[1,2,4,10,28]` and hands back the identical order.
**The positive result stands.**

Interpretation caveat, which the deliverable should state where it says "depth 5 is
FEASIBLE": feasibility is satisfiability of the *necessary* system; it does **not**
exhibit a 4-AP-free permutation of ℕ with those five cuts. (Given §3.8, in fact no such
permutation with a sixth cut of the natural shape appears to exist.)

### 3.8 Depth-6 — verdicts CONFIRMED, interpretation mis-located

I reproduced `[1,2,4,10,28,82]`, `[1,2,4,10,28,83]`, `[1,3,4,10,28,82]`,
`[1,2,4,10,30,88]` as UNSAT with eager transitivity. `scan_d6_v5_28.log` is also much
better than the returned summary suggests: it is a **full-integer** sweep of
`[1,2,4,10,28,V]` for `V ∈ [82,400]`, all UNSAT, with a DONE line. Good work.

**But "the frontier moves to depth 6" mis-locates the obstruction.** By Lemma S
monotonicity I stripped the prefix off and found that the death is already visible with
**three** cuts:

```
[10,28,82]  UNSAT        [4,10,28,82] UNSAT      [2,10,28,82] UNSAT
[11,31,91]  UNSAT        [12,34,100]  UNSAT      [13,37,109]  UNSAT
[10,29,85]  UNSAT        [10,30,88]   UNSAT      [16,46,136]  UNSAT
```
versus the *small-scale* shoulders, which are all SAT:
```
[1,2,4] S   [2,4,10] S   [3,4,10] S   [4,10,28] S
[5,6,16] S  [6,16,46] S  [7,8,22] S   [8,22,64] S   [5,13,37] S
```
So a 6-cut chain is impossible *through these cuts* not because it has six cuts, but
because its **top three** cuts are infeasible on their own. Depth is not the mechanism.

**And the controlling parameter is the *first* of the three cuts, not the scale.** Fixing
`U` and varying `W` isolates it cleanly:

```
shoulder V = 3U-2 :   [8,27,79]  SAT     [9,27,79]  UNSAT
                      [8,28,82]  SAT     [9,28,82]  UNSAT     [10,28,82] UNSAT
                      [8,26,76]  SAT                          [10,31,91] UNSAT  [11,31,91] UNSAT
R1's ratio-5 island:  [8,26,130] SAT     [9,26,130] UNSAT
                      [8,28,140] SAT     [9,28,140] UNSAT     [10,28,140] UNSAT
                                         [9,28,150] UNSAT     [10,28,150] UNSAT
```

With `U` and `V` held fixed, the shoulder **and R1's ratio-5 island** both survive at
`W = 8` and both die at `W = 9`. This is a *first-cut* threshold, and it is the same
phenomenon R1 already tabulated as "**first-cut memory**" (`REPORT.md` §3.7:
`(26,80)` feasible iff `V₁ ≤ 6`; `(20,100)` iff `V₁ ≤ 7`; `(16,70)` iff `V₁ ≤ 6`) — the
threshold value depends on `(U,V)` (e.g. `[7,20,100]` SAT vs `[8,20,100]` UNSAT gives 7
there), so "`W ≤ 8`" is not a universal constant. Credit to R1 for the phenomenon; what
is new here is that **this, not depth, is what stops the chain**:

* every 6-cut chain has `V₄ ≥ 10` — the minimal legal chains are `1,2,4,10,…`,
  `1,3,4,10,…`, `1,5,6,16,…` — so its top triple `(V₄,V₅,V₆)` always has first element
  `≥ 10`, above every first-cut threshold measured so far;
* every 5-cut chain can have `V₃` as small as 4, comfortably below them.

Restating the finding this way matters: the right next experiment is the 2-parameter
`(W,U)` feasibility map plus a **proof of the first-cut threshold**, not a depth-7
search. If the threshold is a theorem with a bound like "`W ≥ 9` kills every
`(W,U,V)` with `U ≥ 3W−2`", it closes the entire in-order programme at one stroke —
far stronger than "depth 6 is empty so far".

Supporting sweeps run for this audit (independent encoder, eager transitivity, every
integer tested, both completed):

```
# DONE (10,28) V in [82,160]:  SAT at []      <- kills every 6-chain through 10,28 with V6 <= 160
# DONE (16,46) V in [136,175]: SAT at []      <- the previously untested continuation of [1,5,6,16,46]
```

Finally, the honest hedge "everything decided is UNSAT" must be kept. No finite
computation can establish depth-6 death: `V₆` ranges over an infinite set, and so do
`V₄,V₅`. Any stronger phrasing would be a finite-for-infinite substitution.

### 3.9 `exhaust5.py`'s exhaustiveness — BROKEN

The file's own docstring says "**EXHAUSTIVE** search for a feasible 5-element cut set
with max ≤ M" and the log header says "exhaustive 5-cut search, max cut ≤ 110". It is
not exhaustive. Two feasible depth-5 cut sets with `max ≤ 110` that it **never tested**:

```
[1,5,6,16,46]  ->  SAT   (my encoder, eager transitivity; witness re-verified with apcheck)
[1,7,8,22,64]  ->  SAT   (idem)
```

Three independent defects produce the holes:

1. **Wrong reachability bound on `V₁`.** The outer loop's feasibility-of-continuation
   test iterates `w = 3*w-2 if w > 1 else w+1` **four** times starting at `w = V₁` —
   i.e. it assumes `V₂ ≥ 3V₁ − 2`. There is no such constraint: the geometry lemma needs
   **three** cuts, so `V₂` may be `V₁ + 1`. The correct minimal chain from `V₁` is
   `V₁, V₁+1, 3V₁+1, 9V₁+1, 27V₁+1`. Consequence at `M = 110`: the loop `break`s at
   `V₁ = 3`, so `V₁ ∈ {3,4}` are never scanned although `[3,4,10,28,82]` and
   `[4,5,13,37,109]` are in range. (Both happen to be UNSAT — I checked — but they were
   never tested, and `[3,4,10,28]`, `[3,4,10,40]` are depth-4 SAT, so the branch was
   alive.)
2. **The exception branches were never finished.** `exhaust5.py` prunes with
   `lo = 3*last - 2`, which by construction skips the `(1, odd, odd+1)` steps;
   `exception_branches.py` exists to cover them, looping `U ∈ {3,5,…,59}`. Its log
   contains **only `U = 3`** and has no `# EXCEPTION BRANCHES DONE` footer — the job was
   killed. `U = 5,7,9,11` are exactly where the two missed sets above live.
3. **Non-UNSAT outcomes are silently treated as alive.** `feas()` returns
   `'TIME_CAP'`/`'GEOM_DEAD'` and the DFS does `if r != 'UNSAT': recurse`. At depth 5 the
   set is then printed as `*** DEPTH-5 FEASIBLE` **without a witness check**, so a
   timeout can be reported as a feasibility. `exhaust5_M110.log` contains exactly one
   such line (`!! TIME_CAP at [1,2,4,10,105] … branch kept alive`), so at least one
   reported "feasible" set family is unverified. `'GEOM_DEAD'` is in fact *UNSAT*, so
   routing it to "alive" is unsound in the wrong direction (it happens not to trigger
   here, because the DFS's pruning already avoids the dead zone).

Neither `exhaust5_M110.log` nor `exhaust5_M200.log` has its `# DONE M=…` line.

**Impact:** the *positive* claim (depth 5 is feasible) is untouched — it needs one
witness and it has several. Any *completeness* statement at depth 5 ("the depth-5
corridor is exactly …") is unsupported. And the missed prefixes matter for the depth-6
question: `[1,5,6,16,46]` and `[1,7,8,22,64]` are precisely the depth-5 sets whose
continuations the depth-6 grid never looked at. I closed most of that hole (§5):
`[16,46,V]` is UNSAT for **every** integer `V ∈ [136,175]`, and also at the three
island landmarks `V = 222, 244, 267` (`≈ [4.8, 5.8]·46`, where R1's window law puts the
only surviving SAT band). No counterexample surfaced. Still untested by anyone:
`[1,7,8,22,64]`'s continuations (`U = 64`; shoulder 190, island `≈ [307,371]`).

### 3.10 "R1's conclusion is WRONG" — partly misattributed

* R1's `REPORT.md` **VERDICT item 3** already reads: "**REVISION** … **in-order is NOT
  dead at all ratios**", and its §3.7 table explicitly names the object in question:
  "**76 S (shoulder = 3V2−2)**", together with "a thin SAT shoulder from 3V2−2 (width
  shrinking to 1–2 points as V1/V2 grows)". R1 **saw** the shoulder and named it. The
  claim that it was "invisible to a coarse grid" is therefore not right; what R1 failed
  to do was **chain** the shoulder — its depth-4 sweep of `{2,8,26,V₄}` starts at 100 and
  never tests 76. That is a real and worthwhile correction, but it is "R1 chased the
  wrong corridor", not "R1's certificates or conclusion were wrong".
* A **genuine** refutation does survive, and the deliverable should lead with it instead:
  R1 VERDICT **item 2** asserts "the 'blocks in increasing position order' ansatz at
  geometric ratio ≤ 4 is dead for EVERY gadget choice … ratio 3 dies at 4 blocks". The
  chain `{1,2,4,10,28}` has every ratio ≤ 2.8 and is feasible with **five** cuts, and
  `{2,8,26,76}` — a shoulder continuation of R1's own prefix — is feasible with four.
  Item 2 is false as stated.
* "the ratio-3 shoulder … **at depth 4 is usually a single integer**" is not true at the
  scale where the new corridor actually lives: the deliverable's own `exhaust5_M110.log`
  shows the feasible `V₄` set after the prefix `[1,2,4]` is the whole interval
  `[10, 37]` — 28 integers, not one. The "single integer" behaviour is a large-`U`
  phenomenon (`(8,26)`: `{76,77}`), which is what R1 reported.

### 3.11 Soundness of the relaxations — SOUND

`solve_lazy` bootstraps only C1/C2 clauses and adds only transitivity instances on
same-block triples, so the solved formula is a subset of the true system: UNSAT is sound.
Its SAT return is checked for per-block acyclicity (`A@A` vs `A.T`, valid because within
a block the tournament is complete) and every SAT is re-verified end-to-end. The TOP /
WINDOW relaxation drops clauses whose literals leave the window (`chain` returns
`'DROP'`) and keeps cross-block constants; dropping clauses only weakens, so its UNSAT is
sound. `toprelax.log` correctly labels its TIME_CAPs "[inconclusive]". The deliverable's
statement that R1's five depth-5 island points are **NOT INDEPENDENTLY RE-VERIFIED** is
accurate and appropriately flagged.

---

## 4. Repair for #7/#8: a complete, search-free proof of the geometry lemma

This removes the `U ≤ 200` dependency entirely.

> **Lemma G.** Let `1 ≤ W < U` and `U < V ≤ 3U − 3`. Then there exist integers
> `x, d ≥ 1` with
> `x ≤ W < x+d ≤ U < x+2d ≤ V < x+3d`
> — hence `W, U, V` cannot all be cuts of a monotone-4-AP-free permutation of ℕ —
> **unless** `W = 1`, `V = U+1` and `U` is odd, in which case no such `(x,d)` exists.

*Proof.* Write `p = U − W ≥ 1` and `s = V − U ≥ 1`. The four requirements are
`x ≤ W`, `x + d ∈ (W, U]`, `x + 2d ∈ (U, V]`, `x + 3d > V`.

**(B) `V ≥ U+2` and `V ≥ 2U − W`.** Take `d = max(p, ⌊s/2⌋ + 1)` and `x = U − d`.
Then `x + d = U ∈ (W,U]`; `x ≥ 1` because `d ≤ U−1` (from `p ≤ U−1` and
`⌊s/2⌋ + 1 ≤ U−1`, using `s = V−U ≤ 2U−3`); `x ≤ W` because `d ≥ p`;
`x + 2d = U + d ∈ (U, V]` because `1 ≤ d ≤ s` (here `p ≤ s` is exactly `V ≥ 2U−W`, and
`⌊s/2⌋+1 ≤ s` needs `s ≥ 2`); and `x + 3d = U + 2d > V` because `2d ≥ 2⌊s/2⌋+2 > s`.

**(A) `U+2 ≤ V ≤ 2U − W − 1`.** Take `x = W` and `d = max(⌊p/2⌋+1, ⌊q/3⌋+1)` with
`q = V − W`. The range hypothesis forces `p ≥ 3` (from `U+2 ≤ 2U−W−1`) and `q ≥ p+2 ≥ 5`.
Then `d ≤ p` (since `⌊p/2⌋+1 ≤ p` for `p ≥ 2`, and `⌊q/3⌋+1 ≤ p` since
`q ≤ 2U−2W−1 = 2p−1 ≤ 3p−1`), and `d ≤ ⌊q/2⌋` (since `⌊p/2⌋+1 ≤ ⌊(p+2)/2⌋ ≤ ⌊q/2⌋`, and
`⌊q/3⌋+1 ≤ ⌊q/2⌋` for `q ≥ 4`). These are exactly `x+d ∈ (W,U]`, `x+2d ∈ (U,V]`,
`x+3d > V`.

**(C) `V = U+1`.** The only admissible value of `x+2d` is `U+1`, so `x = U+1−2d`. Take
`d = ⌈(p+1)/2⌉`. Then `x ≤ W ⟺ 2d ≥ p+1` ✔ ; `x+d = U+1−d > W ⟺ d ≤ p` ✔ (true for all
`p ≥ 1`); `x+3d = U+1+d > V` ✔ ; and `x ≥ 1 ⟺ d ≤ ⌊U/2⌋`. For `W ≥ 2`,
`d = ⌈(U−W+1)/2⌉ ≤ ⌈(U−1)/2⌉ = ⌊U/2⌋` ✔. For `W = 1`, `d = ⌈U/2⌉`, and
`⌈U/2⌉ ≤ ⌊U/2⌋` holds iff `U` is even.

**Sharpness of the exception.** If `W = 1` then `x = 1` is forced, so `x+2d = U+1`
requires `2d = U`, impossible for odd `U`. Hence `(1, U, U+1)` with `U` odd genuinely
admits no forced chain. ∎

> **Lemma G′ (the shoulder is clean).** `V = 3U − 2` is never forced, for any `W`.
> *Proof.* `x + d ≤ U` gives `x + 3d = 3(x+d) − 2x ≤ 3U − 2x ≤ 3U − 2`, so
> `x + 3d > V = 3U − 2` is impossible. ∎ (No machine check needed for
> `geometry.py`'s second output line either.)

**Verification of the repair.** `proof.py` instantiates the closed forms (A),(B),(C)
for every triple `1 ≤ W < U ≤ 400`, `U < V ≤ 3U−3` and checks the four inequalities
directly: **failures occur on exactly the 199 triples `(1, U, U+1)` with `U` odd and
nowhere else.** So the closed forms are correct and the exception set is exactly as
claimed — now with a proof rather than a search.

With Lemma G, **Corollary A1 is unconditionally SOUND**: for `k ≥ 3` take
`W = V_{k−1} ≥ 2`, so `V_{k+1} ≥ 3V_k − 2`; the single possible exception sits at
`(V₁,V₂,V₃) = (1, odd, odd+1)`, which needs `V₁ = 1`.

---

## 5. Additional computations run for this audit

All with `enc.py` (independent encoder, **eager** transitivity, no CEGAR — so every
UNSAT below is unconditional given only C1/C2/C3 necessity), SAT witnesses re-verified
against `experiments/apcheck.py`.

| computation | result |
|---|---|
| witnesses `[1,2,4,10]`, `[1,2,4,10,28]`, `[1,2,4,10,40]` | all clean (perm, cuts, no 4-AP by 3 checkers, no C2) |
| `[1,2,4,10,28,82/83]`, `[1,3,4,10,28,82]`, `[1,2,4,10,30,88]` | UNSAT (confirms deliverable) |
| minimal infeasible core of `[1,2,4,10,28,82]` | `{10,28,82}` — a **3-cut** obstruction |
| shoulder triples: `[1,2,4] [2,4,10] [3,4,10] [4,10,28] [5,6,16] [6,16,46] [7,8,22] [8,22,64] [5,13,37]` | all **SAT** |
| shoulder triples: `[10,28,82] [10,29,85] [10,30,88] [11,31,91] [12,34,100] [13,37,109] [16,46,136]` | all **UNSAT** |
| depth-5 sets missed by `exhaust5.py`: `[1,5,6,16,46]`, `[1,7,8,22,64]` | **SAT** (witnesses verified) — breaks the exhaustiveness claim |
| depth-5 sets missed by the `V₁` bound: `[3,4,10,28,82]`, `[4,5,13,37,109]`, `[1,9,10,28,82]`, `[1,11,12,34,100]` | UNSAT (untested, but harmless) |
| depth-4 sets missed by the `V₁` bound: `[3,4,10,28]`, `[3,4,10,40]` | **SAT** (branch was alive) |
| dense sweep `[10,28,V]`, **every** integer `V ∈ [82,160]` | all UNSAT (`SAT at []`) |
| dense sweep `[16,46,V]`, **every** integer `V ∈ [136,175]` — the previously untested continuation of `[1,5,6,16,46]` | all UNSAT (`SAT at []`) |
| `[16,46,222]`, `[16,46,244]`, `[16,46,267]` (the island band for `U = 46`) | all UNSAT |
| **W-threshold**: `[8,27,79] [8,28,82] [8,26,76] [8,26,130] [8,28,140]` | **SAT** (witnesses verified) |
| **W-threshold**: `[9,27,79] [9,28,82] [9,26,130] [9,28,140] [9,28,150]` | **UNSAT** (same `U,V`, first cut raised by one) |
| raw-enumeration validation of the encoder, 633 cut sets with `max ≤ 10` | 0 mismatches |
| `[2,8,26,76]` (R1's own prefix, shoulder continuation R1 never tested) | **SAT**, witness verified |

No counterexample to any UNSAT was found; no SAT verdict failed re-verification.

---

## 6. Checklist responses

1. **Both orientations.** Handled. C1 emits both; C2 correctly needs only the increasing
   form, and the justification given is correct (§3.1). Verified in the encoder.
2. **Strict positions, `d ≥ 1`, no reuse, no reindexing.** Clean throughout: chains are
   over consecutive AP terms, `d` starts at 1, `x ≥ 1`, values are distinct by
   construction.
3. **Injectivity / surjectivity / order type ω.** Surjectivity is used precisely where
   the top term of the chain (`3U−2` in Theorem A, `x+3d` in C2) is asserted to occupy a
   position after `V`; without it the term need not exist. Order type ω is used
   implicitly in "positions `≤ V`" and, essentially, in the compactness step (§2). All
   the claims are of "no 4-AP-free permutation has these cuts" type, so the classic
   "YES-side argument that never uses surjectivity" trap is avoided.
4. **Compactness / limits.** Not present in the surviving text; the König step it
   inherits from R1 is correct and preserves order type ω (§2). Flagged because it should
   be stated.
5. **Named theorems.** Only König (finitely-branching infinite tree). Hypotheses hold.
6. **Boundary cases.** `U = 2` in Theorem A: fine. `V₁ = 1` singleton block: fine.
   `v − d < 1`: never arises (all chains go upward from `x ≥ 1`). The `(1,odd,odd+1)`
   exception is genuine, not merely unfound (§4).
7. **Circularity.** None. Lemma S is a restriction principle, not a restatement of 196.
8. **Conventions.** ℕ starts at 1 throughout; values vs positions never swapped; no drift
   to 194/195/197; one-sidedness of ℕ is used exactly where the report says (the chain
   anchored at `x = 1`).
9. **Finite vs infinite.** Two places. (a) Corollary A1 — repaired in §4. (b) "the
   frontier moves to depth 6" — no finite computation can decide this; the deliverable's
   hedge "everything **decided** is UNSAT" is the correct phrasing and must not be
   strengthened. Additionally the `exhaust5` "exhaustive" label is a completeness claim
   that the code does not deliver (§3.9).
10. **SAT/CP as theorems.** Encoding re-derived from `PROBLEM.md` and matches
    `cutsys.py`; every UNSAT I re-ran was reproduced by an independent encoder with eager
    transitivity, and spot-checked with CP-SAT integer ranks. No DRUP/UNSAT certificates
    are produced by either implementation — that is the remaining assurance gap for the
    UNSAT side, and it is the same gap R3 closed with DRUP for its own system.

---

## 7. Recommended edits to the deliverable

1. Replace the `U ≤ 200` machine supplement with **Lemma G and Lemma G′** (§4). They are
   short, complete, and turn Corollary A1 from "machine-checked" into "proved".
2. Re-title the headline finding. "R1's conclusion is WRONG" should become: *R1's
   VERDICT item 2 ("in-order at geometric ratio ≤ 4 is dead, dies at 4 blocks") is
   false — `{1,2,4,10,28}` is a 5-cut chain with all ratios ≤ 2.8, and `{2,8,26,76}` is a
   4-cut continuation of R1's own prefix. R1's item 3 already said in-order is not dead;
   what was wrong was the location of the corridor.*
3. Drop "invisible to a coarse grid" (R1 named the shoulder) and drop "at depth 4 is
   usually a single integer" (the deliverable's own log shows `[10,37]` for `[1,2,4]`).
4. Replace "the frontier moves to depth 6" with the accurate mechanism, which is a
   3-cut **first-cut threshold** (R1's own "first-cut memory", §3.7 of `REPORT.md`):
   with `U,V` fixed, `(8,U,V)` is SAT and `(9,U,V)` is UNSAT, at the shoulder *and* at
   R1's ratio-5 island (§3.8). Every 6-cut chain has `V₄ ≥ 10`, above every measured
   threshold; every 5-cut chain can keep `V₃ = 4`, below them. The right next target is a
   **proof of the first-cut threshold**; if it is a theorem it closes the entire in-order
   programme, not just depth 6. A depth-7 search is the wrong experiment.
5. Withdraw the word "exhaustive" from `exhaust5.py` and its logs, or fix the three
   defects in §3.9 and re-run to completion. Add witness verification before printing
   `*** DEPTH-5 FEASIBLE`, and treat `GEOM_DEAD` as UNSAT.
6. In Corollary A2, restrict "linear displacement" to the bounded-ratio sub-family and
   say `β ≥ 3` is a supremum.
7. In Corollary A3, keep the localisation result and drop both attached conclusions
   (§3.5), or justify the identification with R18's notion of "bounded".
8. Write the report to disk. Half of the deliverable currently exists only in a
   truncated chat message and cannot be audited or reproduced.
