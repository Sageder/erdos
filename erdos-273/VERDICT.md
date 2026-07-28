# VERDICT — Erdős Problem 273

**Statement.** Is there a covering system of ℤ, with finitely many classes and pairwise distinct
moduli all $> 1$, every modulus of the form $p-1$ for a prime $p \ge 5$?
(Equivalently: all moduli in $E = \{n \ge 4 : n+1 \text{ prime}\}$.)

## ANSWER: NOT RESOLVED BY THIS RUN.

Neither branch was proved. I did not find a covering system, and I did not prove that none
exists. Everything below is a partial result. **Nothing here should be represented as a solution
to Erdős 273, and no result below is strong enough to be one.**

This file records exactly what *was* proved, what was only measured, and where the remaining gap
sits. The lab notebook is `NOTES.md` (newest first), the route registry `ROUTES.md`, the audits
`AUDITS.md`, the proofs `DRAFT.tex`, and all code `experiments/`.

---

## 1. What was rigorously proved (each independently audited)

Every item here was proved on paper **and** re-verified by a from-scratch script; the audits are
in `AUDITS.md`.

**(T1) Parity split.** *An $E$-covering exists **iff** there are two **disjoint** finite sets
$M_0, M_1 \subseteq H := \{m \ge 2 : 2m+1 \text{ prime}\}$, each carrying a covering system of ℤ
with distinct moduli; and $\mathrm{lcm}_E = 2\,\mathrm{lcm}_H$.*
Derived **six** independent times in this run (main line, routes A, C, D, F, G) and verified in
both directions computationally, including on negative residues. Proof: `attempts/route-M-main/PARITY_SPLIT.md`; verifier
`experiments/M_parity_split.py`.
*This is the correct frame for the problem.* The solved $p\ge3$ variant (Selfridge) is precisely
"$H$ supports **one** covering system"; problem 273 additionally demands a **second, disjoint**
one built from the moduli the first did not use.

**(T2) There is no universal reciprocal-sum constant to exploit.**
$\inf \sum 1/n_i = 1$ over all covering systems with distinct moduli, not attained: the doubling
map $D(C) = \{0 \bmod 2\} \cup \{(2a_i+1) \bmod 2n_i\}$ has cost $\tfrac12 + \tfrac12\mathrm{cost}(C)$,
giving explicit systems of cost $1 + \tfrac13 2^{-k}$ (verified by full mod-lcm sweeps for
$k \le 8$; route F pushed the same construction to $k = 14$, cost $49153/49152$).
Consequently the natural heuristic "a covering needs cost $\approx 4/3$" is **false**, and no
argument that derives a contradiction from an absolute lower bound $\sum 1/n_i \ge c > 1$ can work.
**Scope correction (adversarial audit):** this concerns *unrestricted* systems and does **not**
show that $E$- or $H$-coverings can have cost near 1. No lower bound on the cost of an $E$- or
$H$-covering is proved anywhere in this run; the cheapest $H$-covering found costs $65/48$ with no
downward trend. The earlier phrasing "no reciprocal-sum argument can decide the problem in either
direction" was a non-sequitur and is withdrawn.
Filaseta–Kalogirou (arXiv:2407.15280) reportedly prove that a least modulus $> 4$ forces the excess
to be bounded away from 0. **The primary source could not be opened** (egress blocked), so this is
unverified and not load-bearing. If true it gives a *dichotomy*, not a blanket conclusion: an
$E$-covering **using** the modulus 4 lies in the no-bound regime, whereas one **avoiding** 4 has
least modulus $\ge 6$ and would inherit a positive excess bound.

**(T3) Lower bounds on the lcm.** Every modulus divides $L = \mathrm{lcm}$, so
$\beta(L) := \sum_{n \mid L,\, n \in E} 1/n > 1$ is necessary. An exhaustive sieve over **all** $L$
(not merely smooth ones) gives: the least such $L$ is $\mathbf{55440 = 2^4\cdot3^2\cdot5\cdot7\cdot11}$
($\beta = 6429/6160$), and exactly **90** values $L \le 10^6$ qualify, all divisible by 60.
Moreover $L = 55440$ itself is **eliminated**, twice independently (below), as are 110880 and
several further candidates. Combining the budget condition with the fiber test and checking the
complete candidate list, the adversarial auditor independently confirmed that the only $L_H \le
95000$ with $H$-pool budget $\ge 2$ are $27720, 32760, 50400, 55440, 65520, 75600, 83160, 90720$
and that the first seven are all killed — giving the unconditional bound
$$\boxed{\ \mathrm{lcm} \ \ge\ 2\cdot 90720 \ =\ 181440\ }$$
for any covering system with all moduli in $E$. (Route D obtained this first; it was reproduced by
two further independent solvers.)

**(T4) Forced-overlap lemma and the coprimality test** (route A, audited; now stated in full in
`DRAFT.tex`, together with the strengthened Theorem A3+ that was previously cited but unstated).
For a covering with modulus set $M$ and any *pairwise coprime* $T \subseteq M$,
$$\sum_{m\in M}\tfrac1m - 1 \;\ge\; f(T) := \sum_{m\in T}\tfrac1m - 1 + \prod_{m\in T}\bigl(1-\tfrac1m\bigr),$$
because $S \mapsto \sum_{m\in S}1/m - \mathrm{dens}(\bigcup S)$ is monotone and coprime classes are
independent by CRT **whatever the residues**. Consequence (Theorem A3): if $60 \mid L$ and
$1 < \beta(L) \le 31/30$ then no $E$-covering has lcm dividing $L$ — this kills **63 of the 90**
candidates $\le 10^6$ with no search at all.

**(T5) Exact $q$-adic fiber test** (route D, audited by independent reimplementation).
For a prime $q$ and a pool $S$, $\Phi_q(S) := \max_{\text{assignments}} \min_{r \in \mathbb Z_q}
\sum_{m:\, b_m \equiv r\ (q^{\nu_q(m)})} q^{\nu_q(m)}/m$ must be $\ge 2$ (the two disjoint halves
contribute additively). The Haar average of the fiber budget is exactly $\sum 1/n_i$, so
"$\sum 1/n_i > 1$" is only the *average* condition while covering demands the *minimum*.
Exact branch-and-bound kills $L_H = 27720, 32760, 50400, 55440, 65520, 75600$ and more.

**(T6) Rigidity of the cheap mechanism** (route F).
The only exact partition of $\mathbb Z$ minus one residue class by classes with pairwise distinct
moduli $>1$ is the dyadic staircase $2,4,\dots,2^m$.
**Correction (adversarial audit):** the earlier claim "$E \cap \{2^k\} = \{4,16,256,65536\}$" asserted
that the known Fermat primes are the only ones — an open problem — and is withdrawn; those are
$\subseteq$, the known members. The corollary survives unconditionally by a different route:
$2^k+1$ prime forces $k$ to be a power of 2, and $k, k+1$ are both powers of 2 only for $k=1$, so
$E$ contains **no two consecutive powers of two** and $2 \notin E$; also $4 \notin H$ since
$9 = 3^2$. Hence no non-empty dyadic staircase lies in $E$, and only the trivial $\{2\}$ lies in $H$.
So the *only known* mechanism for driving the reciprocal cost to 1 is unavailable here — which is
not a lower bound on that cost, and other mechanisms are not excluded.

**(T7) A barrier on the negative branch** (route D, with an explicit certificate).
For every **fixed** finite set $Q$ of primes, moduli coprime to $\prod Q$ contribute to every
$Q$-cell for every residue assignment, and $\sum_{m\in H,\ \gcd(m,\prod Q)=1} 1/m = \infty$.
Explicitly, $H \cap [2, 82899]$ already satisfies every single-prime fiber condition at threshold
2, at every level, for every assignment. **Hence no elimination test built from monotone additive
fiber budgets over the cells of a *fixed* finite set of primes can eliminate all lattices.** (The
eliminations used in this run are not refuted by this: they use a prime $q$ depending on $L$.)
A negative resolution therefore appears to need a functional coupling all primes with a bound
uniform in their number.
**Corrections (adversarial audit):** (a) the available technology of that kind — Hough's and
Balister–Bollobás–Morris–**Sahasrabudhe**–Tiba's distortion method — proves an *upper* bound
($\le 10^{16}$, resp. $\le 616000$) on the least modulus of a distinct-moduli covering system, so it
yields a contradiction only for systems all of whose moduli exceed that bound; since $\min E = 4$
it does not apply. The earlier wording "provably requires least modulus $\ge 616000$" mis-described
the theorem and is withdrawn. (b) $H \cap [2,82899]$ is an *interval*, not the divisor pool of any
lattice; the transfer to a lattice uses monotonicity of $\Phi_q$ in the pool (take
$L_H = \mathrm{lcm}$ of that set). (c) "obstruction local at a fixed finite set of primes" is not a
formally defined class; what is actually proved covers monotone additive fiber-budget functionals.

**(T8) Verified partial certificates.** Several explicit sets of $E$-moduli covering *exactly the
even integers* were found and independently re-verified, the cheapest being
$$\{4,6,12,16,18,36,72,96,192,576\}\quad(\text{cost } 65/96,\ \mathrm{lcm}=576),$$
the image under (T1) of the cheapest $H$-covering found anywhere (cost $65/48$, $\mathrm{lcm}=288$).
So covering one parity class with $E$-moduli is easy and explicit. **This is not "half the
problem"** (an earlier phrasing, withdrawn after audit): by Corollary/pivot below, the easy half
carries essentially none of the difficulty, which lies entirely in doing *both* halves with
*disjoint* modulus sets.

## 2. The precise open gap

By (T1), and because $2 \in H$ can lie in at most one of $M_0, M_1$:

> **PIVOT.** Is there a covering system of ℤ with distinct moduli all in $H \setminus \{2\}$
> (equivalently, all of the form $(p-1)/2$ with $p \ge 7$ prime)?
>
> A **negative** answer proves Erdős 273 has answer **NO**. A positive answer is a finite
> certificate that removes the single biggest obstacle to **YES**.

State of the pivot after this run: the fiber test at threshold 1 (`experiments/M_pivot.py`)
**eliminates 91 of the 107 lattices $M \le 5580$** whose pool has budget $> 1$ (51 via $q=2$, 32
via $q=3$, 8 via $q=5$), reproducing route G's SAT-UNSAT results for $M \le 720$ instantly and
extending them far beyond. The 16 undecided lattices are
$1080, 1260, 1680, 2160, 2520, 3240, 3360, 3600, 3780, 3960, 4200, 4320, 4620, 4680, 5040, 5400$.
Deciding even $M = 1080$ exactly is hard: SAT solves $M=180$ in 0.9 s, $M=360$ in 10.5 s,
$M=720$ in 14.9 s, and does not finish $M=1080$ in hours — the UNSAT witness is a counting
argument, which resolution reproduces only exponentially.

**This elimination cannot close the problem, and must not be read as evidence that it will.**
$\Phi_q(S) \ge \sum_{m \in S,\ q \nmid m} 1/m$, so the test at $q$ is vacuous once that sub-budget
exceeds 1. Worse, route C checked the *first genuinely relevant* lattice directly and the test
**already fails there**: at $M = 27720$ the pool $H$-divisors $\setminus\{2\}$ satisfies
$\Phi_2, \Phi_3 \ge 1$ comfortably ($q=2$: the odd part alone gives 0.9605 per leaf against a
deficit of 0.0395 with supply 2.81; $q=3$: base 0.6192, deficit 0.3808, supply 6.5). So the long
run of kills up to $M = 5580$ does **not** continue — it is an artefact of small lattices being
budget-starved, not a trend. (My frontier estimate said the test *could* bite at 27720 since
$A_3 = 0.619 \le 1$; "can bite" is not "does bite", and I record the correction.)

Route C independently searched for an $H$-covering avoiding the modulus 2 at
$L = 360, 630, 660, 720, 810, 840, 900, 960, 990, 1260, 2520, 5040, 27720, 151200, 360360,
720720, 2162160, 10810800$ by three different methods and found **none** — search failure, which
per the problem's own ground rules is zero evidence for a negative answer.

**A further structural fact about $H$** (route C, verified independently): for every odd prime $q$,
$2m+1 \equiv 0 \pmod q \iff m \equiv (q-1)/2 \pmod q$, so $H$ meets that class only at the single
point $m = (q-1)/2$. Hence $H$ contains **no** $m \equiv 1 \pmod 3$ (equivalently $E$ contains no
$n \equiv 2 \pmod 6$), $H \cap \{m \equiv 2 \bmod 5\} = \{2\}$, and so on. This is exactly why the
moduli every cheap least-modulus-3 covering wants are unavailable: $4, 10 \equiv 1 \pmod 3$ and
$12 \equiv 2 \pmod 5$. It yields no obstruction, however: it constrains the *residue* of a modulus,
while covering feasibility depends only on the *divisibility lattice* of the chosen moduli.

## 3. Why neither branch closed — honest diagnosis

*The negative branch* has no available mechanism. Every standard tool is vacuous on $E$:
Hough ($\le 10^{16}$) and BBMST ($\le 616000$) bound the *least* modulus, and $\min E = 4$;
Hough–Nielsen ("some modulus divisible by 2 or 3") is automatic since all of $E$ is even;
the squarefree results do not apply. Budget arguments are dead by (T2). Local-at-fixed-$Q$
arguments are dead by (T7). Route D, chartered specifically to find an obstruction, proved instead
that its own chartered method cannot work.

*The affirmative branch* has no obstruction, only scale. Independent estimates agree: the cheapest
$H$-covering anyone found costs $\approx 1.354$–$1.43$ and the minima show **no downward trend**
(65/48 at $M = 288, 576, 864, 1152, 1728$), while two disjoint halves need pool budget
$> 2\times$ that. Pool budget grows like $2\log\log$, so the crossing point sits at
$\mathrm{lcm} \approx 10^{15}$–$10^{22}$ depending on which cheapest cost is used. Every search
method available caps out around $\mathrm{lcm} \lesssim 10^7$–$10^8$ (memory) and, for exact UNSAT,
around $10^4$–$10^5$ residues. **That is a gap of eight to fifteen orders of magnitude**, and it
is where routes A, B, C, F, G all broke.

Caveat on that estimate: no lower bound on the cost of an $H$-covering was proved. "$\mu_H \ge
65/48$" is pure measurement and must not enter any argument. (T6) explains why the known
cost-reducing mechanism is unavailable, but does not exclude others.

## 4. Corrections to the material supplied with the task

1. **PROMPT.md §4 and §7.10 name "Sawhney".** The author of the covering-systems papers is
   **Julian Sahasrabudhe**: Balister, Bollobás, Morris, **Sahasrabudhe**, Tiba, *On the Erdős
   covering problem: the density of the uncovered set*, Invent. Math. **228** (2022), 377–414.
   Verified independently at bibliographic level.
2. My own hand-written $H$-list in the wave-1 agent briefs **omitted 54** ($2\cdot54+1 = 109$ is
   prime; correspondingly $108 \in E$). `PROBLEM.md`'s list stops at 44 and is correct, and every
   agent recomputed $H$ itself, so no computation was affected. Caught by route G.

## 5. Independent-verification plan

- **Certificates.** `experiments/verify_certificate.py` re-checks any claimed system from scratch:
  admissibility of every modulus by *deterministic trial division* (cross-checked against sympy),
  pairwise distinctness, and coverage by **both** a full mod-$L$ sweep and an exact
  class-elimination argument that terminates with an empty uncovered set. Tested on negative
  controls (a non-covering, and a system using the forbidden moduli 2 and 3).
- **Lean sketch (for a future YES).** The target is `ErdosProblems/273.lean`'s
  `StrictCoveringSystem ℤ`. A certificate $\{(a_i,n_i)\}_{i\le k}$ formalises as a `Finset`, with:
  `injective_moduli` from `decide` on pairwise distinctness; each ideal $\ne 0, \ne \top$ from
  $n_i \ge 4$; the modulus condition $\exists p, p.Prime \wedge 5 \le p \wedge n_i = p-1$ by
  `norm_num` on each $n_i + 1$; and the covering property by `Decidable` evaluation over
  `ZMod L`, i.e. `decide (∀ r : ZMod L, ∃ i, ...)`, feasible only for small $L$ — for large $L$ one
  instead formalises the CRT/class-elimination argument.
- **Lean sketch (for a future NO).** `∀ (S : Finset ℕ), (∀ n ∈ S, n ∈ E) → ∀ a : ℕ → ℤ,
  ∃ x : ℤ, ∀ n ∈ S, ¬ (x ≡ a n [ZMOD n])`. None of the partial results above formalises to this;
  they all quantify over a *fixed* lcm.
- **Reproduction.** `experiments/e_basics.py`, `M_lattice_scan.py`, `M_cost_infimum.py`,
  `M_parity_split.py`, `M_audit_phi.py`, `M_audit_A2A3.py`, `M_pivot.py`, `M_eliminate.py`,
  `M_A2plus.py` are deterministic and exact (`Fraction`, integer arithmetic, no floats near any
  boundary that feeds a proof).

## 6. Highest-value next steps

1. Decide the 16 surviving pivot lattices exactly. A certificate there would be the single biggest
   advance available; each UNSAT is a rigorous lemma.
2. Prove *any* lower bound on the reciprocal cost of a covering with distinct moduli drawn from
   $H$ (or from $E$). This is the one missing ingredient that would turn the measured budget
   squeeze into a real theorem, and it appears to be new mathematics.
3. Route D's unfinished computation: decide $\Phi_{\{2,3\}}(S) < 2$ exactly at $L_H = 720720$
   (the pair condition is strictly stronger than any single prime; a confirmation would push the
   lcm bound past $2 \cdot 10^6$). Needs a pseudo-Boolean/ILP solver, which was unavailable here.
4. Replace flat SAT entirely by fiber elimination plus targeted search on survivors — measured to
   be many orders of magnitude more effective.
