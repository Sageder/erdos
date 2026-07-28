# PROBLEM.md — Erdős Problem 289 (immutable; written once at session start)

## Statement

Integers only; $\ln$ is the natural logarithm; every reciprocal sum is an exact element of
$\mathbb{Q}$ (no floating point anywhere in a proof). A **block** (interval) is a set of
consecutive positive integers
$$[a,b] := \{a, a+1, \dots, b\},\qquad 1 \le a \le b,$$
of length $|[a,b]| = b-a+1$, with **block sum** $H(a,b) := \sum_{n=a}^{b} 1/n \in \mathbb{Q}$.
Blocks $[a_1,b_1],[a_2,b_2]$ are disjoint iff $b_1 < a_2$ or $b_2 < a_1$; **adjacent blocks
$[a,b]$ and $[b+1,c]$ ARE disjoint and count as two blocks** (no gap or maximality condition
is imposed).

**The predicate.** For $k \ge 1$, $k$ is *representable*, written $P(k)$, iff there exist $k$
pairwise disjoint blocks $I_1,\dots,I_k$ of positive integers, each of length $|I_i| \ge 2$, with
$$\sum_{i=1}^{k}\ \sum_{n \in I_i} \frac1n \;=\; 1 .$$
Blocks are unordered; there must be EXACTLY $k$ of them.

**The problem (erdosproblems.com/289, verbatim; this governs).** "Is it true that, for all
sufficiently large $k$, there exist intervals $I_1,\dots,I_k$ with $|I_i| \ge 2$ for
$1 \le i \le k$ such that $1 = \sum_{i=1}^k \sum_{n \in I_i} 1/n$?" That is: does there exist
$K$ with $P(k)$ true for every $k \ge K$?

**Lean cross-check** (google-deepmind/formal-conjectures, `ErdosProblems/289.lean`):
$\forall^{f} k$ in `atTop`, $\exists I : \mathrm{Fin}\,k \to \mathbb{N}\times\mathbb{N}$ with
(a) $(I\,i).1 < (I\,i).2$; (b) for $i \ne j$, $(I\,i).2 < (I\,j).1$ or $(I\,j).2 < (I\,i).1$;
(c) $\sum_i \sum_{n \in \mathrm{Icc}((I\,i).1,(I\,i).2)} n^{-1} = 1$ in $\mathbb{Q}$.

## Ambiguity resolutions (binding for this run)

1. **Exactly $k$ blocks**, not "at most $k$" (index type $\mathrm{Fin}\,k$). Padding is impossible
   anyway: every legal block has strictly positive sum.
2. **$|I_i| \ge 2$ for every $i$.** Site and Lean agree. Bare unit fractions are forbidden.
3. **Disjointness is REQUIRED.** The quoted site sentence is silent; the Lean file imposes
   pairwise separation, which for nonempty integer intervals is exactly pairwise disjointness.
   *Noted discrepancy:* under a non-disjoint reading the problem would be different (and
   overlapping/repeated blocks resolve nothing); the disjoint reading governs here.
4. **Minimum element $\ge 1$.** Lean's $\mathbb{N}$ contains $0$ and Mathlib's junk value
   $0^{-1}=0$ would let $\mathrm{Icc}(0,1)$ "sum" to $1$. The site statement governs: blocks
   consist of positive integers and $1/n$ is the genuine rational. Using the $0$-junk encoding is
   forbidden.
5. **Derived normalization (proved, not assumed).** No block of a solution contains $1$: such a
   block has length $\ge 2$ so contributes $\ge 1 + \tfrac12 > 1$, while all other terms are
   positive. Hence every element of every solution is $\ge 2$.

## What a complete resolution must establish

Let $S := \{k \ge 1 : P(k)\}$. Exactly one branch, proved in full; the answer is not assumed in
advance.

**YES.** $\exists K\ \forall k \ge K:\ P(k)$. Equivalently $S \supseteq [K,\infty)$, i.e. $S$ is
cofinite in $\mathbb{Z}_{\ge1}$.

**NO.** $\forall K\ \exists k \ge K:\ \neg P(k)$. Equivalently $\mathbb{Z}_{\ge1}\setminus S$ is
infinite; the bad $k$ need not be explicit but their infinitude must be proved against ALL block
systems.

**Quantifier order.** In the YES branch the blocks may depend on $k$ arbitrarily; only one
threshold $K$ must work for all larger $k$. "$P(k)$ for infinitely many $k$" is strictly weaker
than YES; "one bad $k$" is strictly weaker than NO. Truth values at finitely many $k$ constrain
neither branch — $P(1)$ is FALSE and that is compatible with both.

## Working reformulation (equivalent; used throughout)

For a finite $U \subseteq \mathbb{Z}_{\ge 2}$ let its **maximal runs** be its maximal blocks of
consecutive integers, of lengths $L_1,\dots,L_r$.

> $P(k)$ holds **iff** there is a finite $U \subseteq \mathbb{Z}_{\ge2}$ with
> $\sum_{n\in U} 1/n = 1$, every maximal run of length $\ge 2$ (equivalently: **$U$ has no
> isolated point**), and $r \le k \le M := \sum_{i=1}^{r}\lfloor L_i/2\rfloor$.

*Proof.* ($\Leftarrow$) The splitting lemma: a block of length $L$ splits into $t$ adjacent blocks
of length $\ge 2$ for each $1 \le t \le \lfloor L/2\rfloor$ (take $t-1$ parts of length $2$ and
one of length $L-2(t-1)\ge2$); doing this inside each run realises every $k \in [r,M]$.
($\Rightarrow$) Given $k$ disjoint blocks, let $U$ be their union; each maximal run of $U$ is a
union of adjacent blocks of length $\ge2$, so $L_i \ge 2$ and the $k$ blocks distribute among the
runs with at most $\lfloor L_i/2\rfloor$ in run $i$; also $r \le k$. $\square$

## Background facts (assumable; each re-verified in `experiments/`)

- **(B1) Non-integrality (Kürschák).** For $b>a\ge1$, $H(a,b)\notin\mathbb{Z}$. Proof: let $2^t$
  be the largest power of $2$ dividing an element of $[a,b]$ ($t\ge1$ as the block contains an
  even number); its multiple in $[a,b]$ is unique (two would be consecutive multiples of $2^t$,
  one divisible by $2^{t+1}$); so exactly one term has $\nu_2 = -t$ and $\nu_2(H(a,b)) = -t \le -1$.
  Hence $P(1)$ is FALSE.
- **(B2) Two-attainer prune.** If $\sum_{n\in U}1/n = 1$ and $p$ is prime with
  $e := \max_{n\in U}\nu_p(n) \ge 1$, then at least TWO elements of $U$ attain $\nu_p = e$
  (else the unique term $1/n_0$ has $\nu_p = -e$ strictly below all others, forcing
  $\nu_p(\text{sum}) = -e < 0 = \nu_p(1)$). Necessary, never sufficient.
- **(B3) Splitting lemma** — as in the reformulation above.
- **(B4) Telescoping.** $\frac1n = \frac1{n+1}+\frac1{n(n+1)}$; block adaptations must verify that
  newly created elements avoid all existing blocks.
- **(B5) Verified identities.** $1 = \frac13+\frac14+\frac15+\frac16+\frac1{20}$ and
  $1 = \frac12+\frac13+\frac1{10}+\frac1{15}$ (neither is a certificate here — singleton blocks).
  The circulating $1 = \frac12+\frac13+\frac14+\frac15+\frac16+\frac1{20}$ is FALSE ($=\frac32$).
