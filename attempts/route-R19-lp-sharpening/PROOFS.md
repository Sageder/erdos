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
