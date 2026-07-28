# AUDIT.md — adversarial audit of `attempts/consolidated/STATUS.md`

Auditor: independent adversarial pass, 2026-07-28. Target: `/home/user/erdos/attempts/consolidated/STATUS.md`
(the consolidation of routes R2, R4, R8, R9), against `/home/user/erdos/PROBLEM.md`.

Method: every hand proof re-derived line by line; every re-runnable number recomputed with
**code written here from the mathematical definition**, never by re-running the routes' or the
consolidator's binaries. Auditor code lives in
`/tmp/claude-0/-home-user-erdos/16d68b37-9cd8-5fc8-ae52-36a43a9b9dde/scratchpad/audit/`
(`classA.c`, `classA2.c`, `classAw.c`, `classS.py`, `constrA.py`, `verify_w.py`, `rand_probe.py`).
All AP checkers cross-validated against `/home/user/erdos/experiments/apcheck.py`
(`has_monotone_kap_brute`, the literal O(C(n,k)) definition scan).

---

## VERDICT TABLE

| # | Claim (as stated in STATUS.md) | Verdict |
|---|---|---|
| 1 | R2 Construction A: L0–L7, Theorem (no monotone 5-AP), Proposition (S1/S2) | **SOUND** |
| 2 | R2 machine numbers (5-AP-free & desc-3-AP-free to 65535, census 1,304,268, S1/S2 split, max/min pos/v, 59.24 %) | **SOUND** — all reproduced exactly |
| 3 | R2 Mod 2 / Mod 3 / Mod 4 hand arguments | **SOUND** |
| 4 | Displacement theorem: `N*₅(C) = +∞` for every `C ≥ 4` | **SOUND** |
| 5 | "Length-5 avoidance costs **exactly** a bounded factor-4 linear corridor" | **REPAIRABLE GAP** (overclaim; only `C*₅ ∈ (4/3, 4]` is established) |
| 6 | R4 class-S theorem: no 4-AP-free injective `a(1..18)` with `a(i) ≤ ⌊4i/3⌋`; hence every 4-AP-free permutation of ℕ has `i ≤ 18` with `a(i) > ⌊4i/3⌋` (⇔ some `v` with `pos(v) < 3v/4`) | **SOUND** — reproduced 3 ways |
| 7 | "Class S needs **no compactness**, **unlike value restrictions which need Lemma 6**"; "the only family in the whole project that yields infinite theorems without a compactness step" | **BROKEN** |
| 8 | "Class S is **immune to Remark 17(a)**'s ∀φ objection"; next-step #2's rationale | **BROKEN** — counterexample `a(i) = 2^i` |
| 9 | R4 class-A thresholds (1→4, 3/2→15, 7/4→31, 15/8→37) and all stored witnesses | **SOUND** — reproduced |
| 10 | R4 survivor rigidity (6472 distinct, prefix `1,7,2,4,3,9,8,5`, 14 constant positions) | **SOUND** — reproduced exactly |
| 11 | R8 T1 (edge-anchored increasing 3-AP with `d > a(1)`) | **SOUND** |
| 12 | R8 T2 (split ℤ-extensions contain an increasing 4-AP) | **SOUND** |
| 13 | R8 T3 (no ternary annulus macro of ℤ avoids 3-APs) | **SOUND** |
| 14 | R8 Theorem W (no odd-`d` monotone 4-AP) | **SOUND** — verified to 13 334 positions |
| 15 | R8 L3, L4 (= CORE Cor. 26), L5, L6 | **SOUND** |
| 16 | R9 census 1…949 812 334, dead ends first at N=12 = 515 296 | **SOUND** — reproduced bit-for-bit |
| 17 | R9 `N*(C)` staircase + node totals + per-level dead counts; k=3 row; k=5 points (13, 35) | **SOUND** — reproduced |
| 18 | Interval theorem (CORE Lemma 8) verified over all avoiders of [1..7], [1..8] | **SOUND** — reproduced, 0 exceptions |
| 19 | `ρ(85) > 2` listed under "PROVED / every one reproduced here" and in the "Exact certified staircase (all reproduced in this directory)" | **REPAIRABLE GAP** — mislabelled; rests on un-re-run SAT |
| 20 | "k=5 at C=3/2: **> 90**" (§5 table) | **REPAIRABLE GAP** — unsourced; nothing in the repo supports 90 |
| 21 | "an exponential fit … cannot detect divergence … **in the one case where C\* is known** it gives no warning" | **REPAIRABLE GAP** — `C*₅` is not known; core point survives but is partly tautological |
| 22 | The five documentation discrepancies (§6.1–§6.5) | **SOUND** (all five confirmed; see §7 for one nuance) |
| 23 | "no computational error found in any of the four routes" | **SOUND** — I found none either |

Nothing in the report is a claimed proof of 196 (YES or NO), and no lemma audited here restates 196
in disguise. Checklist item 7 (circularity): clean.

---

## 1. SOUND — R2 / Construction A (items 1–4)

### 1.1 Hand proofs (`attempts/route-R2/PROOFS.md`), re-derived

* **L0.** `B_m = [4^m, 4^{m+1})`, `|B_m| = 3·4^m`; block `m` starts at position
  `1 + Σ_{j<m} 3·4^j = 4^m` and ends at `4^{m+1}−1`. So `v` and `pos(v)` share the window
  `[4^m, 4^{m+1})`, giving `v/4 < pos(v) < 4v`. Bijection and order type ω are structural.
  **SOUND.** (Both halves of the strict inequality re-derived: `pos(v) < 4^{m+1} ≤ 4v` from
  `v ≥ 4^m`; `pos(v) ≥ 4^m > v/4` from `v < 4^{m+1}`.)
* **L1.** With `l = v₂(e)`: bits `<l` of `u, u+e, u+2e` agree; `bit_l(u) = bit_l(u+2e) = 1−bit_l(u+e)`.
  Hence in vdC order (LSB-first lexicographic) the comparisons `u : u+e` and `u+2e : u+e` are both
  decided at bit `l` in the same direction, so `u+e` is extremal, never positionally middle. Reversal
  preserves extremality. Both orientations covered. **SOUND.**
* **L2, L3, L4.** Positions are block-major; along a descending value chain at increasing positions the
  block index both weakly increases (positions) and weakly decreases (values), so all terms share a
  block, where L1 kills length 3. Hence **no descending monotone 3-AP anywhere** — machine-confirmed to
  N = 65 535. **SOUND.**
* **L5.** `t_{i+1} < 2t_i` for `i ≥ 1` ⇔ `(1−i)d < x`, true since `x ≥ 1`. (It is *false* for `i = 0`,
  and the lemma correctly restricts to `i ≥ 1`.) **SOUND.**
* **L6.** With `t_i = x+id`: `4t_1 − 3x = 4(x+d) − 3x = x+4d = t_4`, so `t_4 < 4t_1`. Three distinct
  blocks among `t_1..t_4` would give `t_4 ≥ 4^{b+2} > 4t_1` where `b = block(t_1)`. **SOUND** (the
  indexing that made `t_4 = 4t_1 − 3x` look wrong on first reading is correct because `t_1 = x+d`).
* **L7.** `u ≺ u+d` in `π_m` ⟺ `bit_l(u) = m mod 2`. **SOUND.**
* **Theorem (no monotone 5-AP).** Descending by L3. Ascending: ≤2 terms per block (L1+L4), ≤2 blocks
  for `t_1..t_4` (L6) forces `{t_1,t_2} ⊂ B_m`, `{t_3,t_4} ⊂ B_{m+1}`; L7 then demands
  `bit_l(t_1) = m mod 2` and `bit_l(t_3) = (m+1) mod 2`, contradicted by `t_3 − t_1 = 2d ≡ 0 (mod 2^{l+1})`.
  **SOUND.**
* **Proposition (S1/S2).** Re-derived including the two cases STATUS's sketch compresses: `block(t_0) = m−1`
  in shape S1 dies by the same `2d` parity argument, and `block(t_0) = m` in S2 would put three terms in
  one block. Converse holds by L2 + L7. **SOUND.**

### 1.2 Machine claims — all reproduced independently

`constrA.py` rebuilds the construction from the prose (LSB-first bit-tuple sort key, reversed for odd `m`),
and scans all `(x,d)` with a numpy position scan cross-validated against `apcheck.has_monotone_kap_brute`
(300 random permutations × k ∈ {3,4,5}, 0 mismatches):

```
first 15 : 2,1,3,15,7,11,13,5,9,14,6,10,12,4,8                                  [matches]
N=  255  bij ✓ window ✓ 5AP inc=0 dec=0  desc-3AP=0  max pos/v=3.968750 (v=64)   min=0.250980
N= 1023  bij ✓ window ✓ 5AP inc=0 dec=0  desc-3AP=0  max=3.968750               min=0.250980
N= 4095  bij ✓ window ✓ 5AP inc=0 dec=0  desc-3AP=0  max=3.998047 (v=1024)      min=0.250061
N=16383  bij ✓ window ✓ 5AP inc=0 dec=0  desc-3AP=0  max=3.998047               min=0.250061
         4-AP census: inc=1304268  dec=0   first (smallest-d) = (x,d)=(2,5) i.e. (2,7,12,17)
N=65535  bij ✓ window ✓ 5AP inc=0 dec=0  desc-3AP=0  max=3.999878 (v=16384)     min=0.250004 (v=65535)
```

S1/S2 predicate implemented from the Proposition's *arithmetic* statement and compared **AP-by-AP**
against the position census at N = 16383: `S1 = 979 436`, `S2 = 324 832`, overlap `0`,
union `= 1 304 268 =` census, `0` missing, `0` spurious. `frac(pos(v) ≤ (9/8)v) = 0.5924`.
Every published R2 number reproduces.

*Why the extrema are where they are* (I re-derived this rather than trusting the measurement): for odd `m`
the vdC-first element of `B_m` is `2^{2m+1}` and the vdC-second is `4^m`, so under the reversal
`pos(4^m) = 4^{m+1} − 2`, giving `pos(v)/v = 4 − 2·4^{−m} ↑ 4`; and `pos(4^{m+1}−1) = 4^m`, giving
`↓ 1/4`. So **`sup pos(v)/v = 4`, not attained; `liminf = 1/4`**. STATUS's "limsup 4, liminf 1/4" is exact.

### 1.3 The displacement theorem (item 4) — SOUND

> `N*₅(C) = +∞` for every `C ≥ 4`.

Restriction of Construction A to values `[1..N]` is a permutation of `[1..N]`, is 5-AP-free (restrictions
of AP-free sequences are AP-free), and satisfies `pos_{σ_N}(v) ≤ pos_A(v) < 4v ≤ ⌊Cv⌋` for `C ≥ 4`
(positions are integers, so `pos ≤ Cv ⇔ pos ≤ ⌊Cv⌋`). No compactness, no limit step. **SOUND.**

---

## 2. REPAIRABLE GAP — "length 5 needs **exactly** a factor-4 corridor" (item 5)

STATUS's verdict §2 and §5 say *"Length-5 avoidance costs exactly a bounded factor-4 linear corridor"*
and *"Length 5 needs exactly a factor-4 linear corridor."*

**Gap.** What is established is
(a) `C = 4` suffices (Construction A), and
(b) `C = 5/4` and `C = 4/3` do not (`N*₅ = 13, 35`, both reproduced here).
Nothing establishes that 4 is *minimal*. The critical constant is only pinned to `C*₅ ∈ (4/3, 4]`.
The `4` in Construction A is exactly what **Lemma 6's proof technique** needs (three distinct blocks of
ratio `r` are excluded only when `4·r^{j+1} ≤ r^{j+2}`, i.e. `r ≥ 4`) — a property of the proof, not of
the problem.

**Adversarial probe (does not close the gap, but is the natural attack).** I built the same
block/vdC/alternating-reversal construction at base 2 and base 3:

```
base 2, N=255 : monotone 5-APs = 424 (first x=1,d=2)   max pos/v = 1.9922
base 3, N=6560: monotone 5-APs = 12395 (first x=5,d=19) max pos/v = 2.9374
base 4, N=16383: monotone 5-APs = 0                     max pos/v = 3.9980
```

so the obvious cheaper constructions fail; but that is evidence, not proof.

**Repair (one line).** Replace "exactly a factor-4 linear corridor" with
"*a factor-4 linear corridor suffices, and a factor-4/3 corridor does not; the critical constant is only
known to lie in (4/3, 4]*". The downstream sentence "the certified k=4 extinction range covers half of the
C-range in which the known k=5 solution lives" then needs the same hedge (the k=5 solution is only known
to live *at* C = 4, not to *need* it).

---

## 3. SOUND — R4 class-S theorem (item 6)

I re-enumerated class S from scratch (`classS.py`), with the incremental legality test asserted against
`apcheck.has_monotone_kap_general` at every node, **and** with a wholly independent pure brute-force
level-by-level extension driven only by the trusted checker. Both agree with STATUS exactly:

```
C=1   : levels 1,1,1,0                                            extinct i=4    (4 nodes incl. root)
C=5/4 : levels 1,1,1,1,1,0                                        extinct i=6    (6 nodes)
C=4/3 : levels 1,1,2,3,5,9,15,23,35,28,20,24,12,14,19,13,2,0      extinct i=18   (227 nodes)
```

The restatement "*equivalently some value `v` with `pos(v) < (3/4)v`*" is correct in **both** directions:
`⌊4i/3⌋ ≥ (4i−2)/3`, so `a(i) > ⌊4i/3⌋ ⇒ v = a(i) ≥ (4i+1)/3 ⇒ i ≤ (3v−1)/4 < 3v/4`; and conversely
`i < 3v/4 ⇒ v > 4i/3 ≥ ⌊4i/3⌋`.

Checklist audit of the derivation: positions strictly increasing ✓, `d ≥ 1` ✓, no value reused ✓,
no reindexing (a **position prefix** keeps its original positions — unlike a value restriction) ✓,
`v−(k−1)d ≥ 1` boundary handled ✓, both orientations checked ✓, no named theorem invoked ✓.
The theorem is a valid necessary condition on any 196-counterexample. **SOUND.**

---

## 4. BROKEN — "class S is the only compactness-free family; value restrictions need Lemma 6" (item 7)

STATUS, §2 table and verdict bullet:

> | **A** | pos(v) ≤ Cv | **yes, via CORE Lemma 6** (König over the value-restriction tree) |
> | **S** | a(i) ≤ ⌊Ci⌋ | **yes, directly — no compactness needed.** |
>
> "*Class S is the only family in the whole project that yields infinite theorems without a compactness step.*"
> "*This needs no compactness (position prefixes inherit the bound directly, unlike value restrictions which need Lemma 6).*"

**This is false.** Value restrictions inherit the class-A bound *just as directly*. If `a` is a
monotone-4-AP-free permutation of ℕ with `pos_a(v) ≤ ⌊Cv⌋` for all `v ≤ N`, then its restriction `σ_N`
satisfies

```
pos_{σ_N}(v) = #{ w ≤ N : pos_a(w) ≤ pos_a(v) } ≤ pos_a(v) ≤ ⌊Cv⌋ ,
```

so class-A extinction at level `N` immediately gives the infinite theorem

> every monotone-4-AP-free permutation of ℕ has some `v ≤ N` with `pos(v) > ⌊Cv⌋`,

with **no König and no compactness**. Concretely, the certified `N*(15/8) = 37` yields
"*every 4-AP-free permutation of ℕ has some `v ≤ 37` with `pos(v) > ⌊15v/8⌋`*", exactly parallel in
strength and directness to the class-S statement.

CORE's own text says so: Lemma 6's **(⇒)** half *is* this restriction computation, and CORE Lemmas 7 and
7b use it explicitly ("*since `pos_{σ_N}(v) ≤ pos_a(v)` for all `N` (as in Lemma 6(⇒))*"). König is needed
only for the **converse** (survival at every `N` ⇒ an infinite avoider) — the direction STATUS is *not*
using when it converts extinction into a theorem.

**Repair.** Delete the contrast. Correct table entry for A: "yes, directly, by restriction (Lemma 6(⇒));
König is needed only for the converse direction". Correct the verdict bullet to "class S is a *position-side*
analogue of the value-side extinction theorems, cheaper to certify". The cost comparison STATUS gives
(227 nodes at `C = 4/3` vs `~10⁶` at `C = 7/4`) is real and survives; the compactness contrast does not.

---

## 5. BROKEN — "class S is immune to Remark 17(a)" (item 8)

STATUS, §2 and ranked next-step #2:

> "*So class S is a pure YES-side constraint generator — which is exactly why it is worth mining: it is
> immune to Remark 17(a)'s '∀φ' objection.*"
> "*Mine the class-S (position-side) ladder … The family is immune to Remark 17(a) because S-survival is
> not equivalent to 196-NO.*"

**Counterexample.** CORE Remark 17(a) objects that extinction for every *linear* profile does not give YES,
because 196-NO needs only *some* profile. On the position side the same objection applies verbatim (a
counterexample may have `a(i)` superlinear) — and it applies **fatally**, not merely as a gap:

> Take `ψ(i) = 2^i` and `a(i) = 2^i`. Then `a` is injective, `a(i) ≤ ψ(i)`, and the value set
> `{2, 4, 8, 16, …}` contains no 3-term AP at all (`2^p + 2^r = 2^{q+1}` with `p<q<r` is impossible),
> so `a(1..N)` is a class-S object for **every** `N`.

Verified with the trusted brute-force checker (`apcheck.has_monotone_kap_brute`, k = 3 and 4) for
`N ≤ 16`. Hence the position-side statement "*for every profile `ψ`, class S goes extinct at some `N`*"
is **FALSE unconditionally**, so no amount of class-S mining can ever be lifted to a proof of 196-YES.

By contrast the value-side statement is *equivalent* to 196-YES (CORE Lemma 6 is a biconditional) —
precisely because each level of the value-side tree consists of **permutations of `[1..N]`**, i.e.
surjectivity is enforced at every finite level. Dropping surjectivity is exactly what class S does, and
`n ↦ 2^n` is exactly the failure mode PROBLEM.md's own checklist warns about
("*A YES-side argument that never uses surjectivity is WRONG (injections like n → 2^n avoid even 3-APs)*").

STATUS notices the one-directionality ("S-survival does not imply 196-NO") and then draws the opposite
conclusion from it: one-directionality makes the ∀ψ target **strictly stronger than YES**, hence
(as just shown) false, not "immune".

**Repair.** (i) Strike "immune to Remark 17(a)" and the "pure YES-side constraint generator … which is why
it is worth mining" rationale. (ii) Replace with the correct scoping: *each* class-S extinction certificate
is a valid necessary condition on a counterexample (item 6 above, SOUND), but the class-S ladder has a hard
ceiling — the `∀ψ` version is refuted by `a(i) = 2^i` — so it cannot be a route to YES, whereas the
value-side ladder at least has the logically correct target. (iii) Next-step #2 should be demoted
accordingly: it produces quotable constraints, not progress toward a decision.

---

## 6. SOUND — R8 (items 11–15)

* **T1.** If `π(2v−c) < π(v)` for all `v ≥ 2c+1`, the orbit of `g(v) = 2v−c` (which maps `[2c+1,∞)` into
  itself since `g(v) ≥ 3c+2 ≥ 2c+1` for `c ≥ 1`) gives an infinite strictly decreasing sequence of ℕ-positions.
  `π(c) = 1 < π(v)` since `v ≥ 2c+1 > c`; `d = v−c ≥ c+1 ≥ 2`. **SOUND.** Both hypotheses used are
  genuinely one-sided (first position; well-foundedness), as R8 says.
* **T2.** `g^k(v) = f` forces `v = c + (f−c)/2^k`, and integrality bounds `k`; `f ≤ c` is impossible since
  `g^k(v) ≥ v ≥ 2c+1`. So finitely many bad `v`. Descent inside the right part gives `(c, v, 2v−c)` with
  `d ≥ c+1`, whence `x = c−d = 2c−v ≤ −1` lies in `ℤ_{≤0}`, i.e. at a position `< s`. **SOUND.**
  (Positions in the right part are bounded below by `s`, so the descent argument is legitimate.)
* **T3.** All four witnesses re-derived arithmetically: `(1,122,243)` step 121, `(−239,2,243)` step 241,
  `(241,485,729)` step 244, `(1,365,729)` step 364; ternary annulus indices `(0,4,5)`, `(4,0,5)`,
  `(4,5,6)`, `(0,5,6)`; middle-value annuli `4, 0, 5, 5`. The "middle annulus must be σ-extreme" step is
  correct (three distinct blocks ⇒ monotone ⟺ σ-middle). Both branches `σ₀<σ₅<σ₄` and `σ₄<σ₅<σ₀` end in
  `σ₅<σ₆ ∧ σ₅>σ₆`. Scaling by `3^j` shifts all indices. **SOUND.**
* **Theorem W.** Position formulas verified symbolically and numerically (`pos(o) = (3o+1)/2`;
  `(3e−2)/4 ≤ pos(e) ≤ 3e/4`), and all four inequalities re-derived:
  `(3x+9d+2)/4`, `(3x+3d+2)/4`, `(3x+2)/4`, `(3x+6d+2)/4`, all `> 0` for `x, d ≥ 1`.
  Machine: **0** odd-`d` monotone 4-APs on prefixes of 400 / 1300 / 4000 / **13 334** positions;
  first even-`d` AP is `(1,3,5,7)`. **SOUND.**
* **L3 / L4 / L5 / L6.** L4 (= CORE Corollary 26): the P-values of a counterexample sit at an infinite
  subset of ℕ (order type ω), and the affine relabelling `ℕ → P` is an order-isomorphism onto the value
  set, so the relabelled object is again a bijection ℕ→ℕ with no monotone 4-AP. **SOUND.**
* **Domain hygiene.** T2/T3 are statements about ℤ (problem 195). STATUS labels them as such and never
  uses them as 196 results — no drift (checklist item 8 clean).
* **Ladder (`d ≢ 0 mod 4`).** I reconstructed the rate schedule independently and found **0** violating
  monotone 4-APs on the permutation prefix of `[1..5332]` — i.e. substantially beyond STATUS's own 2000
  and close to R8's claimed 5864. So R8's k=2 claim is very probably true; the discrepancy (§7.5) is a
  *logging* discrepancy only, and STATUS's phrasing slightly overstates the doubt.

---

## 7. SOUND — R9 / R4 computational claims (items 9, 10, 16, 17, 18, 23)

My own DFS (`classA.c`, and an optimised `classA2.c` with identical node totals) inserts values
`1,2,3,…` in increasing order, checks the monotone-`k`-AP condition from the **raw definition** (both
orientations), and prunes with `pos(v) ≤ ⌊Cv⌋` — sound because inserting a larger value never lowers an
existing position, so every value-restriction of an in-class permutation is in class.

```
census (unbounded profile), k=4:
 N     1 2 6 22 102 564 3336 22266 168864 1307470 11066766 101361722 949812334      [exact match]
 dead  first at N=12 = 515296                                                        [exact match]
 total nodes 1 063 743 456  (= R9's 1 063 743 455 + the virtual root)

k=4 class-A staircase   N*(C) : C=1→4, 5/4→4, 4/3→10, 11/8→10, 3/2→15, 8/5→18,
                                13/8→21, 5/3→26, 7/4→31, 9/5→34                      [exact match]
 total nodes (mine = R9's + 1): 4, 4, 11, 11, 277, 2169, 3021, 126186, 1036993, 57006573
 per-level counts AND per-level dead counts diff-identical to route-R9/cert_C1.75.txt
 level-30 count at C=7/4 = 6472                                                      [exact match]

k=3 calibration  N* = 5, 10, 12, 13, 20, 29 at C = 3/2, 2, 5/2, 3, 4, 6              [exact match]
k=5              N*₅(5/4) = 13 ;  N*₅(4/3) = 35 (2 203 322 nodes)                    [exact match]
3-AP-free counts 1,2,4,10,20,48,104,282,496                                          [exact match]
```

`C = 15/8` (2.65 × 10⁹ nodes) was still running in my environment at the time of writing; it is
independently corroborated by `route-R9/cert_C1.875.txt` (EXTINCT at 37) **and** by R4's SAT log
`logs_A158_sat.txt` (SAT 36 / UNSAT 37), two unrelated engines. I have no reason to doubt it.

**Interval theorem (CORE Lemma 8).** Verified literally: over all 3 336 avoiders of `[1..7]` and all
22 266 avoiders of `[1..8]` (enumerated by brute force through `apcheck`), the set of legal insertion
ranks for the new maximum is always a contiguous interval and always equals `[Lo+1, Hi]` from the
formula — **0 exceptions**.

**Witnesses.** All 15 files in `route-R4/avoiders/` re-checked with `apcheck`: **0** entries contain a
monotone 4-AP; the largest-`N` row of each file reproduces STATUS's table exactly, with exact rational
extrema — `A_2_1` N=56 max pos/v = 2, max a(i)/i = 13; `A_3_1` N=75 max pos/v = 3, max a(i)/i = 27;
`A_5_2_ceil` N=70, 3, 10; `A_15_8` N=36, 28/15, 7/2; `C_2_1` N=49, 2, 2; `B_2_1` N=95, 6, 2;
`seq_B_3_2` N=34 (a sequence, not a permutation), 9/5, 3/2.

**Survivor rigidity.** 6472 rows, all distinct, all monotone-4-AP-free, all satisfying `pos(v) ≤ ⌊7v/4⌋`,
all beginning `1,7,2,4,3,9,8,5`; constant positions = `{1..8, 19, 26..30}`, exactly 14.

`ρ` monotone in `N` (deleting the largest value never raises a position): **SOUND**, so the staircase
really is the inverse of the `N*` table. Fits recomputed independently: `N*(C) ≈ 0.1777 e^{2.9121C}`
(log-`R² = 0.9388`), inverse `ρ(N) ≈ 0.593 + 0.343 ln N`; restricted fit `0.3452 e^{2.5344C}`;
k=5 two-point fit `4.593×10⁻⁶ e^{11.885C}`, `N*₅(4) ≈ 2.03×10¹⁵`. All match `rho_fit.out`.

---

## 8. REPAIRABLE GAPS in labelling and sourcing (items 19, 20, 21)

### 8.1 `ρ(85) > 2` is not certified (item 19)

It appears in §4 under "**PROVED** (complete enumerations; every one reproduced here level-by-level)"
and inside §5's "**Exact certified staircase (all reproduced in this directory)**". It is neither an
enumeration nor reproduced: it rests entirely on `experiments/verify_c2_n90.out`, an eager SAT encoding
that STATUS itself says (§1, §3, §4) it did not re-run, and whose encoding was not re-derived.
STATUS's own methodology paragraph ("Every number I report as MEASURED was produced by code written
here") is violated for this one entry.

*Consequences that inherit the dependency:* `N*(2) ∈ [57, 85]` (the upper end only);
"Length 4 is certified dead only up to `C = 2`"; and the quantitative half of discrepancy §6.1.
*What survives unconditionally:* `ρ(56) ≤ 2` and `ρ(75) ≤ 3` (witnesses, re-verified here), the
staircase up to `ρ(37) > 15/8`, and discrepancy §6.1 as a **documentation** inconsistency — CORE
Remark 17 tabulates `N*(2.0) = 90` as "the minimal N", while the very file it cites records UNSAT at
`N = 85`, so CORE is internally inconsistent regardless of whether the SAT is right.

**Repair.** Move `ρ(85) > 2` from PROVED to MEASURED-not-reproduced, and mark the `[57,85]` bracket
"upper end SAT-dependent".

### 8.2 "k=5 at C=3/2: > 90" is unsourced (item 20)

`k5_C1.5.out` is 0 bytes; §8 says the run was killed without completing. R9's own figure for that cell
is 68 (a beam horizon), and CORE Remark 17(b) says only "survives past N = 70". Nothing in the repository
supports 90. (My own complete DFS did not reach depth 90 in 4 minutes, and a randomized-restart probe
reached only N = 28 — both weak methods that establish nothing, but neither corroborates 90.)
**Repair:** replace with "≥ 68 (beam witness, R9) — exact value not computed".

### 8.3 "the one case where C\* is known" (item 21)

`C*₅` is **not** known; only `C*₅ ≤ 4` is established (this is exactly what §2 above says, and
`rho_fit.out` states it correctly as "`C* <= 4`"). STATUS's executive summary upgrades this to
"the one case where `C*` is known".

Also, the "lesson" is partly tautological: **any** exponential model is finite at every `C`, so it can
never predict a divergence at a finite `C*` — no data needed. And the k=5 "identical procedure" is a
two-point interpolation (`R² = 1` by construction) set against an eleven-point k=4 fit, so the parallel
is rhetorical rather than methodological.

**What survives, and it is genuinely useful:** k=5 possesses a finite divergence point (`≤ 4`) *and*
produces small-`C` extinction data of the same shape as k=4's; therefore the shape of the k=4 extinction
curve carries no information about whether `C*₄` is finite. That does sharpen CORE Remark 17(b) from
"k=5 also dies at small C" to "k=5 also dies at small C **and** is known to stop dying by C = 4".
**Repair:** state the claim in that form, and drop "in the one case where C\* is known".

The downstream editorial conclusion ("R9's weak lean NO should be downgraded to no lean") is a judgement,
not a theorem; nothing here refutes it, but it should not be listed among findings.

---

## 9. Checklist sweep (PROBLEM.md conventions)

1. **Both orientations.** Handled everywhere. R2's descending case is fully killed by L3; my scanners and
   DFS test both; `apcheck.has_monotone_kap_brute` (the ground truth I validated against) covers both by
   allowing negative `d`. R8's T1/T2 produce increasing APs only, which is fine for existence claims.
2. **Strict positions, `d ≥ 1`, no reuse, no reindexing.** All checkers use strict position inequalities
   and `d ≥ 1`; `d = 0` excluded. Value restrictions *do* reindex positions — used correctly (positions
   only shrink); position prefixes do not reindex — also used correctly (class S).
3. **Injectivity / surjectivity / order type ω.** Construction A: all three established structurally (L0).
   Class-A extinction: uses only injectivity + restriction, legitimate because it is a *necessary
   condition*, not a YES proof. **Class S at the `∀ψ` level is where surjectivity is silently dropped —
   see §5, this is the audit's main finding.**
4. **Compactness.** The only König step in the chain is CORE Lemma 6(⇐), which STATUS's extinction
   theorems do not need. Lemma 6's order-type-ω preservation is correctly proved
   (`#pred(v) ≤ φ(v) − 1`), and CORE Lemma 1 supplies the bijection.
5. **Named theorems.** None of Szemerédi / van der Waerden / Ramsey / Erdős–Szekeres is used in any
   audited proof; König is used only where noted. No uniformity issues.
6. **Boundary cases.** `v − (k−1)d ≥ 1` guards present; `⌊Cv⌋` vs `Cv` equivalence for integer positions
   verified; `⌊4i/3⌋ ≥ (4i−2)/3` used correctly in the class-S restatement; L5's `i ≥ 1` restriction is
   necessary and observed.
7. **Circularity.** None. No audited lemma restates 196 or an equivalent unavoidability claim.
8. **Conventions.** ℕ starts at 1 throughout; values vs positions never swapped in the audited material;
   R8's problem-195 content is explicitly labelled.
9. **Finite vs infinite.** R2's infinite 5-AP-free claim rests on the hand proof, not on the N = 65 535
   scan, and STATUS says so. The class-S finite computation is the correct finite shadow of its infinite
   statement. The `N*₅(C) = ∞` theorem is infinite-by-construction, not by extrapolation.
10. **SAT/CP used as theorems.** No SAT result was re-derived or re-run by the consolidation, and STATUS
    generally says so — the single leak is `ρ(85) > 2` (§8.1). R2's Mod-1 frontier, R8's N = 242 / ±242,
    and R9's SIS/N=14,15 remain unverified and are correctly flagged as such.

---

## 10. Bottom line

The consolidation's **computational** record is excellent: every re-runnable number I checked reproduced
exactly, including billion-node totals and per-level dead counts. Every hand proof it certifies (R2 L0–L7 +
Theorem + Proposition; R8 T1, T2, T3, W, L3–L6; the class-S enumeration; CORE Lemma 8) is sound. The new
displacement theorem `N*₅(C) = +∞ for C ≥ 4` is sound and is the report's most valuable contribution.

The failures are all in the **framing**, and one of them matters:

* **BROKEN (item 8).** The class-S programme is claimed to be "immune to Remark 17(a)". It is not; it is
  worse off. `a(i) = 2^i` is an injective, `ψ`-bounded, 3-AP-free sequence for `ψ(i) = 2^i`, so
  position-side `∀ψ`-extinction is false, and the ladder can never reach YES. The value-side ladder,
  which STATUS demotes, is the one with the logically correct target.
* **BROKEN (item 7).** "Only class S avoids compactness" is false; class-A extinction gives infinite
  theorems by the same one-line restriction argument (CORE Lemma 6(⇒), used explicitly in CORE Lemmas 7/7b).
* **REPAIRABLE (items 5, 19, 20, 21).** One overclaim ("exactly a factor-4 corridor"), one mislabelled
  certification (`ρ(85) > 2` inside "PROVED / all reproduced"), one unsourced number ("k=5, C=3/2: > 90"),
  and one overstatement ("the one case where `C*` is known").

Ranked next-step #2 ("mine the class-S ladder") should be rewritten or dropped in light of §5.
Everything else in §7 of STATUS stands.
