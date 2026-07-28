# Lemma M3 — the parity-split equivalence (both directions, proved)

Throughout, a *covering system* is a finite list of classes $a_i \pmod{n_i}$, $1<n_1<\dots<n_k$
(pairwise distinct moduli, all $>1$), with $\bigcup_i (a_i+n_i\mathbb Z)=\mathbb Z$. Put
$$E=\{p-1: p\ \text{prime},\ p\ge5\}=\{n\ge4: n+1\ \text{prime}\},\qquad
H=\{m\ge2: 2m+1\ \text{prime}\}=\tfrac12 E .$$
Note $n\mapsto n/2$ is a bijection $E\to H$: every $n\in E$ is even (as $n+1$ is an odd prime),
and $n=2m$ with $n+1=2m+1$ prime and $n\ge4 \iff m\ge2$. Both sets are infinite.

**Lemma M3.** The following are equivalent.
 (i) There is a covering system with all moduli in $E$.
 (ii) There are two **disjoint** finite sets $M_0,M_1\subseteq H$ such that for each $j\in\{0,1\}$
      there is a covering system of $\mathbb Z$ whose set of moduli is exactly $M_j$.

## Proof

### (i) ⟹ (ii)
Let $\{a_i \bmod n_i\}_{i\le k}$ be a covering system with every $n_i\in E$; write $n_i=2m_i$,
$m_i\in H$, and the $m_i$ are pairwise distinct because the $n_i$ are.

Fix $j\in\{0,1\}$ and set $I_j=\{i: a_i\equiv j \pmod 2\}$, $M_j=\{m_i : i\in I_j\}$.
Since each $i$ lies in exactly one $I_j$ (the parity of $a_i$ is well defined mod 2, and $n_i$ is
even so $a_i+n_i\mathbb Z$ consists solely of integers $\equiv a_i \bmod 2$), the sets $I_0,I_1$
partition $\{1,\dots,k\}$ and hence $M_0\cap M_1=\varnothing$. Both are finite; within each $M_j$
the moduli are distinct.

*Claim: for each $j$, $\{\,b_i \bmod m_i : i\in I_j\,\}$ covers $\mathbb Z$, where $b_i:=(a_i-j)/2$
(an integer, since $a_i\equiv j \bmod 2$).*
Let $y\in\mathbb Z$ be arbitrary and put $x=2y+j$. As the original system covers $\mathbb Z$, there
is $i$ with $x\equiv a_i \pmod{2m_i}$. Then $x\equiv a_i\pmod 2$, and $x\equiv j \pmod 2$, so
$a_i\equiv j\pmod 2$, i.e. $i\in I_j$. Now
$$2y+j\equiv a_i \pmod{2m_i}\iff 2y+j-a_i\in 2m_i\mathbb Z \iff 2(y-b_i)\in2m_i\mathbb Z
\iff y\equiv b_i \pmod{m_i},$$
using $a_i=2b_i+j$. Hence $y$ is covered. Since $y$ was arbitrary — **including every negative
integer**, the argument uses no positivity — the claim holds. Each $m_i>1$ (indeed $m_i\ge2$), so
each is a genuine covering system with modulus set $M_j$.

(If some $I_j$ were empty, then no class covers the integers of parity $j$ at all, contradicting
that the original system covers $\mathbb Z$; so both $M_j$ are nonempty.)

### (ii) ⟹ (i)
For $j\in\{0,1\}$ let $\{b^{(j)}_m \bmod m\}_{m\in M_j}$ be a covering system of $\mathbb Z$ with
modulus set exactly $M_j$. Define, for $m\in M_j$,
$$n:=2m\in E,\qquad a:=2b^{(j)}_m+j .$$
Consider the finite list $\mathcal S=\{\,a \bmod n\,\}$ over all $m\in M_0\cup M_1$.
*Moduli.* Each $n=2m$ with $m\in H$ lies in $E$. They are pairwise distinct: within one $M_j$
because the $m$ are; across the two because $M_0\cap M_1=\varnothing$. All exceed $1$, and the
list is finite.
*Covering.* Let $x\in\mathbb Z$ and let $j\in\{0,1\}$ be its parity, $x=2y+j$. Since $M_j$'s system
covers $\mathbb Z$ there is $m\in M_j$ with $y\equiv b^{(j)}_m \pmod m$; then
$x=2y+j\equiv 2b^{(j)}_m+j = a \pmod{2m}$. So $x$ is covered. $\square$

## Bookkeeping note (the trap)

In $H$-units each $M_j$ needs $\sum_{m\in M_j}1/m>1$. Translating, $\sum_{n\in S_j}1/n>1/2$ where
$S_j=2M_j\subseteq E$; summing over $j=0,1$ gives exactly the ordinary requirement
$\sum_{n}1/n>1$ for the $E$-system. **There is no doubling of the $E$-budget requirement.**
Equivalently: $B_H(Y)=2\,B_E(2Y)$, so "each half needs $>1$ in $H$-units" and "the whole needs
$>1$ in $E$-units" are the same statement. (I made this slip once early in the session and it
inflated the apparent difficulty by a factor of two; it is corrected here and in NOTES.md.)

## Consequences actually used

* $2,3\in H$ (since $5,7$ are prime) and each may be used by **at most one** of $M_0,M_1$. Hence at
  least one of the two subsystems has least modulus $\ge3$, and at least one has least modulus
  $\ge 4$ unless it uses $3$. Note $4\notin H$ ($9=3^2$) and $7,10,12,13\notin H$.
* A covering system with **all** moduli odd and distinct would solve the Erdős–Selfridge odd
  covering problem, which is open. Therefore any construction that forces one of $M_0,M_1$ to
  consist of odd moduli only is a dead end and must be rejected on sight.

## Verification

`experiments/M_parity_split.py` tests both directions computationally on explicit examples: it
takes the verified $H$-covering with modulus set $\{2,3,5,6,9,15,18,20,30,36,90\}$, lifts it by
(ii)⟹(i) to a system of classes with moduli in $E$ covering exactly one parity class, and checks
by a full mod-$L$ sweep that precisely the integers of that parity are covered; and it takes a
random $E$-system, splits it by (i)⟹(ii), and checks that each half covers $\mathbb Z$.
