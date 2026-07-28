# VERDICT.md — Erdős problem 289, autonomous run of 2026-07-28

## Answer

**The problem is NOT resolved by this run.** Neither branch is proved:

- **YES branch** ($\exists K\ \forall k\ge K:\ P(k)$): **not proved.**
- **NO branch** (infinitely many $k$ with $\neg P(k)$): **not proved**, and now strongly
  disfavoured — every candidate obstruction was proved as a lemma and then refuted, and
  solutions are abundant in every range that can be searched.

Nothing below is presented as a resolution. The run reduced the problem to one clean
statement, **(GAD)** below, and proved several theorems along the way, including an
unconditional no-go that kills every local/parametric construction at once.

## The reformulation everything runs on

A finite $U\subseteq\mathbb{Z}_{\ge2}$ is **legal** if it has no isolated point; equivalently
$U$ is a disjoint union of blocks of length $\ge2$. With maximal-run lengths $L_1,\dots,L_r$
put $r(U)=r$ and $M(U)=\sum_i\lfloor L_i/2\rfloor$ (the **capacity**), and
$\Sigma(U)=\sum_{n\in U}1/n$.

> **Proposition (proved).** $P(k)$ holds **iff** there is a legal $U$ with $\Sigma(U)=1$ and
> $r(U)\le k\le M(U)$.

So the problem is exactly: *do the intervals $[r(U),M(U)]$ over all solutions cover a
cofinite set?*

## Established, audited results

Every certificate is re-verified from scratch — `fractions.Fraction`, and for the extreme
ones also `sympy.Rational` and pure integer arithmetic $\sum L/n=L$ with $L=\mathrm{lcm}(U)$.
No float occurs in any verification path. `AUDITS.md` walks PROMPT §7 item by item.

1. **Solutions exist** (none were in hand when this run began). The minimum possible
   $\max U$ is **exactly 85**, with **exactly four** solutions attaining it; the smallest is
   $$1=\tfrac15+\tfrac16+\tfrac1{14}+\tfrac1{15}+\tfrac1{17}+\tfrac1{18}+\tfrac1{20}+\tfrac1{21}+\tfrac1{22}+\tfrac1{27}+\tfrac1{28}+\tfrac1{33}+\tfrac1{34}+\tfrac1{44}+\tfrac1{45}+\tfrac1{54}+\tfrac1{55}+\tfrac1{84}+\tfrac1{85}.$$
   Confirmed by four independent engines and by a pruning-free meet-in-the-middle count.

2. **$P(k)$ is TRUE for $k=6,\dots,65$ (contiguous) and for $k=70,71,91,127,128$**, with
   explicit exactly-$k$ block certificates in `experiments/CERTIFICATES.txt`. 39 269 distinct
   solutions verified. $P(1)$ is FALSE (Kürschák); $P(2)\dots P(5)$ are open, and there is no
   witness for them with $\max U\le400$ (proved: no solution has $\le5$ maximal runs and
   $\max U\le400$, $1.58\cdot10^{10}$ nodes).

3. **Exhaustive negatives.** No solution with $\max U\le84$. The complete list for
   $\max U\le170$ is exactly 25 650 certificates ($9.4\cdot10^{10}$ nodes).

4. **Rule (P)** (proved; strictly stronger than the two-attainer rule): for every prime $p$,
   $\nu_p\bigl(\sum_{n\in U,\,p\mid n}1/n\bigr)\ge0$, i.e. a subset-sum-to-zero condition
   mod $p^{E}$ over the multiples of $p$, decidable by reachability DP. Iterated with
   legality it makes "no solution with $\max U\le76$" a **millisecond** computation
   (previously 547M nodes at $N=70$), and it keeps $\mathrm{lcm}$(universe) small enough for
   exact machine arithmetic far beyond the naive range.

5. **The top run of any solution is prime-free** and lies in $(N/2,N]$, $N=\max U$; its
   length is at most the largest prime gap below $N$. Capacity cannot come from one long
   final run.

6. **No block sum is a unit fraction**: $H(a,b)\ne1/N$ (proved, via the 2-adic level, a
   rough-part bound and Kummer). But a block *system* can be: verified certificates give
   $\tfrac12$, $\tfrac13$, $\tfrac23$, and — far out — $\tfrac12$ with all elements $\ge100$,
   $\tfrac13$ with all elements $\ge200$, $\tfrac16$ with all elements $\ge500$.

7. **The NO branch is dead.** Candidate obstructions O1–O9 are each proved as lemmas and each
   refuted as obstructions; the survivor only constrains $\max U$. A local–global count with
   exactly computed local densities predicts $\#\{\text{solutions}:\max U\le N\}\approx e^{cN}$.

8. **Unconditional no-go for local constructions** (Lemma F3 / Cor. F4). Define a
   *$D$-switch* as a pair $A,B$ of legal systems on a common window with
   $\Sigma(B)-\Sigma(A)\in\tfrac1D\mathbb{Z}$. Then any $D$-switch with $\min\ge x$ satisfies
   $|A\,\triangle\,B|\ge x/D$. Consequently **no family of switches with $D$ fixed and
   $|A\triangle B|$ bounded exists.** This turns the run's earlier counting heuristic into a
   theorem and kills, simultaneously, every identity-based move, the $c$-maps, the doubling
   maps, atom splitting and blow-up families.

9. **Anchor necessity** (Theorem F7). In any switch scheme $W=\bigsqcup X_i$ with
   $X_i\in\{A_i,B_i\}$ and $\Sigma(B_i)-\Sigma(A_i)\in\tfrac1D\mathbb Z$, the requirement
   $\Sigma(W)=\rho$ forces $\sum_i\Sigma(A_i)\in\rho+\tfrac1D\mathbb Z$ — the all-$A$ system
   is itself a gadget. **Switches supply covering but can never replace the gadget condition.**

10. **Reductions** (R1–R3, proved). If for all large $x$ some legal $G\subseteq[x,Kx]$ has
    $\Sigma(G)=1/D$, then the cofinite statement follows (take $D/2$ separated copies).
    Moreover the set $R^\ast$ of rationals realisable arbitrarily far out is a **semigroup**,
    so $1/(2n)\in R^\ast$ for a *single* $n$ already suffices. A covering lemma is proved in
    the exact form needed: if $c_1\le\dots\le c_s$ are positive integers with $c_1=1$ and
    $c_{j+1}\le1+\sum_{i\le j}c_i$, the subset sums are exactly $[0,\sum c_i]\cap\mathbb{Z}$.

## Where the problem now sits

By item 10 everything reduces to a single statement:

> **(GAD)** There are constants $K$ and $D$ such that for every large $x$ some legal
> $G\subseteq[x,Kx]$ has $\Sigma(G)=1/D$.

**Evidence that (GAD) is true.** Gadgets have been *found* at three separated scales, each
verified three ways: $\tfrac12$ with elements in $[104,900]$; $\tfrac13$ with elements in
$[203,5720]$; $\tfrac16$ with elements in $[527,5985]$. Exact entropy minus exact constraint
bits, $\Lambda-\lambda$, grows without bound with window width ($+18.6$ on $[100,400]$,
$+582$ on $[1000,4000]$), at every scale tested.

**Why it is not proved.** Converting that count into existence needs equidistribution of
$\Sigma(U)$ modulo $\tfrac1D\mathbb{Z}$ over legal $U$ — a block-constrained Croot-type
theorem. Theorem F7 says switches cannot get underneath it, and Corollary F4 says no local
family can. The obstruction is structural: legality couples neighbouring integers
($n\in U\Rightarrow n\pm1\in U$) while consecutive integers are coprime, which destroys
exactly the independence a sieve or second-moment argument needs. The literature that
handles the unconstrained analogue (Croot, *Acta Arith.* 99 (2001); Bloom 2021) could not be
used: this session's egress policy returns 403 for arXiv, EuDML and the mirrors, so no
external theorem could be quoted with its hypotheses verified.

**Also ruled out along the way** (each an exhaustive search with a stated range, or a proof):
$H(a,b)=H(c,d)$ has no solution with $(a,b)\ne(c,d)$; the two-atom split has none with
$a\le400$; the balanced-doubling equation is unsolvable for every one of the 990+ solutions
tested; no legal $U\subseteq[100,400]$ has $\Sigma=\tfrac12$ ($1.57\cdot10^{7}$ nodes), which
is why the far-out $\tfrac12$ certificate needs the wider window $[104,900]$.

## Independent-verification plan

- **Certificates:** `python3 experiments/verify.py experiments/ALLSOLS.txt` and
  `python3 experiments/certificates.py experiments/ALLSOLS.txt`; both use exact rationals and
  import nothing from the search code.
- **Negative range:** `experiments/csearch.c` exhausts $N\le80$ in $8.99\cdot10^{9}$ nodes;
  `attempts/route-C/prune.py` shows the Rule (P)+legality fixpoint of $[2,76]$ is empty;
  Route B's independent meet-in-the-middle reproduces the counts at $N=85,\dots,140$.
- **Structure theorems:** `experiments/collide.c`, `two_to_block.c`, `atom_split.py`,
  `balance.py`, `balance2.py`, `cmap.py`, `blowup.py`; `attempts/route-F/NOTES.md` §1–§4 for
  Lemma F3, Cor. F4, Thm F7 and the covering lemma.
- **Lean sketch** (statements only; the headline is unproved). Against
  `google-deepmind/formal-conjectures`, `ErdosProblems/289.lean`:
  ```lean
  theorem legal_iff (k : ℕ) :
      (∃ I : Fin k → ℕ × ℕ, (∀ i, (I i).1 < (I i).2) ∧
         (∀ i j, i ≠ j → (I i).2 < (I j).1 ∨ (I j).2 < (I i).1) ∧
         ∑ i, ∑ n ∈ Finset.Icc (I i).1 (I i).2, (n:ℚ)⁻¹ = 1)
    ↔ ∃ U : Finset ℕ, (∀ n ∈ U, 2 ≤ n) ∧ (∀ n ∈ U, n-1 ∈ U ∨ n+1 ∈ U) ∧
         (∑ n ∈ U, (n:ℚ)⁻¹ = 1) ∧ runCount U ≤ k ∧ k ≤ capacity U
  theorem P_nine : ∑ n ∈ ({5,6,14,15,17,18,20,21,22,27,28,33,34,44,45,54,55,84,85} :
      Finset ℕ), (n:ℚ)⁻¹ = 1
  theorem ruleP (U : Finset ℕ) (h : ∑ n ∈ U, (n:ℚ)⁻¹ = 1) (p : ℕ) (hp : p.Prime) :
      0 ≤ padicValRat p (∑ n ∈ U.filter (p ∣ ·), (n:ℚ)⁻¹)
  ```
- **Before any external communication:** nothing here should be posted as a solution or a
  partial solution of 289. The externally interesting items are the certificates, the exact
  minimum 85, and the structure theorems (items 4–6, 8–10) — statements *about* the problem,
  not a resolution of it.

## Honest bottom line

The run turned Erdős 289 from "no example known here" into "examples are abundant, the
statement is verified for every $k$ from 6 to 65 and for several larger $k$, the exact
threshold $\min\max U=85$ is known, and the negative branch is dead". It proved Rule (P), the
prime-free top run, the non-existence of unit-fraction block sums, an unconditional no-go for
every local/parametric construction, and a chain of reductions ending at the single statement
(GAD). It did **not** resolve the problem in either direction.
