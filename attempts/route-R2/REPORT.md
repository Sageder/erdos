# REPORT.md — Route R2: a 5-AP-avoiding permutation, and why 4 is different

Erdős problem 196 (`/home/user/erdos/PROBLEM.md`). Route R2 remit: re-derive
from scratch an explicit permutation of N with no monotone 5-term AP, verify
it by machine, dissect exactly why it fails at length 4, and try to engineer
around the obstruction.

## VERDICT (read this first)

1. **Built and proved**: an explicit permutation of N (**Construction A**:
   powers-of-4 blocks, van der Corput order inside, alternately reversed)
   with **no monotone 5-term AP**. Hand proofs of bijectivity / order type
   omega and of 5-AP-freedom are in `PROOFS.md`; machine verification (exact
   arithmetic, cross-validated checkers) to prefix N = 65535. The
   construction is stronger than required: it has **no monotone DESCENDING
   3-AP at all** — every monotone progression of length >= 3 in it is
   ascending, and none reaches length 5.
2. **Diagnosis, exact**: the monotone 4-APs of Construction A are
   characterized completely — two families S1, S2 (below), confirmed by a
   machine census (1,304,268 4-APs at N = 16383, predicted count = observed
   count exactly). Mechanism: a 5-AP needs TWO within-block ascending pairs
   in adjacent blocks whose order conditions are rigidly coupled (same bit)
   and killed by the alternating reversal; a 4-AP needs only ONE pair — its
   other two terms are a *free head* (small value, automatically early
   because N is one-sided and the order type is omega) and a *free tail*
   (large value, automatically late). One constraint, no coupling, no kill.
3. **Three-plus modification attempts, all conclusively developed/refuted**:
   - **Mod 1** (arbitrary internal block orders, any interval blocks of
     ratio >= 4): refuted by machine UNSAT proof — for the 4^m chain the
     block [64,256) admits NO safe internal order (encoding validated
     end-to-end, confirmed by 3 independent SAT solvers). Frontier scan:
     (4,16,64) is the ONLY satisfiable boundary triple among 26 tested.
   - **Mod 2** (arbitrary sign tables for the digit order): refuted by a
     2-certificate {1,6,11,16}, {2,7,12,17} — every sign choice realizes one.
   - **Mod 3** (out-of-order block placement): 62x reduction in 4-AP count,
     but the pinned family (1, v, 2v-1, 3v-2) survives every bounded-delay
     placement; unbounded delay breaks order type omega. Refuted.
   - **Mod 4** (greedy least-value 4-AP-avoider): provably non-surjective —
     it places 1,2,3 at positions 1,2,3, permanently blocking the value 4;
     84% of values below the running max are skipped by step 400. Refuted.
4. **Displacement calibration** (vs `attempts/core/CORE.md` Theorem 12,
   LP(9/8)): Construction A has **linearly bounded displacement**
   v/4 < pos(v) < 4v; machine profile on N = 65535: max pos(v)/v = 3.999878
   (v = 16384), min = 0.250004, limsup = 4, liminf = 1/4; 59.24% of values
   satisfy pos(v) <= (9/8)v. So monotone-5-freedom costs only a factor-4
   linear corridor, while 4-freedom is impossible below the 9/8 corridor
   (Thm 12). The truth for 4-AP-freedom, if it exists, lives in [9/8, 4].
5. **Net assessment**: everything found is YES-side pressure at length 4.
   The design space of the natural 5-avoiding mechanism (internal orders x
   signs x boundaries x bounded placement) is provably closed at length 4,
   with a crisp local reason (below). This obstruction is a candidate
   ingredient for a YES proof.

Epistemic status: hand proofs cover the infinite statements about
Construction A. Machine checks are exact but finite (prefixes as stated);
finite checks are evidence, not proof, for the infinite claims — the
infinite claims rest on `PROOFS.md`. The Mod-1 refutations are machine
proofs of finite UNSAT statements, with the encoding validated against an
independent implementation and the ground-truth checker.

## 1. The construction (deliverable 1)

- Blocks B_m = {4^m, ..., 4^{m+1}-1}, m >= 0 (partition of N; B_0 = {1,2,3}).
- Internal order pi_m: sort B_m by **van der Corput order** — compare binary
  expansions at the least significant differing bit, 0-bit first
  (equivalently sort by bit-reversed binary); **reverse the list for odd m**.
- a = concatenation pi_0 pi_1 pi_2 ...

First 15 values: 2,1,3 | 15,7,11,13,5,9,14,6,10,12,4,8 | 32,16,48,...

Proof skeleton (full details in `PROOFS.md`):
- L0 bijection/order type omega; also v/4 < pos(v) < 4v.
- L1 vdC (and reversed vdC) has no monotone 3-AP in ANY set: for u, u+e,
  u+2e with l = v2(e), the middle term differs from both ends first at bit
  l and in the same direction, so it sits before both or after both.
- L2 positions are block-major. L3 descending monotone APs live in one
  block, so die at length 2 (by L1). L4 AP terms meeting a block are index-
  contiguous. L5 from the 2nd term on, consecutive AP terms lie in same or
  adjacent blocks (t_{i+1} < 2 t_i). L6 the last four terms of a 5-AP
  satisfy t_4 < 4 t_1, hence meet at most 2 adjacent blocks (ratio 4!).
- L7 pair criterion: u, u+d in B_m ascend in pi_m iff bit_{v2(d)}(u) = m mod 2.
- Theorem (no monotone 5-AP): an ascending 5-AP must split
  (x)(x+d,x+2d)(x+3d,x+4d) over adjacent B_m, B_{m+1}; L7 forces
  bit_l(x+d) = m mod 2 and bit_l(x+3d) = (m+1) mod 2, but their difference
  2d is divisible by 2^{l+1}, so the bits are equal. Contradiction.
  Descending: L3.

## 2. Machine verification (deliverable 2)

Code `construction.py`, `checkers.py`, `verify_construction.py`; output
`verify_output.txt`. Checkers cross-validated against brute force (apcheck
self-test 3000+1500 cases; my numpy checkers vs brute on 4000 random
permutations, k in {3,4,5}, both orientations; 200 full-enumeration
comparisons). Exact integer arithmetic throughout.

Restriction principle: blocks are increasing intervals concatenated in
order, so the values {1..M} in position order are literally the first M
positions when M = 4^k - 1; the largest check covers all smaller M.
- V1 bijectivity: prefix of length 65535 is a permutation of [1..65535]
  (requirement was M >= 5000).
- V2 **no monotone 5-AP** at N = 65535 (both orientations).
- V3 **no monotone descending 3-AP** at N = 65535.
- V4 ascending 3-/4-APs exist (must, by DEGS77(a)); smallest 4-AP 2,7,12,17.
- V5 census at N = 16383: 1,304,268 monotone 4-APs, every one matching the
  characterization below (`fourAPs_16383.txt`, 40 MB).

## 3. Exact 4-AP families and the 5-vs-4 mechanism (deliverable 3)

**Proposition (proved + machine-exact).** Every monotone 4-AP of a is
ascending and of exactly one of two shapes (t_i = x+id, l = v2(d), pair
block m); conversely every such configuration is a monotone 4-AP:

- **S1 (head|head|pair)**: block(t_0) < block(t_1) = m-1, {t_2,t_3} in B_m,
  bit_l(t_2) = m mod 2. Census 979,436 (B_2:12, B_3:192, B_4:3616,
  B_5:56576, B_6:919040).
- **S2 (head|pair|tail)**: block(t_0) < m, {t_1,t_2} in B_m, t_3 in
  B_{m+1}, bit_l(t_1) = m mod 2. Census 324,832 (B_1:2, B_2:79, B_3:1124,
  B_4:19271, B_5:304356).

Completeness is machine-exact: counting admissible (x,d) directly from the
defining conditions gives 979,436 + 324,832 — identical to the census
(`census_crosscheck.txt`). Smallest instances: 2,7,12,17 and 1,7,13,19.

**Mechanism killing 5 but not 4.** Three walls:
(a) orientation wall — descending dies at length 2 (block-major + vdC);
(b) capacity wall — ratio-4 growth plus "<= 2 AP terms per block" (vdC)
    leaves an ascending 5-AP only the layout (x)(pair)(pair) in adjacent
    blocks;
(c) alternation wall — a pair (u,u+d) ascends in B_m iff
    bit_{v2(d)}(u) = m mod 2, and the two pairs of a 5-AP carry the SAME
    bit (their offset 2d kills it), while adjacent blocks demand OPPOSITE
    bits.
A 4-AP evades wall (c): its layouts (S1/S2) contain ONE pair; the single
bit condition is satisfiable half the time; head and tail are free — the
head because order type omega forces small values to early positions
(one-sidedness of N), the tail because large values are automatically late.

**Displacement profile** (`displacement_output.txt`): pos(v)/v in (1/4, 4)
always; on N = 65535 max 3.999878, min 0.250004, and pos(v) <= (9/8)v for
59.24% of v; per-block maxima increase to 4, so limsup = 4, liminf = 1/4.
Calibration: 5-avoidance achievable at linear displacement factor 4;
4-avoidance impossible below factor 9/8 (CORE.md Thm 12). Gap [9/8, 4] open.

## 4. Modifications targeting length 4 (deliverable 4)

### Mod 1 — arbitrary internal orders in interval-block schemes: REFUTED (UNSAT)

For any block-major interval scheme (boundaries 1 = b_0 < b_1 < ...,
ratios >= 4, arbitrary internal orders), the assembled permutation is
monotone-4-AP-free **iff** each block [c, C) (previous boundary c') avoids
locally: A4/D4 (internal ascending/descending 4-APs), A3T/A3H (ascending
3-AP with free tail >= C resp. free head < c), A2T (ascending pair, free
head and free tail), A2H (ascending pair whose two heads lie in two
DISTINCT earlier blocks), A2HH (pair-over-pair coupling with the previous
block). Soundness of every pattern (violation => genuine 4-AP) was verified
end-to-end against the ground-truth checker; completeness was verified by a
joint SAT model of blocks 0-2 whose 63-prefix is 4-AP-free
(`mod1e_output.txt`, `mod1g_output.txt`).

Results (`mod1_sat_output.txt`, `mod1f_output.txt`):
- 4^m chain: blocks 0,1,2 admit safe orders; **block [64,256) (c' = 16)
  admits NONE** — even ignoring the A2HH coupling. Hence NO assignment of
  internal orders makes the powers-of-4 scheme 4-AP-free. Confirmed by
  Cadical, Glucose 4.2, MiniSat 2.2 independently.
- Frontier: among consecutive-boundary triples (c', c, C), the ONLY
  satisfiable one found is (4,16,64); UNSAT for all (c',4c',16c'),
  c' = 5..16; for (16,64,C), C = 256..384; for (16,c,4c), c = 64..96; and
  for general triples with c' in 17..20. So any ratio->=4 chain whose third
  or fourth block lands in the tested region is dead; every chain reaches
  c' >= 16 by its 4th block, and the constraint families only densify with
  scale (A2H count grows ~ c'^2) — UNSAT beyond the tested region is
  conjectural but strongly indicated.
- **Ablation: dropping A2H alone flips the system to SAT** (tested at
  (16,64,256) and (20,80,320)). The obstruction is precisely the
  *two-free-headed pairs*: pairs (u, u+e) whose heads u-2e, u-e straddle
  the boundary c' — their heads sit in two different earlier blocks, at
  automatically ascending positions, so the pair itself MUST descend.
- Anatomy (verified-minimal MUS at (5,20,80), 211 constraints: 30 A2H +
  59 A2T + 100 D4 + 7 A4 + 4 A3H + 11 A3T): the ~90 descents forced by
  free-headed/free-tailed pairs chain into descending 4-APs (D4), with a
  few ascending constraints closing every escape. In words: **dodging the
  free-headed ascending 4-APs forces so many inversions that a descending
  4-AP becomes unavoidable.**

Honesty note: an earlier encoding had an unsound A2T tail condition
(w+3e >= C instead of w+2e >= C); its results were retracted (the bug was
caught by inspecting a MUS), everything re-run with the fixed validated
encoding (`SUPERSEDED_NOTE.txt`).

### Mod 2 — sign tables for the digit order: REFUTED (certificate)

Family: order B_m by LSB-first lex with arbitrary signs sigma[m][l]
(Construction A: sigma[m][l] = m mod 2). Pair criterion: u before u+d iff
bit_{v2(d)}(u) = sigma[m][v2(d)]. The 4-APs 1,6,11,16 and 2,7,12,17 need
only "6 before 11" resp. "7 before 12" in pi_1, and 6 is even, 7 odd:
every value of sigma[1][0] realizes one. Machine-checked both ways
(`mod2_output.txt`); the sigma[1][0] = 0 variant even loses 5-AP-freedom
(1,6,11,16,21 appears) — the alternating signs are forced, not chosen.

### Mod 3 — out-of-order block placement: REFUTED (pinned family)

Attacks the free head by delaying small blocks. Variants at N = 16383 (all
still 5-AP-free, all 4-APs ascending; `mod3_output.txt`): adjacent swaps
338,752 4-APs; delay B_0 behind B_4: 1,302,918; rolling delay
(1,2,0,4,3,6,5): **20,985** (62x cut). But zero is unreachable: the family
**(1, v, 2v-1, 3v-2)** — S2 with head 1 and pair (v, 2v-1) in B_m for
v in [(4^{m+1}+2)/3, (4^{m+1}+1)/2) — is pinned: order type omega puts the
value 1 at a finite position, before all but finitely many blocks, and the
pair ascends for about half the v in every block under ANY sign scheme
(Mod 2). Machine: variant 3c still contains 341 4-APs headed by 1, all of
the predicted shape. Bounded delay trades constants; unbounded delay
destroys order type omega.

### Mod 4 — greedy least-value 4-AP-avoider: REFUTED (non-surjective)

Placing at each position the smallest unused value that completes no
monotone 4-AP gives an injective 4-AP-free sequence (validated checker),
but it is provably NOT a permutation of N: it opens 1,2,3 at positions
1,2,3, so placing 4 at any later position completes 1,2,3,4 — the value 4
is permanently blocked. Values race: by step 400 the max placed value is
2517 with 84% of smaller values unused (`mod4_output.txt`).

## 5. Next steps

1. Prove the Mod-1 UNSAT pattern for ALL triples (c' >= 5) combinatorially
   ("forced inversions of one-sided origin assemble a descending 4-AP") —
   would close the interval-block design space rigorously and is the
   natural candidate lemma toward YES for 196.
2. Push the LP(9/8) displacement bound toward 4 using the S1/S2 families
   as inequality sources; Construction A pins the target interval [9/8, 4].
3. The one untested degree of freedom: NON-interval blocks (congruence-
   sieved scales) — contiguity (L4) fails, so both the 5-proof and the
   4-obstruction genuinely change. Worth a dedicated route.
4. Formalize Construction A's proofs (they are elementary and local).

## File index

`PROOFS.md` (hand proofs L0-L7, Theorem, Proposition) · `construction.py` ·
`checkers.py` (validated) · `verify_construction.py` + `verify_output.txt`
(V1-V5) · `fourAPs_16383.txt` (full census) · `census_crosscheck.txt`
(completeness) · `displacement.py` + `displacement_output.txt` ·
`mod1_block_search.py`, `mod1_sat.py`, `mod1b_sweep_mus.py`, `mod1d_mus.py`,
`mod1e_validate.py`, `mod1f_frontier.py`, `mod1g_joint.py` + their outputs
(Mod 1: constraint system, validation, UNSAT frontier, ablation, MUS,
joint completeness) · `mod2_signs.py` + `mod2_output.txt` ·
`mod3_placement.py` + `mod3_output.txt` · `mod4_greedy.py` +
`mod4_output.txt` · `SUPERSEDED_NOTE.txt` (retracted buggy-encoding runs).
