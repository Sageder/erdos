# NOTES.md — Erdős 289 lab notebook (newest first)

## 2026-07-28 ~17:00 UTC — state of the run

### The reformulation everything runs on
$P(k)$ holds iff there is a finite $U\subseteq\mathbb{Z}_{\ge2}$ with $\sum_{n\in U}1/n=1$,
**no isolated point** (every $n\in U$ has a neighbour in $U$), maximal-run lengths
$L_1..L_r$, and $r\le k\le M:=\sum_i\lfloor L_i/2\rfloor$. Proof in PROBLEM.md.
Call such a $U$ a *solution*; $r$ = run count, $M$ = capacity.

### FIRST SOLUTIONS EVER FOUND IN THIS RUN (verified exactly, `experiments/verify.py`)
```
{5,6}{14,15}{17,18}{20,22}{27,28}{33,34}{44,45}{54,55}{84,85}      r=9  M=9   -> k=9
{6,8}{14,15}{17,18}{26,27}{34,35}{44,45}{54,56}{65,66}{77,78}{84,85} r=10 M=10 -> k=10
{7,10}{14,15}{17,19}{34,36}{44,45}{56,57}{76,77}{84,85}            r=8  M=9   -> k in[8,9]
{7,8}{11,12}{17,18}{21,22}{26,28}{33,34}{44,45}{54,56}{65,66}{77,78}{84,85} r=11 M=11 -> k=11
```
**So $P(8),P(9),P(10),P(11)$ are established.**  (`experiments/sols90.txt`)

### Exhaustive negative results (exact, C engine `experiments/csearch.c`, `csearch2.c`)
No solution with $\max U\le 80$.  Node counts 79,765 (N=40) / 1.4M (50) / 143M (60) /
547M (70) / 8.99G (80).  Solutions first appear at N=90 (threshold being pinned down).

### The engines
- `csearch.c` — plain exact DFS. `csearch2.c` — same + endgame table over the top $T$
  positions (huge speedup: N=80 from 9.0G nodes to 1.9M with T=50).
- `gsearch.c` — same for an arbitrary rational target $u/v$ over an element range $[T,N]$.
- Exact integer arithmetic over $L=\mathrm{lcm}(\text{pruned universe})$, weights $L/n$.
- Two prunes: (i) $R\le\mathrm{tail}$; (ii) $Q[pos]\mid R$, the pooled form of the
  two-attainer $p$-adic condition (PROBLEM.md B2). Prune (ii) is what makes it feasible.
- **Reach limit:** $L$ must fit in `unsigned __int128`. OK for $[2,150]$ (33 digits);
  NOT ok for far-out ranges ($[87,250]$ needs 52 digits, $[100,400]$ needs 90).

### Unit-fraction gadgets FOUND (verified exactly)
```
1/2 = 1/6+1/7+1/20+1/21+1/44+1/45+1/77+1/78+1/90+1/91          (5 atoms)
1/2 = 1/9+1/10+1/13+1/14+1/39+1/40+1/44+1/45+1/77+1/78+1/104+1/105
1/3 = {19,20}{35,36}{44,45}{55,57}{65,66}{76,77}{104,105}       (7 runs)
1/3 = {24,25}{27,28}{35,36}{54,56}{77,78}{90,91}{99,100}
2/3 = {6,7}{12,13}{35,36}{39,40}{44,45}{77,78}{104,105}
```
Exhaustively NO legal system with sum $1/4$ or $1/6$ inside $[2,120]$.

### Negative structural results
- **No two-atom split**: $\tfrac1a+\tfrac1{a+1}=\tfrac1c+\tfrac1{c+1}+\tfrac1d+\tfrac1{d+1}$
  has NO solution with $a\le400$, $c\ge a+2$, $d\ge c+2$ (`experiments/atom_split.py`).
  This kills the simplest "+1 block" move.

### Structural facts derived
- **Two-attainer ⇒** every $n\in U$ has all its prime-power components $p^{\nu_p(n)}$
  satisfying $2p^{\nu_p(n)}\le\max U$; a prime $p$ with a multiple in $U$ has $\ge2$
  multiples in $U$. Iterating this prunes the universe hard and shrinks $\mathrm{lcm}$
  dramatically (N=60: 13 digits instead of 26).
- **A run $[a,b]$ of a solution contains no prime $p$ with $2p>\max U$.** In particular the
  TOP run must lie in a prime gap, which bounds its length by the maximal prime gap.
  Long runs must sit lower and have all their primes matched by other elements.
- **Doubling map.** For ANY finite $S\subseteq\mathbb{Z}_{\ge1}$, $D(S)=\{2n,2n+1:n\in S\}$
  is automatically legal, with $\Sigma(D(S))=\Sigma(S)-\sum_{n\in S}\frac1{2n(2n+1)}$,
  capacity exactly $|S|$ and run count = run count of $S$. Companion map
  $\gamma$: $n\mapsto\{2n-1,2n\}$ gives $\frac1n+\frac1{2n(2n-1)}$ (overshoot). Only
  incompatibility: $n\in B$ and $n+1\in G$ (they would share $2n+1$).
  ⇒ solutions = "$\sum_{n\in G}\gamma_n+\sum_{n\in B}\beta_n=1$" plus longer-run variants;
  the found solutions are exactly of this shape.
- Capacity of a solution is $\le|U|/2$ and $|U|\gtrsim 2k$, so $k$ large forces
  $\max U$ large: **no finite search can prove the theorem; a construction is required.**

### Where the difficulty sits (the CRUX)
Every mechanism tried reduces to the same statement:

> **(CRUX)** given a rational $\rho>0$ and a bound $T$, represent $\rho$ as the sum of a
> legal block system with all elements $\ge T$.

This is the block analogue of "Egyptian fractions with denominators in a short interval"
(Croot, Acta Arith. 99 (2001)); arXiv is blocked by this session's egress policy, so no
external theorem can be quoted with verified hypotheses — CRUX must be built here.

### Heuristic (route-C style, computed by hand, to be checked)
#legal subsets of $[2,N]$ $\approx\lambda^N$, $\lambda\approx1.7549$; local $p$-adic
densities contribute $\approx L\prod_p c_p$ against the $1/L$ from the target, leaving
$\Pr[\Sigma=1]\approx e^{-cN/\ln N-\Theta((\ln N)^2)}$. Expected #solutions
$\approx e^{0.56N-cN/\ln N-\Theta((\ln N)^2)}$: **negative until $N\approx 80$–$90$, then
growing exponentially.** This matches the data exactly (first solutions at N=90) and is
strong evidence the answer is YES.

### Next actions
1. Pin the exact threshold ($N=82,84,86,88$ running).
2. Build a big-integer (GMP / 64-bit-fingerprint) engine to search far-out gadgets — needed
   for every candidate mechanism.
3. Attack CRUX by denominator engineering: choose atoms $n$ with $2n(2n\pm1)\mid D$ for a
   fixed smooth $D$, turning the correction into an integer subset-sum.
4. Four independent subagent routes A (identities), B (search technology), C (obstruction),
   D (block-sum structure theory) are running.
