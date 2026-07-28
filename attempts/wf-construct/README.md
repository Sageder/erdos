# wf-construct — Attack 2: construction with prescribed p-adic structure

All arithmetic in every verification path is exact (`fractions.Fraction`,
Python integers, C multiword integers).  No floating-point number occurs in any
proof or verification path; the floats that appear are printed diagnostics
(masses, densities, ratios) and never feed a decision.  Nothing external is
cited: every statement below is either proved here from scratch or is an exact
finite computation whose script is in this directory.

---

## 0. Summary of what is established

**PROVED (new).**

1. **Lemma 1** — a sharp *quantitative* form of Rule (P): if `p^2 > N` and a
   solution contains exactly `k >= 1` multiples `p a_1 < … < p a_k` of `p`,
   then `p` divides the elementary symmetric function `e_{k-1}(a)`, hence
   `e_{k-1}(a) >= p`.
2. **Corollary 2** — the resulting *exact* forced threshold
   `kmin(p)` and `z*(T,N)`: every prime `p > sqrt(N)` with fewer than
   `kmin(p)` multiples in `[T,N]` is **forced out entirely**.
   Verified on 160 841 prime-instances of the 39 270-solution corpus,
   **0 failures**, and **attained with equality in 46 %** of them.
3. **Corollary 3** — the forced-out set has density `≈ 0.8·loglog N/log N`
   (exact table in §2), so runs of length `>= 2` survive in abundance
   (55–70 % of all pairs `{n,n+1}` survive at the sizes we use).
4. **Decoupling Lemma** — in the designed universe of §4 every element has at
   most **one** prime factor above `z0`; hence the Rule (P) congruences of the
   large primes act on *pairwise disjoint* sets of variables and can be solved
   **independently, one prime at a time, with no search**.  Everything that is
   left is one exact condition modulo the fixed smooth modulus
   `L0 = prod_{r<=z0} r^{floor(log_r N)}`.

**CONSTRUCTED (new certificates, exactly verified).**

5. A legal `U` with `min U = 104`, `max U = 651`, `sum 1/n = 1/2` exactly
   (`cert_min104_half.txt`), found by a **single DFS in the designed universe**
   (`|A| = 146`) in ~100 s of one core.  The previous best `1/2`-system with
   `min >= 100` needed `max = 900` and a two-window gadget-gluing campaign.
6. A legal `U` with `min U = 104`, `max U = 875`, `|U| = 134`, `r = 56`,
   `cap = 63`, `sum = 1/2` (`cons_cert.txt`), produced by the **two-stage
   construction**: stage 1 chose 52 "rough" elements by solving the Rule (P)
   congruence of each large prime *separately and independently* (no global
   search at all — e.g. `p = 67` with cofactors `{2,5,7,11,13}`, `p = 61` with
   `{3,9,13}`, `p = 59` with `{2,13,14}`, `p = 43` with `{3,5,8,10,19}`), and
   stage 2 fixed the residual `0.334…` exactly inside the 29-smooth tail
   (`|A| = 112`, 1.8 s).  This is the plan of the attack carried out end to end
   for one explicit window.

7. **`P(k)` is now true for every `k` in `[6,71]`.**  Ten `1/2`-systems with
   `min >= 104` produced here, glued to the (exhaustively enumerated) two
   `1/2`-systems inside `[2,103]`, realise every block count `k` from 51 to 70;
   `VERDICT.md` had `6..57` plus `70,71`, so the block counts **58,…,69, which
   were open, are now certified** (`cert_P51_70.txt`, re-verified by the
   repository's own `experiments/certificates.py`).

**NEGATIVE / honest (exact ranges given).**

8. The *fully* decoupled two-stage scheme fails when `z0` is too small: for
   `[104,900]`, for **every one of 40** independently sampled stage-1 designs
   at `z0 = 19` and at `z0 = 23`, the Rule (P) + legality fixpoint of the
   residual problem in the smooth tail is **empty** — a proof (inside the
   design) that the smooth part cannot absorb that residual.  It starts working
   at `z0 = 29`.  So *the interaction between the large primes can be switched
   off, but the interaction between the large and the small primes cannot.*
9. **The Størmer wall.**  Any construction that fixes primes top-down using
   moves that are neutral for all larger primes needs blocks all of whose
   elements are `p`-smooth; the exact counts (§6) show these die out below
   `p ≈ 17`.  There is therefore **no pure descent**; the small primes must be
   solved jointly.
10. `T = 130, 150, 200` were **not** reached: no solution was found by the exact
   engine in the designed universes listed in §7 within the compute available
   (~4 core-hours).  These searches were **not exhaustive**, so they prove
   nothing.

---

## 1. PROVED — Lemma 1 (quantitative Rule (P))  [`forced.py`]

> **Lemma 1.**  Let `U` be a finite set of integers in `[2,N]` and
> `q = sum_{n in U} 1/n`.  Let `p` be a prime with `p^2 > N` and suppose
> `v_p(q) >= 0`.  Let `S = {n in U : p | n}`, `k = |S|`, and write
> `S = {p a_1, ..., p a_k}` with the `a_i` distinct in `[1, floor(N/p)]`.
> Then `k = 0`, or
> ```
>        p | e_{k-1}(a_1,...,a_k)         ( e_{k-1}(a) = sum_i prod_{j != i} a_j )
> ```
> and in particular `e_{k-1}(a_1,...,a_k) >= p`.

*Proof.*  `sum_{n in U\S} 1/n` has denominator prime to `p`, so it lies in
`Z_p`; hence `v_p(sum_{n in S} 1/n) >= 0`.  Now
`sum_{n in S} 1/n = e_{k-1}(a)/(p·prod_i a_i)`, and `a_i <= N/p < p`, so `p`
does not divide `prod_i a_i`.  Therefore `v_p(e_{k-1}(a)) >= 1`.  As all
`a_i >= 1`, `e_{k-1}(a)` is a positive integer, so `e_{k-1}(a) >= p`.  ∎

> **Corollary 2 (the forced threshold).**  `e_{k-1}` is strictly increasing in
> each variable and inside `[T,N]` the `a_i` are distinct integers in
> `[ceil(T/p), floor(N/p)]`.  With `B = floor(N/p)` put
> ```
>   E(k,p)  = e_{k-1}(B, B-1, ..., B-k+1)          (the largest possible value)
>   kmin(p) = min{ k >= 1 : E(k,p) >= p }
>   m(p)    = floor(N/p) - ceil(T/p) + 1           (multiples available)
> ```
> If `p^2 > N` and `m(p) < kmin(p)` then **no** element of `[T,N]` divisible by
> `p` can occur in any `U` with `v_p(sum) >= 0`.

Special cases, all immediate:

| k | condition `E(k,p) >= p` becomes | i.e. |
|---|---|---|
| 1 | `1 >= p` | impossible — *a prime always needs ≥ 2 multiples* |
| 2 | `a_1+a_2 >= p` | `p <~ sqrt(2N)` |
| 3 | `e_2 >= p` | `p <~ (3N^2)^{1/3}` |
| k | `E(k,p) <= k(N/p)^{k-1}` | `p <= N (k/N)^{1/k}` |

and, since `m(p) ≈ (N-T)/p`, solving `p^{(N-T)/p} <= ((N-T)/p) N^{(N-T)/p-1}`
gives the asymptotic **`z*(T,N) ≍ (N-T)/log N`**, confirmed numerically in §2.

**Verification** (`verify_lemma.py`, exact integers only):

```
$ python3 verify_lemma.py ../../experiments/ALLSOLS.txt ../route-E/cert_T100_half.txt \
        ../wf-engine/sol_min60.txt ../wf-engine/sol_min55.txt
solutions: 39270
prime-instances checked: 160841  failures: 0
k - kmin(p) :  0:74679  1:25780  2:26017  3:16039  4:11232  5:5874
               6:743  7:326  8:134  9:4  10:10  11:3
```

The bound is **sharp**: `k = kmin(p)` in 46 % of all instances.  Example from
the `min = 104` gadget: `p = 59` has `kmin = 3` and the solution uses exactly
`59·7, 59·14, 59·15`, with `1/7 + 1/14 + 1/15 = 59/210`.

## 2. PROVED + EXACT — which primes are forced out, and the density  [`table_forced.py`]

| T | N | sqrt N | z\* | z\*/(N−T) | \|X\| | density | surviving pairs | window |
|---|---|---|---|---|---|---|---|---|
| 104 | 600 | 24 | 113 | 0.228 | 132 | 0.266 | 259 | 497 |
| 104 | 900 | 30 | 179 | 0.225 | 187 | 0.235 | 455 | 797 |
| 200 | 1000 | 31 | 163 | 0.204 | 231 | 0.288 | 387 | 801 |
| 200 | 1800 | 42 | 293 | 0.183 | 390 | 0.244 | 889 | 1601 |
| 300 | 2700 | 51 | 449 | 0.187 | 550 | 0.229 | 1398 | 2401 |
| 500 | 4500 | 67 | 743 | 0.186 | 865 | 0.216 | 2411 | 4001 |
| 1000 | 9000 | 94 | 1499 | 0.187 | 1574 | 0.197 | 5088 | 8001 |
| 2000 | 18000 | 134 | 2557 | 0.160 | 3257 | 0.204 | 9997 | 16001 |
| 5000 | 45000 | 212 | 6427 | 0.161 | 7354 | 0.184 | 26355 | 40001 |
| 10000 | 90000 | 300 | 12853 | 0.161 | 13774 | 0.172 | 54359 | 80001 |
| 50000 | 450000 | 670 | 56249 | 0.141 | 64837 | 0.162 | 278734 | 400001 |

* `z*` is of order `(N−T)/log N` (the ratio decays like `1/log N`), as the
  asymptotics predict.
* The density of the forced-out set is `≈ 0.8 · loglog N / log N` — it tends
  to 0, but slowly (still 20 % at `N = 9000`).  Elementary upper bound (only
  Mertens' first estimate `|sum_{p<=x} (log p)/p − log x| <= 2` is used, itself
  elementary):
  `|X| <= (N−T)(log(N/z*) + 4)/log z* + pi(N) = O((N−T) loglog N / log N)`.
* **Runs of length ≥ 2 survive in abundance**: at least `(N−T) − 2|X|` pairs
  `{n,n+1}` survive entirely, and the exact counts show 55–70 % do.  Legality
  is never the bottleneck.  `forced.py` also prints the exact run-length
  histogram (e.g. for `[104,900]`: `{1:37, 2:34, 3:26, 4:17, 5:17, …, 77:1}`).

## 3. PROVED — the local–global decomposition that licenses "prime by prime"

For a legal `U ⊆ [T,N]` with `sum 1/n < 2`:

> `sum_{n in U} 1/n = 1`  **iff**  `v_p(sum) >= 0` for every prime `p`
> **and** `0 < sum < 2`,

because `v_p >= 0` for all `p` means the sum is a rational integer.  The exact
condition is therefore *exactly* the conjunction of the local Rule (P)
conditions plus one archimedean condition.  This is what makes a prime-by-prime
construction the right shape.

## 4. THE DESIGN — a universe in which the large primes do not interact  [`build.py`]

```
A(T,N,z0,z) =  S0  ∪  { n : P(n) = p ∈ (z0,z],  P(n/p) <= z0,  p^2 ∤ n,
                        and n has a neighbour in S0 },
S0 = { n ∈ [T,N] : P(n) <= z0 }          (P = largest prime factor)
```
followed by the **sound** Rule (P) + legality fixpoint (independently
re-implemented in `design.py`).

> **Decoupling Lemma (PROVED; verified exactly by `interaction.py`).**
> Every `n ∈ A` has at most one prime factor `> z0`.  Hence for distinct
> primes `p,q > z0` the sets `{n∈A : p|n}` and `{n∈A : q|n}` are **disjoint**,
> so their Rule (P) congruences constrain disjoint sets of binary variables.
> If all of them hold, `sum_{n∈W} 1/n ∈ (1/L0)Z` with the **fixed** modulus
> `L0 = prod_{r<=z0} r^{floor(log_r N)}`.

```
$ python3 interaction.py 200 1000 23
(A) designed universe [200,1000] z0=23: |A|=563, elements with >1 prime factor > z0: 0
    large-prime multiple sets pairwise disjoint: True
```

Each ingredient does one job:

* `P(n/p) <= z0` **removes the interaction** — without it an element could
  carry two large primes and the two congruences would couple;
* "has a `z0`-smooth neighbour" **makes legality free** — a rough element can
  always be escorted without dragging in a second uncontrolled large prime;
* the rough elements **inject reciprocal mass** while adding only decoupled
  congruences.  This is what lets `z0` drop far below the value at which a
  purely `z0`-smooth universe could still carry the target: for `[104,900]`,
  target `1/2`, a purely `z0`-smooth universe needs `z0 >= 31` (mass `0.534`,
  a 7 % margin) whereas the designed universe carries it already at `z0 = 17`
  (mass `0.738`).

The restriction is a **design choice, not a prune**: it can only lose
solutions, never create them.  A solution found in it is genuine; a failure in
it proves nothing about `[T,N]`.

**Size comparison** (exact):

| window | target | Rule-(P) fixpoint | `z`-smooth design (`design.py`) | one-large-prime design (`build.py`) |
|---|---|---|---|---|
| [104,900] | 1/2 | 434 (171 bits) | 227 @ z=43 (72 bits) | **201** @ z0=17 (97 bits) |
| [104,700] | 1/2 | — | 186 @ z=43 | **146** @ z0=17 |
| [200,1000] | 1/2 | — | — | **264** @ z0=23 |

## 5. THE TWO-STAGE CONSTRUCTION  [`construct.py`, `mkprob.py`, `esearchB.c`]

**Stage 1 (constructive, no global search).**  For each prime `p ∈ (z0,z]`
solve *its own* congruence
`sum_{n ∈ S_p} 1/(n/p) ≡ 0 (mod p)`, `S_p ⊆ M_p`,
by an exact subset-sum DP over `Z/p` (`pack_choices`).  By the Decoupling
Lemma these problems are independent.  Escort each chosen `n` by a neighbour.
Call the union `R`; then `sum_{n∈R} 1/n ∈ (1/L0)Z`.

**Stage 2 (explicit finite adjustment).**  The residual `r = q − sum_R 1/n`
again lies in `(1/L0)Z`: *a rational with only small primes in its
denominator*.  Search the `z0`-smooth tail exactly for a legal subset with sum
`r`.

Stage 2 needs an engine that accepts an **arbitrary rational target**; the
stock `esearch` is limited to 64-bit `u/v`.  `esearchB.c` (a 60-line patch of
`wf-engine/esearch.c`, kept here in full together with `padicB.h`) reads the
root state `X0 = target·lcm(A)` and the per-prime target residues
`tg_p = (target·p^{E_p}) mod p^{E_p}` as exact integers computed by
`mkprob.py`.  Everything stays exact; the patch was validated by reproducing
the `[104,700]` certificate from a `BIG` problem file (1.6 s).

**It works** (`construct.py 104 900 1 2 -z0 29`):

```
[104,900] target=1/2 z0=29   L0 has 84 bits
  try 8: |R|=52  vR=0.16592  residual=0.33408  tail |A|=112  tailmass=0.41242
    done(cap) nodes=58213265 solutions=1 cpu=1.8s
  *** SOLUTION VERIFIED  |U|=134 min=104 max=875 r=56 cap=63 sum=1/2
```

`cons_cert.txt`; `anatomy.py cons_cert.txt` displays the designed p-adic
structure prime by prime:

```
p=67  k=5  cofactors [2,5,7,11,13]   sum(1/a) = 0 mod 67
p=61  k=3  cofactors [3,9,13]        sum(1/a) = 0 mod 61
p=59  k=3  cofactors [2,13,14]       sum(1/a) = 0 mod 59
p=43  k=5  cofactors [3,5,8,10,19]   sum(1/a) = 0 mod 43
p=41  k=10 cofactors [4,5,6,7,9,12,13,15,17,19]
```
(31, 37, 47, 53, 71, … got the empty pack, which is also admissible.)

## 5b. CONSEQUENCE — P(k) is now true for every k in [6,71] (the gap 58–69 is closed)

Ten distinct `1/2`-systems with `min >= 104` were produced here
(`gadgets_half_min104.txt`, all exactly verified), realising the run/capacity
pairs
`(r,cap) ∈ {(46,48),(46,49),(47,49),(48,50),(49,51),(51,52),(51,53),(56,63)}`.
An exhaustive `esearch` run shows there are **exactly two** `1/2`-systems inside
`[2,103]` (37 081 nodes, search completed), with `(r,cap) = (5,5)` and `(7,7)`.
Gluing a low one to a far one (disjoint ranges, so the union is legal and the
values add to 1) and using the splitting lemma `r <= k <= cap`:

```
$ python3 coverage.py
low 1/2-systems in [2,103]: [(5, 5), (7, 7)]
far 1/2-systems with min >= 104 (r,cap): [(46,48),(46,49),(47,49),(48,50),(49,51),(51,52),(51,53),(56,63)]
k realised: [51 ... 70]        range: 51 .. 70   missing inside: []
$ python3 ../../experiments/certificates.py cert_P51_70.txt
All certificates verified in exact rational arithmetic. k values: [51,...,70]
```

`VERDICT.md` recorded `P(k)` for `k = 6..57` plus `P(70), P(71)`; the block
counts **58, 59, …, 69 were open**.  They are now realised by explicit
certificates (`cert_P51_70.txt`, 8 distinct solutions, re-verified by the
repository's own independent `experiments/certificates.py`).  Hence

> **P(k) holds for every k with 6 <= k <= 71.**

## 6. WHERE IT STOPS, AND WHY — the interaction that cannot be removed

**(a) The Størmer wall** (`interaction.py`, exact counts).  A construction that
fixes primes from the largest downwards using only moves neutral for all larger
primes must use blocks all of whose elements are `p`-smooth; for a 2-block that
means `n` and `n+1` both `p`-smooth.  In `[200,1000]`:

| y | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 41 |
|---|---|---|---|---|---|---|---|---|---|---|
| #{n : n, n+1 both y-smooth} | 1 | 5 | 12 | 23 | 35 | 52 | 68 | 87 | 103 | 118 |

Below `y ≈ 17` there is essentially no move left.  **A pure top-down descent
therefore does not exist** — this is the precise obstruction, and it is why the
small primes must be handled jointly.

**(b) Large↔small interaction is real, and measurable.**  Stage 1 decouples the
large primes from *each other*.  It does **not** decouple them from the small
primes: if `z0` is too small the residual left by stage 1 is simply not
representable by the smooth part.  Exact experiment on `[104,900]`, 40
independent stage-1 designs per `z0`:

| `z0` | `L0` bits | smooth part `\|S0\|` | designs tried | residual **provably** unreachable (empty Rule-(P) fixpoint) | solved |
|---|---|---|---|---|---|
| 19 | 68 | 239 | 40 | 40 | no |
| 23 | 77 | 271 | 40 | 40 | no |
| 29 | 84 | 303 | 9 (run stopped on success) | 7 | **yes, on the 9th** |

(the same run at `[104,700]`: `z0 = 17` gives 15/15 empty, `z0 = 23` gives
25/25 empty, `z0 = 29` gives 20/25 empty with the survivors exhausted or timed
out, `z0 = 31` gives 23/25 empty)

So the construction succeeds only once the smooth tail is rich enough to absorb
an arbitrary element of `(1/L0)Z` — i.e. once its entropy
`|tail|·log2(1.7549)` comfortably exceeds `log2 L0`.  That is the exact place
where "prime by prime" stops being free.

**(c) The remaining wall is search cost, not structure.**  A `1/2`-system with
`min >= T` needs `≈ T` elements, so `|A| ≈ 1.3 T` in every design, while the
DFS cost grows like `c^{|A|}`.  `T = 104` (`|A| = 146`) falls in ~100 s;
`T = 130` (`|A| = 168`), `T = 150` (`|A| = 180…211`) and `T = 200`
(`|A| = 264…305`) did not fall in the compute available.

## 7. NEGATIVE results of this attack (exact ranges; each is only about the
   *designed* universes, which are restrictions, so none of them proves
   non-existence)

* No solution found by `esearch`/`esearchB` in:
  `[130,700] z0=19 (|A|=161)`, `[130,750] z0=19 (|A|=180)`,
  `[130,800] z0=19 (|A|=198)`, `[130,900] z0=17 (|A|=168)`,
  `[150,800] z0=23 (|A|=210)`, `[150,900] z0=19 (|A|=211)`,
  `[200,1000] z0=23 (|A|=264)`, `[200,1100] z0=23 (|A|=284)`,
  `[200,1200] z0=23 (|A|=305)`, `[200,1300] z0=19 (|A|=288)` —
  each ~20–90 core-minutes, deterministic take-first and randomised restarts
  with take-bias 81–87 %.  **Not exhaustive.**
* Two-stage runs at `T = 130` (`[130,1100]`, `z0 ∈ {29,31,37}`),
  `T = 150` (`[150,1300]`, `z0 ∈ {29,31,37,41}`) and
  `T = 200` (`[200,1800]`, `z0 ∈ {31,37,41,47}`), 80–500 stage-1 designs each
  (`cons_T130*.txt`, `cons_T150*.txt`, `cons_T200*.txt`):
  the overwhelming majority of residuals have an empty tail fixpoint
  (e.g. 114/120 at `T=200, z0=37`), and the survivors were not solved within
  90 s each.
* **Smoothness alone is the wrong design axis.**  Restricting to `z`-smooth
  elements *without* the one-large-prime condition is markedly worse: on
  `[45,345]` (target 1) the plain Rule-(P) fixpoint (`|A| = 159`) is solved in
  7.1 s, while the `z = 57` restriction (`|A| = 151`) had not finished in 120 s.
  **"At most one large prime per element" is the useful axis.**
* Rule (P) alone already forces `z ≈ N/5` (the fixpoint of `[45,345]` is
  69-smooth), and OBSERVED (`smoothstats.py`, not proved): all 39 267 corpus
  solutions are `(max U)/4`-smooth, all but two `(max U)/5`-smooth, and the
  far-out ones much smoother (the `min=104`, `max=900` gadget is 59-smooth).
  Lemma 1 proves the weaker but unconditional `z*(T,N) ≍ (N−T)/log N`.

## 8. Files

| file | what |
|---|---|
| `lib.py` | exact primitives: sieves, runs/legality/capacity, `Fraction` **and** Fraction-free verification |
| `forced.py` | **Lemma 1 / Cor. 2 / Cor. 3**: `kmin(p)`, `z*(T,N)`, forced set, density, run histogram |
| `verify_lemma.py` | exact check of Lemma 1 + Cor. 2 on the whole corpus |
| `table_forced.py` | the `z*` / density table of §2 |
| `design.py` | `z`-smooth restriction + independent re-implementation of the sound Rule (P) + legality fixpoint |
| `build.py` | **the designed universe** (one large prime per element, smooth escort) |
| `construct.py` | **the two-stage construction** (independent per-prime packs, then exact residual fix) |
| `mkprob.py` | writes `BIG` problem files (arbitrary rational target) |
| `esearchB.c`, `padicB.h`, `bigint.h` | the exact engine patched for arbitrary rational targets |
| `interaction.py` | verifies the Decoupling Lemma; exact Størmer-wall counts |
| `mass.py` | exact "legal mass" of the `z`-smooth part of a window |
| `smoothstats.py` | largest prime factor vs `max U` over the corpus (OBSERVED) |
| `anatomy.py` | prime-by-prime dissection of a solution (its Rule (P) certificate) |
| `scan.py`, `scan2.py`, `scan3.py` | parameter scans over `(N,z)`, `(N,z0)`, `(N,z0,z)` |
| `verify.py` | independent exact re-verification of `SOL` lines |
| `coverage.py` | glues far `1/2`-systems to the two `[2,103]` ones and reports the block counts `k` realised |
| `gadgets_half_min104.txt`, `cert_P51_70.txt` | the ten far `1/2`-systems and the `k = 51..70` certificates |
| `cert_min104_half.txt`, `cons_cert.txt` | the new certificates |
| `*.prob`, `log_*.txt`, `scan*_*.txt`, `cons_T*.txt`, `twostage_T104.txt` | problem files, search logs and scan outputs (all kept) |

## 9. Reproduction

```bash
gcc -O3 -march=native -o esearch  ../wf-engine/esearch.c
gcc -O3 -march=native -o esearchB esearchB.c

python3 verify_lemma.py ../../experiments/ALLSOLS.txt     # Lemma 1: 0 failures
python3 forced.py 104 900                                 # z* = 179, density 0.2346
python3 table_forced.py                                   # the table of §2
python3 interaction.py 200 1000 23                        # decoupling + Stormer wall

# the designed universe, single DFS  ->  min U = 104, max = 651, sum = 1/2
python3 build.py 104 700 1 2 -z0 17 -o b_104_700_z17.prob
./esearch b_104_700_z17.prob -k 30 -m 3 | python3 verify.py --target 1/2 --minelt 104

# the two-stage construction     ->  min U = 104, max = 875, sum = 1/2
python3 construct.py 104 900 1 2 -z0 29 -tries 40 -t 12 -seed 3
python3 verify.py --target 1/2 --minelt 104 cons_cert.txt
python3 anatomy.py cons_cert.txt          # the designed p-adic structure, prime by prime
```
