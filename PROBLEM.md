# PROBLEM.md — Erdős Problem 727 (immutable; written once at session start)

## Statement

$n, k$ range over positive integers. $m!$ is the factorial. $\nu_p(m)$ is the exponent of the
prime $p$ in $m$; $s_p(m)$ is the sum of the base-$p$ digits of $m$; $\binom{a}{b}$ is the
binomial coefficient. The notation $(n+k)!^2$ means $((n+k)!)^2$: the square of the factorial
of $n+k$. For fixed $k$ define
$$S_k = \{\, n \ge 1 : ((n+k)!)^2 \mid (2n)! \,\}.$$

**Problem (erdosproblems.com/727, verbatim; this governs):** "Does $(n+k)!^2 \mid (2n)!$ for
infinitely many $n$?" — asked for every fixed $k \ge 2$. (Site commentary: "It is open even for
$k = 2$." Source: conjecture of Erdős–Graham–Ruzsa–Straus [EGRS75].)

Lean cross-check (google-deepmind/formal-conjectures, `ErdosProblems/727.lean`), fully
consistent with the site:
- Headline `erdos_727`: `answer(sorry) ↔ ∀ k ≥ 2, Set.Infinite {n : ℕ | (n+k)! ^ 2 ∣ (2*n)!}`.
- `erdos_727.variants.k_2` (research open): the $k=2$ case alone — a legitimately named open
  variant; resolving it affirmatively settles the variant but NOT the headline.
- `erdos_727.variants.k_1` (solved, True): Balakran's $k=1$ theorem — background.
- Lean's $n$ includes $0$, the site's starts at $1$: irrelevant for infinitude.

## What a complete resolution must establish

Exactly one branch, proved in full; the answer must not be assumed in advance.

**YES branch:** $\forall k \ge 2\ \forall N\ \exists n > N: ((n+k)!)^2 \mid (2n)!$
(i.e. $S_k$ is infinite for every fixed $k \ge 2$).

**NO branch:** $\exists k_0 \ge 2\ \exists N_0\ \forall n > N_0: ((n+k_0)!)^2 \nmid (2n)!$
(i.e. some single $S_{k_0}$ is finite).

**Monotonicity.** $S_{k+1} \subseteq S_k$ (since $(n+k)! \mid (n+k+1)!$). Hence YES $\iff$
$S_k$ infinite for arbitrarily large $k$; and one finite $S_{k_0}$ makes $S_k$ finite for all
$k \ge k_0$. Proving $S_2$ infinite resolves only the named $k=2$ variant; proving some single
$S_{k_0}$ finite resolves the entire headline negatively.

**Quantifier order.** $k$ is fixed FIRST; $n \to \infty$ afterwards; $k$ must never depend on
$n$. Inside the per-prime criterion below, the prime $p$ is universally quantified AFTER $n$ is
chosen: one $n$ must beat EVERY prime simultaneously. "Infinitely many $n$" permits arbitrarily
sparse families and forbids any finite list.

## Exact per-prime forms

By Legendre, $\nu_p(m!) = \sum_{i\ge1} \lfloor m/p^i \rfloor = \frac{m - s_p(m)}{p-1}$. Then
$$n \in S_k \iff \forall p:\ \nu_p((2n)!) \ge 2\nu_p((n+k)!) \iff \forall p:\ 2 s_p(n+k) - s_p(2n) \ge 2k.$$
(Second equivalence: $2n - s_p(2n) \ge 2(n+k) - 2s_p(n+k) \iff 2s_p(n+k) - s_p(2n) \ge 2k$.)

WARNING — the $2k$-deficit is the technical crux. Since $2(n+k) = 2n + 2k > 2n$, this is NOT
the central-binomial carry condition: the digit-sum inequality carries the additive constant
$2k$. The naive framing "enough base-$p$ carries when adding $(n+k)+(n+k)$" is wrong without
the deficit correction.

Exact carry forms (Kummer). With $m = n+k$:
- $\forall p$: $\#(\text{base-}p\text{ carries in } (n+k)+(n-k)) \ge \nu_p((n-k+1)(n-k+2)\cdots(n+k))$;
- $\forall p$: $\#(\text{base-}p\text{ carries in } (n+k)+(n+k)) \ge \nu_p((2n+1)(2n+2)\cdots(2n+2k))$;
- carries-vs-borrows: with $c_p = \#(\text{carries in } m + m)$ and $b_p = \#(\text{borrows in }
  (2m) - 2k)$, both base $p$, the identity
  $2 s_p(m) - s_p(2m-2k) - 2k = (p-1)(c_p - b_p) + s_p(2k) - 2k$ holds, so
  $$n \in S_k \iff \forall p:\ (p-1)(c_p - b_p) \ge 2k - s_p(2k).$$
  For $p > 2k$ the right side is $0$: the condition is exactly $c_p \ge b_p$. By Kummer,
  $c_p = \nu_p\binom{2m}{m}$ and $b_p = \nu_p\binom{2m}{2k}$, and since
  $2k - s_p(2k) = (p-1)\nu_p((2k)!)$, the full condition over all $p$ is equivalent to the
  product form below. For $k=2$ concretely: $c_2 - b_2 \ge 3$ at $p=2$; $c_3 - b_3 \ge 1$ at
  $p=3$; $c_p \ge b_p$ for all $p \ge 5$.

Product forms: for $n \ge k$,
$$n \in S_k \iff \prod_{j=n-k+1}^{n+k} j \,\Big|\, \binom{2n}{n+k}
        \iff \prod_{j=1}^{2k}(2n+j) \,\Big|\, \binom{2n+2k}{n+k}
        \iff (2m)(2m-1)\cdots(2m-2k+1) \,\Big|\, \binom{2m}{m} \text{ with } m = n+k.$$

Range of relevant primes: only $p \le n+k$ can fail (for $p > n+k$, $\nu_p((n+k)!) = 0$).
Every prime $p \in (n, n+k]$ DOES fail ($\nu_p((2n)!) = 1 < 2$), so all of $n+1, \dots, n+k$
must be composite for $n \in S_k$.

Large-prime criterion: for $p > \max(\sqrt{2n}, 2k)$, writing $n+k = qp + r$, $0 \le r < p$:
the condition at $p$ holds iff $r \ge k$, i.e. fails iff $p$ has a multiple in $(n, n+k]$.
Consequently every $n \in S_k$ with $n > 2k^2$ has $n+1, \dots, n+k$ all $\sqrt{2n}$-smooth,
and conversely along $\sqrt{2n}$-smooth windows all conditions at $p > \sqrt{2n}$ hold
automatically. ($p = 2$: note $s_2(2n) = s_2(n)$.)

## Sanity data (verified during prompt preparation; calibration gate)

- $k=1$: $S_1$ starts $5, 14, 27, 41, 44, 65, 76, 90, 109, 125, 139, 152, 155, 169, \dots$
  ($40$ elements up to $441$). $n=5$: $(6!)^2 = 518400 \mid 10! = 3628800$, quotient $7$.
- $k=2$: smallest element $n = 208$ (no $n < 208$ works). $S_2$ starts
  $208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, 2477, 2663, 2991, 3353, 3415,
  3430, 3439, 3475, 3476, 3551, \dots$; $|S_2 \cap [1, 2\cdot10^5]| = 1981$.
- $k=3$: $S_3$ starts $3475, 8174, 8175, 15195, 16168, 18682, 18743, 19290, \dots$;
  $|S_3 \cap [1, 6\cdot10^4]| = 41$.
- $k=4$: $S_4 \cap [1, 6\cdot10^4] = \{8174, 51984\}$.

## Known background that may be assumed (with attribution)

- **Balakran [Ba29]:** infinitely many $n$ with $((n+1)!)^2 \mid (2n)!$.
- **Catalan:** $(n+1) \mid \binom{2n}{n}$ for all $n \ge 0$.
- **EGRS75:** infinitely many $n$ with $(n+k)!\,(n+1)! \mid (2n)!$; holds whenever
  $k < c \log n$ for a small absolute $c > 0$.
- **Erdős [Er68c]:** $a!\,b! \mid n!$ forces $a + b \le n + O(\log n)$; so solutions of 727
  force $k = O(\log n)$ — fixed $k$ is exactly at the edge.
- Standard toolbox (hypotheses verified, uniformity in $p, n, k$ tracked): Legendre, Kummer,
  Bertrand/prime counting, smooth-number counts (Dickman–de Bruijn, Hildebrand), sieves, CRT,
  Pell/Störmer parametrizations, digit/exponential-sum equidistribution.

## What does NOT count

- $(n+k)!\,(n+1)! \mid (2n)!$ (that is EGRS75), or $k=1$ (Balakran), or any reproof of either.
- Finite lists of $n$; numerics of any size.
- $k$ growing with $n$ in any form.
- Affirmative resolution of some $k \ge 2$ but not all, presented as resolving the headline.
- Heuristic density/independence arguments.
- Shifted/weakened divisibilities: $((n+k)!)^2 \mid (2n+C)!$ with $C > 0$; bounded cofactors;
  conditions verified only for partial prime ranges.
- Misreadings: $(n+k^2)!$, $((n+k)^2)!$, reversed divisibility, trivial integrality of
  $\binom{2n}{n+k}$ confused with $\prod_{j=n-k+1}^{n+k} j \mid \binom{2n}{n+k}$.
- Reductions to unproved statements of comparable strength (infinitude of $k$-term
  $\sqrt{2n}$-smooth windows for $k \ge 3$ assumed rather than proved, smooth-neighbor
  conjectures, Schinzel/Bunyakovsky, digit equidistribution along sparse families).
- Conditional results (ABC, GRH, Cramér, etc.).
- Importing any statement about 727 itself from any source (arXiv 2601.07421 solves 728/729/401
  and explicitly does not claim 727; its methods are usable, its results prove nothing here).
- NO branch: gaps or density-0 statements about $S_{k_0}$; finiteness needs an
  eventual-obstruction proof for EVERY $n > N_0$.
