# AUDITS.md — Erdős 289

## Audit 1 (2026-07-28) — the base certificates and the negative range

**Object audited.** (a) The claim "$P(k)$ holds for $k=7,\dots,18$", with explicit
certificates; (b) the claim "no legal $U$ has $\max U \le 84$; the minimum is 85 with
exactly 4 solutions".

**Verdict: PASS.** Both claims survive; the checklist of PROMPT §7 is walked item by item
below. Nothing here is presented as a resolution of the problem.

### §7 checklist

1. **Exact re-verification by an independent script.** `experiments/verify.py` and
   `experiments/certificates.py` re-read the raw solution files and re-derive everything
   with `fractions.Fraction`. They import nothing from the search code. No float occurs
   anywhere in the verification path (floats appear only inside `two_to_block.c` and
   `collide.c`, which are *hit-finding heuristics* whose every hit is re-checked exactly;
   no proof depends on them). 315 solutions re-verified; 12 explicit per-$k$ certificates
   re-verified. PASS.
2. **Block count exactly $k$; every length $\ge 2$; pairwise disjoint; elements $\ge 2$.**
   `certificates.py::verify` asserts `len(blocks)==k`, `b-a+1>=2`, `a>=2`, and
   sorted-non-overlap `srt[i][1] < srt[i+1][0]`. The splitting lemma is applied
   *concretely* (`split_run`), not merely counted. PASS.
3. **No element 1, no element 0, no Lean $0^{-1}=0$ loophole.** `a>=2` is asserted per
   block; the minimum element over all 315 solutions is 4. PASS.
4. **Inductive constructions.** None are used in the established claims — the $k$-range of
   a single solution comes from the splitting lemma alone, which is proved in PROBLEM.md
   and applied explicitly. Nothing is chained. PASS (vacuous).
5. **Base/step alignment.** No step is claimed, so no gap can open between base and step.
   The claim is exactly "$P(k)$ for $k\in[7,18]$", nothing more. PASS.
6. **Splitting arithmetic.** `split_run(a,b,t)` asserts $1\le t\le\lfloor L/2\rfloor$ and
   that the final piece has length $\ge 2$; a length-3 run is therefore never cut.
   PASS.
7. **Global disjointness preserved.** The only construction used is splitting *inside* a
   run, which cannot create collisions; the verifier re-checks disjointness globally
   anyway. PASS.
8. **Quantifier check.** The established statement is $\exists$ certificates for the
   twelve values $k=7,\dots,18$ — a finite statement, and it is labelled as such
   everywhere. It is **not** claimed to be, and must not be read as, the cofinite
   statement. PASS.
9. **$p$-adic arguments.** The two-attainer rule (PROBLEM.md B2) and route C's RULE A are
   used only as *necessary* conditions, i.e. to delete candidates from a search universe;
   deleting a candidate can only shrink the search space, so a search that returns
   "no solution" is still exhaustive, and a search that returns solutions has them
   verified independently. The rules are never used as sufficient conditions. The
   valuation identity $\nu_p(\text{sum})=\min$ is applied only where the minimum is
   attained once — that is exactly the hypothesis of B2. PASS.
10. **External theorems.** None are load-bearing. Croot's and Bloom's theorems were
    considered and *not used*: the session's egress policy blocks arXiv and EuDML, so
    their statements could not be read and their hypotheses could not be verified. This
    is recorded rather than papered over. PASS.
11. **No circularity.** No lemma assumes representability. The certificates are outputs of
    a search, verified from scratch. PASS.
12. **Walk of PROMPT §3 (what does NOT count), item by item.**
    - *finite table of $k$ with no mechanism* — **this is exactly what is established
      here, and it is NOT presented as a resolution.** Recorded as a finite result.
    - *infinitely many but not cofinitely many $k$* — not claimed.
    - *blocks of length 1* — excluded by assertion (item 2).
    - *overlapping/repeated blocks* — excluded by assertion (item 2).
    - *"at most $k$" readings / padding* — excluded: `len(blocks)==k` is asserted.
    - *element 1 or the $0$-junk loophole* — excluded (item 3).
    - *approximate/asymptotic sums* — excluded: `Fraction` equality with 1.
    - *decomposing something other than 1* — the verifier compares to `1` exactly. The
      $1/2$ and $1/3$ gadgets are clearly labelled as gadgets, not as resolutions.
    - *NO branch by finitely many bad $k$* — not claimed; the NO branch is reported as
      refuted only in the sense that every *candidate obstruction* was refuted, which is
      itself not a proof of YES and is labelled as such.
    - *splitting reduction presented as a resolution* — explicitly not: ROUTES.md and
      NOTES.md state that the reduction is rigorous but the infinite family is missing.
    - *probabilistic/density arguments* — the local-global heuristic is labelled
      HEURISTIC in every file that mentions it.
    - *reduction to an unproved statement of comparable strength* — the CRUX is recorded
      as an OPEN reduction, explicitly not as progress toward a resolution.
    - *conditional results* — none.

### Cross-checks performed

- **Two independent engines agree on the negative range.** `experiments/csearch.c`
  (weak pooled prune, no legality-cascade) exhausted $N\le 80$ with 8.99·10⁹ nodes and
  $N=82,84$ with 3.9·10⁶ / 7.8·10⁶ nodes under the stronger endgame engine, finding
  nothing; route C's independent `dfs.c` over the RULE A+B fixpoint agrees, and its
  reference run of the untouched `csearch.c` at $N=85$ (2.71·10¹⁰ nodes) returns exactly
  the same four solutions. Three code paths, same answer.
- **Calibration.** Removing the no-isolated-point constraint reproduces the classical
  counts of Egyptian representations of 1 (5, 21, 40, 199 for $N=15,20,25,30$) and finds
  $\{2,3,10,15\}$, $\{3,4,5,6,20\}$ — the identities quoted in PROBLEM.md B5.
- **The false circulating identity** $1=\frac12+\frac13+\frac14+\frac15+\frac16+\frac1{20}$
  was recomputed and is indeed $\frac32$; it is not used anywhere.

## Audit 2 (2026-07-28) — negative structural claims

**Object.** "No atom split", "block sums are injective", "no unit fraction is a single
block sum", "the top run is prime-free".

**Verdict: PASS with a scope warning.**

- *Atom split* (`atom_split.py`): the reduction to "$p^2+4q^2$ a perfect square" is
  re-derived here: $\beta_d=p/q$ ⟺ $pd^2+(p-2q)d-q=0$, discriminant $(p-2q)^2+4pq=p^2+4q^2$.
  Every candidate is confirmed by an exact `Fraction` identity before being reported.
  Exhaustive **only** for $a\le 400$ and $c \le 8a+40$ — a bounded search, and the file
  says so.
- *Injectivity of block sums* (`collide.c`): fingerprints are a **necessary** condition
  for equality, so no true collision can be missed; the search is exhaustive over all
  2 841 941 blocks with elements $\le 3000$ and $H\le1$. Scope: elements $\le3000$ only.
- *$1/n$ never a single block sum* (`two_to_block.c`): the binary search uses long
  doubles, so a *hit* could in principle be missed if the true $d$ fell outside the
  $\pm1$ window; the window plus the monotonicity of $H(c,\cdot)$ makes that impossible
  for the magnitudes involved, and the sanity case $5/6=H(2,3)$ is found. Scope:
  $n\le60$, $c\le 2\cdot10^5$. **This is a bounded search, not a theorem.**
- *Top run prime-free*: this one is a **proof**, not a search. If $[c,N]$ is the top run
  of a solution and $p\in[c,N]$ is prime, the two-attainer rule forces a second multiple
  of $p$ in $U$, necessarily $\ge 2p$, so $2p\le N$; and if $c\le N/2$ the run contains
  $(N/2,N]$, which contains a prime by Bertrand. Hence $c>N/2$ and $[c,N]$ contains no
  prime. Corollary: a 2-run solution is impossible. Re-derived independently above; no
  computation is load-bearing. PASS.

## Standing warnings for any future draft

- A table of $k$ values, however long, is not the cofinite statement (PROMPT §3, item 1).
  Any DRAFT.tex must carry the infinite family or must not be written.
- The local-global count is a heuristic. Its local densities were computed exactly, but
  the independence across primes is a model assumption, and the model is known to be
  wrong in the small range (it predicts $\approx12$ solutions at $N=80$, where the truth
  is 0) until one conditions on the proved necessary conditions.
