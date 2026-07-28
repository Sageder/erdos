# AUDIT — route R16-τ (τ-repair question)

Adversarial audit, 2026-07-28. Auditor re-implemented τ from the definition in a separate
file (`/tmp/.../scratchpad/audit_all.py`, `audit_lemmaC.py`) and used only
`/home/user/erdos/experiments/apcheck.py` (`has_monotone_kap_brute`,
`has_monotone_kap_general`) as ground truth for monotone-AP detection. All the route's own
scripts were re-run.

## 0. Meta

**M1 — There is no REPORT.md, and the scripts forward-reference one.**
`/home/user/erdos/attempts/route-R16-tau/` contains only scripts and `.out` files.
`open_tau.py`, `override.py`, `selfsim_chain.py`, `theory_checks.py`, `level0_blocks.py`,
`level_sat.py` all cite "proved in REPORT.md sec. 4/5/6" for their central claims. Those
sections do not exist anywhere on disk. The only statement of the proofs is the returned
summary, which is itself truncated in the middle of P7. Every proof below therefore had to
be reconstructed from a one-or-two-line sketch. This is the single biggest defect of the
route as delivered: the docstrings assert provenance that cannot be checked.

**M2 — Scope.** Nothing in P1–P7 bears on either branch of Erdős 196. They are (i) a
re-derivation of CORE Remark 20(a), (ii) structure theory for τ, and (iii) three negative
results about τ-based repair families. The route states this. No claim is circular; in
particular Theorem 16(c) — which CORE itself already flagged as a vacuous P ⟺ P — is
**not** used anywhere here. Only Theorem 16(a) is used, and correctly.

**M3 — The VERDICT paragraph's "located corridor" is not a proved claim.**
"the obstruction is not at any base-3 level, it is the coherence between levels" reads as
a result but is not one, and as phrased it sits awkwardly against the route's own P5,
which says τ's rule is fatal *at every single (level, context)*. The defensible reading —
"the *level-0 problem* (kill monotone 4-APs with 3∤d) may be solvable by an ω-order even
though τ's rule is not" — rests entirely on `level0_blocks.py` returning SAT for
N ≤ 300 under a contiguous-base-3-block layout (`lvl0blocks.out`, `lvl0big.out`).
PROBLEM.md is explicit that finite computations cannot settle the infinite statement, and
a *satisfiable* finite instance is even weaker evidence than an UNSAT one. Report it as an
experiment, never as a location theorem. (Checklist item 9.)

---

## 1. Verdicts

### P1 — Lemma T (τ kills all monotone 4-APs, context-dependent priorities). **SOUND.**

Re-derived. With `v = v₃(d)`, `3^v | d` so all four terms of `(x, x+d, x+2d, x+3d)` share
their digits below level `v`; hence all three *adjacent* pairs have `v₃` exactly `v` and the
identical context `c = x mod 3^v`, and are decided by the one priority `pr(v,c)`. Their
level-`v` digits are `a, a+δ, a+2δ, a+3δ = a (mod 3)` with `δ = dig_v(d) ≠ 0`, so the three
adjacent comparisons form a closed 3-cycle of ranks, and neither `≺≺≺` nor `≻≻≻` can hold.
Both orientations are covered by the same cycle. τ is genuinely a linear order (it is lex
order on the key `(pr(l, n mod 3^l)[dig_l(n)])_{l≥0}`, which is well defined since any two
naturals agree in all but finitely many digits), so transitivity is not assumed but proved.

Independent machine check: 13 priority families (6 constant, 3 per-level, 4
context-dependent), full `(x,d)` scan on the τ-sorted `[1..3000]`, plus 780 random subsets
through `has_monotone_kap_general` and 2600 8-element subsets through
`has_monotone_kap_brute`: **0 monotone 4-APs**; 3-APs present in every family.

Caveats, both harmless: (a) this is CORE Remark 20(a) with the priority allowed to depend
on the shared low digits `c` as well as on `l` — a real but modest strengthening, and the
summary's "re-derived and strengthened" is accurate; (b) the summary says 3-APs are present
"as DEGS77(a) requires" — DEGS77(a) is a theorem about permutations of ℕ and τ is not one,
so it *requires* nothing here. τ does contain 3-APs, verified.

### P2 — Lemma O (openness is a two-digit condition) + Cor O2 + never-open set. **SOUND.**

Re-derived. `u` open at `d` means `u−2d ≺_τ u−d ≺_τ u`; all three values share context
`c = u mod 3^v` (`v = v₃(d)`, `3^v | 2d`), so increase forces
`(dig_v(u−2d), dig_v(u−d), dig_v(u)) = (x₁,x₂,x₃)`. Because `x₁+x₂+x₃ ≡ 0 (mod 3)` one has
`x₃−x₂ ≡ x₂−x₁`, so the single condition `δ = δ*` suffices, and `dig_v(u) = x₃`,
`dig_v(u−2d) = x₃−2δ* = x₁`. Converse identical. Cor O2 is the same statement with the
smallest admissible `d = δ*·3^v`, and `u−2d ≥ 1 ⟺ 2δ*3^v < u`; `δ* ∈ {1,2}` always, so
`v₃(δ*3^v) = v` as needed. The domain condition `u − 2d ≥ 1` is carried correctly
everywhere (checklist item 6).

Independent machine check: raw definition vs formula for **all** `u ≤ 3000` across the same
13 families, plus Cor O2 — 0 mismatches. Never-open classification verified as an exact set
identity on `[1..60000]`: `{u : all base-3 digits in {0,1}} ∪ {2·3^L}` — matches.

Cosmetic: the summary writes `δ* = x₂ − x₁`; it must be `(x₂ − x₁) mod 3` (the code does
this).

### P3 — Theorem T3 (explicit infinite forcing chain in τ). **SOUND**, with two stated-hypothesis slips and an overstated "significance".

The chain is real. `26 →(9) 35 →(12) 47 →(9) 56 →(22) 78 = 3·26`; scaling by 3 concatenates
copies into `3^k·{26,35,47,56}`. Verified from the raw definition (not via Lemma O) for 36
consecutive links (9 scaled copies): every link has `d ≥ 1`, `u−2d ≥ 1`, values strictly
increasing, `(u−2d, u−d, u)` τ-increasing, and `u+d ≺_τ u`. So τ contains an infinite
strictly ≺-descending sequence.

Slips, both repairable in one line each:
1. **Lemma O3 (`u` open at `d` ⟺ `3u` open at `3d`) needs priorities constant in level
   *and* context.** The summary states it unconditionally. Machine check: true for all 6
   constant families, **false** for context-dependent families. The chain uses the natural
   (constant) priorities, so T3 itself is unaffected; state the hypothesis.
2. "By Theorem 16(a) each step gives `u_{k+1} ≺_τ u_k`" quotes Theorem 16(a) in its
   CORE form, which is stated for a monotone-4-AP-free **permutation** of ℕ. τ is not a
   permutation. The proof of 16(a) uses only 4-AP-freeness of a *linear order*, which P1
   supplies, so the conclusion stands — but the generalisation must be said out loud, and
   the scripts do verify `t.before(u+d, u)` directly, which makes the point moot in practice.

**Corollary T3′ — SOUND.** If a monotone-4-AP-free order `≺` had `u_k` `≺`-open at `d_k`
for all `k ≥ K`, the tail `u_K ≻ u_{K+1} ≻ ⋯` would be an infinite `≺`-descending sequence,
impossible in type ω. So infinitely many links break, and by Lemma O each break reverses τ
on `(u_k−2d_k, u_k−d_k)` or `(u_k−d_k, u_k)`. `v_k = v₃(d_k)` runs
`2,1,2,0, 3,2,3,1, 4,3,4,2, …` → ∞, as claimed.

**"Significance" paragraph — OVERSTATED (not a proof claim, but flag it).** "τ's two known
defects coincide … the same phenomenon" is not established. An infinite forcing chain
*implies* infinite predecessor sets; the converse is not shown, and τ's infinite
predecessor sets are visible far more cheaply — with natural priorities
`3 ≻_τ 9 ≻_τ 27 ≻_τ 81 ≻ ⋯` is an infinite descending sequence read straight off the
level-`k` rule. T3 refines the defect; it does not identify the two.

### P4 — Prop R1 (LSD-rigidity, contexts allowed). **SOUND.**

At `l = 0` the context is empty, so the decision on any pair with distinct residues mod 3
is a function of the two residues alone: a tournament on `{0,1,2}`, transitive because `≺`
is, hence a linear order `x₁ R x₂ R x₃`. The entire (infinite) `x₁` residue class then
precedes every element of the `x₂` class, so those have infinite predecessor sets. The
"upgrades CORE Remark 20(c)" claim is accurate: 20(c) allowed the priority to vary by
level, P4 additionally allows dependence on the shared low digits.

### P5 — Prop R2 (per-level override density) + corollary. **SOUND. This is the route's strongest result.**

Re-derived. Fix any linear order `≺` on ℕ with all predecessor sets finite (4-AP-freeness
is *not* needed — the proposition is stronger than advertised), any priority family, any
`l ≥ 0` and any `c`. `S_{l,c} = {n ≥ 1 : n ≡ c mod 3^l}` splits into three infinite classes
by `dig_l`; a cross-class pair has `v₃`-difference exactly `l` and shared context `c`, so τ
decides it by `pr(l,c)`; the whole infinite `x₁`-class τ-precedes any `z` in the
`x₂`-class, while `pred_≺(z)` is finite. Hence infinitely many pairs of `S_{l,c}` disagree
with τ. ∎ Machine-measured over 52 `(family, l, c)` combinations.

Corollary checks out in both directions: "τ at levels ≤ L, free above" dies at `l = 0`;
"free below L, τ at levels ≥ L" dies at `l = L` (any `c`). No tie-break above/below is
consulted by the argument, so none can rescue either. Order type ω is used exactly once and
correctly (finiteness of `pred_≺(z)`); injectivity/surjectivity are not needed beyond that.

### P6 — Prop R3 (τ-convex reversal schedules). **REPAIRABLE GAP. Its Lemma C is BROKEN as stated; the conclusion survives with the replacement proof below.**

*What is correct.* The convexity step is right: if `≺` agrees with τ off a set `A` and is
reversed inside `A`, and `u,w ∈ A`, `z ∉ A` with `u ≺_τ z ≺_τ w`, then `u ≺ z ≺ w` forces
`u ≺ w`, contradicting the reversal — so every reversed piece is τ-convex.

*The gap.* **Lemma C — "every τ-convex set with ≥ 2 elements is infinite and densely
ordered by τ" — is FALSE for the context-dependent priorities that P1 and P4 explicitly
admit.** Counterexample (verified, `audit_lemmaC.py`):

```
pr(0, 0) = (0,1,2)            # rank(dig 0)=0 < rank(dig 1)=1 < rank(dig 2)=2
pr(l, 1) = (2,0,1)  for l ≥ 1 # digit 0 has MAX rank in context c = 1
pr(l, c) = (0,1,2)  otherwise
```

This τ is a linear order and is monotone-4-AP-free (P1 applies). But `1 ≺_τ 2` with
**nothing strictly between them**: `n ≡ 0 (mod 3)` gives `n ≺ 1`; `n ≡ 1 (mod 3)`, `n ≠ 1`
first differs from 1 at some level `m ≥ 1` in context `1`, where `dig_m(1) = 0` has maximal
rank, so `n ≺ 1`; `n ≡ 2 (mod 3)`, `n ≠ 2` first differs from 2 at some `m ≥ 1` in context
`2`, where `dig_m(2) = 0` has minimal rank, so `n ≻ 2`. Machine-confirmed: no `n ≤ 2·10⁵`
lies strictly between, and the residue-class case split is exhaustive. So `{1,2}` is a
τ-convex set of size 2 — finite, not dense. The summary's proof sketch ("`w+x·3^{l′}` or
`u+x·3^{l′}` according to whether `pr(l′,·)(0) is the minimum`") silently assumes the two
constructions see the *same* priority; with contexts they see `pr(l′, u)` and `pr(l′, w)`,
and an adversary can make the first fail and the second fail simultaneously at every level.

Lemma C **is** correct for every context-free family (priorities depending on `l` only,
including constant): then `p_{l′}[0] = 0` makes the `u`-side construction work and
`p_{l′}[0] = 2` makes the `w`-side work, and one of the two always applies.
Machine-verified for all 9 context-free families (2700 random pairs, gap-free).

*The repair (conclusion of P6 survives, for arbitrary context-dependent priorities).*
Do not go through density at all:

> Let `≺` be τ with a family of pairwise disjoint pieces reversed, and suppose every
> `pred_≺` is finite. Let `X₁ , X₂` be the `pr(0)`-first and `pr(0)`-second residue classes
> mod 3, so `X₁` is infinite and entirely τ-before `X₂`. Fix `z ∈ X₂` and let `A` be its
> piece (`A = {z}` if none). Cross-piece pairs agree with τ, so
> `pred_≺(z) ⊇ X₁ ∖ A`; finiteness forces `A ⊇ X₁ ∖ F` with `F` finite (in particular
> `A ≠ {z}` and `A` is infinite). Now apply the same one level down *inside* `X₁`: with
> context `c = x₁` at level 1, `X₁ = Y₁ ⊔ Y₂ ⊔ Y₃` in `pr(1, x₁)`-order, `Y₁` entirely
> τ-before `Y₂ ∪ Y₃`. Pick `y ∈ Y₁ ∖ F ⊆ A`. Every element of `(Y₂ ∪ Y₃) ∖ F ⊆ A` is
> τ-after `y` and lies in the same reversed piece, hence `≺`-before `y`. That set is
> infinite, so `pred_≺(y)` is infinite. Contradiction. ∎

This never mentions density, never needs `A` convex, and holds for arbitrary `pr(l,c)`. It
also subsumes the "all pieces are singletons ⇒ `≺ = τ` ⇒ P4" endgame.

*Scope reminder.* Even repaired, P6 kills only orders of the shape "τ with disjoint pieces
reversed". A general linear order's disagreement set with τ need not decompose that way, so
P6 is not "τ-repairs are dead"; the headline "τ-convex reversal schedules are dead" is the
correct scope and should stay that narrow.

### P7 — Override calculus. **SOUND but essentially tautological; one sentence of it is not a theorem.**

`A` is `≺`-increasing iff each adjacent pair is `≺`-increasing iff each pair is overridden
exactly when its τ-sign is `−`, i.e. `O ∩ {P₁,P₂,P₃} = S₋`; likewise decreasing/`S₊`. That
is a restatement of "disagree = flipped" and needs no hypothesis on `≺` beyond being a
linear order. The non-trivial input is P1's cycle, which makes `S₊`, `S₋` both non-empty of
sizes `{1,2}`, whence "override 0 or all 3 ⇒ safe" and the unique minority slot. The
`|S₋| = 1 ⟺ δ = δ*` / `|S₊| = 1 ⟺ δ = 2δ*` refinement is correct (checked by hand for all
three starting digits and independently by machine).

Independent check: random (non-graded, non-τ-related) linear orders on `[1..90]` against
random context-dependent τ, all `(x,d)`: 0 mismatches, and `|S₋| = 1 ⟺ dig_v(d) = δ*`
holds in every instance. The route's own `override.py` reports `mismatches=0` for its 5
orders.

The trailing sentence — "Damage is confined to APs on which the schedule is inhomogeneous,
i.e. **to boundaries**" — is not a theorem. "Inhomogeneous on this AP's three adjacent
pairs" is exactly what the calculus says; "boundaries" is an extra geometric reading of the
override set that is nowhere defined or proved. Keep the first clause, drop the second.

---

## 2. Checklist coverage

1. **Both orientations.** Lemma T's 3-cycle kills both; P7 states both. Lemma O is
   deliberately one-sided (increasing) because Theorem 16(a) is. OK.
2. **Positions strictly increasing, `d ≥ 1`, no reuse, no reindexing.** All AP scans use
   `d ≥ 1`, four distinct terms, and the positional test `p₀<p₁<p₂<p₃` / `p₀>p₁>p₂>p₃`.
   `taulib.mono4_witnesses` cross-validated against both trusted checkers (950 cases).
3. **Injectivity / surjectivity / order type ω.** τ is never claimed to be a permutation.
   Order type ω enters only as "predecessor sets finite" and only in P5, P6 and Cor T3′ —
   correctly, and it is the *hypothesis* being contradicted, so the "YES side that never
   uses surjectivity" trap does not apply (nothing here argues a YES side).
4. **Compactness / limits.** None used. König is not invoked (the route uses Thm 16(a)
   only, not 16(b)/(c)).
5. **Named theorems.** Only Theorem 16(a) from CORE and DEGS77(a) in passing. 16(a) is used
   outside its stated hypothesis (permutation vs linear order) — see P3 slip 2; harmless.
   DEGS77(a) is cited as if it constrained τ; it does not — see P1 caveat.
6. **Boundaries.** `u − 2d ≥ 1` is carried in Lemma O, Cor O2 and every script.
   `v₃(δ*3^v) = v` needs `δ* ≠ 0`, which holds. Cor O2's search bound `3^v ≤ u` is
   sufficient since `2δ*3^v < u ⇒ 3^v < u`. One boundary the density sketch glosses: the
   "middle digit at level `l`" candidate can be `0 ∉ ℕ`, which is why the high-level
   construction is needed; the sketch's "when available" covers it only implicitly.
7. **Circularity.** None. Theorem 16(c) (self-flagged in CORE as P ⟺ P) is not used.
8. **Conventions.** ℕ from 1 throughout; values vs positions never swapped; no drift to
   194/195/197.
9. **Finite vs infinite.** P1–P7 are proofs, not finite extrapolations — with the single
   exception of the VERDICT's "corridor" framing (M3), which leans on SAT-at-N≤300.
10. **SAT used as theorem.** No SAT result is used as a theorem in P1–P7. For the record,
    the encodings in `level_sat.py` / `level0_blocks.py` were re-derived and are faithful:
    variables `x(u,w)` for `u<w`, the two clauses `[-a,-b,c]`, `[a,b,-c]` per triple
    forbid exactly the two 3-cycles (a 3-cycle-free tournament is a linear order), and
    `[-y1,-y2,-y3]` / `[y1,y2,y3]` forbid exactly the increasing / decreasing orientation.
    Models are independently re-verified. Every reported run is SAT, so the fact that the
    "second solver" confirmation (Glucose on the same clause list) is not an independent
    UNSAT check never bites here.

---

## 3. Summary table

| Claim | Verdict |
|---|---|
| P1 Lemma T (τ 4-AP-free, contexts allowed) | **SOUND** |
| P2 Lemma O, Cor O2, never-open classification | **SOUND** |
| P3 Theorem T3 (explicit infinite forcing chain) | **SOUND** (Lemma O3 hypothesis omitted; Thm 16(a) quoted outside its stated hypothesis; "significance" overstated) |
| P3′ Corollary T3′ | **SOUND** |
| P4 Prop R1 (LSD-rigidity with contexts) | **SOUND** |
| P5 Prop R2 + truncation corollary | **SOUND** (strongest result of the route) |
| P6 Prop R3 (τ-convex reversal schedules) | **REPAIRABLE GAP** — Lemma C **BROKEN** by explicit counterexample; conclusion restored by the replacement proof in §1 |
| P7 Override calculus | **SOUND but tautological**; "damage confined to boundaries" is not a theorem |
| VERDICT "corridor is the coherence between levels" | **NOT PROVED** — finite SAT observation (N ≤ 300) |
| Delivery | **DEFECTIVE** — no REPORT.md; six scripts cite non-existent sections of it |
