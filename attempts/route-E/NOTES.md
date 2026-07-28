# Route E — the CRUX: which rationals are sums of legal systems far from the origin?

All arithmetic below is exact (`fractions.Fraction`, `sympy.Rational`, or integer
arithmetic in C).  Floating point is used **only** inside `estimate.py`, which
produces heuristics that are labelled as such and never enters a certificate or
a negative claim.

Vocabulary: a finite `U ⊆ Z_{≥2}` is **legal** if it has no isolated point.
`Σ(U) := Σ_{n∈U} 1/n`.  A **window** is an interval `[T,N]`.

---------------------------------------------------------------------------
## 0. Headline results

**POSITIVE (new).**  `1/2` **is** the sum of a legal system all of whose
elements are `≥ 100`:

```
1/2 = Σ 1/n over the 145-element legal set with min 104, max 900
104 105 106 111 112 115 116 117 119 120 123 124 132 133 135 136 143 144 145 152 153
161 162 164 165 175 176 184 185 186 187 204 205 207 208 209 220 221 222 230 231 246
247 248 252 253 260 261 264 265 266 279 280 287 288 296 297 318 319 323 324 325 340
341 350 351 352 369 370 371 377 378 384 385 390 391 406 407 408 413 414 429 430 434
435 450 451 455 456 480 481 493 494 527 528 539 540 558 559 560 594 595 608 609 615
616 620 621 629 630 637 638 644 645 650 651 665 666 667 735 736 740 741 774 775 779
780 782 783 805 806 825 826 832 833 850 851 860 861 884 885 896 897 899 900
```
65 maximal runs, capacity 66 ⇒ it realises **exactly `k` blocks for `k = 65, 66`**.
(file `cert_T100_half.txt`; verified three times: by `verify.py`, inside
`hunt.py`, and independently with `sympy.Rational`.)

**NEGATIVE (new, exhaustive).**  See §3.

**STRUCTURAL (new, exhaustive).**  Every natural "sum-preserving push-out move"
that has been proposed fails; see §5.  A counting argument (§5.3) explains why
*any* map of that shape must fail.

---------------------------------------------------------------------------
## 1. Proved lemmas (these are theorems, not heuristics)

### Lemma 1 (power-smoothness of far-out systems).
Let `U ⊆ [T,N]` be legal with `Σ(U) = ρ = u/v`.  Let `p` be a prime with `p ∤ v`.
Then for every `n ∈ U`, `p^{ν_p(n)} ≤ N − T`.

*Proof.*  Let `e = max{ν_p(m) : m ∈ U}`; assume `e ≥ 1`.  Split
`Σ(U) = p^{−e}·Σ_{ν_p(m)=e} 1/(m/p^e) + (terms of ν_p ≥ 1−e)`.  If exactly one
element attained `e`, the first sum would be a `p`-adic unit and
`ν_p(Σ(U)) = −e < 0 = ν_p(ρ)`, a contradiction.  Hence at least two elements of
`U` are divisible by `p^e`; they are distinct multiples of `p^e` inside `[T,N]`,
so `p^e ≤ N−T`.  As `ν_p(n) ≤ e`, done. ∎

### Lemma 2 (two-attainer congruence, quantitative).
In the situation of Lemma 1 let `p^e m_1 < … < p^e m_s` (`s ≥ 2`) be the elements
of `U` with `ν_p = e`.  Then `Σ_i 1/m_i ≡ 0 (mod p)`, equivalently
`e_{s−1}(m_1,…,m_s) ≡ 0 (mod p)`.  Since `0 < e_{s−1} ≤ s·(N/p^e)^{s−1}`,
```
      p  ≤  s·(N/p^e)^{s−1},        2 ≤ s ≤ #{multiples of p^e in [T,N]}.
```
In particular, **if `p^e` has exactly two multiples in `[T,N]` and one of them
lies in `U`, then `p^{e+1} ≤ 2N`.**

*Proof.*  The congruence is the vanishing of the leading `p`-adic term, as in
Lemma 1.  For `s = 2`, `e_1 = m_1+m_2 ≤ 2N/p^e` is a positive multiple of `p`. ∎

Lemma 2 is exactly the deletion rule implemented (in its complete "does *some*
nonempty subset satisfy the congruence" form) in `universe.py`, together with
the legality rule "an element both of whose neighbours are deleted is deleted".
Iterating the two rules to a fixpoint only deletes elements that lie in no
legal solution, so it is **sound**.

### Lemma 3 (doubling / scaling map).
Let `V` be a finite set of integers `≥ 2`, `V = B ⊔ G`, and
`W := {2n, 2n+1 : n ∈ B} ∪ {2m−1, 2m : m ∈ G}`.  Then
* `min W ≥ 2 min V − 1`, `max W ≤ 2 max V + 1`;
* the 2-blocks are pairwise disjoint **iff** no `n ∈ B` has `n+1 ∈ G` (they would
  share `2n+1`); when that holds `W` is legal;
* with `c(k) := 1/(k(k+1))`,
  `Σ(W) = Σ_{n∈V} 1/n − Σ_{n∈B} c(2n) + Σ_{m∈G} c(2m−1)`, because
  `1/(2n)+1/(2n+1) = 1/n − c(2n)` and `1/(2m−1)+1/(2m) = 1/m + c(2m−1)`.

Hence `Σ(W) = Σ(V)` **iff** the *balance equation*
```
      Σ_{n∈B} 2/(4n²−1)  =  Σ_{n∈V} 1/(2n(2n−1))                    (BAL)
```
holds (add `Σ_{n∈V} c(2n−1)` to both sides and use `c(2n−1)+c(2n) = 2/(4n²−1)`).

**If (BAL) had a solution for every `V`, CRUX would be proved**: start from any
`V` with `Σ(V) = ρ`, iterate; the minimum doubles each time.  §5 shows it does
not.

---------------------------------------------------------------------------
## 2. The engine (`search.c`) — how the searches became feasible

`L := lcm(universe)` (enlarged so the target denominator divides it),
`S(W) := Σ_{n∈W} L/n`, so `Σ(W) = S(W)/L`.  **`L` is never formed.**  For each
prime `p` we track only `s_p := S mod p^{E_p−f_p}` — a machine word, because
`p^{E_p} ≤ N`.  (`f_p` = exponent of `p` in a prescribed allowed denominator `D`;
`f_p = 0` in exact mode.)  Two modes:

* **mode 1** (exact): require `S ≡ R0 = (L/v)u` mod every `p^{E_p}`.
* **mode 0** (gadget): require the denominator of `Σ(W)` to divide `D`, i.e.
  `s_p ≡ 0 mod p^{E_p−f_p}` for every `p`.

Key structural fact: `ν_p(L/n) = E_p − ν_p(n)`, so `L/n ≡ 0 mod p^{E_p−f_p}`
unless `ν_p(n) > f_p`.  **Only those elements move `s_p`.**

Prunes, both proved:
* **(P1) size** (mode 1 only): `0 ≤ ρ − (partial sum) ≤ Σ` of `1/n` over the
  remaining universe, evaluated with *integer* fixed-point bounds (scale `2^96`,
  directed rounding) — conservative, hence rigorous.
* **(P2) per-prime arc consistency.**  Let
  `A(p,i) := { Σ_{j∈J}(L/n_j) mod p^{E_p−f_p} : J ⊆ {i,…,cnt−1} }`, computed once
  by a backward subset-sum DP.  Prune unless `(target_p − s_p) mod · ∈ A(p,i)`.
  `A(p,·)` changes only at positions that move `s_p`, so the test costs O(few)
  per node.  (P2) strictly contains the classical "gcd of remaining weights
  divides remaining target" prune.

**Effect of (P2):** exhausting `[100,300]` for the target `1/3` went from
**39,103,586,845 nodes / 12 min** (previous-generation engine `fsearch.c`, kept
in this directory) to **250,952 nodes / 0.04 s** — a factor `1.6·10^5`.
Cross-validation: on `[2,105]`, target `1`, `search.c` enumerates exactly the
**96** legal systems found independently by route C (set equality checked).

---------------------------------------------------------------------------
## 3. Exhaustive negative results (all exact; ranges stated)

| statement | evidence |
|---|---|
| No legal `U ⊆ [100,209]` has `Σ(U)` with a `{2,3}`-smooth denominator (in particular `≠ 1/2, 1/3, 1`) | RULE A + legality fixpoint makes the universe **empty** |
| The same for `[200,380]`, and the first nonempty windows are `[100,210]`, `[200,400]` | fixpoint |
| No legal `U ⊆ [100,280]` with `Σ(U) = 1/3` | exhaustive, 1.53·10⁹ nodes (old engine) |
| No legal `U ⊆ [100,300]` with `Σ(U) = 1/3` | exhaustive, 3.91·10¹⁰ nodes (old engine) **and** 2.51·10⁵ nodes (new engine) — two independent codes agree |
| No legal `U ⊆ [100,350]` with `Σ(U) = 1/2` | exhaustive, 11 814 nodes |
| No legal `U ⊆ [100,400]` with all elements 45-smooth and `Σ(U) = 1/2` | exhaustive, 1.418·10⁷ nodes |
| No legal `U ⊆ [100,350]` with all elements `y`-smooth, `y ≤ 70`, and `Σ(U)=1/2` | exhaustive |
| No legal `U ⊆ [200,800]` with all elements 60-smooth and `Σ(U) = 1/2` | exhaustive, 2.68·10⁵ nodes |

(The `y`-smooth statements are about the restricted universe only; deleting
elements is sound but of course loses solutions.)

---------------------------------------------------------------------------
## 4. The method that produced the certificate

Direct exact search for `Σ(U) = 1/2` inside one window fails: `[100,400]` has
`log₂ L = 81` while the number of legal subsets is only `2^{86}`, so the
*expected* number of solutions is `≈ 2^0` (see `estimate.py`) — right at the
threshold — and the tree is far too large to exhaust.

The working method is **two-scale**:

1. **Gadgets.**  In a window `W₁` search (mode 0) for legal systems whose sum has
   denominator dividing a fixed smooth `D` (we used `D = 10! = 3 628 800`).  This
   relaxes one exact `81`-bit condition to a `60`-bit one, and gadgets become
   plentiful: `[100,400]` yields ≈ 45 **distinct** gadget values per second
   (17 358 distinct values collected; `pool_A.txt`).
2. **Exact combination.**  Search a disjoint higher window `W₂` (here
   `[401,900]`, restricted to 60-smooth elements to keep `log₂(L/D) = 64`) for
   gadgets `σ₂`, and test whether `1/2 − σ₂` occurs in the `W₁` pool.  A union of
   legal systems in disjoint windows is legal, and the sum is exact.

The hit came after 12 `W₂`-gadgets (≈ 5 min): `σ₁ = 33409/86400`,
`σ₂ = 9791/86400`, `σ₁+σ₂ = 43200/86400 = 1/2`.

Files: `mk.py` (universe + problem file), `search.c`, `pool.py`, `hunt.py`,
`combine.py`, `tune.py`, `estimate.py`, `sweep.py`.

### Tuning rules discovered
* With a prime cap `y`, `log₂ L` grows only **logarithmically** in `N` (all
  exponents `E_p` are `≤ log_p N`), while `maxsum` keeps growing.  So very wide
  capped windows are cheap.  Example: `[100,1000] y=35` has `|U| = 170`,
  `maxsum = 0.593`, `log₂L = 61`.
* Empirically the mode-0 search is comfortable while `log₂(L/D) ≲ 65` and dies
  around `75`.  The mode-1 search is comfortable while `maxsum/ρ ≲ 1.2`.
* `estimate.py` predicts `log₂ E[#solutions]`; the predictions matched every
  exhaustive outcome above (negative where it predicted `< 0`).

---------------------------------------------------------------------------
## 5. Scaling maps: a precise no-go

### 5.1 No push-up relations between block sums
`H(a,b) := Σ_{n=a}^b 1/n`.  Searched exhaustively (61-bit fingerprint + exact
confirmation, `relations.py`):
* `H(a,b) = H(c,d)` with `c > b`: **no solutions** for `b ≤ 30`, all elements `≤ 400`.
* `H(a,b) = H(c,d) + H(e,f)` with `b < c ≤ d < e ≤ f`: **no solutions** for
  `b ≤ 20`, all elements `≤ 250`.

So a block cannot be traded for blocks strictly further out, even with two.

### 5.2 The doubling map never preserves the sum on a real certificate
`scale_test.py` decides (BAL) exhaustively over all `2^{|V|}` admissible splits:

| `V` | result |
|---|---|
| all **96** legal `U ⊆ [2,105]` with `Σ(U)=1` | **0** admit a balanced doubling |
| the `1/2` certificates (max 91, max 105) | 0 |
| the `1/3` certificates (max 105, max 100) | 0 |
| the `2/3` certificate | 0 |

(The bare equation `Σ_{even k} 1/(k(k+1)) = Σ_{odd k} 1/(k(k+1))` *does* have
solutions — e.g. `1/(8·9)+1/(14·15) = 1/(7·8)+1/(35·36) = 47/2520`, found by
`balance.py` — but they never arise as a *partition* of a certificate.)

### 5.3 Why every such map must fail (counting)
A "local" push-out map assigns to each `n ∈ V` one of `c` blocks near `mn`.  It
produces `c^{|V|}` candidate systems, and requires one exact rational identity.
The sum of the produced system has denominator whose relevant part is of size
`≈ Π_{n∈V} (mn)²`, i.e. `≈ 2 log₂(mN)` bits **per element**.  Break-even needs
```
      log₂ c  ≳  2 log₂ (m·max V),
```
i.e. `c ≳ (m·max V)²`.  With the doubling map `c = 2` and `m·max V ≈ 200`: the
constraint is over-determined by a factor `≈ 15`.  To break even one must allow
`≈ (mN)²` offsets per element, i.e. blocks placed anywhere in a range of length
`(mN)²` — but then the elements are of size `(mN)³` and the same inequality
reappears one scale up.  **The freedom and the constraint grow at the same
rate**; no local map of this type can work.  This is the precise reason the
"+1 block" move (route B), the two-atom split, and the doubling map all fail.

### 5.4 Why greedy fails
For unit fractions the Fibonacci–Sylvester step `r ↦ r − 1/⌈1/r⌉` strictly
decreases the numerator.  For a pair block `{a,a+1}` of value
`(2a+1)/(a(a+1))`, the greedy step from `r = u/v` with minimal admissible `a`
gives numerator `u' = u·a(a+1) − v(2a+1)`, and minimality only yields
`u' < 2u a²/(2a−1) ≈ u·a`.  **The numerator can grow by a factor `a`.**  So the
standard termination proof breaks at the very first step; block-greedy is not a
finite algorithm.

---------------------------------------------------------------------------
## 6. Status of the CRUX

**What the data says.**  For a window `[T,N]`, let `Λ(T,N) := log₂` (number of
legal subsets) and `λ := log₂ L`.  Solutions to `Σ = ρ` exist as soon as
`Λ − λ` is comfortably positive (`estimate.py` refines this with the sum
distribution).  Measured:

| window | `\|U\|` | `maxsum` | `log₂L` | `Λ` | `Λ−log₂L` |
|---|---|---|---|---|---|
| `[100,400]` | 135 | 0.665 | 81 | 86 | 5 |
| `[100,450]` | 156 | 0.728 | 87 | 100 | 13 |
| `[100,500]` | 192 | 0.836 | 99 | 124 | 25 |
| `[100,600]` | 247 | 0.973 | 114 | 161 | 47 |
| `[100,800]` | 385 | 1.294 | 154 | 257 | 103 |
| `[200,1600] y=45` | 287 | 0.546 | 82 | 184 | 102 |
| `[500,4000] y=45` | 337 | 0.270 | 83 | 202 | 119 |
| `[1000,8000] y=45` | 388 | 0.158 | 97 | 172 | 75 |

The gap `Λ − log₂L` **grows without bound** as the window widens, at every `T`
tested.  Together with the fact that the `p`-adic conditions of Lemma 2 are
satisfiable for every prime that survives the fixpoint, this is strong evidence
that **CRUX is TRUE**: for every `ρ > 0` and every `T` there is a legal system
with elements `≥ T` and sum `ρ`, with `max ≈ C(ρ)·T`.  It is **not proved here**.

**What is missing for a proof.**  Exactly a block analogue of Croot's theorem:

> *(Representation Lemma, open here)*  There are `C` and `D` such that for all
> large `T` and every rational `ρ ∈ (1/C, 1)` whose denominator divides `D`,
> `ρ` is the sum of a legal system with elements in `[T, CT]`.

Every mechanism tried in this route reduces to it, and §5 shows no *local*
algebraic move can supply it: one needs a genuine counting/`p`-adic
equidistribution argument (choose, for each prime `p ≤ (N−T)/log N`, which
multiples of `p` to include so that Lemma 2's congruence holds, and show the
residual smooth part can be corrected).  That step — proving the choices for
different primes can be made *simultaneously* — is where an elementary attack
stops: the choices interact because one integer is a multiple of many primes,
and the legality constraint ("`n ∈ U ⟹ n±1 ∈ U`") couples neighbouring
integers, which destroys the independence a sieve/second-moment argument needs.

---------------------------------------------------------------------------
## 7. Reach of the method (honest limits, measured)

The two-scale method needs, for the target `ρ`, a set of **disjoint** windows
above `T` whose total available sum exceeds `ρ` and each of which is cheap
enough to search.  "Cheap" means (measured on this machine)
`log₂(L/D) ≲ 65` in gadget mode, or `maxsum/ρ ≲ 1.2` with `log₂L ≲ 85` in exact
mode.  Both quantities are forced by the window:

| `T` | cheapest windows with `log₂(L/D) ≤ 65` | their total `maxsum` | `ρ = 1/2` reachable? |
|---|---|---|---|
| 100 | `[100,400]` (60) + `[401,900] y=60` (64) | 0.673 + 0.224 = 0.897 | **yes — certificate found** |
| 200 | `[200,900] y=50` (60) + `[901,3200] y=45` (60) | 0.489 + 0.127 = 0.616 | tight: `σ₁` must sit in the top 25 % of window 1 |
| 500 | `[500,4000] y=45` (63) | 0.270 | no (total ≈ 0.32 < 1/2); `ρ = 1/4` is in range |
| 1000 | `[1000,8000] y=45` (75) | 0.158 | no; `ρ = 1/6` or `1/8` is in range |

So with the present engine, `ρ = 1/2` is demonstrated at `T = 100`; for
`T = 200` it is borderline and for `T = 500, 1000` the *cheap* windows can only
reach smaller `ρ` (`1/4`, `1/6`, `1/8`).  This is a limit of the SEARCH, not a
mathematical obstruction: `estimate.py` predicts, e.g.,
`2^{24.5}` legal systems in `[200,3200]` (42-smooth) with sum `1/2`,
`2^{93.8}` in `[200,3200]` (43-smooth),
`2^{14.6}` in `[500,4000]` (45-smooth) with sum `1/4`,
`2^{89.4}` in `[500,8000]` (50-smooth) with sum `1/3`,
`2^{36.3}` in `[1000,16000]` (45-smooth) with sum `1/6`.
Exact searches for those were launched (`y200.txt`, `y200b.txt`, `y500.txt`,
`w1000.txt`) and had not terminated when this note was written; the machine was
running at load 25+ on 4 cores, i.e. each search received under 25 % of one core.

## 8. Files

* `verify.py`      — independent exact verifier (sum, `≥ T`, no isolated point, runs, `r`, `cap`).
* `universe.py`    — RULE A + legality fixpoint (`build`, `build_with_banned`).
* `mk.py`          — writes a problem file (exact target, or "denominator divides `D`", optional prime cap).
* `search.c`       — the engine (§2).  `fsearch.c` is the previous generation, kept for cross-checking.
* `pool.py`        — collects and re-verifies a pool of gadgets in a window.
* `hunt.py`        — two-window exact combination (this produced the certificate).
* `combine.py`     — k-window exact combination by meet-in-the-middle.
* `tune.py`, `estimate.py`, `sweep.py`, `scan.py` — window/parameter selection and heuristics.
* `scale_test.py`, `balance.py`, `relations.py` — the no-go results of §5.
* `cert_T100_half.txt`, `pool_A.txt`, `all_2_105.txt` — data.

---------------------------------------------------------------------------
## 9. Reproducing the certificate

```bash
gcc -O2 -o search search.c
# window 1: gadgets with denominator dividing 10! in [100,400]
python3 pool.py 100 400 3628800 100 400000 pool_A.txt A 3 0
# window 2: problem file for [401,900] restricted to 60-smooth elements
python3 mk.py 401 900 0 1 1 3628800 prob_C_401_900.txt 60
# hunt: gadget sigma2 in window 2 with 1/2 - sigma2 in the window-1 pool
python3 hunt.py 1/2 pool_A.txt prob_C_401_900.txt 100000 400000 101
# independent check
python3 verify.py 1/2 $(cat cert_T100_half.txt) --minelt 100
```

## 10. Search status at the end of the session

Launched and still running when the session ended (the machine was shared:
load 25+ on 4 cores, so each process received well under one core):

| file | window | cap | target | `log₂L` | predicted `log₂E[#sol]` | status |
|---|---|---|---|---|---|---|
| `y200.txt`  | `[200,3200]` | 42 | `1/2` | 81 | 24.5 | no result in 28 min |
| `y200b.txt` | `[200,3200]` | 43 | `1/2` | 86 | 93.8 | no result in 15 min |
| `t200third.txt` | `[200,1600]` | 37 | `1/3` | 70 | 29.1 | no result in 17 min |
| `y500.txt`  | `[500,4000]` | 45 | `1/4` | 83 | 14.6 | no result in 50 min |
| `w1000.txt` | `[1000,16000]` | 45 | `1/6` | 117 | 36.3 | stopped to free CPU |

None of these produced a NEGATIVE result either (they were not exhausted), so
nothing is claimed about them.
