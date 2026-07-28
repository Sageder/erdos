# PROBLEM.md — Erdős Problem 273 (immutable; written once at session start)

## Statement

All numbers are integers; "prime" means a positive rational prime. For $a\in\mathbb Z$ and
$n\ge 1$ the residue class $a \bmod n$ is the two-sided set $a+n\mathbb Z$.

**Covering system (governing definition).** A covering system is a *finite* list of residue
classes $a_1 \pmod{n_1},\dots,a_k \pmod{n_k}$, $k\ge 1$, with integer residues $a_i$ and moduli
satisfying $1 < n_1 < n_2 < \cdots < n_k$, such that $\bigcup_{i=1}^k (a_i+n_i\mathbb Z)=\mathbb Z$.
Binding conventions: (i) finite; (ii) moduli pairwise DISTINCT; (iii) every modulus $>1$.
Overlaps are allowed; every integer must be covered.

**Admissible moduli.**
$$E:=\{p-1:\ p\ \text{prime},\ p\ge 5\}=\{4,6,10,12,16,18,22,28,30,36,40,42,46,52,58,60,66,70,\dots\}.$$
Membership test: $n\in E$ iff $n\ge 4$ and $n+1$ is prime. All elements of $E$ are even.

**Problem (erdosproblems.com/273, verbatim; this governs):** "Is there a covering system all of
whose moduli are of the form $p-1$ for some primes $p\ge 5$?"  (Erdős–Graham [ErGr80, p. 24].)

**Lean cross-check** (google-deepmind/formal-conjectures, `ErdosProblems/273.lean`):
$\exists\,c:\mathrm{StrictCoveringSystem}\ \mathbb Z$ with every modulus ideal equal to
$(p-1)\mathbb Z$ for a prime $p\ge5$. `StrictCoveringSystem` = finite-index family of cosets of
ideals of $\mathbb Z$, union $=\mathbb Z$, every ideal $\ne 0$ and $\ne\mathbb Z$, moduli map
injective. Site and Lean statements agree in every respect. The $p\ge3$ variant (Selfridge,
solved) is NOT this problem.

**Conventions.** Residues are unrestricted integers. A finite union of residue classes is
periodic mod $L=\mathrm{lcm}(n_1,\dots,n_k)$; hence "covers $\mathbb Z$" $\iff$ "covers
$\{0,\dots,L-1\}$" $\iff$ "covers all sufficiently large positive integers". The mod-$L$ sweep is
the canonical finite verification.

## What a complete resolution must establish

Exactly one of:

**YES.** Exhibit $k\ge1$, moduli $n_1<\cdots<n_k$ all in $E$, residues $a_1,\dots,a_k$, and prove
$\bigcup_i(a_i+n_i\mathbb Z)=\mathbb Z$. Certificate must ship with (i) primality verification of
every $n_i+1$; (ii) a distinctness check; (iii) an exhaustive mod-$L$ coverage verification in
exact integer arithmetic by an independent script in `experiments/`.

**NO.** Prove: for every $k\ge1$, every choice of distinct $n_1<\cdots<n_k$ from $E$, and every
choice of residues, some integer is uncovered. Equivalently: for every finite $S\subseteq E$ and
every residue assignment the uncovered set is nonempty (hence of density $\ge 1/\mathrm{lcm}(S)$).

**Quantifier order.** YES is purely existential — one finite object, decidable by finite
computation, so machine search is a legitimate complete proof strategy. NO is universal over
infinitely many finite subsets of the infinite set $E$ and over all residue assignments; no finite
enumeration establishes it. Failure to find certificates is zero evidence for NO; a heuristic that
a certificate "should exist" is zero evidence for YES.
