# Route R3 — digit/parity orderings repaired to order type ω: REPORT

Session 1, 2026-07-27/28. PROBLEM.md governs. All machine claims are backed by scripts in
this directory; every checker was cross-validated against `experiments/apcheck.py`
(itself brute-force-validated). Finite checks are evidence, not proof; the items marked
**proved** have complete proofs below.

## Verdict first

1. **No surviving construction.** Twenty-six digit-defined orderings of N with order
   type omega were built and machine-checked on value restrictions [1..10^4]; all contain
   monotone 4-APs, all already among values <= 24. Each failure is structurally
   diagnosed (Sec. 5); the failures are lawful, not accidental.
2. **Contiguous scale-blocks are dead in every base tested — a theorem for b = 2, 3, 4.**
   For base 2 by a two-line forced family (Theorem A, human proof): the 4-AP
   **2^M (1, 6, 11, 16)** meets four pairwise distinct dyadic blocks, so any ordering
   that eventually keeps dyadic blocks in contiguous increasing position windows
   contains a monotone increasing 4-AP *regardless of the internal block orders*.
   For bases 3 and 4 by machine-exact infeasibility (Theorem B): the purely arithmetic
   constraint system that any single block D_3 internal order must satisfy is UNSAT
   (two independent solver stacks), and a scaling embedding (Lemma Sc) propagates death
   to every later block. This kills the entire "repair the parity recursion by blocking
   it" program in its contiguous form.
3. **The parity-recursion mechanism itself cannot be rescued to order type omega**
   (Proposition B, proved): any order that breaks all 4-APs by the valuation mechanism
   that sigma uses gives 2^t infinitely many predecessors. Repairs must break
   infinitely many APs by genuinely different means.
4. **Positive discovery: the base-3 priority comparator tau kills all monotone 4-APs on
   every subset of N** (Lemma T, proved) — the exact analog, one level up, of the
   parity recursion killing 3-APs. tau is the natural "4-AP-free kernel" for this
   route; its defect is the same as sigma's (order type >> omega). The repair question
   for tau is the sharpest surviving open direction (Sec. 7).
5. Deliverable-1 digit lemmas L1 (valuation trichotomy), L2 (block-gap), L3 (carry
   identity) are proved and machine-tested (20 000 random (x,d) <= 10^6 + exhaustive
   small ranges): `lemmas_check.py`.
6. Near-contiguity (deliverable 3): with separation 2 (adjacent dyadic blocks may
   interleave) **no single 4-AP is forced** (Theorem A(c), proved via L2), so the
   base-2 obstruction is sharp at distance 2; exact finite feasibility of 2-separated
   orderings is probed by CP-SAT (Sec. 4.4).

Cross-route consistency: route-R1's minimal infeasible cut-set {8, 26, 80} is exactly
{3^2-1, 3^3-1, 3^4-1} — the top elements of the base-3 blocks D_1, D_2, D_3. Two
independent routes located the same death sites. CORE.md Thm 12 + R1/R4 empirics
(linear displacement profiles die for C <= 3) explain a priori why all block-graded
designs here (displacement caps <= 4v) had to die, and why the only superlinear family
tried (recursive v2-promotion, Sec. 5) was the right *kind* of attempt even though it
fails for an identifiable reason (promotion inheritance).

---

## 1. Notation

N = {1,2,...}. v2(n), v3(n): 2-/3-adic valuations. s2(n): binary digit sum.
block_b(n) = floor(log_b n); D^b_j = [b^j, b^{j+1}) ∩ N (the base-b blocks); D_j means
the base at hand. A 4-AP is (x, x+d, x+2d, x+3d), x, d >= 1. For an ordering (= a
bijection a: N->N or its induced order, cf. CORE.md Lemma 1), "monotone" is as in
PROBLEM.md. "pi-increasing pair (u,w)" means u before w.

## 2. Where 4-APs live in digit terms (deliverable 1)

### Lemma L1 (valuation trichotomy along 4-APs) — proved, machine-tested

Let x, d >= 1 and v = v2(d). Exactly one of:

* (i) v2(x) < v. Then v2(x+kd) = v2(x) for k = 0,1,2,3 (constant).
* (ii) v2(x) = v. Then v2(x) = v2(x+2d) = v; v2(x+d), v2(x+3d) >= v+1, and
  min(v2(x+d), v2(x+3d)) = v+1 exactly.
* (iii) v2(x) > v. Then v2(x+d) = v2(x+3d) = v; v2(x), v2(x+2d) >= v+1, and
  min(v2(x), v2(x+2d)) = v+1 exactly.

Corollaries. Along any 4-AP, v2 takes at most 3 distinct values; the set of indices k
minimizing v2(x+kd) is {0,1,2,3}, {0,2} or {1,3}; in cases (ii)/(iii) the multiset of
valuations is {v, v, v+1, s} with s >= v+1, the two v's at distance 2d.

*Proof.* Write d = 2^v e, e odd. (i) If s := v2(x) < v: x + kd = 2^s(x/2^s + k 2^{v-s} e)
and x/2^s is odd while k 2^{v-s} e is even, so the bracket is odd: v2 = s for all k.
(ii) If x = 2^v a, a odd: x + kd = 2^v(a + ke); a + ke is odd for even k (v2 = v) and
even for odd k (v2 >= v+1). Moreover (x+3d) - (x+d) = 2d has v2 exactly v+1, so x+d and
x+3d cannot both have v2 >= v+2; hence the min is exactly v+1. (iii) If v2(x) > v:
x + kd = 2^v(x/2^v + ke) with x/2^v even: for odd k the bracket is odd (v2 = v); for
k = 0, 2 both terms have v2 >= v+1, and (x+2d) - x = 2d has v2 = v+1, so again the min
is exactly v+1. QED

Machine test: `lemmas_check.py` (exhaustive x,d < 260; 20 000 random pairs <= 10^6). OK.

### Lemma L2 (block-gap lemma) — proved, machine-tested

Let m_k = block_b(x+kd). Then m_0 <= m_1 <= m_2 <= m_3 and:

* for every b >= 2: m_2 <= m_1 + 1 and m_3 <= m_2 + 1;
* for b >= 3: m_3 <= m_1 + 1 — hence **at least one of the adjacent pairs
  (x+d, x+2d), (x+2d, x+3d) lies inside a single base-b block**, and the block
  pattern of any 4-AP is (m_0, k, k, k), (m_0, k, k, k+1) or (m_0, k, k+1, k+1)
  (m_0 <= k arbitrary — only the first gap can be large);
* for b = 2: m_3 <= m_1 + 2, and four pairwise distinct blocks do occur
  (Theorem A(a)); the gap m_1 - m_0 is unbounded in every base.

*Proof.* For k >= 1, x+(k+1)d < 2(x+kd) iff x+(k-1)d > 0, which holds; if
x+kd < b^{m+1} then x+(k+1)d < 2 b^{m+1} <= b^{m+2}, giving m_{k+1} <= m_k + 1 for any
b >= 2. Also x+3d < 3(x+d) (iff 2x > 0), so for b >= 3: x+d < b^{m+1} implies
x+3d < 3 b^{m+1} <= b^{m+2}, i.e. m_3 <= m_1 + 1. For b = 2: x+3d < 4(x+d) gives
m_3 <= m_1 + 2. Monotonicity is trivial. Pattern list: from m_1 <= m_2 <= m_3 <= m_1+1.
Unboundedness of m_1 - m_0: x = 1, d large. QED

Machine test: same script, bases 2,3,4,5; also verified: 463 543 four-distinct-block
4-APs with x,d < 2000 in base 2, none in bases >= 3 (implied by the lemma). OK.

### Lemma L3 (carry identity) — proved, machine-tested

Since x + (x+3d) = (x+d) + (x+2d), Legendre/Kummer (c(a,b) = s2(a)+s2(b)-s2(a+b) =
number of carries in the binary addition a+b) gives

  [s2(x) + s2(x+3d)] - [s2(x+d) + s2(x+2d)] = c(x, x+3d) - c(x+d, x+2d).

In particular the Thue-Morse signs along any 4-AP satisfy
t(x) xor t(x+3d) xor t(x+d) xor t(x+2d) = parity of c(x,x+3d) + c(x+d,x+2d).
(Machine test compares direct carry simulation with the Legendre formula; both checks
in `lemmas_check.py`.) This is why no *fixed* TM-pattern lemma along 4-APs exists —
the sign is a carry statistic, not an invariant; construction O7's failure (Sec. 5) is
the constructive face of this.

## 3. The two comparators, and why sigma's mechanism cannot be repaired

### Lemma S (parity comparator) — proved, machine-tested

Define the sigma-order on any S ⊆ N: u before w iff at the first level l >= 0 where the
parities of g^l(u), g^l(w) differ (g(n) = ceil(n/2)), the odd one comes first (any fixed
per-level priority works). Then the sigma-order has **no monotone 3-AP on any subset**.
Its restriction to [1..N] is the parity recursion sigma_N (verified:
`experiments/parity_construction.py`).

*Proof.* Induction on d. If d is odd, x and x+2d have equal parity, x+d the other;
whichever priority level 0 uses, x+d is separated from {x, x+2d} on the same side:
positions (early, late, early) or (late, early, late) — not monotone. If d is even, all
terms have equal parity and g maps the AP to an AP with difference d/2 (g is
x -> (x+1)/2 on odds, x/2 on evens; equal-parity terms shift uniformly), recurse. QED

### Lemma T (base-3 priority comparator tau kills 4-APs on every subset) — proved, machine-tested

Fix any permutations pr_l of {0,1,2} (one per level l). Define tau: u before w iff at
the lowest base-3 digit level l where u, w differ, pr_l(digit_l(u)) < pr_l(digit_l(w)).
Then the tau-order of **any** S ⊆ N has **no monotone 4-AP (either orientation)** —
while (necessarily, DEGS77(a)) it has monotone 3-APs.

*Proof.* Let (x+kd) be a 4-AP, v = v3(d), delta = digit_v(d) in {1,2}, a = digit_v(x).
All four terms agree at digits < v (adding kd cannot touch them), and digit_v(x+kd) =
a + k delta mod 3 (no carry into level v). So the level-v digits along the AP are
a, a+delta, a+2delta, a — with a, a+delta, a+2delta pairwise distinct. For each
adjacent pair the first differing level is exactly v, so the positional order of each
adjacent pair is decided by pr_v on the cycle a -> a+delta -> a+2delta -> a. A monotone
increasing 4-AP needs pr_v(a) < pr_v(a+delta) < pr_v(a+2delta) < pr_v(a): impossible;
decreasing likewise. QED

Machine test: 3000 random subsets x random per-level priorities; zero monotone 4-APs;
3-APs present as expected. tau is **not** of order type omega (with natural priorities
every positive multiple of 3 precedes 1). — This is the R3 "kernel object": the finite
parity gadget of the problem statement, upgraded one AP-length, as a single global
comparator valid on all of N.

### Proposition B (no omega-order breaks everything the sigma-way) — proved

Say an order "uses the valuation mechanism" if for every 4-AP in cases (ii)/(iii) of
L1, every minimal-valuation term precedes every higher-valuation term (this is exactly
how the sigma-limit breaks all such APs — lower v2-class first). Then some element has
infinitely many predecessors; hence (CORE.md Lemma 1) the order is not induced by any
permutation of N.

*Proof.* Fix t >= 1 and any odd u > 2^t. The quadruple
(x, x+d, x+2d, x+3d) = (2^t, u, 2u-2^t, 3u-2^{t+1}) with d = u - 2^t >= 1 odd is a
4-AP of naturals; v = v2(d) = 0 and v2(x) = t > 0: case (iii). Its minimal-valuation
terms are u and 3u-2^{t+1} (odd), its higher-valuation terms include 2^t. The
mechanism forces u before 2^t — for every odd u > 2^t. QED

Consequently *any* type-omega repair must break infinitely many 4-APs (for each t, all
but finitely many of the APs above) by comparisons *within* the mechanism's blind spot.
The same argument transported through Lemma T's cycles blocks the naive "tau-limit
repair" (see Sec. 7). Machine sanity: family verified in `lemmas_check.py`.

## 4. Contiguous and near-contiguous block orderings (deliverable 3)

Say an ordering has *eventually contiguous base-b blocks* if there is M0 such that for
all M0 <= m < m', every element of D^b_m precedes every element of D^b_{m'}. Say it is
*g-separated* (base 2) if pos(u) < pos(w) whenever block_2(w) >= block_2(u) + g — g = 1
is contiguity, g = 2 lets adjacent blocks interleave arbitrarily.

### Theorem A (base-2 contiguity is dead; sharp at separation 2) — proved

(a) For every M >= 0, the 4-AP x = 2^M, d = 5 2^M, i.e. 2^M (1, 6, 11, 16), has its
terms in the pairwise distinct dyadic blocks D^2_M, D^2_{M+2}, D^2_{M+3}, D^2_{M+4}.

(b) Every ordering of N with eventually contiguous dyadic blocks (any internal
orders!) contains a monotone increasing 4-AP — namely 2^{M0} (1,6,11,16).

(c) Under 2-separation, no single 4-AP is forced: by L2 (b=2), consecutive terms among
x+d, x+2d, x+3d have block gaps <= 1, and only pairs with gap >= 2 are position-forced;
a forced monotone AP would need all three adjacent gaps >= 2 — impossible.

*Proof.* (a) direct: 1; 6 in [4,8); 11 in [8,16); 16 in [16,32); scaled by 2^M (blocks
shift by M). (b) all four blocks are >= M0 and pairwise distinct, so the four positions
are forced increasing. (c) as stated. QED  (Machine: `lemmas_check.py`; and the CP-SAT
probe on contiguous base-2 at N = 30 returns exactly this forced AP: `satprobe.py`.)

Note Theorem A is not implied by CORE.md Thm 12 (tame-kill): contiguous-block orderings
have displacement ~ v, far outside any |pos(v) - cv| <= B profile.

### Lemma R (exact residual system for contiguous blocks, b >= 3) — proved, machine-validated

Let b >= 3 and let an ordering have contiguous base-b blocks with internal orders pi_j.
For a 4-AP, by L2 its block pattern is (m0, k, k, k), (m0, k, k, k+1) or
(m0, k, k+1, k+1). Cross-block adjacent pairs are automatically position-increasing;
decreasing monotone 4-APs exist only inside a single block. Hence the ordering is
monotone-4-AP-free **iff** for every j:

* (R0) pi_j has no monotone 4-AP with all four terms in D_j (both orientations);
* (R1) *edge 3-APs*: pi_j has no increasing 3-AP (u, u+d, u+2d) in D_j with
  1 <= u-d < b^j (bottom-grounded: the extension term u-d sits in an earlier block) or
  with u+3d >= b^{j+1} (top-grounded: the extension sits in a later block);
* (R2) *forced pairs*: pi_j inverts (places w = u+d before u) every pair
  (u, u+d) in D_j with
  F1: 1 <= u-d < b^j and u+2d >= b^{j+1} (pair = middle of a low-high straddle), or
  F2: u-2d >= 1, u-d < b^j, block_b(u-2d) < block_b(u-d) (pair = top of an AP whose
  two lower terms lie in two distinct earlier blocks);
* (R3) *2+2 straddles*: for every AP with x, x+d in D_j and x+2d, x+3d in D_{j+1}
  (2+2 splits only occur between adjacent blocks: non-adjacent would need
  d >= b^{i+1}(b-1) > x+d, absurd), pi_j inverts (x, x+d) or pi_{j+1} inverts
  (x+2d, x+3d).

*Proof.* Case enumeration over the three patterns and the position of m0 relative to k,
using: cross-block pairs increase; a decreasing AP needs all adjacent pairs decreasing,
impossible with a cross-block pair. Each pattern contributes exactly one of R0-R3:
(m0, k, k, k+1) with m0 < k has same-block pair (x+d, x+2d) only — F1 with u = x+d;
(m0, m1, k, k) with m0 < m1 < k has same-block pair (x+2d, x+3d) only — F2 with
u = x+2d; (m0, k, k, k) with m0 < k is a bottom-grounded R1; (k, k, k, k+1) a
top-grounded R1; (k, k, k+1, k+1) and (m0=k-1 cases) give R3 or F-pairs; all-in-one
block gives R0. Conversely each violated item exhibits a monotone 4-AP. QED

Machine validation: `lemmaR_check.py` — for random internal orders (bases 3, 4, 5),
the witness set of the assembled permutation equals the case-rule prediction AP-by-AP;
the observed block patterns are exactly the predicted ones. OK.

### Lemma Sc (scaling embedding) — proved

For b >= 3 let Sigma_j denote the *decoupled* system {R0, R1, R2} for block D_j (these
constraints mention only pi_j — R3 is dropped). If Sigma_j is unsatisfiable then so is
Sigma_{j+1}. Hence "Sigma_{j0} UNSAT" kills **all** contiguous base-b block orderings,
since any such ordering satisfies Sigma_j for every j (necessity direction of Lemma R).

*Proof.* Given pi on D_{j+1} satisfying Sigma_{j+1}, define pi' on D_j by: u before w
iff bu before bw. Multiplication by b maps D_j into D_{j+1}, maps 4-APs to 4-APs and
preserves each defining inequality: u-d < b^j iff bu-bd < b^{j+1}; u+3d >= b^{j+1} iff
bu+3bd >= b^{j+2}; u-d >= 1 implies bu-bd >= b >= 1; and block_b(bm) = block_b(m)+1
preserves the F2 strict block inequality. So pi' satisfies Sigma_j. Contrapositive
gives the claim. QED

### Theorem B (contiguous base-3 and base-4 blocks are dead) — machine-exact, triple-checked

* Base 3: Sigma_1 (D_1=[3,9)) SAT, Sigma_2 (D_2=[9,27)) SAT,
  **Sigma_3 (D_3=[27,81)) UNSAT**. Verified by CP-SAT (`singleblock.py`, 11 s),
  independently by Glucose 4.2 with a pure boolean transitivity encoding
  (`singleblock_xcheck.py`, 0.2 s), and at **protocol grade** by Cadical103 with DRUP
  proof logging plus an independent hand-written RUP+deletion proof checker
  (`dratcert.py`; checker passes positive AND negative control tests): the proof has
  only **738 lines** (735 RUP additions), ending in the empty clause
  (`sigma3_base3.cnf`, `sigma3_base3.drat`). A 735-step resolution proof over a
  1431-variable encoding is short enough that a human-readable proof is plausibly
  extractable — flagged as next step.
* Base 4: Sigma_1, Sigma_2 SAT; **Sigma_3 (D_3=[64,256)) UNSAT** (CP-SAT 288 s;
  Glucose 14 s).
* With Lemma Sc: every Sigma_j, j >= 3, is UNSAT in bases 3 and 4 => **no contiguous
  base-3 or base-4 block ordering of N avoids monotone 4-APs**, regardless of the
  internal orders. Combined with Theorem A (base 2): contiguity is dead in bases
  2, 3, 4.

Coupled version (base 3, blocks D_0..D_4 with R3 included, full AP set on [1..N]):
SAT for N = 86, **UNSAT for N = 87** (death just after D_4 = [81, 243) opens);
verified by CP-SAT and Glucose; an *irreducible* core of 245 APs was extracted and
re-verified UNSAT by CP-SAT as a third check (`muscert.py`,
`mus_core_base3_N87.txt`). Note 87 kills earlier than the decoupled Sigma_3 (whose
constraints reach values up to 107); the coupling (R3) accelerates death.

Structure of the infeasibility (`dissect_D3.py`, `dissect_D3.out`): inside Sigma_3
(base 3) split the constraints into families {4AP, g3bot, g3top, F1, F2} (459 internal
4-APs; 243 + 243 bottom-/top-grounded 3-APs with overlap 122; 290 F1; 64 F2). **Every
proper sub-conjunction of the five families is SAT; only all five together are
UNSAT**, with an irreducible core of 140 constraints (65 4AP + 28 F1 + 34 F2 +
3 g3bot + 10 g3top). The death is genuinely global — no two- or three-ingredient human
proof exists at the family level; any human proof must couple internal 4-AP-freeness
with both edge disciplines and both forced-pair families.

Bases 5, 6, 8 decoupled probes: D_1 SAT for b = 5, 8 (pre-restart run); the D_2+
solves were deferred at cutoff (heavy machine contention from parallel routes; script:
`restprobes.py`). The b = 3, 4 results already establish the qualitative point;
extending to all b (or finding a base where Sigma_j stays SAT forever) is an explicit
next step (Sec. 7).

### 4.4 Near-contiguity: 2-separated dyadic blocks

By Theorem A(c) nothing is forced at separation 2, and this regime is exactly
"contiguous base-4 = paired dyadic blocks" *weakened* (base-4 contiguity is strictly
stronger: it also separates the two blocks inside each pair from the neighbouring
pair). Since contiguous base-4 is dead (Theorem B) while nothing forces death at
separation 2, the boundary of the obstruction lies between these two disciplines.
CP-SAT feasibility of 2-separated dyadic orderings of [1..N]
(`satprobe.probe_separated`; the separation discipline is re-verified on every
returned model; an encoding gap found mid-session — chain constraints only covering
even offsets — was fixed before any result was recorded): probe running at session
cutoff for N = 127, 255; verdicts go to NOTES.md.

**Why no Theorem-B-style local kill exists for separation 2 (proved).** The analog of
Sigma_j for 2-separation lives on the window U_m = B_m ∪ B_{m+1} = [2^m, 2^{m+2})
(window order fully free; values < 2^{m-1} forced before, values >= 2^{m+3} forced
after). But its forced-pair families are *empty*: F1 needs u+2d >= 2^{m+3} with
u+d < 2^{m+2}, yet u+2d = (u+d) + d < 2^{m+2} + 2^{m+2} = 2^{m+3}; F2 needs
u - d < 2^{m-1} with u >= 2^m, so d > 2^{m-1} and u-2d < 0. So the decoupled window
system is only "internal 4-APs + grounded edge 3-APs", and it is SAT (machine: U_3,
U_4 at least, `sep2window.py`). Consequence: any impossibility proof for 2-separated
dyadic orderings must couple at least two overlapping windows (U_m ∩ U_{m+1} =
B_{m+1} is shared) — the single-scale mechanism that killed contiguity (Theorem B)
provably cannot kill separation 2. This sharpens deliverable 3: contiguity dies
locally; 2-separation can only die globally, if at all. Displacement caveat (cross-route):
2-separation caps pos(v) <= 8v, a linear profile with C = 8; CORE Thm 12 + R4
empirics make even feasible finite stretches unlikely to extend to N. Growing
separation g(m) -> infinity evades both this cap and Theorem A — that is where any
surviving blocked design must live.

## 5. Constructions and diagnoses (deliverable 2)

All in `orderings.py` (16) + `promo_rec.py` and floor-variants (10). Each is a key
function; the induced ordering sorts N by key. **Order type omega** for all:
block-graded keys have finite grades and each value is preceded only by values of
<= its grade (<= C v of them, C <= 4); the promotion family has key rho with rho
injective and rho(v) >= v, so #{w : rho(w) < rho(v)} < rho(v) < infinity. Bijectivity:
sorting an injective key of type omega enumerates every value exactly once (CORE.md
Lemma 1). Restrictions to [1..M] verified to be permutations of [1..M] for M = 10^4.

Verdicts (restriction to [1..10^4]; "min" = minimal max-term of a witness):

| # | ordering (grade; internal) | verdict | min | failure mode |
|---|---|---|---|---|
| O1 | dyadic blocks; sigma | FAILS | 7 | Theorem A + F-pairs: (1,3,5,7) blocks (0,1,2,2), pair (5,7) sigma-increasing |
| O2 | base-4 blocks; sigma | FAILS | 7 | (1,3,5,7): both same-block pairs sigma-increasing (R3-mode); also F1 (2,7,12,17) |
| O3 | base-4 blocks; 3 chunks reversed, sigma chunks | FAILS | 9 | chunk reversal assembles **decreasing** APs: (6,7,8,9) dec — cross-chunk pairs auto-decrease, sigma inverts (9,8) |
| O4 | base-3 blocks; tau natural | FAILS | 4 | (1,2,3,4): tau leaves both same-block pairs increasing (R3-mode) |
| O4b | base-3 blocks; tau, priorities flipped in odd blocks | FAILS | 11 | grounded 3-AP: (8;9,10,11) — D_2's natural priorities make (9,10,11) increasing (R1-mode) |
| O5 | base-3 blocks; 6 chunks (len 3^{j-1}) reversed, tau | FAILS | 6 | chunk length divides in-block d: (9,12,15,18) all-cross-chunk => forced decreasing (R0-mode); degenerate reversal at j=1 |
| O6 (C=1,2,3) | v2-promotion capped: key n 2^{min(v2,C)} | FAILS | 7 | case-(i) APs untouched: (1,3,5,7) all-odd, value order (P-mode / Prop B blind spot) |
| O6w | windowed capped promotion + sigma | FAILS | 11 | same blind spot one scale up: (5,7,9,11) |
| O7 | dyadic; Thue-Morse split; sigma | FAILS | 7 | L3: TM signs are carry statistics, the split does not separate (1,3,5,7) usefully |
| O7b | base-3; s3-parity split; tau | FAILS | 10 | same: (1,4,7,10) |
| O8 | negabinary length blocks; lex | FAILS | 7 | length-grading has the contiguity disease: (4,5,6,7) lengths (3,3,5,5), both pairs lex-increasing |
| O8r | negabinary length; reverse lex | FAILS | 7 | same at (4,5,6,7) |
| O9 | dyadic; boustrophedon (alternate-bit complement) | FAILS | 11 | (1,6,11,16) among first killers — the Theorem A family survives the in-block scramble |
| O9g | dyadic; reflected-Gray zigzag | FAILS | 4 | Gray order starts 0,1,3,2,...: (1,2,3,4) increasing |
| OM.h (h(s)=2s,3s,s+1,s^2,2^s-1) | recursive v2-promotion rho(2^s u)=2^{h(s)}(2 rho(ceil(u/2))-1) | FAILS | 4 | promotion inheritance: odd u recurses through ceil(u/2) and inherits the even's promotion — (1,2,3,4) with rho=(1,4,7,16) monotone |
| OMfloor.h (5 variants) | same with floor(u/2) recursion | FAILS | 4-12 | best: h=2s dies at (3,6,9,12): rho(9)=33 inherits rho(4)=16 — inheritance one level deeper; (1,6,11,16) reappears |

Structural failure taxonomy (each mode is now *understood*, not anecdotal):

* **A-mode** (Theorem A): any base-2-graded contiguous design is killed by
  2^M (1,6,11,16) outright.
* **R1/R2/R3-modes** (Lemma R): sigma/tau internals satisfy R0+R1 (sigma has no
  monotone 3-APs at all; tau no 4-APs) but were never designed for the *pair*
  conditions R2/R3; and by Theorem B no redesign of internals can satisfy all of
  R0-R3 anyway.
* **D-mode**: chunk-reversal repairs of R2/R3 create decreasing APs out of
  auto-decreasing cross-chunk pairs plus one inverted in-chunk pair — orientation
  whack-a-mole that Theorem B certifies to be unwinnable inside contiguous blocks.
* **P-mode**: promotion schemes break exactly the L1-cases (ii)/(iii) they aim at
  *only if* placements track values within a factor < ~2 (uniform drift); the
  recursive structure needed for case (i) (a self-similar copy of the whole problem
  inside each v2-class) forces unbounded, non-uniform drift ("promotion
  inheritance"), which re-opens cases (ii)/(iii). Capped promotion (bounded drift)
  is blocked by Proposition B instead. This dichotomy is the precise sense in which
  "sigma-repair by delay schedules" fails.

Checker validation: `orderings.crossvalidate()` — 400 random-permutation verdicts and
150 exact witness-set comparisons against brute force, plus every construction at
M = 40, 90, 160 against `apcheck.has_monotone_kap_pos`. OK.

## 6. What this rules out, in one paragraph

Every ordering of N in which "scale" (any base-b top digit, b = 2, 3, 4; also
negabinary length) is weakly respected by position — eventually contiguous blocks,
with arbitrary internal rearrangement — contains a monotone 4-AP. The parity/base-3
recursions are not "almost omega" objects awaiting a clever finite delay schedule: the
sigma mechanism is non-omega *per se* (Prop B), bounded promotion inherits its blind
spot, recursive promotion destroys its own cross-class inequality, and contiguous
blocking of any tested base dies by Theorem A/B. The surviving space for R3-style
NO-witnesses is: scale-respecting only with **separation >= 2 and unboundedly growing
interleave depth** (superlinear displacement — independently mandated by CORE Thm 12 +
R4 empirics), with internals that are tau-like on 3-adic (not 2-adic) data.

## 7. Sharpest surviving idea and next steps

**Sharpest surviving idea — "omega-repair of tau".** tau (Lemma T) breaks every 4-AP
through the level-v3(d) digit cycle a -> a+delta -> a+2delta -> a: every 4-AP
*automatically* carries 1 or 2 pr_v-descents among its three adjacent pairs, in both
orientations. An ordering need only *retain enough* of tau's comparisons: for each
4-AP, one adjacent pair whose tau-comparison (at level v3(d)) is a descent must keep
its tau-orientation. The analog of Proposition B for tau says keeping *all* of them is
non-omega; but unlike sigma (two classes, one mechanism), tau has 6 priority choices
per level and, on average, 2 usable descents per orientation — slack sigma never had.
Concretely: find a "level-local repair schedule" — finite windows W_1 ⊂ W_2 ⊂ ...
exhausting N, tau-comparisons preserved inside windows at low levels and overridden
across windows only at levels where the overridden pairs' APs retain another in-window
descent. The machine side is ready: Lemma R generalizes to any window discipline, and
`probe_separated` extends to growing g(m). Next steps, ordered:

1. Decide 2-separated dyadic (and base-3 adjacent-interleave) feasibility at
   N = 127-511 (probe running); if SAT, mine the models for 3-adic structure; if
   UNSAT, extract a core — that would *prove* bounded-lag death, matching
   route-R1's lag-2 result, and force g(m) -> infinity designs.
2. Extend Theorem B's base sweep (b = 5, 6, 8 decoupled probes; are ALL bases dead?);
   a proof for general b from the F1+F2+edge system, guided by the Farkas/LP dual of
   the 140-core, would subsume Theorem A and be a lemma of independent value for 196.
3. Formalize the tau-repair schedule question and probe it by SAT on windows
   [1..3^k] with growing overrides.
4. Cross-route: R1's cut-set {8, 26, 80} = {3^j - 1} matches the base-3 block tops
   found lethal here; unify the two death mechanisms (likely the same finite
   obstruction viewed twice).

## 8. File index

* `lemmas_check.py` — L1, L2, L3, Theorem A(a), S, T, Prop B family; all pass.
* `orderings.py` — construction framework, 16 orderings, checker + cross-validation,
  diagnosis; run output summarized in Sec. 5.
* `promo_rec.py` — recursive promotion family (floor variants run inline; NOTES.md).
* `satprobe.py` — CP-SAT probes: contiguous base-b (coupled) and g-separated dyadic
  (fixed encoding, model-verified separation).
* `singleblock.py` / `singleblock_xcheck.py` — decoupled Sigma_j systems, CP-SAT + pysat.
* `muscert.py`, `mus_core_base3_N87.txt` — coupled base-3 N=87 UNSAT + 245-AP
  irreducible core, triple-checked.
* `dissect_D3.py`, `dissect_D3.out` — family dissection of Sigma_3; 140-constraint core.
* `lemmaR_check.py` — Lemma R case-rule validation (bases 3, 4, 5).
* `restprobes.py` — restarted background probes (bases 5/6/8; 2-separated dyadic).
* `dratcert.py`, `sigma3_base3.cnf`, `sigma3_base3.drat` (and base-4 analogues) —
  DIMACS + DRUP proof + independent RUP verification for Theorem B.
* `sep2window.py` — decoupled window systems for 2-separated dyadic orderings
  (forced families provably empty; windows SAT).
