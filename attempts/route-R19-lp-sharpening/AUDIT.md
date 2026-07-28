# AUDIT — route R19 (LP sharpening), adversarial

Auditor: independent adversarial pass, 2026-07-28. Target: `PROOFS.md` (§§1–6) of
`attempts/route-R19-lp-sharpening` plus the author's summary. Governing statement:
`PROBLEM.md`. Everything below was re-derived by hand and, where numerical,
re-computed with code written from scratch for this audit (no import of `r19lib`;
ground truth for AP-freeness is `experiments/apcheck.py`'s literal 4-subset scan).

Audit scripts (scratch, exact integer / `Fraction` arithmetic):
`/tmp/claude-0/-home-user-erdos/16d68b37-9cd8-5fc8-ae52-36a43a9b9dde/scratchpad/`
— `audlib.py`, `aud1.py` … `aud6.py` (identities, triadic formulas, witnesses,
exhaustive Thm 7/8 check, P6 check), `mix9.c` (exhaustive Thm 7/8 on all
monotone-4-AP-free permutations of [1..9]), `dfs3.c` (independent exhaustive
extinction search, no SAT solver), `mintau.c` (independent exact min Στ).

---

## Verdict table

| Claim | Verdict |
|---|---|
| P1 = Prop 1 (dictionary m/R/τ/e*) | **SOUND** |
| P2 = Prop 2 (ledger ⇒ Στ ≤ N²+N−N(N+1)/(2C)) | **SOUND** (but see Observation A: the inequality is strictly weaker than a triviality) |
| Prop 3(i) (C < C_ledger(N) ⇒ ledger proves LP-inc(C)) | **SOUND** |
| Prop 3(ii) + "exact ceiling C_ledger(N)" | **REPAIRABLE GAP** (two gaps: floors; and the ceiling is not the ceiling of profile-only reasoning — a strictly better constant follows from the route's own data) |
| P3 = Prop 4, Prop 5, Cor 6 (ledger ceiling < 2) | **SOUND** (repair for the floor step supplied and verified below; conclusion also survives the strengthened supply bound) |
| P4 = Prop 12 ("closures do not help the ledger") | **REPAIRABLE GAP — not a theorem**; downgrade to a remark |
| P5 = Thm 7 (I-step + **D-step**) | **SOUND** |
| P5 = Thm 8 (mixed closure ⊆ pred(u), \|Cl±(u)\| ≤ pos(u)) | **SOUND** |
| P5 = Thm 9 ("196-YES ⟺ infinite mixed chain", "strict refinement of Thm 16") | **SOUND BUT VACUOUS**; "strict refinement" is not a mathematical claim — REPAIRABLE (reword) |
| P6 (A_e has no 4-AP of difference ≥ e; \|A_e\| ≤ e·r₄(⌈N/e⌉)) | **SOUND** |
| CERTIFIED: mixed closure on all avoiders N ≤ 9 | **CONFIRMED independently** |
| CERTIFIED: plain extinction C=1, 5/4, 3/2, 7/4 | **CONFIRMED independently** (exhaustive DFS, no SAT solver) — this closes the DRAT gap for the *results* |
| CERTIFIED: ledger-ceiling table §6.1 | **MOSTLY CONFIRMED**, two data-integrity defects (N=20 row; 5 bogus stored witnesses) |
| MEASURED §6.3 (triadic vs D-step) | **REPRODUCED EXACTLY** |
| MEASURED §6.4 (closures on SAT avoiders) | **NOT REPRODUCIBLE** from stored artifacts (no witnesses stored) |

---

## 1. P1 — Prop 1 (dictionary). SOUND.

Re-derivation. For v < w, pos(v) ≥ pos(w) ⟺ pos(v) > pos(w), so
m(w) = min{v ≤ w : pos(v) ≥ pos(w)} is the least element of [1..w] outside pred(w),
[1..m(w)−1] ⊆ pred(w), m(w) ∉ pred(w); pred(w) is exactly the value set of positions
< pos(w), so R(pos(w)) = m(w) − 1. (b) is reindexing by the bijection pos. (c) is the
layer-cake identity R(p) ≥ j ⟺ τ_j ≤ p−1, giving Σ_p R(p) = Σ_j (N − τ_j) = N² − Στ.
All boundary cases fine (R(1) = 0, m(1) = 1, e*(1) = 0, τ_j ≤ N so no negative counts).

Machine (independent implementation, `aud1.py`): identities (a),(b),(c), the two
characterisations of e*, and the scope-note identity `#{w : m(w) ≤ s} = τ_s` hold on
3000 random permutations of sizes 1–11. Also verified: **m is idempotent**
(m(m(w)) = m(w) on 2000 random permutations), which is exactly the reason the
"chained/multi-scale ledger" in the FAILED list gives nothing — that remark is correct.

## 2. P2 — Prop 2. SOUND, but the inequality is weaker than a triviality.

pos(w) ≤ pos(m(w)) ≤ ⌊C·m(w)⌋ ≤ C·m(w); sum and apply Prop 1. Correct; uses finite
surjectivity (Σ pos = N(N+1)/2) legitimately, obtained from the restriction principle.

**Observation A (new, and the report should state it).** For *any* permutation of
[1..N] with pos(v) ≤ Cv — 4-AP-free or not — one has τ_j = max_{v≤j} pos(v) ≤
min(N, ⌊Cj⌋), hence Στ ≤ P_N(C) := Σ_{j≤N} min(N, ⌊Cj⌋). Over a grid of
C ∈ {4/4,…,24/4} × N ≤ 300 (exact arithmetic, `aud5.py`):

  **P_N(C) ≤ B_N(C) := N² + N − N(N+1)/(2C) always**, with equality only at C = 1,
  and typically B_N − P_N = Θ(N).

So the ledger's supply inequality is *implied by, and strictly weaker than*, the
elementary bound τ_j ≤ min(N, ⌊Cj⌋). Both are Θ(N)-close to (1 − 1/(2C))N², so the
whole ledger constant 1/(2−2γ) is really the calibration of the trivial profile bound
against the demand bound. This does not falsify anything but it re-scopes Prop 2/3
(see §3 Gap B), and it also shows why "improve the supply side" is a dead end.

## 3. Prop 3. (i) SOUND. (ii) REPAIRABLE GAP (two independent gaps).

(i) is immediate and correct: C < C_ledger(N) ⇒ B_N(C) < S_inc(N) ≤ Στ(σ) for every
inc-4-AP-free σ, contradicting Prop 2.

**Gap A (floor slip).** Prop 3(ii) is stated for "the argument that combines only
Σ_w pos(w) = N(N+1)/2 with **pos(w) ≤ ⌊C·m(w)⌋**", but its proof only refutes the
floor-free relaxation `Σ pos ≤ C·Σ m`. The floor-refined ledger is
`Σ_w ⌊C m(w)⌋ = Σ_s (τ_s − τ_{s−1})·⌊Cs⌋ ≥ N(N+1)/2`, which depends on the whole
m-distribution, not on Σ m alone, and is up to N stronger. Since
CΣm − N ≤ Σ⌊Cm⌋ ≤ CΣm, the true ceiling of the floor-refined unweighted ledger lies in
`[C_ledger(N), C_ledger(N)·(N+3)/(N+1)]` — an O(1/N) relative gap, but the word
"exact" is unjustified as written. *Repair:* state Prop 3(ii) for the floor-free
ledger (Prop 2's last inequality), or redefine C_ledger by the floor-refined condition.
Note the report's own scope note concedes that weighted ledgers are outside Prop 3(ii);
the floor step *is* a weighting (weights ⌊C(s+1)⌋ − ⌊Cs⌋ on τ_s after Abel summation).

**Gap B (the ceiling is not the ceiling).** "C_ledger(N) is the exact ceiling at board
size N" is false for the natural method class *"any upper bound on Στ derived from the
profile alone, compared against a profile-free demand bound"*. By Observation A the
sharper supply bound is P_N(C), and the resulting criterion `S_inc(N) > P_N(C)` is
strictly easier to satisfy. Concretely, with the route's **own** datum S_inc(16) = 159
(which I re-proved independently, §8):

  P₁₆(41/32) = 158 < 159 = S_inc(16)  ⇒  **LP-inc(41/32 = 1.28125) holds**,

versus the report's C < 136/113 = 1.20354 at the same board size. Similarly at
N = 8/12/24/32/40 the trivial supply beats C_ledger(N) by factors
1.094 / 1.081 / 1.049 / 1.044 / 1.033 (`aud5.py`). So Prop 3(ii) *understates* what the
route's own data proves; the "exact ceiling" language should be restricted to the
literal floor-free ledger.

**Scoping point that must be made explicit (else Prop 3 is circular).** S_inc(N) is the
minimum over inc-4-AP-free permutations **with no profile constraint**. That is the
right choice, and it must be stated as a restriction on the *demand* side, because if
the demand bound may use the profile the framework collapses: for every profile-C
permutation Στ ≤ P_N(C) ≤ B_N(C), so the profile-aware minimum never exceeds B_N(C)
when the class is non-empty, and the ledger "derives a contradiction" exactly when the
class is already empty — i.e. exactly when LP-inc(C) is already true. Prop 3 as written
is fine; the reader must not be allowed to read S_inc as profile-aware.

*Also:* Cor 6 (and the whole framework) tacitly assumes any ledger argument proves
LP-inc(C) via a contradiction at a finite board. That is how CORE Thm 12 works, and the
additive-slack form only *weakens* the supply bound (B is replaced by
N²+N − (N(N+1)/2 − NQ)/C > B), so no evasion there — but the assumption should be
stated.

## 4. P3 — Prop 4, Prop 5, Corollary 6. SOUND (with one repair, supplied).

Prop 4's proof is correct: for v ∈ I_k = [3^k, 3^{k+1}) one has pos(v) = 4·3^k − 1 − v,
so τ_j = pos(3^k) = 3^{k+1} − 1 for every j ∈ I_k; the geometric sum gives
Στ_T = (3/4)N² + N/2 at N = 3^{K+1} − 1, whence C_ledger(N) ≤ 2(N+1)/(N+2) < 2.
Machine: exact match for K = 1..9 (N up to 59048); Prop 5's uniform formula
`Στ_T = N² − NA + (3/4)A² + N − A + 1/4` matches for **all** N ≤ 2000 (exact
`Fraction`); triadic verified inc-4-AP-free and pos(v) ≤ 3v−1 at N = 26, 80, 242, 728;
C_ledger UBs reproduced (9/5, 27/14, 81/41, 243/122, 729/365).

The "< 2 for every finite N" step is correct and has a clean proof the report can use:
with A ≤ N < 3A, 4(B_N(2) − Στ_T) = −[(N−A)(N−3A) + (N−4A+1)] > 0 because
(N−A)(N−3A) ≤ 0 and N − 4A + 1 ≤ −A < 0.

**Repair applied for Gap A at C ≥ 2:** since ⌊Cs⌋ ≥ 2s for C ≥ 2, the floor-refined
ledger asks Σ_w ⌊C m(w)⌋ ≥ Σ_w 2m(w) = 2(N + N² − Στ) ≥ N(N+1)/2, i.e. exactly
Στ ≤ B_N(2) — which is the inequality just proved for triadic. Verified numerically for
all N ≤ 2000. So **Cor 6 holds for the floor-refined unweighted ledger too**.

**Cor 6 also survives the strengthened supply bound of Observation A:** Στ_T(N) ≤ P_N(2)
for all N ≤ 3000, with *equality* exactly at N = 3^{K+1} − 1 (margins 0 at
N = 8, 26, 80, 242, 728, 2186). Since a contradiction needs strict inequality, no
profile-only supply bound refutes C = 2 either. (The margin is only Θ(N), i.e. the
ceiling 2 is asymptotically attained by triadic; it is not a comfortable barrier.)

Wording: the summary's header "**LEDGER CEILING = 2**" should read "≤ 2"; the body of
§6.1 states this correctly ("The PROVED statement is only sup_N C_ledger(N) ≤ 2").

## 5. P4 — Prop 12. NOT A THEOREM (REPAIRABLE: downgrade to a remark).

Two ingredients are correct and verifiable:
* the I-step is precisely case i = 2 of CORE Thm 12's demand disjunction, conditioned on
  the failure of cases i = 0, 1 (re-derived: openness of u = x+2e at scale e says
  pos(x) < pos(x+e) < pos(x+2e)); so it adds no new drop to the ledger's demand count;
* Σ_u |Cl±(u)| ≤ Σ_u pos(u) = N(N+1)/2 is trivially true.

But the load-bearing sentence — "the only inequality a lower bound yields is
Σ_u|Cl±(u)| ≤ N(N+1)/2" — quantifies over an undefined class of arguments and is not
provable; the conclusion "Mission item (1)'s proposed lever is structurally void" is
therefore rhetoric, not a proposition. A one-line counter-consideration: combining
Thm 8 with the profile gives |Cl±(u)| ≤ pos(u) ≤ Cu, a constraint on closure sizes that
is not of the stated form and that the ledger framework does not see. *Repair:* relabel
Prop 12 as a Remark and tag its conclusion MEASURED (the 24–44 % occupancy figure is
the actual evidence).

## 6. P5 — Theorems 7, 8, 9.

**Theorem 7. SOUND.** I-step is CORE Thm 16(a). D-step re-derived from scratch: assume
pos(u+2d) < pos(u+d) < pos(u) with u − d ≥ 1, and suppose pos(u) < pos(u−d). Reading
the four values in increasing position order gives (u+2d, u+d, u, u−d) = (x+3d, x+2d,
x+d, x) with x = u−d ≥ 1 and d ≥ 1 — a decreasing monotone 4-AP in PROBLEM.md's exact
sense (positions strictly increasing, common difference d ≥ 1 in the values, no value
reused). Positions are distinct by injectivity, so pos(u−d) < pos(u). Existence of
u+d, u+2d uses surjectivity of the permutation of ℕ (in the finite check, u+2d ≤ N —
correctly enforced in `mixed_closure.py:coopen_scales`). No boundary slip (u−2d ≥ 1 for
the I-step, u−d ≥ 1 for the D-step).

**Theorem 8. SOUND.** Every edge strictly decreases pos, chains are ≺-descending, so
Cl±(u)∖{u} ⊆ pred(u), |pred(u)| = pos(u) − 1. Order type ω is used here (and only here)
and is justified.

**Theorem 9. SOUND BUT VACUOUS; "strict refinement" unsupported.** Finite branching is
correct (open scales d ≤ (u−1)/2, co-open d ≤ u−1, out-degree ≤ 3(u−1)/2 — the report
writes "<", harmless). But by Theorem 8 *no* monotone-4-AP-free permutation of ℕ admits
an infinite mixed chain; hence the right-hand side of the claimed equivalence is
"∀σ ∈ S : false", which is equivalent to S = ∅, i.e. to 196-YES, for trivial reasons.
The König step is superfluous (Cl±(u) is finite unconditionally by Thm 8). The claim
that this is "a strict refinement of CORE Thm 16" is not a mathematical statement: both
statements are logically equivalent (each ⟺ 196-YES); what is true is the *measured*
fact that the mixed closure is larger. The report's own Remark 11 concedes the
reformulation status; the summary should too. Nothing here is wrong, but nothing here
is progress toward YES either — checklist item 7 (circularity) applies.

**Machine (independent, `mix9.c`).** I-step, D-step, closure containment and
|Cl±(u)| ≤ pos(u) on **all** monotone-4-AP-free permutations of [1..N] for N = 4..9:
22 / 102 / 564 / 3336 / 22 266 / 168 864 boards (= 195 154), **zero violations**;
max |Cl±| = 2/3/3/4/5/6. Counts match the report exactly.

## 7. P6 — the A_e side lemma. SOUND.

A_e = {w : pos(v) < pos(w) for all v ≤ w−e}. If w, w+d, w+2d, w+3d ∈ A_e with d ≥ e,
then each term is ≥ e below the next, so each consecutive pair is forced increasing and
(w, w+d, w+2d, w+3d) is an increasing monotone 4-AP. Splitting [1..N] into residue
classes mod e (each of size ≤ ⌈N/e⌉; a 4-AP inside a class has difference a multiple of
e, hence ≥ e) gives |A_e| ≤ e·r₄(⌈N/e⌉). Verified exhaustively on all inc-4-AP-free
permutations of [1..N], N ≤ 8 (`aud3.py`): zero violations, and A_e agrees with
{w : e*(w) < e}. Correctly reported as quantitatively too weak.

## 8. Machine claims (CERTIFIED / MEASURED)

**8.1 Plain linear-profile extinction — CONFIRMED by an independent method.**
I wrote an exhaustive depth-first search that uses no SAT/CP solver at all
(`dfs3.c`): assign pos(1), pos(2), …, pos(N) in **value** order with pos(v) ≤ ⌊Cv⌋;
every monotone 4-AP has a largest value, so checking, at the assignment of v, all
(v−3d, v−2d, v−d, v) for both orientations is a complete test; plus a Hall
feasibility prune. Results (exhaustive, exact):

| C | N | verdict | nodes |
|---|---|---|---|
| 1 | 3 / 4 | SAT / **UNSAT** | 4 |
| 5/4 | 3 / 4 | SAT / **UNSAT** | 4 |
| 3/2 | 14 / **15** | SAT / **UNSAT** | 371 / 1387 |
| 7/4 | 30 / **31** | SAT / **UNSAT** | 5.2·10⁷ / **8.07·10⁷** |

This reproduces every extinction point in §6.5 by a fourth engine and a structurally
different (non-clausal, non-propositional) method, so the honest DRUP/DRAT gap the
author flagged no longer endangers the *results* (the trace itself remains unchecked;
the author's diagnosis that pysat's Cadical stream is not a stand-alone DRAT proof for
the rebuilt formula is plausible and I did not pursue it). Both stored SAT witnesses
(C=3/2, N=14 and C=7/4, N=30) verified against `apcheck.has_monotone_kap_brute` and the
profile. **Not verifiable:** "C=2 SAT at N=49" — no witness stored; my DFS did not find
one in 110 s (this is not evidence against; a plain DFS is a poor solution-finder).
Downgrade that row to "reported, witness not retained".

I also re-derived both CP-SAT encodings: `plain_extinct.py` (fully reified drop
booleans b_i ⟺ pos(u+(i+1)e) < pos(u+ie), then `BoolOr(b)` = "not all ascents" and
`BoolOr(¬b)` = "not all descents", plus AllDifferent and pos(v) ∈ [1, min(N,⌊Cv⌋)]) and
`min_tau.py` (half-reified drops — sound, since only b ⇒ drop is needed — plus
τ₁ = pos(1), τ_j = max(τ_{j−1}, pos(j)), minimise Στ). Both are faithful to the
mathematical statements. Monotonicity in N used by the bisection is correct
(restriction principle).

**8.2 min Στ optima — CONFIRMED.** Independent exact branch-and-bound (`mintau.c`,
value-order assignment so τ accumulates exactly, bound τ_j ≥ max(τ_v, j) for j > v):
S_inc = 22 (N=6), **40 (N=8)**, 62 (10), 75 (11), **90 (N=12)**, **159 (N=16)** —
matching the "OPT" rows of §6.1 (N = 8, 12, 16) with no solver in common.

**8.3 §6.1 table — recomputed, two defects.** Every C_ledger value in the table is the
correct function of the stated Στ (all 18 rows re-derived as exact rationals). But:
* **N = 20 row is unsupported.** The report states min Στ = 248 → 105/86 = 1.22093;
  both logs (`min_tau.log`, `min_tau_plain.log`) state 249 → 70/57 = 1.22807, and no
  witness with 248 exists anywhere in the directory. The report's row is the *stronger*
  (smaller-ceiling) claim, so this is a real, if immaterial, overstatement.
* **`witnesses.txt` contains 5 permutations whose Στ is not the claimed value**:
  N=48 (actual 1581 vs claimed 1576), N=56 (2330 vs 2200), N=64 (3043 vs 2952),
  N=80 (**6229 vs 4840**), N=96 (**9214 vs 6376**). The claimed numbers are in fact the
  *triadic* values (Prop 5 gives 1576/2200/2952/4840/6376 at those N — I checked), so
  the numeric claims survive, but the stored objects do not certify them. The
  local-search block *does* verify exactly (N=40:1031, 48:1518, 56:2150, 64:2776,
  80:4652, 96:6124, 112:8180, 128:10734 — all genuine inc-4-AP-free permutations with
  exactly the claimed Στ), and those are the rows the final table uses. Fix the file.
* Minor: the summary says γ ≤ 0.678 "everywhere except N=80"; the table itself has
  0.68559 at N=56.
* Minor: `min_tau.py`'s docstring states a *wrong* formula ("ledger proves LP-inc(C)
  iff min Στ > C·N(N+1)/2", "C_ledger = 2·min_tau/(N(N+1))"); the code's `C_ledger`
  function is right. Fix the docstring — it is the primary tool documentation.

**8.4 §6.3 (triadic vs D-step) — REPRODUCED EXACTLY** with independent code
(`aud6.py`): N=26: I-trig 7 / 0 viol, D-trig 78 / 48 viol, 18/26 escapes, ratio 2.18;
N=80: 95/0, 780/507, 69/80, 2.69; N=242: 966/0, 7260/4800, 228/242, 2.89.

**8.5 §6.4 (mixed closures on SAT avoiders) — NOT REPRODUCIBLE.** The permutations
come from `sat_order.solve` and are not stored, so the numbers (in particular the
`max |Cl±(u)|/pos(u) = 0.980 at N = 160, u = 97, pos = 153` that the recommended next
step leans on) cannot be checked; `stuck_scan.log` reports the unrestricted ratio as
1.000 at every N, and the report's restricted-to-pos ≥ N/4 column appears nowhere in
the logs. Store the witnesses, or tag the row "not retained".

## 9. Checklist sweep

1. **Both orientations.** Handled where needed: the D-step is a genuine
   decreasing-orientation rule and is used correctly; P1–P3, P6 and Cor 6 are
   explicitly increasing-only (the correct choice — they bound *increasing-only*
   methods) and say so. The plain-extinction encodings cover both orientations.
2. **Positions/differences/reuse.** Verified: all 4-AP tests I re-derived agree with
   the literal position-4-subset definition on 3000+ random boards; d ≥ 1 throughout;
   no reindexing.
3. **Injectivity / surjectivity / ω.** Injectivity: distinct positions (Thm 7),
   AllDifferent (encodings). Surjectivity: Σ pos = N(N+1)/2 (Prop 2, the ledger's whole
   left-hand side) and the existence of u±d, u+2d at finite positions (Thm 7).
   ω: pred(u) finite (Thm 8) and no infinite descending chain (Thm 9). No YES-side
   claim in R19 rests on an argument that omits surjectivity — and note the only
   YES-side statement (Thm 9) is vacuous anyway.
4. **Compactness/limits.** R19 introduces none of its own. The one citation
   (CORE Lemma 6, in `plain_extinct.py`'s docstring) is stated correctly and CORE's
   proof does preserve order type ω (φ-bounded tree + König + Lemma 1). ✓
5. **Named theorems.** König (Thm 9): hypotheses verified but the use is superfluous.
   r₄/Szemerédi (P6): used only for an upper bound on 4-AP-free sets, correctly, in a
   branch the author already declares dead.
6. **Boundary cases.** u−2d ≥ 1, u−d ≥ 1, u+2d ≤ N enforced; m(1)=1, e*(1)=0; τ_j ≤ N
   so Prop 1(c) has no negative terms; C_ledger's denominator N²+N−S_inc > 0 always
   (Στ ≤ N²). The one real floor slip is Prop 3(ii) (Gap A).
7. **Circularity.** Theorem 9 is a vacuous restatement of 196-YES (flagged). Prop 3
   would become circular if S_inc were read as profile-aware (flagged, §3).
8. **Conventions.** N starts at 1; values vs positions never swapped (checked
   numerically throughout); no drift to 194/195/197.
9. **Finite vs infinite.** Finite computations are consistently tagged as evidence
   about finite boards. Prop 3(i) *is* a legitimate finite→infinite step (restriction),
   and Cor 6's negative claim implicitly assumes finite-board ledger arguments — should
   be stated, but the additive-slack variant only weakens the supply side, so the claim
   is robust.
10. **SAT/CP as theorems.** Encodings re-derived and faithful; every UNSAT point
    re-confirmed by an independent non-SAT exhaustive search; the "OPT" min-Στ values
    re-confirmed by independent branch-and-bound.

## 10. Net assessment

Nothing in R19 is **BROKEN**. The two mathematically substantive novelties are:
(a) the exact ledger↔Στ dictionary (P1–P2), which is correct and useful, and
(b) the D-step / mixed closure (Thm 7–8), which is correct, genuinely two-orientation,
and exhaustively verified — but whose "equivalence" packaging (Thm 9) is vacuous, so
the route's headline "strict refinement of CORE Thm 16" should not be read as progress.
The ceiling result (Cor 6) is correct and survives both repairs I applied (floors;
strengthened profile-only supply), but the margin is only Θ(N): triadic *saturates* the
C = 2 profile bound at N = 3^{K+1} − 1.

Two things the route should take from this audit:
* the ledger supply side is strictly dominated by `τ_j ≤ min(N, ⌊Cj⌋)` (Observation A);
  using it, the route's own S_inc(16) = 159 already yields **LP-inc(1.28125)**, better
  than the 1.20354 claimed as the board-16 ceiling;
* fix `witnesses.txt` (5 mismatched entries) and the N = 20 table row (248 → 249).
