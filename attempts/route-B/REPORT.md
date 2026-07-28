# Route B — computational attack on Erdős 289

**Headline: legal `U` with `sum_{n in U} 1/n = 1` EXIST. The smallest possible
maximum element is 85, and there are exactly four certificates attaining it.**

Throughout, *legal* means `U ⊆ Z_{≥2}` finite with no isolated point (equivalently a
disjoint union of runs of consecutive integers, each of length ≥ 2).

All arithmetic in every verification path is exact: `fractions.Fraction` in Python,
`unsigned __int128` in C (`L = lcm(universe)` never exceeds 128 bits in any run
reported here — the bit length is printed by every search).

---

## 1. The four minimal certificates (max(U) = 85)

Verified independently by `verify.py` (Fraction only, no search code reused):

| # | U (runs separated by `.`) | \|U\| | run lengths | r | M | k realised |
|---|---|-----|-------------|---|---|---|
| 1 | 5 6 . 14 15 . 17 18 . 20 21 22 . 27 28 . 33 34 . 44 45 . 54 55 . 84 85 | 19 | 3,2,2,2,2,2,2,2,2 | 9 | 9 | 9 |
| 2 | 6 7 8 . 14 15 . 17 18 . 26 27 . 34 35 . 44 45 . 54 55 56 . 65 66 . 77 78 . 84 85 | 22 | 3,3,2,2,2,2,2,2,2,2 | 10 | 10 | 10 |
| 3 | 7 8 9 10 . 14 15 . 17 18 19 . 34 35 36 . 44 45 . 56 57 . 76 77 . 84 85 | 20 | 4,3,3,2,2,2,2,2 | 8 | 9 | 8,9 |
| 4 | 7 8 . 11 12 . 17 18 . 21 22 . 26 27 28 . 33 34 . 44 45 . 54 55 56 . 65 66 . 77 78 . 84 85 | 24 | 3,3,2,2,2,2,2,2,2,2,2 | 11 | 11 | 11 |

`r` = number of maximal runs, `M = sum floor(L_i/2)`; by the splitting lemma the
certificate realises exactly the k in `[r, M]`.

Certificate 1 in full:
`1 = 1/5+1/6+1/14+1/15+1/17+1/18+1/20+1/21+1/22+1/27+1/28+1/33+1/34+1/44+1/45+1/54+1/55+1/84+1/85`

---

## 2. The new tool: a much stronger universe reduction

The pre-existing `experiments/csearch.c` used the "two-attainer" prune. It is a
special case of the following, which is what unlocked everything here.

### Rule (P) — p-adic block condition

> For every prime `p`, `S_p := sum_{n in U, p|n} 1/n` satisfies `nu_p(S_p) >= 0`.

*Proof.* `1 = S_p + S'_p` where `S'_p` sums `1/n` over the `n in U` with `p` not
dividing `n`; each such `1/n` lies in `Z_p`, so `nu_p(S'_p) >= 0`. If
`nu_p(S_p) < 0` then `nu_p(1) = nu_p(S_p + S'_p) = nu_p(S_p) < 0`, contradiction. QED

Operationally, with `E = max_{n in A, p|n} nu_p(n)`, each `p^E/n` lies in `Z_p` and
the rule is the **subset-sum-to-zero condition mod `p^E`**

```
sum_{n in U, p|n}  (p^E / n)  ==  0   (mod p^E)
```

over the multiples of `p` in the current universe `A`. An element `n` may be deleted
whenever *no* subset of the multiples of `p` in `A` containing `n` has residue `0`.
This is decided by a forward/backward reachability DP over the `p^E` residues
(`reduce.py:prime_prune`), cost `O(|multiples| * p^E)`.

Two-attainer is the case where the top level has a single element: then the only
subset is `{n}`, whose residue is a unit. Rule (P) is far stronger — e.g. for
`N = 80` it kills 17, 23, 29, 31, 37 and all their multiples, which two-attainer
keeps. Example: multiples of 23 in `[2,80]` are 23,46,69, so `V = {1,2,3}` and the
nonempty subset sums `1, 1/2, 1/3, 3/2, 4/3, 5/6, 11/6` have numerators
`1,1,1,3,4,5,11`, none divisible by 23 — so no multiple of 23 can occur at all.
By contrast for `p = 19` the subset `{19,57,76}` gives `1 + 1/3 + 1/4 = 19/12`,
so multiples of 19 must be either none or exactly `{19,57,76}`.

### Rule (I) — isolated-point propagation

> If `n-1` is not in `A` and `n+1` is not in `A`, then `n` can never have a
> neighbour, so delete `n`.

Both rules only delete elements that provably lie in no solution, so their fixpoint
`A(N)` is a valid over-approximation of every solution `U ⊆ [2,N]`.

### Effect

| N | \|A(N)\| (rule P+I) | \|universe\| in `csearch.c` | log2(search space) | L (bits) |
|---|---|---|---|---|
| 70 | **0** | 57 | — | — |
| 80 | 34 | 66 | 23 | 25 |
| 100 | 51 | — | 34 | 33 |
| 120 | 66 | — | 45 | 38 |
| 150 | 78 | — | 54 | 44 |
| 160 | 81 | — | 56 | 45 |
| 200 | 102 | — | 69 | 47 |
| 300 | 170 | — | 114 | 69 |

`A(N)` is a disjoint union of runs, and a legal `U` is obtained by choosing
independently, in each run of `A(N)`, a subset with no isolated point *inside that
run* (runs of `A(N)` never interact, since the neighbours of the run endpoints are
banned). The search space is therefore `prod_i f(L_i)` where `f` counts binary
strings of length `L` with no isolated 1 (`f = 1,2,4,7,12,21,37,65,...`).

**Validation of rule (P)** (`validate_reduce.py`):
* on the relaxed problem (no isolated-point condition) all `2/5/10/21/40/199` exact
  reciprocal-sum-1 subsets of `[2,N]` for `N = 12,15,18,20,24,30` survive rule (P);
* 4000 random sets: the mod-`p^E` formulation agrees exactly with a direct
  `Fraction` computation of `nu_p(S_p)`;
* the classical identities `1 = 1/3+1/4+1/5+1/6+1/20`, `1 = 1/2+1/3+1/10+1/15`,
  `1 = 1/2+1/4+1/6+1/12`, `1 = 1/2+1/3+1/7+1/42`, `1 = 1/2+1/4+1/10+1/12+1/15`
  all survive.

---

## 3. Exhaustive results

### 3.1 By reduction alone (milliseconds)

`A(N)` is EMPTY for **every `N <= 76`**. Since a solution `U ⊆ [2,N]` must satisfy
`U ⊆ A(N)`, and the empty sum is `0 != 1`:

> **There is no legal `U` with `max(U) <= 76`.**

This reproves — in milliseconds, by pure constraint propagation — the previously
known result for `N <= 70` (which had cost 547 million DFS nodes), and extends it.
`A(77)` is the first non-empty reduced universe (23 elements).

### 3.2 By exhaustive DFS over `A(N)` (`bsearch.c`)

Prunes: (1) `R > tail[pos]`; (2) `Q[pos]` does not divide `R`; (3) per-prime p-adic
reachability (`x_p` = residue contributed by already chosen multiples of `p`; the
still-open multiples of `p` must be able to supply `-x_p mod p^{E_p}`; the reachable
sets are precomputed per position).

| N | nodes | certificates with max(U) <= N | wall time (1 core) |
|---|---|---|---|
| 84 | 63,645 | **0** | < 0.01 s |
| 85 | 213,739 | **4** | 0.01 s |
| 90 | 213,739 | 4 | 0.01 s |
| 100 | 5,694,173 | 39 | 0.1 s |
| 110 | 14,158,743 | 96 | 0.1 s |
| 120 | 126,809,111 | 163 | 1.3 s |
| 130 | 126,809,111 | 163 | 1.4 s |
| 140 | 799,979,228 | 425 | 8.0 s |
| 150 | 12,284,280,908 | 5,451 | 173 s |
| 160 | 39,793,513,500 | 20,993 | ~14 min |
| 170 | 94,036,672,206 | 25,650 | ~2 h on 4 cores (heavy machine contention) |

> **Exhaustively: there is no legal `U` with `max(U) <= 84`; there are exactly four
> with `max(U) = 85`; and the complete list of legal `U` with `max(U) <= 170`
> consists of 25,650 sets, every one re-verified with `fractions.Fraction`.**

Distribution of `max(U)` over the 20,993 with `max(U) <= 160`
(only run-ends of `A(160)` can occur):

```
85:4  91:2  96:1  100:32  105:57  115:16  120:51  133:78
136:184  144:512  145:4514  153:5379  154:10163
```

**Exact k-realisability inside the exhaustive class.** Over all 25,650 certificates
with `max(U) <= 170` the number of maximal runs `r` ranges over `7..`, and

> for `k >= 1`, a witness for `P(k)` using only integers `<= 170` exists
> **iff `7 <= k <= 23`**.

### 3.3 Independent cross-validation

The pre-existing `experiments/csearch.c` — different code, different (weaker)
universe reduction, different node ordering — was run at `N = 85` to completion:
27,143,471,018 nodes, and it output **exactly the same four certificates**.
This independently validates both rule (P) and `bsearch.c`.

The 4-way job-split of `bsearch` was validated at `N = 150`:
`1531 + 1329 + 1317 + 1274 = 5451`, matching the single-job count.

---

## 3.4 Restricted exhaustive search: few blocks (`fewruns2`)

`P(k)` needs a certificate with `r <= k <= M`, so bounding the number of maximal
runs `r` bounds `k` from below. `fewruns.c` (derived from `bsearch.c`) adds a cap
`RMAX` on the number of maximal runs together with the exact bound

> a `U`-run always lies inside one run of the universe `A`, so a `U` using at most
> `j` further runs from position `pos` has sum at most
> `runcap[pos][j] = max(runcap[nxt][j], weight(first universe run) + runcap[nxt][j-1])`.

(The naive "the first `j` universe runs are the heaviest" version of this bound is
WRONG — a later, longer universe run can outweigh an earlier one — and it silently
lost solutions; the bug was caught by cross-checking against the certificate list
and is fixed. Validation of the fixed version: `RMAX=25` reproduces the exhaustive
counts 163 at `N=120` and 425 at `N=140`; `RMAX=13` gives 206 and `RMAX=10` gives
74 at `N=140`, both matching a direct count of the run numbers in the exhaustive
certificate list.)

Results:

| RMAX | N | nodes | certificates |
|---|---|---|---|
| 6 | 160 | 147,941,463 | 0 |
| 6 | 200 | 444,324,346 | 0 |
| 6 | 250 | 6,322,165,390 | **1** |
| 5 | 300 | 1,206,484,145 | **0** |

The unique certificate with at most 6 maximal runs and `max(U) <= 250` is

```
1 = 1/4+1/5+1/6 + 1/9+1/10 + 1/19+1/20 + 1/44+1/45 + 1/132+1/133 + 1/209+1/210
```

i.e. `U = {4,5,6, 9,10, 19,20, 44,45, 132,133, 209,210}`, six blocks
`[4,6],[9,10],[19,20],[44,45],[132,133],[209,210]`, run lengths `3,2,2,2,2,2`,
`r = M = 6`. **So `P(6)` is TRUE**, and 210 is the smallest possible maximum
element of a `k = 6` witness.

> **Exhaustively: no legal `U` with at most 5 maximal runs has `max(U) <= 300`.**
> Hence `P(k)` for `k <= 5` has no witness using integers `<= 300`.
> (`P(1)` is false outright, by Kürschák non-integrality.)

## 4. Certificates and the block count k

For a certificate with maximal runs of lengths `L_1,...,L_r`, the splitting lemma
makes it realise `P(k)` for exactly `k in [r, M]`, `M = sum floor(L_i/2)`.

To reach large `k` the search is restricted to the class
`{U legal : min(U) >= lo, max(U) <= N}`, whose reduced universe is computed by
`reduce_universe(N, lo=lo)`. **This is a restricted class** — certificates found are
of course unconditionally valid, but *absence* of certificates in a window is only a
statement about that window.

See section 6 for the k coverage achieved.

---

## 5. Files

| file | role |
|---|---|
| `reduce.py` | rules (P) and (I), universe fixpoint (also windowed, `lo=`) |
| `validate_reduce.py` | adversarial validation of rule (P) |
| `structure.py` | run decomposition of `A(N)` and search-space size |
| `gen_universe.py`, `gen_window.py` | emit universes for the C searches |
| `bsearch.c` | exhaustive DFS, exact `__int128`, 3 prunes, job splitting |
| `hunt.c` | randomised restart version of the same search |
| `pairsearch.c`, `pairhunt.c` | search restricted to *all runs of length exactly 2* (fixes `k` exactly) |
| `verify.py` | **independent** Fraction verifier of certificates |
| `analyze.py` | re-verifies a pool and reports run lengths / k coverage |
| `sols_N*.txt`, `pool/` | certificates |

## 6. k coverage

(filled in at the end of the run — see `kcoverage.txt`)
