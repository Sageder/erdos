# STATUS.md — consolidated status of routes R2, R4, R8, R9

Erdős problem 196 (statement of record: `/home/user/erdos/PROBLEM.md`).
Prepared 2026-07-28 by the consolidation agent. Scope: read the four routes' code,
logs and partial reports; re-run everything cheap and load-bearing with
**independent re-implementations**; separate PROVED from MEASURED from UNVERIFIED.

All my code and raw outputs are in this directory. Nothing outside
`attempts/consolidated/` was modified.

---

## 0. Verification method and global ledger

Every number I report as MEASURED was produced by code written here from the
mathematical specification, not by re-running the routes' own binaries.

| my tool | what it is | validated against |
|---|---|---|
| `verify_R2.py` | Construction A from the prose spec + numpy monotone-k-AP checker | `experiments/apcheck.py` brute-force **and** position checkers: 400 random permutations × k ∈ {3,4,5}, 0 mismatches; plus the N=63 construction prefix |
| `verify_R2_S1S2.py` | independent arithmetic predicate for R2's S1/S2 4-AP families | compared AP-by-AP against a position census over all (x,d), N=16383 |
| `tamedfs.c` | complete DFS over φ-bounded monotone-4-AP-free permutations (insertion tree, CORE Lemma 8) | reproduces the avoider counts 1,2,6,22,102,564,3336,22266,168864,1307470,11066766,101361722,949812334 and route R9's **total node counts bit-for-bit** |
| `tamedfs_k.c` | same for general AP length k | reproduces all k=4 results; reproduces R9's k=3 table (5,10,12,13,20,29 at C=1.5,2,2.5,3,4,6) |
| `seqdfs.c` | complete DFS over injective **sequences** a(1..N) with a(i) ≤ ⌊Ci⌋ (route R4's class Bp/"S") | reproduced level-by-level by a pure brute-force enumeration driven by `apcheck.has_monotone_kap_general` |
| `verify_witnesses.py` | re-checks every stored R4 avoider/survivor and R9's N=50 witness with `apcheck` | — |
| `verify_R8.py` | Theorem W and the mod-4 rate ladder, re-implemented from the prose | `apcheck` conventions |

Headline: **every claim I was able to re-run matched exactly**, including total
node counts of billion-node searches. I found no computational error in any of
the four routes. I found five documentation discrepancies (§6).

---

## 1. Route R2 — DEGS77(b) reconstruction ("Construction A")

Directory `attempts/route-R2/`. REPORT.md **is** present and complete (14 kB);
the coordinator's note that R2 was interrupted is out of date.

### PROVED

`route-R2/PROOFS.md` contains full hand proofs; I audited them line by line and
found them **sound**. They are the same statements as CORE.md Theorem 21.

*Construction A.* Blocks `B_m = [4^m, 4^{m+1})` (so `|B_m| = 3·4^m`, `B_0={1,2,3}`)
listed one after another in increasing m; each block sorted in **van der Corput
order** (compare binary expansions at the least significant differing bit, 0 first),
**reversed when m is odd**. First 15 values: `2,1,3 | 15,7,11,13,5,9,14,6,10,12,4,8`.

Proof skeleton (each step re-checked):
- **L0** blocks are finite and partition ℕ and are listed in order ⇒ bijection of
  order type ω; and v, pos(v) lie in the *same* window `[4^m,4^{m+1})` ⇒
  **v/4 < pos(v) < 4v**.
- **L1** vdC order (and its reverse) contains no monotone 3-AP *in any set*: for
  u, u+e, u+2e with l = v₂(e), the middle term differs from *both* ends first at
  bit l and in the same direction, so it is extremal, never in the middle.
- **L2** positions are block-major. **L3** hence a monotone *descending* AP lives
  in one block and dies at length 2 (blocks weakly decrease along a descending
  value sequence and weakly increase along positions ⇒ all terms in one block).
- **L4** AP terms meeting a block are index-contiguous. **L5** t_{i+1} < 2t_i for
  i ≥ 1 ⇒ consecutive terms from the 2nd on lie in the same or adjacent blocks.
- **L6** t₄ = 4t₁ − 3x < 4t₁, so t₁..t₄ of a 5-AP meet at most **2** blocks (ratio 4).
- **L7 pair criterion** for u, u+d ∈ B_m with l = v₂(d):
  **u precedes u+d in π_m ⟺ bit_l(u) = m mod 2.**
- **Theorem.** No monotone 5-AP. Descending: L3. Ascending: L1+L4 give ≤2 terms
  per block, L6 gives ≤2 blocks for t₁..t₄, so the split is forced to
  {t₁,t₂}⊂B_m, {t₃,t₄}⊂B_{m+1}; L7 demands bit_l(t₁)=m mod 2 and
  bit_l(t₃)=(m+1) mod 2, but t₃−t₁ = 2d ≡ 0 (mod 2^{l+1}) forces the bits equal. ∎
- **Proposition.** Every monotone 4-AP of a is ascending, of exactly one of two
  shapes S1 (head|head|pair) or S2 (head|pair|tail), with an explicit bit condition.

### MEASURED (independent re-implementation, `verify_R2.py`, `verify_R2.out`)

This answers the coordinator's specific question. Requirement was M ≥ 5000;
I verified to **M = 65535**.

| N | bijective | v & pos(v) in same window | monotone 5-AP | monotone descending 3-AP | smallest monotone 4-AP | max pos(v)/v | min pos(v)/v |
|---:|---|---|---|---|---|---:|---:|
| 255 | ✓ | ✓ | **none** | **none** | (2,7,12,17) | 3.968750 (v=64) | 0.250980 |
| 1023 | ✓ | ✓ | **none** | **none** | (2,7,12,17) | 3.968750 | 0.250980 |
| 4095 | ✓ | ✓ | **none** | **none** | (2,7,12,17) | 3.998047 (v=1024) | 0.250061 |
| 16383 | ✓ | ✓ | **none** | **none** | (2,7,12,17) | 3.998047 | 0.250061 |
| 65535 | ✓ | ✓ | **none** | **none** | (2,7,12,17) | **3.999878** (v=16384) | 0.250004 |

Because blocks are increasing intervals concatenated in order, the length-(4^k−1)
prefix *is* the value-restriction to [1..4^k−1]; and value-restriction to any
smaller M is a restriction of that, so 5-AP-freeness holds for every M ≤ 65535.
Order type ω is structural (finite blocks, listed in order) and is witnessed by
the window property, which I checked for every v ≤ 65535.

4-AP census at N = 16383: **1,304,268 monotone 4-APs, all increasing, 0 decreasing**
— matching R2's reported count exactly. Independently classifying every (x,d) by
R2's *arithmetic* S1/S2 predicate gives S1 = 979,436, S2 = 324,832, overlap 0,
total 1,304,268, and the predicate agrees with the position census
**AP-by-AP with 0 mismatches**. R2's Proposition is therefore confirmed as an
exact characterisation, not just a count match. (3-AP count at N=16383:
14,397,932 increasing, 0 decreasing.)

**Displacement calibration (the key datum).** `pos(v)/v ∈ (1/4, 4)` always;
per-block maxima increase to 4, so **limsup pos(v)/v = 4, liminf = 1/4**, and
`pos(v) ≤ (9/8)v` for 59.24 % of v ≤ 65535 (matching R2's 59.24 %).
Consequence, and it is a **theorem**:

> For the k = 5 problem, the extinction level of the profile family
> `pos(v) ≤ ⌊Cv⌋` is **N\*₅(C) = +∞ for every C ≥ 4**, because the value
> restrictions of Construction A are 5-AP-free permutations of [1..N] with
> max pos(v)/v < 4 for every N.

This is the calibration the whole displacement programme has been missing (R9
listed it as its own next-step #3). See §5.

### UNVERIFIED

- **Mod 1** (arbitrary internal block orders in interval-block schemes): the UNSAT
  proofs — block [64,256) admits no safe internal order; the frontier scan over 26
  boundary triples with (4,16,64) the only satisfiable one; the A2H ablation; the
  211-constraint MUS at (5,20,80). Three solvers (CaDiCaL, Glucose 4.2, MiniSat 2.2)
  reportedly agree, the encoding was validated end-to-end against the ground-truth
  checker, and an earlier buggy A2T condition was caught and retracted
  (`SUPERSEDED_NOTE.txt`). **I did not re-run any of it.** Note R2 itself flags the
  region beyond the tested triples as *conjectural*.
- **Mod 3** counts (338,752 / 1,302,918 / 20,985 / 341 monotone 4-APs under various
  out-of-order block placements). Not re-run.
- Mod 2 and Mod 4 I re-checked **by hand**, both correct:
  Mod 2 — 6,11 ∈ B₁ with d = 5, v₂(5)=0, bit₀(6)=0 and bit₀(7)=1, so either value
  of σ[1][0] realises one of the 4-APs (1,6,11,16), (2,7,12,17);
  Mod 4 — the greedy least-value avoider opens 1,2,3 at positions 1,2,3, after which
  placing 4 anywhere completes the increasing 4-AP (1,2,3,4): value 4 is permanently
  blocked, so the greedy sequence is not surjective.

### VERDICT

**Fully successful as a diagnostic route; no path to 196.** The deliverable — an
explicit, independently re-derived and machine-verified 5-AP-free permutation of ℕ
with a complete structure theorem for its 4-APs — is solid and is now the project's
single most useful calibration object. The route's own conclusion (the length-5
mechanism is a **two-pair** parity argument, and four terms cannot supply two pairs)
is already folded into CORE.md as Remarks 22/23/25 and is corroborated by R1's
certificates. The engineering-around attempts are negative results of unequal
certification strength: Mod 2 and Mod 4 are airtight and trivial; Mod 3 is a
correct pinned-family argument ((1, v, 2v−1, 3v−2) is a genuine AP with step v−1,
and order type ω pins the value 1 at a finite position); Mod 1 is the substantial
one and rests entirely on unreproduced SAT.

---

## 2. Route R4 — displacement-bounded avoider search

Directory `attempts/route-R4/`. **No REPORT.md exists.** The route's results live
in `results/thresholds.tsv`, `results/frontier.jsonl`, the `logs_*_sat.txt` files
and a NOTES.md entry. This section is R4's report of record.

### The class taxonomy (this is R4's distinctive contribution)

From `engine.py`'s header, with the logical status of each class spelled out —
R4 got this right and it is the thing most worth carrying forward:

| class | constraint | does extinction at N give an **infinite** theorem? |
|---|---|---|
| **A** | pos(v) ≤ Cv for all v | **yes, via CORE Lemma 6** (König over the value-restriction tree) |
| **B** | a(i) ≤ Ci, object a permutation of [1..N] | **no** — neither value-restrictions nor position-prefixes of an infinite permutation inherit this; finite-board fact only |
| **C** | A and B jointly | only the A part survives to infinity |
| **D** | pos(v) ≤ 2v for v ≤ N/2 | via Lemma 6, for the prefix values |
| **S** (= Bp) | injective **sequence** a(1..N) of distinct positive integers with a(i) ≤ ⌊Ci⌋ | **yes, directly — no compactness needed.** The position prefix a(1..N) of any 4-AP-free permutation with a(i) ≤ Ci is exactly such an object. |

Class S is the only family in the whole project that yields infinite theorems
*without* a compactness step, and it constrains a NO-witness from the **position**
side, whereas everything else in CORE (Theorem 12, Remark 17, R9, R20's v log v)
constrains from the **value** side.

Note the one-directional nature, which R4 did not state and which matters:
S-*survival* at every N does **not** imply 196-NO, because an infinite ψ-bounded
branch of the prefix tree need not be surjective onto values (CORE Lemma 9 lets
you drop surjectivity onto *positions*, not onto *values*). So class S is a pure
YES-side constraint generator — which is exactly why it is worth mining: it is
immune to Remark 17(a)'s "∀φ" objection.

### PROVED (complete enumerations; all reproduced here)

Class S, `seqdfs.c`, cross-validated level-by-level by brute force through `apcheck`:

| C | level counts of the S-tree | extinct at |
|---|---|---|
| 1 | 1,1,1,0 | i = 4 |
| 5/4 | 1,1,1,1,1,0 | i = 6 |
| 4/3 | 1,1,2,3,5,9,15,23,35,28,20,24,12,14,19,13,2,0 | **i = 18** (whole tree: **227 nodes**) |
| 3/2 | alive at i = 34 (R4 witness, re-verified here) | not reached |

> **Theorem (R4, class S; verified three independent ways here).**
> There is no injective sequence a(1), …, a(18) of distinct positive integers with
> a(i) ≤ ⌊4i/3⌋ for all i and no monotone 4-term AP among its values.
> Hence **every monotone-4-AP-free permutation of ℕ has some position i ≤ 18 with
> a(i) > ⌊4i/3⌋** — equivalently some value v with pos(v) < (3/4)v.
> The certificate is a 227-node tree; it is essentially hand-checkable.

Class A thresholds (min N with no avoider), reproduced exactly by `tamedfs.c`:
C = 1 → 4, 3/2 → 15, 7/4 → 31, **15/8 → 37**. R4's SAT route obtained
15/8 independently (`logs_A158_sat.txt`: SAT at N=36, UNSAT at N=37).

Class C (both bounds) at C = 2: max SAT N = 49, UNSAT N = 50 and confirmed
through 56 (`logs_C2_sat.txt`). Finite-board statement only (see table above).

### MEASURED (witnesses, all re-verified here with `apcheck` — `verify_witnesses.out`)

Every one of the stored avoiders and every entry of every survivor population
is monotone-4-AP-free: **0 violations out of ~21 700 checked permutations.**

| file | largest N | max pos(v)/v | max a(i)/i | consequence |
|---|---:|---:|---:|---|
| `A_2_1.txt` | **56** | 2.0000 | 13 | ρ(56) ≤ 2 |
| `A_3_1.txt` | **75** | 3.0000 | 27 | ρ(75) ≤ 3 (a **plain** witness, stronger than the asym N=74 cited in CORE) |
| `A_5_2_ceil.txt` | 70 | 3.0000 | 10 | — |
| `A_15_8.txt` | 36 | 1.8667 | 3.5 | matches the exact threshold |
| `C_2_1.txt` | 49 | 2.0000 | 2.0000 | both bounds jointly to N=49 |
| `B_2_1.txt` | 95 | 6.0000 | 2.0000 | — |
| `seq_B_3_2.txt` | 34 (a *sequence*, not a permutation) | 1.8 | 1.5000 | class-S alive at C=3/2, N=34 |

**Survivor rigidity, re-verified:** all **6472** last-level (N=30) class-A C=7/4
survivors are distinct, and every one of them begins `1,7,2,4,3,9,8,5` — in fact
**14 of the 30 positions are constant across the entire surviving population**
(positions 1–8, 19, 26–30). The count 6472 equals my DFS's level-30 count exactly.

### UNVERIFIED

The SAT/CP-SAT half of the route: the C-class UNSAT at N=52, the A C=2 and C=3
SAT runs at N ≥ 53 (I verified their *witnesses*, which is what matters, but not
the search logs), the CP-SAT spot checks, and the `results/mining.txt` structural
claims other than the rigid-head one I re-checked. Also: R4 never wrote a report,
so its "frontier still alive" statements exist only as jsonl records.

### VERDICT

**Computationally sound and fully reproducible; one genuinely new infinite theorem.**
The class-A numbers are duplicates of R9 and of the SAT campaign — which is a
positive (three independent engines agree exactly) but adds nothing new. The real
asset is **class S**, which is under-exploited: it produces certified infinite
theorems at a cost ~4 orders of magnitude below the class-A family (227 nodes at
C=4/3 versus ~10⁶ at the comparable class-A point C=7/4), and it is the only
family in the project immune to Remark 17(a).

---

## 3. Route R8 — ℤ-vs-ℕ transfer at length 4

Directory `attempts/route-R8/`. REPORT.md **is** present and complete (25 kB).

### PROVED (hand proofs; I audited each and re-derived the arithmetic)

- **T1** (sharpened DEGS77(a)). For a bijection a: ℕ→ℕ with π = a⁻¹ and c = a(1),
  some v ≥ 2c+1 has π(v) < π(2v−c); hence (c, v, 2v−c) is an **increasing** monotone
  3-AP whose first term is a(1) and whose step d = v−c ≥ c+1 **exceeds** its first
  term. *Checked:* g(v)=2v−c maps [2c+1,∞) into itself (g(v) ≥ 3c+2 ≥ 2c+1 for c ≥ 1);
  the contrary hypothesis gives an infinite π-decreasing orbit, impossible in type ω.
  **VALID**, and strictly stronger than CORE Lemma 2.
- **T2** (split impossibility). If b: ℤ→ℤ is a bijection whose values at positions
  < s are exactly ℤ_{≤0} ∪ X with X ⊂ ℕ finite, then b contains an increasing
  monotone 4-AP. *Checked:* only finitely many v ≥ 2c+1 have g-orbits meeting X
  (g^k(v)=f forces v = c+(f−c)/2^k); T1's descent inside the right part yields
  (c, v, 2v−c), and x := c−d = 2c−v ≤ −1 sits left of s, giving the 4-AP
  (c−d, c, c+d, c+2d). **VALID.** Consequence: 196-NO does **not** yield a ℤ-avoider
  by concatenation, and building a ℤ-4-avoider whose positives are position-bounded
  below *is* solving 196.
- **T3** (annulus-macro impossibility, ℤ, k=3). *Checked arithmetically:* the four
  witnesses (1,122,243), (−239,2,243), (241,485,729), (1,365,729) are genuine APs
  with steps 121, 241, 244, 364, and their ternary annulus indices are
  (0,4,5), (4,0,5), (4,5,6), (0,5,6). The σ-extremality chain then forces
  σ₅ strictly between σ₀ and σ₄, and simultaneously σ₅ < σ₆ and σ₅ > σ₆. **VALID.**
- **Theorem W** (LeSaulnier–Vijay-type, new proof). W = 2, (1,4,6), (3,8,10),
  (5,12,14), … is a permutation of ℕ with **no monotone 4-AP of odd common
  difference**. *Checked:* the position formulas pos(odd o) = (3o+1)/2 and
  (3e−2)/4 ≤ pos(even e) ≤ 3e/4 hold on the whole 3000-position prefix; the four
  inequalities in the two parity cases are correct as written. **VALID.**
- **L3** (restriction), **L4** (affine self-reduction: every AP-restriction of a
  196-counterexample is again one — this is CORE Corollary 26, independently
  derived), **L5** (affine rigidity: an AP-preserving map is affine, and no affine
  map is a bijection ℤ↔ℕ), **L6** (band pigeonholes: 5-APs have an adjacent
  same-*dyadic*-band pair among their last three terms; 4-APs the same with
  *ternary* bands). All elementary and correct.

### MEASURED (independently re-implemented here, `verify_R8.out`)

- Theorem W: no monotone 4-AP with odd d on prefixes of 400 / 1300 / **4000**
  positions (values up to 5334); even-d 4-APs present as they must be, first (1,3,5,7).
- Ladder level k=2: my own Bresenham reconstruction of "four ascending residue
  streams mod 4 with bit-reversed geometric rates (1,4,2,8) on residues (1,2,3,0)"
  has **no monotone 4-AP with d ≢ 0 mod 4 through 2000 positions**.

### UNVERIFIED (SAT; not re-run)

- ℕ, k=4, base-3 joint band macro: SAT to N = 80, **UNSAT at N = 242**
  (`e7_b3_all_asc.log`, 1 456 760 clauses).
- ℤ, k=4, base-3 alternating annuli: verified windows [−80,80], **UNSAT at ±242**
  (`e10_zb3_k4_M4.log`, 11 685 870 clauses). The coincidence of these two horizons
  is R8's central transfer claim and rests entirely on these two solver runs.
- ℤ, k=5, base-2 alternating: verified 5-AP-free windows [−127,127].
- All [LIT] statements about problem 195 (Geneson k ≤ 5, Adenwalla k ≤ 4). R8
  marks them [LIT] and never uses them in a proof — correct hygiene. Not re-checked
  (and per this session's rules, not to be re-fetched).
- The report's "ladder verified for k = 2 (N = 5864) and k = 3 (N = 1255)" is **not
  in the log**; `e9_lv.log` records only ~800-position checks. See §6.5.

### VERDICT

**Complete, honest, and correctly self-limiting; no live thread toward 196.**
Four genuine theorems (T1, T2, T3, W) plus a complete folding-obstruction taxonomy
(restriction blocked by an order-type dichotomy whose good branch is 196-hard;
zigzag folds blocked by b1/b2; value conjugation blocked by L5). Its two most
useful exports are already absorbed: T1's sharpened 3-AP and L4 = CORE Corollary 26.
Its one substantive *new* empirical finding — ℕ and ℤ dying at the *same* scale
horizon (alive at 80, dead at 242) in the strongest macro framework, so the
length-4 obstruction has a scale-local core not explained by the left edge alone —
is unreproduced SAT and should be treated as a hypothesis until the N=242 cores
are mined. That mining is R8's own next-step #1 and remains the only follow-up
worth funding here.

---

## 4. Route R9 — structural census of finite avoiders

Directory `attempts/route-R9/`. REPORT.md **is** present and complete (24 kB).
The "certification batch still running" flagged in NOTES **has since completed**
(`cert_C1.875.txt`), and its result contradicts the report's own prediction — see §6.3.

### PROVED (complete enumerations; every one reproduced here level-by-level)

Avoider counts and dead ends (`tamedfs.c` with an effectively unbounded profile,
1,063,743,455 nodes):

```
N      1  2  3   4    5    6     7      8       9        10         11          12           13
count  1  2  6  22  102  564  3336  22266  168864  1307470  11066766  101361722  949812334
dead   0  0  0   0    0    0     0      0       0        0         0     515296     —
```
Exact match with R9's census, **including the first appearance of dead ends at N=12
with exactly 515,296 of them.**

Certified extinction levels N\*(C) of the class-A tree `pos(v) ≤ ⌊Cv⌋`
(min N with no avoider). My independent DFS matches R9's per-level counts, per-level
dead counts **and total node counts exactly**:

| C | N\*(C) | total nodes (mine = R9's) |
|---|---:|---:|
| 1 | 4 | 3 |
| 5/4 | 4 | 3 |
| 4/3 | 10 | 10 |
| 11/8 | 10 | 10 |
| 3/2 | **15** | 276 |
| 8/5 | **18** | 2 168 |
| 13/8 | 21 | 3 020 |
| 5/3 | 26 | 126 185 |
| 7/4 | **31** | 1 036 992 |
| 9/5 | **34** | 57 006 572 |
| 15/8 | **37** | 2 654 502 055 |

(C = 5/4, 11/8, 13/8, 5/3 are new points I added; the rest reproduce R9.)
Beyond: ρ(56) ≤ 2 and ρ(75) ≤ 3 from R4's verified witnesses; ρ(85) > 2 from the
eager two-solver UNSAT in `experiments/verify_c2_n90.out`.

Also reproduced: R9's k=3 calibration row (N\* = 5, 10, 12, 13, 20, 29 at
C = 1.5, 2, 2.5, 3, 4, 6) and the verified N=50, C≤2 witness
(permutation of [1..50], monotone-4-AP-free, max pos(v)/v = 2.000000 exactly).

The **interval theorem** R9 states in §1.1 is CORE Lemma 8 (independent derivation),
and my DFS is built on it; its correctness is implicitly re-confirmed by the exact
agreement of all avoider counts with brute force at small N.

### MEASURED but not re-run

- SIS (sequential importance sampling) counts to N = 32: 7.7882 × 10²⁹ ± 0.15 %,
  mean branching 14.6 and rising, dead-end fraction 5.7 %. R9's estimator is
  unbiased by construction and agrees with exact counts at N ≤ 14; I did not re-run it.
- Exact counts at N = 14 (9,471,574,188) and N = 15 (100,130,083,830). My level-13
  agreement makes these credible but they are not independently confirmed here.
- All statistics histograms (LIS/LDS, fixed points, 3-AP counts, pos(1) distribution),
  and the 3-AP-free subpopulation analysis.

### NOT EVIDENCE (R9 says so itself, correctly)

All **beam** horizons (k=4 at C = 2, 2.5, 3, 4, 6, 8; all k=5 rows). R9 proves in
its §6.3 that beams produce false floors — its C=3 beams died at levels 59–63 while
witnesses exist at N = 75 (I re-verified R4's N=75 plain witness). These numbers
must never be quoted as extinction levels.

### VERDICT

**The census is trustworthy — the strongest reproducibility record of the four
routes.** Matching total node counts of a 2.65 × 10⁹-node search bit-for-bit is
about as good as independent confirmation gets. Its *reading*, however, needs
revision: R9's "weak lean NO" rests on (i) k=4 clustering with k=5 rather than k=3,
and (ii) the logarithmic growth of the empirical φ floor. Point (i) is a
qualitative similarity between "harder pattern" and "known NO" that carries no
logical force; point (ii) is refuted as evidence in §5 below. The correct reading
of R9's data is **no lean at all**.

---

## 5. The cross-route calibration (the coordinator's question, answered)

> *How does the displacement max_v pos(v)/v of extendable finite avoiders grow with N?*

Define **ρ(N) := min over monotone-4-AP-free permutations σ of [1..N] of
max_v pos_σ(v)/v.** ρ is **nondecreasing** in N (deleting the largest value only
lowers positions), so ρ is exactly the inverse staircase of the N\*(C) table above,
and "min over all avoiders" = "min over extendable avoiders" wherever the value of
ρ is unchanged at the next level.

**Exact certified staircase** (all reproduced in this directory):

```
ρ(N) ≤ 1      for N ≤ 3      ρ(4)  > 1
ρ(N) ≤ 4/3    for N ≤ 9      ρ(10) > 11/8
ρ(N) ≤ 3/2    for N ≤ 14     ρ(15) > 3/2
ρ(N) ≤ 8/5    for N ≤ 17     ρ(18) > 8/5
ρ(N) ≤ 13/8   for N ≤ 20     ρ(21) > 13/8
ρ(N) ≤ 5/3    for N ≤ 25     ρ(26) > 5/3
ρ(N) ≤ 7/4    for N ≤ 30     ρ(31) > 7/4
ρ(N) ≤ 9/5    for N ≤ 33     ρ(34) > 9/5
ρ(N) ≤ 15/8   for N ≤ 36     ρ(37) > 15/8
ρ(N) ≤ 2      for N ≤ 56     ρ(85) > 2         (N*(2) ∈ [57, 85])
ρ(N) ≤ 3      for N ≤ 75     nothing certified above
```

**Fit** (`rho_fit.py`, `rho_fit.out`). Least squares over the 11 exact points:
`N*(C) ≈ 0.178·e^{2.912 C}` (R² = 0.939), i.e. **ρ(N) ≈ 0.59 + 0.343·ln N**.
Restricted to the large-C end (C ∈ [1.6, 1.875]): `N*(C) ≈ 0.345·e^{2.534 C}`,
i.e. `ρ(N) ≈ 0.42 + 0.395·ln N`. Both predict N\*(2) ≈ 55–60 against a truth in
[57, 85], so the fit is well calibrated *in sample*. This reproduces R9's
`ρ(N) ≈ 0.38 ln N + 0.5` and R20's `N*(C) ≈ 4 e^{4.15(C−1.25)}` (same curve,
different parametrisation).

### Why this statistic does NOT support a NO lean — the k=5 control

R9 and NOTES.md both read "ρ(N) grows only logarithmically, so tame profiles like
v log v survive" as (weak) NO-side evidence. Run the identical procedure on k = 5,
where the infinite answer **is known**:

| C | k=3 (YES known) | k=4 (open) | k=5 (NO known) |
|---|---:|---:|---:|
| 1 | 3 | 4 | — |
| 5/4 | 3 | 4 | **13** |
| 4/3 | 3 | 10 | **35** |
| 3/2 | 5 | 15 | > 90 (not completed) |
| 2 | 10 | [57, 85] | — |
| 3 | 13 | ≥ 76 | — |
| **4** | 20 | ? | **+∞ (THEOREM, §1)** |
| 6 | 29 | ? | **+∞ (THEOREM, §1)** |

(k=3 and k=5 entries at C ≤ 4/3 and the k=4 column are exact complete enumerations
run here; the k=5 C ≥ 4 entries are the theorem from R2's Construction A.)

Fit the two exact k=5 points the same way: `N*₅(C) ≈ 4.6·10⁻⁶ · e^{11.885 C}`,
which predicts a **finite** N\*₅(4) ≈ 2 × 10¹⁵. **That prediction is false** — the
truth is +∞. So:

> **An exponential fit to small-C extinction data cannot detect a divergence at a
> finite C\*, and in the one case where C\* is known it gives no warning at all.**

Therefore the k=4 law `N*(C) ≈ a e^{bC}` is **not** evidence that ρ(N) → ∞, and
"ρ grows only like log N" is **not** evidence that ρ is unbounded either. The
statistic supports neither branch. This sharpens CORE Remark 17(b) (which observed
that k=5 *also* dies at small C) into a quantitative statement about what the
extinction curve can and cannot reveal, and it strengthens Remark 27's blind-spot
warning: the blind spot is not merely computational, it is *inferential*.

### What the calibration DOES establish — "how much displacement avoidance needs"

- **Length 5 needs exactly a factor-4 linear corridor.** Construction A achieves
  5-AP-freedom with `sup_v pos(v)/v = 4` (limsup 4, liminf 1/4, verified to 65535),
  and `N*₅(5/4) = 13`, `N*₅(4/3) = 35` show a factor-4/3 corridor is *not* enough.
  The whole answer at length 5 lives inside a bounded linear corridor.
- **Length 4 is certified dead only up to C = 2** (ρ(85) > 2), and alive at C = 3
  up to N = 75. So the certified k=4 extinction range covers **half** of the
  C-range in which the known k=5 solution lives. By the fitted law, reaching C = 4
  would need N ≈ 8 × 10³ – 2 × 10⁴ — squarely inside Remark 27's blind spot.
- Consequently **nothing certified rules out a 196-counterexample with bounded
  linear displacement**, e.g. `sup pos(v)/v ∈ [3, 4]`. And CORE Theorem 14 shows
  that a linear profile at exactly C = 3 already suffices to kill *all increasing*
  4-APs (the triadic reversed-block permutation T, pos(v) ≤ 3v−1). The corridor
  C ∈ [3, 4], where the increasing orientation is already solvable and the k=5
  solution lives, has never been probed for the plain (two-orientation) target.

---

## 6. Discrepancies found in shared documents (flagged, not edited)

1. **CORE.md Remark 17** tabulates `N*(2.0) = 90` and calls N\*(C) "the minimal N
   with no such permutation". But `experiments/verify_c2_n90.out` records UNSAT
   already at **N = 85** (cadical 297 s + glucose 200 s, agreeing), and route R4 has
   a verified witness at **N = 56** (`route-R4/avoiders/A_2_1.txt`, re-checked here,
   max pos(v)/v = 2.0000). So the minimal N is in **[57, 85]**; "90" is merely where
   CEGAR happened to be run. The fitted law is unaffected (it predicts ≈ 60).
2. **CORE.md Remark 17** lists C = 1.25 as the first threshold with N\* = 4; note
   N\*(1) = 4 as well, so C = 1.25 is not the smallest C with that value.
3. **Route R9 REPORT §5.1** lists `C = 15/8: run in progress (predicted 41)`.
   The run **finished**: `cert_C1.875.txt` shows EXTINCT at n = **37** after
   2,654,502,055 nodes. I reproduced it exactly, and R4's SAT agrees (SAT 36 /
   UNSAT 37). The prediction 41 was wrong; the exponential fit should be refitted
   with (1.875, 37) — I did so in `rho_fit.py`.
4. **Route R9 REPORT §6.1** says "ρ(74) ≤ 3 (SAT-route *asym* witness at N=74)".
   R4 has a **plain** verified witness at N = 75 with max pos(v)/v = 3.0000, so
   ρ(75) ≤ 3 for the plain target.
5. **Route R8 REPORT §5** claims the bit-reversed-rate ladder was "verified for
   k = 2 (N = 5864) and k = 3 (N = 1255)". `e9_lv.log` records only ~800-position
   checks. My independent reconstruction confirms the k = 2 statement to 2000
   positions; the k = 3 statement is **unverified**.
6. **ROUTES.md** still lists R2, R4, R8, R9 as "active". R2, R8, R9 have complete
   REPORT.md files; R4 has none and its results are only in `thresholds.tsv`
   plus a NOTES entry (this document now serves as its report of record).

---

## 7. Ranked next steps

1. **Finish the k=5 extinction ladder with the same engines used for k=4** — exact
   or SAT-certified N\*₅(C) at C = 3/2, 7/4, 2 — and publish the k=4 and k=5 curves
   side by side. This is the only way to convert the project's large body of
   extinction data into a usable signal, because k=5 is the sole case with both a
   known infinite answer and a known displacement constant (exactly 4, now proved
   and verified). If the two curves are constant multiples of each other throughout
   the reachable range, the k=4 curve carries no information about C\* and the
   ∀C-extinction programme (R15/R19) should be closed as a YES route. If their
   curvature differs, that difference is the project's first empirical
   YES/NO discriminator. Cost: my `tamedfs_k.c` reached C = 4/3 for k=5 in 2.2 M
   nodes; C = 3/2 overflowed a 20-minute budget, so this needs R4's propagating
   engine or the CEGAR/order encoding.
2. **Mine the class-S (position-side) ladder.** Certify S at C = 3/2 (alive at
   N = 34, so the wall is above that) and C = 2. Each success is a quotable
   infinite theorem needing **no compactness**, of the form "every 4-AP-free
   permutation of ℕ has a position i ≤ N_C with a(i) > C·i", and the certificates
   are ~10⁴× cheaper than the value-side ones. The family is immune to
   Remark 17(a) because S-survival is *not* equivalent to 196-NO.
3. **Probe the plain target in the corridor C ∈ [3, 4]** — the range where the
   increasing orientation is already solvable (Theorem 14's triadic T at C = 3)
   and where the length-5 answer lives. Currently completely unprobed for the
   two-orientation target; R4's N = 75 witness is the only data point.
4. **Mine R8's N = 242 / ±242 UNSAT cores** (R8's own next-step #1). If the
   shared scale-local core is macro-independent it is a candidate YES-side lemma
   for both 195(k=4) and 196; if it is an artifact of band contiguity, it redirects
   R1's corridor search.
5. Low priority: re-run R2's Mod-1 SAT frontier with an independent encoding —
   it is the only unreproduced piece of R2 and it carries the route's strongest
   negative claim ("no interval-block scheme of ratio ≥ 4 works at length 4").

---

## 8. Artifacts in this directory

| file | role |
|---|---|
| `verify_R2.py` / `.out` | independent Construction A + checkers, V0–V6, to N = 65535 |
| `verify_R2_S1S2.py` / `.out` | AP-by-AP confirmation of R2's S1/S2 characterisation at N = 16383 |
| `tamedfs.c` | independent complete DFS for φ-bounded 4-AP-free permutations |
| `tamedfs_k.c` | same for general k (used for the k=3 and k=5 calibrations) |
| `seqdfs.c` | independent complete DFS for class S (injective sequences a(i) ≤ ⌊Ci⌋) |
| `tame_C1.8.out`, `tame_C1.875.out`, `census_unbounded.out` | reproduced R9 certificates |
| `k5_C1.5.out` | k=5, C=3/2 run (did **not** complete within budget) |
| `verify_witnesses.py` / `.out` | apcheck re-verification of all R4/R9 stored witnesses |
| `verify_R8.py` / `.out` | Theorem W + mod-4 ladder re-implementation |
| `rho_fit.py` / `.out` | the ρ(N) staircase, fits, and the k=5 calibration |
