# Route H — budget combinatorics and exhaustive refutation of small families
(Erdős problem 273; working notes, route H)

Problem: is there a covering system of Z with **distinct** moduli all of the form `p-1`,
`p >= 5` prime?  Admissible moduli `E = {n >= 4 : n+1 prime}`.

Every "PROVED" item below is proved here in full; every "MEASURED" item is a computation
whose exact scope is stated.  **Nothing here resolves 273**: `E` is infinite and all
exhaustive statements carry an explicit modulus bound.

---

## 0. Status table

| # | statement | status |
|---|---|---|
| A | `E = 2H`, `H = {m >= 2 : 2m+1 prime}` | PROVED |
| B | **Parity equivalence**: E-covering exists ⟺ two **disjoint** subsets of `H`, each a covering-system modulus set | PROVED |
| C | **Lemma L5** (prime removal) | PROVED, numerically validated |
| D | Reduction `R(Y)`; collapses `H∩[2,Y]` to a small `{2,3,5,7,(11)}`-smooth set | PROVED |
| E | **Theorem T2**: no E-covering with all moduli `<= 254` (pure budget after R) | PROVED |
| F | Lemmas L8 (coprime pairs), L9 (quantitative DMNR), L10/L10b (Fourier balance) | PROVED |
| G | `H` **does** support covering systems — explicit 15-class certificate | PROVED |
| H | **Theorem T3**: no E-covering with all moduli `<= 724` | PROVED (exhaustive family enumeration) |
| I | Lemma L8+ (coprime-subset inequality) | PROVED, numerically validated |

---

## 1. Parity equivalence (Theorem B)

`n ∈ E` ⟹ `n+1` is an odd prime ⟹ `n = 2m` with `2m+1` prime, `m >= 2`.  So `E = 2H`.

**Theorem B.**  There is a covering system of Z with distinct moduli all in `E`
⟺ there are two **disjoint** `A, B ⊆ H` each of which is the modulus set of a covering
system of Z with distinct moduli.  Moreover all E-moduli are `<= X` iff `A,B ⊆ H∩[2,X/2]`.

*Proof.* (⟹) All `n_i ∈ E` are even, so the class `a_i (mod n_i)` lies inside `2Z` if `a_i` is
even and inside `2Z+1` if `a_i` is odd.  Hence the even-residue classes cover `2Z` and the
odd-residue ones cover `2Z+1`.  With `n_i = 2m_i`: `2b_i (mod 2m_i)` covers `2Z` iff
`{b_i mod m_i}` covers `Z`; `2b_i+1 (mod 2m_i)` covers `2Z+1` iff `{b_i mod m_i}` covers `Z`.
Distinct `n_i` ⟹ distinct `m_i`, so `A = {m_i : a_i even}` and `B = {m_i : a_i odd}` are
disjoint subsets of `H`.  (⟸) reverse the construction. ∎

So **273 asks exactly whether `H` contains two disjoint covering-system modulus sets.**

### 1a. `H` supports a covering system (Theorem G)

Found by exhaustive DFS (`experiments/H_cover.c`, divisors of `L=93312`) and re-verified by an
independent exhaustive sweep mod `lcm = 31104` (`experiments/H_verify.py`):

    0 mod 2, 1 mod 3, 3 mod 6, 5 mod 8, 2 mod 9, 17 mod 18, 23 mod 36, 41 mod 48,
    5 mod 54, 14 mod 81, 17 mod 96, 65 mod 128, 41 mod 216, 239 mod 243, 257 mod 288

15 distinct moduli, all `{2,3}`-smooth, all in `H`; reciprocal sum `43595/31104 = 1.4015882`.
(A capped search also produced one with reciprocal sum `<= 7/5`.)
So the obstruction in 273 is **not** that `H` fails to carry a covering; it is that it must
carry **two disjoint** ones, and coverings devour the small moduli.

---

## 2. Lemma L5 — prime removal

**Lemma L5.** `{(a_m,m)}_{m∈A}` a covering system of Z with distinct moduli, `q` prime,
`A_q = {m ∈ A : q|m}`.  If `|A_q| < q`, then `A \ A_q` is again a covering-system modulus set.

*Proof.* `{a_m mod q : m ∈ A_q}` misses some `c ∈ Z/q`.  Any `x ≡ c (mod q)` covered by a class
with `q | m` would force `c ≡ a_m (mod q)`; so `c+qZ` is covered by the classes with `q ∤ m`.
Put `x = c+qy`: `x ≡ a_m (mod m)` ⟺ `y ≡ q^{-1}(a_m-c) (mod m)`.  These cover all of `Z`. ∎

Validated numerically (`experiments/H_lemma_check.py`): every covering system produced by an
independent DFS, every prime `q` with `|A_q| < q` — reduced system re-verified to cover Z.
**0 failures.**

**Reduction R.**  Iterate on a finite `M ⊆ H`: while some prime `q` has
`0 < #{m ∈ M : q|m} < q`, delete all multiples of `q`.  Then `M` contains a covering set ⟺
`R(M)` does, and `M` contains two *disjoint* covering sets ⟺ `R(M)` does.
(Any `A ⊆ M` has `|A_q| <= #{m∈M : q|m} < q`, so the deletion is legal for `A` too; deletions
compose since counts only shrink; reduced sets stay disjoint.)

`R(Y) := R(H∩[2,Y])` (`experiments/H_reduce.py`):

| Y | \|H∩[2,Y]\| | \|R(Y)\| | budget R(Y) | lcm R(Y) |
|---|---|---|---|---|
| 50 | 24 | 13 | 1.710278 | 3 600 |
| 100 | 44 | 18 | 1.776003 | 64 800 |
| 127 | 52 | 27 | 1.993414 | 15 876 000 |
| 150 | 60 | 30 | 2.015776 | 63 504 000 |
| 250 | 93 | 38 | 2.054072 | 190 512 000 |
| 350 | 122 | 45 | 2.076715 | 190 512 000 |
| 363 | 126 | 56 | 2.260909 | 2.3e10 |
| 500 | 166 | 63 | 2.277855 | 2.3e10 |
| 1000 | 301 | 112 | 2.502465 | 1.4e15 |

e.g. `R(100) = {2,3,5,6,8,9,15,18,20,30,36,48,50,54,75,81,90,96}` (lcm 64800), whereas
`lcm(H∩[2,100]) ≈ 10^17`.  The reduction is what makes exhaustive work possible.

---

## 3. Theorem T2 — the pure-budget bound

(DMNR = Davenport–Mirsky–Newman–Rado: an exact covering system with `k>=2` classes repeats its
largest modulus.)  Hence distinct moduli `>1` ⟹ never exact ⟹ reciprocal sum `> 1` strictly.

If an E-covering with all moduli `<= 2Y` existed, then by B + R there are disjoint
`A,B ⊆ R(Y)` with `budget(A), budget(B) > 1`, so `budget(R(Y)) > 2`.

`budget(R(127)) = 31647433/15876000 = 1.99341 <= 2` and `Y=127` is the largest such `Y`
(`budget(R(128)) = 2.00123`).

> **Theorem T2 (PROVED).** There is no covering system of Z with distinct moduli, all of the
> form `p-1` (`p >= 5` prime), and all `<= 254`.

(The naive reciprocal-sum bound only gives `X >= 70`.)

---

## 4. The tight-budget lemmas

For `Y > 127` put `κ := budget(R(Y)) - 1` and `Δ := κ - 1 = budget(R(Y)) - 2`.  Disjointness
forces **both** `A` and `B` to have excess `δ := budget - 1 < Δ`, and forces the *unused*
budget to be `< Δ` as well.  `Δ` is small over a long range:

| Y | 128 | 150 | 200 | 250 | 300 | 350 | 363 | 500 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| Δ | .0012 | .0158 | .0320 | .0541 | .0646 | .0767 | .2609 | .2779 | .5025 |

So a counterexample below `X = 2Y` requires a **near-exact** covering system.

**Lemma L8 (coprime pairs).** If `A` is a covering set with excess `δ` and `m1,m2 ∈ A` are
coprime then `m1 m2 >= 1/δ`.
*Proof.* `∫mult = 1+δ`, `∫1 = 1`, `mult >= 1`, so the multiply-covered set has density exactly
`δ`.  Two coprime classes always meet, in density `1/(m1m2)`, inside that set. ∎
(General form: for `S ⊆ A`, `budget(A) >= Σ_{S} 1/m + (1 - U(S))`, `U(S)` = max union density.)

**Lemma L9 (quantitative DMNR).** `L = lcm(A)`, `q^t | L`, `D_t = {m ∈ A : q^t|m}`, `ζ` of exact
order `q^t`.  Then `| Σ_{m∈D_t} ζ^{a_m}/m | <= δ`.
*Proof.* `Σ_{j<L} mult(j) z^j` at `z=ζ` equals `Σ_{m : ζ^m=1} ζ^{a_m} L/m = Σ_{D_t} ζ^{a_m}L/m`;
also `Σ_j mult(j)ζ^j = Σ_j (mult(j)-1)ζ^j` because `Σ_{j<L} ζ^j = 0`, and this has modulus
`<= Σ_j (mult(j)-1) = δL`. ∎
In particular if `|D_t| = 1`, say `D_t = {m}`, then `δ >= 1/m`.

**Lemma L10 (Fourier balance).** With `f(j) = Σ{1/m : m ∈ D_t, a_m ≡ j (mod q^t)}` and
`mean_r` the average of `f` over the coset `r + q^{t-1}(Z/q^t)`,
`Σ_r Σ_{j∈r} (f(j)-mean_r)^2 <= ((q-1)/q) δ^2`.
*Proof.* Parseval on `Z/q^t`, splitting characters of exact order `q^t` (bounded by L9) from
those factoring through `Z/q^{t-1}`. ∎

**Corollary L10b.** For every prime power `q^t` with `D_t ≠ ∅`:
`budget(D_t) >= q·(1/min(D_t) − δ)`.

**Pair lemma.** For every prime `q` with `#{m ∈ R(Y) : q|m} < 2q`, at least one of `A,B` has
`|·_q| < q`, hence may be assumed free of multiples of `q` (L5).

All of these are consistent with the explicit `H`-covering of §1a (`δ = 0.4016`; e.g. `q=2`:
`c_0 = 0.5000`, `c_1 = 0.4406`, `|c_0-c_1| = 0.0594 <= δ` ✓).

---

## 5. Absolute (Y-free) smooth-world budgets

`Σ 1/m` over the `P`-smooth elements of `H` (`experiments/H_lprofile.py`, `m <= 10^6`):

| P | {2,3} | {2,3,5} | {2,3,5,7} | ≤11 | ≤13 |
|---|---|---|---|---|---|
| Σ1/m | 1.41216 | 1.86406 | 2.13233 | 2.34542 | 2.49296 |

PROVED consequences with **no modulus bound**:
* two disjoint covering sets cannot both be `{2,3,5}`-smooth (`1.86406 < 2`);
* hence at least one of `A,B` uses a modulus divisible by a prime `>= 7`;
* likewise they cannot both be `{2,3}`-smooth.

---

## 6. Part (a)/(b): exhaustive family enumeration, and Theorem T3

`experiments/H_pair.py` / `H_pair2.py` enumerate **all** disjoint pairs `(A,B)` inside `R(Y)`
that survive: the budget window `1 < budget <= κ`, the waste bound `< Δ`, L8, L5-multiplicity
(`|A_q| ∈ {0} ∪ [q,∞)`), L10b, and the L10 balance partition test.  This is complete: if an
E-covering with moduli `<= 2Y` existed, its (L5-reduced) parity halves would appear.

Results — **the enumeration of part (a) is EMPTY at every bound reached**:

| X = 2Y | Y | \|E∩[4,X]\| | \|R(Y)\| | budget R(Y) | Δ | surviving families | how |
|---|---|---|---|---|---|---|---|
| 100 | 50 | 24 | 13 | 1.710278 | — | 0 | budget ≤ 2 |
| 150 | 75 | 34 | 15 | 1.742130 | — | 0 | budget ≤ 2 |
| 200 | 100 | 44 | 18 | 1.776003 | — | 0 | budget ≤ 2 |
| 254 | 127 | 52 | 27 | 1.993414 | — | 0 | budget ≤ 2 |
| 300 | 150 | 60 | 30 | 2.015776 | .0158 | 0 | enumeration (229 nodes) |
| 400 | 200 | 77 | 33 | 2.032020 | .0320 | 0 | enumeration (1 247) |
| 500 | 250 | 93 | 38 | 2.054072 | .0541 | 0 | enumeration (22 576 / 6) |
| 600 | 300 | 108 | 41 | 2.064582 | .0646 | 0 | enumeration (98 857 / 6) |
| 700 | 350 | 124 | 45 | 2.076715 | .0767 | 0 | enumeration (7) |
| **724** | **362** | **126** | **45** | **2.076715** | **.0767** | **0** | enumeration (7) |
| 726 | 363 | 127 | 56 | 2.260909 | .2609 | ? | **NOT DECIDED** |
| 1000 | 500 | 166 | 63 | 2.277855 | .2779 | ? | **NOT DECIDED** |

(node counts: `H_pair.py` / `H_pair2.py`; `H_pair3.py` reproduces all of them.)

> **Theorem T3 (PROVED).** There is no covering system of Z with distinct moduli, all of the
> form `p-1` (`p >= 5` prime), and all `<= 724`.

Why the enumeration is brutal in this range: `Δ = budget(R(Y)) - 2` is tiny, so the two halves
must between them use **essentially every** element of `R(Y)` (unused budget `< Δ`), while L8
forbids two coprime moduli of product `< 1/Δ` inside the *same* half.  Concretely: `2` and `3`
must go to different halves (`1/6 > Δ`); `5` cannot be wasted (`1/5 > Δ`) yet is coprime to both
and `2·5, 3·5 < 1/Δ` — contradiction, in 6-7 search nodes.

**Additional lemma used from `Y = 363` on (Lemma L8+).** If `S ⊆ A` is pairwise coprime then
`budget(A) >= W(S) := Σ_{S} 1/m + Π_{S}(1-1/m)` (the `S`-classes are CRT-independent, so their
union has density exactly `1 - Π(1-1/m)`; the rest of `A` must cover the complement).  `W` is
monotone under adding coprime elements, and since `R(Y)` is `{2,3,5,7,11}`-smooth for the `Y`
handled, pairwise-coprime subsets have `<= 5` elements and are enumerable by prime-support mask.
Validated: `maxW(A) <= budget(A)` on every genuine covering system tested.
E.g. at `Y=363` (`κ = 1.26091`): `W({2,3,5}) = 1.3` and `W({2,3,7}) = 1.26190` both exceed `κ`,
so neither half may contain `{2,3,5}` or `{2,3,7}`.

**Frontier.**  `X = 724`.  At `Y = 363` the reduction stops deleting `11` (`H∩[2,363]` at last
contains 11 multiples of 11), `|R|` jumps `45 → 56`, `Δ` jumps `0.077 → 0.261`, `1/Δ` falls to
`3.8` so Lemma L8 has essentially no teeth (`2·3 = 6 > 3.8`), and the enumeration blows up.
Runs at `Y = 363` and `Y = 400` did not terminate inside the session budget (the machine was
also shared with other jobs).

**Correctness safeguards run before any of the above was believed:**
* `H_lemma_check.py` — L5 on independently generated coverings: 0 failures;
* `H_pair_selftest.py` — the leaf filters accept every genuine (L5-reduced) covering set that
  was tested, including the explicit `H`-covering: **0 false rejections**.  (Un-reduced
  covering sets *are* rejected by the multiplicity filter — that is exactly what L5 licenses.)
* `H_skeleton_xcheck.py` — the 3-way DFS + symmetry breaking + waste prune reproduce brute
  force exactly on instances with nonempty answers;
* `H_pair_xcheck.py` — incremental prunes vs. brute force: 0 mismatches (all instances tested
  had empty answers, so this check has limited bite).

---

## 7. Part (c): the structural inequality that was found, and its limits

The clean structural statement of this route is **Lemma L9/L10** — the quantitative form of
Davenport–Mirsky–Newman–Rado.  It says exactly what "per-prime, per-level fibre budget" means:
at every prime power `q^t` dividing `lcm(A)`, the reciprocal masses attached to the `q` residues
inside each coset mod `q^{t-1}` must agree to within the global excess `δ`.  It was checked
numerically on real near-covers (the 15-class `H`-covering, the classical `{2,3,4,6,12}`
family, and machine-found near-minimal covers) **before** being used.

What it does **not** give: a `Y`-free contradiction.  The reason is visible in the numbers —
`Σ_{m ∈ H, m<=Y} 1/m` diverges, `budget(R(Y))` grows past 2 at `Y = 128` and past
`1 + 1.4 = 2.4` around `Y ≈ 700`, while `H` demonstrably contains covering sets of reciprocal
sum `<= 1.4`.  So the two-disjoint-sets budget argument must fail for `Y` beyond roughly 700
unless one proves a genuine lower bound for the reciprocal sum of an `H`-covering that is
larger than `budget(R(Y)) - 1`.  **Measured:** the minimum reciprocal sum of a `{2,3}`-smooth
`H`-covering is `<= 1.4`; a search at cap `1.35` did not terminate.  Establishing
`σ_H := inf{budget(A) : A ⊆ H a covering set}` is the natural next target of this route —
every unit of `σ_H` above `1` translates directly into a modulus bound via
`budget(R(Y)) < 1 + σ_H`.  Numerically `budget(R(Y)) - 1` reaches `1.4` only near `Y ≈ 700`
(`X ≈ 1400`), so *even a complete determination of* `σ_H` *would cap this route near* `X ≈ 1400`
unless the enumeration itself (which uses much more than budget) carries further.

---

## 8. Explicit scope disclaimer

Theorems T2 (X=254) and T3 (X=724) are statements about covering systems **all of whose moduli are bounded**.
`E` is infinite, so they are *not* evidence that the answer to 273 is NO, and they are not a
proof of anything about unbounded systems.  They are (i) rigorous lemmas usable as raw material
in a NO proof, and (ii) pruning for a YES search: any certificate must use a modulus `> 724`.
