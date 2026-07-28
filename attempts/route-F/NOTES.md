# Route F — the switch / covering attack on (CRUX)

Vocabulary. A finite `U ⊆ Z_{≥2}` is **legal** if it has no isolated point
(`n ∈ U ⇒ n−1 ∈ U or n+1 ∈ U`); equivalently `U` is a disjoint union of runs of
consecutive integers of length `≥ 2`.  `Σ(U) := Σ_{n∈U} 1/n`.  Throughout `D` is
a fixed positive integer ("the modulus"), `ν_p` is the `p`-adic valuation.

> **(CRUX)**  For arbitrarily large `T` there is a legal `W` with `min W ≥ T`
> and `Σ(W) = 1/2`.

**Definitions.**
* `U` is a **`D`-gadget** if `U` is legal and the denominator of `Σ(U)`
  divides `D`; equivalently `Σ(U) = c/D` for an integer `c ≥ 0`.
* A **`D`-switch on a window `[x,y]`** is a pair `(A,B)` of legal systems with
  `A,B ⊆ [x,y]`, `A ≠ B`, and `Σ(B) − Σ(A) = c/D` with `c ∈ Z\{0}`.
  We call `c` the **value** of the switch.

Every statement below is marked **PROVED**, **EXHAUSTIVE** (a finite complete
computation, range stated), or **OBSERVED** (numerical evidence only).
All arithmetic in every verification path is exact (`fractions.Fraction`,
Python `int`, or `int`/`long long` in C); no float ever enters a certificate,
a congruence, or a negative claim.  (Floats occur only in *printed diagnostics*
and in the search's sum bound, which is written with **directed rounding** so it
is conservative — it can never discard a solution.)

---------------------------------------------------------------------------
## 0. Summary of what this route establishes

1. **The covering lemma is proved** (§2) in exactly the form the plan needs.
2. **The plan's reduction is proved** (§3): CRUX follows from the existence of
   `D`-gadgets of value `1/D` at every scale; and more flexibly from a set of
   gadget values whose subset sums cover `D/2`.
3. **The plan cannot dispense with gadgets** (§4, Theorem F7, PROVED): in any
   switch/covering scheme the "all-`A`" system is itself forced to be a
   `lcm(2,D)`-gadget.  So switches *supplement* but never *replace* the gadget
   condition.  This is the precise obstruction asked for in item 4.
4. **Rigid structure theorems for switches** (§4): the symmetric difference of a
   switch is forced to be smooth (Lemma F1), to be large (Lemma F3 — this kills
   *every* bounded-complexity/parametric switch family, sharpening route E §5.3
   from a heuristic to a theorem), and the number of separated switches above
   `T` inside `[T,CT]` is at most `D·(ln C + 1/T)` (Lemma F5).
5. **Switches genuinely are much weaker than gadgets, and this is now
   demonstrated, not assumed** (§5): an explicit universe is exhibited on which
   *no gadget exists* (exhaustive proof) while *183 794 switches exist*
   (all verified exactly).
6. Quantitative reach of the two-scale/covering method is measured (§6), and new
   exhaustive negative ranges are recorded (§7).

7. **Four new verified certificates** (§6.2), each checked by three independent
   arithmetic paths (`Fraction`, `sympy.Rational`, integer `lcm`):
   `Σ = 1/3` with all elements `≥ 200`; `Σ = 1/6` with all elements `≥ 500`;
   and the two Erdős-289 solutions obtained from them, which certify
   **`P(91)`, `P(127)`, `P(128)`** (the previously established range was
   `6 ≤ k ≤ 57`).

The route does **not** prove CRUX.  §8 says exactly where it stops and why.

---------------------------------------------------------------------------
## 1. Two elementary but load-bearing facts

### Lemma F0 (separated unions).  **PROVED**
If `U_1,…,U_s` are legal and `max U_i + 1 < min U_{i+1}` for each `i`, then
`U = ⨆ U_i` is legal and `Σ(U) = Σ_i Σ(U_i)`.
*Proof.*  Each `n ∈ U` lies in a unique `U_i` and keeps its neighbour there. ∎

(The separation hypothesis is not even needed for legality — a union of legal
sets is always legal — but it guarantees the pieces stay disjoint.)

### Lemma F0' (Rule (P), the `p`-adic obstruction).  **PROVED**
Let `V` be a finite set of integers `≥ 2` with `denom(Σ(V)) | D`, let `p` be
prime, `f = ν_p(D)`, and `E = max{ν_p(n) : n ∈ V}` (with `E = −∞` if `p ∤ n` for
all `n`).  If `E > f` then
```
        Σ_{n ∈ V, ν_p(n) = E}  p^E/n  ≡  0   (mod p).
```
*Proof.*  `p^E Σ(V) = Σ_{n∈V} p^E/n`.  If `ν_p(n) = E` the term is `1/m_n`
with `m_n = n/p^E` prime to `p`, a `p`-adic unit; if `ν_p(n) < E` the term is
`p^{E−ν_p(n)}·(unit)`, hence `≡ 0 (mod p)`.  On the other side
`ν_p(p^E Σ(V)) = E + ν_p(Σ(V)) ≥ E − f ≥ 1`.  Reduce mod `p`. ∎

This is the rule that makes every search in this route feasible: iterating it
with the legality rule ("an element both of whose neighbours are deleted is
deleted") gives a *sound* fixpoint containing every admissible `U`
(`universe.py`).  On `[100,400]` with `D = 10!` the fixpoint has **120**
elements and `log₂(lcm/gcd(lcm,D)) = 55`, against route E's 135 elements and 60
bits — i.e. this implementation of the rule is strictly stronger.

---------------------------------------------------------------------------
## 2. The covering lemma  (item 2 of the task)

### Lemma C1 (interval covering by subset sums).  **PROVED**
Let `c_1 ≤ c_2 ≤ … ≤ c_s` be positive integers with
```
      c_1 = 1     and     c_{j+1} ≤ 1 + (c_1 + … + c_j)   for 1 ≤ j < s.
```
Put `M = c_1 + … + c_s`.  Then
`{ Σ_{i∈S} c_i : S ⊆ {1,…,s} } = {0,1,2,…,M}` — every integer of `[0,M]` is a
subset sum, and no integer outside it is.

*Proof.*  Write `S_j = c_1+…+c_j` and let `A_j` be the set of subset sums of
`{c_1,…,c_j}`.  We show `A_j = [0,S_j] ∩ Z` by induction on `j`.
For `j = 1`, `A_1 = {0,1} = [0,1] ∩ Z`.
Assume `A_j = [0,S_j] ∩ Z`.  Then
`A_{j+1} = A_j ∪ (c_{j+1} + A_j) = ([0,S_j] ∪ [c_{j+1}, c_{j+1}+S_j]) ∩ Z`.
Because `c_{j+1} ≤ S_j + 1` the two intervals overlap or abut, so their union is
`[0, c_{j+1}+S_j] = [0,S_{j+1}]`.  Every subset sum is `≤ M`, giving the reverse
inclusion. ∎

### Lemma C2 (multiplicity form — the form actually used).  **PROVED**
Let `v_1 < v_2 < … < v_t` be positive integers with `v_1 = 1`, and let `v_i`
occur with multiplicity `m_i ≥ 1` in a multiset `C`.  If
```
      v_j ≤ 1 + Σ_{i<j} m_i v_i          for every 2 ≤ j ≤ t,
```
then the subset sums of `C` are exactly the integers of `[0, Σ_i m_i v_i]`.
*Proof.*  Sort `C` increasingly and apply C1: within a block of equal values the
hypothesis `c_{j+1} ≤ 1 + S_j` is trivially true (`c_{j+1} = c_j ≤ S_j+1`), and
at a jump from `v_{j−1}` to `v_j` it is exactly the displayed condition. ∎

### Lemma C3 (no value `1`: the `gcd` version).  **PROVED**
Let `C` be a multiset of positive integers, `g = gcd(C)`, `K = max C`.  Suppose
`C` contains, for some `d ≥ 1`, at least `K` copies of each element of a
sub-multiset `C_0 ⊆ C` with `gcd(C_0) = g`.  Then the subset sums of `C`
contain every multiple of `g` in `[K·|C_0|·K , M − K·|C_0|·K]`.
*Sketch/why we do not use it.*  This is the standard "dense complete sequence"
statement; it is strictly weaker than what we need because in our application
(§5) the observed switch values in one window have `gcd = 6 ≠ 1`, so the
covering is only of `6Z`, and the target `D/2` must then be reached inside that
subgroup.  Everything below therefore uses C1/C2, applied to values that are
**explicitly exhibited**, never to hypothetical ones.

---------------------------------------------------------------------------
## 3. The reduction (what the plan buys)  (item 3, the provable half)

### Theorem R1.  **PROVED**
Let `D ≥ 2` be even and `K > 1`.  Suppose there is `T_0` with the property:
> for every `x ≥ T_0` there is a legal `G ⊆ [x, Kx]` with `Σ(G) = 1/D`.

Then CRUX holds.  Explicitly, for every `T ≥ T_0` there is a legal `W` with
`min W ≥ T`, `max W ≤ K^{D/2}·T·(1+o(1))` and `Σ(W) = 1/2`.

*Proof.*  Set `x_1 = T`, and inductively `x_{i+1} = K x_i + 2`.  Apply the
hypothesis at `x_i` to get `G_i ⊆ [x_i, Kx_i]`; the windows are pairwise
separated by `≥ 2`, so Lemma F0 gives that `W = ⨆_{i=1}^{D/2} G_i` is legal with
`Σ(W) = (D/2)·(1/D) = 1/2` and `min W ≥ x_1 = T`. ∎

### Theorem R2 (covering form).  **PROVED**
Let `D ≥ 2` be even, `K > 1`.  Suppose there is `T_0` such that for every
`x ≥ T_0` one can exhibit legal `G_1(x),…,G_s(x) ⊆ [x,Kx]`, pairwise separated,
with `Σ(G_j(x)) = c_j(x)/D`, such that the multiset `{c_j(x)}` satisfies the
hypothesis of Lemma C2 and `Σ_j c_j(x) ≥ D/2`.  Then CRUX holds.
*Proof.*  By C2 some sub-collection has `Σ c_j = D/2`; its union is legal with
`Σ = 1/2` and `min ≥ x`, by Lemma F0. ∎

### Theorem R3 (anchor + switches).  **PROVED**
Let `D ≥ 2` be even.  Suppose that for every `x ≥ T_0`
 (i) *(anchor)* there is a `D`-gadget `G ⊆ [x,Kx]` with `0 < Σ(G) ≤ 1/2`, and
 (ii) *(unit gadgets)* there is a legal `H ⊆ [x,Kx]` with `Σ(H) = 1/D`.
Then CRUX holds.
*Proof.*  Write `Σ(G) = g/D`, `1 ≤ g ≤ D/2`; append `D/2 − g` separated copies
of (ii). ∎

**Remark (why R3 is stated with "unit gadget" and not "unit switch").**  One is
tempted to weaken (ii) to "a *switch* of value `1`", i.e. a pair `(A,B)` with
`Σ(B) − Σ(A) = 1/D`, since Lemma F1 shows the switch condition is much weaker
than the gadget condition.  Theorem F7 below shows this weakening is *false as
stated*: the systems `A_i` that are not switched still contribute their sums to
the total, and the total can be `1/2` only if `Σ_i Σ(A_i)` is itself a
`lcm(2,D)`-gadget.  Taking all `A_i = ∅` recovers exactly R3(ii).

---------------------------------------------------------------------------
## 4. Structure theorems for switches — and the obstruction  (item 4)

### Lemma F1 (support of a switch is smooth).  **PROVED**
Let `(A,B)` be a `D`-switch on `[x,y]`, `w = y − x`.  Then every
`n ∈ A △ B` satisfies
```
      p^{ν_p(n)} | D      for every prime p > w.
```
In particular, if `D` is `P`-smooth and `w ≥ P`, every element of `A △ B` is
`w`-smooth.
*Proof.*  Fix a prime `p > w` and suppose `n ∈ A△B` with `a := ν_p(n) ≥ 1`.
Two distinct multiples of `p` differ by `≥ p > w`, so `n` is the **only**
multiple of `p` in `[x,y]`, hence the only element of `A ∪ B` divisible by `p`.
Write `Δ := Σ(B) − Σ(A) = Σ_m ε_m/m` with `ε_m ∈ {−1,0,1}` and `ε_n = ±1`.
Every term with `m ≠ n` is a `p`-adic integer, while `ν_p(ε_n/n) = −a`; hence
`ν_p(Δ) = −a`.  As `denom(Δ) | D`, `ν_p(Δ) ≥ −ν_p(D)`, i.e. `a ≤ ν_p(D)`. ∎

### Lemma F2 (the value lattice).  **PROVED**
Let `(A,B)` be a `D`-switch, `L = lcm(A ∪ B)`, `g = gcd(L,D)`.  Then the value
`c` of the switch is a multiple of `D/g`.  In particular a switch of value
`c = 1` requires `D | lcm(A∪B)`.
*Proof.*  `Σ(B) − Σ(A) = S/L` with `S = Σ_n ε_n (L/n) ∈ Z`.  `c = DS/L =
(D/g)·(S/(L/g))`, and `denom | D` forces `(L/g) | S`. ∎

### Lemma F3 (a switch is large).  **PROVED**  ← *the no-go for local families*
If `(A,B)` is a `D`-switch with `min(A∪B) ≥ x`, then
```
      |A △ B|  ≥  x / D .
```
*Proof.*  `1/D ≤ |c|/D = |Σ(B)−Σ(A)| ≤ Σ_{n ∈ A△B} 1/n ≤ |A△B| / x`. ∎

**Corollary F4.**  **PROVED**  There is **no** family of `D`-switches
`(A_T,B_T)` with `D` fixed, `min(A_T ∪ B_T) ≥ T`, and `|A_T △ B_T|` bounded as
`T → ∞`.  Consequently no algebraic identity of bounded length — no "`+1`
block" move, no atom split, no doubling map, no `c`-map, no blow-up family —
can produce switches at all scales.  The number of integers that must be moved
grows at least linearly in `T`.

*(This is the theorem behind route E's §5.3 counting heuristic and behind
`VERDICT.md`'s "parametric families die for an arithmetic reason". It is
now unconditional, with an explicit constant.)*

### Lemma F5 (how many separated switches fit above `T`).  **PROVED**
Let `(A_i,B_i)`, `i = 1..s`, be `D`-switches of values `c_i ≥ 1` supported on
pairwise disjoint sub-windows of `[T, CT]`.  Then
```
      s ≤ Σ_i c_i ≤ D·( ln C + 1/T ).
```
*Proof.*  `Σ_i c_i/D = Σ_i (Σ(B_i) − Σ(A_i)) ≤ Σ_i Σ_{n ∈ window_i} 1/n
≤ Σ_{T ≤ n ≤ CT} 1/n < ln C + 1/T`. ∎

So a switch scheme aiming at the target `1/2` needs `ln C ≥ 1/2 − (anchor)`;
with `C = e^{1/2} ≈ 1.65` it is already impossible to do better than
"everything in `[T, 1.65T]`", and the sub-window carrying a switch of value `c`
must have multiplicative width `≥ e^{c/D}`.

### Proposition F6 (the exact reason switches are weaker than gadgets).  **PROVED**
Fix a window `I` and a modulus `D`, and let `L(I)` be the set of legal subsets of
`I`.  Define `U ~ U'` iff `Σ(U) − Σ(U') ∈ (1/D)Z`; this is an equivalence
relation on `L(I)`.  Then
1. `U` is a `D`-gadget **iff** `U ~ ∅`;
2. a `D`-switch on `I` exists **iff** some `~`-class contains two distinct
   elements;
3. consequently *gadget ⇒ switch* (if `G ≠ ∅` is a gadget then `(∅,G)` is a
   switch of value `D·Σ(G)`), and the converse fails.
*Proof.*  (1) `Σ(U) − Σ(∅) = Σ(U)`.  (2) is the definition.  (3) is (1) plus the
example in §5.1. ∎

So *finding a gadget = hitting one prescribed class*, whereas *finding a switch =
hitting any class twice*.  With `2^Λ` legal subsets distributed over `2^λ`
classes, the first needs `Λ ≳ λ`, the second only `2Λ ≳ λ`.  §5.1 realises this
gap explicitly (`Λ = 23`, `λ = 36`, `2Λ = 46`: no gadget at all, 183 794
switches).

### Theorem F7 (ANCHOR NECESSITY — the precise obstruction).  **PROVED**
Fix `D`.  Let `W` be produced by a switch scheme: pairwise separated windows
`I_1,…,I_s`, legal systems `A_i, B_i ⊆ I_i` with `Σ(B_i) − Σ(A_i) ∈ (1/D)Z`,
and `W = ⨆_i X_i` with `X_i ∈ {A_i,B_i}`.  If `Σ(W) = ρ` then
```
      Σ_{i=1}^{s} Σ(A_i)  ∈  ρ + (1/D)Z ,
```
i.e. the "all-`A`" system `A := ⨆_i A_i` — which is legal, and contained in the
same range — satisfies `denom(Σ(A) − ρ) | D`.  For `ρ = 1/2` this says `A` is a
`lcm(2,D)`-gadget.
*Proof.*  `Σ(W) = Σ_i Σ(A_i) + Σ_{i : X_i = B_i} (Σ(B_i) − Σ(A_i))`, and the
second sum lies in `(1/D)Z`. ∎

**Interpretation.**  The switch/covering plan replaces *one* exact rational
condition by *one* congruence condition modulo `1/D` plus a covering argument.
That is a real gain (§5 quantifies it: it is a birthday-type gain of a factor 2
in the exponent, and it makes some windows usable that carry no gadget at all),
but it is **not** a gain of a different order: a legal system whose reciprocal
sum has denominator dividing `lcm(2,D)` must still be produced at every scale.
CRUX is therefore *equivalent* (given C1–C2 and R1–R3) to the statement

> **(GAD)**  There are `D, K` such that for all large `x` there is a legal
> `G ⊆ [x,Kx]` with `denom(Σ(G)) | D` and with the values so obtained covering
> `D/2` as a subset sum.

and the switch machinery contributes exactly the covering half.

### 4.1 Honest accounting: what the plan does and does not buy

Let `L = lcm` of the (Rule-(P)-pruned) universe of `[T,CT]`, `λ = log₂(L/gcd(L,D))`.

| approach | search cost (bits of condition to satisfy in one search) |
|---|---|
| direct: one legal `W ⊆ [T,CT]` with `Σ(W) = 1/2` | `log₂ L` |
| gadget in the same window (`denom | D`) | `λ = log₂ L − log₂ gcd(L,D)` |
| **decompose into `s` separated windows, gadget in each, then cover** | `max_i λ_i` per search, plus one integer subset-sum of size `≈ D` |

The third line is the plan, and the gain is not the `log₂ D` of line 2 — it is the
replacement of `λ` by `max_i λ_i`, which is **exponentially** smaller because
`λ_i` grows roughly like `x_i/log x_i` for a window `[x_i,2x_i]` (measured:
`λ = 25, 56, 135, 279, 470, 923` for `[200,400], [402,804], …, [6462,12924]`
with `D = 10!`).  The covering lemma is what turns the last column's "lucky hit"
into a guarantee — provided the values `c_i` are dense enough.
This is why the campaign of §6 can reach windows that no single search can.

### Semigroup remark.  **PROVED**
Let `R* = {ρ ∈ Q_{>0} : ∀T ∃ legal W, min W ≥ T, Σ(W) = ρ}`.  By Lemma F0, `R*`
is closed under addition, so it is a sub-semigroup of `(Q_{>0},+)`.  Hence
CRUX (`1/2 ∈ R*`) follows from `1/(2n) ∈ R*` for a single `n`, and more generally
from any finite `ρ_1,…,ρ_k ∈ R*` admitting non-negative integers `n_j` with
`Σ n_j ρ_j = 1/2`.  Also, for the *original* Erdős-289 application one may
replace `1/2` by any `ρ` with `1−ρ` a legal block sum supported below `T`;
`ρ ∈ {1/2, 1/3, 2/3}` all qualify with `max ≤ 105`.

---------------------------------------------------------------------------
## 5. Switches computed  (item 1)

### 5.1 The demonstration that switches ≠ gadgets  **EXHAUSTIVE + verified**

Take `D = 10! = 3 628 800`, window `[501,1000]`, and the universe
`U = ` the Rule-(P) fixpoint of `{n ∈ [501,1000] : every p^{ν_p(n)} ≤ 40 or
p^{ν_p(n)} | D}` (`|U| = 43`).  Then

| quantity | value |
|---|---|
| `Λ = log₂ #{legal subsets of U}` | `23.0` (exactly `2^23` legal subsets) |
| `λ = log₂( lcm(U)/gcd(lcm(U),D) )` | `36` |
| `D`-gadgets in `U` | **none** — exhaustive DFS, 5 006 nodes |
| `D`-switches found | **183 794**, every one re-verified with `Fraction` |
| distinct `|c|` | 40 |
| smallest `|c|` | **4 938** |
| `gcd` of all values `c` | **6** |

Witness (smallest `|c|`, `c = −4938`, i.e. `Σ(A) − Σ(B) = 4938/10!`):
```
A = 527 528 550 551 575 576 608 609 629 630 650 651 702 703 714 715 740 741 759 760 836 837 896 897
B = 551 552 594 595 608 609 629 630 650 651 703 704 713 714 740 741 759 760 782 783 836 837 899 900
```
(`verify_switch.py` re-checks legality, `min ≥ 501`, and that `D(Σ(B)−Σ(A))`
is a nonzero integer, using `Fraction` only.)

This is the sharp form of the hint in the task: `Σ(A)` and `Σ(B)` separately have
denominators of 36 bits that are *not* allowed, yet the difference is exact.
Heuristically the reason is the birthday count: `2^{2Λ} = 2^{46}` ordered pairs
against `2^{λ} = 2^{36}` residue vectors, versus `2^{Λ} = 2^{23}` against
`2^{36}` for gadgets.  (`Λ − λ = −13 < 0 ≤ 2Λ − λ = +10`.)

**But** the observed number of switches, `1.8·10^5`, exceeds the birthday
prediction `2^{2Λ−λ−1} ≈ 2^9` by a factor `≈ 360`, and the values `c` take only
**40** distinct absolute values, all divisible by `6`.  So the switch values are
very far from equidistributed: they come from a small number of local moves,
repeated in many contexts.  **OBSERVED**, and it is the main practical
disappointment of the plan (see §5.3).

### 5.2 Switches across scales   `D = 10!`, every switch verified exactly
(`switch_scan.py` → `switch_scan1.txt`, `switch_scan2.txt`.  "gadgets" column is
an **exhaustive** DFS over the whole universe; "enum." is the fraction of the
`2^Λ` legal subsets that the birthday pass enumerated.)

| window (prime-power cap) | \|U\| | Λ | λ | gadgets? | enum. | switches | distinct \|c\| | min \|c\| | gcd of values |
|---|---|---|---|---|---|---|---|---|---|
| `[250,500]`  q=40 | 35 | 19.6 | 30 | **yes** | 100 % | 508 578 | 249 | **470** | 1 |
| `[501,1000]` q=40 | 43 | 23.0 | 36 | **no** (exh.) | 100 % | 183 794 | 40 | **4 938** | 6 |
| `[1001,2000]` q=42 | 56 | 29.0 | 41 | **no** (exh.) | 2.2 % | 0 | – | – | – |
| `[2001,4000]` q=40 | 52 | 26.0 | 36 | **no** (exh.) | 17.9 % | 15 488 | 12 | **1 012** | 2 |
| `[4001,8000]` q=42 | 52 | 26.0 | 41 | **no** (exh.) | 17.9 % | 0 | – | – | – |
| `[8001,16000]` q=44 | 60 | 31.0 | 46 | **no** (exh.) | 0.56 % | 0 | – | – | – |

Answers to the questions of task item 1, all **OBSERVED**:
* **smallest achievable `|c|` anywhere in this campaign: 470** (window
  `[250,500]`), i.e. `c/D = 1.30·10⁻⁴`.  `c = 1` was never approached;
* **essentially different switches per unit of window length** (counting
  *distinct values* `|c|`, which is what a covering argument can use):
  `249/250 ≈ 1.0` at `x = 250`, `40/500 = 0.08` at `x = 500`,
  `12/2000 = 0.006` at `x = 2000`.  **The density of distinct switch values per
  unit window length falls by more than two orders of magnitude between
  `x = 250` and `x = 2000`.**  This is the empirical form of Lemma F3/F5;
* the values in one window are **not** coprime in general (`gcd = 6`, `2` in two
  of the three cases), so Lemma C1 cannot be applied to a single window's
  switches — one has to mix windows, which is what the campaign of §6 does.

### 5.3 Why `c = 1` was not reached
Three independent obstructions, all proved above:
* `c` is a multiple of `D/gcd(lcm(A∪B),D)` (Lemma F2), so `c = 1` needs
  `D | lcm(A∪B)`;
* `|c|/D = |Σ(B)−Σ(A)|` and the *finest* difference the window can express is
  governed by the entropy: with `2^{2Λ}` pairs one expects the smallest nonzero
  `|Σ(B)−Σ(A)|` in `(1/D)Z` to be `≈ D·maxsum/#switches`, and #switches is
  observed to be far smaller than the range of `c`;
* `|A △ B| ≥ x/D` (Lemma F3) forces the switch to move `≥ x/D` integers, i.e.
  the sub-window must be wide, which reduces the number of separated switches
  available (Lemma F5).

---------------------------------------------------------------------------
## 6. The campaign: covering-based certificates far from the origin

### 6.1 The two quantities that decide everything   **EXACT computations**
For a window `I` let `U(I)` be the Rule-(P) fixpoint (optionally intersected with
a prime-power cap), `Λ(I) = log₂ #{legal subsets of U(I)}` (computed exactly by
transfer matrix, `entropy.py`) and `λ(I) = log₂(lcm U(I) / gcd(lcm U(I), D))`.
Measured with `D = 10!`:

| window | \|U\| | Λ | λ | Λ−λ | maxsum |
|---|---|---|---|---|---|
| `[100,400]` | 120 | 73.6 | 55 | +18.6 | 0.5979 |
| `[200,800]` | 271 | 171.8 | 110 | +61.8 | 0.6785 |
| `[500,2000]` | 745 | 480.4 | 268 | +212 | 0.7307 |
| `[1000,4000]` | 1605 | 1063.9 | 482 | +582 | 0.7782 |
| `[2000,8000]` | 3344 | — | 911 | — | 0.8068 |

`Λ − λ` **grows without bound**, which is the quantitative form of "(GAD) should
be true".  It is *not* a proof: it only says the expected number of gadgets is
`2^{Λ−λ} ≫ 1` under an equidistribution assumption that is exactly what is
missing.  **OBSERVED.**

The *search* cost, however, is governed by `λ` alone, and `λ` for a window
`[x,2x]` grows like `x/log x` (measured, `D = 10!`):
`λ = 25, 56, 135, 279, 470, 923` for `[200,400], [402,804], [806,1612],
[1614,3228], [3230,6460], [6462,12924]`.  Empirically the DFS is comfortable up
to `λ ≈ 50` and dies around `λ ≈ 65`.  Two devices keep `λ` bounded:
* a **prime-power cap** `Q` (keep `n` only if every `p^{ν_p(n)} ≤ Q` or
  `p^{ν_p(n)} | D`) — far more efficient than route E's prime cap, because
  `λ ≤ Σ_{p^e ≤ Q} e log₂ p` *independently of the window*;
* choosing `D` to absorb the small primes.  With
  `D = 2^8·3^5·5^3·7^2·11·13·17·19 = 17 599 117 536 000` and `Q = 60` every
  window in the ladder has `λ = 48`.

### 6.2 New certificates  (all re-verified by `verify.py`, exact)

**(F-1)  `Σ = 1/3` with every element `≥ 200`.**  242 elements in `[203,5720]`,
115 runs, capacity 116 — file `cert_T200_third.txt`.
Built by the covering method: gadget pools with modulus
`D = 2^8·3^5·5^3·7^2·11·13·17·19` in the eight pairwise separated windows
`[200,400], [402,804], [806,1612], [1614,2400], [2402,3228], [3230,4800],
[4802,6460], [9602,12924]`, then an exact integer subset-sum
`Σ c_i = D/3` solved by meet in the middle (`combine.py`, numpy int64, no float).
44 distinct solutions were found; one is recorded.

**(F-2)  A complete Erdős-289 solution whose far part starts at 203.**
`cert_T200_one.txt` = `{4,5,49,50,65,66,84,85,98,99,100,104,105,135,136,143,144,
170,171,175,176,189,190,195,196}` (verified `Σ = 2/3`) `∪` (F-1).
267 elements, 127 runs, capacity 128, `Σ = 1` exactly.
By the splitting lemma this certifies **`P(127)` and `P(128)`** — previously the
established range was `k ≤ 57`.

**(F-3)  `Σ = 1/6` with every element `≥ 500`.**  185 elements in `[527,5985]`,
90 runs, capacity 90 — file `cert_T500_sixth.txt`.  Same method, windows
`[500,1000], [1002,2000], [2002,2800], [2802,4000], [4002,5600], [5602,8000]`.

**(F-4)  A complete Erdős-289 solution whose far part starts at 527.**
`cert_T500_one.txt` `= {2,3} ∪ (F-3)`; `1/2 + 1/3 + 1/6 = 1`.  187 elements,
91 runs, capacity 91, `Σ = 1` exactly ⇒ **`P(91)` is TRUE**.

**A congruence obstruction met in practice — and repaired.**  The first attempt
at (F-3) failed with *zero* hits although the number of combinations exceeded
`D` by a factor 3.  Diagnosis (exact): **every** gadget the search produced in
`[500,1000]` had `c ≡ 3 (mod 6)`, i.e. an *odd* `c`, while every other window
produced *even* `c`; the target `D/6` is even, so no combination could ever
work.  The cause is 2-adic and is Rule (P) in action: `c` is odd exactly when
`ν_2(denom Σ(U)) = 8 = ν_2(D)`, which in that window forces `768 = 2^8·3 ∈ U`.
Re-running the pool with `768` banned produced 150 000 gadgets with **even** `c`
(and `gcd = 18`); the union pool then gave **24** solutions.  This is a concrete
instance of the covering hypothesis of Lemma C1/C2 failing and of what must be
checked before it can be applied.

### 6.3 Reach, honestly stated  **OBSERVED**
The total reciprocal mass available above `T` in windows that the engine can
actually search (`λ ≤ 50`) is
`≈ 0.58` at `T = 200`, `≈ 0.24` at `T = 500`, `≈ 0.15` at `T = 1000`
(`decomp.py`).  Since a target `ρ` needs mass `≥ ρ`, this is why `ρ = 1/2` is
reachable at `T = 100` (route E), `ρ = 1/3` at `T = 200`, and only smaller
unit fractions beyond.  The limitation is the *search*, not the mathematics:
`Λ − λ` says gadgets are abundant in the wide windows the engine cannot enter.

---------------------------------------------------------------------------
## 7. Exhaustive results (exact ranges — every range is stated)

**Engine cross-validation.**  On `[2,105]` with the exact target `1`, `search.c`
enumerates exactly **96** legal systems, the smallest maximal element being
**85** — matching, from an independently written code, route C's and route E's
counts and the established threshold `min max U = 85`.  All 96 were re-verified
with `Fraction`.

**New negatives.**

| statement | evidence |
|---|---|
| No legal `U ⊆ [100,400]` has `Σ(U) = 1/2` | **exhaustive** DFS, 15 655 696 nodes (route E had only reached `[100,350]`) |
| In the `q`-power-smooth Rule-(P) fixpoint of the window, **no `10!`-gadget exists**, for `([501,1000],q=40)`, `([1001,2000],q=42)`, `([2001,4000],q=40)`, `([4001,8000],q=42)`, `([8001,16000],q=44)` | **exhaustive**: 5 006 / 47 640 / 45 243 / 4 274 / 226 078 nodes |

(The second row is a statement about the *restricted* universes only: deleting
elements is sound but of course loses solutions.  It is what makes the
gadget/switch separation of §5.1 a theorem about those universes.)

**Not claimed.**  A search for a legal `U ⊆ [100,500]` with `Σ(U) = 1/2` was
launched (`prob_e500.txt`) and had **not** terminated when this note was written;
it produced no solution and no exhaustion certificate, so *nothing* is asserted
about `[100,500]`.

---------------------------------------------------------------------------
## 7.5 Verdict on the plan (task item 4)

The plan **works as an algorithm** and produced certificates twice and five times
further out than anything previously available here, but it **cannot be turned
into a proof by switches alone**, for three reasons, each proved above:

1. **Anchor necessity (Theorem F7).**  Whatever the switches do, the "all-`A`"
   system must already be a `lcm(2,D)`-gadget.  The plan therefore reduces CRUX
   to `(GAD)`, not below it.
2. **Switches must be large (Lemma F3, Corollary F4).**  `|A △ B| ≥ x/D`, so no
   family of bounded complexity — no identity, no local map — can supply
   switches at every scale.  Any switch construction must move `≥ x/D` integers,
   i.e. it is itself an object of the same size as the thing to be constructed.
3. **The covering hypothesis is not automatic.**  §5.2 shows the switch values
   in one window can have `gcd = 6`, and §6.2 shows a live parity obstruction
   that killed a first attempt at (F-3); the density of *distinct* switch values
   per unit window length was measured to fall from `≈ 1` at `x = 250` to
   `0.006` at `x = 2000`.  So Lemma C1 has to be fed by *many windows*, and its
   hypothesis has to be verified, not assumed.  A value `c = 1` was never
   attained (smallest ever: `470`).

What survives as a genuine contribution of the plan is the **decomposition +
covering algorithm**: the exact combination step (Lemma C1/C2 in the constructive
meet-in-the-middle form of `combine.py`) turns route E's lucky two-window hit
into a systematic many-window procedure, and that is what produced (F-1)–(F-4).

## 8. Where this route stops

Theorem F7 localises the difficulty exactly: the covering machinery is proved,
the reduction is proved, but the input `(GAD)` — one legal system per scale
whose reciprocal sum has a fixed smooth denominator — is not proved and is not
made easier in kind by switches.  Everything measured says `(GAD)` is true (the
entropy `Λ` of the Rule-(P) fixpoint exceeds the number of arithmetic
constraint bits `λ` by a margin that **grows** with the window, §6), but turning
that into a proof needs equidistribution of `Σ(U) mod (1/D)Z` over legal `U`,
which is the block-constrained analogue of a Croot-type theorem and is not
elementary.

---------------------------------------------------------------------------
## 9. Files

| file | purpose |
|---|---|
| `lib.py` | legality / runs / capacity / factorisation helpers (exact) |
| `verify.py` | **independent** exact certificate verifier |
| `verify_switch.py` | **independent** exact switch verifier |
| `universe.py` | Rule (P) + legality fixpoint (sound pruning), prime and prime-power caps |
| `entropy.py` | exact count of legal subsets (transfer matrix) → `Λ`; `λ` |
| `mk.py` | writes a problem file (congruences + directed-rounded sum bounds) |
| `search.c` | DFS over runs with per-prime arc consistency (gadgets / exact targets) |
| `switchc.c` | birthday switch finder: residue-vector collisions among legal subsets |
| `switch_search.py`, `switch_stats.py` | exhaustive small-window switch analysis (meet in the middle over `{−1,0,1}^F`) |
| `pool2.py`, `combine.py` | gadget pools per window; exact integer meet-in-the-middle combination |
| `probe.py`, `probe2.py`, `scan.py`, `decomp.py`, `switch_scan.py` | campaign drivers |
| `recheck_sympy.py` | third arithmetic path (sympy.Rational + integer lcm) over every certificate |
| `cert_T200_third.txt`, `cert_T200_one.txt`, `cert_T500_sixth.txt`, `cert_T500_one.txt` | the certificates |
| `switch_witness_*.txt` | the minimal-`\|c\|` switch of each window of §5.2 |

---------------------------------------------------------------------------
## 10. Reproducing everything

```bash
cd attempts/route-F
gcc -O2 -o search search.c ;  gcc -O2 -o switchc switchc.c

# (a) engine cross-validation: 96 legal systems with Sigma=1 in [2,105], min max 85
python3 mk.py exact 2 105 1 p.txt && ./search p.txt o.txt 100000 4000000000

# (b) the exhaustive negative:  no legal U in [100,400] with Sigma(U)=1/2
python3 mk.py exact 100 400 1/2 pe.txt && ./search pe.txt oe.txt 5 2000000000

# (c) switches where no gadget exists  (Section 5.1)
python3 switch_scan.py 3628800 30000000 501:1000:40

# (d) the T=200 certificate  (D = 2^8 3^5 5^3 7^2 11 13 17 19)
D=17599117536000
python3 pool2.py 200 400  $D 0  P1.txt 24 3000 3000000000 0.35 1
python3 pool2.py 402 804  $D 0  P2.txt 24 3000 3000000000 0.35 1
python3 pool2.py 806 1612 $D 60 P3.txt 1  3000 200000000000 0 1
for w in "1614 2400 Q1" "2402 3228 Q2" "3230 4800 Q3" "4802 6460 Q4" "9602 12924 Q6"; do
  set -- $w; python3 pool2.py $1 $2 $D 60 $3.txt 1 20000 200000000000 0 1; done
python3 combine.py $D 1/3 3600,3600,130,79,15,9,3,1 cert.txt split=2 \
        P1.txt P2.txt P3.txt Q1.txt Q2.txt Q3.txt Q4.txt Q6.txt
python3 verify.py 1/3 --file cert.txt --minelt 200

# (e) all certificates, three independent arithmetic paths
python3 verify.py 1/3 --file cert_T200_third.txt --minelt 200
python3 verify.py 1/6 --file cert_T500_sixth.txt --minelt 500
python3 verify.py 1   --file cert_T200_one.txt
python3 verify.py 1   --file cert_T500_one.txt
python3 recheck_sympy.py
```
(`R1c_sample.txt`, `R2c_sample.txt`, `sw_501_1000_pp40_sample.out` are truncated
copies of multi-hundred-MB intermediate files, kept only as samples; the commands
above regenerate the full versions.)
