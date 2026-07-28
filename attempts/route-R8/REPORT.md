# Route R8 — Transfer analysis: Erdős 196 (ℕ, monotone 4-APs) vs the ℤ-analogue (Erdős 195)

**Verdict first.** Route R8 does not resolve 196. What it establishes, with proofs and
machine verification:

1. **Exact ℤ-side map** (all re-derived/verified here; nothing imported on faith): for
   permutations of ℤ (doubly infinite sequences), monotone-AP forcing is known only for the
   trivial length 2; length-3 forcing is open, length-4 forcing is open, and length 5 is NOT
   forced (Adenwalla [LIT]; independently supported here by machine-verified 5-AP-free
   two-sided windows covering [−127,127] built from my own macro). So Erdős 195's answer lies
   in {2, 3, 4}, while for ℕ the corresponding answer lies in {3, 4} (DEGS77). **Length 4 is
   exactly the overlap: open on both sides, and neither resolution transfers automatically.**
2. **Proved impossibility theorem T3**: no "annulus macro" arrangement of ℤ (scale blocks in
   any order, any internal arrangements) avoids monotone **3**-APs — the entire
   block-construction toolbox is provably useless for the ℤ length-3 problem.
3. **Proved impossibility theorem T2**: any "split" extension of any ℕ-permutation to ℤ (all
   non-positives to the left, in any order, up to finitely many exceptions) contains a
   monotone 4-AP. So 196-NO would not give a ℤ-avoider by concatenation, and a ℤ-avoider
   yields a 196-witness only under a boundedness hypothesis that is itself 196-hard.
4. **A complete folding-obstruction taxonomy** for (a) restriction, (b) interleaving,
   (c) conjugation — each with either a proved impossibility lemma or machine-found witness
   families on actual verified ℤ-objects.
5. **Transferable technique, fully re-derived**: a new 12-line proof of a
   LeSaulnier–Vijay-type theorem (Theorem W): the explicit permutation
   `2, (1,4,6), (3,8,10), (5,12,14), …` of ℕ has **no monotone 4-AP with odd common
   difference** (machine-verified to N = 13334). The Adenwalla-type ladder (no monotone 4-AP
   with d ≢ 0 mod 2^k) is reconstructed as "ascending residue streams with bit-reversed
   geometric rates", verified for k = 2 (N = 5864) and k = 3 (N = 1255). Its limit
   obstruction is identified and proved (Lemma L4): every AP-restriction of a
   196-counterexample is again a 196-counterexample, so no ladder (which leaves deep classes
   ascending) can close.
6. **Machine evidence on the open length-4 problems**: at the necessary "pure-cross" level,
   base-3 annuli admit legal two-sided macros at k = 4 (base-2 provably do not), and verified
   4-AP-free two-sided windows cover [−80, 80]; but the full constraint system for that macro
   is solver-certified UNSAT by ±242 — the **same scale horizon (alive at 80, dead at 242)**
   as the one-sided ternary system. The k = 4 obstruction thus has a scale-local core shared
   by ℕ and ℤ, whereas the k = 3 gap (forced on ℕ, wide open with all macros dead on ℤ) is
   genuinely a one-sided/two-sided structural gap.

Everything below is self-contained: every lemma used in an argument is proved here; every
construction is machine-verified with exact arithmetic (scripts in this directory, logs
cited). SAT results marked "solver-certified" rely on CaDiCaL's UNSAT answer; every SAT
(existence) answer was re-verified independently by the exact checkers.

---

## 0. Definitions pinned (ℤ-analogue vs our problem)

Our problem (PROBLEM.md, binding): bijection a : ℕ → ℕ, ℕ = {1,2,…}; monotone 4-AP =
positions i₁<i₂<i₃<i₄ whose values form an AP with common difference ±d, d ≥ 1.

**ℤ-analogue (Erdős 195).** A permutation of ℤ is a bijection b : ℤ → ℤ viewed as the doubly
infinite sequence …, b(−1), b(0), b(1), …. A monotone k-AP: positions p₁<⋯<p_k **in ℤ**,
values an AP read increasingly or decreasingly. Problem 195 asks for the largest k such that
every permutation of ℤ contains a monotone k-AP. (Statement pinned from the erdosproblems 195
mirror, fetched 2026-07-28: "Geneson [Ge19] proved that k ≤ 5. Adenwalla [Ad22] proved that
k ≤ 4." — i.e. the record is a ℤ-permutation with no monotone 5-AP; no nontrivial lower
bound is recorded.)

Differences from our setting, all load-bearing:
* position order type ζ (= ℤ) instead of ω: **no first position**, and **infinite descending
  position chains exist**;
* value set ℤ: **no least value**; every AP extends backwards inside the value set (in ℕ,
  x − d is a value only if d < x);
* a monotone AP may **cross 0** in values — no ℕ-analogue.

Source-access note: the full texts of arXiv 2211.04451 / 2302.09662 were not retrievable in
this environment (egress-blocked); bibliographic facts were pinned from the problem-195
statement mirror and abstracts. Accordingly **no construction was imported**: every object
below is built and verified from scratch. Literature claims are labeled [LIT] and are never
used in proofs.

## 1. Verified map of the ℤ side at lengths 3, 4, 5+

| length | permutations of ℕ (196 side) | permutations of ℤ (195 side) |
|---|---|---|
| 2 | forced (trivial) | forced (trivial) |
| 3 | **forced** — DEGS77(a) (certified background); re-proved here as Theorem T1 with a sharper conclusion (edge-anchored increasing 3-AP with d > first term) | **open**; T1's two ingredients both fail two-sided; annulus-macro avoidance **provably impossible** (Theorem T3, hand proof); bounded-displacement avoidance impossible (Lemma D, exact small-C extinction certificates) |
| 4 | **open** (= Erdős 196); partial avoidance: no monotone 4-AP with d ≢ 0 mod 2^k (Theorem W here for k=1, proved; ladder verified for k=2,3) | **open**; [LIT] nothing recorded; here: pure-cross feasibility proved possible at base 3 with legal two-sided slot orders, verified 4-AP-free windows [−80,80], and solver-certified death of that macro at ±242 |
| 5 | not forced — DEGS77(b) (certified; also reconstructed at SAT level to N = 255, `e3_sat.py`) | **not forced** — [LIT] Adenwalla "k ≤ 4"; independently supported: verified 5-AP-free windows [−127,127] (dyadic alternating macro, `e4_zjoint_k5.log`) and [−80,80] (ternary, `e10_zb3_k5.log`) |
| 6+ | subsumed by 5 | subsumed by 5 ([LIT] Geneson's 6-avoider not needed) |

So 195 ∈ {2,3,4}, 196's "largest forced length" ∈ {3,4}.

## 2. Theorem T1 (one-sided 3-AP forcing; re-derivation of DEGS77(a) plus a bonus)

**Theorem T1.** Let a : ℕ → ℕ be a bijection, π = a⁻¹, c = a(1). Then some v ≥ 2c+1
satisfies π(v) < π(2v−c); hence (c, v, 2v−c) is an **increasing** monotone 3-AP whose first
term is the very first value c and whose common difference d = v−c ≥ c+1 **exceeds its first
term**.

*Proof.* If instead π(2v−c) < π(v) for every v ≥ 2c+1, then g(v) = 2v−c maps [2c+1, ∞) into
itself (g(v) ≥ 3c+2 ≥ 2c+1 as c ≥ 1), and the orbit v₀ = 2c+1, v_{k+1} = g(v_k) gives an
infinite strictly decreasing sequence of positions in ℕ — impossible. π(c) = 1 < π(v) is
automatic, and c < v < 2v−c. ∎

**Where one-sidedness enters** (both fail in ℤ): (i) a first position whose value precedes
everything; (ii) well-foundedness of positions. This answers "is the ℤ 3-AP situation
actually different": the forcing mechanism is intrinsically one-sided, and no two-sided
forcing proof is known (§1).

**Bonus**: the 3-AP produced has d > c = its first term, so its backward extension c − d is
≤ 0 — it *leaves ℕ*. Every permutation of ℕ contains such a left-edge 3-AP. This powers T2.

## 3. Theorem T2 (split impossibility — folding strategy (a-inverse) is dead)

**Theorem T2.** Let b : ℤ → ℤ be a bijection such that for some position s and some **finite**
X ⊂ ℕ, the values at positions < s are exactly ℤ_{≤0} ∪ X. (X = ∅ is the naive extension:
any ℕ-permutation on the right, the non-positives in any order on the left.) Then b contains
an increasing monotone 4-AP.

*Proof.* The right part r = (b(s), b(s+1), …) is an ω-indexed injective sequence with value
set S = ℕ∖X. Let c = b(s) ≥ 1, g(v) = 2v−c. For f ∈ X, g^k(v) = f forces
v = c + (f−c)/2^k: no solutions when f ≤ c (as g^k(v) ≥ v ≥ 2c+1 > f), at most
⌊log₂(f−c)⌋+1 otherwise; so only finitely many v ≥ 2c+1 have g-orbits meeting X. Pick
v₀ ≥ 2c+1 with v₀ ∈ S and orbit(v₀) ⊆ S. T1's descent inside r yields v in the orbit with
π_r(v) < π_r(g(v)): an increasing monotone 3-AP (c, v, 2v−c) in r with d = v−c ≥ c+1. Then
x := c−d ≤ 0 is a value of b at some position < s, i.e. before all of r. So (x, c, v, 2v−c)
is an increasing monotone 4-AP of b. ∎

(The mirror — everything ≥ 1 to the left, up to finitely many exceptions — follows via
v ↦ −v, p ↦ −p, which preserves monotone APs.)

**Consequences.** (i) A 196-counterexample cannot be extended to a ℤ-avoider by any split
layout; negatives must be interleaved cofinally rightward. (ii) Conversely, by the
Restriction Lemma L3, a ℤ-4-avoider whose positive values occupy positions bounded below
restricts to a 196-counterexample; T2 shows such objects cannot come from splitting —
building one at all *is* solving 196.

## 4. Folding-obstruction taxonomy (deliverable 2)

Experiments use two actual, independently verified windows (`e11_prepare.py`,
`windows.json`, log `e11_folding.log`): `Z_dyadic_5free_M6` (255 values, no monotone 5-AP)
and `Z_ternary_4free_M3` (161 values covering [−80,80], no monotone 4-AP).

**(a) Restriction to positive values.**
* **Lemma L3 (Restriction).** Any subsequence (in position order) of an injective sequence
  has only monotone APs that the full sequence has. *Proof:* subsequence positions are
  order-embedded; the AP condition is intrinsic to values. ∎ (Machine: 0 new APs in both
  restrictions.)
* **Obstruction:** the restriction is an ℕ-permutation iff positive values occupy positions
  bounded below (order type ω). In any alternating-annulus macro, every annulus contains
  positive values and annuli alternate sides, so positives are cofinal both ways: order type
  ζ. Measured: positives sit 42 left / 85 right (dyadic object), 60 left / 20 right
  (ternary object). Demanding boundedness instead is 196-hard (T2 + L3, §3).

**(b) Zigzag fold to order type ω.** With ψ = |·|-order on positions (0, +1, −1, +2, −2, …)
and μ : ℤ → ℕ, μ(v) = 2v (v ≥ 1), 1−2v (v ≤ 0), the fold F(b)(n) = μ(b(ψ(n))) is an
ℕ-sequence. Two failure families, both machine-instantiated:
* **b1 (position-order failure).** Same-parity monotone APs of F(b) pull back to genuine
  ℤ-APs of b, monotone for |p|-order though non-monotone for p-order — b's avoidance says
  nothing about |p|-order. Witnesses in the fold of the 4-free object: (2,8,14,20) ←
  ℤ-AP (1,4,7,10); (1,5,9,13) ← ℤ-AP (0,−2,−4,−6). Counts for the 5-free object's fold:
  103 even-class + 178 odd-class monotone 4-APs.
* **b2 (value-map failure).** Parity-alternating (odd-d) monotone APs of F(b) pull back to
  *non-APs* — constraints invisible in ℤ. Witnesses: (1,2,3,4) ← (0,1,−1,2);
  (1,4,7,10) ← (0,2,−3,5). Counts: 256 alternating 4-APs (5-free object), 14 (4-free).
* For *any* bijection ψ : ℕ → ℤ the ψ-order cannot extend the ζ-order (ω ≠ ζ), so some
  cofinal family of position pairs is reversed and b1-type families persist; a fold can only
  work if the ℤ-object is co-designed with ψ — which is exactly the stream mechanism of §5.

**(c) Value conjugation.**
* **Lemma L5 (Affine rigidity).** If φ : A → ℤ (A ∈ {ℕ, ℤ}) maps every 3-AP of A to a 3-AP
  (φ(x) − 2φ(x+1... for all x, d: φ(x) + φ(x+2d) = 2φ(x+d)), then φ is affine. *Proof:* the
  d = 1 instances give constant first differences. ∎ No affine map is a bijection ℤ → ℕ or
  ℕ → ℤ (affine images of ℤ are unbounded both ways; of ℕ, one-sided APs). Hence **every**
  value bijection between ℤ and ℕ creates APs from non-APs and destroys APs — family b2 is
  unavoidable under any conjugation. (Machine samples: μ breaks 2/4 sampled ℤ-APs, μ⁻¹
  breaks 2/4 sampled ℕ-APs.)

**Summary.** (a) is blocked by an order-type dichotomy whose good branch is 196-hard; (b) is
blocked by b1 unless co-designed, plus L5-unavoidable b2; (c) is blocked by L5. The only
surviving transfer is the co-designed stream mechanism — §5.

## 5. Transferable technique: the parity-stream mechanism (deliverable 3)

μ maps (non-positives, positives) onto (odds, evens); killing the b2-family means killing
odd-difference APs by pure interleaving. That can be done outright:

**Theorem W (LV-type theorem; new construction, full proof).** Let
W = 2, (1, 4, 6), (3, 8, 10), (5, 12, 14), … — after the initial 2, concatenate the triples
(2i−1, 4i, 4i+2), i ≥ 1. Then W is a permutation of ℕ with **no monotone 4-term AP of odd
common difference**, in either orientation.

*Proof.* W lists all odds ascending and all evens ascending: a permutation of ℕ. Positions:
pos(o) = (3o+1)/2 for odd o; pos(2) = 1 and for even e: (3e−2)/4 ≤ pos(e) ≤ 3e/4
(e = 4i ↦ 3i = 3e/4; e = 4i+2 ↦ 3i+1 = (3e−2)/4; e = 2 ↦ 1 = (3·2−2)/4). Let
x, x+d, x+2d, x+3d ⊆ ℕ, d odd; terms alternate parity.

Case x odd — terms (o, e, o′, e′) = (x, x+d, x+2d, x+3d):
pos(o′) − pos(e) ≥ (3(x+2d)+1)/2 − 3(x+d)/4 = (3x+9d+2)/4 > 0, so pos(e) < pos(o′) always —
a decreasing monotone AP would need pos(e) > pos(o′): impossible.
pos(o′) − pos(e′) ≥ (3(x+2d)+1)/2 − 3(x+3d)/4 = (3x+3d+2)/4 > 0, so pos(e′) < pos(o′)
always — an increasing monotone AP would need pos(o′) < pos(e′): impossible.

Case x even — terms (e, o, e′, o′):
pos(o) − pos(e′) ≥ (3(x+d)+1)/2 − 3(x+2d)/4 = (3x+2)/4 > 0, so pos(e′) < pos(o) always —
increasing needs pos(o) < pos(e′): impossible.
pos(o) − pos(e) ≥ (3(x+d)+1)/2 − 3x/4 = (3x+6d+2)/4 > 0, so pos(e) < pos(o) always —
decreasing needs pos(e) > pos(o): impossible. ∎

(Machine: no odd-d monotone 4-AP on the prefix permutation of [1..13334]; `e9_lv.log`. W has
even-d monotone 4-APs, e.g. 2,4,6,8 — necessarily, by L4 below. [LIT] LeSaulnier–Vijay 2011
proved the same avoidance statement; their construction was not consulted.)

**Mechanism isolated:** two ascending streams, evens at double rate. The proof uses only:
(α) each stream ascending (stream rank = value order), (β) rate skew ≥ 2.

**Adenwalla-type ladder (reconstructed).** Level k: 2^k ascending streams (residues mod 2^k),
emitted with geometric rates 2^{rev_k(r)} (bit-reversed exponents; exact fractional
scheduling). Machine-verified: k = 2, rates (1,4,2,8) on residues (1,2,3,0): no monotone
4-AP with d ≢ 0 mod 4 on [1..5864]; k = 3 (bit-reversed rates): none with d ≢ 0 mod 8 on
[1..1255] (`e9_lv.py`). The pairwise-skew lemma explains why: two residue classes coupled by
an AP with d ≢ 0 mod 2^k carry distinct bit-reversed exponents, giving skew ≥ 2 in a
non-cyclic orientation pattern (plain geometric rates 2^c fail — witness 3, 6, 9, 12 —
because the class path can descend in rate; bit-reversal breaks all monotone rate paths).
Full general-k proof not completed here; k = 1 is Theorem W.

**Limit obstruction of the ladder (proved).**
* **Lemma L4 (affine self-reduction).** For φ(n) = αn+β, α ≠ 0: k-APs correspond to k-APs,
  orientation preserved iff α > 0. Hence for any bijection a : ℕ → ℕ (or ℤ → ℤ) and any
  infinite AP P of values, the P-values in position order, relabelled through the affine
  bijection ℕ → P, form again a bijection whose monotone k-APs all come from monotone k-APs
  of a inside P (L3 + affinity; position set of P-values has order type ω resp. ζ).
  **Every AP-restriction of a 196-counterexample is again a 196-counterexample.** ∎
* Corollary: in a 196-counterexample no infinite AP of values — in particular no residue
  class mod 2^k — can be ascending or descending (an ascending class q, q+r, q+2r, … in
  ascending position order is itself a monotone AP of every length). Ladder constructions
  have all streams ascending; mechanism (α) requires it. **Killing d ≢ 0 mod 2^k needs
  ascending streams; killing d ≡ 0 mod 2^k forbids them.** A 196-NO object must be scrambled
  at every 2-adic level with cross-level coordination — self-similarity is forced.

## 6. The band/annulus framework: length 4 vs 5, ℕ vs ℤ

**Lemma L6 (pigeonholes; one-line proofs, machine-checked exhaustively in range).** For a
k-AP t, t+d, …, t+(k−1)d of positive integers, (t+(k−1)d)/(t+(k−3)d) < 2 iff (5−k)d < t;
and (t+3d)/(t+d) < 3 always. Three positive values with max/min ratio < B lie in at most 2
consecutive base-B bands [B^m, B^{m+1}), so two adjacent ones share a band. Hence:
* k = 5: every 5-AP in ℕ has an adjacent same-band pair among its last three terms, dyadic
  bands, unconditionally;
* k = 4: same with **ternary** bands, unconditionally; with dyadic bands it fails exactly
  when d ≥ t (witness (t,d) = (1,5): 6, 11, 16 in three distinct dyadic bands).
In ℤ both fail for APs crossing or starting near 0 — the "pure-cross" families.

In a value-ascending band macro, decreasing monotone APs live inside one band, and an
increasing k-AP is broken iff some adjacent same-band pair is internally reversed (cross-band
pairs are automatically position-increasing). L6 says the needed pair exists — the framework
is complete for k = 5 (base 2) and k = 4 (base 3) on ℕ. Machine landscape (each SAT
re-verified exactly; UNSAT solver-certified):

| system | result |
|---|---|
| ℕ, k=5, base 2, decoupled per-band conditions (A),(B),(C) | SAT bands 0–5, UNSAT at band 6 (`e3_perblock.py`) — decoupling too lossy |
| ℕ, k=5, base 2, joint | SAT through N = 255, verified (`e3_sat.py`) |
| ℕ, k=4, base 3, decoupled | UNSAT at band 2 (`e6_all4.log`) |
| ℕ, k=4, base 3, joint | SAT to N = 80, **UNSAT at N = 242** (`e7_b3_all_asc.log`): no ternary ascending band macro on [1, 3^5) avoids monotone 4-APs |
| ℕ, k=4 odd d only, base 3, joint | SAT through N = 242, verified 0 violations |
| ℕ, k=4, base 2, slot order 0,1,2,4,3,6,5,… (passes pure-cross), joint | SAT to N = 31, UNSAT at N = 63 |
| ℕ, k=4 odd d, base 2, same slots | SAT to N = 127, UNSAT at N = 255 |
| ℤ, k=5, base 2 alternating annuli, joint | SAT: verified 5-AP-free windows **[−127, 127]** (`e4_zjoint_k5.log`) |
| ℤ, k=4, base 2 alternating | macro refuted outright by the pure-cross family (−16, d=9): −16, −7, 2, 11, annulus scales (4,2,1,3) slot-monotone (`e4_zjoint_k4.log`) |
| ℤ, k=4, base 3 alternating, joint | SAT: verified 4-AP-free windows **[−80, 80]**; **UNSAT at ±242** (`e10_zb3_k4_M4.log`) |
| ℤ, k=5, base 3 alternating, joint | SAT: verified windows [−80, 80] (`e10_zb3_k5.log`) |

**Pure-cross level (necessary conditions for any annulus macro; `e5_scaleorder.log`,
`e8_zeta.log`).** A k-AP whose adjacent terms always lie in distinct annuli is monotone iff
its annulus sequence is slot-monotone; within-annulus freedom cannot break it.
* ℕ: base 2, k=4: patterns exist (e.g. 1, 6, 11, 16) but some slot orders pass; base 3,
  k ≥ 4: **no pure-cross patterns at all** (L6); k=3: patterns exist, alternating-type
  orders pass (consistent with DEGS forcing living below the pure-cross level).
* ℤ: k=3, bases 2 and 3: **UNSAT over all slot orders** → Theorem T3. k=4: base 2 fails for
  every legal (ζ-realizable) order tested; base 3: alternating ζ-orders pass all patterns
  (scales ≤ 6). k=5: alternating passes (both bases).

**Theorem T3 (annulus-macro impossibility, ℤ, k = 3; hand proof).** With ternary annuli
A_m = {v : 3^m ≤ |v| < 3^{m+1}} (A₀ ∋ 0, ±1, ±2), there is no arrangement of ℤ in which
every annulus occupies a contiguous block of positions (blocks in any order σ, any
within-annulus arrangements) without a monotone 3-AP.

*Proof.* Four APs, each with terms in pairwise distinct annuli, so each must have its middle
annulus σ-extreme among its three:
(1, 122, 243): scales (0, 4, 5) ⇒ σ₄ extreme in {σ₀, σ₄, σ₅};
(−239, 2, 243): scales (4, 0, 5) ⇒ σ₀ extreme in {σ₀, σ₄, σ₅};
together: σ₅ lies strictly between σ₀ and σ₄.
(241, 485, 729): scales (4, 5, 6) ⇒ σ₅ extreme in {σ₄, σ₅, σ₆};
(1, 365, 729): scales (0, 5, 6) ⇒ σ₅ extreme in {σ₀, σ₅, σ₆}.
If σ₀ < σ₅ < σ₄, the third forces σ₅ < σ₆ (not max), the fourth forces σ₅ > σ₆ (not min):
contradiction; σ₄ < σ₅ < σ₀ is symmetric. ∎ (Multiplying the witnesses by 3^j shifts all
scales by j, so "eventually-annulus" macros die too. A 5-pattern core exists for base 2.)

**Interpretation — where the gaps live.**
* Length 3: ℕ forced (T1, edge-powered); ℤ open with the macro toolbox provably dead (T3)
  and the forcing mechanism provably unavailable (T1 analysis). A genuine structural
  one-sided/two-sided gap.
* Length 4: the necessary pure-cross conditions separate base 2 from base 3 and ℤ-k3 from
  ℤ-k4; but the full ternary systems die at the **same scale horizon** one-sided and
  two-sided (alive at 80, dead by 242). The length-4 obstruction has a scale-local core
  present in both worlds — it is *not* explained by the left edge alone, though on ℕ the
  edge families (d ≥ t; T1's bonus; T2) are additional and specifically one-sided.
* Length 5: macro avoidance verified in both worlds; not forced on either side.

## 7. Displacement lemma (calibration)

**Lemma D.** If b : ℤ → ℤ (or ℕ → ℕ) is injective with |b(p) − p| ≤ C for all p, then for
every d ≥ 2C+1 every AP x, x+d, …, x+(k−1)d is increasing monotone
(p(x+jd) ≥ x+jd−C > x+(j−1)d+C ≥ p(x+(j−1)d)). All monotone-AP avoiders, one- or two-sided,
have unbounded displacement. Machine: exact extinction certificates for small C (one-sided
k=3: max depth 4/7/9/11/13/15 for C = 1..6; two-sided k=3: 4/8/10/12 for C = 1..4;
`dfs_compare_k34.log`), consistent with the trivial bound. This kills all near-identity
transfer maps at once.

## 8. Assessment for 196 and next steps

**Assessment.** (i) All avoidance technology examined (bands/annuli, streams, ladders) is
*edge-limited on ℕ*: it fails on families with d ≥ x (backward extension leaves ℕ) — and
additionally hits a scale-local length-4 core that appears even two-sided. (ii) The forcing
technology (T1 descent) is *edge-powered* and stalls at length 3: its natural 4-term
extension produces the 4th term below the edge — available in ℤ (that is exactly T2), absent
in ℕ. (iii) L4 forces any 196-counterexample to be self-similar under AP-restriction:
scrambled at every 2-adic level; no finite-level ladder suffices; this is the precise reason
LV/Adenwalla-type partial results cannot be pushed to all d by iteration. (iv) The ℤ-vs-ℕ
gap at length 4 is thinner than folklore suggests: within the strongest framework tried here,
both worlds die at the same horizon; what ℤ buys is freedom at the *macro* level (pure-cross
feasibility, no forced edge families), not at the local level. On balance R8's evidence
tilts weakly toward the two problems being genuinely independent at length 4, with 196
turning on the one-sided edge + self-similarity requirements that no folding can supply.

**Next steps (ranked).**
1. Mine the N = 242 one-sided and ±242 two-sided UNSAT cores: if the shared scale-local core
   is macro-independent it is a candidate YES-side lemma for both 195(k=4) and 196; if it is
   an artifact of band contiguity, redesign macros around it (feed routes R1/R4).
2. Close a per-annulus closed form for the ℤ 5-avoider (would finish a fully independent
   re-proof of "195: k ≤ 4" — currently machine-verified to ±127 without closed form).
3. Test the other pure-cross-passing ζ-orders (RRLL, RLLR, R0-then-alt) for ℤ ternary k=4
   beyond ±80 before concluding the two-sided macro family is exhausted.
4. Prove the general-k bit-reversed-rates ladder theorem (quotable partial result for the
   restricted-difference version of 196).

## 9. File index (all in attempts/route-R8/)

| file | role |
|---|---|
| `zcheck.py`, `fastcheck.py` | signed/two-sided exact checkers, cross-validated vs brute force (4000 + 2500 random cases) |
| `dfs_compare.py`, `dfs_compare_k34.log` | Lemma D calibration; exact extinction certificates |
| `e3_block_search.py`, `e3_sat.py`, `e3_perblock.py` | ℕ dyadic k=5 band framework (simple families, global SAT to N=255, decoupled conditions) |
| `e4_zsat.py`, `e4_zjoint.py`, `e4_zjoint_k5.log`, `e4_zjoint_k4.log` | ℤ dyadic alternating macro: k=5 verified windows ±127; k=4 pure-cross refutation family (−16, 9) |
| `e5_scaleorder.py`, `e5_scaleorder.log` | pure-cross pattern enumeration + slot-order SAT (bases 2/3/4, ℕ and ℤ, k = 3..6) |
| `e6_ternary_n.py`, `e6_all4.log`, `e6_odd4.log`, `e6_all5.log` | ℕ ternary decoupled per-band systems |
| `e7_joint_general.py`, `e7_b2_*.log`, `e7_b3_all_asc.log` | ℕ joint band SAT with arbitrary slot orders (finite impossibility results) |
| `e8_zeta.py`, `e8_zeta.log` | ζ-realizable slot-order tests; minimal UNSAT cores for T3 |
| `e9_lv.py`, `e9_lv.log` | Theorem W verification (N = 13334); bit-reversed-rate ladder (mod 4, mod 8) |
| `e10_zb3.py`, `e10_zb3_k4.log`, `e10_zb3_k4_M4.log`, `e10_zb3_k5.log` | ℤ ternary annuli: k=4 verified windows ±80 + UNSAT at ±242; k=5 windows ±80 |
| `e11_prepare.py`, `e11_folding.py`, `windows.json`, `e11_folding.log` | folding experiments on verified ℤ-objects: obstructions (a), (b1), (b2), (c) instantiated |
