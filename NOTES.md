# NOTES.md — Erdős 289 lab notebook (newest first)

## 2026-07-28 ~18:40 UTC — consolidated state

### The reformulation everything runs on
$P(k)$ holds iff there is a finite $U\subseteq\mathbb{Z}_{\ge2}$ with $\sum_{n\in U}1/n=1$,
**no isolated point**, maximal-run lengths $L_1..L_r$, and $r\le k\le M:=\sum_i\lfloor L_i/2\rfloor$
(splitting lemma; proof in PROBLEM.md). Call such a $U$ a *solution*, $r$ its run count,
$M$ its capacity.

### ESTABLISHED (all exact, independently re-verified)

1. **Solutions exist.** The minimum possible $\max U$ is exactly **85**, with exactly four
   solutions. Smallest:
   $1=\tfrac15+\tfrac16+\tfrac1{14}+\tfrac1{15}+\tfrac1{17}+\tfrac1{18}+\tfrac1{20}+\tfrac1{21}+\tfrac1{22}+\tfrac1{27}+\tfrac1{28}+\tfrac1{33}+\tfrac1{34}+\tfrac1{44}+\tfrac1{45}+\tfrac1{54}+\tfrac1{55}+\tfrac1{84}+\tfrac1{85}$.
2. **No solution has $\max U\le84$** — three independent engines agree (mine with the pooled
   $p$-adic prune, route B's Rule (P) DP, route C's RULE A+B fixpoint, which is EMPTY for
   all $N\le76$).
3. **$P(k)$ is TRUE for $k=6,\dots,65$ (contiguous) and for $k=70,71,91,127,128$**, with explicit exactly-$k$ block certificates
   emitted and re-verified by `experiments/certificates.py` (count $=k$, all lengths $\ge2$,
   pairwise disjoint, elements $\ge2$, sum $=1$ in $\mathbb{Q}$).
4. **$P(1)$ is FALSE** (Kürschák). $P(2)\dots P(5)$ are OPEN. What *is* proved is that the
   top run $[c,N]$ of any solution satisfies $c>N/2$ and is prime-free (a prime $p$ in it
   needs a second multiple $\ge 2p$), so a 2-run solution needs both runs nearly prime-free;
   that is strong evidence against $P(2)$ but NOT a proof. Empirically the minimum run count
   over all 27 069 solutions is exactly 6, attained once.
5. **$H(a,b)$ is never a unit fraction** — PROVED (route D), via the 2-adic level plus a
   rough-part bound and Kummer, with one exceptional pair $(k,b)=(5,16)$ checked by hand.
6. **A legal block system CAN sum to a unit fraction:**
   $\tfrac12=\tfrac16+\tfrac17+\tfrac1{20}+\tfrac1{21}+\tfrac1{44}+\tfrac1{45}+\tfrac1{77}+\tfrac1{78}+\tfrac1{90}+\tfrac1{91}$
   (max element 91) — this **refutes** route D's Conjecture Q2 ("no unit fraction lies in any
   $B(T)$"), whose exhaustive support only reached max element 85. Also
   $\tfrac13$ and $\tfrac23$ are legal block sums.
7. **The NO branch is dead.** Route C refuted every candidate obstruction O1–O9; the only
   surviving one (O10) says $\max U$ and $\max U-1$ are never prime — it constrains the top
   element, not existence. An honest local–global count with EXACTLY computed local
   densities predicts $\#\{\text{solutions with }\max\le N\}\approx e^{cN}\to\infty$
   (fitted $e^{0.098N}$ on $[80,200]$), matching the data.

### NEGATIVE structural results (each a bounded search unless marked PROVED)

- **No atom split** $\tfrac1a+\tfrac1{a+1}=\tfrac1c+\tfrac1{c+1}+\tfrac1d+\tfrac1{d+1}$
  ($a\le400$).
- **Block sums are injective**: no two distinct blocks share a value (elements $\le3000$,
  2.84M blocks, two 62-bit fingerprints); route D makes this a *complete* decision
  procedure with NO element bound and confirms it for 5187 blocks. Kills "replace a block
  by a longer block of equal sum", which would have raised capacity at fixed run count.
- **BALANCE (capacity doubling by atom recolouring) is unsolvable** for all 990 known
  solutions (`experiments/balance.py`, meet-in-the-middle, exact). Diagnosis: admissible
  colourings are PREFIX colourings of each run, so only $\prod(L_i+1)\approx3^r$ of them,
  against a target of lcm-sized denominator.
- **The $c$-map family fails** ($c\ge3$: atoms $\{cn,cn+1\}$ / $\{cn-1,cn\}$ have NO
  adjacency conflict, so all $2^{|U|}$ colourings are admissible, and the image realises
  exactly $k=|U|$ blocks). No hit for $6\le k\le22$, $c\in\{3,4,5,6\}$
  (`experiments/cmap.py`). **Diagnosis — and this is the sharp one:** the coarse term
  $B_c(U)=\sum(\tfrac1{cn}+\tfrac1{cn+1})$ has denominators divisible by $cn$, while the
  corrections $\tfrac{2}{c^2n^2-1}$ have denominators $(cn-1)(cn+1)$, coprime to $cn$. The
  corrections can therefore never repair the coarse term. Any parametric family with a
  "main term + small corrections" shape dies the same way.
- **$B(T)$ is not shift-invariant** (route D): $5/6\in B(2)$ but $5/6\notin B(5)$ even
  allowing elements $\le66$ (491.9M nodes); $7/12\in B(3)\setminus B(4)$.

### The CRUX (the whole remaining gap) — now sharpened to (GAD)

> **(CRUX)** For arbitrarily large $T$, is $\tfrac12$ (or some fixed rational) the sum of a
> legal block system with all elements $\ge T$?

**Answered affirmatively at three scales** (verified three ways): $\tfrac12$ on $[104,900]$,
$\tfrac13$ on $[203,5720]$, $\tfrac16$ on $[527,5985]$. Route F then proved the reduction
$R^\ast$ is a *semigroup*, so everything reduces to

> **(GAD)** there are $K,D$ with: for every large $x$ some legal $G\subseteq[x,Kx]$ has
> $\Sigma(G)=1/D$.

and proved two no-go theorems (Cor. F4: any $D$-switch with $\min\ge x$ has
$|A\triangle B|\ge x/D$, so no local/parametric family exists at all; Thm F7: switches
supply covering but can never replace the gadget condition). See VERDICT.md items 8–10.

If YES: $1=\tfrac12+\tfrac12$ with one fixed gadget in $[6,91]$ and one far out gives
solutions whose capacity $\to\infty$ (a $\tfrac12$-system with elements $\asymp T$ needs
$\asymp T$ elements, so capacity $\asymp T$) while the run count stays a fixed fraction of
it — the intervals $[r,M]$ then chain and cover a cofinite set of $k$. **That is a complete
YES proof.** Every mechanism examined in this run reduces to CRUX.

Status: OPEN. It is the block analogue of Egyptian-fraction representability with
denominators in a short interval (Croot, *Acta Arith.* 99 (2001); Bloom, 2021). **Those
papers cannot be used here**: this session's egress policy returns 403 for arXiv, EuDML and
the mirrors, so no external statement can be quoted with hypotheses verified. Reproving a
Croot-type theorem, additionally constrained to block structure, is a research-paper-sized
analytic task; the block constraint forces coprime consecutive pairs, which fights the
multiplicative structure those proofs rely on.

### Why no short construction exists (diagnosis, repeated failures)
Exactness always reduces to hitting a rational of lcm-sized denominator by a subset sum
with $2^{O(k)}$ options. Naive entropy loses; real solutions survive only because their
$p$-adic conditions (Rule (P) / RULE A) hold at every prime simultaneously — i.e. the local
densities give back a factor $\approx\prod_p p$. A parametric family cannot arrange that,
as the $c$-map denominator argument shows concretely.

### Engines
`experiments/csearch.c` (plain), `csearch2.c` (+ endgame table over the top $T$ positions;
N=80 drops from 9.0G nodes to 1.9M), `csearch3.c` (reads an external pruned universe),
`csearch4.c` (+ minimum $|U|$, to target large capacity), `gsearch.c`/`gsearch3.c`
(arbitrary rational target on $[T,N]$), `collide.c`, `two_to_block.c`.
Reach: exact `unsigned __int128` needs $L=\mathrm{lcm}(\text{pruned universe})<2^{127}$;
with the RULE A+B fixpoint that holds up to $N=600$ (126 bits) — 68 bits at $N=300$.

### Next actions
1. Await routes A, B, E (E is searching $\tfrac12$ on $[100,350]$ and $[100,400]$ — the
   direct CRUX test).
2. Keep pushing exhaustive/size-targeted searches for larger $k$ (currently 65 contiguous).
3. If CRUX stays open, VERDICT.md must say the problem is NOT resolved and record exactly
   what is proved.
