# VERDICT.md — Erdős problem 289, autonomous run of 2026-07-28

## Answer

**The problem is NOT resolved by this run.** Neither branch was proved:

- **YES branch** ($\exists K\ \forall k\ge K:\ P(k)$): **not proved.**
- **NO branch** (infinitely many $k$ with $\neg P(k)$): **not proved**, and now strongly
  disfavoured — every candidate obstruction was refuted, and solutions are provably
  plentiful in the range that can be searched.

Per the run protocol this is stated plainly and nothing below is presented as a resolution.
The rest of this file records what *was* established rigorously and exactly where the
problem now sits.

## The reformulation everything runs on

A finite $U\subseteq\mathbb{Z}_{\ge2}$ is **legal** if it has no isolated point; equivalently
$U$ is a disjoint union of blocks of length $\ge2$. With maximal-run lengths $L_1,\dots,L_r$
put $r(U)=r$ and $M(U)=\sum_i\lfloor L_i/2\rfloor$ (the **capacity**).

> **Proposition.** $P(k)$ holds **iff** there is a legal $U$ with $\sum_{n\in U}1/n=1$ and
> $r(U)\le k\le M(U)$.

Proved in `PROBLEM.md` and `DRAFT.tex` (splitting lemma in both directions). So the problem
is exactly: *do the intervals $[r(U),M(U)]$, over all solutions $U$, cover a cofinite set?*

## Established, audited results

All certificates are re-verified from scratch by `experiments/verify.py` and
`experiments/certificates.py` using `fractions.Fraction` only — no float appears in any
verification path. Audit in `AUDITS.md` walks PROMPT §7 item by item.

1. **Solutions exist** (none were known to this run at the start; the first were found here).
   The minimum possible $\max U$ is **exactly 85**, and there are **exactly four** solutions
   attaining it. The smallest:
   $$1=\tfrac15+\tfrac16+\tfrac1{14}+\tfrac1{15}+\tfrac1{17}+\tfrac1{18}+\tfrac1{20}+\tfrac1{21}+\tfrac1{22}+\tfrac1{27}+\tfrac1{28}+\tfrac1{33}+\tfrac1{34}+\tfrac1{44}+\tfrac1{45}+\tfrac1{54}+\tfrac1{55}+\tfrac1{84}+\tfrac1{85}.$$
   Established by four independent engines (mine, and routes A, B, C), which agree on both
   the emptiness below 85 and the count at 85.

2. **$P(k)$ is TRUE for $k=6,7,\dots,51$**, with explicit exactly-$k$ block certificates.
   26 487 distinct solutions verified. Examples:
   - $k=6$: $(\tfrac14+\tfrac15+\tfrac16)+(\tfrac19+\tfrac1{10})+(\tfrac1{19}+\tfrac1{20})+(\tfrac1{44}+\tfrac1{45})+(\tfrac1{132}+\tfrac1{133})+(\tfrac1{209}+\tfrac1{210})=1$;
   - $k=51$: a 51-block certificate with all elements in $[45,345]$.
   $P(1)$ is FALSE (Kürschák). $P(2),\dots,P(5)$ remain open (no solution with $\max U\le345$
   has fewer than 6 blocks).

3. **Rule (P)** (proved; strictly stronger than the two-attainer rule of PROBLEM.md B2). If
   $\Sigma(U)=q$ and $p$ is prime with $E=\max\{\nu_p(n):n\in U\}$, then
   $\sum_{n\in U,\;p\mid n}p^{E}/n\equiv0 \pmod{p^{E}}$. Iterating it together with legality
   collapses the candidate universe: the fixpoint of $[2,N]$ is **empty for every $N\le76$**
   — a millisecond proof replacing a $9\cdot10^{9}$-node exhaustive search — and the
   surviving universe has a remarkably small lcm (68 bits at $N=300$), which is what makes
   exact 128-bit searching possible far beyond the naive range.

4. **The top run of any solution is prime-free** (proved). If $[c,N]$ is the top maximal run
   then $c>N/2$ and $[c,N]$ contains no prime; hence its length is bounded by the largest
   prime gap below $N$. Capacity therefore cannot be manufactured by one long final run.

5. **No block sum is a unit fraction**: $H(a,b)\ne1/N$ for all $b>a\ge1$, $N\ge1$ (proved via
   the 2-adic level, a rough-part bound and Kummer, with the finitely many exceptional pairs
   checked exactly). Independently corroborated: over $5\,053\,495$ block sums with
   $a\le4000$ the smallest numerator is $5$, attained only by $H(2,3)=5/6$.

6. **A block *system* can sum to a unit fraction** — e.g.
   $\tfrac12=\tfrac16+\tfrac17+\tfrac1{20}+\tfrac1{21}+\tfrac1{44}+\tfrac1{45}+\tfrac1{77}+\tfrac1{78}+\tfrac1{90}+\tfrac1{91}$
   (max element 91), and similarly $\tfrac13$ and $\tfrac23$. This **refutes** the natural
   conjecture (raised inside this run) that no unit fraction is a legal block sum, whose
   exhaustive support only reached max element 85.

7. **The NO branch is dead.** Candidate obstructions O1–O9 ($p$-adic, parity, smoothness,
   legality cascade, minimum-isolated-points, "many rationals but never 1") are each
   *proved as lemmas* and each *refuted as obstructions*. The only survivor constrains
   $\max U$ (it is never prime, nor one more than a prime), not existence. An honest
   local–global count with **exactly computed** local densities predicts
   $\#\{\text{solutions}:\max U\le N\}\approx e^{cN}\to\infty$ (fitted $e^{0.098N}$ on
   $[80,200]$), matching the observed counts.

## Where the problem now sits

Solutions exist with all elements $\ge45$ (max 345, $r=40$, $M=51$). A legal system with
elements $\asymp T$ and reciprocal sum $\tfrac12$ (or $1$) necessarily has $\asymp T$
elements, so its capacity grows linearly in $T$. Hence:

> **(CRUX)** For arbitrarily large $T$, is there a legal block system with all elements
> $\ge T$ whose reciprocal sum is $\tfrac12$ (equivalently, a solution with $\min U\ge T$)?

**If CRUX holds, the YES branch follows**: pair a fixed $\tfrac12$-gadget with a far-out one,
or take the far-out solution directly; capacities then tend to infinity while run counts stay
a bounded fraction of them, so the intervals $[r,M]$ chain and cover a cofinite set of $k$
(`DRAFT.tex`, Prop. 5.1). Every mechanism examined in this run reduces to CRUX.

**Why it could not be closed here.** CRUX is the block-structured analogue of representing a
rational by distinct unit fractions with denominators in a short interval (Croot, *Acta
Arith.* 99 (2001); Bloom 2021). Those results could not be used: this session's egress policy
returns 403 for arXiv, EuDML and the mirrors, so no external theorem could be quoted with its
hypotheses verified — and reproving one, additionally constrained to block structure, is a
research-paper-sized analytic task. The block constraint forces coprime consecutive pairs,
which fights the multiplicative structure such proofs rely on.

**Shortcuts that are ruled out** (each a real negative result of this run):
- *Equal-sum blocks*: $H(a,b)=H(c,d)$ has no solution with $(a,b)\ne(c,d)$ for all blocks
  with elements $\le3000$ (2.84M blocks, two independent 62-bit fingerprints); route D turns
  this into a complete decision procedure with **no** element bound. So a block cannot be
  swapped for a longer block of equal sum — which would have raised capacity at fixed run
  count.
- *Atom splitting*: $\tfrac1a+\tfrac1{a+1}=\tfrac1c+\tfrac1{c+1}+\tfrac1d+\tfrac1{d+1}$ has
  no solution with $a\le400$, $c\ge a+2$, $d\ge c+2$.
- *Capacity doubling by recolouring* (BALANCE): admissible colourings of the atom-doubling
  map are exactly **prefix** colourings of each run, giving only $\prod(L_i+1)\approx3^{r}$
  of them against a target of lcm-sized denominator; unsolvable for all 990 solutions tested,
  and still unsolvable on the largest ones under branch-and-bound.
- *Parametric families die for an arithmetic reason.* For $c\ge3$ the maps
  $n\mapsto\{cn,cn+1\}$, $n\mapsto\{cn-1,cn\}$ give disjoint atoms for **every** colouring
  ($2^{|U|}$ of them) and realise exactly $k=|U|$ blocks; but the coarse term has
  denominators divisible by $cn$ while the corrections $\tfrac{2}{c^2n^2-1}$ have
  denominators $(cn-1)(cn+1)$, coprime to $cn$ — the corrections can never repair the coarse
  term. Blow-up families $n\mapsto[qn-d+s_n,qn+d+s_n]$ fail the same way. Exactness always
  reduces to hitting a rational of lcm-sized denominator with $2^{O(k)}$ options; only the
  full entropy of unrestricted legal sets, together with the $p$-adic conditions, suffices —
  which is exactly why a short explicit construction does not exist.
- *$B(T)$ is not shift-invariant*: $\tfrac56\in B(2)$ but $\tfrac56\notin B(5)$ even allowing
  elements $\le66$; $\tfrac7{12}\in B(3)\setminus B(4)$.

## Independent-verification plan

- **Reproduce the certificates:** `python3 experiments/verify.py experiments/ALLSOLS.txt`
  and `python3 experiments/certificates.py experiments/ALLSOLS.txt` (exact rationals only;
  they import nothing from the search code).
- **Reproduce the negative range:** `experiments/csearch.c` (`./csearch 80`) exhausts
  $N\le80$ in $8.99\cdot10^{9}$ nodes; `csearch2.c` with an endgame table does $N\le86$
  quickly; `attempts/route-C/prune.py` shows the Rule-(P)+legality fixpoint of $[2,76]$ is
  empty. Three code paths, same answer.
- **Reproduce the structure theorems:** `experiments/collide.c` (block-sum injectivity),
  `experiments/two_to_block.c` (no unit fraction is a block sum),
  `experiments/atom_split.py`, `experiments/balance.py`, `experiments/balance2.py`,
  `experiments/cmap.py`, `experiments/blowup.py`.
- **Lean sketch** (statements only; none of these is the headline). Against
  `google-deepmind/formal-conjectures`, `ErdosProblems/289.lean`:
  ```lean
  -- the reformulation actually used
  theorem legal_iff (k : ℕ) :
      (∃ I : Fin k → ℕ × ℕ, (∀ i, (I i).1 < (I i).2) ∧
         (∀ i j, i ≠ j → (I i).2 < (I j).1 ∨ (I j).2 < (I i).1) ∧
         ∑ i, ∑ n ∈ Finset.Icc (I i).1 (I i).2, (n:ℚ)⁻¹ = 1)
    ↔ ∃ U : Finset ℕ, (∀ n ∈ U, 2 ≤ n) ∧ (∀ n ∈ U, n-1 ∈ U ∨ n+1 ∈ U) ∧
         (∑ n ∈ U, (n:ℚ)⁻¹ = 1) ∧ runCount U ≤ k ∧ k ≤ capacity U
  -- a base certificate
  theorem P_nine : ∑ n ∈ ({5,6,14,15,17,18,20,21,22,27,28,33,34,44,45,54,55,84,85} :
      Finset ℕ), (n:ℚ)⁻¹ = 1
  -- Rule (P)
  theorem ruleP (U : Finset ℕ) (h : ∑ n ∈ U, (n:ℚ)⁻¹ = 1) (p : ℕ) (hp : p.Prime) :
      0 ≤ padicValRat p (∑ n ∈ U.filter (p ∣ ·), (n:ℚ)⁻¹)
  ```
  The headline statement to target remains `erdos_289`: the $\forall^{f}$-atTop statement
  over `Fin k`-indexed disjoint intervals with the exact rational sum — **unproved here**.
- **Before any external communication:** nothing in this run should be posted as a solution
  or partial solution of 289. The externally interesting items are the certificates
  (item 2), the exact minimum 85 (item 1), and the structure theorems (items 3–6); they are
  statements *about* the problem, not a resolution of it.

## Honest bottom line

The run turned Erdős 289 from "no example known here" into "examples are abundant and the
statement is verified for every $k$ from 6 to 51", proved the exact threshold
$\min\max U=85$, proved several structure theorems (Rule (P), prime-free top run, no block
sum is a unit fraction), and killed the negative branch. It reduced the cofinite statement to
one clean analytic question (CRUX) and ruled out, with proofs or exhaustive searches, every
short constructive route to it. It did **not** resolve the problem in either direction.
