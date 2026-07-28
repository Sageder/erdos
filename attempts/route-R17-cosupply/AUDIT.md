# AUDIT — route R17 (co-supply gap of Theorem 16)

Adversarial audit, 2026-07-28. Auditor ran with the goal of BREAKING the claims.
No `REPORT.md` / `STATUS.md` exists in this directory; the audited text is the
author's returned summary (quoted claim names below) plus the 7 shipped scripts.

Audit scripts written for this review (all in this directory, all runnable):

- `audit_recheck.py` — fully independent re-implementation of R17.1/.3/.4/.5/.6′
  over ALL 4-AP-free permutations of [1..N], N ≤ 9 (imports only the trusted
  `experiments/apcheck.py`; does not import `forcing2.py`).
- `audit_window_validate.py` — re-runs the `supply_window.py` grid; decodes and
  verifies **every** SAT model (permutation + 4-AP-freeness + all asserted order
  constraints), re-confirms **every** UNSAT with a second solver (Glucose42), and
  compares the UNSAT set against Prop R17.3's prediction.
- `audit_satstats.py` — recomputes the SAT-board statistics the summary quotes but
  no shipped script produces (immediate-death edge fractions; longest chains to N=320).
- `audit_r178_counterexample.py` — explicit counterexample to Lemma R17.8's
  closing bound.

---

## 0. VERDICT TABLE

| claim | verdict |
|---|---|
| Thm R17.1 (records are G-closed ⇒ ¬co-supply) | **SOUND** (scope note; script-vs-report reproducibility defect) |
| Thm R17.2 (no propagation statement; (B) refuted as a family) | **SOUND** (methodological caveat on the word "REFUTED") |
| Prop R17.3 (exact scale exclusion) | **SOUND** for the UNSAT half; **REPAIRABLE GAP** in the "can be a G*-sink" side-claim (repaired here, conclusion survives); "exactly" is window-relative, not a theorem |
| Thm R17.4 (record supply, ≥ pos(w)−1 open values in (w,2w)) | **SOUND** (comparison to CORE's "(w,1.5w]" is not apples-to-apples) |
| Cor R17.5 (record inversion law) | **SOUND but redundant** — it is the u = w+d instance of Theorem 16(a) |
| Thm R17.6 (the six-rule digraph G*) | **SOUND** as a construction; the headline biconditional "196-YES ⟺ some value has infinite G*-closure" is **TRUE BUT VACUOUS** (P ⟺ P) |
| Thm R17.6′ (midpoint-anchor doubling chain) | **SOUND** |
| Prop R17.9 (one-anchor budget) | **SOUND with a scoping correction** (bounds a *consecutive* run, not an anchor's total use; U1-only) |
| Prop R17.7 (calibration of (C)) | **SOUND**, one stated criterion is imprecise (drops U₀ and the u ≥ U₀ restriction) |
| Lemma R17.8 (quantitative supply) | **BROKEN** — the closing explicit bound is false; explicit counterexample below. First half is sound. |
| all quoted machine measurements | **REPRODUCED** (table in §3), except two that are quoted over a range that starts later than stated |

Nothing in the report claims to prove 196 either way, and nothing found here changes
that. The one broken item (R17.8) is a side remark that nothing else depends on.

---

## 1. Claims marked PROVED — detailed verdicts

### Thm R17.1 (records are closed) — SOUND

Proof re-derived: `u` open at scale `d` means `u−2d ≥ 1` and
`pos(u−2d) < pos(u−d) < pos(u)`; Theorem 16(a) then forces `u+d ≺ u`; since
`u+d > u`, a larger value precedes `u`, so `u ∉ Λ`. Contrapositive: every record is a
G-sink. Uses only injectivity + 4-AP-freeness. The step to "infinitely many closed
values" invokes CORE Lemma 11(b), whose proof that Λ is infinite genuinely uses
**surjectivity** (the running maximum of a bijection is unbounded) — checklist item 3
is satisfied, and it is satisfied in the only place it is needed.

Machine claim independently reproduced (`audit_recheck.py`, N = 4..9, all
195 154 avoiders):

```
genuine violations (record open at d with u+d ≤ N): 0
board-edge incidences (record open at d with u+d > N): 134 503   [report: 134 503]
```

**Reproducibility defect (not a mathematical error).** No shipped script performs that
separation. `census.py` prints, under the heading `A record-is-G-closed violations`,
the *unseparated* per-(board,record) count: 3, 29, 182, 1334, 9509, 87448 at
N = 4..9 (98 505 total). A reader running the shipped script sees a large nonzero
number where the report claims 0. Fix: `census.py` should split `viol_rec` on
`u + d ≤ N`.

**Scope note.** R17.1 refutes only the ∀-form of co-supply ("*every* value is open").
The cofinal form ("open values exist above every w") is TRUE — Lemma 16.1 makes
`w+2e` open — and is untouched. Since a chain must continue *at the specific value it
has reached*, the ∀-form is the one that matters, so the verdict on target (A) stands.

### Thm R17.2 (no propagation statement) — SOUND

Re-derived: in a permutation of order type ω, all edges of the digraph point
≺-downwards, hence `Cl(u) ∖ {u} ⊆ pred(u)` is finite and the induced digraph is
acyclic. Take a longest path `u₀ → … → u_k` inside `Cl(u₀)` starting at a non-sink
`u₀`. Then `u_k` is a sink, and moreover **every** successor of `u_{k−1}` is a sink
(a non-sink successor would extend the path). So both
"∀ open u ∀ scale d: u+d open" and "∀ open u ∃ scale d: u+d open" are refuted.
The existence of a non-sink comes from Lemma 16.1 (uses ω). Correct for G and G*.

This is, precisely, the observation that CORE Theorem 16(c)'s biconditional is
vacuous: since Theorem 16(b) already proves closures are finite, "every 4-AP-free
permutation admits an infinite forcing chain" is equivalent to "no 4-AP-free
permutation exists". R17.2 is the right thing to have noticed, and it is correct.

**Methodological caveat on the report's logical convention.** "REFUTED = ¬X is
derivable ⇒ X is never provable modularly" is *not* a theorem. If 196-YES holds then
every statement about 4-AP-free permutations is derivable, including X. The correct
statement (which the report half-concedes) is: *any proof of a refuted X is
automatically a complete proof of 196-YES*. So "stop work on (A)" is sound project
management — (A) is not a sub-goal — but it must not be read as "(A) is false" or
"(A) is unprovable".

### Prop R17.3 (exact scale exclusion) — SOUND (UNSAT half); "exactly" is window-relative

Hand proof re-derived and correct. If `u` is open at `d` then `u+d ≺ u`. Openness of
`u+d` at scale `d` requires `pos(u) < pos(u+d)`; openness at scale `d/2` (d even)
requires `pos(u) < pos(u+d/2) < pos(u+d)`. Both need `u ≺ u+d`. Contradiction. ∎

Window results re-run and **strengthened** (`audit_window_validate.py`), all 15
(w,e) pairs, w ∈ {1,2,3}, e ∈ {2,3,4,6,8}, N = w+5e:

- every UNSAT re-confirmed by a second, independent solver (Glucose42);
- every SAT model decoded and checked: genuine permutation of [1..N], 4-AP-free by
  `apcheck`, and satisfying the asserted base and openness constraints (the shipped
  `supply_window.py` never validates its SAT models — `cosupply_sat.py` does);
- UNSAT set for `w+3e` is **exactly** `{e} ∪ {e/2 : e even}` in all 15 cases;
  UNSAT set for `w+2e` is empty in all 15 cases. `ALL CHECKS PASS`.

SAT-encoding faithfulness re-derived independently: variables `x_{uv}` for u<v with
the two transitivity clauses `[-a,-b,c]`, `[a,b,-c]` forbid exactly the two cyclic
patterns on each triple, so models are exactly linear orders; the 4-AP clauses use
only the three *adjacent* comparisons, which is sound because ≺ is total and
transitivity is enforced separately. Restriction principle applies (all conditions
mention only values ≤ N), so UNSAT ⇒ theorem for ℕ. Faithful.

**Two caveats.**

1. "**exactly** the excluded set" is a claim about SAT results, i.e. "not excluded by
   values ≤ w+5e". It is *not* a theorem; a larger window could exclude more scales.
   The UNSAT half is a theorem, and it coincides with the hand proof — so the hand
   proof, not the solver, is what carries R17.3.
2. **REPAIRABLE GAP** in the side-claim "*w+3e can be a G-sink and a G\*-sink in every
   window tested*". `supply_window.sink_clauses` implements only U1, U2, D1, D2 —
   **U3 and D3 are missing**, and `analyse()` calls it with `('U1','U2','D1','D2')`.
   So the tested object is not a G*-sink. Repair: I added the missing U3/D3 sink
   clauses and re-ran all 15 windows — still SAT in every case, so the conclusion
   survives unchanged. (`sat_measure.py`'s docstring has the same stale 4-rule list
   while its code uses all six — cosmetic.)

### Thm R17.4 (record supply) — SOUND

Re-derived: `w ∈ Λ`, `v ≺ w` ⇒ `v < w` (recordness); with `d = w−v ≥ 1`,
`pos(v) < pos(w) < pos(2w−v)` (second inequality by recordness), so `u = 2w−v` is open
at scale `d` with `u−2d = v ≥ 1`; Theorem 16(a) gives `3w−2v ≺ 2w−v`. Distinct
`v ∈ pred(w)` give distinct `u = 2w−v ∈ (w, 2w−1]`, hence ≥ `pos(w)−1` open values in
`(w,2w)`. ω-free given the record. Reproduced exactly: **105 957** instances over
N ≤ 9, 0 failures of openness and 0 failures of the forced descent.

**Framing note (not an error).** The comparison "vs CORE's ω-derived *one open value
in (w,1.5w]*" is not apples-to-apples: R17.4 requires `w ∈ Λ`, a density-0 set, while
the CORE sentence is quantified over all `w`. Separately, that CORE sentence looks
unsupported on its own terms — Lemma 16.1 supplies *some* `e`, with no bound, so
`w+2e ∈ (w,1.5w]` does not follow. R17.4 should not be advertised as strengthening a
claim that has not itself been established.

### Cor R17.5 (record inversion law) — SOUND but redundant

Re-derived: `w ∈ Λ`, `w−d ≺ w`, `w−d ≥ 1` ⇒ `pos(w−d) < pos(w) < pos(w+d)` (the last
by recordness), so `pos(w+2d) < pos(w+d)` else `(w−d,w,w+d,w+2d)` is an increasing
4-AP. Reproduced: **31 223** instances, 0 violations. The report's remark "*Not
implied by CORE L15*" is true, but it *is* the `s = w+d` instance of Theorem 16(a)
(equivalently the `v = w−d` case of R17.4): `w+d` is open at scale `d` because
`w−d ≺ w ≺ w+d`. So it is not independent content.

### Thm R17.6 (the six-rule forced-descent digraph G*) — SOUND construction, VACUOUS headline

*Rules.* Independently re-derived. With `l_i = [x+(i−1)d ≺ x+id]`, 4-AP-freeness gives
exactly `(¬l1∨¬l2∨¬l3)` and `(l1∨l2∨l3)`; their six unit propagations are exactly the
table's U1,U2,U3,D1,D2,D3 (checked over all 8 truth assignments, and each rule's
source/target algebra re-derived by hand). All six code implementations match the
table, including the `≥ 1` and `≤ N` guards. "Complete for single-AP reasoning" is
correct: resolving the two clauses of one AP yields only tautologies, so unit
propagation is all a single AP can give. Note the constraints themselves are not new
— they are CORE Lemma 11(a)'s "no 000, no 111" pair; G* is a new *organization* of
them, not a new constraint.

*Descending / finite out-degree.* Every rule's conclusion is `t ≺ s`, so all edges
descend and `Cl_{G*}(u) ∖ {u} ⊆ pred(u)`, giving `|Cl_{G*}(u)| ≤ pos(u)`. Out-degree:
U1 (`d ≤ (s−1)/2`), U3 (`d ≤ s−1`), D1 (`d ≤ s−1`), D2 (`d ≤ (s−1)/3`),
D3 (`d ≤ (s−1)/2`) are all a priori bounded; only U2 has unbounded `d`, and its
targets all lie in `pred(s) ∩ (s,∞)`, which is finite. The parenthetical
"(U2/D1 need d ≤ E(s))" is right for U2 and unnecessary for D1 — harmless.

*Machine.* Reproduced exactly: **1 694 236** rule instances over all 195 154 avoiders
N ≤ 9, every edge ≺-descending (`forcing2.py`). The closure bound
`|Cl_{G*}(u)| ≤ pos(u)` is an immediate consequence of that plus transitivity, and is
additionally asserted along every anchored chain by `anchor_chain.py`.

*Records escape only via D2.* Verified by hand for all six rules: U1, U2, U3 all
conclude `w+d ≺ w`, contradicting recordness; D1 needs `w+d ≺ w`; D3 needs `w+d ≺ w`;
only D2's premise `w−d ≺ w−2d ≺ w−3d` and conclusion `w−d ≺ w` involve no value above
`w`. (`cosupply_sat.py`'s docstring lists only "U1,U2,D1" as the excluded rules —
incomplete, but the conclusion is right.)

**The headline is vacuous.** "196-YES ⟺ some value has infinite G*-closure" unfolds to
"196-YES ⟺ every 4-AP-free permutation of ℕ has a value with infinite G*-closure".
The same theorem proves `|Cl_{G*}(u)| ≤ pos(u) < ∞` for every u, so the right-hand
side is equivalent to "no 4-AP-free permutation of ℕ exists", i.e. to 196-YES itself.
It is a true biconditional carrying zero information — the same defect as CORE
Theorem 16(c), and R17.2 applies to G* verbatim (the report says so). König is not
needed at all once the closure bound is in hand. Calling G* a "**strict strengthening
of Thm 16 that removes the record obstruction**" is justified only as a statement
about *measured* chain lengths and sink densities on finite boards; it removes one
obstruction (records as sinks) and leaves the fatal one (R17.2) exactly where it was.

### Thm R17.6′ (midpoint-anchor chain) — SOUND

Re-derived: if `m − 2^j d ≺ m ≺ m + 2^j d` then `(m−2^j d, m, m+2^j d)` is a
positionally increasing 3-AP of step `2^j d`, so `m + 2^j d` is open at that scale and
Theorem 16(a) forces `m + 2^{j+1} d ≺ m + 2^j d`. For `j = 0..K` these chain into
`m+d ≻ m+2d ≻ m+4d ≻ ⋯ ≻ m+2^{K+1}d`, a ≺-descending sequence of `K+2` distinct
values, so `pos(m+d) ≥ K+2`. Requires `2^K d ≤ m−1`, as the report states. Genuinely
ω-free (only Theorem 16(a) and distinctness of positions). Reproduced exactly:
`anchor_chain.py exh` gives 6 + 57 + 476 + 4044 + 35026 + 346628 = **386 237**
anchored runs at N ≤ 9, all chains descending, all closure bounds respected — the
report's number to the digit.

### Prop R17.9 (one-anchor budget) — SOUND with a scoping correction

The doubling law is right: for a U1 step `u → u+d` with anchor `a = u−d`, the next
step `u+d → u+d+d'` has anchor `u+d−d'`, so equal anchors force `d' = 2d`; and
`u−2d = a−d ≥ 1` forces `d ≤ a−1`. Hence a **maximal run of consecutive same-anchor
steps** has length ≤ `⌊log₂((m−1)/d)⌋+1`, and an infinite chain would need infinitely
many anchor changes. That is the conclusion the report draws, and it is correct.

**Correction to the phrasing.** "One anchor supports ≤ ⌊log₂((m−1)/d)⌋+1 steps" is
false if read as a *global* budget for that anchor: a U1 chain is strictly increasing
in value, so a later revisit of anchor `m` uses a strictly larger scale, but the
scales need not double — the global bound is `m−1`, not logarithmic. Also, R17.9 is
U1-only (G); U2/U3/D-steps in G* have no such anchor.

### Prop R17.7 (calibration of (C)) — SOUND, one criterion imprecise

The counting step is correct: `|Cl(u)| ≤ pos(u)` (from Thm 16(b)), so
`|Cl(u)| ≥ f(u)` for `u ≥ U₀` gives `pos(u) ≥ f(u)` there; positions `1..P` carry `P`
distinct values, each of which is either `< U₀` or has `f(u) ≤ P`, whence
`P ≤ U₀−1 + #{u ≥ U₀ : f(u) ≤ P}`.

The simplified restatement "*contradiction iff `#{u : f(u) ≤ P} < P` for some P*"
drops both `U₀−1` and the restriction `u ≥ U₀`. The exact criterion is
`∃P : U₀−1 + #{u ≥ U₀ : f(u) ≤ P} < P`. The three worked examples are correct under
the exact criterion (checked: `f(u)=u+1` for `u ≥ U₀` gives `P ≤ P−1`, contradiction;
`f(u)=u` gives `P ≤ P+U₀−1`, none; `f = log` gives `P ≤ U₀−1+e^P`, none).

The "iff" is defensible but should be stated precisely: the criterion is exactly
Hall's condition for a bijection `pos` with `pos(u) ≥ f(u)`, so it characterises when
*the counting argument alone* yields a contradiction, not when a contradiction exists.

Worth adding (implied, not stated): a lower bound valid only on a **sparse** set of
`u` can never produce a contradiction, since the complement already supplies
unboundedly many values with small `pos`. Any usable `f` must be cofinite.

"No admissible f exists for Thm 16's digraph" — correct: records are G-sinks, so
`|Cl_G(w)| = 1` on the infinite set Λ, hence `#{u : f(u) ≤ P} = ∞` for every `P ≥ 1`
and Hall never fails. Likewise "for G*, (C) first requires only finitely many
G*-sinks" is a correct necessary condition.

---

## 2. Claim marked PROVED that is BROKEN

### Lemma R17.8 (quantitative supply) — BROKEN (closing bound)

**What is sound.** "For `e₀ > E(w)`, some `k ≤ pos(w+e₀)−2` has
`(w, w+2^k e₀, w+2^{k+1}e₀)` increasing" is correct, where
`E(w) := max{v > w : v ≺ w} − w` (as in Lemma 16.1). Because every `2^k e₀ > E(w)`,
each `w ≺ w+2^k e₀` holds, so each failure genuinely yields `w+2^{k+1}e₀ ≺ w+2^k e₀`,
and consecutive failures chain into a ≺-descending sequence bounded by `pos(w+e₀)`.

**What is broken.** The conclusion

> "so Lemma 16.1's scale is ≤ `m·pos(w)·2^{pos(w+m·pos(w))}` — explicit but exponential
> in displacement"

silently replaces the hypothesis `e₀ > E(w)` by `e₀ = m·pos(w)`. Pigeonhole over
`e ∈ {m, 2m, …, pos(w)·m}` does give *one* such `e₀` with `w ≺ w+e₀` — but the
doubling argument needs `w ≺ w+2^k e₀` for **every** `k`, and that is exactly what
`e₀ > E(w)` buys and `e₀ = m·pos(w)` does not. **`E(w)` is not bounded by any function
of `pos(w)`.**

**Explicit counterexample** (`audit_r178_counterexample.py`). Lemma 16.1 — which
R17.8 is a quantitative refinement of — is a statement about *any* permutation of ℕ,
and the R17.8 derivation nowhere uses 4-AP-freeness. Take `m = 1`, `w = 1` and the
permutation of ℕ beginning

```
5, 1, 3, 33, 25, 31, 29, 21, 19, 23, 27, 17, 13, 11, 15, 9, 7, 6, 8, 10, 12, 14, 16, 4, 2, …
```

(general recipe: `5, 1, 3` then any topological order making `pos(1+2e) < pos(1+e)`
for every `e ≤ E`, then all remaining values in increasing order — order type ω,
bijective). Here `pos(1) = 2` and `pos(1 + m·pos(1)) = pos(3) = 3`, so the claimed
bound is `1·2·2³ = 16`, yet **no `e ≤ 400`** makes `(1, 1+e, 1+2e)` positionally
increasing (verified for E = 16, 50, 400; the recipe scales to any E).

**Even inside the 4-AP-free class the substitution is unjustified**: on 4-AP-free
permutations of [1..9] the ratio `E(w)/pos(w)` already reaches 4 — e.g.
`(9,1,2,4,3,7,5,8,6)` has `w = 1`, `pos(w) = 2`, `E(w) = 8`.

**Repair.** State the bound in terms of `E(w)`:
`e ≤ 2^{pos(w+e₀)−1}·e₀` with `e₀ := m·⌈(E(w)+1)/m⌉`. This is explicit but *not*
explicit in `pos(w)` alone. If one insists on a `pos`-only bound, the correct shape is
much worse: at most `pos(w)−1` of the scales `m·2^j` can be "bad", so one must go out
to `j ≈ pos(w)·(Q+1)` to guarantee a good run, giving `m·2^{O(pos(w)·Q)}` where `Q`
bounds `pos` on the relevant range. The qualitative moral the report draws
("exponential in displacement; cannot be fed into a Thm-12-style linear ledger")
survives; the displayed formula does not.

**Impact: none downstream.** No other R17 claim uses R17.8.

---

## 3. Reproduction of every quoted measurement

All reproduced on this box.

| quoted | reproduced | tool |
|---|---|---|
| 195 154 avoiders, N ≤ 9 | 195 154 (22+102+564+3336+22266+168864) | `audit_recheck.py` |
| 1 694 236 G* rule instances, all edges descending | 1 694 236, 0 violations | `forcing2.py` |
| 0 genuine record-openness violations; 134 503 board-edge ones | 0 / 134 503 | `audit_recheck.py` |
| R17.4: 105 957 instances | 105 957, 0 failures | `audit_recheck.py` |
| R17.5: 31 223 instances | 31 223, 0 failures | `audit_recheck.py` |
| R17.6′: 386 237 anchored runs | 386 237, 0 failures | `anchor_chain.py exh` |
| "84 % exhaustively at N=9" (G edges landing on a G-sink) | 169 591/201 448 = **84.2 %** | `census.py 9` |
| "40–67 % of Theorem-16 forcing edges" (SAT boards) | 67, 68, 64, 56, 47, 48, 48, 43, **40** % at N = 40…320 | `audit_satstats.py` |
| "immediate-death edges … → 2–9 %" (G*) | 33, 15, **9, 8, 6, 4, 3, 3, 2** % at N = 40…320 | `audit_satstats.py` |
| "Sinks 40–65 % → 1–3 %" | G: 65→38 %; G*: 25, 11, **3, 3, 2, 1, 1, 1, 0** % | `audit_satstats.py` |
| "longest chain 14 → 132 at N=320" | G = 3…13 (14 at N=260), G* = 12…**132** at N=320 | `audit_satstats.py` |
| "6–9 of 10 records escape at N ≥ 80" | 6/8, 6/9, 7/10, 8/9 at N = 80,100,130,160 | `sat_measure.py` |
| "adversary holds one anchor to 2–3 steps regardless of N" | chain length 2 (N ≤ 160), 3 (N = 200, 260) | `anchor_chain.py sat` |
| window UNSAT sets = `{e, e/2}` | exact match, 15/15, second solver confirms | `audit_window_validate.py` |

Two presentational quibbles: the ranges "1–3 %" (G*-sinks) and "2–9 %"
(G* immediate-death edges) hold only from N ≥ 80; at N = 40, 60 the values are
25 %/11 % and 33 %/15 %. And "longest chain 14 → 132" pairs numbers from different
board sizes (G = 14 occurs at N = 260 in both the author's and my run; at N = 320 my
witness gives G = 13). These are single-witness solver measurements, not stable
statistics — different SAT witnesses give different values.

---

## 4. Checklist sweep

1. **Both orientations.** Handled. Theorem 16 / rule U1 uses only the increasing
   clause; G* adds the decreasing clause's three propagations (D1,D2,D3). All six
   re-derived. The SAT encodings assert both clauses per AP.
2. **Positions strictly increasing, d ≥ 1, no reuse, no reindexing.** Clean
   throughout. Every rule's guards (`u−2d ≥ 1`, `u−3d ≥ 1`, `s+d ≤ N`, …) were checked
   against the mathematics; `open_scales` correctly caps `d ≤ (u−1)/2`.
3. **Injectivity / surjectivity / ω.** Injectivity: everywhere (≺ is a linear order).
   ω: closure finiteness (R17.1/.2/.6), Lemma 16.1, R17.7's counting. Surjectivity:
   used exactly once, and correctly — Λ infinite in CORE Lemma 11(b), which is what
   turns "records are closed" into "infinitely many closed values". No YES-side
   argument here that skips surjectivity (there is no YES-side argument here at all;
   R17's positive content is all negative/structural).
4. **Compactness / limits.** None used. König is invoked rhetorically in R17.6 but is
   not needed (the closure bound already gives finiteness). No order-type-preservation
   step to check.
5. **Named theorems.** Only König (redundantly) and the restriction principle. No
   Szemerédi/vdW/Ramsey/Erdős–Szekeres used, so no uniformity to track.
6. **Boundary cases.** Checked: `u−2d ≥ 1` and `u−3d ≥ 1` guards present in code and
   statements; `d/2` in R17.3 only applies for even `d` (the report says so, and my
   validator only predicts `e/2` for even `e` — exact match); `w−d ≥ 1` needed in
   R17.5 (stated); `w=1` in R17.4 is fine because a record 1 has `pos(1)=1` so the
   claimed count is 0.
7. **Circularity.** One genuine instance, already flagged: the R17.6 biconditional is
   `P ⟺ P`. It is not *false* and it does not corrupt anything else, but it must not
   be presented as an "exact reformulation" with content. R17.1/.2/.3/.4/.5/.6′/.7/.9
   are not circular.
8. **Conventions.** ℕ starts at 1 throughout; values vs positions never swapped
   (`pos[v]` vs `perm[i]` are consistently used); no drift to 194/195/197.
9. **Finite vs infinite.** Handled honestly. The scripts' docstrings correctly state
   that finite boards give *subgraphs* of G* (edges missing, never spurious) and that
   SAT gives no conclusion. One place where the finite shadow is exact and the report
   uses it correctly: U1-openness of `v` depends only on values ≤ `v`, so the G-digraph
   on [1..N] is the true restriction except for edges leaving the board. No finite
   computation is passed off as an infinite proof.
10. **SAT/CP as theorems.** Encoding re-derived and faithful (§1, R17.3). Protocol
    gap: the shipped `supply_window.py` uses a single solver with no proof logging and
    never validates SAT models. I re-ran every UNSAT with Glucose42 and validated
    every SAT model against `apcheck`; all pass. `cosupply_sat.py` already does both
    (its `second=True` path and its decode-and-assert) — good practice that
    `supply_window.py` should copy.

---

## 5. What a reader should take away

- The route's core negative finding (R17.1 + R17.2) is **correct and worth keeping**:
  Theorem 16's forcing-chain reformulation is self-defeating, because in any
  ≺-descending digraph over an order of type ω every chain dies at a sink, and records
  are guaranteed sinks of G. Any "chain continuation" lemma of universal shape is
  refuted; only a cofinite quantitative lower bound `|Cl(u)| ≥ f(u)` with
  `#{u : f(u) ≤ P} < P` for some P (equivalently `f(u) ≥ u+1` eventually) can bite,
  and no such f exists for G.
- G* is a legitimate, correctly derived, strictly larger digraph, and the empirical
  gain is real (sinks 40–65 % → 1–3 %, chains 13–14 → 132 at N = 320). Its logical
  status is unchanged from Theorem 16's.
- **One claim is broken** (Lemma R17.8's explicit bound) and must be corrected or
  deleted before it is quoted anywhere. It is quarantined — nothing depends on it.
- Two hygiene items to fix in place: `census.py`'s "violations" line does not perform
  the board-edge separation the report reports, and `supply_window.sink_clauses` omits
  rules U3 and D3 from its G*-sink test (I re-ran with them; still SAT).
