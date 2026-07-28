# LITERATURE.md — Route E: literature and toolbox verification for Erdős Problem 273

Background only. Nothing here is a step of a proof of Problem 273; this file records what the
covering-systems literature actually says, in citable form, and — for each item — whether its
hypotheses hold for
$$E=\{p-1:\ p\ \text{prime},\ p\ge 5\}=\{4,6,10,12,16,18,22,28,30,36,40,42,46,52,58,60,66,70,\dots\}.$$

---

## 0. VERIFICATION METHOD AND ITS LIMITS — READ FIRST

**Hard access limitation.** In this sandbox all outbound HTTPS is refused at the organisation's
egress gateway (`403` to `CONNECT` for every host tried: `arxiv.org`, `annals.math.princeton.edu`,
`link.springer.com`, `projecteuclid.org`, `doi.org`, `en.wikipedia.org`, `math.dartmouth.edu`,
`people.math.sc.edu`, `dms.umontreal.ca`, `par.nsf.gov`, `ar5iv.*`, `semanticscholar.org`, …).
`WebFetch` returns 403 for every URL as well. **No primary PDF could be opened.** The only working
channel was `WebSearch`, whose answers are machine summaries of the primary sources.

Consequently **nothing below is a verbatim transcription checked against a PDF**, unlike the house
standard used in `attempts/route-R8/TOOLBOX.md` for Erdős 727. Each item carries a verification tag:

| tag | meaning |
|---|---|
| **[V2]** | statement returned consistently by ≥ 2 independent search queries, wording stable, and consistent with the standard form of the result. Safe to quote as "the literature states", not as "verbatim". |
| **[V1]** | returned by exactly one query; wording plausible but single-sourced. Treat as provisional. |
| **[COMP]** | verified here by exact computation (script in `erdos-273/experiments/`, `E_`-prefixed). |
| **[U]** | could NOT be verified; reported as unconfirmed. Do not cite. |

**Anyone building on this file should re-verify the exact constants against the PDFs when network
access is available.** Items 4 (FFKPY quantitative reciprocal-sum rate) and 7 (effectivity of the
Filaseta–Kalogirou constant) are the two places where an unverified constant would actually matter.

**Compliance with the search restriction.** Only ordinary mathematical background and standard named
theorems were searched. No search was made for solutions, claims, forum posts or preprints about
Erdős Problem 273 itself, and no "proof" of it was read or imported. Two incidental notes:

* Two 2025 arXiv titles surfaced with "a question of Erdős and Graham … covering systems"
  (`arXiv:2501.15170`, Adenwalla; `arXiv:2504.09579`). A **title-and-topic-level** check (no further
  reading) shows they concern a *different* Erdős–Graham question — whether the divisors $>1$ of some
  $n$ can be the moduli of a distinct covering system in which any two congruences that are
  simultaneously satisfiable have coprime moduli. **Not Problem 273.** They were not read further.
* A 2025 item titled "Covering System with Restricted Moduli: Theory, Existence and …" appeared in
  *World Journal of Advanced Engineering Technology and Sciences* (`wjaets.com`). This is not a
  reputable mathematics venue; the search engine's synthesis of it produced sweeping "sieve
  obstruction theorems" for smooth/restricted-prime-factor moduli that appear nowhere in the
  refereed literature. **It was not read and nothing from it is used or endorsed below.** Flagged so
  that nobody later mistakes those synthesised claims for real theorems.

---

## 1. LOUD FLAGS — errors and traps in the working notes as handed to this route

**F1. WRONG AUTHOR NAME (certain).** The fourth author of the "distortion method" group is
**Julian SAHASRABUDHE**, not "Sawhney". The correct list is
**P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe, M. Tiba** (abbreviated **BBMST** below).
Every citation in the project must be corrected. (Mehtaab Sawhney is a different mathematician who,
as far as this search found, has no paper in this line.) **[V2]**

**F2. TRAP — there is NO density lower bound in terms of the plain reciprocal sum.** Our brief asked
"is there a theorem bounding the density of the uncovered set … in terms of the minimum modulus /
reciprocal sum?" The answer is subtler than the natural guess, and the natural guess is *false*:
FFKPY (2007) explicitly asked whether "moduli distinct and sufficiently large, $\sum 1/d_i<C$"
forces the uncovered set to have density $\ge \delta(C)>0$, and BBMST's Inventiones paper says this
condition **is not sufficient**; they prove a lower bound $e^{-4C}/2$ where $C$ is a *weighted*
reciprocal sum $\sum \mu(d_i)/d_i$ with $\mu(p^i)=1+(\log p)^{3+\varepsilon}/p$, and they show
**no** bound depending only on $C$ holds if the weight is any $1+O(1/p)$ (in particular not for the
plain sum). Any argument in this project that assumes "small reciprocal sum ⟹ positive uncovered
density" is unsound as stated. **[V2]**

**F3. TRAP — the infimum of $\sum 1/n_i$ over distinct covering systems is exactly $1$, and there is
NO absolute positive lower bound on the excess.** Distinct covering systems with least modulus
$m_0\in\{2,3,4\}$ exist with $\sum 1/n_i<1+\varepsilon$ for every prescribed $\varepsilon>0$. A
positive excess is guaranteed only once $m_0>4$ (Filaseta–Kalogirou 2024). **Since $4\in E$**, an
$E$-system that uses the modulus $4$ sits precisely in the regime where no positive excess bound
exists. See item 7. **[V2]**

**F4. Correctly remembered.** The following working-note claims came back verified and need no
correction: the DMNR statement (item 1); Hough's $10^{16}$ (item 2); the BBMST bound $616000$
(item 3 — statement, attribution and host paper verified; only the corollary's number inside the
paper is unconfirmed); Hough–Nielsen "divisible by 2 or 3" (item 5); Nielsen's least modulus 40, and
the Krukenberg/Choi/Gibson/Owens chain (item 8). The pairing "$616000$ + *On the Erdős covering
problem: the density of the uncovered set*, Invent. Math. **228** (2022)" in the brief is correct.

**F5. Mostly vacuous for $E$.** Hough ($m_0\le 616000$), Hough–Nielsen (some modulus divisible by 2
or 3), BBMST's squarefree-odd theorem and Cummings–Filaseta–Trifonov ($m_0\le118$ for squarefree
moduli) impose **no restriction at all** on $E$-systems: $\min E=4$, every element of $E$ is even,
and $E$ contains non-squarefree elements. The only imported theorem that genuinely constrains an
$E$-system is **Schinzel's conjecture, now a theorem of BBMST** (item 3(c)) — and the
**Dalton–Trifonov** least-modulus-4 constraints (item 8). **[COMP]/[V2]**

---

## 1b. EXACT FACTS ABOUT $E$ USED BELOW — all **[COMP]**

Computed by `erdos-273/experiments/E_applicability.py` (exact rationals where it matters; the large-$X$
budgets are float sums, which is ample for a $\log\log$ comparison).

* $\min E=4$ ($4=5-1$); $E\cap[4,200]$ begins $4,6,10,12,16,18,22,28,30,36,40,42,46,52,58,60,\dots$
* **Every element of $E$ is even** (checked on $E\cap[4,1000]$; trivially true since $p$ is odd).
* $E$ is **not** squarefree: $66$ of the $166$ elements of $E\cap[4,1000]$ are squarefree; the
  non-squarefree ones begin $4,12,16,18,28,36,40,52,60,72$.
* **Budget growth** $B(X)=\sum_{n\in E,\,n\le X}1/n$ against $\log\log X$:

  | $X$ | $|E\cap[4,X]|$ | $B(X)$ | $\log\log X$ | $B(X)-\log\log X$ |
  |---|---|---|---|---|
  | $10^2$ | 24 | 1.084145 | 1.527180 | $-0.443035$ |
  | $10^3$ | 166 | 1.471110 | 1.932645 | $-0.461535$ |
  | $10^4$ | 1227 | 1.756207 | 2.220327 | $-0.464120$ |
  | $10^5$ | 9590 | 1.978428 | 2.443470 | $-0.465042$ |
  | $10^6$ | 78496 | 2.160485 | 2.625792 | $-0.465307$ |
  | $10^7$ | 664577 | 2.314606 | 2.779943 | $-0.465337$ |

  So $B(X)=\log\log X-0.4653\ldots+o(1)$ (Mertens for shifted primes). **The budget is brutally
  scarce: $B(10^7)=2.31$, and reaching budget $3$ needs $X\approx e^{e^{3.465}}\approx8\times10^{13}$.**
* The budget first exceeds $1$ at $n=70$: $\sum_{n\in E,\,n\le70}1/n=162396943/160240080=1.01346\ldots$
  over the $18$ smallest elements, whose lcm is $480\,720\,240=2^4\cdot3^2\cdot5\cdot7\cdot11\cdot13\cdot23\cdot29$.
* Divisibility inside $E$ (Schinzel): $85$ pairs $a<b\le200$ in $E$ with $a\mid b$; **no** element of
  $E\cap[4,200]$ fails to divide some larger element of $E$ below $10^4$.
* Divisors of $360$ lying in $E$: $\{4,6,10,12,18,30,36,40,60,72,180\}$, reciprocal sum
  $7/9=0.7\overline7<1$ — so the Selfridge template's modulus set is *budget-infeasible* once the
  modulus 2 is removed (item 9).

---

## 2. THE ITEMS

### Item 1 — Davenport–Mirsky–Newman–Rado (DMNR)

**Statement (as the literature gives it).** Let $a_1\ (\mathrm{mod}\ n_1),\dots,a_k\
(\mathrm{mod}\ n_k)$, $k\ge2$, be an **exact** (= disjoint) cover of $\mathbb Z$, with the moduli
ordered $n_1\le n_2\le\cdots\le n_k$. Then $n_{k-1}=n_k$: the largest modulus occurs at least twice.
Equivalently: **there is no exact cover of $\mathbb Z$ by $k\ge2$ residue classes with pairwise
distinct moduli.** **[V2]**

**Standard proof (recorded because it is short and we may want it in a draft).** For $|z|<1$,
disjointness plus covering gives
$\sum_{s=1}^{k} z^{a_s}/(1-z^{n_s})=\sum_{n\ge0}z^{n}=1/(1-z)$.
If $n_{k-1}<n_k$, let $z\to e^{2\pi i/n_k}$ radially: every term on the left stays bounded except the
$s=k$ term, which blows up, while the right side tends to a finite limit — contradiction. **[V2]**

**Attribution.** Conjectured by Erdős (1950); proved shortly after by **L. Mirsky and D. J. Newman**,
who never published it; the same proof was found independently by **H. Davenport and R. Rado**.
Hence the four-name attribution. **[V2]**

**Refinement (Znám 1968/69; M. Newman 1971).** In an exact cover, if $N$ denotes the largest modulus
then $N$ occurs at least $p$ times, where $p$ is the smallest prime factor of $N$. **[V2]** — one
search summary instead reported "$p$ = smallest prime dividing the lcm of the moduli"; the two
differ, and I could not open either primary source. Use the $N$-version, and re-check before citing.
**[V1 on which of the two variants is the published one]**
References: Š. Znám, *On exactly covering systems of arithmetic sequences*, Math. Ann. **180** (1969),
227–232; M. Newman, *Roots of unity and covering sets*, Math. Ann. **191** (1971), 279–282. **[U on
exact volume/page data — not opened]**

**Does it apply to $E$?** Yes, formally: any covering system with moduli in $E$ has distinct moduli
all $>1$, so it can never be exact — some integer is covered at least twice, i.e. the excess
$\sum 1/n_i-1>0$ is strictly positive. That is the *only* thing DMNR gives.

**Branch.** Neither. It gives $\sum_{i}1/n_i>1$ (strict) for any $E$-system, which is a necessary
condition already satisfied by $E$ from the 18th element on (see item 7 and `E_applicability.py`).
It is *not* a source of a quantitative excess: see F3.

---

### Item 2 — Hough, minimum modulus problem

**Reference.** R. D. Hough, *Solution of the minimum modulus problem for covering systems*,
**Ann. of Math. (2) 181 (2015), no. 1, 361–382**; DOI `10.4007/annals.2015.181.1.6`;
preprint `arXiv:1307.0874`. **[V2]**

**Definition used there.** A *distinct covering system* is a finite collection of congruences
$a_i \bmod m_i$ with $1<m_1<m_2<\cdots<m_k$ such that every integer satisfies at least one of them.
(Identical to our PROBLEM.md convention.) **[V2]**

**Theorem 1 (Hough).** *The least modulus of a distinct covering system is at most $10^{16}$.*
**[V2]** (Method: Lovász Local Lemma / "sieve of Eratosthenes"-style density estimates with a
carefully chosen probability measure.)

**Does it apply to $E$?** The hypothesis holds (an $E$-system is a distinct covering system), but the
conclusion is vacuous: $\min E=4\le 10^{16}$, and indeed $E$ has $\ge 1$ element below $616000$.

**Branch.** Neither. Hough's theorem cannot obstruct $E$; it only says a covering system cannot avoid
small moduli, and $E$ contains small moduli.

---

### Item 3 — BBMST: the $616000$ bound and the density of the uncovered set

**(a) Reference.** P. Balister, B. Bollobás, R. Morris, **J. Sahasrabudhe**, M. Tiba,
*On the Erdős covering problem: the density of the uncovered set*,
**Invent. Math. 228 (2022), 377–414**; DOI `10.1007/s00222-021-01087-5`; preprint `arXiv:1811.03547`.
**[V2]** (See F1: not "Sawhney".)

**(b) Main theorem (Theorem 1.1), as the paper's abstract states it.**
Erdős–Graham conjectured: if the moduli are distinct elements of $[n,Cn]$ and $n$ is large, the
density of uncovered integers is bounded below by a constant depending only on $C$; this was proved
by FFKPY (2007), who further asked whether the same holds assuming only that the moduli are distinct,
sufficiently large, and $\sum_{i=1}^k 1/d_i<C$. **BBMST show that this condition is *not* sufficient,
and give an essentially best possible condition that is:**

> if all of the moduli are sufficiently large, then the union misses a set of density at least
> $e^{-4C}/2$, where $C=\sum_{i=1}^{k}\mu(d_i)/d_i$ and $\mu$ is the multiplicative function with
> $\mu(p^i)=1+(\log p)^{3+\varepsilon}/p$ for some $\varepsilon>0$;
>
> and no such lower bound (depending only on $C$) holds when $\mu(p^i)$ is replaced by any function
> of the form $1+O(1/p)$.

**[V2]** — the two independent retrievals agreed on the weight $\mu(p^i)=1+(\log p)^{3+\varepsilon}/p$
and the constant $e^{-4C}/2$. **[U]** on the precise meaning of "sufficiently large" (whether the
threshold depends on $C$ and $\varepsilon$, and whether it is effective).

**Answer to the brief's question.** *Is there a theorem bounding the density of the uncovered set, or
the reciprocal sum, in terms of the minimum modulus?* — **Not in the plain form we hoped.** What
exists is: (i) FFKPY's $[N,CN]$ theorem (item 4); (ii) BBMST's weighted-sum theorem above, whose
hypothesis is "all moduli sufficiently large", **not** a hypothesis on the minimum modulus alone; and
(iii) the qualitative FFKPY/Erdős–Selfridge statement "bounded reciprocal sum ⟹ bounded least
modulus". The naive statement is **false** — see F2.

**(c) Second main theorem: Schinzel's conjecture (1967), now proved.**
*Every covering system with distinct moduli contains two moduli $n_i\ne n_j$ with $n_i\mid n_j$.*
**[V2]** (Stated in the same Inventiones paper as their second main theorem.)

**(d) The constant $616000$.** Several independent sources state: "In 2022 Balister, Bollobás, Morris,
Sahasrabudhe and Tiba reduced Hough's bound to $616\,000$ by the distortion method", i.e. *every
covering system with distinct moduli has minimum modulus $\le 616000$.* **[V2]**
A later retrieval of the Inventiones article page states that the paper "provides an alternative
(somewhat simpler) proof of a breakthrough result of Hough … with an improved bound", so the
$616000$ lives in **this** paper (as a corollary of Theorem 1.1); the corollary's number inside the
paper is still **[U]**. The expository account of the method is *Erdős covering systems*,
**Acta Math. Hungar. 161 (2020), 540–549**, DOI `10.1007/s10474-020-01048-z` (`arXiv:2211.01417`,
an 8-page note). The same page also records "further progress on the problem of Erdős and Selfridge"
(the odd-moduli problem). **[V1]**

**(e) Companion paper.** BBMST, *The structure and number of Erdős covering systems*,
**J. Eur. Math. Soc. 26 (2024), no. 1, 75–109** (`arXiv:1904.04806`): the number of minimal covering
systems with exactly $n$ elements is $\exp\big((\tfrac{4\sqrt\tau}{3}+o(1))\,n^{3/2}/(\log n)^{1/2}\big)$,
answering a 1952 question of Erdős. **[V1]** (constant $\tau$ unverified). Not directly usable here.

**Hypotheses vs. $E$.**
* (b) needs *all* moduli large. An $E$-system contains 4 (or at least small elements of $E$), so
  Theorem 1.1 cannot be applied to the whole system. It *can* be applied to the sub-family of large
  moduli, but then it bounds only the density uncovered by that sub-family — the small moduli are
  unconstrained. Usable only in a hybrid argument.
* (c) **applies verbatim to $E$** and is a real constraint: an $E$-covering must contain $n_i\mid n_j$
  with both in $E$. `E_applicability.py` shows this is easy to satisfy inside $E$ (e.g.
  $4\mid12,\ 6\mid12,\ 6\mid18,\ 4\mid16,\ 6\mid30,\ 4\mid40$), so it is not fatal — but any
  construction or search that produces a divisibility antichain of $E$-moduli is provably doomed.
* (d) vacuous for $E$ (as item 2).

**Branch.** (c) helps the **NO** branch only as a structural filter, and helps the **YES** branch as
a *design rule* (build in divisibility chains). (b) is the right shape for a NO argument but its
hypothesis fails for $E$ as a whole; and F2 blocks the naive reciprocal-sum version.

---

### Item 4 — Filaseta, Ford, Konyagin, Pomerance, Yu (2007)

**Reference.** M. Filaseta, K. Ford, S. Konyagin, C. Pomerance, G. Yu, *Sieving by large integers and
covering systems of congruences*, **J. Amer. Math. Soc. 20 (2007), no. 2, 495–517**;
preprint `arXiv:math/0507374`. **[V2]**

**What they prove.** The paper states three conjectures and proves strong forms of all three:

* **Conjecture 1 (Erdős–Selfridge, 1973).** If $S$ is a finite set of integers $>N$ and residues
  $r(n)\bmod n$ $(n\in S)$ cover $\mathbb Z$, and $\sum_{n\in S}1/n$ is bounded, then the least
  element of $S$ is bounded. Equivalently: for every $B>0$ there is $N_B$ such that a covering system
  with distinct moduli all $>N_B$ has $\sum 1/n_i>B$. **PROVED.** **[V2]**
* **Conjecture 2 (Erdős–Graham).** For each fixed $K>1$ there is $d_K>0$ such that for $N$ large, the
  complement of any union of residue classes $r(n)\bmod n$ over distinct $n\in(N,KN]$ has density
  $\ge d_K$. **PROVED, in a strong form:** **[V2]**

  > if $1<C\le N^{\log\log\log N/(4\log\log N)}$, then for any $N\le n_1<\cdots<n_k\le CN$ and any
  > choice of residue classes, the density of integers not covered is at least
  > $(1-o(1))\prod_{i}(1-1/n_i)$.

  **[V2]** (two independent retrievals; the second added the $(1-o(1))$ factor). One retrieval added
  that the bound is tight — the density is attained for some choice of residues. **[V1]**
* **Conjecture 3.** If $S$ is a finite set of moduli $>N$ admitting residues covering $\mathbb Z$,
  then $\max S$ cannot be $O(N)$. **PROVED.** **[V2]**

**What I could NOT verify.** The **explicit quantitative growth rate** of $\sum_{n\in S}1/n$ as a
function of the least modulus $N$. Sources uniformly paraphrase it as "the sum of the reciprocals of
the moduli grows quickly with the minimum modulus", and I could not open the paper to extract the
inequality. **Do not quote a rate.** **[U]**
(Heuristic only, *not* literature: iterating the $[N,CN]$ theorem over consecutive windows with
$C=N^{\log\log\log N/4\log\log N}$ gives a number of windows up to $X$ that is a slowly growing
function of $\log X$, so the honest expectation is an *iterated-logarithmic* rate — far too weak to
beat $E$'s $\log\log$-sized budget by itself. Flagged as inference.)

**Hypotheses vs. $E$.** The $[N,CN]$ theorem applies to *any* set of distinct moduli in such a window,
so it applies to the part of an $E$-system lying in a window $[N, N^{1+\gamma}]$,
$\gamma\le\log\log\log N/(4\log\log N)$. Note that within any such window the whole of $E$ carries
budget only
$\sum_{n\in E\cap[N,CN]}1/n\approx\log\frac{\log CN}{\log N}\le\log(1+\gamma)\to0$,
so the windowed theorem says the large-modulus part of an $E$-system is essentially "independent
sieving" and contributes essentially nothing. Conjecture 1's conclusion, however, is **not**
applicable: it needs *all* moduli $>N_B$, and $4\in E$.

**Branch.** The **NO** branch — this is the strongest genuinely quantitative import available. But it
constrains only the tail; a complete NO proof still has to handle the small $E$-moduli
$4,6,10,12,16,\dots$, which is exactly where the problem's difficulty lives.

---

### Item 5 — Hough–Nielsen, and follow-ups

**Reference.** R. D. Hough, P. P. Nielsen, *Covering systems with restricted divisibility*,
**Duke Math. J. 168 (2019), no. 17, 3261–3295**; DOI `10.1215/00127094-2019-0058`;
preprint `arXiv:1703.02133`. **[V2]**

**Theorem 1 (Hough–Nielsen).** *Every distinct covering system of congruences has a modulus divisible
by either $2$ or $3$.* **[V2]** — i.e. there is no covering system whose (distinct, $>1$) moduli are
all coprime to $6$. Method: Lovász Local Lemma with a CRT-based dependency graph.

**The working note's version of this item is CORRECT.**

**Follow-ups.**
* J. Klein, D. Koukoulopoulos, S. Lemieux, *On the $j$-th smallest modulus of a covering system with
  distinct moduli*, **Int. J. Number Theory 20 (2024), no. 2, 471–479**; DOI
  `10.1142/S1793042124500234`; `arXiv:2212.01299`.
  **Theorem 1.** There is an absolute $c>0$ such that the $j$-th smallest modulus of a **minimal**
  covering system with distinct moduli is $\le\exp\!\big(cj^{2}/\log(j+1)\big)$. ("Minimal" = no
  proper subfamily covers $\mathbb Z$; the hypothesis is necessary, since redundant large moduli can
  otherwise be inserted.) **Theorem 2** (complementary construction): for each $j\ge5$ there is a
  minimal covering system with $j$ distinct moduli
  $2<2^2<\cdots<2^{j-4}<3\cdot2^{j-5}<2^{j-3}<3\cdot2^{j-4}<3\cdot2^{j-3}$. **[V2]** for Theorem 1;
  **[V1]** for the exact form of Theorem 2's chain (the retrieved list looks garbled in its ordering
  and should be re-checked).
* B. Cummings, M. Filaseta, O. Trifonov, *An upper bound for the minimum modulus in a covering system
  with squarefree moduli*, **Acta Math. Hungar.** (2024/25); DOI `10.1007/s10474-024-01496-x`;
  `arXiv:2211.08548`. **Theorem.** If a covering system has distinct squarefree moduli then its
  minimum modulus is at most **118**. They also show the $k$-th smallest modulus of a covering system
  with distinct moduli (provided it is needed for the covering) is bounded by an absolute constant.
  **[V2]**

**Hypotheses vs. $E$.** *Every element of $E$ is even* (**[COMP]**), so Hough–Nielsen is satisfied
automatically and gives **nothing**. The squarefree results do not apply: $E$ contains many
non-squarefree elements ($4,12,16,18,28,36,40,52,60,72,\dots$) and an $E$-system need not be
squarefree. KKL applies to any minimal $E$-covering and bounds its $j$-th smallest modulus, but the
bound $\exp(cj^2/\log j)$ is astronomically weak for our purposes and $c$ is not made explicit here.

**Branch.** Neither, for $E$. These are the theorems people reach for first and they are all vacuous
on an all-even modulus set.

---

### Item 6 — covering systems with moduli in a prescribed thin set: what is actually known

Ordered from strongest to weakest, restricted to refereed results.

1. **Odd moduli (Erdős–Selfridge problem).** *Is there a covering system with distinct odd moduli
   $>1$?* — **OPEN**, and one of the best-known problems in the area. **[V2]**
   Partial results:
   * R. J. Simpson, D. Zeilberger, *Necessary conditions for distinct covering systems with
     square-free moduli*, Acta Arith. **59** (1991), 59–70: such a system needs at least **18** primes.
     **[V1]**
   * S. Guo, Z.-W. Sun, *On odd covering systems with distinct moduli*, **Adv. in Appl. Math. 35
     (2005), 182–187**: if a covering system with odd, distinct, squarefree moduli exists, the lcm of
     the moduli has at least **22** prime divisors. **[V2]**
   * **BBMST, *The Erdős–Selfridge problem with square-free moduli*, Algebra Number Theory 15 (2021),
     no. 3, 609–626** (`arXiv:1901.11465`): **if the moduli of a covering system are distinct and
     squarefree, then some modulus is even.** I.e. the squarefree case of the odd problem is
     completely settled. **[V2]**
   * J. Harrington, Y. Sun, W. H. T. Wong, *Covering systems with odd moduli*, **Discrete Math. 345
     (2022), 112936**: variant in which one odd prime modulus may repeat, all others distinct, odd,
     $>1$; and the squarefree sub-case. **[V2]** (abstract retrieved; exact theorems not verified).
   * A 2025 sequel *A further investigation on covering systems with odd moduli* exists
     (`arXiv:2507.16135`). **[U]** — not examined.
2. **Squarefree moduli.** Minimum modulus $\le118$ (Cummings–Filaseta–Trifonov, item 5). **[V2]**
3. **Moduli coprime to 6 / with restricted prime divisors.** Impossible (Hough–Nielsen, item 5).
   **[V2]**
4. **Moduli restricted to the divisors of a fixed $L$ — "covering numbers".** Z.-W. Sun (2007)
   defines $L$ to be a *covering number* if some covering system has distinct moduli that are
   divisors of $L$ greater than $1$; $L$ is *primitive* if no proper divisor of $L$ is a covering
   number. Sun's sufficient criterion: if $p_1<\cdots<p_r$ are primes and $\alpha_1,\dots,\alpha_r\ge1$
   satisfy $\prod_{t\le s}(\alpha_t+1)\ \ge\ p_s-1+\delta_{r,s}$ for every $s$, then
   $L=\prod p_i^{\alpha_i}$ is a covering number. **[V1]** (the exact form of the $\delta_{r,s}$ term
   should be re-checked). Follow-ups: *On primitive covering numbers*, Int. J. Number Theory 13
   (2017) (`arXiv:1406.6851`), and *New primitive covering numbers and their properties*, J. Number
   Theory (2016). **[V1]**
   *This is the closest existing framework to our problem*: an $E$-system is exactly a covering system
   whose moduli are divisors of $L=\mathrm{lcm}$ lying in the thin set $E$. The literature on covering
   numbers does **not** restrict which divisors may be used, so it does not transfer directly.
5. **Shifted primes $p-1$ or $p+1$, smooth numbers, numbers with a bounded number of prime factors.**
   **I found NO refereed work on covering systems whose moduli are restricted to any of these sets**,
   beyond the Erdős–Graham question itself (our problem) and the Selfridge example of item 9.
   The only hit was the non-reputable `wjaets.com` item flagged in §0, which was not read.
   **[V1 — a negative literature finding, i.e. "no evidence found", not a proof of non-existence;
   with the sandbox restricted to a search engine this is weaker evidence than usual.]**

**Branch.** Neither, directly. The message for the project is: **the thin-set covering literature is
essentially empty except for the odd/squarefree lines, and every tool there exploits a *parity or
squarefree* structure that $E$ does not have** (all $E$-elements are even, and $E$ contains plenty of
non-squarefree elements $4,12,16,18,28,36,\dots$). Expect no off-the-shelf theorem to decide 273.

---

### Item 7 — the minimum of $\sum 1/n_i$ over covering systems with distinct moduli

This is the quantitatively decisive item for our problem, and the answer is **not** the convenient one.

**Baseline.** Density gives $\sum_i 1/n_i\ge1$ for any covering system (counted with multiplicity),
and DMNR (item 1) upgrades it to $\sum_i 1/n_i>1$ strictly for a finite **distinct** covering system
with $m_0>1$. **[V2]**

**Infimum.** **The infimum is exactly $1$ and it is not attained.** There exist finite distinct
covering systems with least modulus $m_0\in\{2,3,4\}$ and $\sum 1/n_i<1+\varepsilon$ for **any**
prescribed $\varepsilon>0$. **[V2]** (stated in the introduction of Filaseta–Kalogirou, below; the
attribution of these constructions to a specific author was **not** determined — **[U]**).

**Davenport's 1952 problem / the Erdős–Selfridge 1973 belief.** Davenport asked for a condition on the
minimum modulus $m_0$ of a finite distinct covering system forcing $\sum1/n_i$ to be **bounded away
from 1**; in 1973 Erdős and Selfridge said they believed $m_0>4$ suffices. **[V2]**

**Theorem (M. Filaseta, A. Kalogirou, 2024).** *This is the case: for finite distinct covering systems
with minimum modulus $m_0>4$, the sum of the reciprocals of the moduli is bounded away from $1$.*
**[V2]**
Reference: *Covering systems with the sum of the reciprocals of the moduli close to $1$*,
`arXiv:2407.15280` (submitted 21 July 2024). **[U]** on journal publication status, on whether the
bound is **explicit/effective**, and on the size of the excess. This matters: an ineffective or
microscopic excess is useless for us.

**Hypotheses vs. $E$ — the crux.**
* $\min E=4$. **[COMP]** So an $E$-covering that uses the modulus $4$ has $m_0=4$, i.e. sits exactly
  **outside** Filaseta–Kalogirou and inside the regime where $\sum1/n_i$ can be $1+\varepsilon$.
  Nothing in the literature then bounds the excess from below by an absolute constant.
* An $E$-covering that does **not** use $4$ has $m_0\ge6>4$, so Filaseta–Kalogirou applies and the
  excess is bounded away from $0$ by an absolute constant $\delta$ — but $\delta$ is not known to us
  and may be tiny.
* $E$'s total budget is unbounded but grows like $\log\log X$: measured,
  $\sum_{n\in E,\,n\le X}1/n=\sum_{5\le p\le X+1}1/(p-1)=\log\log X-0.4653\ldots+o(1)$ (§1b,
  **[COMP]**; the constant is the shifted-prime Mertens constant). So a budget-based NO argument must
  beat a *growing* budget and cannot rest on $\sum1/n_i>1$ alone (the 18 smallest elements of $E$
  already exceed 1: `E_basics.py`, `E_applicability.py`) — but the growth is so slow
  ($B(10^7)=2.31$) that any *fixed* required excess $>1.32$ would already force astronomically large
  moduli. This is the one place where a verified numerical excess bound would be decisive, and it is
  exactly the number the literature does not supply (see **[U]** above).

**Branch.** Both branches are informed, neither is decided. For **NO**: any argument of the form
"$E$-systems cannot afford the required excess" must supply the excess bound itself, because the
literature supplies none in the $m_0=4$ regime and only an unverified constant for $m_0\ge5$.
For **YES**: the $m_0\in\{2,3,4\}$ near-optimal constructions are an existence proof that extremely
efficient distinct covering systems exist at least modulus 4 — but they are not known to be
realisable with moduli from $E$.

---

### Item 8 — explicit covering systems with prescribed least modulus

Chronology (all systems have distinct moduli):

| least modulus $m_0$ | author | reference | notes |
|---|---|---|---|
| 2 | folklore | — | $\{0(2),0(3),1(4),5(6),7(12)\}$; $\sum1/n_i=\tfrac43$, lcm $12$ **[COMP]** |
| up to 18 | C. E. Krukenberg | PhD thesis, Univ. of Illinois at Urbana–Champaign, 1971 | the $m_0=18$ system uses divisors of $2^7\cdot3^3\cdot5^2\cdot7^2\cdot11^2\cdot13^2\cdot17^2\cdot19=475\,371\,719\,222\,400$ as moduli **[V2]** (product re-checked **[COMP]**) |
| 20 | S. L. G. Choi | *Covering the set of integers by congruence classes of distinct moduli*, Math. Comp. **25** (1971), 885–895 | **[V2]** |
| 25 | D. J. Gibson | *A covering system with least modulus 25*, Math. Comp. **78** (2009), 1127–1146 | moduli are divisors $\ge25$ of $L_1=2^5\cdot3^3\cdot5^2\cdot7^2\cdot11\cdot13\cdot17$, extended by $19,23,29^7$; built in three stages **[V1]**, exponents partially garbled in retrieval |
| 40 | P. P. Nielsen | *A covering system whose smallest modulus is 40*, J. Number Theory **129** (2009), no. 3, 640–666 | introduced recursion into the construction **[V2]** (volume/issue/pages confirmed) |
| **42** | T. Owens | MSc thesis, Brigham Young University, 2014 | current record; **over $10^{50}$ congruences**; refines Nielsen's recursion **[V2]** |

Krukenberg's and Gibson's notation for describing such systems is what made Nielsen's and Owens's
$10^{50}$-congruence systems writable at all. **[V2]**

**Reciprocal sums.** **[U] — not obtainable.** None of the retrieved sources reports
$\sum1/n_i$ for the $m_0\in\{18,20,25,40,42\}$ systems, and the systems are far too large to
reconstruct here (Owens: $>10^{50}$ congruences). What *is* known qualitatively: by FFKPY these sums
must grow with $m_0$, and by Filaseta–Kalogirou they are bounded away from $1$ for $m_0\ge5$. Do not
guess numbers.

**Extremal constraints (very relevant to $E$, whose least modulus is 4).**
J. Dalton, O. Trifonov, *Extreme covering systems of the integers*,
**J. Integer Seq. 25 (2022), Article 22.9.1** (`arXiv:1905.07386`): for a distinct covering system,
* if the least modulus is $3$, the lcm of the moduli is $\ge120$;
* **if the least modulus is $4$, the largest modulus is $\ge60$ and the lcm of the moduli is $\ge360$;**
and the constants $60,120,360$ are best possible. **[V2]**
Follow-up: *On a conjecture of Krukenberg and a problem of Dalton and Trifonov*, INTEGERS **26**
(2026), #A38 (`arXiv:2508.18062`). **[V1]**

**Does it apply to $E$?** Yes — directly. Any covering system with moduli in $E$ that uses the modulus
$4$ (i.e. has $m_0=4$) must have $\mathrm{lcm}\ge360$ and a modulus $\ge60$. Note $60\in E$ and
$\mathrm{lcm}$ of the 18 smallest elements of $E$ is $480\,720\,240\gg360$, so this is a weak but
genuine and *verified* necessary condition, and it is the correct sanity check for any small search.

**Branch.** These are the concrete templates for the **YES** branch (what a least-modulus-$m_0$ system
looks like), and Dalton–Trifonov gives cheap necessary conditions usable as search filters.

---

### Item 9 — Selfridge's system with all moduli of the form $p-1$, $p=3$ allowed

**Status of the attribution.** Erdős–Graham (*Old and new problems and results in combinatorial number
theory*, Monogr. Enseign. Math. **28**, Genève, 1980, p. 24) pose the $p\ge5$ question (our Problem
273) and record that Selfridge found such a system when $p=3$ is allowed (so the modulus $2$ is
permitted), with moduli dividing $360$. **This attribution is taken from the project's own PROBLEM.md
and from the standard framing of the problem; I did NOT attempt to verify it against the
Erdős–Graham monograph or any page about Problem 273, per the search restriction. [U on the
attribution and on Selfridge's actual list of congruences.]**

**What I *did* establish, independently and exactly. [COMP]**
Script: `erdos-273/experiments/E_selfridge360.py` (exhaustive DFS over $\mathbb Z/360\mathbb Z$,
exact integer arithmetic, each modulus usable at most once, plus an independent element-wise
re-verification of the returned system).

* The divisors $d>1$ of $360$ with $d+1$ prime are exactly
  $$A=\{2,4,6,10,12,18,30,36,40,60,72,180\},\qquad \sum_{d\in A}\tfrac1d=\tfrac{23}{18}=1.2\overline{7}.$$
* **A covering system with all moduli in $A$ exists.** One explicit witness (all 12 moduli used, all
  distinct, all of the form $p-1$ with $p$ prime, all dividing $360$):

  | $a$ | mod $n$ | $p=n+1$ |
  |---|---|---|
  | 0 | 2 | 3 |
  | 1 | 4 | 5 |
  | 3 | 6 | 7 |
  | 7 | 10 | 11 |
  | 11 | 12 | 13 |
  | 1 | 18 | 19 |
  | 1 | 30 | 31 |
  | 7 | 36 | 37 |
  | 23 | 40 | 41 |
  | 19 | 60 | 61 |
  | 67 | 72 | 73 |
  | 175 | 180 | 181 |

  Verified: every residue mod $360$ is covered; moduli pairwise distinct; each $n+1$ prime;
  $\sum 1/n=23/18$. (This need not be Selfridge's own system — it is *a* system of exactly the
  advertised shape, which confirms that the $p\ge3$ variant is genuinely solvable inside the divisors
  of 360.)
* **Removing the modulus $2$ (i.e. the $p\ge5$ world restricted to divisors of $360$) kills it
  immediately:** $A\setminus\{2\}$ has reciprocal sum $7/9=0.7\overline{7}<1$, and the exhaustive
  search confirms no covering exists. So the whole weight of Selfridge's construction rests on the
  single class $0\ (\mathrm{mod}\ 2)$, which carries half of $\mathbb Z$ and is exactly what Problem
  273 forbids.

**Branch.** This is a **calibration** result, not a proof ingredient: it shows the $p\ge3$ variant is
easy and that its solution degenerates entirely when $2$ is removed. It also shows the natural
"divisors of a smooth $L$" template must be pushed to much larger $L$ for the $p\ge5$ problem, since
$E\cap\mathrm{Div}(360)$ has budget $<1$.

---

## 3. SUMMARY TABLE: does the tool bite on $E$?

| # | result | hypotheses hold for $E$? | use |
|---|---|---|---|
| 1 | DMNR / Znám–Newman | yes | gives only $\sum1/n_i>1$ strictly |
| 2 | Hough $10^{16}$ | yes, conclusion vacuous ($\min E=4$) | neither |
| 3b | BBMST weighted-density | **no** — needs all moduli large | hybrid only |
| 3c | Schinzel (BBMST) | **yes** | NO-filter / YES design rule: need $n_i\mid n_j$ inside $E$ |
| 3d | BBMST $616000$ | yes, vacuous | neither |
| 4 | FFKPY $[N,CN]$ density $\ge(1-o(1))\prod(1-1/n_i)$ | yes, on any window | best quantitative import; controls the tail only |
| 4' | FFKPY Erdős–Selfridge (all moduli $>N$) | **no** ($4\in E$) | neither |
| 5 | Hough–Nielsen "2 or 3" | yes, vacuous (all of $E$ even) | neither |
| 5' | KKL $j$-th modulus | yes (minimal systems) | far too weak numerically |
| 6 | odd / squarefree thin-set theorems | **no** | neither |
| 7 | Filaseta–Kalogirou $m_0>4$ | only if $4\notin$ system | NO branch, constant unverified |
| 8 | Dalton–Trifonov $m_0=4\Rightarrow$ lcm $\ge360$, $\max\ge60$ | yes, if $4$ is used | cheap search filter |
| 9 | Selfridge $p\ge3$ (verified here) | — | calibration only |

---

## 4. BIBLIOGRAPHY (with the identifiers that were verifiable)

* P. Erdős, R. L. Graham, *Old and new problems and results in combinatorial number theory*,
  Monographies de L'Enseignement Mathématique **28**, Genève, 1980. (Source of Problem 273, p. 24.)
* Š. Znám, *On exactly covering systems of arithmetic sequences*, Math. Ann. **180** (1969), 227–232. **[U]**
* M. Newman, *Roots of unity and covering sets*, Math. Ann. **191** (1971), 279–282. **[U]**
* S. L. G. Choi, *Covering the set of integers by congruence classes of distinct moduli*,
  Math. Comp. **25** (1971), 885–895.
* C. E. Krukenberg, *Covering sets of the integers*, PhD thesis, Univ. of Illinois, 1971.
* R. J. Simpson, D. Zeilberger, Acta Arith. **59** (1991), 59–70. **[V1]**
* S. Guo, Z.-W. Sun, *On odd covering systems with distinct moduli*, Adv. in Appl. Math. **35**
  (2005), 182–187.
* M. Filaseta, K. Ford, S. Konyagin, C. Pomerance, G. Yu, *Sieving by large integers and covering
  systems of congruences*, J. Amer. Math. Soc. **20** (2007), 495–517. `arXiv:math/0507374`.
* Z.-W. Sun, *On covering numbers*, in Combinatorial Number Theory (2007). **[V1]**
* D. J. Gibson, *A covering system with least modulus 25*, Math. Comp. **78** (2009), 1127–1146.
* P. P. Nielsen, *A covering system whose smallest modulus is 40*, J. Number Theory **129** (2009),
  no. 3, 640–666.
* T. Owens, *A covering system with minimum modulus 42*, MSc thesis, Brigham Young Univ., 2014. **[V1]**
* R. D. Hough, *Solution of the minimum modulus problem for covering systems*, Ann. of Math. (2)
  **181** (2015), 361–382. DOI `10.4007/annals.2015.181.1.6`. `arXiv:1307.0874`.
* R. D. Hough, P. P. Nielsen, *Covering systems with restricted divisibility*, Duke Math. J. **168**
  (2019), 3261–3295. DOI `10.1215/00127094-2019-0058`. `arXiv:1703.02133`.
* P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe, M. Tiba, *Erdős covering systems*,
  Acta Math. Hungar. **161** (2020), 540–549. DOI `10.1007/s10474-020-01048-z`. `arXiv:2211.01417`.
* — , *The Erdős–Selfridge problem with square-free moduli*, Algebra Number Theory **15** (2021),
  609–626. `arXiv:1901.11465`.
* — , *On the Erdős covering problem: the density of the uncovered set*, Invent. Math. **228** (2022),
  377–414. DOI `10.1007/s00222-021-01087-5`. `arXiv:1811.03547`.
* — , *The structure and number of Erdős covering systems*, J. Eur. Math. Soc. **26** (2024), 75–109.
  `arXiv:1904.04806`. **[V1]**
* J. Dalton, O. Trifonov, *Extreme covering systems of the integers*, J. Integer Seq. **25** (2022),
  Art. 22.9.1. `arXiv:1905.07386`.
* J. Harrington, Y. Sun, W. H. T. Wong, *Covering systems with odd moduli*, Discrete Math. **345**
  (2022), 112936.
* J. Klein, D. Koukoulopoulos, S. Lemieux, *On the $j$-th smallest modulus of a covering system with
  distinct moduli*, Int. J. Number Theory **20** (2024), 471–479. DOI `10.1142/S1793042124500234`.
  `arXiv:2212.01299`.
* B. Cummings, M. Filaseta, O. Trifonov, *An upper bound for the minimum modulus in a covering system
  with squarefree moduli*, Acta Math. Hungar. (2024/25). DOI `10.1007/s10474-024-01496-x`.
  `arXiv:2211.08548`.
* M. Filaseta, A. Kalogirou, *Covering systems with the sum of the reciprocals of the moduli close to
  $1$*, `arXiv:2407.15280` (2024).
* Balister (ed. Fischer–Johnson), *Erdős covering systems*, in **Surveys in Combinatorics 2024**,
  LMS Lecture Note Ser. **493**, Cambridge Univ. Press, pp. 31–54. (The natural single entry point;
  not accessible from this sandbox.) **[V1]**

## 5. SCRIPTS PRODUCED BY THIS ROUTE

* `erdos-273/experiments/E_selfridge360.py` — exhaustive exact search for a covering of
  $\mathbb Z/360\mathbb Z$ by distinct moduli $d\mid360$ with $d+1$ prime; prints and re-verifies a
  witness; and shows the $p\ge5$ restriction (drop the modulus 2) admits none.
* `erdos-273/experiments/E_applicability.py` — exact facts about $E$ used above to decide which
  imported hypotheses hold: $\min E=4$; budget $\sum_{n\in E,n\le X}1/n$ against $\log\log X$;
  parity and squarefreeness; divisibility pairs inside $E$ (Schinzel); first $X$ where the budget
  exceeds 1 and the corresponding lcm; divisors of 360 inside $E$.
