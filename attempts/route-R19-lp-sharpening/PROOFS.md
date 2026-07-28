# Route R19 — PROOFS (statements with full proofs)

Conventions: PROBLEM.md governs. For a permutation σ of [1..N] (or of ℕ),
pos = σ⁻¹, `v ≺ w` means pos(v) < pos(w), pred(v) = {w : w ≺ v}.
All numbered claims below are proved here; machine checks are named but never
substitute for a proof.

---

## §1. The prefix-completion dictionary

For a permutation σ of [1..N] define

- `m(w) := min{ v ≤ w : pos(v) ≥ pos(w) }`   (so m(w) = w iff w is *grounded*),
- `e*(w) := w − m(w)`  = max{ e ≥ 1 : pos(w−e) > pos(w) }, or 0 if there is no such e
  (this is exactly CORE Thm 12's max drop scale),
- `R(p) := max{ j ≥ 0 : [1..j] ⊆ σ([1..p−1]) }`   (staircase / prefix reach; R(1) = 0),
- `τ_j := max_{v ≤ j} pos(v)`   (completion time of the initial segment [1..j]).

**Prop 1 (dictionary).** For every permutation σ of [1..N]:

  (a) `m(w) = R(pos(w)) + 1`  for every w;
  (b) `Σ_{w=1}^N m(w) = N + Σ_{p=1}^N R(p)`;
  (c) `Σ_{p=1}^N R(p) = N² − Σ_{j=1}^N τ_j`;
  hence `Σ_w m(w) = N + N² − Σ_j τ_j` and
  `Σ_w e*(w) = N(N+1)/2 − N − Σ_p R(p) = Σ_j τ_j − N² + N(N+1)/2 − N`.

*Proof.* (a) For v ≤ w one has pos(v) ≥ pos(w) iff v ∉ pred(w) (v = w gives equality).
So m(w) is the least element of [1..w] outside pred(w); equivalently
[1..m(w)−1] ⊆ pred(w) and m(w) ∉ pred(w). Since pred(w) is exactly the set of values
at positions < pos(w), the largest complete initial segment inside σ([1..pos(w)−1]) is
[1..m(w)−1], i.e. R(pos(w)) = m(w) − 1.

(b) pos is a bijection [1..N] → [1..N], so summing (a) over w reindexes to
Σ_p (R(p) + 1).

(c) `R(p) ≥ j ⟺ [1..j] ⊆ σ([1..p−1]) ⟺ τ_j ≤ p−1 ⟺ p > τ_j`. Hence
Σ_p R(p) = Σ_p #{j ≥ 1 : R(p) ≥ j} = Σ_j #{p ≤ N : p > τ_j} = Σ_j (N − τ_j).
The last display follows from Σ_w w = N(N+1)/2. ∎

*Machine check:* `r19lib.self_test()` verifies (a)–(c) and the two characterisations of
e* on 2000 random permutations of sizes 3–12, and cross-validates the increasing- and
decreasing-4-AP checkers against `experiments/apcheck.py` brute force on 4000 boards.

---

## §2. Exact reduction of the CORE Thm 12 ledger

**Prop 2 (the ledger IS a lower bound on Σ τ).**
Let σ be a permutation of [1..N] with `pos(v) ≤ C·v` for all v (C ≥ 1 rational).
Then

    N(N+1)/2 = Σ_w pos(w) ≤ Σ_w ⌊C·m(w)⌋ ≤ C·Σ_w m(w) = C·( N + N² − Σ_j τ_j ),

i.e.  **Σ_j τ_j ≤ N² + N − N(N+1)/(2C)**  is *forced* by the profile.

*Proof.* pos(m(w)) ≥ pos(w) by definition of m(w), and pos(m(w)) ≤ ⌊C·m(w)⌋ by the
profile; then Prop 1(b,c). ∎

**Definition.** `S_inc(N) := min{ Σ_j τ_j : σ a permutation of [1..N] with no increasing
monotone 4-AP }`, and

    C_ledger(N) := N(N+1) / ( 2 ( N² + N − S_inc(N) ) ).

**Prop 3 (exact ceiling of the ledger method).** For C ≥ 1:

  (i) if `C < C_ledger(N)` then no increasing-4-AP-free permutation of [1..N] satisfies
      pos(v) ≤ Cv — the ledger inequality of Prop 2 is violated, so the ledger *proves*
      LP-inc(C);
  (ii) if `C ≥ C_ledger(N)` then the ledger inequality of Prop 2 is *satisfied* by the
      Σ-τ-minimising increasing-4-AP-free permutation of [1..N]; so the **unweighted
      ledger** — the argument that combines only Σ_w pos(w) = N(N+1)/2 with
      pos(w) ≤ ⌊C·m(w)⌋, which is exactly CORE Thm 12 — derives no contradiction at
      board size N, no matter how the demand side is improved.

Consequently the unweighted ledger proves LP-inc(C) exactly for `C < sup_N C_ledger(N)`.

*Proof.* Immediate from Prop 2 and the definition of S_inc(N). ∎

*Scope note.* Prop 3(ii) bounds the **unweighted** ledger only. A weighted variant
`Σ_w λ_w pos(w) ≤ C Σ_w λ_w m(w)` needs a lower bound on the left side; since pos is
only known to be a bijection, the available bound is the rearrangement one
(`Σ λ_w pos(w) ≥ Σ_k λ_{(k)}·k` with λ sorted decreasingly), which is a strictly larger
method class and is NOT covered by Prop 3(ii). Note also that adding the injectivity
Hall condition to the unweighted ledger changes nothing: by Prop 1(a),
`#{w : m(w) ≤ s} = τ_s`, so `#{w : ⌊C m(w)⌋ ≤ ⌊Cs⌋} ≤ ⌊Cs⌋` is literally the profile
hypothesis `τ_s ≤ ⌊Cs⌋` again.

**Calibration.** CORE Thm 12 is the demand bound `Σ_j τ_j ≥ (5/9)N² − O(N)`
(equivalently Σ e* ≥ N²/18 − O(N)); the corresponding constant is
`1/(2 − 2·(5/9)) = 9/8`. In general a demand bound `Σ τ ≥ γN² − O(N)` yields
LP-inc(C) for every `C < 1/(2 − 2γ)`.

| γ | 1/2 | 5/9 | 31/43 | 3/4 | 5/6 |
|---|---|---|---|---|---|
| C | 1 | **9/8** (Thm 12) | 43/24 (R6 level) | **2** | 3 (Thm 14 ceiling) |

---

## §3. The ledger cannot reach C = 2 (triadic computes Σ τ exactly)

**Prop 4.** Let T be the triadic reversed-block permutation of CORE Thm 14
(blocks I_k = [3^k, 3^{k+1}) listed in increasing k, each internally decreasing).
For `N = 3^{K+1} − 1` (complete blocks) the restriction of T to [1..N] satisfies

        Σ_{j=1}^N τ_j  =  (3/4) N² + N/2      (exactly),

and therefore `C_ledger(N) ≤ 2(N+1)/(N+2) < 2`.

*Proof.* In T, pos(v) = 4·3^k − 1 − v for v ∈ I_k, so within a block pos decreases with
v and the block occupies positions [3^k, 3^{k+1}). Hence for j ∈ I_k,
τ_j = max_{v ≤ j} pos(v) = pos(3^k) = 3^{k+1} − 1 (all earlier blocks sit at smaller
positions). Therefore
Σ_j τ_j = Σ_{k=0}^{K} |I_k|·(3^{k+1}−1) = Σ_{k=0}^{K} 2·3^k(3^{k+1}−1)
        = Σ_{k=0}^{K} (6·9^k − 2·3^k) = (3/4)(9^{K+1} − 1) − (3^{K+1} − 1).
With N = 3^{K+1} − 1, 9^{K+1} = (N+1)², so Σ_j τ_j = (3/4)((N+1)²−1) − N
= (3/4)N² + N/2. Then N² + N − Σ τ = N²/4 + N/2 and
C_ledger(N) ≤ N(N+1)/(2(N²/4+N/2)) = 2(N+1)/(N+2). ∎

**Prop 5 (uniform version).** For every N ≥ 1, writing A = 3^K for the unique power of
3 with A ≤ N < 3A, the restriction of T to [1..N] has
`Σ_j τ_j = N² − NA + (3/4)A² + N − A + 1/4`, whence
`C_ledger(N) ≤ N(N+1) / (2(NA − (3/4)A² + A − 1/4)) < 2` for every N.

*Proof.* Blocks I_0,…,I_{K−1} are complete and contribute as in Prop 4; the top block is
the interval [A, N] listed in decreasing order at positions [A, N], so pos(A) = N and
τ_j = N for every j ≥ A. Summing gives the displayed formula. Writing N = xA with
x ∈ [1,3) the denominator is 2A²(x − 3/4) + O(A) and the ratio is
x²/(2x − 3/2) + O(1/A), whose supremum over x ∈ [1,3) is 2, attained only in the limits
x → 1 and x → 3; the exact rational expression is < 2 for every finite N. ∎

**Corollary 6 (ledger ceiling).** No CORE-Thm-12-ledger argument can prove LP-inc(C)
for any C ≥ 2. (Compare CORE Thm 14: *no* increasing-only argument can pass C = 3.)

*Machine check:* `measure_gamma.py` verifies Σ τ_T(N) = (3/4)N²+N/2 at
N = 3^k−1, k = 2..9, and that T is increasing-4-AP-free with pos(v) ≤ 3v−1 up to
N = 19682.

---

## §4. The mixed (two-orientation) forcing closure

Fix a monotone-4-AP-free permutation a of ℕ (both orientations forbidden).

**Definition.** u is *open at scale d* (d ≥ 1, u−2d ≥ 1) if pos(u−2d) < pos(u−d) < pos(u);
u is *co-open at scale d* (d ≥ 1, u−d ≥ 1) if pos(u+2d) < pos(u+d) < pos(u).

**Theorem 7 (mixed forcing).**
  (I-step, = CORE Thm 16(a)) If u is open at d then pos(u+d) < pos(u).
  (D-step, NEW) If u is co-open at d then pos(u−d) < pos(u).

*Proof.* (I) (u−2d, u−d, u, u+d) is a 4-AP with difference d whose first three terms are
positionally increasing; pos(u+d) > pos(u) would make it an increasing monotone 4-AP.
(D) (u+2d, u+d, u, u−d) is a 4-AP with difference −d; its first three terms are
positionally increasing by co-openness (pos(u+2d) < pos(u+d) < pos(u)); if in addition
pos(u) < pos(u−d) then those four values, read in increasing position order, are
u+2d, u+d, u, u−d — a decreasing monotone 4-AP. Positions are distinct, so
pos(u−d) < pos(u). ∎

**Definition.** The *mixed forcing digraph* has, at each u, the edges u ⟶ u+d for every
open scale d and u ⟶ u−d for every co-open scale d. `Cl±(u)` is the forward closure.

**Theorem 8 (mixed closure bound).** For every u,
`Cl±(u) ∖ {u} ⊆ pred(u)`, hence `|Cl±(u)| ≤ pos(u) < ∞`.

*Proof.* Every edge u ⟶ u′ has pos(u′) < pos(u) by Theorem 7; induct along chains and
use transitivity of ≺. pred(u) has exactly pos(u) − 1 elements. ∎

**Theorem 9 (equivalence).** The mixed digraph is finitely branching: at u the open
scales satisfy d ≤ (u−1)/2 and the co-open scales satisfy d ≤ u−1, so the out-degree is
< 3(u−1)/2. Hence Cl±(u) is infinite iff there is an infinite mixed forcing chain
(König), and since an infinite chain is an infinite ≺-descending sequence (impossible at
order type ω, CORE Lemma 1),

  **196-YES ⟺ every monotone-4-AP-free permutation of ℕ admits an infinite mixed
  forcing chain.**

This refines CORE Theorem 16: the mixed digraph contains the increasing-only one, so
every witness for Thm 16 is a witness here, and the closure is strictly larger in
practice (measured factor 2–4, §R19 REPORT).

**Remark 10 (why the D-step is a genuine two-orientation invariant).** The triadic
permutation T of CORE Thm 14 satisfies the I-step everywhere (it has no increasing 4-AP)
but violates the D-step at a positive rate — 48 of 78 triggers at N = 26, 507 of 780 at
N = 80, 4800 of 7260 at N = 242 — and its mixed closures escape pred(u) for 228 of 242
values, with |Cl±(u)|/pos(u) up to 2.89. So Theorem 8 is exactly an invariant that the
increasing-only extremal object fails, and it fails *only* because of the decreasing
in-block runs (the D-step's conclusion is derived from a decreasing 4-AP, which T
contains: e.g. (12,11,10,9)).

**Remark 11 (structure of co-open scales).** In the infinite setting pred(u) is finite,
so u+d ≺ u for only finitely many d; co-openness at d requires u+d ≺ u, hence there are
at most pos(u) − 1 co-open scales at u. Both the I- and D-mechanisms are therefore
driven entirely by pred(u): the mixed closure is a structure *inside* pred(u), never a
way of escaping it. This is why Theorem 9, like Theorem 16, is a reformulation and not
yet a proof — but it is a strictly tighter one.

*Machine check:* `mixed_closure.py` mode M1 verifies the I-step, D-step and Theorem 8 on
ALL 195 154 monotone-4-AP-free permutations of [1..N] for N = 4..9 (22, 102, 564, 3336,
22 266, 168 864 boards), zero violations.

---

## §5. Where Theorem 16 does *not* help the ledger

**Prop 12.** The I-step contributes nothing new to the ledger's demand side.

*Proof.* CORE Thm 12's demand is: for every (x,e) with x+3e ≤ N some i ∈ {0,1,2} has
pos(x+(i+1)e) < pos(x+ie), i.e. the value x+(i+1)e has an e-drop. The I-step applied at
u = x+2e is exactly the case i = 2 of that disjunction (its hypothesis is the failure of
cases i = 0, 1). The transitive closure bound of Theorem 8 is a *lower* bound
pos(u) ≥ |Cl±(u)|, and the ledger derives its contradiction from *upper* bounds on
Σ pos, which is pinned to N(N+1)/2; the only inequality a lower bound yields is
Σ_u |Cl±(u)| ≤ N(N+1)/2, an independent constraint (measured occupancy 0.24–0.44 on SAT
avoiders at N ≤ 160, i.e. slack of a factor 2–4). ∎

---

## §6. Machine results (status record for route R19)

Tags: **PROVED** (§§1–5 above) / **CERTIFIED** (machine, explicit witness or multi-engine
agreement) / **MEASURED** / **CONJECTURED**. Finite computations are evidence about
finite boards only; they never prove an infinite statement.

### 6.1 CERTIFIED — ledger ceiling C_ledger(N) at concrete N

Each row is certified by an explicit increasing-4-AP-free permutation of [1..N]
(`witnesses.txt`), re-verified by a checker cross-validated against
`experiments/apcheck.py`. Upper bounds only; a better witness can only lower them.
`OPT` = CP-SAT proved optimum (brute-force confirmed for N ≤ 9).

| N | best Σ τ | γ = Στ/N² | C_ledger(N) ≤ | status |
|---|---|---|---|---|
| 8  | 40  | 0.62500 | 9/8 = 1.12500 | OPT (brute force = CP-SAT) |
| 12 | 90  | 0.62500 | 13/11 = 1.18182 | OPT |
| 16 | 159 | 0.62109 | 136/113 = 1.20354 | OPT |
| 18 | 200 | 0.61728 | 171/142 = 1.20423 | witness (CP-SAT lb 196) |
| 20 | 248 | 0.62000 | 105/86 = 1.22093 | witness |
| 22 | 301 | 0.62190 | 253/205 = 1.23415 | witness |
| 24 | 360 | 0.62500 | 5/4 = 1.25000 | witness |
| 26 | 428 | 0.63314 | 351/274 = 1.28102 | witness |
| 28 | 491 | 0.62628 | 406/321 = 1.26480 | witness |
| 32 | 641 | 0.62598 | 528/415 = 1.27229 | witness (plain-target optimum) |
| 40 | 1031 | 0.64438 | 820/609 = 1.34647 | witness (CP-SAT 420 s) |
| 48 | 1518 | 0.65885 | 196/139 = 1.41007 | witness (local search) |
| 56 | 2150 | 0.68559 | 798/521 = 1.53167 | witness (local search) |
| 64 | 2776 | 0.67773 | 260/173 = 1.50289 | witness (local search) |
| 80 | 4652 | 0.72688 | 810/457 = 1.77243 | witness (local search; weakest row) |
| 96 | 6124 | 0.66450 | 1164/797 = 1.46048 | witness (local search) |
| 112 | 8180 | 0.65210 | 1582/1119 = 1.41376 | witness (local search) |
| 128 | 10734 | 0.65515 | 1376/963 = 1.42887 | witness (local search) |

Proved optima only for N <= 16 (CP-SAT OPTIMAL, brute-force confirmed N <= 9); all other
rows are upper bounds from explicit witnesses, and they degrade with N only because the
search degrades. Needed for CORE Thm 12's 9/8: gamma = 5/9 = 0.5556. Needed for R6's
43/24: gamma = 31/43 = 0.7209. Needed for C = 2: gamma = 3/4.

**MEASURED:** best-known gamma(N) lies in [0.617, 0.727] over 8 <= N <= 128, and <= 0.678 at every N in that range except N = 80 (where the search stalled near triadic), against the
0.7209 that a ledger proof of 43/24 would need and the 0.75 that C = 2 would need.
For the PLAIN (both-orientation) target the Sigma-tau minima coincide with the
increasing-only ones at N = 8, 12, 16, 20, 24, so the ledger ceiling is the same there.

**CONJECTURED (weakly supported):** sup_N C_ledger(N) is around 1.3-1.4, i.e. strictly
below R6's machine-assisted 43/24 = 1.7917. Support: at every N where a good witness was
found, gamma(N) <= 0.686 << 0.7209. Caveat: these are search results, not optima (optimality is proved only to N = 16);
at N = 80 the search stalled and gave only 1.772, so the data does NOT exclude
sup_N C_ledger(N) = 2. The PROVED statement is only sup_N C_ledger(N) <= 2 (Prop 5),
i.e. the ledger certainly cannot reach C = 2.

### 6.2 CERTIFIED — mixed closure (Theorems 7–9)

`mixed_closure.py M1`: I-step, D-step and Theorem 8 hold on **all 195 154
monotone-4-AP-free permutations of [1..N], N = 4..9** (22 / 102 / 564 / 3336 / 22 266 /
168 864 boards), zero violations.

### 6.3 MEASURED — triadic violates the D-step (mission item 2)

| N | I-triggers | I-violations | D-triggers | D-violations | u with escaping Cl± | max \|Cl±(u)\|/pos(u) |
|---|---|---|---|---|---|---|
| 26 | 7 | 0 | 78 | 48 | 18/26 | 2.18 |
| 80 | 95 | 0 | 780 | 507 | 69/80 | 2.69 |
| 242 | 966 | 0 | 7260 | 4800 | 228/242 | 2.89 |

The ratio tends to 3, matching pos(v) ≤ 3v−1: the triadic's only defence against the
mixed closure bound is its profile constant 3.

### 6.4 MEASURED — mixed closures on SAT-found plain avoiders

| N | max \|Cl_inc\| (Thm 16) | max \|Cl±\| | max \|Cl±(u)\|/pos(u), pos ≥ N/4 | stuck values | Σ\|Cl±\|/(N(N+1)/2) |
|---|---|---|---|---|---|
| 40 | 9 | 34 | 0.935 | 35.0% | 0.362 |
| 80 | 20 | 57 | 0.826 | 35.0% | 0.238 |
| 130 | 65 | 110 | 0.948 | 28.5% | 0.274 |
| 160 | 78 | 150 | 0.980 (u = 97, pos(u) = 153) | 30.6% | 0.341 |

### 6.5 CERTIFIED — plain linear-profile extinction, pos(v) ≤ ⌊Cv⌋

| C | max SAT N | minimal UNSAT N | engines |
|---|---|---|---|
| 1 | 3 | 4 | CP-SAT, Cadical195, Glucose42 |
| 5/4 | 3 | 4 | CP-SAT, Cadical195, Glucose42 |
| 3/2 | 14 | **15** | CP-SAT, Cadical195, Glucose42 (agree) |
| 7/4 | 30 | **31** | CP-SAT, Cadical195, Glucose42 (agree); DRUP trace 39 993 B |
| 2 | ≥ 49 | unresolved (UNKNOWN at N = 64, 500 s) | — |

Witnesses (verified with `experiments/apcheck.py` and against the profile):
C = 3/2, N = 14: `[1,4,2,3,10,7,5,6,11,8,13,12,9,14]`;
C = 7/4, N = 30: `[1,7,2,4,3,9,8,5,6,23,19,16,20,18,14,10,12,13,11,28,30,24,22,29,21,15,26,25,17,27]`.

**Limitation (honest).** The logged DRUP/DRAT trace for (C = 7/4, N = 31) is NOT
independently checkable by the checker written here: `drup_check.py` (forward RUP +
RAT-on-pivot, and also RAT-on-any-literal) validates the first 478 additions and then
rejects lemma #1171 `(69, 533, −280)`. Most likely pysat's Cadical proof stream is not
a stand-alone DRAT trace for the formula as rebuilt. **The UNSAT results rest on
three-engine agreement across two structurally different encodings, not on a checked
proof.**
