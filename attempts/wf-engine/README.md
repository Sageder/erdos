# wf-engine — an exact search engine for legal block systems, with no 128-bit ceiling

Recon 1 (ENGINE).  Everything here is exact integer / rational arithmetic.
No floating-point number occurs in any verification path; the only `double`
in the C sources is the wall-clock limit.

## What is here

| file | what |
|---|---|
| `bigint.h` | hand-rolled fixed-width unsigned multiword arithmetic (compare / add / subtract / mul-by-word / div-by-word / mod-by-word / decimal print). On x86-64 the 128/64 division is the hardware `divq`. |
| `padic.h` | the **dynamic Rule-(P) lookahead**: per-prime residue reachability tables, tested at every DFS node. |
| `esearch.c` | exact search for a legal `W ⊆ A ⊆ [T,N]` with `Σ 1/n = u/v`. |
| `gadget.c` | exact search for a legal `W ⊆ A ⊆ [T,N]` with `Σ 1/n = a/D`, `a` free, value confined to `[lo,hi]` ("gadget mode"). |
| `prune.py` | Rule-(P) + legality **universe fixpoint** of `[T,N]` for an exact target *or* for gadget mode; writes the problem file. |
| `threshold.py` | for each `T`, the smallest `N` for which the fixpoint of `[T,N]` can still carry the target — i.e. an exhaustive **proof** that no solution has `min ≥ T`, `max < N`. |
| `verify.py` | independent re-verification of `SOL` lines with `fractions.Fraction` only. |
| `pool.py`, `glue.py` | gadget pools in disjoint windows, glued by exact integer subset-sum. |
| `climb.sh`, `sweep.sh` | drivers. |

Build: `gcc -O3 -march=native -o esearch esearch.c` and likewise for `gadget.c`.

## Why the 128-bit ceiling disappears (the rescaling)

The old engines fixed `L = lcm(A)`, carried `R = (residual target)·L`, and
needed `L < 2^127`; `[100,780]` already needs 152 bits.  Here, with
`A = {e_0 < … < e_{cnt-1}}`, put

    L_i = lcm{ e_j : j ≥ i },      L_cnt = 1,
    w_i = L_i / e_i,               g_i = L_i / L_{i+1},

and carry `X_i = (residual target)·L_i`, an integer because the residual must
be a sub-sum of `{1/e_j : j ≥ i}`.  Then

    take e_i :  X_{i+1} = (X_i − w_i)/g_i,     skip e_i :  X_{i+1} = X_i/g_i,

and **exact divisibility by `g_i` is precisely the old pooled prune `Q[i] | R`**
(with `Q[i] = L_0/L_i`): `Q[i] | R ⟺ X_i ∈ Z`.  Two consequences:

* `g_i` divides `e_i ≤ N` — if `p^a` leaves the lcm at `i` then `e_i` is the
  unique remaining multiple of `p^a`, and the `p^a` for distinct `p` are
  coprime — so the prune is a **multiword ÷ single word**, never a big/big
  remainder;
* `L_i` collapses as `i` grows, so the operand width **shrinks with depth**.
  The wide part of the tree is the shallow part.

`gadget.c` runs the same recursion in accumulating form with
`K_i = lcm(D, e_i, …, e_{cnt-1})`, `Z_i = (partial sum)·K_i`, `K_cnt = D`, so
that `Z_cnt = a` is the numerator of the gadget value `a/D`.

## The two prunes that were kept, plus the one that was added

1. **Universe fixpoint** (`prune.py`, offline).  Rule (P): if `Σ 1/n = u/v` and
   `E ≥ ν_p(n)` for all `n ∈ W`, then `Σ_{n∈W, p|n} p^E/n ≡ p^E·u/v (mod p^E)`.
   Taking `E` = max over the current universe, an element may be deleted when
   no subset of the `p`-multiples containing it has the right residue; decided
   exactly by forward/backward subset-reachability carried as Python-integer
   **bitmasks** (one bit per residue), so each prime costs
   `O(#multiples · p^E / 64)` word operations instead of `O(#multiples · p^{2E})`.
   Plus legality.  Iterate to a fixpoint.
   In gadget mode `p^E·a/D` runs over all multiples of `p^{E−ν_p(D)}`, so the
   congruence becomes `≡ 0 (mod p^{E−ν_p(D)})`.
2. **Pooled divisibility** `Q[i] | R`, now free (see above).
3. **NEW — dynamic Rule-(P) lookahead** (`padic.h`).  All the moduli `p^E` are
   `≤ N`, so for each prime the *full* backward reachability table
   `reach[k][r] = [r is a subset sum, mod p^E, of the weights of the multiples
   of p at positions ≥ k]` fits in `(#multiples+1)·p^E` bytes — a few MB in
   total.  At every node the residue still needed is looked up.  Only primes
   dividing `e_i` are touched (all other weights vanish), ~3 lookups per node.
   This is what made far-out ranges tractable: on `[104,400]` it took the
   engine from *zero* hits in 7.5·10⁸ nodes to a solution in 5 s, and on
   `[2,130]` it replaced a 20-minute, 4.7·10⁹-node exhaustion by **0.7 s**.

The endgame table over the top `K` universe indices stores 61-bit
**fingerprints** (`X mod (2^61−1)`) of every legal completion.  A miss is a
proof that no completion works (fingerprints have no false negatives); a hit
triggers an **exact** multiword completion.  Correctness is therefore
independent of the fingerprints.

## Validation against the known answers

```
$ python3 prune.py 2 76 1 1
[2,76] target=1/1  |A|=0            <- fixpoint EMPTY, as previously established
$ python3 prune.py 2 84 1 1 -o p_2_84.txt ; ./esearch p_2_84.txt
done nodes=24664 solutions=0 cpu=0.0s          <- NO solution with max ≤ 84
$ python3 prune.py 2 85 1 1 -o p_2_85.txt ; ./esearch p_2_85.txt
SOL 5 6 14 15 17 18 20 21 22 27 28 33 34 44 45 54 55 84 85
SOL 6 7 8 14 15 17 18 26 27 34 35 44 45 54 55 56 65 66 77 78 84 85
SOL 7 8 9 10 14 15 17 18 19 34 35 36 44 45 56 57 76 77 84 85
SOL 7 8 11 12 17 18 21 22 26 27 28 33 34 44 45 54 55 56 65 66 77 78 84 85
done nodes=95754 solutions=4 cpu=0.0s          <- EXACTLY 4 with max = 85
```

Exhaustive solution counts `#{U : max U ≤ N}` (`./esearch p_2_N.txt -q -k 28`),
against the 27 582-solution corpus in `experiments/ALLSOLS.txt` and against
`csearch2`:

| N | 85 | 100 | 105 | 110 | 120 | 130 | 140 |
|---|---|---|---|---|---|---|---|
| this engine | 4 | 39 | 96 | 96 | 163 | 163 | 425 |
| corpus / csearch2 | 4 | 39 | 96 | 96 | 163 | 163 (4.7·10⁹ nodes, 20 min) | — |

`N = 130` now costs **0.7 s / 2.2·10⁷ nodes**.  The endgame table is verified
not to change any count (`-k 0`, `-k 18`, `-k 26` on `[2,110]` all give 96).

## Exhaustive negative results for the CRUX (`threshold.py`)

The fixpoint only deletes elements that cannot occur in *any* legal `W` with
the given sum, so an empty (or sum-deficient) fixpoint is a proof.  For target 1:

| T | 2 | 5 | 10 | 20 | 30 | 40 | 45 | 50 | 55 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nmin(T) | 77 | 77 | 85 | 136 | 208 | 246 | 287 | 305 | 345 | 369 | 476 | 532 | 582 | 657 | 671 | 721 | 900 | 1131 |

**No legal `U` with `min U ≥ T`, `max U < Nmin(T)` and `Σ 1/n = 1` exists.**
(`T = 2`: reproduces the known "fixpoint empty for `N ≤ 76`".)  The ratio
`Nmin(T)/T` sits in `[6.1, 6.9]` throughout, so a solution far out needs a
window of relative width at least ≈ 6.

Beyond `Nmin` the engine decides windows exhaustively until the tree explodes;
the practical wall is `|A| ≈ 170` universe elements.

## Finding solutions far out (the CRUX)

Deterministic take-first DFS solves `[45,345]` in ≈40 s.  Beyond that the
randomised-restart mode with a **take-bias** is much better: solutions use
about `1/maxsum ≈ 80 %` of the universe mass, so trying "take" first with
probability 85 % matches the shape of a solution.  Calibration on the
known-solvable `[45,345]`: `-p 60` and `-p 75` fail in 30 s, `-p 85` succeeds in
**3.9 s CPU**.

```
$ ./esearch p_45_345.txt -k 30 -m 1 -R 1 -B 3000000 -p 85 -t 30
done(cap) nodes=117611669 solutions=1 cpu=3.9s
$ python3 prune.py 55 420 1 1 -o w_55_420.prob
$ ./esearch w_55_420.prob -k 30 -m 1 -R 1 -B 5000000 -p 85 -t 1800
done(cap) nodes=1230007999 solutions=1 cpu=37.8s
```

### Certificates found here (all re-verified by `verify.py`, exact `Fraction`)

* `sol_45_345.txt` — `|U| = 112`, `min = 45`, `max = 345`, `r = 40`, `cap = 49`.
* `sol_min55.txt` — `|U| = 146`, `min = 55`, `max = 414`, `r = 49`, `cap = 65`:

```
55 56 57 58 60 61 62 63 64 65 66 68 69 70 74 75 76 77 78 80 81 85 86 90 91 92
93 98 99 100 105 106 110 111 112 114 115 116 117 118 119 120 122 123 124 132
133 135 136 140 141 143 144 145 147 148 152 153 154 155 156 161 162 164 165
170 171 172 174 175 176 182 183 184 185 186 187 188 189 190 195 196 204 205
207 208 209 210 215 216 221 222 224 225 230 231 232 234 235 245 246 247 248
260 261 264 265 272 273 275 276 279 280 287 288 295 296 297 305 306 318 319
320 322 323 324 325 340 341 344 345 350 351 352 368 369 370 371 377 378 405
406 407 408 413 414
```

This beats the previous record for the CRUX with target 1 (`min U = 50`, from
`experiments/ALLSOLS.txt`) and gives `P(k)` for every `k ∈ [49,65]` from a
single system all of whose elements are `≥ 55`.

## Gadget mode and gluing

`gadget.c` finds legal systems whose value is *any* `a/D`.  Since gadgets in
pairwise disjoint windows glue (union of legal sets in disjoint windows is
legal, values add), `glue.py` then only has to solve the integer equation
`a_1 + … + a_m = D`.  Observed rates (11 s CPU, one core):

| window | `D` | gadgets |
|---|---|---|
| `[104,400]` | `10! = 3628800` | 60 046 |
| `[55,500]` | `10!` | 0 |
| `[55,500]` | `11! = 39916800` | 905 |
| `[55,500]` | `13!/(2·9) = 518918400` | 14 592 |
| `[55,500]` | `2^9 3^5 5^3 7^2 11·13` | 387 336 |
| `[401,1200]` | `10!` | 0 |
| `[401,1200]` | `2^9 3^5 5^3 7^2 11·13` | 154 |
| `[501,2500]` | any tried | 0 |

**Diagnosis (negative, and worth recording).**  Gadget yield collapses as the
window moves up: a window `[T,N]` loses every prime in `(N/2,N]` outright
(one multiple cannot satisfy Rule (P)), and the surviving primes in `(N/3,N/2]`
have only two multiples, so the number of simultaneous mod-`p` conditions grows
like `π(N/2)` while the freedom does not.  `D` can only buy back the primes
dividing it, and `D` must stay below ≈`10^9` for two pools to collide.  This is
why *window splitting is expensive*: `[55,450]` as one range has `|A| = 197`
and `maxsum = 1.24`, but split as `[55,150] ∪ [151,450]` it keeps only
`18 + 90 = 108` elements with `maxsum = 0.58 < 1`.  Gluing therefore helps only
when each window is itself wide (ratio `≥ 3.5`), which is the regime `T ≥ 100`.

## Multiword stress tests (no 128-bit ceiling)

Planted-solution tests on unpruned universes, so that `lcm(A)` is as large as
possible; each has a unique planted legal solution and the engine must return
exactly it:

```
$ ./esearch mw_test.prob  -k 20      # A = [900,1000],  lcm = 554 bits  (9 words)
T=900 N=1000 target=34295913467/5421296277000 |A|=101  lcm bits=554  words=9
SOL 900 901 950 951 999 1000
done nodes=137 solutions=1 cpu=0.0s

$ ./esearch mw_test2.prob -k 20      # A = [2000,2400], lcm = 1899 bits (30 words)
T=2000 N=2400 target=45712528933081/14101658502932000 |A|=401  lcm bits=1899  words=30
SOL 2000 2001 2002 2200 2201 2399 2400
done nodes=46915 solutions=1 cpu=0.1s
```

1899 bits is 15x the old ceiling and costs 0.13 s.  `MAXW = 200` words allows
12800-bit lcms; the pruned universes that actually arise need 80-250 bits
(`[100,780]` = 152 bits, the case the old engines could not do).
