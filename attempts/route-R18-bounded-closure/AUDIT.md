# AUDIT — route R18 (bounded closure). Adversarial review.

Auditor stance: adversarial. Goal was to break the claims. Date 2026-07-28.
Target: `/home/user/erdos/attempts/route-R18-bounded-closure/` — **no `REPORT.md` or `STATUS.md`
exists**; the claims audited are those in the author's returned summary, with proofs read from the
module docstrings of `blocks.py`, `triesat.py`, `forcing_tools.py`, `blockalone.py`,
`blockalone_cp.py`, `windowsat.py`, `sat_height.py`, `measure.py`, `verify_unsat.py`, `blocksat.py`.
The summary itself is truncated mid-sentence ("Self-tested: e").

Everything below was re-derived by hand and, where a computation was involved, re-run with
independently written code (not importing the route's modules) and cross-checked with
`experiments/apcheck.py`.

---

## Verdict table

| Claim | Verdict |
|---|---|
| Prop R18.1 (vacuity of σ_N; HFIN(K) implies YES; HFIN(K) false ∀K) | **SOUND** |
| Prop R18.2 (block confinement of forcing edges) | **REPAIRABLE GAP** — missing hypothesis |
| Prop R18.3 (no logical gain from a height/closure bound over a φ-bounded family) | **SOUND** |
| Prop R18.4 (O meets every infinite AP; C infinite; C has no infinite AP) | **SOUND** |
| Prop R18.5 ("a forcing chain never repeats a scale") | **BROKEN** — explicit counterexample |
| Thm R18.6 (block decomposition of 4-AP-freeness) | **SOUND** |
| Cor R18.6.1(i) `r ≥ 3 ⇒ no [1+1+1+1]` | **SOUND** |
| Cor R18.6.1(ii) `r ≥ 2 ⇒ no [2+1+1]` | **BROKEN** — counterexample; correct at `r ≥ 3`, or `r ≥ 2` for *exact* geometric cuts |
| Cor R18.6.1(iii) `[2+2]` links only adjacent blocks (`r ≥ 3`) | **SOUND** |
| Cor R18.6.1(iii) `[1+1+2]` links only adjacent blocks | **BROKEN** — counterexample (harmless) |
| Cor R18.6.1(iv) isolated-block UNSAT kills the architecture | **SOUND** (but does not need the chain structure) |
| Lemma R18.7 (binary trie comparator has no monotone 3-AP on any subset) | **SOUND** |
| Thm R18.8 (collapse to unit/2-SAT) | **SOUND** derivation; **testing gap** in the direction actually used |
| "trie family dead for every ratio, one level deep" | **TRUE**, but the filed evidence is a finite sample; general proof supplied below |
| "geometric cuts r=3 and r=4 are dead" (two new finite theorems) | **SOUND** modulo solver correctness (4 engines, 2 independent derivations) — **scope must be stated** |
| Side finding: C=2 profile threshold | R18's data **contradicts CORE.md Remark 17**; R18 is right, CORE.md's entry is mislabelled |

No claim on the YES side is asserted by this route, so checklist item 3's trap ("a YES-side
argument that never uses surjectivity") applies only to the HFIN(K) ⇒ YES implication inside
Prop R18.1, which does use it (via the restriction principle). Verified below.

---

## 1. Prop R18.1 (vacuity) — SOUND

**(a) σ_N has an empty forcing digraph.** `experiments/parity_construction.py` verifies σ_N is
monotone-3-AP-free for all N ≤ 256 and N ∈ {512,1024,1536,2048}; PROBLEM.md grants it for all N.
No monotone 3-AP ⇒ no value is open ⇒ no edges. I re-confirmed with `forcing_tools`:

```
parity N=20/40/60/100/257 : 4-AP-free=True, edges=0, max|Cl|=1, max h=0, #open=0
```

So "all closures ≤ B" is SAT at every N for every B ≥ 1. The literal mission item 2 carries no
information. Correct.

**(b) HFIN(K) ⇒ 196-YES.** Re-derived step by step:
openness of `u` at scale `d` involves only the values `u−2d, u−d, u`, and restriction to `[1..M]`
preserves their relative order, so `u` open in `a` ⟺ open in `a↾[1..M]` (for `u ≤ M`); edges of the
restriction are exactly `a`'s edges with head ≤ M, hence `h_{a↾M}(u) ≤ h_a(u)`. Given HFIN(K), for
each H pick N(H) and apply it to `a↾[1..N(H)]` — legitimate because the restriction principle
(PROBLEM.md) says the values `{1..N}` in position order form a permutation of `[1..N]`, **and this
is exactly where surjectivity of `a` is used**. Get `u_H ≤ K` with `h_a(u_H) ≥ H`. Pigeonhole over
the finite set `{1..K}` gives a fixed `u*` with arbitrarily long forcing paths. The forcing digraph
is finitely branching (scales at `u` satisfy `d ≤ (u−1)/2`), so König's lemma on the tree of finite
forcing paths from `u*` yields an infinite path; Thm 16(a) makes it ≺-descending; order type ω
(CORE Lemma 1) forbids that. Correct. Order type ω and surjectivity are both used, injectivity
implicitly throughout.

**(c) HFIN(K) is FALSE for every K.** Immediate from (a) at H = 1. Correct.

*Notational hazard only:* the same symbol `σ_N` denotes the parity permutation in (a),(c) and the
restriction `a↾[1..N]` in (b). Not an error, but it should be disambiguated in any write-up.

## 2. Prop R18.2 (block confinement) — REPAIRABLE GAP

As stated in the summary's VERDICT §1 — "**In any layered permutation** … every forcing edge stays
inside one block" — this is **false**. The proof leans on `pos(u+d) < pos(u)`, which is Thm 16(a)
and is available **only for monotone-4-AP-free permutations**.

Counterexample (constructed, verified with `forcing_tools.forcing_digraph`): the identity
permutation of `[1..9]` is layered for cuts `(1,4,10)`; value 3 is open at scale 1
(`pos(1)<pos(2)<pos(3)`), so there is a forcing edge `3 →(1)→ 4` with `blk(3)=0`, `blk(4)=1`.

**Repair:** state it as "in a monotone-4-AP-free layered permutation …". With that hypothesis the
argument is correct and gives `Cl(u) ⊆ B(u) ∩ [u,∞)`, `h(u) < |B(u)|`. The docstring of `blocks.py`
has the same omission. The route's *conclusion* (chain-termination is free inside the layered
design family) is unaffected, because that family is by construction 4-AP-free.

Machine claim re-checked: all three witness files have 0 cross-block forcing edges.

```
witness_geom3_N26.json: N=26 cuts=[1,3,9,27]  4AP-free=True layered=True edges=26  cross=0
witness_geom3_N80.json: N=80 cuts=[1,3,9,27,81] 4AP-free=True layered=True edges=192 cross=0
witness_geom4_N63.json: N=63 cuts=[1,4,16,64] 4AP-free=True layered=True edges=106 cross=0
```

## 3. Prop R18.3 (no logical gain) — SOUND

`h(u) ≤ |Cl(u)|−1` (values strictly increase along edges, so a path's vertices are distinct and lie
in `Cl(u)`); `|Cl(u)| ≤ pos(u)` is Thm 16(b) applied to the restriction, which is 4-AP-free by the
restriction principle; `pos_{a↾N}(u) ≤ pos_a(u) = φ(u)` because restriction only deletes elements.
Chain valid. The conclusion — that UNSAT of "φ-bounded **and** height/closure-bounded" is strictly
weaker than what a YES theorem needs — follows and is correct.

**Encoding audit of `sat_height.py` (checklist item 10).** Re-derived. `op[u,d]` is introduced only
by `x1 ∧ x2 → op` and used only negatively, so the minimal model `op = openness` is always
available: complete. Any model gives an `op` superset of the true openness, so the H-clauses are
at least as strong as the real height constraint: sound. `K = 0` is special-cased to
`¬x1 ∨ ¬x2`, which correctly forbids any in-board out-edge. Targets are restricted to `u+d ≤ N`,
matching `h_N`. Decoded models are re-verified with `apcheck` and `board_stats`. Faithful.

**Convention flag:** `sat_height.py` uses `pos(v) ≤ ⌈C·v⌉`; CORE.md Remark 17 states `⌊C·v⌋`. They
agree only at integer C. The C = 1.5 and C = 3 rows of `log_satheight.txt` are therefore **not**
comparable with CORE.md's table.

## 4. Prop R18.4 (supply corollaries) — SOUND

(a) For an infinite AP `A + bℕ₀` apply Lemma 16.1 at `w = A`, modulus `m = b`: it produces
`e ∈ bℕ` (so `e ≥ b ≥ 1`) with `(w, w+e, w+2e)` positionally increasing, i.e. `w+2e` is open at
scale `e`, and `w+2e = A+2e ∈ A + bℕ`. Boundary `u−2d = A ≥ 1` fine. Holds in **any** permutation
of ℕ; the ω-hypothesis enters through Lemma 16.1's own proof. Correct.

(b) If `C` were finite, every `u > max C` is open, so an edge `u → u+d` exists with
`u+d > max C`; iterate for an infinite chain, ≺-descending by Thm 16(a) — contradiction with
order type ω. Correct (4-AP-freeness is stated).

(c) Immediate from (a). Correct.

## 5. Prop R18.5 — **BROKEN as stated**

Claim in the summary: *"A forcing chain never repeats a scale: u open at d ⟹ u+d not open at d.
Machine-verified on all 195 154 4-AP-free boards N ≤ 9 (0 violations)."*

The displayed implication is correct and trivial (if `u+d` were open at `d` we would need
`pos(u) < pos(u+d)`, contradicting Thm 16(a)). But it only forbids **consecutive** edges from
sharing a scale. The headline "a forcing chain never repeats a scale" is a strictly stronger,
**false** statement, and the machine check does not test it — `measure.py`'s own docstring and
output label M2 correctly as *"no two **consecutive** forcing edges share a scale"*; the summary
over-claims relative to its own code.

**Counterexample** (found by SAT, verified with `apcheck.has_monotone_kap_pos` and
`forcing_tools.open_scales` / `open_scales_brute` / `verify_theorem16`):

```
perm (N=40, monotone-4-AP-free):
[31,35,33,27,37,36,38,29,40,39,11,14,19,15,13,21,20,30,17,25,
 16,23,34,22,32,18,26,24,28,8,9,12,10,2,1,4,5,7,6,3]

forcing chain   6 --d=1--> 7 --d=3--> 10 --d=1--> 11
open scales:    6:[1,2]   7:[3]   10:[1]   11:[]
positions:      pos(6)=39 > pos(7)=38 > pos(10)=33 > pos(11)=11   (strictly ≺-descending, as required)
```

Scale `d = 1` is used twice on one chain. Exhaustive search over all 4-AP-free boards with N ≤ 9
finds none — the pattern needs N ≥ ~11, which is why the author's N ≤ 9 sweep saw 0.

**Repair:** restate as "consecutive forcing edges have distinct scales". No bound on chain length
follows, and none was drawn, so nothing downstream breaks.

## 6. Thm R18.6 (BLOCK DECOMPOSITION) — SOUND

Re-derived from the statement alone. Both orientations handled (checklist item 1):

* Decreasing: `pos(x+3d) < pos(x)` with `x+3d > x` forces `blk(x+3d) ≤ blk(x)`, while
  `x+3d > x` forces `blk(x+3d) ≥ blk(x)`; `blk` is weakly increasing along the AP, so all four
  terms share one block. Only shape `[4]` can carry a decreasing 4-AP. Correct.
* Increasing: cross-block comparisons are automatic, so the increasing 4-AP exists iff every
  maximal same-block run is positionally increasing. Negating per composition gives exactly the
  eight rows; `[1+1+1+1]` has no same-block run and is therefore unconditional. Correct.

All eight compositions of 4 are enumerated. `blocks.constraints()`'s classification by the equality
pattern `(b₀=b₁, b₁=b₂, b₂=b₃)` coincides with the maximal-run decomposition precisely because
`blk` is weakly increasing. Loop bounds `d ≤ (N−1)/3`, `x ≤ N−3d` are correct.

**Independent cross-validation** (my own implementation of the *table*, not importing `blocks.py`):
4000 random `(cuts, block-orders)` instances, agreement in both directions with
`apcheck.has_monotone_kap_pos` **and** with `blocks.check_orders` — 0 mismatches (3785 with a
4-AP, 215 without, so both directions are exercised).

## 7. Cor R18.6.1 (scale confinement) — two sub-claims BROKEN, headline SOUND

**(i) `r ≥ 3 ⇒ no [1+1+1+1]`: SOUND.** With `k = blk(x+d)`, `l = blk(x+3d) ≥ k+2`:
`3c_{k+1} ≤ c_{k+2} ≤ c_l ≤ x+3d < 3(x+d) < 3c_{k+1}`. Verified: 0 instances at cuts `3^j` up to 900,
and 0 at the non-geometric ratio-≥3 cuts `(1,4,100,300,900,2700)` up to 2600.

**(ii) `r ≥ 2 ⇒ no [2+1+1]`: BROKEN.** The displayed algebra
`x+3d < 3c_{j+1} − 2c_j = (3r−2)c_j` silently substitutes `c_{j+1} = r c_j`, i.e. assumes *exact*
geometric cuts, while the hypothesis is `c_{j+1} ≥ r c_j`.

Counterexample: cuts `(1,10,20,40,80,…)` satisfy `c_{j+1} ≥ 2c_j`; take `x = 2, d = 6`:
`(2, 8, 14, 20)` has blocks `(0,0,1,2)` — shape `[2+1+1]`. Five such instances up to N = 300
(also `(3,6)`, `(1,7)`, `(2,7)`, …).

Correct statements: from `r c_{j+1} ≤ c_{j+2} ≤ x+3d < 3c_{j+1} − 2c_j < 3c_{j+1}` one gets `r < 3`,
so `[2+1+1]` is impossible whenever `r ≥ 3`; and for *exact* geometric cuts `c_j = r^j` it is
impossible already for `r ≥ 2` (verified: 0 instances for `r = 2,3,4,5` up to `3r⁵`).

**(iii) adjacency.** `[2+2]` at `r ≥ 3` is genuinely adjacent (`k ≥ j+2` would give
`c_k ≥ 3c_{j+1} > x+3d`); verified 0 non-adjacent `[2+2]` at cuts `3^j` up to 900. **SOUND.**
`[1+1+2]` adjacency is **BROKEN**: at cuts `3^j`, `(x,d) = (1,13)` gives `(1,14,27,40)` with blocks
`(0,2,3,3)` — `j = 0`, `k = 2`. 3306 such instances up to 900. (`[1+2+1]` is likewise non-adjacent,
5687 instances, e.g. `(1,10,19,28)` → blocks `(0,2,2,3)`.) **Harmless:** `[1+1+2]` and `[1+2+1]` are
*intra-block unit* demands (on `B_l` resp. `B_k`) and never link two blocks, so the "for `r ≥ 3` the
only inter-block coupling is the disjunctive `[2+2]` between consecutive blocks" conclusion survives
intact. Only the `l = k+1` half of the `[1+1+2]` sentence is true.

**(iv) "an isolated block being UNSAT kills the whole architecture": SOUND**, but it is a plain
constraint-dropping relaxation and holds for **every** cut sequence — the chain structure is not
needed for it. Likewise `windowsat.py`'s window relaxation is correct (window membership of the two
extreme AP terms implies membership of the interior, since windows are intervals).

**Impact on the route's results: none.** `blocks.constraints()` and `triesat.collect()` enumerate all
eight shapes unconditionally. The only place (ii) is leaned on is `blockalone.py`'s claim that the
isolated-block constraint set is *complete* at `N = 2c_{j+1}+2`; that is true for exact geometric
cuts (with `[2+1+1]` absent, the binding bound is `[1+2+1]`'s `x+3d < 2c_{j+1} − c_j`) but would be
false for a general ratio-≥2 sequence. And completeness only matters for reading SAT verdicts —
every UNSAT verdict is valid regardless, since a smaller `N` only drops constraints.

## 8. Lemma R18.7 (binary trie comparator) — SOUND

`d = 2^v d'`, `d'` odd ⇒ adding `d` leaves bits `< v` untouched and flips bit `v`, so `x`/`x+d` and
`x+d`/`x+2d` both first differ at level `v` with the same residue `r = x mod 2^v`, and
`bit_v` reads `a, 1−a, a`. Hence exactly one of "`x` before `x+d`", "`x+d` before `x+2d`" holds,
killing both the increasing and the decreasing triple. Correct.

Independently verified: 2000 random (flip-vector, subset) pairs, **0** monotone 3-APs; and
`triesat.trie_key`'s sort key provably realises the stated comparator (checked on all ordered pairs
of `[1..64)` for 200 random flip vectors). Bit identities checked on 20000 random `(x,d)`.

**Caveat the route gets right:** the trie order on all of ℕ need **not** have order type ω (e.g.
`f ≡ 1` puts every odd number before every even one, so 2 has infinitely many predecessors). It is
used only inside finite blocks, and order type ω comes from the layered wrapper. Stated correctly
in `triesat.py`.

## 9. Thm R18.8 (collapse to unit/2-SAT) — SOUND derivation, one testing gap

All four translations re-derived and confirmed:
`[1+1+2] ⇒ f^{(l)}_{v,r} = 1−a`; `[1+2+1] ⇒ f^{(k)}_{v,r} = a`; `[2+1+1] ⇒ f^{(j)}_{v,r} = 1−a`;
`[2+2] ⇒ ¬(f^{(j)}_{v,r} = a ∧ f^{(k)}_{v,r} = a)`. `[4]/[3+1]/[1+3]` are automatic by R18.7. Every
constrained node `(block, v, r)` is genuinely reached by two values of that block, so no spurious
constraints are generated. The parenthetical "(unit; vacuous for ratio ≥ 2)" inherits the broken
Cor R18.6.1(ii) but is harmless under the theorem's own `r ≥ 3` hypothesis.

**Testing gap.** `triesat._selftest` asserts only `pred_ok ⇒ actual_ok`; the direction actually used
for the death results (`INFEASIBLE ⇒ no trie construction exists`) is never tested. I tested it:
ratio 3, N = 200, 400 random flip vectors — **0/400** produced a 4-AP-free permutation, as predicted.

**"Dead for every ratio, one level deep, explicitly."** The filed evidence is a finite scan
(ratios 3–32 at N = 3000), and it even reports **ratio 64 as FEASIBLE at N = 3000** — an artefact of
`N` being too small for block 1 = `[64, 4096)` to be complete, not a counterexample. A general proof
is available and should replace the scan:

> For every `r ≥ 3` take `x ∈ {1,2}` and the least **odd** `d` with `x+3d ≥ r²`; then
> `x < r ≤ x+d`, `x+2d < r²`, so `(x, x+d, x+2d, x+3d)` has shape `[1+2+1]` with the pair
> `x+d, x+2d` in block `B₁ = [r, r²)`. Since `d` is odd, `v = v₂(d) = 0`, `r_res = x mod 1 = 0`,
> `a = x mod 2`. The two APs demand `f^{(1)}_{0,0} = 1` (from `x=1`) and `f^{(1)}_{0,0} = 0`
> (from `x=2`). Contradiction.

Witnesses confirmed for **every** `r ∈ [3, 399]`: `r=3 → (1,4,7,10) / (2,5,8,11)`;
`r=4 → (1,6,11,16) / (2,7,12,17)`; `r=64 → (1,1366,2731,4096) / (2,1367,2732,4097)`. Hand-check for
`r=3`: 4 and 7 split at level 0 (residue 0), so "7 before 4" ⟺ `f₀,₀ = 1`; 5 and 8 also split at
level 0, so "8 before 5" ⟺ `f₀,₀ = 0`. Both are required; no assignment works.

Note this only prunes the **NO-side design space** (trie-comparator layered permutations). It is not
a YES result and is not presented as one.

## 10. "Geometric cuts r=3 and r=4 are dead" — SOUND modulo solver correctness; **state the scope**

**Logic.** The intra-block constraints for one block `B_j` are *necessary* conditions on the internal
order of `B_j` in any 4-AP-free layered permutation of ℕ with those cuts (Thm R18.6, audited SOUND).
Dropping `[2+2]` and all other blocks is a relaxation. Hence isolated-block UNSAT ⇒ **no**
monotone-4-AP-free layered permutation of ℕ with those cuts exists. This is a legitimate
finite ⇒ infinite step (checklist item 9): the finite computation certifies a necessary condition of
the infinite object, not the infinite object itself.

**Independent replication.** I re-derived the intra-block necessary constraints directly from the
definition of a monotone 4-AP (no import of `blocks.py`) and reproduced the author's counts exactly:

```
r=3, B_3=[27..80]  : inv=354  noinc3=364  no4=459   -> UNSAT  (cadical, glucose, minisat, CP-SAT)
r=4, B_3=[64..255] : inv=2763 noinc3=4608 no4=6048  -> UNSAT  (cadical, glucose, minisat)
```

CP-SAT with an integer-position + AllDifferent model (a genuinely different encoding) gives
`r=3 block 3: UNSAT (11.4 s)`. Together with the author's own `blockalone.py` (CaDiCaL) and
`scan_blocks.py`/`blockalone_cp.py` (CP-SAT), that is **four solver families across two independent
constraint derivations**. UNSAT confirmed independently (checklist item 10).

**Not an artefact of one constraint family.** Localisation on `r=3`, `B_3`:
`inv` alone SAT, `inv+noinc3` SAT, `inv+no4` SAT, `noinc3+no4` SAT. All three families are needed —
the certificate is a genuine interaction, not a single-family collapse.

**SCOPE, which the summary does not state.** "Dead" means *dead as an architecture over ℕ*, not
*dead at every N*. `witness_geom3_N80.json` is a genuine monotone-4-AP-free layered permutation of
`[1..80]` with cuts `(1,3,9,27,81)` — I re-verified it with `apcheck` (0 cross-block forcing edges,
`max|Cl| = 47`). The constraints that kill `B_3` come from APs whose top term exceeds 80. I located
the exact thresholds with my own encoding, two solvers agreeing:

```
ratio 3 layered:  N=86 SAT (cadical, glucose)  |  N=87 UNSAT (cadical, glucose)
ratio 4 layered:  N=170 SAT (cadical, glucose) |  N=171 UNSAT (cadical, glucose)
```

Any statement of the theorems must read: *there is no monotone-4-AP-free layered permutation of
`[1..N]` with cuts `c_j = 3^j` for `N ≥ 87` (resp. `c_j = 4^j` for `N ≥ 171`); a fortiori none of ℕ.*
Also: this is the **specific** cut sequence `c_j = r^j`, not every cut sequence of ratio `r`
(e.g. `(1,4,100,300,900,2700)` has ratio ≥ 3 and is untouched by these certificates).

## 11. Side finding — R18's C = 2 data contradicts CORE.md Remark 17

`log_c2thresh.txt` reports plain (no monotone 4-AP, both orientations) under `pos(v) ≤ 2v`:
SAT at N = 68, 70, 72; UNSAT at N = 74, 76, 78, 80 with CaDiCaL **and** Glucose agreeing.
CORE.md Remark 17 tabulates `N*(C)` as *"the minimal N with no such permutation of [1..N]"* and
lists `N*(2.0) = 90`. Since SAT is inherited downward (delete the largest value; all other positions
weakly decrease), UNSAT at 74 makes 90 non-minimal.

I re-ran this from scratch with my own eager order encoding (`⌊2v⌋ = 2v`, so the ⌈⌉/⌊⌋ convention
difference is irrelevant at C = 2):

```
INDEPENDENT eager k=4 C=2 N=72 : SAT   (cadical 101.5 s; glucose 130.5 s)
INDEPENDENT eager k=4 C=2 N=74 : UNSAT (cadical 251.0 s; glucose 159.3 s)
```

R18 is right. The source of CORE.md's number is `experiments/profile_cegar2.out`, which only ever
claimed *"EXTINCTION at C=2.0, N=90 (inherited for all larger N)"*, and
`experiments/verify_c2_n90.out`, which verified UNSAT at N = 85 and 90 only. **CORE.md's re-labelling
of that as the minimal N is the error**, and the true threshold is N* ∈ {73, 74}. Related convention
hazard: `experiments/plain_thresholds.py` and `sat_height.py` use `pos(v) ≤ ⌈Cv⌉`, CORE.md Remark 17
says `⌊Cv⌋`; the two coincide only at integer C, which is why `plain_thresholds.out`'s
`C=1.25 → 14`, `C=1.5 → 22` look incompatible with CORE's `4, 15`. This should be reconciled in the
lab record. R18's summary does not flag any of this.

## 12. Process notes

* No `REPORT.md`/`STATUS.md` in the route directory; the deliverable exists only as module
  docstrings plus the returned summary, which is truncated mid-sentence. Statements audited here
  are those in the summary.
* `log_geom5_N124.txt` is empty; `log_cp_r5b3.txt` is UNKNOWN (2000 s timeout) — the ratio-5
  architecture is **not** decided, and the summary correctly does not claim it is.
* `r5_block2_order.json` is a bare list (no `cuts` key), so `measure.py`'s `M3` silently skips it.
  Cosmetic.

## 13. Items checked and found clean

* Both orientations handled everywhere they are needed (Thm R18.6's `[4]` row, `no4` clauses in
  `verify_unsat.py`/`blockalone.py`/`blocksat.py`/my replications).
* Positions strictly increasing, `d ≥ 1`, no value reused, no reindexing: `constraints()` loops
  `d ∈ [1, (N−1)/3]`, `x ∈ [1, N−3d]`; `assemble()` asserts the block orders tile `[1..N]`;
  all decoded permutations are re-checked against `apcheck`.
* Boundary cases: `u−2d ≥ 1` enforced in `open_scales`; `bound ≥ N ⇒ skip` in the profile
  cardinality constraints is correct; `L = max(1, N.bit_length())` suffices to separate any two
  values of `[1..N]` in `trie_key`.
* Named theorems: only König (finitely-branching tree; branching bound `d ≤ (u−1)/2` verified) and
  the ω-order Lemma 1. Hypotheses hold. No Szemerédi/vdW/Ramsey use, so no uniformity to track.
* Circularity: HFIN(K) is a genuinely finite statement about boards of `[1..N]`; it does not restate
  196. It is also false, so nothing is smuggled in.
* No drift to problems 194/195/197; ℕ starts at 1 throughout; values vs positions never swapped
  (`pos[v]` indexing is consistent in `forcing_tools.positions` and everywhere downstream).
